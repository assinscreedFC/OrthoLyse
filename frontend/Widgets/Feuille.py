import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QSlider, QPushButton, QSizePolicy, QLabel, QMenu
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont, QPalette, QColor
from frontend.controllers.Menu_controllers import NavigationController


class Feuille(QWidget):
    def __init__(self):
        super().__init__()
        self.controller=NavigationController()