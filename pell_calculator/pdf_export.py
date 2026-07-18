"""Export the combined HTML report to a PDF file."""

from PyQt6.QtCore import QMarginsF
from PyQt6.QtGui import QPageLayout, QPageSize, QTextDocument
from PyQt6.QtPrintSupport import QPrinter


def export_pdf(html, path):
    printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
    printer.setOutputFileName(path)
    printer.setPageLayout(QPageLayout(
        QPageSize(QPageSize.PageSizeId.Letter),
        QPageLayout.Orientation.Portrait,
        QMarginsF(12, 12, 12, 12),
        QPageLayout.Unit.Millimeter,
    ))
    doc = QTextDocument()
    doc.setHtml(html)
    doc.print(printer)
