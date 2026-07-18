"""The main window: input tabs on the left, live-calculated results on the right.

Starts EMPTY: no audit is loaded until the user imports their Degree Works PDF,
so the import visibly does the work. Financial inputs carry sensible defaults
that the user edits to their own situation.
"""

import datetime
import math

from PyQt6.QtWidgets import (
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .audit_parser import parse_audit_pdf
from .calculations import compute
from .help_page import HELP_HTML
from .matching import match_audit
from .pdf_export import export_pdf
from .report import (
    build_report,
    render_budget,
    render_dashboard,
    render_degree,
    render_paycheck,
    render_school,
    render_sophia,
)


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pell Grant Rip-Off Calculator - SNHU edition")
        self.inputs = {}
        self.views = {}
        self.audit = None
        self.terms = []
        self.matches = None
        self._build_ui()
        self.recalc()

    # ---------------- input helpers ----------------

    def _spin(self, key, value, maximum=1_000_000):
        s = QDoubleSpinBox()
        s.setRange(0.0, maximum)
        s.setDecimals(2)
        s.setValue(value)
        s.valueChanged.connect(self.recalc)
        self.inputs[key] = s
        return s

    def _ispin(self, key, value, maximum=1000):
        s = QSpinBox()
        s.setRange(0, maximum)
        s.setValue(value)
        s.valueChanged.connect(self.recalc)
        self.inputs[key] = s
        return s

    def values(self):
        return {k: float(w.value()) for k, w in self.inputs.items()}

    # ---------------- UI ----------------

    def _tab(self, title, key, groups):
        page = QWidget()
        h = QHBoxLayout(page)
        if groups:
            left = QWidget()
            lv = QVBoxLayout(left)
            for g in groups:
                lv.addWidget(g)
            lv.addStretch()
            scroll = QScrollArea()
            scroll.setWidget(left)
            scroll.setWidgetResizable(True)
            scroll.setFixedWidth(410)
            h.addWidget(scroll)
        view = QTextEdit()
        view.setReadOnly(True)
        self.views[key] = view
        h.addWidget(view, 1)
        self.tabs.addTab(page, title)

    def _build_ui(self):
        self.tabs = QTabWidget()

        # Personal fields all start at 0: nothing about any one person is
        # preloaded. Only universal, editable facts have defaults (SNHU's
        # cost per credit and credits per term, Sophia's published price,
        # and a standard 40-hour week).
        g_old = QGroupBox("Paycheck - OLD")
        f = QFormLayout(g_old)
        f.addRow("Hourly wage ($):", self._spin("o_wage", 0.00))
        f.addRow("Hours per week:", self._spin("o_hours", 40.00))
        f.addRow("Taxes taken out (%):", self._spin("o_tax", 0.00))
        g_new = QGroupBox("Paycheck - NEW")
        f = QFormLayout(g_new)
        f.addRow("Hourly wage ($):", self._spin("n_wage", 0.00))
        f.addRow("Hours per week:", self._spin("n_hours", 40.00))
        f.addRow("Taxes taken out (%):", self._spin("n_tax", 0.00))

        g_school = QGroupBox("SNHU / Pell (raw numbers)")
        f = QFormLayout(g_school)
        f.addRow("Cost per credit ($):", self._spin("per_credit", 354.00))
        f.addRow("Credits per 8-week term:", self._ispin("cpt", 6, 24))
        f.addRow("OLD Pell award per year ($):", self._spin("o_pell", 0.00))
        f.addRow("NEW Pell award per year ($):", self._spin("n_pell", 0.00))

        g_bills = QGroupBox("Monthly bills")
        f = QFormLayout(g_bills)
        f.addRow("Child support ($):", self._spin("cs", 0.00))
        f.addRow("Rent ($):", self._spin("rent", 0.00))
        f.addRow("Food ($):", self._spin("food", 0.00))
        f.addRow("Electric ($):", self._spin("electric", 0.00))
        f.addRow("Internet ($):", self._spin("internet", 0.00))
        f.addRow("Phone ($):", self._spin("phone", 0.00))
        f.addRow("Transportation / gas ($):", self._spin("transport", 0.00))
        f.addRow("Medical ($):", self._spin("medical", 0.00))
        f.addRow("Other ($):", self._spin("other", 0.00))

        g_import = QGroupBox("Your audit")
        fv = QVBoxLayout(g_import)
        btn = QPushButton("Import Degree Works audit PDF...")
        btn.clicked.connect(self.import_pdf)
        fv.addWidget(btn)
        self.import_label = QLabel("Nothing imported yet. Everything below fills in "
                                   "automatically when you import your audit PDF.")
        self.import_label.setWordWrap(True)
        fv.addWidget(self.import_label)
        f = QFormLayout()
        f.addRow("Credits required:", self._ispin("req", 0, 300))
        f.addRow("Credits applied (incl. IP/PR):", self._ispin("applied", 0, 300))
        f.addRow("Registered terms left to pay\n(lower it if current term is paid):",
                 self._ispin("terms_left", 0, 12))
        fv.addLayout(f)

        g_sophia = QGroupBox("Sophia plan")
        f = QFormLayout(g_sophia)
        f.addRow("Sophia price per month ($):", self._spin("sophia_mo", 99.00))
        f.addRow("Months you'll need\n(2 active courses at a time):", self._ispin("sophia_months", 1, 12))

        self._tab("Dashboard", "dash", [])
        self._tab("Paycheck", "pay", [g_old, g_new])
        self._tab("School && Pell", "school", [g_school])
        self._tab("Monthly Budget", "budget", [g_bills])
        self._tab("Degree Progress", "degree", [g_import])
        self._tab("Sophia Savings", "sophia", [g_sophia])
        self._tab("Help", "help", [])
        self.views["help"].setHtml(HELP_HTML)

        top = QHBoxLayout()
        top.addStretch()
        import_btn = QPushButton("Import audit PDF...")
        import_btn.clicked.connect(self.import_pdf)
        top.addWidget(import_btn)
        export_btn = QPushButton("Export PDF report...")
        export_btn.clicked.connect(self.export_report)
        top.addWidget(export_btn)

        root = QVBoxLayout(self)
        root.addLayout(top)
        root.addWidget(self.tabs)

    # ---------------- actions ----------------

    def import_pdf(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose your Degree Works audit PDF", "", "PDF files (*.pdf)")
        if not path:
            return
        try:
            audit, terms = parse_audit_pdf(path)
        except Exception as e:
            QMessageBox.warning(self, "Couldn't parse PDF",
                                f"{e}\n\nYou can still type your numbers manually on the "
                                f"Degree Progress tab.")
            return
        self.audit = audit
        self.terms = terms
        self.matches = match_audit(audit)
        self.inputs["req"].setValue(audit["credits_required"])
        self.inputs["applied"].setValue(audit["credits_applied"])
        self.inputs["terms_left"].setValue(len(terms))
        months = max(1, math.ceil(self.matches["classes_needed"] / 2))
        self.inputs["sophia_months"].setValue(months)
        rules_found = len(self.matches["rules"])
        uncovered = len(self.matches["uncovered"])
        self.import_label.setText(
            f"Loaded: {audit['student']} (audit {audit['date']}) - "
            f"{audit['credits_applied']}/{audit['credits_required']} credits, "
            f"{len(terms)} registered term(s), {rules_found} unmet class rule(s) "
            f"({uncovered} not coverable by Sophia), "
            f"{len(audit['completed'])} completed classes detected")
        self.recalc()

    def export_report(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF report", "pell_ripoff_report.pdf", "PDF files (*.pdf)")
        if not path:
            return
        if not path.lower().endswith(".pdf"):
            path += ".pdf"
        c = compute(self.values())
        today = datetime.date.today().strftime("%m/%d/%Y")
        try:
            export_pdf(build_report(c, self.audit, self.terms, self.matches, today), path)
        except Exception as e:
            QMessageBox.warning(self, "Export failed", str(e))
            return
        QMessageBox.information(self, "Report saved", f"PDF saved to:\n{path}")

    def recalc(self):
        c = compute(self.values())
        self.views["dash"].setHtml(render_dashboard(c, self.audit))
        self.views["pay"].setHtml(render_paycheck(c))
        self.views["school"].setHtml(render_school(c))
        self.views["budget"].setHtml(render_budget(c))
        self.views["degree"].setHtml(render_degree(c, self.audit, self.terms))
        self.views["sophia"].setHtml(render_sophia(c, self.audit, self.matches))
