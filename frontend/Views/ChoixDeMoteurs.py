import sys
from PySide6.QtWidgets import QApplication, QLabel, QPushButton,QWidget,QVBoxLayout, QHBoxLayout, QFrame,QSizePolicy,QSpacerItem
from PySide6.QtGui import QPixmap,QIcon
from PySide6.QtCore import Qt

from frontend.controllers.Menu_controllers import NavigationController

class ChoixDeMoteurs(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = NavigationController()

        self.resize(1117,768)

        #background de la page
        self.background=QLabel(self)
        self.background.setPixmap(QPixmap("./assets/image/background3.jpg").scaled(self.size(), Qt.KeepAspectRatioByExpanding,Qt.SmoothTransformation))
        self.background.setScaledContents(True)
        self.background.setGeometry(0,0,self.width(),self.height())
        self.setStyleSheet("""
        QPushButton{
            color:white;
            font-family:georgia;
            font-size:30px;
            background-color: rgba(255, 255, 255, 0.01);
            border-radius: 30px;
            
            border: 3px solid white;
            padding: 10px;
           
            
        }
        QPushButton::hover{
                           background-color:#c5c5c5;
                           }
        """)
        
        self.choixTranscription()
        self.separateur()
        self.choixAnalyse()
        self.creerBoutonValider()
        self.ajusterBtnSize()
        self.alignerWidgets()

    def choixTranscription(self):
        #sous forme d'un layout vertical
        self.textIconHLayout=QHBoxLayout()
        self.textIconHLayout.setAlignment(Qt.AlignCenter)
        #creer le texte
        self.text1=QLabel("Modèle de transcription",self)
        self.text1.setStyleSheet("""QLabel{
            color:white;
            font-size: 35px;
            font-family: georgia;
        }""")
        self.text1.setWordWrap(True)
        self.text1.setAlignment(Qt.AlignCenter)
        
        
        
        

        #creer l'icone
        
        self.helpIcone = QPushButton()
        self.helpIcone.setIcon(QIcon("./assets/icons/help.png"))  # Assurez-vous que le chemin est correct
        self.helpIcone.setIconSize(self.helpIcone.sizeHint())  # Ajuste la taille de l'icône au bouton
        self.helpIcone.setStyleSheet("border: none;")
        
        

        #aligner le texte et l'icone horizontalement
        
        
        self.textIconHLayout.addWidget(self.text1)

        self.textIconHLayout.addSpacing(5)
        
        self.textIconHLayout.addWidget(self.helpIcone)
        
        

        #creer les boutons 
        #self.btnTiny=QPushButton("Tiny",self)
        self.btnBase=QPushButton("Base",self)
        self.btnSmall=QPushButton("Small",self)
        self.btnMedium=QPushButton("Medium",self)
        self.btnLarge=QPushButton("Turbo",self)

        #aligner le layout horizontal et les boutons verticalement
        self.transcriptionVLayout=QVBoxLayout()
        self.transcriptionVLayout.setAlignment(Qt.AlignCenter)
        self.transcriptionVLayout.addStretch(3)
        self.transcriptionVLayout.addLayout(self.textIconHLayout)
        self.transcriptionVLayout.addStretch(10)
        #self.transcriptionVLayout.addWidget(self.btnTiny,alignment=Qt.AlignCenter)
        #self.transcriptionVLayout.addStretch(1)
        self.transcriptionVLayout.addWidget(self.btnBase,alignment=Qt.AlignCenter)
        self.transcriptionVLayout.addStretch(1)
        self.transcriptionVLayout.addWidget(self.btnSmall,alignment=Qt.AlignCenter)
        self.transcriptionVLayout.addStretch(1)
        self.transcriptionVLayout.addWidget(self.btnMedium,alignment=Qt.AlignCenter)
        self.transcriptionVLayout.addStretch(1)
        self.transcriptionVLayout.addWidget(self.btnLarge,alignment=Qt.AlignCenter)
        self.transcriptionVLayout.addStretch(10)

        


    def separateur(self):
        self.line=QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setStyleSheet("border: 3px dotted white;")

    def choixAnalyse(self):

        #creer le texte
        self.text2=QLabel("Moteur pour analyser la transcription",self)
        self.text2.setStyleSheet("""QLabel{
            color:white;
            font-size: 35px;
            font-family: georgia;
        }""")
        self.text2.setWordWrap(True)
        self.text2.setAlignment(Qt.AlignCenter)

        #creer les deux boutons 
        self.btnNltk=QPushButton("NLTK",self)
        self.btnSpacy=QPushButton("Spacy",self)

        #aligner le texte et les deux boutons verticalement
        self.analyseVLayout=QVBoxLayout()
        self.analyseVLayout.setAlignment(Qt.AlignCenter)
        self.analyseVLayout.addStretch(1)
        self.analyseVLayout.addWidget(self.text2,alignment=Qt.AlignCenter)
        self.analyseVLayout.addStretch(3)
        self.analyseVLayout.addWidget(self.btnNltk,alignment=Qt.AlignCenter)
        self.analyseVLayout.addStretch(1)
        self.analyseVLayout.addWidget(self.btnSpacy,alignment=Qt.AlignCenter)
        self.analyseVLayout.addStretch(3)

    def creerBoutonValider(self):
        self.btnValider=QPushButton("Valider")
        self.btnValider.setFixedHeight(60)
        self.btnValider.setStyleSheet("""QPushButton{
                                        border-radius:30px;
                                        font-size:20px;
                                      }
                                      
                                      QPushButton::hover{
                                        background-color:grey;
                                      
                                      }""")
        self.btnValider.clicked.connect(self.retour_menu)
        #ajouter ce bouton dans un layout horizontal
        self.btnValiderLayout=QHBoxLayout()
        self.btnValiderLayout.setAlignment(Qt.AlignRight)
        self.btnValiderLayout.addStretch(1)
        self.btnValiderLayout.addWidget(self.btnValider,alignment=Qt.AlignRight)
        

    def ajusterBtnSize(self):
        buttons=[self.btnBase,self.btnSmall,self.btnMedium,self.btnLarge,self.btnNltk,self.btnSpacy]
        for btn in buttons:
            btn.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
            btn.setMaximumSize(210,60)
            btn.setMinimumSize(190,60)
            self.text1.setMinimumWidth(400)
            self.text2.setMinimumWidth(400)
            self.text1.setMaximumWidth(700)
            self.text1.setWordWrap(True)
            


    def alignerWidgets(self):
        #creer un layout horizontal
        self.mainVLayout=QVBoxLayout()
        self.mainVLayout.setAlignment(Qt.AlignCenter)

        self.mainLayout=QHBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignCenter)

        self.mainLayout.addStretch(2)
        self.mainLayout.addLayout(self.transcriptionVLayout)
        self.mainLayout.addStretch(2)
        self.mainLayout.addWidget(self.line)
        self.mainLayout.addStretch(2)
        self.mainLayout.addLayout(self.analyseVLayout)
        self.mainLayout.addStretch(2)
        

        self.mainVLayout.addStretch(2)
        self.mainVLayout.addLayout(self.mainLayout)
        

        #ajouter ce layout dans le layout vertical principal
        self.mainVLayout.addStretch(2)
        self.mainVLayout.addLayout(self.btnValiderLayout)
        self.mainVLayout.addStretch(0)
        
        
        


        self.setLayout(self.mainVLayout)
        

    def retour_menu(self):
        self.controller.change_page("Home")

    def resizeEvent(self, event):
        """Redimensionner l'image de fond lorsqu'on redimensionne la fenêtre"""
        self.background.setPixmap(QPixmap("assets/background3.jpg").scaled(self.size(), Qt.KeepAspectRatioByExpanding,Qt.SmoothTransformation))
        self.background.setGeometry(0,0,self.width(),self.height())

        # Calculer la taille de la police en fonction de la hauteur de la fenêtre
        font_size1 = max(20, int(self.height() / 21))  # Ajuster la taille de la police avec un minimum de 20px
        font_size2 = max(20, int(self.height() / 25))
        
        # Appliquer la taille de la police à tous les labels
        self.text1.setStyleSheet(f"QLabel{{color:white; font-size:{font_size1}px; font-family: georgia;}}")
        self.text2.setStyleSheet(f"QLabel{{color:white; font-size:{font_size1}px; font-family: georgia;}}")
        
        # Appliquer la taille de la police à tous les boutons si nécessaire
        self.btnBase.setStyleSheet(f"QPushButton{{color:white; font-size:{font_size2}px; background-color: rgba(255, 255, 255, 0.01); border-radius: 30px; border: 3px solid white; padding: 10px;}}")
        self.btnSmall.setStyleSheet(f"QPushButton{{color:white; font-size:{font_size2}px; background-color: rgba(255, 255, 255, 0.01); border-radius: 30px; border: 3px solid white; padding: 10px;}}")
        self.btnMedium.setStyleSheet(f"QPushButton{{color:white; font-size:{font_size2}px; background-color: rgba(255, 255, 255, 0.01); border-radius: 30px; border: 3px solid white; padding: 10px;}}")
        self.btnLarge.setStyleSheet(f"QPushButton{{color:white; font-size:{font_size2}px; background-color: rgba(255, 255, 255, 0.01); border-radius: 30px; border: 3px solid white; padding: 10px;}}")
        self.btnNltk.setStyleSheet(f"QPushButton{{color:white; font-size:{font_size2}px; background-color: rgba(255, 255, 255, 0.01); border-radius: 30px; border: 3px solid white; padding: 10px;}}")
        self.btnSpacy.setStyleSheet(f"QPushButton{{color:white; font-size:{font_size2}px; background-color: rgba(255, 255, 255, 0.01); border-radius: 30px; border: 3px solid white; padding: 10px;}}")

        # Ajuster les espacements et la largeur minimale des labels si nécessaire
        self.text1.setMinimumSize(400,70)
        self.text2.setMinimumSize(400,70)
        self.text1.setMaximumSize(700,100)
        self.text2.setMaximumSize(700,100)
        
        super().resizeEvent(event)

        
            

        


