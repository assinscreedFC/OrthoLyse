import os
import sys

from PySide6.QtCore import QUrl
from PySide6.QtGui import QFontDatabase, QFont, QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer, QMediaPlayer

class PlayerController:
    """Contrôleur global pour gérer la navigation"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PlayerController, cls).__new__(cls)
            cls._instance.parent = None
        return cls._instance

    def set_controllers(self, file_path):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(file_path))
        self.is_playing = False
        self.player.stop()
        self.duration = 0
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.slider.valueChanged.connect(self.seek_position)  # Connect the slider to seek position
        # Connecter la vérification de la fin de l'audio
        self.player.mediaStatusChanged.connect(self.handle_media_status)

    def toggle_play_pause(self):
        if not self.is_playing:
            self.player.play()
            self.play_pause_button.setIcon(QIcon("./assets/SVG/pause.svg"))
        else:
            self.player.pause()
            self.play_pause_button.setIcon(QIcon("./assets/SVG/play_arrow.svg"))
        self.is_playing = not self.is_playing

    def rewind_10s(self):
        new_pos = max(self.player.position() - 10000, 0)
        self.player.setPosition(new_pos)

    def forward_10s(self):
        new_pos = min(self.player.position() + 10000, self.player.duration())
        self.player.setPosition(new_pos)

    def update_position(self, position):
        if self.duration > 0:
            self.slider.blockSignals(True)
            progress = int(position / self.duration * 100)
            self.slider.setValue(progress)
            self.slider.blockSignals(False)
        current_sec = position // 1000
        mm, ss = divmod(current_sec, 60)
        self.left_time_label.setText(f"{mm:02d}:{ss:02d}")

    def update_duration(self, dur):
        self.duration = dur
        total_sec = dur // 1000
        mm, ss = divmod(total_sec, 60)
        self.right_time_label.setText(f"{mm:02d}:{ss:02d}")

    def seek_position(self, slider_value):
        if self.duration > 0:
            new_pos = int(slider_value / 100 * self.duration)
            self.player.setPosition(new_pos)



    def handle_media_status(self, status):
        """
        Vérifie si la lecture est terminée.
        Si c'est le cas, remet le bouton Play et réinitialise la position.
        """
        from PySide6.QtMultimedia import QMediaPlayer
        if status == QMediaPlayer.EndOfMedia:
            # Remettre le bouton Play et réinitialiser la position de lecture
            self.play_pause_button.setIcon(QIcon("./assets/SVG/play_arrow.svg"))
            self.is_playing = False
            self.player.setPosition(0)

    def set_font(self, font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print("Erreur de chargement de police")
            return QFont(), ""
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 24)
        return font, font_family
