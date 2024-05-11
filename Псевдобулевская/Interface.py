import sys
from os.path import exists
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QFileDialog,
    QCheckBox,
    QSpinBox,
    QErrorMessage
)


class PseudoBoolWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.number_label = QLabel("Количество булевых переменных", self)
        layout.addWidget(self.number_label)

        self.number_input = QSpinBox(self)
        self.number_input.setRange(2, 20)
        layout.addWidget(self.number_input)

        self.folder_path_text = QLineEdit(self)
        self.folder_path_text.setPlaceholderText(
            "Путь до папки для сохранения")

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_path_text)

        self.folder_path_button = QPushButton("Выбрать папку", self)
        self.folder_path_button.clicked.connect(self.get_folder_path)
        folder_layout.addWidget(self.folder_path_button)
        layout.addLayout(folder_layout)

        self.description_checkbox = QCheckBox("Добавить описание задачи", self)
        layout.addWidget(self.description_checkbox)

        self.student_mark_checkbox = QCheckBox(
            "Добавить места пометок о сдаче студентами", self)
        layout.addWidget(self.student_mark_checkbox)

        self.anwers_checkbox = QCheckBox("Добавить страницу с ответами", self)
        layout.addWidget(self.anwers_checkbox)

        self.save_button = QPushButton("Сгенерировать", self)
        self.save_button.clicked.connect(self.generate_all)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def get_folder_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выбрать папку")
        if folder_path:
            self.folder_path_text.setText(folder_path)

    def generate_all(self):
        if not (exists(self.folder_path_text.text())):
            QErrorMessage(self).showMessage("Путь к папке указан не верно")
            return

        # сюда вставить функцию создания латеха


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PseudoBoolWindow()
    window.show()
    sys.exit(app.exec())
