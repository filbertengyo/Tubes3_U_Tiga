import os
import sys
from PyQt6.QtCore import QDir
from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow
import faulthandler

faulthandler.enable()

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))        
    QDir.addSearchPath('icon', os.path.join(root, 'icon'))
    app = QApplication(sys.argv)

    # Load Stylesheet
    try:
        with open("style.css", "r") as f:
            style = f.read()
            app.setStyleSheet(style)
            print("Stylesheet loaded successfully.")
    except FileNotFoundError:
        print("Stylesheet file 'style.qss' not found. Using default styles.")

    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())