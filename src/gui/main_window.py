from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from .search_page import SearchPage
from .summary_page import SummaryPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CV Analyzer App")
        self.setGeometry(100, 100, 900, 700)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.search_page = SearchPage(self)
        self.summary_page = SummaryPage(self)

        self.stacked_widget.addWidget(self.search_page)
        self.stacked_widget.addWidget(self.summary_page)

        self.show_search_page()

    def show_search_page(self):
        self.stacked_widget.setCurrentWidget(self.search_page)

    def show_summary_page(self, data=None):
        if data:
            self.summary_page.load_data(data)
        self.stacked_widget.setCurrentWidget(self.summary_page)