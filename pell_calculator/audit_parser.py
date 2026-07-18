"""Parser for Ellucian Degree Works academic evaluation PDFs.

Extracts everything the calculator needs from ANY student's audit:
  - credits required/applied, institutional credits, GPA, audit date
  - every in-progress (IP) or pre-registered (PR) class, grouped by term
  - every completed class (letter grade), used to avoid suggesting
    Sophia courses that duplicate credit the student already has
  - every unmet "Still needed: N Class in ..." rule, including which
    course prefixes/attributes are accepted and which courses are excluded
  - the free elective requirement and how many elective credits are applied
"""

import re

COURSE_RE = re.compile(
    r"([A-Z]{2,4}\s?\d{3})\s+(.{3,60}?)\s+(IP|PR)\s+\(?(\d+)\)?\s+(20\d{2})\s+(C-\d)\s*\(([^)]*)\)"
)

COMPLETED_RE = re.compile(
    r"([A-Z]{2,4}\s?\d{3})\s+.{3,60}?\s+([A-F][+-]?)\s+\d+\s"
)

RULE_RE = re.compile(r"Still needed:\s*(\d+)\s+Class(?:es)?\s+in\s+", re.IGNORECASE)


def _parse_rules(text):
    """Pull each 'Still needed: N Class in ...' rule block out of the audit text."""
    rules = []
    for m in RULE_RE.finditer(text):
        chunk = text[m.end():m.end() + 700]
        # Rule text is a run of "XXX @ with transfer = Y or ..." clauses;
        # cut the chunk at the first line that clearly isn't part of the rule.
        stop = re.search(r"\n(?=[A-Z][a-z]+(?: [A-Za-z&:]+)*\s*\n)", chunk)
        if stop:
            chunk = chunk[:stop.start()]
        prefixes = sorted(set(re.findall(r"\b([A-Z]{2,4})\s*@", chunk)))
        attributes = sorted(set(re.findall(r"attribute\s*=\s*([A-Z]{3,6})", chunk)))
        exceptions = []
        for ex in re.finditer(r"Except\s+([A-Z]{2,4})\s+(\d{3})((?:\s+or\s+\d{3})*)", chunk):
            pfx = ex.group(1)
            exceptions.append(f"{pfx} {ex.group(2)}")
            for extra in re.findall(r"\d{3}", ex.group(3)):
                exceptions.append(f"{pfx} {extra}")
        if not prefixes and not attributes:
            continue
        # Requirement title: the nearest preceding line that reads like
        # "<Title> <COURSE 123> ..." (a requirement heading followed by the
        # course listed under it); fall back to the last non-empty line.
        before = text[max(0, m.start() - 300):m.start()]
        cand = re.findall(r"([A-Z][A-Za-z&:'/,\- ]{2,60}?)\s+[A-Z]{2,4}\s?\d{3}\s", before)
        if cand:
            title = cand[-1].strip()
        else:
            lines = [ln.strip() for ln in before.splitlines() if ln.strip()]
            title = re.split(r"\s+[A-Z]{2,4}\s?\d{3}\s", lines[-1])[0].strip() if lines else "Requirement"
        title = title or "Requirement"
        rules.append({
            "title": title,
            "count": int(m.group(1)),
            "prefixes": prefixes,
            "attributes": attributes,
            "exceptions": exceptions,
        })
    return rules


def parse_audit_pdf(path):
    """Return (audit_dict, terms_list) parsed from a Degree Works audit PDF.

    Raises ValueError if the file doesn't look like a Degree Works evaluation.
    """
    from pypdf import PdfReader

    text = "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    if "Degree Works" not in text and "Credits required" not in text:
        raise ValueError("This doesn't look like a Degree Works academic evaluation PDF.")

    def grab(pattern, cast=int, default=None):
        m = re.search(pattern, text)
        return cast(m.group(1)) if m else default

    audit = {
        "student": grab(r"Student name\s*([A-Za-z ,.'-]+)", str, "(imported audit)").strip(),
        "credits_required": grab(r"Credits required:\s*(\d+)", int, 120),
        "credits_applied": grab(r"Credits applied:\s*(\d+)", int, 0),
        "institutional_done": grab(r"total of\s*(\d+)\s*institutional", int, 0),
        "gpa": grab(r"(?:Overall|Cumulative)\s+GPA\s*([\d.]+)", str, "?"),
        "date": grab(r"Audit date\s*([\d/]+)", str, "?"),
        "elective_required": grab(r"requires\s+(\d+)\s+free elective credits", int, 0),
        "elective_applied": grab(r"Electives\s+Credits applied:\s*(\d+)", int, 0),
        "rules": _parse_rules(text),
        "completed": sorted({re.sub(r"\s+", " ", c.strip())
                             for c, _grade in COMPLETED_RE.findall(text)}),
    }

    seen = set()
    by_term = {}
    for code, title, status, _credits, year, cterm, span in COURSE_RE.findall(text):
        code = re.sub(r"\s+", " ", code.strip())
        if code in seen:
            continue
        seen.add(code)
        key = (int(year), int(cterm[2]))
        label = f"{year} {cterm} ({re.sub(r'[^A-Za-z-]+', ' ', span).strip()})"
        by_term.setdefault(key, {"label": label, "status": [], "classes": []})
        by_term[key]["status"].append(status)
        by_term[key]["classes"].append((code, title.strip()))

    terms = []
    for key in sorted(by_term):
        t = by_term[key]
        status = "IN PROGRESS NOW" if "IP" in t["status"] else "PRE-REGISTERED"
        terms.append((t["label"], status, t["classes"]))

    if not terms and audit["credits_applied"] == 0:
        raise ValueError("Couldn't find credits or registered classes in this PDF.")
    return audit, terms
