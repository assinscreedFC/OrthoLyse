import os
import sys

from PySide6.QtGui import QFontDatabase, QFont


class NavigationController:
    """Contrôleur global pour gérer la navigation"""

    _instance = None  # Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NavigationController, cls).__new__(cls)
            cls._instance.main_window = None  # Référence à MainWindow
            cls._instance.central_widget = None  # Référence au QStackedWidget
        return cls._instance

    def set_main_window(self, main_window, central_widget):
        """Enregistre la référence de MainWindow et du QStackedWidget"""
        self.main_window = main_window
        self.central_widget = central_widget

    def toggle_menu(self):
        """Afficher ou masquer le menu transparent"""
        if self.main_window.menu.isVisible():
            self.main_window.menu.hide()
        else:
            self.main_window.menu.show()


    def change_page(self, page_name):
        """Change la page dans QStackedWidget"""
        if self.central_widget:
            if page_name == "Home":
                self.central_widget.setCurrentWidget(self.main_window.home)
            elif page_name == "Menu":
                print("Changement de page vers Menu")
                self.central_widget.setCurrentWidget(self.main_window.menu)
            elif page_name == "ModeDeChargement":
                self.central_widget.setCurrentWidget(self.main_window.mode_de_chargement)
            elif page_name == "ImporterAudio":
                self.central_widget.setCurrentWidget(self.main_window.importer_audio)

    def set_font(self,index):
        absolute_path = os.path.abspath(index)
        print(f"Tentative de chargement de la police depuis : {absolute_path}")  # Afficher le chemin absolu

        font_id = QFontDatabase.addApplicationFont(absolute_path)
        #font_id = QFontDatabase.addApplicationFont(index)
        if font_id == -1:
            print("Erreur : Impossible de charger la police.")
            sys.exit(1)
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, 14)  # 14 = Taille de la police

        return font,font_family
            # Ajouter d'autres conditions pour d'autres pages si nécessaire
