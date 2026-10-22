"""Read-only schema dump of the BMP Database for the integration phase.

Connects to the SQL Server database with pyodbc, reads INFORMATION_SCHEMA and the
catalog views, and writes a data dictionary draft (markdown and JSON) plus the
view, procedure, and function definitions. Nothing is written to the database.

Run from arcgispro-py3, from the qa/bmp folder:

    "C:\\Program Files\\ArcGIS\\Pro\\bin\\Python\\envs\\arcgispro-py3\\python.exe" scripts/dump_bmp_schema.py
    ... --samples      also list the distinct values of short code-like columns
    ... --out PATH     output folder (default docs/bmp-database)

Connection settings come from scripts/.env (gitignored; see scripts/.env.example)
or the environment:

    BMP_DB_SERVER      host, or host\\instance, or host,port
    BMP_DB_DATABASE    database name
    BMP_DB_USER        leave blank for Windows authentication
    BMP_DB_PASSWORD
    BMP_DB_DRIVER      optional, default "ODBC Driver 17 for SQL Server"

The output names tables, columns, keys, views, and procedures and gives row
counts. It never records the server name or credentials. The repo is public, so
review the output before committing it.
"""
import argparse
import json
import logging
import os
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

import pyodbc
from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
log = logging.getLogger("dump_bmp_schema")

# Columns whose values are personal data are never sampled, whatever their size.
PRIVATE = re.compile(r"name|owner|mail|email|phone|address|addr|street|contact|user|pass|login|agent|note|comment", re.I)
SAMPLE_MAX_DISTINCT = 25
SAMPLE_TEXT_TYPES = {"char", "nchar", "varchar", "nvarchar", "bit", "tinyint", "smallint", "int"}


def connect():
    load_dotenv(HERE / ".env")
    server = os.environ.get("BMP_DB_SERVER", "").strip()
    database = os.environ.get("BMP_DB_DATABASE", "").strip()
    driver = os.environ.get("BMP_DB_DRIVER", "ODBC Driver 17 for SQL Server").strip()
    user = os.environ.get("BMP_DB_USER", "").strip()
    password = os.environ.get("BMP_DB_PASSWORD", "")
    if not server or not database:
        sys.exit("Set BMP_DB_SERVER and BMP_DB_DATABASE in scripts/.env (see scripts/.env.example).")
    auth = f"UID={user};PWD={password};" if user else "Trusted_Connection=yes;"
    conn = pyodbc.connect(
        f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};{auth}ApplicationIntent=ReadOnly;",
        autocommit=True, readonly=True, timeout=30,
    )
    # Catalog reads only; this keeps the dump from waiting on anyone's open transaction.
    conn.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
    log.info("connected to database %s (server name not recorded)", database)
    return conn, database


def rows(conn, sql, *params):
    cur = conn.execute(sql, *params)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def read_schema(conn):
    tables = rows(conn, """
        SELECT TABLE_SCHEMA AS [schema], TABLE_NAME AS [name], TABLE_TYPE AS [type]
        FROM INFORMATION_SCHEMA.TABLES ORDER BY TABLE_TYPE, TABLE_SCHEMA, TABLE_NAME""")
    columns = rows(conn, """
        SELECT TABLE_SCHEMA AS [schema], TABLE_NAME AS [table], COLUMN_NAME AS [name], ORDINAL_POSITION AS [position],
               DATA_TYPE AS [type], CHARACTER_MAXIMUM_LENGTH AS [length], NUMERIC_PRECISION AS [precision],
               NUMERIC_SCALE AS [scale], IS_NULLABLE AS [nullable], COLUMN_DEFAULT AS [default]
        FROM INFORMATION_SCHEMA.COLUMNS ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION""")
    counts = rows(conn, """
        SELECT s.name AS [schema], t.name AS [table], SUM(p.rows) AS [rows]
        FROM sys.tables t
        JOIN sys.schemas s ON s.schema_id = t.schema_id
        JOIN sys.partitions p ON p.object_id = t.object_id AND p.index_id IN (0, 1)
        GROUP BY s.name, t.name""")
    keys = rows(conn, """
        SELECT tc.TABLE_SCHEMA AS [schema], tc.TABLE_NAME AS [table], tc.CONSTRAINT_TYPE AS [kind],
               tc.CONSTRAINT_NAME AS [constraint], kcu.COLUMN_NAME AS [column], kcu.ORDINAL_POSITION AS [position]
        FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
        JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
          ON kcu.CONSTRAINT_NAME = tc.CONSTRAINT_NAME AND kcu.TABLE_SCHEMA = tc.TABLE_SCHEMA AND kcu.TABLE_NAME = tc.TABLE_NAME
        WHERE tc.CONSTRAINT_TYPE IN ('PRIMARY KEY', 'UNIQUE', 'FOREIGN KEY')
        ORDER BY tc.TABLE_SCHEMA, tc.TABLE_NAME, tc.CONSTRAINT_NAME, kcu.ORDINAL_POSITION""")
    foreign = rows(conn, """
        SELECT fk.name AS [constraint],
               OBJECT_SCHEMA_NAME(fk.parent_object_id) AS [schema], OBJECT_NAME(fk.parent_object_id) AS [table],
               COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS [column],
               OBJECT_SCHEMA_NAME(fk.referenced_object_id) AS [ref_schema], OBJECT_NAME(fk.referenced_object_id) AS [ref_table],
               COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS [ref_column]
        FROM sys.foreign_keys fk
        JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id
        ORDER BY 2, 3, 1, fkc.constraint_column_id""")
    try:
        indexes = rows(conn, """
        SELECT s.name AS [schema], t.name AS [table], i.name AS [index], i.type_desc AS [kind], i.is_unique AS [unique],
               STRING_AGG(c.name, ', ') WITHIN GROUP (ORDER BY ic.key_ordinal) AS [columns]
        FROM sys.indexes i
        JOIN sys.tables t ON t.object_id = i.object_id
        JOIN sys.schemas s ON s.schema_id = t.schema_id
        JOIN sys.index_columns ic ON ic.object_id = i.object_id AND ic.index_id = i.index_id AND ic.is_included_column = 0
        JOIN sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id
        WHERE i.name IS NOT NULL
        GROUP BY s.name, t.name, i.name, i.type_desc, i.is_unique
        ORDER BY 1, 2, 3""")
    except pyodbc.Error as e:  # STRING_AGG needs SQL Server 2017 or later
        log.warning("index listing skipped: %s", str(e)[:120])
        indexes = []
    modules = rows(conn, """
        SELECT OBJECT_SCHEMA_NAME(m.object_id) AS [schema], OBJECT_NAME(m.object_id) AS [name], o.type_desc AS [kind],
               o.modify_date AS [modified], m.definition AS [definition]
        FROM sys.sql_modules m
        JOIN sys.objects o ON o.object_id = m.object_id
        ORDER BY o.type_desc, 1, 2""")
    triggers = rows(conn, """
        SELECT OBJECT_SCHEMA_NAME(t.parent_id) AS [schema], OBJECT_NAME(t.parent_id) AS [table], t.name AS [trigger],
               t.is_disabled AS [disabled]
        FROM sys.triggers t WHERE t.parent_class = 1 ORDER BY 1, 2, 3""")
    return {"tables": tables, "columns": columns, "counts": counts, "keys": keys, "foreign_keys": foreign,
            "indexes": indexes, "modules": modules, "triggers": triggers}


def sample_values(conn, schema):
    """Distinct values of short code-like columns, so status codes and flags are known. Skips personal data."""
    samples = {}
    for c in schema["columns"]:
        if c["type"] not in SAMPLE_TEXT_TYPES or PRIVATE.search(c["name"]):
            continue
        if c["type"] in ("varchar", "nvarchar", "char", "nchar") and (c["length"] or 0) > 20 and c["length"] != -1:
            continue
        if c["length"] == -1:
            continue
        qualified = f"[{c['schema']}].[{c['table']}]"
        try:
            n = conn.execute(f"SELECT COUNT(DISTINCT [{c['name']}]) FROM {qualified}").fetchone()[0]
            if n is None or n > SAMPLE_MAX_DISTINCT:
                continue
            vals = conn.execute(
                f"SELECT TOP {SAMPLE_MAX_DISTINCT} [{c['name']}], COUNT(*) FROM {qualified} GROUP BY [{c['name']}] ORDER BY COUNT(*) DESC"
            ).fetchall()
            samples[f"{c['schema']}.{c['table']}.{c['name']}"] = [[str(v), int(k)] for v, k in vals]
        except pyodbc.Error as e:
            log.warning("could not sample %s.%s: %s", c["table"], c["name"], e)
    return samples


def write_outputs(schema, samples, database, out):
    out.mkdir(parents=True, exist_ok=True)
    (out / "schema.json").write_text(json.dumps({"database": database, "dumped": date.today().isoformat(), **schema,
                                                 "samples": samples}, indent=1, default=str), encoding="utf-8")
    with (out / "modules.sql").open("w", encoding="utf-8") as f:
        f.write(f"-- {database}: view, procedure, function, and trigger definitions, dumped {date.today()}\n")
        for m in schema["modules"]:
            f.write(f"\n-- ===== {m['kind']} {m['schema']}.{m['name']} (modified {m['modified']}) =====\n{m['definition']}\nGO\n")

    counts = {(c["schema"], c["table"]): c["rows"] for c in schema["counts"]}
    cols = defaultdict(list)
    for c in schema["columns"]:
        cols[(c["schema"], c["table"])].append(c)
    keycols = defaultdict(list)
    for k in schema["keys"]:
        keycols[(k["schema"], k["table"], k["column"])].append("PK" if k["kind"] == "PRIMARY KEY" else "UQ" if k["kind"] == "UNIQUE" else "FK")
    fks = defaultdict(list)
    for f in schema["foreign_keys"]:
        fks[(f["schema"], f["table"], f["column"])].append(f"{f['ref_table']}.{f['ref_column']}")

    lines = [f"# {database}: schema dump", "",
             f"Dumped {date.today()} by `scripts/dump_bmp_schema.py` (read-only). Data dictionary draft for the integration phase; "
             "add the meaning of each table and column, then move the result into `bmp-database.md`.", ""]
    for kind, title in (("BASE TABLE", "Tables"), ("VIEW", "Views")):
        lines += [f"## {title}", ""]
        for t in [t for t in schema["tables"] if t["type"] == kind]:
            key = (t["schema"], t["name"])
            n = counts.get(key)
            lines += [f"### {t['schema']}.{t['name']}" + (f" ({n:,} rows)" if n is not None else ""), "",
                      "| Column | Type | Null | Key | Default | Meaning |", "|---|---|---|---|---|---|"]
            for c in cols[key]:
                typ = c["type"]
                if c["length"]:
                    typ += "(max)" if c["length"] == -1 else f"({c['length']})"
                elif c["type"] in ("decimal", "numeric"):
                    typ += f"({c['precision']},{c['scale']})"
                keys = ", ".join(keycols.get((t["schema"], t["name"], c["name"]), []))
                refs = ", ".join(fks.get((t["schema"], t["name"], c["name"]), []))
                if refs:
                    keys = f"{keys if 'FK' in keys else (keys + ' FK').strip()} to {refs}".strip()
                sample = samples.get(f"{t['schema']}.{t['name']}.{c['name']}")
                meaning = ("values: " + "; ".join(f"{v} ({k})" for v, k in sample[:8])) if sample else ""
                lines.append(f"| {c['name']} | {typ} | {'yes' if c['nullable'] == 'YES' else 'no'} | {keys} | "
                             f"{(c['default'] or '').strip()} | {meaning} |")
            idx = [i for i in schema["indexes"] if (i["schema"], i["table"]) == key]
            if idx:
                lines += ["", "Indexes: " + "; ".join(f"{i['index']} ({i['columns']}{', unique' if i['unique'] else ''})" for i in idx)]
            trg = [x for x in schema["triggers"] if (x["schema"], x["table"]) == key]
            if trg:
                lines += ["", "Triggers: " + ", ".join(f"{x['trigger']}{' (disabled)' if x['disabled'] else ''}" for x in trg)]
            lines.append("")
    procs = [m for m in schema["modules"] if m["kind"] not in ("VIEW",)]
    lines += ["## Procedures, functions, and triggers", "", "Definitions are in `modules.sql`.", ""]
    lines += [f"- {m['kind'].lower().replace('_', ' ')} `{m['schema']}.{m['name']}` (modified {str(m['modified'])[:10]})" for m in procs]
    lines.append("")
    (out / "schema.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", default=str(ROOT / "docs" / "bmp-database"), help="output folder")
    ap.add_argument("--samples", action="store_true", help="list distinct values of short code-like columns (skips personal data)")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    conn, database = connect()
    schema = read_schema(conn)
    log.info("%d tables and views, %d columns, %d modules", len(schema["tables"]), len(schema["columns"]), len(schema["modules"]))
    samples = sample_values(conn, schema) if args.samples else {}
    if samples:
        log.info("sampled %d code-like columns", len(samples))
    conn.close()
    out = Path(args.out)
    write_outputs(schema, samples, database, out)
    log.info("wrote %s, %s, %s", out / "schema.md", out / "schema.json", out / "modules.sql")


if __name__ == "__main__":
    main()
