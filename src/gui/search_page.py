import sys
import math
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QRadioButton, QComboBox, QGroupBox, 
                             QMessageBox, QScrollArea, QSpinBox)
from PyQt6.QtGui import QFont, QDesktopServices
from PyQt6.QtCore import QUrl, Qt, QThread
import os

from .result_card import ResultCard 
from src.logic.search_worker import SearchWorker

class SearchPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # State Variables
        self.all_results = []
        self.current_page = 1
        self.results_per_page = 10
        self.search_thread = None
        self.search_worker = None
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("CV Analyzer App")
        title_label.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        main_layout.addWidget(title_label)

        # Search Criteria GroupBox
        input_group = QGroupBox()
        input_layout = QVBoxLayout(input_group)

        # Keywords Layout
        keywords_layout = QHBoxLayout()
        keywords_layout.addWidget(QLabel("Keywords (comma-separated):"))
        self.keywords_entry = QLineEdit()
        self.keywords_entry.setPlaceholderText("e.g., Python, React, SQL")
        keywords_layout.addWidget(self.keywords_entry)
        input_layout.addLayout(keywords_layout)
        
        options_layout = QVBoxLayout()
        
        # Algorithm Group
        options_layout.addWidget(QLabel("Algorithm:"))
        self.kmp_radio = QRadioButton("KMP")
        self.bm_radio = QRadioButton("BM")
        self.aho_radio = QRadioButton("Aho-Corasick")
        self.aho_radio.setChecked(True)
        options_layout.addWidget(self.kmp_radio)
        options_layout.addWidget(self.bm_radio)
        options_layout.addWidget(self.aho_radio)
        
        dropdown_layout = QHBoxLayout()
        
        # Top Matches Group
        dropdown_layout.addWidget(QLabel("Top Matches:"))
        self.top_n_spinbox = QSpinBox()
        self.top_n_spinbox.setMinimum(1)
        self.top_n_spinbox.setMaximum(1000)
        self.top_n_spinbox.setValue(25)
        dropdown_layout.addWidget(self.top_n_spinbox)
        
        # Results Per Page Group
        dropdown_layout.addWidget(QLabel("Results Per Page:"))
        self.results_per_page_combo = QComboBox()
        self.results_per_page_combo.addItems(["5", "10", "20", "50"])
        self.results_per_page_combo.setCurrentText("10")
        dropdown_layout.addWidget(self.results_per_page_combo)
        
        options_layout.addLayout(dropdown_layout)

        input_layout.addLayout(options_layout)
        main_layout.addWidget(input_group)
        
        # Search and Cancel Buttons
        search_button_layout = QHBoxLayout()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.on_search_clicked)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel_clicked)
        self.cancel_button.setEnabled(False)
        search_button_layout.addWidget(self.search_button)
        search_button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(search_button_layout)


        # Results GroupBox
        results_group = QGroupBox()
        results_group_layout = QVBoxLayout(results_group)
        main_layout.addWidget(results_group, 1)

        self.summary_label = QLabel("Ready to search.")
        results_group_layout.addWidget(self.summary_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.card_container = QWidget()
        self.card_layout = QVBoxLayout(self.card_container)
        self.card_layout.setSpacing(10)
        self.card_layout.addStretch()

        scroll_area.setWidget(self.card_container)
        results_group_layout.addWidget(scroll_area)

        # Pagination Controls
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("< Previous")
        self.prev_button.setEnabled(False)
        self.prev_button.clicked.connect(self.go_to_prev_page)
        
        self.page_label = QLabel("Page 1 / 1")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.next_button = QPushButton("Next >")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.go_to_next_page)
        
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_button)
        pagination_layout.addStretch()
        
        results_group_layout.addLayout(pagination_layout)

    def on_search_clicked(self):
        keywords = [k.strip() for k in self.keywords_entry.text().split(',') if k.strip()]
        if not keywords:
            QMessageBox.warning(self, "Input Error", "Please enter at least one keyword.")
            return
        
        if self.kmp_radio.isChecked():
            algorithm = "KMP"
        elif self.bm_radio.isChecked():
            algorithm = "BM"
        else:
            algorithm = "AhoCorasick"
            
        top_n = self.top_n_spinbox.value()
        self.results_per_page = int(self.results_per_page_combo.currentText())

        self.search_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.summary_label.setText("Searching... Please wait.")
        
        self.search_thread = QThread()
        self.search_worker = SearchWorker(keywords, algorithm, top_n)
        self.search_worker.moveToThread(self.search_thread)
        
        self.search_thread.started.connect(self.search_worker.run)
        self.search_worker.search_finished.connect(self.on_search_finished)
        self.search_worker.search_error.connect(self.on_search_error)
        
        self.search_thread.start()

    def on_cancel_clicked(self):
        if self.search_worker:
            self.search_worker.cancel()
        if self.search_thread:
            self.search_thread.quit()
            self.search_thread.wait()
        self.summary_label.setText("Search cancelled.")
        self.search_button.setEnabled(True)
        self.cancel_button.setEnabled(False)

    def on_search_finished(self, results, exact_time, fuzzy_time):
        self.all_results = results
        time_text = f"Exact Match ({self.search_worker.algorithm}): {exact_time:.2f} ms"
        if fuzzy_time > 0:
            time_text += f" | Fuzzy Match: {fuzzy_time:.2f} ms"
        self.summary_label.setText(f"Found {len(self.all_results)} total results. {time_text}")
        
        self.search_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.current_page = 1
        self.update_page_display()
        
        self.search_thread.quit()
        self.search_thread.wait()

    def on_search_error(self, error_message):
        QMessageBox.critical(self, "Search Error", f"An unexpected error occurred: {error_message}")
        self.all_results = []
        self.search_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.summary_label.setText("Search failed.")
        
        self.search_thread.quit()
        self.search_thread.wait()
        
        self.update_page_display()

    def update_page_display(self):
        self.clear_layout(self.card_layout)

        total_results = len(self.all_results)
        if total_results == 0:
            self.page_label.setText("Page 0 / 0")
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
            no_results_label = QLabel("No matching applicants found.")
            self.card_layout.insertWidget(0, no_results_label)
            return

        total_pages = math.ceil(total_results / self.results_per_page)
        start_index = (self.current_page - 1) * self.results_per_page
        end_index = start_index + self.results_per_page
        
        page_results = self.all_results[start_index:end_index]

        for res_data in page_results:
            card = ResultCard(res_data)
            card.summary_requested.connect(self.handle_summary_request)
            card.view_cv_requested.connect(self.handle_view_cv_request)
            self.card_layout.insertWidget(self.card_layout.count() - 1, card)
        
        self.page_label.setText(f"Page {self.current_page} / {total_pages}")
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < total_pages)

    def go_to_prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_page_display()

    def go_to_next_page(self):
        total_pages = math.ceil(len(self.all_results) / self.results_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self.update_page_display()

    def clear_layout(self, layout):
        while layout.count() > 1:
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def handle_summary_request(self, data: dict):
        self.controller.show_summary_page(data)

    def handle_view_cv_request(self, cv_path: str):
        if cv_path and os.path.exists(cv_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(cv_path))
        else:
            QMessageBox.critical(self, "File Not Found", f"This is a dummy card. The CV file could not be found at:\n{cv_path}")