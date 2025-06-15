from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QMessageBox, QGroupBox, QFrame, QScrollArea
)
from PyQt6.QtGui import QFont, QDesktopServices
from PyQt6.QtCore import QUrl, Qt
import os


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
        group_box = QGroupBox(title)
        layout = QVBoxLayout(group_box)
        layout.setSpacing(10)
        return group_box, layout

    def _create_info_entry(self, title, subtitle="", description=""):
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
            desc_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            layout.addWidget(desc_label)

        return frame

    def _clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_data(self, data):
        print(data)
        self.applicant_data = data
        self._clear_layout(self.details_layout)

        # --- Identity Section ---
        identity_frame = QFrame()
        identity_frame.setObjectName("IdentityFrame")
        identity_layout = QVBoxLayout(identity_frame)

        name_label = QLabel(data.get('name', 'Unknown Applicant'))
        name_label.setFont(QFont("Helvetica", 16, QFont.Weight.Bold))
        name_label.setObjectName("SummaryName")

        details_layout_inner = QVBoxLayout()
        details_layout_inner.addWidget(QLabel(f"<b>Birthdate:</b> {data.get('date_of_birth', 'N/A')}"))
        details_layout_inner.addWidget(QLabel(f"<b>Address:</b> {data.get('address', 'N/A')}"))
        details_layout_inner.addWidget(QLabel(f"<b>Phone:</b> {data.get('phone_number', 'N/A')}"))

        identity_layout.addWidget(name_label)
        identity_layout.addLayout(details_layout_inner)
        self.details_layout.addWidget(identity_frame)

        # --- Extracted Info Section ---
        summary = data.get('summary', {})

        summary_group, summary_layout = self._create_section_group("Summary")

        summary_label = QLabel(summary)
        summary_label.setWordWrap(True)
        summary_layout.addWidget(summary_label)

        self.details_layout.addWidget(summary_group)

        # # --- Skills Section (as plain text) ---
        # skills_group, skills_layout = self._create_section_group("Consolidated Skills")
        # skills_text = summary.get('Consolidated_Skills', '').strip()
        # if skills_text:
        #     skills_label = QLabel(skills_text)
        #     skills_label.setWordWrap(True)
        #     skills_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        #     skills_layout.addWidget(skills_label)
        # else:
        #     skills_layout.addWidget(QLabel("No skills found or extracted."))
        # self.details_layout.addWidget(skills_group)

        # # --- Job History Section ---
        # history_group, history_layout = self._create_section_group("Job History")
        # experience = summary.get('Work_History', [])
        # if experience:
        #     for item in experience:
        #         title = item.get('Company', 'N/A')
        #         subtitle = f"({item.get('Date', 'N/A')})"
        #         description = item.get('Position', 'N/A')
        #         history_layout.addWidget(self._create_info_entry(title, subtitle, description))
        # else:
        #     history_layout.addWidget(QLabel("No job history found or extracted."))
        # self.details_layout.addWidget(history_group)

        # # --- Education Section ---
        # education_group, education_layout = self._create_section_group("Education")
        # education = summary.get('Education', {})
        # if education and education.get('School'):
        #     title = education.get('School', 'N/A')
        #     subtitle = education.get('Degree', 'N/A')
        #     description = f"Years: {education.get('Years', 'N/A')}\nFull Text: {education.get('Full_Text', 'N/A')}"
        #     education_layout.addWidget(self._create_info_entry(title, subtitle, description))
        # else:
        #     education_layout.addWidget(QLabel("No education history found or extracted."))
        # self.details_layout.addWidget(education_group)

        # # Optional Sections: Summary, Highlights, Accomplishments
        # optional_sections = {
        #     "Summary": summary.get('Summary'),
        #     "Highlights": summary.get('Highlights'),
        #     "Accomplishments": summary.get('Accomplishments')
        # }

        # for section_name, content in optional_sections.items():
        #     if content:
        #         section_group, section_layout = self._create_section_group(section_name)
        #         label = QLabel(content)
        #         label.setWordWrap(True)
        #         label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        #         section_layout.addWidget(label)
        #         self.details_layout.addWidget(section_group)

    def on_view_cv(self):
        cv_path = self.applicant_data.get('cv_path')
        if cv_path and os.path.exists(cv_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(cv_path))
        else:
            QMessageBox.critical(self, "File Not Found", f"The CV file could not be found at:\n{cv_path}")