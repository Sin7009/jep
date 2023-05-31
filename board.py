# view.py
#
# The view for Jep board
# Импорт необходимых модулей и классов
from PyQt6.QtWidgets import QLabel, QStackedWidget, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from category_view import CategoryView
from clue_view import ClueView
from final_jep_view import FinalJepView, WinnerView

# Класс виджета для отображения доски
class Board(QStackedWidget):
    def __init__(self, root, parent, model):
        super().__init__()
        self.root = root
        self.parent = parent
        self.model = model
        self.CAT_IND = 0
        self.CLUE_IND = 1
        self.FJ_IND = 2
        self.WINNER_IND = 3
        self.SJ_CARD = 4
        self.DJ_CARD = 5
        self.DD_CARD = 6
        self.FJ_CARD = 7

        self.initUI()

    def initUI(self):
        # Создание виджетов для отображения категорий, подсказок и т. д.
        self.category_view = CategoryView(self.root, self, self.model)
        self.clue_view = ClueView(self.root, self, self.model)
        self.final_jep_view = FinalJepView(self.root, self, self.model)
        self.winner_view = WinnerView(self.root, self, self.model)

        # Создание виджетов с изображениями и установка их свойств
        self.sj_card = QLabel(self)
        self.sj_card.setPixmap(QPixmap("resources/img/jeopardy.jpg"))
        self.sj_card.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sj_card.setScaledContents(True)
        self.sj_card.resize(self.width(), self.height())
        self.sj_card.show()

        self.dj_card = QLabel(self)
        self.dj_card.setPixmap(QPixmap("resources/img/double-jeopardy.png"))
        self.dj_card.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dj_card.setScaledContents(True)
        self.dj_card.resize(self.width(), self.height())
        self.dj_card.show()

        self.dd_card = QLabel(self)
        self.dd_card.setPixmap(QPixmap("resources/img/daily-double.png"))
        self.dd_card.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dd_card.setScaledContents(True)
        self.dd_card.resize(self.width(), self.height())
        self.dd_card.show()

        self.fj_card = QLabel(self)
        self.fj_card.setPixmap(QPixmap("resources/img/final-jeopardy.jpg"))
        self.fj_card.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fj_card.setScaledContents(True)
        self.fj_card.resize(self.width(), self.height())
        self.fj_card.show()

        # Добавление виджетов в стековый виджет
        self.addWidget(self.category_view)
        self.addWidget(self.clue_view)
        self.addWidget(self.final_jep_view)
        self.addWidget(self.winner_view)
        self.addWidget(self.sj_card)
        self.addWidget(self.dj_card)
        self.addWidget(self.dd_card)
        self.addWidget(self.fj_card)

        # Установка стилей и отображение доски
        self.setStyleSheet("background-color: black;")
        self.show_categories()
        self.show()

    # Отображение категорий
    def show_categories(self):
        self.curr_index = self.CAT_IND
        self.setCurrentIndex(self.curr_index)

    # Отображение подсказки
    def show_clue(self, i, j):
        # Установка текущей подсказки
        self.model.curr_clue_row = i
        self.model.curr_clue_col = j
        self.model.curr_clue_value = (self.model.curr_clue_row + 1) * self.model.base_clue_value
        # Заполнение подсказки в соответствии с моделью
        self.clue_view.populate_clue(self.model.clues[i][j].question, self.model.clues[i][j].answer)
        if self.model.clues[i][j].daily_double:
            self.model.play_sound('daily_double')
            self.show_card(self.DD_CARD)
        else:
            self.curr_index = self.CLUE_IND
            self.setCurrentIndex(self.curr_index)

    # Отображение финального вопроса
    def show_final_jep(self):
        self.curr_index = self.FJ_IND
        self.setCurrentIndex(self.curr_index)

    # Отображение победителя
    def show_winner(self):
        self.curr_index = self.WINNER_IND
        self.setCurrentIndex(self.curr_index)

    # Отображение определенной карточки (изображения)
    def show_card(self, ind):
        if ind == self.SJ_CARD:
            self.curr_index = self.SJ_CARD
        elif ind == self.DJ_CARD:
            self.curr_index = self.DJ_CARD
        elif ind == self.DD_CARD:
            self.curr_index = self.DD_CARD
        elif ind == self.FJ_CARD:
            self.curr_index = self.FJ_CARD
        self.setCurrentIndex(self.curr_index)

    # Обновление виджета
    def update(self, new_round):
        if new_round:
            if self.model.round == 1:
                self.show_card(self.SJ_CARD)
            elif self.model.round == 2:
                self.show_card(self.DJ_CARD)
            elif self.model.round == 3:
                self.show_card(self.FJ_CARD)
        self.category_view.update()
        self.clue_view.update()
        self.final_jep_view.update()
        self.winner_view.update()
