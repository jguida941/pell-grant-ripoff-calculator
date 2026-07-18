"""Match a parsed audit's unmet requirements against the Sophia catalog.

Deterministic, no guessing: the audit's own "Still needed" rule says which
course prefixes are accepted as transfer credit (for example "FAS @ with
transfer = Y or PHL @ with transfer = Y Except HIS 100 or 200"), so a Sophia
course qualifies when its published SNHU equivalent starts with an accepted
prefix, isn't in the exception list, and doesn't duplicate credit the
student already earned.
"""

import math
import re

from .constants import SOPHIA_CATALOG


def _norm(code):
    return re.sub(r"[^A-Z0-9]", "", code.upper())


def _prefix(code):
    m = re.match(r"([A-Z]+)", _norm(code))
    return m.group(1) if m else ""


def match_audit(audit, catalog=SOPHIA_CATALOG):
    """Return per-rule Sophia suggestions plus free-elective suggestions."""
    completed = {_norm(c) for c in audit.get("completed", [])}

    rules = []
    for r in audit.get("rules", []):
        allowed = set(r.get("prefixes", []))
        excluded = {_norm(e) for e in r.get("exceptions", [])}
        suggestions = [
            (sophia, code, title) for sophia, code, title in catalog
            if _prefix(code) in allowed
            and _norm(code) not in excluded
            and _norm(code) not in completed
        ]
        rules.append({**r, "suggestions": suggestions, "covered": bool(suggestions)})

    elective_gap = max(0, audit.get("elective_required", 0) - audit.get("elective_applied", 0))
    elective_suggestions = [
        (sophia, code, title) for sophia, code, title in catalog
        if _norm(code) not in completed
    ]

    classes_needed = sum(r["count"] for r in rules) + math.ceil(elective_gap / 3)
    return {
        "rules": rules,
        "elective_gap": elective_gap,
        "elective_suggestions": elective_suggestions,
        "classes_needed": classes_needed,
        "uncovered": [r for r in rules if not r["covered"]],
    }
