from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PySide6.QtGui import QFont, QPalette, QColor, QPixmap
from PySide6.QtCore import Qt, QEvent


class AudioUploadWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Appliquer le style pour avoir un fond arrondi
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 20px;
                padding: 20px;
            }
        """)

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Titre
        self.title_label = QLabel("Téléchargez l’audio")
        self.title_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)

        # Barre de séparation
        self.separator = QLabel()
        self.separator.setFixedHeight(2)
        self.separator.setStyleSheet(
            "background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #9c27b0, stop:1 #ff4081);")

        # Zone de drag & drop
        self.drop_area = DropArea()

        # Boutons en bas
        self.button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #00BCD4;
                color: #00BCD4;
                padding: 6px 12px;
                border-radius: 10px;
                font-size: 12px;
            }
        """)

        self.transcribe_button = QPushButton("Transcrire")
        self.transcribe_button.setStyleSheet("""
            QPushButton {
                background-color: #9E9E9E;
                color: white;
                padding: 6px 12px;
                border-radius: 10px;
                font-size: 12px;
            }
        """)
        self.transcribe_button.setEnabled(False)

        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.transcribe_button)

        # Ajouter tous les éléments au layout principal
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.separator)
        self.layout.addWidget(self.drop_area)
        self.layout.addLayout(self.button_layout)


class DropArea(QWidget):
    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)

        # Style
        self.setStyleSheet("""
            QWidget {
                border: 2px dashed #00BCD4;
                border-radius: 15px;
                background-color: rgba(0, 188, 212, 0.1);
            }
        """)

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Icône
        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap("assets/upload_icon.svg").scaled(50, 50, Qt.KeepAspectRatio))
        self.icon_label.setAlignment(Qt.AlignCenter)

        # Texte
        self.text_label = QLabel("Faites glisser votre audio ici\nou")
        self.text_label.setFont(QFont("Arial", 12))
        self.text_label.setAlignment(Qt.AlignCenter)

        # Bouton "Parcourir"
        self.browse_button = QPushButton("Parcourir")
        self.browse_button.setStyleSheet("""
            QPushButton {
                background-color: #00BCD4;
                color: white;
                padding: 6px 12px;
                border-radius: 10px;
                font-size: 12px;
            }
        """)

        self.browse_button.clicked.connect(self.open_file_dialog)

        # Ajouter les éléments au layout
        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.text_label)
        self.layout.addWidget(self.browse_button)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        print("Fichier déposé:", files[0])  # Ajoute la gestion du fichier ici

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Sélectionner un fichier audio", "",
                                                   "Fichiers audio (*.mp3 *.wav *.flac)")
        if file_path:
            print("Fichier sélectionné :", file_path)  # Ajoute la gestion du fichier ici


import sys
from PySide6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Téléchargement Audio")
        self.setGeometry(100, 100, 400, 300)  # Position et taille de la fenêtre

        # Ajouter le widget principal
        self.upload_widget = AudioUploadWidget()
        self.setCentralWidget(self.upload_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
