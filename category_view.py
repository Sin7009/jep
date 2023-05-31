# category_view.py
#
# Category view for the stack window
# Импортируем необходимые модули и классы
from functools import partial

import keyboard
import pyperclip

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

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
        self.widget = QWidget()
        self.layout = QGridLayout(self.widget)
        font_db = QFontDatabase()
        _id = font_db.addApplicationFont("./resources/fonts/swiss-911.ttf")
        font = QFont("Swiss911 UCm BT", 36)
        # Добавление меток категорий в сетку
        # Установка шрифта и стилей для каждой метки
        self.category_labels = [None for i in range(len(self.model.categories))]
        for i in range(len(self.model.categories)):
            p = (0, i)
            cat_label = QLabel(self.model.categories[i])
            cat_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            cat_label.setAlignment(Qt.AlignCenter)
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
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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

    # Обработчик событий нажатия клавиш
    def keyPressEvent(self, event):
        s = event.text()
        try:
            if s.isdigit():
                # Если нажата цифровая клавиша, выбрать текущего игрока
                if 1 <= int(s) <= len(self.model.players):
                    self.model.curr_player = int(s) - 1
            elif keyboard.is_pressed('k') or keyboard.is_pressed('л'):
                # Если нажата клавиша 'k' или 'л', обработать правильный ответ
                self.model.correct_answer()
                self.root.update()
            elif keyboard.is_pressed('j') or keyboard.is_pressed('о'):
                # Если нажата клавиша 'j' или 'о', обработать неправильный ответ
                self.model.incorrect_answer()
                self.root.update()
            elif keyboard.is_pressed('!'):
                # Если нажата клавиша '!', сбросить счет
                self.model.reset_score()
                self.root.update()
            elif keyboard.is_pressed('q') or keyboard.is_pressed('й'):
                confirm_exit = QMessageBox.question(self, 'Подтвердите выход', 'Вы действительно хотите выйти из игры?',
                                                    QMessageBox.Yes | QMessageBox.No)
                if confirm_exit == QMessageBox.Yes:
                    self.model.exit_game()
        except ValueError:
            # Обработка исключения, если клавиша не задействована или не сопоставлена
            pass 
