"""Create and seed the hosted table behind EIP Priority Lists (qa/eip/priority-lists.html).

The table holds one row per change to one project on one working group's list. Rows are
only ever added; for each (list, working group, project) the newest row wins, and a row
with tier 0 takes the project off the list. The page reads the table anonymously and adds
rows anonymously, so the service needs Create and Query only, no Update or Delete.

Fields: fy, listkey, wg, eip, project, tier, request, criteria, note, who, agency, source,
plus editor tracking (CreationDate is the clock the page sorts by).

Run with the ArcGIS Pro environment, signed in to TRPA's ArcGIS Online in Pro:

  "%ProgramFiles%\\ArcGIS\\Pro\\bin\\Python\\envs\\arcgispro-py3\\python.exe" scripts\\eip_priority_lists_table.py --create
  ... --seed --dry-run                      show the FY27 baseline the survey would give
  ... --seed                                write the baseline rows (survey, newest list per group)
  ... --seed --sheet "FY27 master sheet.xlsx"   also load last year's master sheet (survey rows win)

Then paste the printed table URL into TABLE.url in qa/eip/priority-lists.html. Sharing:
the script shares the item with everyone; check Settings on the item in ArcGIS Online
if adds from the page fail.
"""
import argparse
import re
import sys
from datetime import datetime, timezone

SERVICE_NAME = "EIP_Priority_Lists"
TITLE = "EIP Priority Lists"
SURVEY_VIEW = ("https://services5.arcgis.com/fXXSUzHD5JjcOt1v/arcgis/rest/services/"
               "EIP_Funding_Priorities_picks_public_view/FeatureServer/0")
SURVEY_ROUND = "FY28"          # the round tag on the survey records being treated as the baseline
BASELINE_FY = "FY27"           # what those records become in the new table
CURRENT_FY = "FY28"

WORKING_GROUPS = [
    "Tahoe Fire and Fuels Team",
    "Water Infrastructure for Fire Suppression Working Group",
    "Stormwater Quality Improvement Committee",
    "Tahoe Watershed Improvement Group",
    "Aquatic Invasive Species Coordinating Committee",
    "Tahoe Basin Recovery Implementation Team (LCT)",
    "Recreation Infrastructure Action Team",
    "EIP Coordinating Committee (Accountability)",
]
# Sheet tabs and column values that name a group in fewer words
WG_ALIASES = {
    "tfft": WORKING_GROUPS[0], "fire and fuels": WORKING_GROUPS[0], "forest health": WORKING_GROUPS[0],
    "water infrastructure": WORKING_GROUPS[1], "wifs": WORKING_GROUPS[1],
    "swqic": WORKING_GROUPS[2], "stormwater": WORKING_GROUPS[2],
    "twig": WORKING_GROUPS[3], "watershed": WORKING_GROUPS[3],
    "ais": WORKING_GROUPS[4], "aquatic": WORKING_GROUPS[4],
    "lct": WORKING_GROUPS[5], "cutthroat": WORKING_GROUPS[5],
    "recreation": WORKING_GROUPS[6],
    "accountability": WORKING_GROUPS[7], "eipcc": WORKING_GROUPS[7],
}
CRITERIA_KEYS = {  # criteria short names as the tool writes them, to the keys the page stores
    "measurable progress": "measure", "threshold contribution": "contrib", "multiple benefits": "multi",
    "non-federal leverage": "leverage", "stakeholder support": "support", "federal nexus": "federal",
    "agency capacity": "capacity", "federal funding history": "history", "nhpa compliance": "nhpa", "esa compliance": "esa",
}
EIP_ID = re.compile(r"\d{2}\.\d{2}\.\d{2}\.\d{4}")
PICK_LINE = re.compile(r"^\s*(LTRA|Other)\b.*?\bP([123])\b(?:\s*\$\s*([\d,]+(?:\.\d+)?)\s*([MK])?)?\s*(\d{2}\.\d{2}\.\d{2}\.\d{4})\s*(.*)$", re.I)

TABLE_DEF = {
    "name": "picks", "type": "Table", "displayField": "project",
    "description": "One row per change to one project on one working group's EIP priority list; newest row wins.",
    "capabilities": "Create,Query", "hasAttachments": False, "isDataVersioned": False, "supportsRollbackOnFailure": True,
    "objectIdField": "OBJECTID",
    "editFieldsInfo": {"creationDateField": "CreationDate", "creatorField": "Creator", "editDateField": "EditDate", "editorField": "Editor"},
    "fields": [
        {"name": "OBJECTID", "type": "esriFieldTypeOID", "alias": "OBJECTID", "nullable": False, "editable": False},
        {"name": "fy", "type": "esriFieldTypeString", "alias": "Fiscal year", "length": 16, "nullable": True, "editable": True},
        {"name": "listkey", "type": "esriFieldTypeString", "alias": "List (ltra or other)", "length": 8, "nullable": True, "editable": True},
        {"name": "wg", "type": "esriFieldTypeString", "alias": "Working group", "length": 120, "nullable": True, "editable": True},
        {"name": "eip", "type": "esriFieldTypeString", "alias": "EIP project number", "length": 20, "nullable": True, "editable": True},
        {"name": "project", "type": "esriFieldTypeString", "alias": "Project name", "length": 255, "nullable": True, "editable": True},
        {"name": "tier", "type": "esriFieldTypeSmallInteger", "alias": "Priority (0 removes)", "nullable": True, "editable": True},
        {"name": "request", "type": "esriFieldTypeDouble", "alias": "Request (dollars)", "nullable": True, "editable": True},
        {"name": "criteria", "type": "esriFieldTypeString", "alias": "LTRA criteria keys", "length": 255, "nullable": True, "editable": True},
        {"name": "note", "type": "esriFieldTypeString", "alias": "Note", "length": 4000, "nullable": True, "editable": True},
        {"name": "who", "type": "esriFieldTypeString", "alias": "Changed by", "length": 120, "nullable": True, "editable": True},
        {"name": "agency", "type": "esriFieldTypeString", "alias": "Agency", "length": 120, "nullable": True, "editable": True},
        {"name": "source", "type": "esriFieldTypeString", "alias": "Source (survey, master-sheet, tool)", "length": 32, "nullable": True, "editable": True},
        {"name": "CreationDate", "type": "esriFieldTypeDate", "alias": "CreationDate", "nullable": True, "editable": False},
        {"name": "Creator", "type": "esriFieldTypeString", "alias": "Creator", "length": 128, "nullable": True, "editable": False},
        {"name": "EditDate", "type": "esriFieldTypeDate", "alias": "EditDate", "nullable": True, "editable": False},
        {"name": "Editor", "type": "esriFieldTypeString", "alias": "Editor", "length": 128, "nullable": True, "editable": False},
    ],
}
EDITOR_TRACKING = {"enableEditorTracking": True, "enableOwnershipAccessControl": False, "allowOthersToQuery": True,
                   "allowOthersToUpdate": False, "allowOthersToDelete": False, "allowAnonymousToQuery": True,
                   "allowAnonymousToUpdate": False, "allowAnonymousToDelete": False}


def log(msg):
    print(msg, flush=True)


def connect(user):
    from arcgis.gis import GIS
    if user:
        import getpass
        return GIS("https://www.arcgis.com", user, getpass.getpass(f"ArcGIS Online password for {user}: "))
    return GIS("pro")


def find_table(gis):
    hits = gis.content.search(f'title:"{TITLE}" AND owner:{gis.users.me.username}', item_type="Feature Service")
    for it in hits:
        if it.title == TITLE:
            return it
    return None


def create(gis):
    from arcgis.features import FeatureLayerCollection
    item = find_table(gis)
    if item:
        log(f"Table already exists: {item.homepage}")
        return item
    item = gis.content.create_service(name=SERVICE_NAME, service_type="featureService", has_static_data=False,
                                      capabilities="Create,Query", item_properties={"title": TITLE, "snippet": TABLE_DEF["description"]},
                                      tags=["EIP", "LTRA", "priorities", "TRPA Tools"])
    flc = FeatureLayerCollection.fromitem(item)
    flc.manager.add_to_definition({"tables": [TABLE_DEF]})
    flc.manager.update_definition({"capabilities": "Create,Query", "editorTrackingInfo": EDITOR_TRACKING, "allowGeometryUpdates": False})
    item.share(everyone=True)
    log(f"Created {item.homepage}")
    return item


def table_of(item):
    from arcgis.features import FeatureLayerCollection
    return FeatureLayerCollection.fromitem(item).tables[0]


def parse_money(s):
    if s is None:
        return None
    m = re.match(r"\$?\s*(\d+(?:\.\d+)?)\s*([MmKk])?", str(s).replace(",", "").strip())
    if not m:
        return None
    return float(m.group(1)) * (1e6 if (m.group(2) or "").lower() == "m" else 1e3 if (m.group(2) or "").lower() == "k" else 1)


def survey_baseline():
    """Newest survey record per working group, parsed into rows. Older records for the same group are reported, not merged."""
    import requests
    feats, offset = [], 0
    while True:
        r = requests.get(f"{SURVEY_VIEW}/query", params={"where": f"funding_round_filled_in_by_the='{SURVEY_ROUND}'", "outFields": "*",
                                                        "orderByFields": "CreationDate DESC", "resultOffset": offset, "resultRecordCount": 1000, "f": "json"}, timeout=60).json()
        feats += r.get("features", [])
        if not r.get("exceededTransferLimit"):
            break
        offset += 1000
    newest, dropped = {}, []
    for f in feats:  # already newest first
        a = f["attributes"]
        text = a.get("picks_text") or a.get("your_ranked_picks_project_numbe") or ""
        lines = text.split("\n")
        m = re.match(r"\s*Working group:\s*(.+)", lines[0]) if lines else None
        wg = m.group(1).strip() if m else ""
        if not wg or wg.startswith("Other"):
            continue
        if wg in newest:
            dropped.append((wg, a.get("reviewer_name"), a.get("CreationDate")))
            continue
        notes = {}
        for ln in (a.get("notes_text") or a.get("notes") or "").split("\n"):
            nm = re.match(r"\s*(\d{2}\.\d{2}\.\d{2}\.\d{4})\s*:\s*(.*)$", ln)
            if nm:
                notes[nm.group(1)] = nm.group(2).strip()
        rows = []
        for ln in lines[1:]:
            pm = PICK_LINE.match(ln)
            if not pm:
                continue
            listkey, tier, amt, unit, eip, name = pm.groups()
            req = parse_money(f"{amt}{unit or ''}") if amt else None
            note = notes.get(eip, "")
            crit = []
            cm = re.match(r"\s*Criteria addressed:\s*([^.]*)\.?\s*(.*)$", note, re.I | re.S)
            if cm:
                crit = [CRITERIA_KEYS[k] for k in (x.strip().lower() for x in cm.group(1).split(",")) if k in CRITERIA_KEYS]
                if crit:
                    note = cm.group(2).strip()
            rows.append({"fy": BASELINE_FY, "listkey": listkey.lower(), "wg": wg, "eip": eip, "project": name.strip()[:255], "tier": int(tier),
                         "request": req, "criteria": ",".join(crit), "note": note[:4000], "who": a.get("reviewer_name") or "", "agency": a.get("agency") or "", "source": "survey"})
        newest[wg] = {"who": a.get("reviewer_name"), "when": a.get("CreationDate"), "rows": rows}
    return newest, dropped


def sheet_rows(path):
    """Last year's master sheet as rows: one tab per group, or a Working group column. Columns are matched by name."""
    import pandas as pd
    frames = pd.read_excel(path, sheet_name=None, dtype=str) if path.lower().endswith((".xlsx", ".xls", ".xlsm")) else {"": pd.read_csv(path, dtype=str)}
    out = []
    for tab, df in frames.items():
        df.columns = [str(c).strip().lower() for c in df.columns]
        col = lambda *names: next((c for c in df.columns if any(n in c for n in names)), None)
        c_id, c_t, c_q, c_n, c_w = col("tracker #", "project #", "eip #", "project number"), col("priority"), col("request"), col("note"), col("working group")
        if not c_id or not c_t:
            log(f"  skipping tab {tab!r}: no project number or priority column")
            continue
        for _, r in df.iterrows():
            idm = EIP_ID.search(str(r.get(c_id, "")))
            tier = re.search(r"[123]", str(r.get(c_t, "")))
            if not idm or not tier:
                continue
            wg_raw = (str(r.get(c_w, "")) if c_w else tab).strip().lower()
            wg = next((v for k, v in WG_ALIASES.items() if k in wg_raw), None) or next((g for g in WORKING_GROUPS if g.lower() == wg_raw), None)
            if not wg:
                log(f"  no working group match for {wg_raw!r}; row for {idm.group(0)} skipped")
                continue
            out.append({"fy": BASELINE_FY, "listkey": "ltra", "wg": wg, "eip": idm.group(0), "project": "", "tier": int(tier.group(0)),
                        "request": parse_money(r.get(c_q)) if c_q else None, "criteria": "", "note": (str(r.get(c_n, "")) if c_n else "").strip()[:4000],
                        "who": "FY27 master sheet", "agency": "", "source": "master-sheet"})
    return out


def seed(item, sheet, dry_run):
    newest, dropped = survey_baseline()
    survey_rows = [r for g in newest.values() for r in g["rows"]]
    extra = sheet_rows(sheet) if sheet else []
    log(f"Survey baseline: {len(newest)} working groups, {len(survey_rows)} picks")
    for wg, g in newest.items():
        log(f"  {wg}: {len(g['rows'])} picks, sent by {g['who']} on {datetime.fromtimestamp(g['when'] / 1000, timezone.utc):%Y-%m-%d}")
    for wg, who, when in dropped:
        log(f"  older list for {wg} by {who} ({datetime.fromtimestamp(when / 1000, timezone.utc):%Y-%m-%d}) not used")
    if sheet:
        log(f"Master sheet: {len(extra)} rows from {sheet}")
    if dry_run:
        return
    table = table_of(item)
    existing = table.query(where="fy='" + BASELINE_FY + "'", return_count_only=True)
    if existing:
        log(f"The table already holds {existing} {BASELINE_FY} rows; not seeding again. Delete them in ArcGIS Online first to reseed.")
        return
    # master sheet first, survey after, so the survey row is newer where both name the same project
    for batch_name, rows in (("master sheet", extra), ("survey", survey_rows)):
        for i in range(0, len(rows), 500):
            res = table.edit_features(adds=[{"attributes": r} for r in rows[i:i + 500]])
            bad = [x for x in res.get("addResults", []) if not x.get("success")]
            log(f"  {batch_name}: added {len(rows[i:i + 500]) - len(bad)} rows" + (f", {len(bad)} failed: {bad[0]}" if bad else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--create", action="store_true", help="create the hosted table (no-op if it exists)")
    ap.add_argument("--seed", action="store_true", help="write the FY27 baseline rows")
    ap.add_argument("--sheet", help="last year's master sheet (.xlsx or .csv) to add to the baseline")
    ap.add_argument("--dry-run", action="store_true", help="with --seed: report the baseline without writing")
    ap.add_argument("--user", help="ArcGIS Online user name (default: the portal ArcGIS Pro is signed in to)")
    a = ap.parse_args()
    if not (a.create or a.seed):
        ap.print_help(); sys.exit(1)
    if a.seed and a.dry_run and not a.create:
        seed(None, a.sheet, True); return
    gis = connect(a.user)
    item = create(gis) if a.create else find_table(gis)
    if not item:
        sys.exit("Table not found; run with --create first.")
    if a.seed:
        seed(item, a.sheet, a.dry_run)
    log(f"\nTable URL for TABLE.url in qa/eip/priority-lists.html:\n  {table_of(item).url}\nItem: {item.homepage}")


if __name__ == "__main__":
    main()
