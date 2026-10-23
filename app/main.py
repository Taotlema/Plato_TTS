'''
Author: Ayemhenre Isikhuemhen
Date: 2026-10-18
LastEditors: AI
File Description: Central nerve of Plato it does two things, finds app and boots up the main window.
'''

# imports
import sys # command line arguments
from pathlib import Path # file/directory navigation
from PyQt6.QtWidgets import QApplication # PyQT
from app.ui.main_window import MainWindow # main_window file from app

# Import path: Python finds application folder and compile
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Main Function: Boot up the main window
def main():
    qt_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(qt_app.exec())


if __name__ == "__main__":
    main()