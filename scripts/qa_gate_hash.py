"""Print the hash assets/qa-gate.js expects for a new QA password.

Usage, from the repo root:
    python scripts/qa_gate_hash.py "new password"

Paste the output into HASH in assets/qa-gate.js. SALT here must match
SALT in that file.
"""
import hashlib
import sys

SALT = "tools.trpa.gov/qa"


def gate_hash(password: str) -> str:
    return hashlib.sha256((SALT + password).encode("utf-8")).hexdigest()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(gate_hash(sys.argv[1]))
