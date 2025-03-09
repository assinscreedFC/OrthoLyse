from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QLabel

from frontend.Widgets.AudioPlayer import AudioPlayer
from frontend.Widgets.Feuille import Feuille
from frontend.controllers.Menu_controllers import NavigationController


class Transcription(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.controller = NavigationController()
        self.layout=QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.audio_player=AudioPlayer()
        self.feuille=Feuille()
        self.layout.addWidget(self.audio_player)
        self.layout.setSpacing(10)
        self.layout.addWidget(self.feuille)


        self.setLayout(self.layout)
