"""The in-app Help tab: step-by-step instructions in plain language."""

from .constants import BAD, HEAD


def h2(text):
    return f'<h2><font color="{HEAD}">{text}</font></h2>'


HELP_HTML = "".join([
    h2("HOW TO USE THIS - step by step"),

    h2("Step 1. Get your audit PDF"),
    '<p>Log in to your student portal, open your <b>Academic Evaluation</b> (Degree Works), '
    'and download or print it to PDF. It is the page that shows "Credits required / Credits '
    'applied", your classes with grades, and "Still needed" items.</p>',

    h2("Step 2. Import it"),
    '<p>Click <b>"Import audit PDF..."</b> (top right) and pick that file. The label on the '
    'Degree Progress tab confirms what loaded: your name, credits, how many registered terms '
    'and unmet requirements were found. If it cannot read your PDF, it says so, and you can '
    'type your credits manually on the Degree Progress tab instead.</p>',

    h2("Step 3. Paycheck tab - enter your wages"),
    '<p><b>OLD</b> = before your raise (or before whatever changed). <b>NEW</b> = now.<br>'
    'Hourly wage, hours per week, and taxes taken out in percent.<br>'
    '<b>Finding your tax percent from a paystub:</b> (gross pay minus take-home pay) divided '
    'by gross pay, times 100. Example: gross $800, take-home $684.72: '
    '(800 - 684.72) / 800 x 100 = 14.4%.</p>',

    h2("Step 4. School &amp; Pell tab - enter your Pell awards"),
    '<p><b>OLD Pell award per year</b> = what you used to get. <b>NEW Pell award per year</b> '
    '= what your current award letter says. Find both in your school financial aid portal or '
    'at studentaid.gov under your aid history.<br>'
    'Cost per credit ($354) and credits per term (6) are SNHU standards; change them only if '
    'yours differ. The tab then shows what school really costs you per term and per month '
    'under both awards.</p>',

    h2("Step 5. Monthly Budget tab - enter your bills"),
    '<p>Child support, rent, food, electric, internet, phone, transportation, medical, other. '
    'Fill in only what applies to you. The tab shows what is left of your take-home pay each '
    'month under the old and new situation.</p>',

    h2("Step 6. Read the results"),
    '<p><b>Dashboard</b>: the headline numbers and the verdict (ahead or worse off per month).<br>'
    '<b>Degree Progress</b>: your registered terms with classes, priced under both Pell awards, '
    'plus routes for any still-unscheduled credits.<br>'
    '<b>Sophia Savings</b>: which Sophia courses your own audit accepts for its open '
    'requirements, and the savings. Courses that would duplicate credit you already earned are '
    'filtered out. If a requirement cannot be covered by Sophia, it says so plainly.</p>',

    h2("Step 7. Export"),
    '<p>Click <b>"Export PDF report..."</b> to save the whole analysis as a multi-page PDF '
    'you can show an advisor, a family member, or your financial aid office.</p>',

    h2("How the Sophia matching works (why you can trust it)"),
    '<p>Your audit prints the actual acceptance rule for every unmet requirement, for example: '
    '"1 Class in @ @ with attribute = EFAU or EFAC or FAS @ with transfer = Y or PHL @ with '
    'transfer = Y ... Except HIS 100 or 200". The app reads that rule from YOUR pdf and '
    'matches it against Sophia\'s published SNHU equivalency chart (snhu.sophia.org, 84 '
    'courses). A course is suggested only when its official SNHU equivalent fits your rule, '
    'is not excluded by it, and does not repeat credit you already have. No guessing.</p>',

    h2("Before you spend money"),
    f'<p><font color="{BAD}"><b>Always confirm with your school before paying anyone.</b></font> '
    'Message your advisor with your exact course picks and get written confirmation they apply '
    'to your open requirements. Equivalency charts change. Your aid portal, advisor, and the '
    'registrar are the official word. This app is a budgeting model, not financial or academic '
    'advice.</p>',

    h2("Troubleshooting"),
    '<p><b>Tiles show "-"</b>: nothing entered yet. Import your audit or type a wage or Pell '
    'amount.<br>'
    '<b>Numbers look wrong</b>: check your tax percent and that Pell awards are per YEAR, not '
    'per term.<br>'
    '<b>PDF will not import</b>: it must be a Degree Works Academic Evaluation PDF. You can '
    'still type credits required/applied and terms left on the Degree Progress tab.</p>',
])
