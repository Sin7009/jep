# clue_view.py
#
# Clue view for the stack window
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class ClueView(QWidget):
    def __init__(self, root, parent, model):
        super().__init__()
        self.root = root
        self.parent = parent
        self.model = model
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        font_id = QFontDatabase.addApplicationFont("./resources/fonts/korina-bold.ttf")
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font = QFont(font_families[0], 48)
        else:
            font = QFont("Arial", 48)  # Fallback font if loading fails

        self.q_label = QLabel()
        self.q_label.setFont(font)
        self.q_label.setStyleSheet("color: white;")
        self.q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.q_label.setWordWrap(True)

        self.a_label = QLabel()
        self.a_label.setFont(font)
        self.a_label.setStyleSheet("color: white;")
        self.a_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.a_label.setWordWrap(True)

        self.layout.addWidget(self.q_label)
        self.layout.addWidget(self.a_label)
        self.setLayout(self.layout)
        self.setStyleSheet("background-color:#060CE9;")
        self.show()

    def populate_clue(self, question, answer):
        self.a_label.hide()
        self.q_label.setText(question)
        self.a_label.setText("Ответ: " + answer)
        self.q_label.show()
        self.model.reset_timer()

    def show_answer(self):
        self.q_label.show()
        self.a_label.show()

    def update(self):
        pass  # Nothing to update in clue view
