"""Entry point: python3 -m pell_calculator"""

import sys

from PyQt6.QtWidgets import QApplication

from .constants import STYLE
from .ui import Calculator


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)
    w = Calculator()
    w.resize(1500, 950)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
