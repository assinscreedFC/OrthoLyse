from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout

from frontend.Widgets.AudioPlayer import AudioPlayer
from frontend.Widgets.Feuille import Feuille


class Transcription(QWidget):
    def __init__(self,text,mapping_data,path=None):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        from frontend.controllers.Menu_controllers import NavigationController

        self.controller = NavigationController()
        self.ui(text,mapping_data,path)

    def ui(self,text,mapping_data,path=None):

        self.path =path
        self.text=text
        self.mapping_data=mapping_data

        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        if self.controller.get_audio_player():
            self.audio_player = self.controller.get_audio_player()
        else:
            self.audio_player = AudioPlayer(self.path)
            self.controller.set_audio_player(self.audio_player)

        self.audio_player.position_en_secondes.connect(self.on_position_changed)

        self.feuille = Feuille("./assets/SVG/icone_file_text.svg", "Transcription", "Analyser", "Coriger",
                               "rgba(255, 255, 255, 255)", self.text)
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

    def hideEvent(self, event):
        super().hideEvent(event)
        if self.audio_player and self.audio_player.player and self.audio_player.is_playing==True:
            self.audio_player.toggle_play_pause()

    def test(self,event):
        self.feuille.setFixedSize((self.width() // 2), round(self.height() * 0.90))
        self.feuille.widget.setFixedSize(self.feuille.width(), self.feuille.height())
        #print(self.width(), self.height())