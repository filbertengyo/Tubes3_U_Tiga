from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QMessageBox, QGroupBox, QFrame, QScrollArea)
from PyQt6.QtGui import QFont, QDesktopServices
from PyQt6.QtCore import QUrl, Qt
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
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("SummaryScrollArea")
        
        container_widget = QWidget()
        self.details_layout = QVBoxLayout(container_widget)
        self.details_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll_area.setWidget(container_widget)
        main_layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        back_button = QPushButton("< Back to Search")
        back_button.clicked.connect(self.controller.show_search_page)
        view_cv_button = QPushButton("View Original CV")
        view_cv_button.clicked.connect(self.on_view_cv)
        
        button_layout.addStretch()
        button_layout.addWidget(view_cv_button)
        button_layout.addWidget(back_button)
        main_layout.addLayout(button_layout)

    def _create_section_group(self, title):
        """Helper to create a styled QGroupBox for each section."""
        group_box = QGroupBox(title)
        layout = QVBoxLayout(group_box)
        layout.setSpacing(10)
        return group_box, layout

    def _create_info_entry(self, title, subtitle="", description=""):
        """Helper to create a styled entry for Job History or Education."""
        frame = QFrame()
        frame.setObjectName("InfoEntryFrame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 5, 10, 5)

        title_label = QLabel(title)
        title_label.setFont(QFont("Helvetica", 11, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setObjectName("SubtitleLabel")
            layout.addWidget(subtitle_label)

        if description:
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
            
        return frame
    
    def _clear_layout(self, layout):
        """Removes all widgets from a layout."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_data(self, data):
        self.applicant_data = data
        self._clear_layout(self.details_layout)
        
        full_text = self.applicant_data.get('full_profile_text', '')
        extractor = RegexExtractor(full_text)
        details = extractor.extract_all()

        # Identity Section
        name = f"{self.applicant_data.get('first_name', '')} {self.applicant_data.get('last_name', '')}".strip()
        identity_frame = QFrame()
        identity_frame.setObjectName("IdentityFrame")
        identity_layout = QVBoxLayout(identity_frame)
        name_label = QLabel(name)
        name_label.setFont(QFont("Helvetica", 16, QFont.Weight.Bold))
        name_label.setObjectName("SummaryName")
        
        # Create a grid-like layout for details
        details_layout_inner = QVBoxLayout()
        details_layout_inner.addWidget(QLabel(f"<b>Birthdate:</b> {self.applicant_data.get('date_of_birth', 'N/A')}"))
        details_layout_inner.addWidget(QLabel(f"<b>Address:</b> {self.applicant_data.get('address', 'N/A')}"))
        details_layout_inner.addWidget(QLabel(f"<b>Phone:</b> {self.applicant_data.get('phone', 'N/A')}"))
        
        identity_layout.addWidget(name_label)
        identity_layout.addLayout(details_layout_inner)
        self.details_layout.addWidget(identity_frame)
        
        # Skills Section
        skills_group, skills_layout = self._create_section_group("Skills")
        skills_tags_layout = QHBoxLayout()
        skills_tags_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        skills = details.get('skills', [])
        if skills:
            for skill in skills:
                skill_tag = QPushButton(skill)
                skill_tag.setObjectName("SkillTag")
                skill_tag.setEnabled(False)
                skills_tags_layout.addWidget(skill_tag)
        else:
            skills_tags_layout.addWidget(QLabel("No skills found."))
            
        skills_layout.addLayout(skills_tags_layout)
        self.details_layout.addWidget(skills_group)

        # Job History Section
        history_group, history_layout = self._create_section_group("Job History")
        experience = details.get('experience', [])
        if experience:
            for item in experience:
                # This is a simple parser, can be improved
                parts = item.split('\n')
                title = parts[0]
                subtitle = parts[1] if len(parts) > 1 else ""
                history_layout.addWidget(self._create_info_entry(title, subtitle))
        else:
            history_layout.addWidget(QLabel("No job history found."))
        self.details_layout.addWidget(history_group)

        # Education Section
        education_group, education_layout = self._create_section_group("Education")
        education = details.get('education', [])
        if education:
            for item in education:
                parts = item.split('\n')
                title = parts[0]
                subtitle = parts[1] if len(parts) > 1 else ""
                education_layout.addWidget(self._create_info_entry(title, subtitle))
        else:
            education_layout.addWidget(QLabel("No education history found."))
        self.details_layout.addWidget(education_group)


    def on_view_cv(self):
        cv_path = self.applicant_data.get('cv_path')
        if cv_path and os.path.exists(cv_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(cv_path))
        else:
            QMessageBox.critical(self, "File Not Found", f"The CV file could not be found at:\n{cv_path}")
