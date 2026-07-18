"""Shared constants: budgeting model, colors, styling, default audit data,
and the Sophia course equivalency tables (verbatim from snhu.sophia.org, July 2026)."""

WEEKS_PER_MONTH = 4   # 4-paycheck month, the way most people budget
MONTHS_PER_TERM = 2   # an 8-week SNHU term is about 2 months

GOOD = "#1e8e3e"
BAD = "#c62828"
HEAD = "#23417a"
MUTED = "#5b6478"

STYLE = """
QWidget { font-size: 13px; background: #eef1f6; color: #1a1d26; }
QTabWidget::pane { border: 1px solid #d5dae4; border-radius: 6px; background: #eef1f6; }
QTabBar::tab {
    background: #dde3ee; color: #3a445c; padding: 8px 18px; font-weight: bold;
    border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 2px;
}
QTabBar::tab:selected { background: #23417a; color: white; }
QGroupBox {
    background: #ffffff; border: 1px solid #d5dae4; border-radius: 10px;
    margin-top: 16px; font-weight: bold; padding-top: 6px;
}
QGroupBox::title {
    subcontrol-origin: margin; subcontrol-position: top left;
    left: 12px; top: 2px; color: #23417a;
}
QDoubleSpinBox, QSpinBox {
    background: #ffffff; border: 1px solid #bcc4d4; border-radius: 5px;
    padding: 3px 6px; min-width: 95px; font-weight: normal;
}
QPushButton {
    background: #23417a; color: white; font-weight: bold; border: none;
    border-radius: 6px; padding: 8px 14px;
}
QPushButton:hover { background: #2e54a0; }
QTextEdit { background: #ffffff; border: 1px solid #d5dae4; border-radius: 10px; }
QScrollArea { border: none; }
QLabel { font-weight: normal; }
"""

# Complete Sophia -> SNHU equivalency catalog, verbatim from snhu.sophia.org
# (Sophia's official SNHU partner page, fetched July 2026).
# Format: (Sophia course, SNHU equivalent code, SNHU equivalent title)
SOPHIA_CATALOG = [
    ("Anatomy and Physiology I", "BIO 205", "Human Anatomy and Physiology I"),
    ("Anatomy and Physiology I Lab", "BIO 205L", "Human Anatomy and Physiology I Lab"),
    ("Anatomy and Physiology II", "BIO 211", "Human Anatomy and Physiology II"),
    ("Anatomy and Physiology II Lab", "BIO 211L", "Human Anatomy and Physiology II Lab"),
    ("Ancient Greek Philosophers", "PHL-ELE", "Philosophy Elective"),
    ("Approaches to Studying Religions", "PHL 230", "Religions of the World"),
    ("Art History I", "FAS 201", "Introduction to Humanities I"),
    ("Art History II", "FAS 202", "Introduction to Humanities II"),
    ("Business Communication", "ENG 220", "Business Communication"),
    ("Business Data Analytics", "QSO 250", "Business Analytics"),
    ("Business Ethics", "PHL-ELE", "Philosophy Elective"),
    ("Business Law", "BUS 206", "Business Law I"),
    ("Calculus I", "MAT 225", "Calculus I: Single-Variable Calculus"),
    ("Career Readiness", "GEN-ELE", "General Elective"),
    ("College Algebra", "MAT 136", "Introduction to Quantitative Analysis"),
    ("College Readiness", "GEN-ELE", "General Elective"),
    ("Computer Applications", "IT-ELE", "Information Technology Elective"),
    ("Conflict Resolution", "COM-ELE", "Communication Elective"),
    ("Criminology", "CJ 340", "Criminology"),
    ("Critical Thinking", "PHL 111", "Introduction to Critical Thinking"),
    ("Developing Effective Teams", "OL-ELE", "Organizational Leadership Elective"),
    ("English Composition I", "ENG 130", "Foundations of Written Communication"),
    ("English Composition II", "ENG 190", "Research and Persuasion"),
    ("Environmental Science", "ENV 101", "Environmental Science"),
    ("Financial Accounting", "ACC 201", "Financial Accounting"),
    ("Foundations of English Composition", "ENG-ELE", "English Elective"),
    ("Foundations of Statistics", "MAT-ELE", "Mathematics Elective"),
    ("French I", "LFR 111", "Beginning French I"),
    ("Health, Fitness, and Wellness", "HTH-ELE", "Health Courses Elective"),
    ("Healthcare Management", "HCM-ELE", "Healthcare Management Elective"),
    ("Human Biology", "BIO-ELE", "Biology Elective"),
    ("Human Biology Lab", "BIO 210L", "Anatomy and Physiology Lab"),
    ("Human Resource Management", "HRM 200", "Human Resource Functions"),
    ("IT Career Exploration", "IT-ELE", "Information Technology Elective 100 Level"),
    ("Introduction to Business", "OL 110", "Intro to Business"),
    ("Introduction to Career Readiness", "GEN-ELE", "General Elective"),
    ("Introduction to Chemistry", "CHM-ELE", "Chemistry Elective"),
    ("Introduction to Chemistry Lab", "CHM-ELE", "Chemistry Elective - 100 Level"),
    ("Introduction to College Mathematics", "MAT 136", "Introduction to Quantitative Analysis"),
    ("Introduction to Criminal Justice", "CJ 112", "Introduction to Criminal Justice"),
    ("Introduction to Ethics", "PHL 212", "Intro to Ethics"),
    ("Introduction to Information Technology", "IT 200", "Fundamentals of Information Technology"),
    ("Introduction to Java Programming", "IT 145", "Foundation in Application Development"),
    ("Introduction to Networking", "IT 212", "Introduction to Computer Networks"),
    ("Introduction to Nutrition", "HTH-ELE", "Health Courses Elective"),
    ("Introduction to Physics", "PHY 101", "Principles of Physics"),
    ("Introduction to Psychology", "PSY 108", "Introduction to Psychology"),
    ("Introduction to Python Programming", "IT 140", "Introduction to Scripting"),
    ("Introduction to Relational Databases", "CS 231", "Database Systems"),
    ("Introduction to Sociology", "SOC 112", "Introduction to Sociology"),
    ("Introduction to Statistics", "MAT 240", "Applied Statistics"),
    ("Introduction to Web Development", "IT 270", "Web Site Design"),
    ("Lifespan Development", "PSY 211", "Lifespan Development"),
    ("Macroeconomics", "ECO 202", "Macroeconomics"),
    ("Managerial Accounting", "ACC 202", "Managerial Accounting"),
    ("Medical Terminology", "HCM 205", "Medical Terminology"),
    ("Microbiology", "BIO 212", "Microbiology"),
    ("Microbiology Lab", "BIO-ELE", "Biology Elective - 200 Level"),
    ("Microeconomics", "ECO 201", "Microeconomics"),
    ("Operations Management", "QSO 300", "Operations Management"),
    ("Organizational Behavior", "OL-ELE", "Organizational Leadership Elective"),
    ("Personal Finance", "FIN 250", "Personal Financial Planning"),
    ("Precalculus", "MAT 142", "Precalculus with Limits"),
    ("Principles of Finance", "FIN 320", "Principles of Finance"),
    ("Principles of Leadership", "OL 328", "Leadership"),
    ("Principles of Management", "OL 215", "Principles of Management"),
    ("Principles of Marketing", "MKT-ELE", "Marketing Elective"),
    ("Project Management", "QSO 340", "Project Management"),
    ("Public Speaking", "COM 213", "Public Speaking and Presentation Skills"),
    ("Public and Community Health", "PHE 101", "Fundamentals of Public Health"),
    ("Spanish I", "LSP 111", "Beginning Spanish I"),
    ("Spanish II", "LSP 112", "Beginning Spanish II"),
    ("Student Success", "GEN-ELE", "General Elective"),
    ("The Essentials of Managing Conflict", "OL-ELE", "Organizational Leadership Elective"),
    ("U.S. Government", "POL 210", "American Politics"),
    ("U.S. History I", "HIS 113", "United States History 1"),
    ("U.S. History II", "HIS 114", "United States History 2"),
    ("Visual Communications", "GRA 205", "Fundamentals of Design"),
    ("Workplace Communication", "COM 127", "Introduction to Communication"),
    ("Workplace Writing I", "ENG 130", "Foundations of Written Communication"),
    ("Workplace Writing II", "ENG 190", "Research and Persuasion"),
]

SOPHIA_PRICING = ("Pricing (sophia.org/plans-and-pricing, July 2026): $99/month, "
                  "$299/4 months, $799/12 months. Two active courses at a time, "
                  "self-paced, ACE-recommended.")
