import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QSlider, QPushButton, QSizePolicy, QLabel, QMenu, QPlainTextEdit, QGraphicsBlurEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont, QPalette, QColor, QPixmap
from frontend.controllers.Menu_controllers import NavigationController


class Feuille(QWidget):
    def __init__(self,icone=None,text_top=None):
        super().__init__()
        self.controller=NavigationController()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedSize((self.width()//2), self.height()*0.80)
        self.font,self.font_family=self.controller.set_font('./assets/Fonts/Inter,Montserrat,Roboto/Inter/Inter-VariableFont_opsz,wght.ttf')
        self.inner_widget()

    def inner_widget(self):
        self.widget=QWidget(self)
        self.widget.setFixedSize(self.width(),self.height())
        self.widget.setStyleSheet("""
            #feuille {
                background-color: rgba(245, 245, 245, 0.85);
                border-radius: 20px;
                border: 1px solid #7B7C7C;
            }
        """)
        self.widget.setObjectName("feuille")
        self.widget.setAutoFillBackground(True)

        # Créer un layout principal pour le widget
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(20,10,20,20)

        self.top()
        self.body()
        self.bottom()


        # Attribuer le layout principal au widget
        self.widget.setLayout(self.main_layout)


    def top(self):

        self.icon_label = QLabel()
        # Remplace par ton icône, ex: "assets/transcription_icon.png"
        pix = QPixmap("./assets/SVG/icone_file_text.svg").scaled(18, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(pix)

        # Titre
        self.title_label = QLabel("Transcription…")
        self.title_label.setStyleSheet("color: #4C4C4C;")
        self.title_label.setFont(QFont(self.font_family, 14))
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.icon_label)
        label_layout.addWidget(self.title_label)
        label_layout.addStretch(1)
        label_layout.setContentsMargins(10,0,0,0)
        self.main_layout.addLayout(label_layout)

    def body(self):
        self.text_edit = QPlainTextEdit("helloooooooooooooooooo")
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont(self.font_family,10))

        self.text_edit.setStyleSheet("background-color: #fafafa;color: black; border-radius: 10px;"
                                     "padding-top: 5px;padding-bottom: 5px;padding-left: 10px;padding-right: 10px;")
        self.main_layout.addWidget(self.text_edit)

    def bottom(self):
        self.right_boutton=self.boutton(self.widget,"Annuler","#15B5D4","#15B5D4","#FFFFFF")
        self.left_boutton=self.boutton( self.widget,"transcrire","#FFFFFF","#15B5D4","#15B5D4")

        label_layout = QHBoxLayout()
        label_layout.addStretch(1)
        label_layout.addWidget(self.right_boutton)
        label_layout.addWidget(self.left_boutton)


        label_layout.setContentsMargins(0, 0, 10, 0)
        self.main_layout.addLayout(label_layout)

    def boutton(self,parent=None,text="Boutton",color_text="#FFFFFF",color_br="#B3B3B3",color_bg="#B5B5B5"):
        # Créer le QPushButton
        boutton_init = QPushButton(parent)
        boutton_init.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        boutton_init.setMinimumSize(90, 25)  # Ajustez les dimensions si nécessaire
        #boutton_init.setMaximumSize(100, 40)

        boutton_init.setStyleSheet(f"""
                background-color: {color_bg};
                border-radius: 12px;
                border: 2px solid {color_br};
            """)
        boutton_init.setCursor(Qt.PointingHandCursor)

        # Créer un QLabel à l'intérieur du bouton pour le texte centré
        label = QLabel(text, boutton_init)
        label.setStyleSheet(f"color: {color_text}; border: none;")
        label.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        label.setAlignment(Qt.AlignCenter)  # Centrage horizontal et vertical
        self.font,self.font_family=self.controller.set_font("./assets/Fonts/Inter,Montserrat,Roboto/Inter/static/Inter_24pt-SemiBold.ttf")
        self.font = QFont(self.font_family, 10)

        label.setFont(self.font)

        # Utiliser un layout vertical pour ajouter le QLabel dans le QPushButton
        layout = QHBoxLayout(boutton_init)
        layout.addWidget(label)  # Ajouter le QLabel au centre du bouton
        layout.setContentsMargins(0, 0, 0, 0)  # Marges à zéro pour remplir tout l'espace du QPushButton
        layout.setSpacing(0)

        return boutton_init
