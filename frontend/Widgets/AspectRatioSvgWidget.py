from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QRect

class AspectRatioSvgWidget(QSvgWidget):
    def __init__(self, svg_file, parent=None):
        super().__init__(parent)
        self.load(svg_file)

    def paintEvent(self, event):
        painter = QPainter(self)
        renderer = self.renderer()
        if not renderer.isValid():
            return super().paintEvent(event)
        # Taille du widget et taille par défaut du SVG
        widget_rect = self.rect()
        svg_size = renderer.defaultSize()
        # Calcul du redimensionnement en conservant le ratio
        scaled_size = svg_size.scaled(widget_rect.size(), Qt.KeepAspectRatio)
        # Centrer le SVG dans le widget
        x = (widget_rect.width() - scaled_size.width()) // 2
        y = (widget_rect.height() - scaled_size.height()) // 2
        target_rect = QRect(x, y, scaled_size.width(), scaled_size.height())
        renderer.render(painter, target_rect)
