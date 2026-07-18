# Pell Grant Rip-Off Calculator (SNHU edition)

A desktop app (PyQt6) that shows exactly what a Pell Grant cut costs you. Import
your Degree Works audit PDF and it calculates: what school really costs per term
and per month after Pell, how much of your raise the cut eats, your monthly
budget, your remaining terms priced out, and which Sophia Learning courses can
finish your open requirements by transfer credit for a fraction of tuition.

The app starts EMPTY. Nothing about your degree is hardcoded: import your own
audit PDF and watch every tab fill in from your actual data.

## Install

```
python3 -m pip install -r requirements.txt
```

## Run

```
python3 -m pell_calculator
```

or the old command, which still works:

```
python3 payment_calc.py
```

## Quick start

New user? Read **HOW_TO_USE.md** for step-by-step instructions (the same guide
is on the app's **Help** tab).

1. Click "Import audit PDF..." (top right) and pick the Academic Evaluation PDF
   downloaded from your student portal (Degree Works / Ellucian).
2. Set your wages, tax percent, Pell awards, and bills on the Paycheck, School
   and Pell, and Monthly Budget tabs.
3. Read the Dashboard for the verdict, Degree Progress for your remaining terms
   priced out, and Sophia Savings for matched courses.
4. Click "Export PDF report..." to save the whole analysis as a multi-page PDF.

## How it works (so you can trust it)

### 1. Parsing your audit PDF

The importer reads the text of an Ellucian Degree Works "Academic Evaluation"
PDF (pypdf) and extracts, with regular expressions:

- Credits required and applied: the "Credits required: X Credits applied: Y" line.
- Institutional credits, GPA, audit date, student name: their labeled lines.
- Registered classes: every line shaped like
  `CS 360 Mobile Architect & Programming IP (3) 2026 C-4 (Jun - Aug)` where the
  grade slot is IP (in progress) or PR (pre-registered). They are grouped by
  term and priced per term.
- Completed classes: every line with a letter grade (A through F). These are
  used to avoid suggesting a Sophia course that duplicates credit you already
  earned. Withdrawals (W) do not count as completed.
- Unmet requirements: every "Still needed: N Class in ..." rule block. Degree
  Works prints the actual acceptance rule, for example:

  ```
  Still needed: 1 Class in @ @ with attribute = EFAU or EFAC or ENG @ with
  transfer = Y or FAS @ with transfer = Y ... or PHL @ with transfer = Y
  Except HIS 100 or 200
  ```

  The parser extracts the accepted course prefixes (ENG, FAS, PHL, ...), the
  accepted attributes (EFAU, EFAC), and the excluded courses (HIS 100, HIS 200).
- Free electives: "Your program requires N free elective credits" versus the
  "Electives Credits applied: M" section gives the elective gap.

If a PDF cannot be parsed, the app says so and the fields stay manually editable.

### 2. Matching Sophia courses to YOUR requirements

The app embeds the complete published Sophia-to-SNHU equivalency chart from
snhu.sophia.org (Sophia's official SNHU partner page, fetched July 2026): 84
courses, each with the exact SNHU course code it transfers in as (for example
Art History I transfers as FAS 201, Introduction to Ethics as PHL 212).

Matching is deterministic, not guesswork:

- A Sophia course qualifies for an unmet requirement when the SNHU code it
  transfers in as starts with a prefix your audit's own rule accepts, is not in
  the rule's "Except" list, and does not duplicate a class you already completed.
- Any transferable Sophia course can fill a free elective slot (again minus
  duplicates of completed credit).
- If no Sophia course matches a rule, the app says so plainly: that requirement
  has to be taken at SNHU (for example upper-level major courses).

### 3. The Pell math

Based on SNHU's published Financial Aid Offer Terms and Conditions:

- SNHU online undergrad runs six 8-week terms per year, grouped into three
  16-week semesters. A semester (two consecutive terms) is the Pell payment
  period.
- Full time is 12 credits per semester (6 per term). Enrollment intensity =
  semester credits / 12, capped at 100%.
- Pell per semester = (yearly award / 2) x intensity. Per term = half of that.
- Year-Round Pell funds a third semester at the same rate (up to 150% of the
  award per year), so attending all six terms never shrinks the per-term amount.

Example: a $7,395 award gives $1,848.75 per term against $2,124 tuition
(6 credits x $354), so you owe $275.25 per term ($137.63/month). A $1,020 award
gives $255 per term, so you owe $1,869 per term ($934.50/month). That cut costs
$796.88 more per month.

**Summer crossover terms:** a term that spans July 1 sits across two federal
award years, and the school chooses which award year pays it (FSA Handbook,
"Summer Terms, Crossover Payment Periods, and Year-Round Pell"). If your aid
office says your summer term is funded by the old award year, set "terms funded
at the OLD Pell" on the Degree Progress tab and the totals adjust.

### 4. Money model

- Take-home pay = hourly wage x hours x (1 - tax%).
- The budget is shown two ways: a "4-week budget period" (4 paychecks; a year
  has 13 of these) and a true calendar-month average (weekly pay x 52 / 12).
  Bills like rent are per calendar month, so the calendar-month row is the
  honest monthly average; only paychecks scale between the two views.
- Budget = take-home minus child support, rent, bills, and the after-Pell
  school cost.
- Cost to graduate = (registered terms x what you owe per term, respecting the
  crossover setting) + either one more SNHU term per 6 unscheduled credits, or
  the Sophia subscription cost.

## Project structure

```
payment_cal/
├── README.md
├── HOW_TO_USE.md            # step-by-step user guide (also on the Help tab)
├── requirements.txt
├── payment_calc.py          # thin launcher (kept for the old command)
└── pell_calculator/
    ├── __init__.py
    ├── __main__.py          # entry point (python3 -m pell_calculator)
    ├── constants.py         # styling + the full Sophia equivalency catalog
    ├── audit_parser.py      # Degree Works PDF parser (credits, terms, rules)
    ├── matching.py          # audit rules x Sophia catalog matcher
    ├── calculations.py      # all money math, pure functions
    ├── report.py            # HTML renderers for tabs + printable report
    ├── pdf_export.py        # PDF writer (QPrinter)
    ├── help_page.py         # the Help tab content
    └── ui.py                # main window, tabs, inputs
```

## Sources

- SNHU Financial Aid Offer Terms and Conditions:
  https://www.snhu.edu/consumer-information/financial-aid-offer-terms-and-conditions
- Sophia pricing: https://www.sophia.org/plans-and-pricing/
- Sophia to SNHU equivalencies: https://snhu.sophia.org/

## Limitations and disclaimer

- The parser is built for Ellucian Degree Works evaluations (tested on an SNHU
  audit). Other schools' audit formats may not parse; fields stay editable.
- The Sophia catalog is a snapshot (July 2026). Equivalencies change. The app
  tells you to confirm picks with your advisor, and it means it: get written
  confirmation before paying for any Sophia course.
- SNHU recalculates actual Pell on day 15 of each term from credits you are
  attending. This is a budgeting model, not financial or academic advice. Your
  aid portal, advisor, and the registrar are the official word.
