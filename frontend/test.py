from PySide6.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget
from PySide6.QtGui import QTextCursor, QTextCharFormat, QFont, QColor
from PySide6.QtCore import Qt, QTimer
import sys

class A4PageWidget(QWidget):
    def __init__(self):
        super().__init__()

        # On fixe une taille qui correspond approximativement à une feuille A4 en pixels (à adapter selon les besoins)
        self.setFixedSize(595, 842)
        # Style pour simuler le papier
        self.setStyleSheet("background-color: white; border: 1px solid #ccc;")

        # Création du QTextEdit pour le contenu éditable
        self.text_edit = QTextEdit(self)
        # On retire le fond du QTextEdit pour qu'il soit transparent et laisse transparaître le style du widget parent
        self.text_edit.setStyleSheet("background-color: transparent;")
        self.text_edit.setAcceptRichText(True)
        # Texte initial (modifiable)
        self.text_edit.setText("Ce texte sera synchronisé avec l'audio et chaque mot sera souligné au bon moment.")

        # Layout pour placer le QTextEdit avec une marge interne (simulant des marges de page)
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)

    def underline_word(self, word_index):
        """
        Met en surbrillance (souligné) le mot à l'index donné.
        Avant de souligner, on efface la mise en forme précédente.
        """
        # Récupérer le QTextCursor
        cursor = self.text_edit.textCursor()

        # Effacer la mise en forme de tout le document
        cursor.select(QTextCursor.Document)
        clear_format = QTextCharFormat()
        clear_format.setUnderlineStyle(QTextCharFormat.NoUnderline)
        cursor.setCharFormat(clear_format)

        # Récupérer le texte brut et découper en mots
        text = self.text_edit.toPlainText()
        words = text.split()

        if word_index < 0 or word_index >= len(words):
            return

        # Calculer la position du mot dans le texte
        pos = 0
        for i, w in enumerate(words):
            if i == word_index:
                break
            pos += len(w) + 1  # +1 pour l'espace
        # Placer le curseur à la position du mot et sélectionner le mot
        cursor.setPosition(pos)
        cursor.movePosition(QTextCursor.NextWord, QTextCursor.KeepAnchor)

        # Définir le format de soulignement
        fmt = QTextCharFormat()
        fmt.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        fmt.setUnderlineColor(QColor("red"))
        cursor.mergeCharFormat(fmt)
        self.text_edit.setTextCursor(cursor)

# Exemple d'utilisation avec un timer pour simuler la synchronisation avec l'audio
if __name__ == '__main__':
    app = QApplication(sys.argv)
    page = A4PageWidget()
    page.show()

    current_word = 0

    def highlight_next():
        nonlocal current_word
        page.underline_word(current_word)
        current_word += 1

    # Timer pour souligner un mot toutes les 2 secondes (à adapter avec la synchronisation audio)
    timer = QTimer()
    timer.timeout.connect(highlight_next)
    timer.start(2000)

    sys.exit(app.exec())
