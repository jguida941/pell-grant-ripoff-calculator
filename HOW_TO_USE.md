# How to use the Pell Grant Rip-Off Calculator - step by step

This same guide is inside the app on the **Help** tab.

## Step 0. Launch the app

One command, any computer:

```
python3 start.py
```

On a Mac you can also just **double-click `start.command`** in the project
folder (the first time, macOS may make you right-click it and choose **Open**).

The first launch creates a private `.venv` folder in the project and installs
the two requirements (PyQt6 and pypdf) into it automatically — give it a
minute. Every launch after that is instant. If you instead start the app with
plain `python3 payment_calc.py` and see "No module named 'PyQt6'" or "No module
named 'pypdf'", that Python doesn't have the requirements — close it and use
`python3 start.py`.

## Step 1. Get your audit PDF

Log in to your student portal, open your **Academic Evaluation** (Degree Works),
and download or print it to PDF. It is the page that shows "Credits required /
Credits applied", your classes with grades, and "Still needed" items.

## Step 2. Import it

Click **"Import audit PDF..."** (top right) and pick that file. The label on the
Degree Progress tab confirms what loaded: your name, credits, how many
registered terms and unmet requirements were found. If it cannot read your PDF,
it says so, and you can type your credits manually on the Degree Progress tab
instead.

## Step 3. Paycheck tab - enter your wages

- **OLD** = before your raise (or before whatever changed). **NEW** = now.
- Hourly wage, hours per week, and taxes taken out in percent.
- Finding your tax percent from a paystub:
  (gross pay minus take-home pay) divided by gross pay, times 100.
  Example: gross $800, take-home $684.72 gives (800 - 684.72) / 800 x 100 = 14.4%.

## Step 4. School & Pell tab - enter your Pell awards

- **OLD Pell award per year** = what you used to get.
- **NEW Pell award per year** = what your current award letter says.
- Find both in your school financial aid portal or at studentaid.gov under your
  aid history.
- Cost per credit ($354) and credits per term (6) are SNHU standards; change
  them only if yours differ.

The tab then shows what school really costs you per term and per month under
both awards.

## Step 5. Monthly Budget tab - enter your bills

Child support, rent, food, electric, internet, phone, transportation, medical,
other. Fill in only what applies to you. The tab shows what is left of your
take-home pay under the old and new situation, two ways: per 4-week budget
period (4 paychecks) and per true calendar month (weekly pay x 52 / 12, the
honest monthly average since bills are per calendar month).

## Step 5b. Summer crossover (if you have a summer term)

A term that spans July 1 sits across two federal award years, and your school
chooses which award year pays it. Ask your aid office: "Which Pell award year
funds my current summer term, and what exact amount applies to it?" If they say
the OLD award year, set "terms funded at the OLD Pell" on the Degree Progress
tab and the totals adjust.

## Step 6. Read the results

- **Dashboard**: the headline numbers and the verdict (ahead or worse off per month).
- **Degree Progress**: your registered terms with classes, priced under both
  Pell awards, plus routes for any still-unscheduled credits.
- **Sophia Savings**: which Sophia courses your own audit accepts for its open
  requirements, and the savings. Courses that would duplicate credit you already
  earned are filtered out. If a requirement cannot be covered by Sophia, it says
  so plainly.

## Step 7. Export

Click **"Export PDF report..."** to save the whole analysis as a multi-page PDF
you can show an advisor, a family member, or your financial aid office.

## How the Sophia matching works (why you can trust it)

Your audit prints the actual acceptance rule for every unmet requirement, for
example: "1 Class in @ @ with attribute = EFAU or EFAC or FAS @ with transfer =
Y or PHL @ with transfer = Y ... Except HIS 100 or 200". The app reads that rule
from YOUR pdf and matches it against Sophia's published SNHU equivalency chart
(snhu.sophia.org, 84 courses). A course is suggested only when its official SNHU
equivalent fits your rule, is not excluded by it, and does not repeat credit you
already have. No guessing.

## Before you spend money

**Always confirm with your school before paying anyone.** Message your advisor
with your exact course picks and get written confirmation they apply to your
open requirements. Equivalency charts change. Your aid portal, advisor, and the
registrar are the official word. This app is a budgeting model, not financial or
academic advice.

## Troubleshooting

- **Tiles show "-"**: nothing entered yet. Import your audit or type a wage or
  Pell amount.
- **Numbers look wrong**: check your tax percent and that Pell awards are per
  YEAR, not per term.
- **"No module named 'pypdf'" when importing** (or "No module named 'PyQt6'"
  at launch): the app was started with a Python that doesn't have the
  requirements installed. Close it and launch with `python3 start.py` (or
  double-click `start.command` on a Mac) — it installs everything into `.venv`
  automatically.
- **PDF will not import**: it must be a Degree Works Academic Evaluation PDF.
  You can still type credits required/applied and terms left on the Degree
  Progress tab.
