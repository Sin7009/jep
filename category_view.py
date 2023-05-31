# category_view.py
#
# Category view for the stack window
from functools import partial

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import game

# Класс виджета для отображения категорий
class CategoryView(QWidget):
    def __init__(self, root, parent, model):
        super().__init__()
        self.root = root
        self.parent = parent
        self.model = model
        self.initUI()

    def initUI(self):
        # Создание прокручиваемой области
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Создание виджета и размещение в нем элементов с помощью сетки
        self.widget = QWidget()
        self.layout = QGridLayout(self.widget)
        QFontDatabase.addApplicationFont('./resources/fonts/swiss-911.ttf')
        font = QFont("Swiss911 UCm BT", 36)
        # Добавление меток категорий в сетку
        # Установка шрифта и стилей для каждой метки
        self.category_labels = [None for i in range(len(self.model.categories))]
        for i in range(len(self.model.categories)):
            p = (0, i)
            cat_label = QLabel(self.model.categories[i])
            cat_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            cat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cat_label.setWordWrap(True)
            cat_label.setStyleSheet("color: white;")
            self.layout.addWidget(cat_label, *p)
            self.category_labels[i] = cat_label

            # Уменьшение шрифта категорий в зависимости от количества знаков
            category_length = len(self.model.categories[i])
            if category_length <= 10:
                font_size = 36
            else:
                font_size = 24

            font.setPointSize(font_size)
            cat_label.setFont(font)

        # Добавление кнопок в сетку
        self.button_widgets = [[None for j in range(len(self.model.clues[i]))] for i in range(len(self.model.clues))]
        for i in range(len(self.model.clues)):
            for j in range(len(self.model.clues[i])):
                p = (i+1, j)
                button = QPushButton("₽{}".format((i+1) * game.CLUE_MULT * self.model.round))
                button.setFont(font)
                button.setStyleSheet("color: #FFCC00;")
                button.clicked.connect(partial(self.parent.show_clue, i, j))
                button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                self.layout.addWidget(button, *p)
                self.button_widgets[i][j] = button

        # Установка стилей и размещение области прокрутки в основном макете
        self.setStyleSheet("background-color:#060CE9;")
        self.layout.setRowStretch(len(self.model.clues)+1, 1)
        self.scroll_area.setWidget(self.widget)
        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(self.scroll_area)

        self.setLayout(self.layout_main)
        self.show()

    # Метод обновления виджета
    def update(self):
        for i in range(len(self.model.categories)):
            self.category_labels[i].setText(self.model.categories[i])
            
        for i in range(len(self.model.clues)):
            for j in range(len(self.model.clues[i])):
                if self.model.clues[i][j].answered:
                    self.button_widgets[i][j].setEnabled(False)
                    self.button_widgets[i][j].setStyleSheet("background-color: #808080;")
                else:
                    self.button_widgets[i][j].setText("₽{}".format((i+1) * game.CLUE_MULT * self.model.round))
                    self.button_widgets[i][j].setEnabled(True)
                    self.button_widgets[i][j].setStyleSheet("background-color: #060CE9; color: #FFCC00")
