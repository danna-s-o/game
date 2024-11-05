from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget,\
    QPushButton, QVBoxLayout, QWidget, QMessageBox, QFileDialog, QTextEdit

from PyQt6.QtGui import QAction
import sys


class MyNoteApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Мои заметки')
        self.setGeometry(200, 200, 400, 300)

        # Создание текстового редактора
        self.text_edit = QTextEdit()

        # Создание кнопок
        self.save_button = QPushButton('Сохранить заметку')
        self.load_button = QPushButton('Загрузить заметку')

        # Действия кнопок
        self.save_button.clicked.connect(self.save_note())

        # Добавление элементов в макет
        layout = QVBoxLayout() # Сетка
        layout.addWidget(self.text_edit)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

        # Основной виджет
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    #Методы класса
    def save_note(self):
        print('Замтка сохранена')



if __name__ == '__main__':
    # Создать приложение. Приложению нужен один (и только один) экземпляр QApplication.
    # Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
    # Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
    app = QApplication(sys.argv)

    # Создаём виджет Qt — окно.
    main_window = MyNoteApp() #Создать окно

    main_window.show()
    """
    В Qt все виджеты верхнего уровня — окна, то есть у них нет родительского элемента 
    и они не вложены в другой виджет или макет. В принципе, окно можно создать, используя любой виджет.

    Виджеты без родительского элемента по умолчанию невидимы. Поэтому после создания объекта window 
    необходимо всегда вызывать функцию .show(), чтобы сделать его видимым. .show() можно удалить, 
    но тогда, запустив приложение, вы не сможете выйти из него!
    """

    # Запускаем цикл событий.
    sys.exit(app.exec())