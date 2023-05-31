from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from board import Board
from player_view import PlayerBarWidget

class View(QMainWindow):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Своя Игра')
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.main_content = Board(self, self.central_widget, self.model)
        self.player_bar = PlayerBarWidget(self, self.central_widget, self.model)
        self.layout.addWidget(self.main_content, 80)
        self.layout.addWidget(self.player_bar, 20)
        self.central_widget.setStyleSheet("background-color: black;")
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        self.central_widget.show()
        self.showFullScreen()
        self.show()

    def update(self):
        new_round = self.model.check_next_round()
        self.main_content.update(new_round)
        self.player_bar.update()

    def keyPressEvent(self, event):
        s = event.text()
        try:
            if not self.model.wager_mode:
                if s.isdigit():
                    if 1 <= int(s) <= len(self.model.players):
                        self.model.curr_player = int(s) - 1
                elif s == 'k' or s == 'л':
                    self.model.correct_answer()
                    self.update()
                elif s == 'j' or s == 'о':
                    self.model.incorrect_answer()
                    self.update()
                elif s == '!' or event.key() == Qt.Key.Key_Tab:
                    self.model.reset_score()
                    self.update()
                elif event.key() == Qt.Key.Key_Escape:
                    self.model.mark_answered()
                    self.parent.show_categories()
                    self.update()
                elif s == 'q' or s == 'й':
                    confirm_exit = QMessageBox.question(
                        self,
                        'Подтвердите выход',
                        'Вы действительно хотите выйти из игры?',
                        QMessageBox.StandardButtons(QMessageBox.Yes | QMessageBox.No)
                    )
                    if confirm_exit == QMessageBox.Yes:
                        self.model.exit_game()
                elif event.key() == Qt.Key.Key_Space or event.key() == Qt.Key.Key_Return:
                    if isinstance(self.main_content.currentWidget(), Board):
                        clue_view = self.main_content.currentWidget().clue_view
                        clue_view.show_answer()
            else:
                if s.isdigit():
                    self.model.update_wager(int(s))
                elif s == 'k' or s == 'л':
                    self.model.correct_wager()
                    self.update()
                elif s == 'j' or s == 'о':
                    self.model.incorrect_wager()
                    self.update()
                elif s == 'c' or s == 'с':
                    self.model.reset_wager()
                elif s == 'w' or s == 'ц':
                    self.model.wager_mode = False
        except ValueError:
            # Handle exception if the key is not used or not mapped
            pass
