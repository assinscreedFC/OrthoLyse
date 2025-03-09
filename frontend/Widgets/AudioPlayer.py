import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QSlider, QPushButton, QSizePolicy, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont, QPalette, QColor

from frontend.Widgets.HoverSlider import HoverSlider
from frontend.controllers.Player_controllers import PlayerController


class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.controller=PlayerController()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.font,self.font_family=self.controller.set_font("./assets/Fonts/Inter,Montserrat,Roboto/Inter/static/Inter_24pt-SemiBold.ttf")

        self.inner_widgets()
        self.controller.set_controllers("D:/disc E/vscode pyhton/python/upc projet test/audio.wav")
        self.slots()

    def inner_widgets(self):
        # Créer un widget principal pour les éléments internes
        self.inner_widget = QWidget(self)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Configurer le style et les propriétés du widget
        self.inner_widget.setAutoFillBackground(True)
        self.inner_widget.setFixedSize((642 // 2)-40, 100) #j'ai mit ca par rapport a la plus petit tailler d'ecran il feras un peu moin de la moitier de l'ecran pour pouvoir le diviser correctemenrt avec la zone de texte

        self.inner_widget.setStyleSheet(f"""
            background-color: #ffffff;
            border-radius: {50 // 4}px;
        """)
        self.inner_widget.setObjectName("AudioPlayer")

        # Créer un layout principal pour le widget
        self.main_layout = QVBoxLayout(self.inner_widget)
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Ajouter les composants dans le layout principal
        self.top_part()
        self.main_layout.setSpacing(5)  # Espacement entre les sections
        self.bottom_part()

        # Attribuer le layout principal au widget
        self.inner_widget.setLayout(self.main_layout)

    def timer_label(self):
        time_label = QLabel("00:00", self.inner_widget)
        time_label.setStyleSheet("color: #000;")  # texte gris clair
        time_label.setFont(QFont(self.font_family, 10))
        return time_label

    def top_part(self):
        """
            !: mettre un getter pour recuper l'url de l'audio
        """

        self.slider=HoverSlider(Qt.Horizontal,self.inner_widget)
        self.slider.setValue(0)
        self.slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding
                                  )
        self.slider.setFixedWidth((642//4))
        self.slider.setRange(0, 100)#!mettre un getter remplacer le 100 par la durer de l'audio

        self.left_time_label = self.timer_label()
        self.right_time_label = self.timer_label()

        layoutH = QHBoxLayout()
        layoutH.setAlignment(Qt.AlignCenter)
        layoutH.setSpacing(10)
        layoutH.addWidget(self.left_time_label)
        layoutH.addWidget(self.slider,alignment=Qt.AlignCenter)
        layoutH.addWidget(self.right_time_label)

        self.main_layout.addLayout(layoutH)

        # Placer ces références dans le contrôleur
        self.controller.slider = self.slider
        self.controller.left_time_label = self.left_time_label
        self.controller.right_time_label = self.right_time_label



    def boutton(self,file_path):
        button = QPushButton()
        button.setIcon(QIcon(file_path))
        button.setIconSize((self.size() / 15))
        button.setFixedSize(40, 40)
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet("""
                            QPushButton {
                                background-color: #fff;
                                border-radius: 19px;
                            }
                            QPushButton:hover {
                                background-color: #CCC;
                            }
                        """)
        return button

    def bottom_part(self):
        # --- Barre du bas : Boutons ---
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(30)
        bottom_layout.setAlignment(Qt.AlignCenter)


        # Bouton retour -10s
        self.rewind_button = self.boutton("./assets/SVG/replay-10.svg")
        # Bouton central Play/Pause
        self.play_pause_button = self.boutton("assets/SVG/play_arrow.svg")
        # Bouton avance +10s
        self.forward_button = self.boutton("assets/SVG/forward-10.svg")


        bottom_layout.addWidget(self.rewind_button)
        bottom_layout.addWidget(self.play_pause_button)
        bottom_layout.addWidget(self.forward_button)
        self.main_layout.addLayout(bottom_layout)

        # Placer la référence du bouton Play/Pause dans le contrôleur
        self.controller.play_pause_button = self.play_pause_button
        pass

    def slots(self):

        self.slider.sliderMoved.connect(self.controller.seek_position)
        self.play_pause_button.clicked.connect(self.controller.toggle_play_pause)
        self.rewind_button.clicked.connect(self.controller.rewind_10s)
        self.forward_button.clicked.connect(self.controller.forward_10s)
