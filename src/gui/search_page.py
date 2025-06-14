import sys
import math
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QRadioButton, QComboBox, QGroupBox, 
                             QMessageBox, QScrollArea, QSpinBox)
from PyQt6.QtGui import QFont, QDesktopServices
from PyQt6.QtCore import QUrl, Qt
import os
import random

from .result_card import ResultCard 

# from src.logic.search_handler import perform_search 

class SearchPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # State Variables
        self.all_results = []
        self.current_page = 1
        self.results_per_page = 10
        
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
        self.kmp_radio.setChecked(True)
        options_layout.addWidget(self.kmp_radio)
        options_layout.addWidget(self.bm_radio)
        
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
        
        # Search Button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.on_search_clicked)
        main_layout.addWidget(self.search_button)

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
        
        top_n = self.top_n_spinbox.value()
        self.results_per_page = int(self.results_per_page_combo.currentText())

        # DUMMY DATA GENERATION
        self.all_results = []
        num_dummy_results = top_n 
        first_names = ["Farhan", "Ariel", "Aland", "Ciko", "Haikal", "Rafi", "Eka", "Ikhwan"]
        for i in range(num_dummy_results):
            num_matched = random.randint(1, len(keywords))
            matched_kws = random.sample(keywords, k=num_matched)
            dummy_result = {
                'applicant_id': 100 + i,
                'name': f"{random.choice(first_names)} - Applicant #{i+1}",
                'cv_path': f"C:/path/to/dummy_cv_{i}.pdf",
                'match_count': len(matched_kws),
                'matched_keywords': {kw: random.randint(1, 3) for kw in matched_kws},
                'first_name': 'Dummy', 'last_name': f'User {i+1}',
                'email': f'dummy{i+1}@test.com', 'phone': '08123456789',
                'full_profile_text': f'This is the full text for applicant {i+1}. Skills include {", ".join(matched_kws)}.'
            }
            self.all_results.append(dummy_result)
        
        self.summary_label.setText(f"Found {len(self.all_results)} total results.")
        self.current_page = 1
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
