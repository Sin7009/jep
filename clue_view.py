# clue_view.py
#
# Clue view for the stack window
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import keyboard
import pyperclip

class ClueView(QWidget):
    def __init__(self, root, parent, model):
        super().__init__()
        self.root = root
        self.parent = parent
        self.model = model
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        font_db = QFontDatabase()
        _id = font_db.addApplicationFont("./resources/fonts/korina-bold.ttf")
        font = QFont("Korinna", 48)

        self.q_label = QLabel()
        self.q_label.setFont(font)
        self.q_label.setStyleSheet("color: white;")
        self.q_label.setAlignment(Qt.AlignCenter)
        self.q_label.setWordWrap(True)

        self.a_label = QLabel()
        self.a_label.setFont(font)
        self.a_label.setStyleSheet("color: white;")
        self.a_label.setAlignment(Qt.AlignCenter)
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

    def keyPressEvent(self, event):
        s = event.text()

        try:
            if not self.model.wager_mode:
                if s.isdigit():
                    if 1 <= int(s) <= len(self.model.players):
                        self.model.curr_player = int(s) - 1
                elif keyboard.is_pressed('space') or keyboard.is_pressed(' '):
                    self.show_answer()
                elif keyboard.is_pressed('esc'):
                    self.model.mark_answered()
                    self.parent.show_categories()
                    self.root.update()
                elif keyboard.is_pressed('k') or keyboard.is_pressed('ф'):
                    self.model.correct_answer()
                    self.root.update()
                elif keyboard.is_pressed('j') or keyboard.is_pressed('о'):
                    self.model.incorrect_answer()
                    self.root.update()
                elif keyboard.is_pressed('w') or keyboard.is_pressed('ц'):
                    print('wager on')
                    self.model.wager_mode = True
                    self.parent.setStyleSheet('border: 3px solid red')
                elif keyboard.is_pressed('!') or keyboard.is_pressed('1'):
                    self.model.reset_score()
                    self.root.update()
                elif keyboard.is_pressed('q') or keyboard.is_pressed('й'):
                    confirm_exit = QMessageBox.question(self, 'Подтвердите выход', 'Вы действительно хотите выйти из игры?',
                                                        QMessageBox.Yes | QMessageBox.No)
                    if confirm_exit == QMessageBox.Yes:
                        self.model.exit_game()
            else:
                    if s.isdigit():
                        self.model.update_wager(int(s))
                    elif keyboard.is_pressed('space') or keyboard.is_pressed(' '):
                        self.show_answer()
                    elif keyboard.is_pressed('k') or keyboard.is_pressed('ф'):
                        self.model.correct_wager()
                        self.root.update()
                    elif keyboard.is_pressed('j') or keyboard.is_pressed('о'):
                        self.model.incorrect_wager()
                        self.root.update()
                    elif keyboard.is_pressed('c') or keyboard.is_pressed('с'):
                        self.model.reset_wager()
                    elif keyboard.is_pressed('w') or keyboard.is_pressed('ц'):
                        print('wager off')
                        self.model.wager_mode = False
                        self.parent.setStyleSheet('')
                    elif keyboard.is_pressed('q') or keyboard.is_pressed('й'):
                        confirm_exit = QMessageBox.question(self, 'Подтвердите выход', 'Вы действительно хотите выйти из игры?',
                                                            QMessageBox.Yes | QMessageBox.No)
                        if confirm_exit == QMessageBox.Yes:
                            self.model.exit_game()
        except ValueError:
            # Обработка исключения, если клавиша не задействована или не сопоставлена
            pass 