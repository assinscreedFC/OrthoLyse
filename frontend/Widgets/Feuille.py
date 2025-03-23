import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QSlider, QPushButton, QSizePolicy, QLabel, QMenu, QPlainTextEdit, QGraphicsBlurEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont, QPalette, QColor, QPixmap


class Feuille(QWidget):
    """
    Classe représentant un widget avec une interface de transcription comprenant :
    - Un titre avec une icône
    - Une zone de texte pour afficher ou éditer la transcription
    - Deux boutons pour valider ou corriger la transcription
    """

    def __init__(self, icone="./assets/SVG/icone_file_text.svg", text_top="Transcrire",
                 left_button_text="Transcrire", right_butto_text="Coriger",
                 bg_color="rgba(245, 245, 245, 0.85)", plain_text=""):
        """
        Initialise la feuille de transcription avec une icône, un titre, des boutons et un fond personnalisés.

        Args:
            icone (str): Le chemin de l'icône à afficher en haut du widget.
            text_top (str): Le titre de la section en haut du widget.
            left_button_text (str): Le texte du bouton gauche.
            right_butto_text (str): Le texte du bouton droit.
            bg_color (str): La couleur de fond du widget.
            plain_text (str): Le texte initial de la transcription.
        """
        super().__init__()
        self.icone = icone
        self.text_top = text_top
        self.left_button_text = left_button_text
        self.right_butto_text = right_butto_text
        self.bg_color = bg_color

        from frontend.controllers.Menu_controllers import NavigationController
        self.controller = NavigationController()
        self.plain_text = plain_text
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedSize((self.width() // 2), self.height() * 0.80)

        # Définition de la police
        self.font, self.font_family = self.controller.set_font(
            './assets/Fonts/Inter,Montserrat,Roboto/Inter/static/Inter_24pt-SemiBold.ttf'
        )
        self.inner_widget()

    def inner_widget(self):
        """
        Crée et configure le widget intérieur contenant l'interface utilisateur de la feuille.
        """
        self.widget = QWidget(self)
        self.widget.setFixedSize(self.width(), self.height())
        self.widget.setStyleSheet(f"""
            #feuille {{
                background-color: {self.bg_color};
                border-radius: 20px;
                border: 2px solid #15B5D4;
            }}
        """)
        self.widget.setObjectName("feuille")
        self.widget.setAutoFillBackground(True)

        # Créer un layout principal pour le widget
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(20, 10, 20, 20)

        self.top()
        self.body()
        self.bottom()

        # Attribuer le layout principal au widget
        self.widget.setLayout(self.main_layout)

    def top(self):
        """
        Crée et configure la section supérieure du widget : icône et titre.
        """
        self.icon_label = QLabel()
        # Remplace par ton icône, ex: "assets/transcription_icon.png"
        pix = QPixmap(self.icone).scaled(18, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(pix)

        # Titre
        self.title_label = QLabel(self.text_top)
        self.title_label.setStyleSheet("color: #4C4C4C;")
        self.title_label.setFont(QFont(self.font_family, 14))

        label_layout = QHBoxLayout()
        label_layout.addWidget(self.icon_label)
        label_layout.addWidget(self.title_label)
        label_layout.addStretch(1)
        label_layout.setContentsMargins(10, 0, 0, 0)
        self.main_layout.addLayout(label_layout)

    def body(self):
        """
        Crée et configure la section centrale du widget : zone de texte pour la transcription.
        """
        if self.controller.get_text_transcription() is not None:
            self.text_edit = QPlainTextEdit(self.controller.get_text_transcription())
        else:
            self.text_edit = QPlainTextEdit("")

        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont(self.font_family, 10))

        self.text_edit.setStyleSheet("background-color: #fafafa;color: black; border-radius: 10px;"
                                     "padding-top: 5px;padding-bottom: 5px;padding-left: 10px;padding-right: 10px;")
        self.main_layout.addWidget(self.text_edit)

    def bottom(self):
        """
        Crée et configure la section inférieure du widget : boutons gauche et droit.
        """
        self.right_boutton = self.boutton(self.widget, self.right_butto_text, "#15B5D4", "#15B5D4", "#FFFFFF")
        self.left_boutton = self.boutton(self.widget, self.left_button_text, "#FFFFFF", "#15B5D4", "#15B5D4")

        # Connecter les boutons à leurs actions respectives
        if self.right_butto_text == "Coriger":
            self.right_boutton.clicked.connect(lambda: self.controller.change_page("CTanscription"))
        elif self.right_butto_text == "Annuler":
            self.right_boutton.clicked.connect(lambda: self.controller.change_page("Transcription"))
        if self.left_button_text == "Valider":
            self.controller.set_text_transcription(self.text_edit.toPlainText())
            self.left_boutton.clicked.connect(
                lambda: (self.controller.set_text_transcription(self.text_edit.toPlainText()),
                         self.controller.change_page("Transcription"))
            )

        label_layout = QHBoxLayout()
        label_layout.addStretch(1)
        label_layout.addWidget(self.right_boutton)
        label_layout.addWidget(self.left_boutton)
        label_layout.setContentsMargins(0, 0, 10, 0)
        self.main_layout.addLayout(label_layout)

    def boutton(self, parent=None, text="Boutton", color_text="#FFFFFF", color_br="#B3B3B3", color_bg="#B5B5B5"):
        """
        Crée un bouton personnalisé avec un texte centré et des couleurs personnalisées.

        Args:
            parent (QWidget): Le widget parent auquel le bouton appartient.
            text (str): Le texte affiché sur le bouton.
            color_text (str): La couleur du texte.
            color_br (str): La couleur de la bordure du bouton.
            color_bg (str): La couleur de fond du bouton.

        Returns:
            QPushButton: Le bouton créé.
        """
        # Créer le QPushButton
        boutton_init = QPushButton(parent)
        boutton_init.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        boutton_init.setMinimumSize(90, 25)  # Ajustez les dimensions si nécessaire

        boutton_init.setStyleSheet(f"""
                background-color: {color_bg};
                border-radius: 12px;
                border: 2px solid {color_br};
            """)
        boutton_init.setCursor(Qt.PointingHandCursor)

        # Créer un QLabel à l'intérieur du bouton pour le texte centré
        label = QLabel(text, boutton_init)
        label.setStyleSheet(f"color: {color_text}; border: none;")
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        label.setAlignment(Qt.AlignCenter)  # Centrage horizontal et vertical
        self.font, self.font_family = self.controller.set_font(
            "./assets/Fonts/Inter,Montserrat,Roboto/Inter/static/Inter_24pt-SemiBold.ttf")
        self.font = QFont(self.font_family, 10)

        label.setFont(self.font)

        # Utiliser un layout vertical pour ajouter le QLabel dans le QPushButton
        layout = QHBoxLayout(boutton_init)
        layout.addWidget(label)  # Ajouter le QLabel au centre du bouton
        layout.setContentsMargins(0, 0, 0, 0)  # Marges à zéro pour remplir tout l'espace du QPushButton
        layout.setSpacing(0)

        return boutton_init
