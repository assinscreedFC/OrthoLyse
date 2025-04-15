import sys
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame,QSizePolicy
from PySide6.QtGui import QPixmap, QFont, QPainter, QBrush, QPen, QColor
from PySide6.QtCore import Qt


class Informations(QWidget):
    def __init__(self):
        super().__init__()
        self.label_image = QLabel(self)
        self.label_image.setScaledContents(True)  # Pour que l'image suive la taille du QLabel


        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)  # Pas de marges

        self.layout.addWidget(self.label_image)
        self.setLayout(self.layout)

        self.pixmap = QPixmap("./assets/image/info.PNG")  # Charge ton image
        self.label_image.setPixmap(self.pixmap)



    def resizeEvent(self, event):
        if not self.pixmap.isNull():
            # Redimensionne l'image selon la nouvelle taille
            self.label_image.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        super().resizeEvent(event)