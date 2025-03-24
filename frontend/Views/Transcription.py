from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QLabel
import json
from backend.transcription import transcription
from frontend.Widgets.AudioPlayer import AudioPlayer
from frontend.Widgets.Feuille import Feuille


class Transcription(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        from frontend.controllers.Menu_controllers import NavigationController

        self.controller = NavigationController()
        self.ui()

    def ui(self):

        self.path = self.controller.get_file_transcription_path()
        if self.controller.get_text_transcription() is None:

            result=transcription(self.path, 0)
            self.text=result["text"]
            self.mapping_data=result["mapping"]
            self.controller.set_text_transcription(self.text)
            self.controller.set_mapping_data(self.mapping_data)
        else:
            print(("valider"))
            self.text = self.controller.get_text_transcription()
            self.mapping_data=self.controller.get_mapping_data()

        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.audio_player = AudioPlayer(self.path)
        self.audio_player.position_en_secondes.connect(self.on_position_changed)

        self.feuille = Feuille("./assets/SVG/icone_file_text.svg", "Transcription", "Transcrire", "Coriger",
                               "rgba(245, 245, 245, 0.85)", self.text)
        self.feuille.setObjectName("feuille")
        # self.feuille.setStyleSheet('QWidget#feuille{background-color: white; border-radius: 20px;border: 1px solid black}')
        self.layout.addWidget(self.audio_player)
        self.layout.setSpacing(10)
        self.layout.addWidget(self.feuille)

        self.setLayout(self.layout)

    def on_position_changed(self, current_time_s):
        """
        Slot: appelé par le signal du AudioPlayer.
        On surligne le segment du texte correspondant à current_time_s (secondes).
        """
        self.feuille.mettre_a_jour_surlignage(current_time_s, self.mapping_data)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        print("Nouvelle taille de Feuille :", self.width(), self.height())
        self.test(event)

    def test(self,event):
        self.feuille.setFixedSize((self.width() // 2), round(self.height() * 0.90))
        self.feuille.widget.setFixedSize(self.feuille.width(), self.feuille.height())
        #print(self.width(), self.height())