from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal, Qt

class ResultCard(QFrame):
    """
    A custom widget that displays a single applicant's search result in a card format.
    It emits signals when its action buttons are clicked.
    """
    # Custom signal
    summary_requested = pyqtSignal(dict)
    view_cv_requested = pyqtSignal(str)

    def __init__(self, applicant_data: dict, parent=None):
        super().__init__(parent)
        self.setObjectName("ResultCard")
        self.applicant_data = applicant_data
        self.init_ui()

    def init_ui(self):
        self.setFrameShape(QFrame.Shape.StyledPanel) # Provides a border and background
        self.setFrameShadow(QFrame.Shadow.Raised) # Adds a shadow effect
        self.setMinimumHeight(120)

        # Main Layout
        main_layout = QVBoxLayout(self)
        
        # Top Section (Name and Match Count)
        top_layout = QHBoxLayout()
        
        name_label = QLabel(self.applicant_data.get('name', 'Unknown Applicant'))
        name_label.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        top_layout.addWidget(name_label)
        
        top_layout.addStretch()
        
        match_count = self.applicant_data.get('match_count', 0)
        match_label = QLabel(f"{match_count} Matches")
        top_layout.addWidget(match_label)
        
        main_layout.addLayout(top_layout)

        # Middle Section (Matched Keywords)
        keywords = self.applicant_data.get('matched_keywords', {})
        keywords_text = "Found on: " + ", ".join(keywords.keys())
        keywords_label = QLabel(keywords_text)
        keywords_label.setWordWrap(True)
        main_layout.addWidget(keywords_label)
        
        main_layout.addStretch()

        # Bottom Section (Action Buttons)
        button_layout = QHBoxLayout()
        button_layout.addStretch() # Pushes buttons to the right

        summary_button = QPushButton("View Summary")
        summary_button.setCursor(Qt.CursorShape.PointingHandCursor)
        summary_button.clicked.connect(self.emit_summary_request)
        button_layout.addWidget(summary_button)
        
        view_cv_button = QPushButton("View CV File")
        view_cv_button.setCursor(Qt.CursorShape.PointingHandCursor)
        view_cv_button.clicked.connect(self.emit_view_cv_request)
        button_layout.addWidget(view_cv_button)

        main_layout.addLayout(button_layout)

    def emit_summary_request(self):
        self.summary_requested.emit(self.applicant_data)

    def emit_view_cv_request(self):
        self.view_cv_requested.emit(self.applicant_data.get('cv_path', ''))