"""HTML renderers for every tab, plus the combined printable report."""

from .constants import (
    BAD,
    GOOD,
    HEAD,
    MUTED,
    SOPHIA_CATALOG,
    SOPHIA_PRICING,
    WEEKS_PER_MONTH,
)

TABLE = '<table width="100%" cellspacing="0" cellpadding="6" border="0.5" bordercolor="#d5dae4">'


def money(x):
    sign = "-" if round(x, 2) < 0 else ""
    return f"{sign}${abs(x):,.2f}"


def color(x, good_when_positive=True):
    positive = round(x, 2) >= 0
    c = GOOD if positive == good_when_positive else BAD
    return f'<font color="{c}"><b>{money(x)}</b></font>'


def th(*cells):
    tds = "".join(
        f'<td align="{a}" bgcolor="#23417a"><font color="white"><b>{t}</b></font></td>'
        for t, a in cells
    )
    return f"<tr>{tds}</tr>"


def tr(label, *vals, bold=False):
    b1, b2 = ("<b>", "</b>") if bold else ("", "")
    tds = "".join(f'<td align="right">{b1}{v}{b2}</td>' for v in vals)
    return f"<tr><td>{b1}{label}{b2}</td>{tds}</tr>"


def h2(text):
    return f'<h2><font color="{HEAD}">{text}</font></h2>'


def tile(label, value, sub=""):
    return (
        f'<td bgcolor="#ffffff" align="center" style="padding:12px">'
        f'<font color="{MUTED}" size="2">{label}</font><br>'
        f'<font size="5"><b>{value}</b></font><br>'
        f'<font color="{MUTED}" size="2">{sub}</font></td>'
    )


IMPORT_PROMPT = (
    f'<p style="font-size:15px"><font color="{BAD}"><b>No audit loaded yet.</b></font> '
    'Click <b>"Import audit PDF..."</b> (top right) and pick the Academic Evaluation '
    'PDF from your student portal. Your credits, remaining terms, unmet requirements, '
    'and Sophia matches will fill in automatically.</p>'
)


def render_dashboard(c, audit):
    v = c["in"]
    worse = c["n_left_mo"] - c["o_left_mo"]
    worse_cal = c["n_left_mo_cal"] - c["o_left_mo_cal"]
    verdict = (
        f'<font color="{GOOD}"><b>You come out AHEAD {money(worse)} per 4-week period '
        f'({money(worse_cal)} per calendar month) vs the old situation.</b></font>'
        if round(worse, 2) >= 0 else
        f'<font color="{BAD}"><b>Despite the raise you are WORSE OFF by {money(-worse)} per '
        f'4-week period ({money(-worse_cal)} per true calendar month) than at the old wage '
        f'with the old Pell.</b></font>'
    )
    raise_take = c["n_take_mo"] - c["o_take_mo"]
    school_up = c["n_school_mo"] - c["o_school_mo"]
    pct = school_up / max(0.01, raise_take) * 100
    who = (f"{audit['student']} (audit {audit['date']}, GPA {audit['gpa']})"
           if audit else "no audit loaded")
    parts = [h2(f"PELL GRANT RIP-OFF CALCULATOR: {who}")]
    if not audit:
        parts.append(IMPORT_PROMPT)
    if v["o_wage"] == 0 and v["n_wage"] == 0:
        parts.append(
            '<p><b>Then enter your own numbers:</b> wages and tax on the Paycheck tab, '
            'your OLD and NEW Pell awards on the School &amp; Pell tab, and your bills on '
            'the Monthly Budget tab. Everything recalculates as you type. '
            'Find your tax percent on a paystub: (gross minus take-home) / gross x 100.</p>')
    # Before anything personal is entered, show placeholders instead of
    # numbers computed from nothing (like negative leftover with $0 income).
    fresh = (not audit and v["o_wage"] == 0 and v["n_wage"] == 0
             and v["o_pell"] == 0 and v["n_pell"] == 0)
    if fresh:
        parts += [
            '<table width="100%" cellspacing="8"><tr>',
            tile("Pell was cut by", "-", "waiting for your Pell awards"),
            tile("School / month (NEW Pell)", "-", "waiting for your numbers"),
            tile("Left over / month (NEW)", "-", "waiting for your numbers"),
            "</tr></table>",
        ]
        return "".join(parts)
    parts += [
        '<table width="100%" cellspacing="8"><tr>',
        tile("Pell was cut by", money(c["pell_cut"]) + "/yr",
             f'{money(v["o_pell"])} to {money(v["n_pell"])}'),
        tile("School / month (NEW Pell)", money(c["n_school_mo"]), f'was {money(c["o_school_mo"])}'),
        tile("Left over / 4-week period (NEW)", money(c["n_left_mo"]), f'was {money(c["o_left_mo"])}'),
        "</tr>",
    ]
    if audit:
        parts += [
            "<tr>",
            tile("Cost to graduate - all SNHU", money(c["n_grad_snhu"]),
                 f'{c["terms_left"]} registered + {c["unsched_terms"]} extra term(s)'),
            tile("Cost to graduate - Sophia route", money(c["n_grad_sophia"]),
                 f'{c["terms_left"]} SNHU terms + Sophia {money(c["sophia_cost"])}'),
            tile("Sophia saves you", money(c["sophia_savings"]),
                 f'on the last {c["unsched"]} unscheduled credits'),
            "</tr>",
        ]
    parts += [
        "</table>",
        f'<p style="font-size:15px">{verdict}</p>',
        f'<p>The Pell cut raised school from {money(c["o_school_mo"])} to {money(c["n_school_mo"])} '
        f'per month (<font color="{BAD}"><b>+{money(school_up)}/month</b></font>). '
        f'Your raise is worth {money(raise_take)} per 4-week period after tax. '
        f'The school increase eats <b>{pct:.0f}%</b> of it.</p>',
    ]
    return "".join(parts)


def render_paycheck(c):
    cs_wk = c["in"]["cs"] / WEEKS_PER_MONTH
    return "".join([
        h2("PAYCHECK"), TABLE,
        th(("", "left"), ("OLD", "right"), ("NEW", "right"), ("CHANGE", "right")),
        tr("Gross per week", money(c["o_gross_wk"]), money(c["n_gross_wk"]),
           color(c["n_gross_wk"] - c["o_gross_wk"])),
        tr("Take-home per week (after tax)", money(c["o_take_wk"]), money(c["n_take_wk"]),
           color(c["n_take_wk"] - c["o_take_wk"])),
        tr("After child support, per week", money(c["o_take_wk"] - cs_wk), money(c["n_take_wk"] - cs_wk),
           color(c["n_take_wk"] - c["o_take_wk"])),
        tr("Take-home per 4-week month", money(c["o_take_mo"]), money(c["n_take_mo"]),
           color(c["n_take_mo"] - c["o_take_mo"]), bold=True),
        tr("Gross per 4-week month", money(c["o_gross_wk"] * 4), money(c["n_gross_wk"] * 4),
           color((c["n_gross_wk"] - c["o_gross_wk"]) * 4)),
        "</table>",
        f'<p>Raise: {money(c["n_gross_wk"] - c["o_gross_wk"])}/week gross = '
        f'{money((c["n_gross_wk"] - c["o_gross_wk"]) * 4)}/4-week month = '
        f'{money((c["n_gross_wk"] - c["o_gross_wk"]) * 8)} per 8-week term.</p>',
    ])


def render_school(c):
    v = c["in"]
    return "".join([
        h2("SCHOOL &amp; PELL (SNHU) - calculated"),
        f'<p>Six 8-week terms/year = three 16-week semesters; a semester (2 terms) is the Pell '
        f'payment period. {int(v["cpt"])} cr/term = {int(v["cpt"] * 2)} cr/semester = '
        f'<b>{c["intensity"] * 100:.0f}% enrollment intensity</b> (12 cr = full time). '
        f'Pell = half the yearly award per semester times intensity. Year-Round Pell funds the '
        f'3rd semester at the same rate, so six terms never shrinks the per-term amount.</p>',
        TABLE,
        th(("", "left"), ("OLD PELL", "right"), ("NEW PELL", "right"), ("CHANGE", "right")),
        tr("Pell award per year", money(v["o_pell"]), money(v["n_pell"]),
           color(v["n_pell"] - v["o_pell"])),
        tr("Pell per semester (2 terms)", money(c["o_pell_term"] * 2), money(c["n_pell_term"] * 2),
           color((c["n_pell_term"] - c["o_pell_term"]) * 2)),
        tr("Pell per 8-week term", money(c["o_pell_term"]), money(c["n_pell_term"]),
           color(c["n_pell_term"] - c["o_pell_term"])),
        tr("Tuition per term", money(c["tuition_term"]), money(c["tuition_term"]), "same"),
        tr("YOU OWE per term", money(c["o_owed_term"]), money(c["n_owed_term"]),
           color(c["n_owed_term"] - c["o_owed_term"], good_when_positive=False), bold=True),
        tr("School cost per month", money(c["o_school_mo"]), money(c["n_school_mo"]),
           color(c["n_school_mo"] - c["o_school_mo"], good_when_positive=False), bold=True),
        "</table>",
        '<p><i>Source: SNHU Financial Aid Offer Terms and Conditions '
        '(snhu.edu/consumer-information). SNHU recalculates actual Pell on day 15 of each term '
        'from credits you are attending; your aid portal is the final word.</i></p>',
    ])


def render_budget(c):
    rows = [h2("BUDGET (4-week budget period)"), TABLE,
            th(("", "left"), ("OLD", "right"), ("NEW", "right")),
            tr("Take-home pay (4 paychecks)", money(c["o_take_mo"]), money(c["n_take_mo"]))]
    for label, val in c["bill_items"]:
        if val > 0:
            rows.append(tr(f"- {label}", money(-val), money(-val)))
    rows += [
        tr("- School (after Pell)", money(-c["o_school_mo"]), money(-c["n_school_mo"])),
        tr("= LEFT OVER per 4-week period", color(c["o_left_mo"]), color(c["n_left_mo"]), bold=True),
        tr("True calendar-month take-home (x 52/12)",
           money(c["o_take_mo_cal"]), money(c["n_take_mo_cal"])),
        tr("= LEFT OVER per calendar month", color(c["o_left_mo_cal"]), color(c["n_left_mo_cal"]),
           bold=True),
        "</table>",
        f'<p>Bills total {money(c["bills"])}/month. Add food and utilities on the left '
        f'to see the real picture.</p>',
        '<p><i>Note: a "4-week period" is 4 paychecks; a year has 13 of those but only 12 '
        'calendar months. Bills like rent are per calendar month, so the calendar-month row '
        '(weekly pay x 52 / 12) is the honest monthly average.</i></p>',
    ]
    return "".join(rows)


def render_degree(c, audit, terms):
    if not audit:
        return h2("DEGREE PROGRESS") + IMPORT_PROMPT
    v = c["in"]
    rows = [
        h2(f"DEGREE PROGRESS: {audit['student']}"),
        f'<p><b>{int(v["req"])}</b> credits required &bull; <b>{int(v["applied"])}</b> applied '
        f'(incl. in-progress/pre-registered; {audit["institutional_done"]} institutional completed) '
        f'&bull; <b>{c["unsched"]} credits ({c["unsched_classes"]} classes) still unscheduled</b> '
        f'&bull; GPA {audit["gpa"]} &bull; audit {audit["date"]}</p>',
        h2("Registered terms (locked in at SNHU)"),
        TABLE,
        th(("Term", "left"), ("Classes", "left"), ("Tuition", "right"),
           ("OLD Pell cost", "right"), ("NEW Pell cost", "right")),
    ]
    for term, status, classes in terms:
        cls = "<br>".join(f"{code} - {title}" for code, title in classes)
        rows.append(
            f'<tr><td><b>{term}</b><br><font color="{MUTED}" size="2">{status}</font></td>'
            f'<td>{cls}</td>'
            f'<td align="right">{money(c["tuition_term"])}</td>'
            f'<td align="right">{money(c["o_owed_term"])}</td>'
            f'<td align="right"><b>{money(c["n_owed_term"])}</b></td></tr>'
        )
    # Empty second cell keeps totals under the right columns
    # (Term | Classes | Tuition | OLD Pell | NEW Pell).
    rows += [
        tr(f"TOTAL for {c['terms_left']} remaining registered term(s)", "",
           money(c["tuition_term"] * c["terms_left"]),
           money(c["o_registered_cost"]), money(c["n_registered_cost"]), bold=True),
        "</table>",
    ]
    if c["crossover_terms"] > 0:
        rows.append(
            f'<p><i>The NEW Pell total above prices the first {c["crossover_terms"]} '
            f'registered term(s) at the OLD Pell rate (summer crossover setting on the left).</i></p>')
    rows.append(
        '<p><b>Summer crossover:</b> a term that spans July 1 (like a Jun-Aug term) can be paid '
        'from EITHER award year; your school assigns it. Ask your aid office: "Which Pell award '
        'year funds my current summer term, and what exact amount applies to it?" Then set '
        '"terms funded at the OLD Pell" on the left to match.</p>')
    if c["unsched"] > 0:
        rows += [
            h2(f"Still unscheduled: {c['unsched']} credits ({c['unsched_classes']} classes)"),
            TABLE,
            th(("Route for those credits", "left"), ("Cost", "right"), ("Timing", "right")),
            tr(f"{c['unsched_terms']} more SNHU term(s), NEW Pell", money(c["n_final_snhu"]),
               f"+{c['unsched_terms'] * 2} months after last registered term"),
            tr("Same, with the OLD Pell", money(c["o_final_snhu"]),
               f"+{c['unsched_terms'] * 2} months"),
            tr("Sophia transfer, done alongside registered terms", money(c["sophia_cost"]),
               "no extra terms", bold=True),
            "</table>",
            '<p>The Sophia Savings tab matches your audit\'s unmet requirements against the '
            'published Sophia equivalency catalog automatically.</p>',
        ]
    return "".join(rows)


def _catalog_rows(entries, limit=None):
    rows = [TABLE, th(("Sophia course", "left"), ("Transfers to SNHU as", "left"))]
    shown = entries if limit is None else entries[:limit]
    for sophia, code, title in shown:
        rows.append(f"<tr><td>{sophia}</td><td>{code} - {title}</td></tr>")
    rows.append("</table>")
    if limit is not None and len(entries) > limit:
        rows.append(f'<p><font color="{MUTED}">...and {len(entries) - limit} more '
                    f'transferable courses.</font></p>')
    return rows


def render_sophia(c, audit, matches):
    rows = [
        h2("SOPHIA ROUTE: matched to YOUR audit"),
        f"<p><b>{SOPHIA_PRICING}</b></p>",
        '<p>Equivalencies are verbatim from <b>snhu.sophia.org</b>, Sophia\'s official SNHU partner '
        'page. Matches below come from your audit\'s own "Still needed" rules. Equivalencies change; '
        'get written advisor confirmation before paying.</p>',
    ]
    if not audit or matches is None:
        rows.append(IMPORT_PROMPT)
        rows.append(h2(f"Full Sophia catalog ({len(SOPHIA_CATALOG)} courses)"))
        rows += _catalog_rows(SOPHIA_CATALOG)
        return "".join(rows)

    if not matches["rules"] and matches["elective_gap"] <= 0:
        rows.append(f'<p><font color="{GOOD}"><b>Your audit shows no unmet class rules and no '
                    f'free-elective gap.</b></font> Nothing left that Sophia needs to cover.</p>')

    for r in matches["rules"]:
        rows.append(h2(f'{r["title"]}: needs {r["count"]} class(es)'))
        accepted = ", ".join(r["prefixes"]) or "(attribute only)"
        exc = f' (except {", ".join(r["exceptions"])})' if r["exceptions"] else ""
        rows.append(f'<p>Audit accepts transfer prefixes: <b>{accepted}</b>{exc}.</p>')
        if r["covered"]:
            rows += _catalog_rows(r["suggestions"])
        else:
            rows.append(
                f'<p><font color="{BAD}"><b>No Sophia course matches this requirement.</b></font> '
                f'It has to be taken at SNHU (or ask your advisor about other transfer options).</p>')

    if matches["elective_gap"] > 0:
        rows.append(h2(f'Free electives: {matches["elective_gap"]} more credits needed'))
        rows.append('<p>Any transferable Sophia course fills a free elective. Courses that would '
                    'duplicate credit you already earned are filtered out:</p>')
        rows += _catalog_rows(matches["elective_suggestions"], limit=15)

    rows += [
        h2("The money"),
        TABLE,
        th(("", "left"), ("SNHU term(s)", "right"), ("Sophia", "right"), ("YOU SAVE", "right")),
        tr(f"Last {c['unsched']} credits, NEW Pell", money(c["n_final_snhu"]), money(c["sophia_cost"]),
           color(c["n_final_snhu"] - c["sophia_cost"]), bold=True),
        tr(f"Last {c['unsched']} credits, OLD Pell (reference)", money(c["o_final_snhu"]),
           money(c["sophia_cost"]), color(c["o_final_snhu"] - c["sophia_cost"])),
        "</table>",
        '<p><b>Checklist before paying Sophia:</b><br>'
        '1. Message your SNHU advisor with your exact picks and get written confirmation '
        'they apply to your open requirements.<br>'
        '2. Check you are under SNHU\'s 90-credit transfer max (institutional credits do not '
        'count against it).<br>'
        '3. Finish the courses and send the free Sophia transcript to SNHU BEFORE applying '
        'for degree conferral.</p>',
    ]
    return "".join(rows)


def build_report(c, audit, terms, matches, generated_on):
    """One printable HTML document with every section, for PDF export."""
    sections = [
        render_dashboard(c, audit),
        render_paycheck(c),
        render_school(c),
        render_budget(c),
        render_degree(c, audit, terms),
        render_sophia(c, audit, matches),
    ]
    who = audit["student"] if audit else "no audit loaded"
    when = audit["date"] if audit else "-"
    parts = [
        f'<h1><font color="{HEAD}">Pell Grant Rip-Off Report</font></h1>'
        f'<p>{who} &bull; audit {when} &bull; report generated {generated_on}</p>',
        sections[0],
    ]
    for s in sections[1:]:
        parts.append(f'<div style="page-break-before:always">{s}</div>')
    parts.append(
        '<p><i>Sources: snhu.edu/consumer-information (financial aid terms), '
        'sophia.org/plans-and-pricing, snhu.sophia.org (equivalencies). '
        'This is a budgeting model, not financial or academic advice; your SNHU aid portal, '
        'advisor, and the registrar are the official word.</i></p>')
    return "".join(parts)
