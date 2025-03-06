from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QMainWindow, QPushButton, QApplication, QWidget, QLabel, QVBoxLayout, \
    QSizePolicy, QHBoxLayout, QToolBar, QStackedWidget
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QImage, QPalette, QBrush,QPainter,QPixmap
from PySide6.QtCore import Qt, QBuffer, QByteArray
from Widgets.Header import Header
from Widgets.NavBar import NavBar
from frontend.Views.Home import Home
from frontend.Views.ImporterAudio import ImporterAudio
from frontend.Views.Menu import Menu
from frontend.Views.ModeDeChargement import ModeDeChargement
from frontend.controllers.Menu_controllers import NavigationController


#anis


class MyWindow(QMainWindow):
    #taille minimum de la fenetre w=642 h=450
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ma première fenêtre Qt avec Python")
        self.setWindowIcon(QIcon("icon.png"))
        self.setMinimumSize(642,450)
        self.resize(642, 450)

        #element pour stack les widgets pour permettre de naviger entre les different page de notre app
        self.qStackwidget=QStackedWidget()
        #home
        self.home=Home()
        #self.home.setStyleSheet("border: 1px solid #fff;background-color: #fff;")

        self.qStackwidget.addWidget(self.home)
        #menu
        self.menu=Menu()
        self.qStackwidget.addWidget(self.menu)
        #mode de chargment
        self.mode_de_chargement=ModeDeChargement()
        self.qStackwidget.addWidget(self.mode_de_chargement)
        #Importer audio
        self.importer_audio=ImporterAudio()
        self.qStackwidget.addWidget(self.importer_audio)
        # Créer un QLabel pour afficher l'image de fond
        self.label_fond = QLabel(self)
        self.label_fond.setAlignment(Qt.AlignCenter)

        # Charger l'image
        self.pixmap = QPixmap("./assets/image/background.jpg")
        # Appliquer l'image redimensionnée
        self.ajuster_image()


        # Connecter le redimensionnement de la fenêtre à la mise à jour de l'image
        self.resizeEvent = self.on_resize

        # Enregistrement dans le contrôleur
        self.controller = NavigationController()
        self.controller.set_main_window(self, self.qStackwidget)


        self.qStackwidget.setCurrentWidget(self.home)
        self.setCentralWidget(self.qStackwidget)

        # Créer un QToolBar et le rendre transparent
        self.toolbar = QToolBar("Menu")
        self.toolbar.setMovable(False)  # Interdit de déplacer la toolbar
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.setStyleSheet("background-color: rgba(0, 0, 0, 1);")  # Rendre la toolbar semi-transparente

        # Ajouter des actions à la toolbar
        action_home = QAction("Accueil", self)
        action_home.triggered.connect(self.show_home)
        self.toolbar.addAction(action_home)

        action_menu = QAction("Menu", self)
        action_menu.triggered.connect(self.show_menu)
        self.toolbar.addAction(action_menu)

        action_import_audio = QAction("import", self)
        action_import_audio.triggered.connect(self.show_importer_audio)
        self.toolbar.addAction(action_import_audio)
        self.qStackwidget.setCurrentWidget(self.importer_audio)

    def show_home(self):
        """Afficher la page d'accueil"""
        self.qStackwidget.setCurrentWidget(self.home)

    def show_menu(self):
        """Afficher le menu principal not used"""
        self.qStackwidget.setCurrentWidget(self.menu)

    def show_importer_audio(self):
        """Afficher le menu principal not used"""
        self.qStackwidget.setCurrentWidget(self.importer_audio)

    def ajuster_image(self):
        # Redimensionner l'image pour s'adapter à la fenêtre
        pixmap_redimensionne = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.label_fond.setPixmap(pixmap_redimensionne)
        self.label_fond.setGeometry(0, 0, self.width(), self.height())

    def on_resize(self,event):
        self.ajuster_image()
    # Un gestionnaire d'événements (voir les connexions ci-dessus).
    def doSomething(self):
        print(self.sender().text(), "cliqué")

def load_all_stylesheets(directory):
    """Charge et concatène tous les fichiers QSS d'un dossier."""
    styles = ""
    for filename in sorted(os.listdir(directory)):  # Trier les fichiers pour un chargement structuré
        if filename.endswith(".qss"):
            with open(os.path.join(directory, filename), "r") as file:
                styles += file.read() + "\n"
    return styles

if __name__ == "__main__":
    app = QApplication(sys.argv)
    style=load_all_stylesheets("./style/")
    app.setStyleSheet(style)
    
    myWindow = MyWindow()
    myWindow.show()

    sys.exit(app.exec())