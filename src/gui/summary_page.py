from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox, QGroupBox)
from PyQt6.QtGui import QFont, QDesktopServices
from PyQt6.QtCore import QUrl
import os
from src.extractor.regex_extractor import RegexExtractor

class SummaryPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.applicant_data = {}
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        self.title_label = QLabel("CV Summary")
        self.title_label.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        main_layout.addWidget(self.title_label)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setFont(QFont("Courier", 10))
        main_layout.addWidget(self.details_text)

        button_layout = QHBoxLayout()
        back_button = QPushButton("< Back to Search")
        back_button.clicked.connect(self.controller.show_search_page)
        view_cv_button = QPushButton("View Original CV")
        view_cv_button.clicked.connect(self.on_view_cv)
        
        button_layout.addStretch()
        button_layout.addWidget(view_cv_button)
        button_layout.addWidget(back_button)
        main_layout.addLayout(button_layout)

    def load_data(self, data):
        self.applicant_data = data
        name = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
        self.title_label.setText(f"CV Summary: {name}")

        extractor = RegexExtractor(data.get('full_profile_text', ''))
        details = extractor.extract_all()

        skills = "\n\t- ".join(details.get('skills', ['Not found']))
        education = "\n\t- ".join(details.get('education', ['Not found']))
        experience = "\n\t- ".join(details.get('experience', ['Not found']))

        display_text = f"""
NAME: {name}
EMAIL: {data.get('email', 'N/A')}
PHONE: {data.get('phone', 'N/A')}

==================== SKILLS ====================
\t- {skills}

================== EDUCATION ===================
\t- {education}

================== EXPERIENCE ==================
\t- {experience}
        """
        self.details_text.setText(display_text)

    def on_view_cv(self):
        cv_path = self.applicant_data.get('cv_path')
        if cv_path and os.path.exists(cv_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(cv_path))
        else:
            QMessageBox.critical(self, "File Not Found", f"The CV file could not be found at:\n{cv_path}")
