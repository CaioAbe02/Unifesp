from __future__ import annotations
from abc import ABC, abstractmethod

class Report(ABC):
  @abstractmethod
  def accept(self, visitor: ReportVisitor):
    pass

class FinancialReport(Report):
  def __init__(self, revenue: float, expenses: float):
    self.revenue = revenue
    self.expenses = expenses

  def accept(self, visitor: ReportVisitor):
    return visitor.visit_financial_report(self)

class InverntoryReport(Report):
  def __init__(self, category: str, total_items: int):
    self.category = category
    self.total_items = total_items

  def accept(self, visitor: ReportVisitor):
    return visitor.visit_inventory_report(self)

class SalesReport(Report):
  def __init__(self, total_sales: int, revenue: float):
    self.total_sales = total_sales
    self.revenue = revenue

  def accept(self, visitor: ReportVisitor):
    return visitor.visit_sales_report(self)

class ReportVisitor(ABC):
  @abstractmethod
  def visit_financial_report(self, report: FinancialReport):
    pass

  @abstractmethod
  def visit_inventory_report(self, report: InverntoryReport):
    pass

  @abstractmethod
  def visit_sales_report(self, report: SalesReport):
    pass

class PdfExporter(ReportVisitor):
  def visit_financial_report(self, report: FinancialReport):
    print(f"FINANCIAL REPORT\nRevenue: {report.revenue}\nExpenses: {report.expenses}")

  def visit_inventory_report(self, report: InverntoryReport):
    print(f"INVENTORY REPORT\nCategory: {report.category}\nTotal items: {report.total_items}")

  def visit_sales_report(self, report: SalesReport):
    print(f"SALES REPORT\nTotal sales: {report.total_sales}\nRevenue: {report.revenue}")

class XmlExporter(ReportVisitor):
  def visit_financial_report(self, report: FinancialReport):
    print(f'<?xml version="1.0" enconding="UTF-8"?>\n<salesReport>\n\t<revenue>{report.revenue}\n\t</revenue>\n\t<expenses>{report.expenses}\n\t</expenses>\n</salesReport>')

  def visit_inventory_report(self, report: InverntoryReport):
    print(f'<?xml version="1.0" enconding="UTF-8"?>\n<salesReport>\n\t<category>{report.category}\n\t</category>\n\t<total_items>{report.total_items}\n\t</total_items>\n</salesReport>')

  def visit_sales_report(self, report: SalesReport):
    print(f'<?xml version="1.0" enconding="UTF-8"?>\n<salesReport>\n\t<total_sales>{report.total_sales}\n\t</total_sales>\n\t<revenue>{report.revenue}\n\t</revenue>\n</salesReport>')

class HtmlExporter(ReportVisitor):
  def visit_financial_report(self, report: FinancialReport):
    print(f'<body>\n<h1>Financial Report</h1>\n<p>Revenue: {report.revenue}</p>\n<p>Expenses: {report.expenses}</p>\n</body>')

  def visit_inventory_report(self, report: InverntoryReport):
    print(f'<body>\n<h1>Financial Report</h1>\n<p>Category: {report.category}</p>\n<p>Total items: {report.total_items}</p>\n</body>')

  def visit_sales_report(self, report: SalesReport):
    print(f'<body>\n<h1>Financial Report</h1>\n<p>Total sales: {report.total_sales}</p>\n<p>Revenue: {report.revenue}</p>\n</body>')

def main():
  pdf = PdfExporter()
  xml = XmlExporter()
  html = HtmlExporter()

  financial = FinancialReport(120000, 40000)
  inventory = InverntoryReport("Hardware", 2000)
  sales = SalesReport(4200, 58000)

  financial.accept(pdf)

  print()

  inventory.accept(xml)

  print()

  sales.accept(html)



if __name__ == "__main__":
  main()
