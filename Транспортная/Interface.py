import sys
import random
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QScrollArea, QHBoxLayout
from TaskGenerator.Транспортная.LatexExport import GenerateLatex


class TransportationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Поиск оптимального маршрута")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Кнопка случайной генерации
        self.random_button = QPushButton("Случайная генерация")
        self.random_button.clicked.connect(self.randomize_values)
        self.random_button.setFixedSize(200, 30)
        self.layout.addWidget(self.random_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Поле ввода количества городов
        self.num_cities_label = QLabel("Количество городов:")
        self.num_cities_label.setFixedSize(200, 30)
        self.layout.addWidget(self.num_cities_label)

        self.num_cities_entry = QComboBox()
        self.num_cities_entry.setFixedSize(200, 30)
        for i in range(2, 11):
            self.num_cities_entry.addItem(str(i))
        self.num_cities_entry.currentIndexChanged.connect(self.update_fields)
        self.layout.addWidget(self.num_cities_entry)

        # Кнопка для добавления полей ввода для дорог между городами
        self.add_button = QPushButton("Добавить города")
        self.add_button.clicked.connect(self.add_road_fields)
        self.add_button.setFixedSize(200, 30)
        self.layout.addWidget(self.add_button)

        # Создание выпадающих списков для выбора наличия дороги между городами и полей ввода времени в пути
        self.road_comboboxes = []
        self.time_entries = []

        # Метка для добавления дорог
        self.roads_label = QLabel("Добавьте дороги:")
        self.roads_label.setFixedSize(200, 30)

        # Кнопка для нахождения оптимального маршрута
        self.find_button = QPushButton("Найти оптимальный маршрут")
        self.find_button.clicked.connect(self.find_optimal_route)
        self.find_button.setFixedSize(200, 30)

        # Кнопка для переноса в LaTeX
        self.latex_button = QPushButton("Перенести в LaTeX")
        self.latex_button.clicked.connect(self.transfer_to_latex)
        self.latex_button.setFixedSize(200, 30)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(QWidget())  # Создаем виджет для скролла
        self.scroll.widget().setLayout(self.layout)
        self.setCentralWidget(self.scroll)

    def update_fields(self):
        # Удаление предыдущих полей при изменении количества городов
        while len(self.road_comboboxes) > 0:
            self.layout.removeWidget(self.road_comboboxes.pop())
        while len(self.time_entries) > 0:
            self.layout.removeWidget(self.time_entries.pop())

        # Удаление предыдущих меток "Время в пути:" и "Между городом X и городом Y:"
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            if isinstance(item.widget(), QLabel) and (item.widget().text().startswith("Между городом") or item.widget().text() == "Время в пути:"):
                item.widget().deleteLater()

    def add_road_fields(self):
        # Добавление полей ввода для дорог между городами
        num_cities = int(self.num_cities_entry.currentText())

        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                road_label = QLabel(f"Между городом {i+1} и городом {j+1}:")
                road_label.setFixedSize(200, 30)
                self.layout.addWidget(road_label)

                road_combobox = QComboBox()
                road_combobox.addItems(["Нет", "Да"])
                road_combobox.setFixedSize(200, 30)
                self.layout.addWidget(road_combobox)
                self.road_comboboxes.append(road_combobox)

                time_label = QLabel("Время в пути:")
                time_label.setFixedSize(200, 30)
                self.layout.addWidget(time_label)

                time_entry = QLineEdit()
                time_entry.setFixedSize(200, 30)
                self.layout.addWidget(time_entry)
                self.time_entries.append(time_entry)

        self.layout.addWidget(self.roads_label)

        # Группировка кнопок "Найти оптимальный маршрут" и "Перенести в LaTeX"
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.find_button)
        button_layout.addWidget(self.latex_button)
        self.layout.addLayout(button_layout)

    def find_optimal_route(self):
        num_cities = int(self.num_cities_entry.currentText())
        road_matrix = [[0] * num_cities for _ in range(num_cities)]
        time_matrix = [[0] * num_cities for _ in range(num_cities)]

        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                road_index = i * (num_cities - 1) + j - i - 1
                road_combobox = self.road_comboboxes[road_index]
                time_entry = self.time_entries[road_index]
                if road_combobox.currentText() == "Да":
                    road_matrix[i][j] = 1
                    road_matrix[j][i] = 1
                    time_matrix[i][j] = float(time_entry.text())
                    time_matrix[j][i] = float(time_entry.text())

        # Выведем матрицы дорог и времени для демонстрации
        print("Матрица дорог:")
        for row in road_matrix:
            print(row)
        print("Матрица времени в пути:")
        for row in time_matrix:
            print(row)

        # Добавим здесь расчет оптимального маршрута на основе наличия дорог между городами и времени в пути
        pass

    def transfer_to_latex(self):
        num_cities = int(self.num_cities_entry.currentText())
        road_matrix = [[0] * num_cities for _ in range(num_cities)]
        time_matrix = [[0] * num_cities for _ in range(num_cities)]

        road_index = 0  # Индекс для доступа к комбобоксам и полям ввода времени
        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                if road_index < len(self.road_comboboxes):
                    road_combobox = self.road_comboboxes[road_index]
                    time_entry = self.time_entries[road_index]
                    if road_combobox.currentText() == "Да":
                        road_matrix[i][j] = 1
                        road_matrix[j][i] = 1
                        time_matrix[i][j] = float(time_entry.text())
                        time_matrix[j][i] = float(time_entry.text())
                    road_index += 1  # Увеличиваем индекс после использования комбобоксов и полей ввода времени

        latex_generator = GenerateLatex(road_matrix, time_matrix)
        latex_filename = "transportation_data.tex"
        latex_generator.export_to_latex(latex_filename)
        
    def randomize_values(self):
        num_cities = int(self.num_cities_entry.currentText())
        for i in range(len(self.road_comboboxes)):
            self.road_comboboxes[i].setCurrentIndex(random.randint(0, 1))
            self.time_entries[i].setText(str(random.randint(1, 10)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransportationWindow()
    window.showMaximized()  # Display the window in full screen
    sys.exit(app.exec())