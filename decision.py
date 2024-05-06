import random
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, \
    QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QMessageBox, QSpinBox, QHBoxLayout
from PyQt6.QtCore import Qt
from random import randint
# from scipy.optimize import linprog

class ResultWindow(QWidget):
    def __init__(self, result):
        super().__init__()
        self.setWindowTitle("Результат")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        result_label = QLabel(f"Результат: {result}")
        layout.addWidget(result_label)

        self.setLayout(layout)


class TSPGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор задачи коммивояжера")
        self.setGeometry(150, 150, 400, 300)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.city_count_label = QLabel("Количество городов:")
        self.city_count_spinbox = QSpinBox()
        self.city_count_spinbox.setMinimum(3)
        self.city_count_spinbox.setMaximum(100)
        self.city_count_spinbox.setValue(5)

        self.create_table_button = QPushButton("Создать таблицу")
        self.create_table_button.clicked.connect(self.create_table)

        self.solve_button = QPushButton("Решить задачу")
        self.solve_button.clicked.connect(self.solve_tsp)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.city_count_label)
        controls_layout.addWidget(self.city_count_spinbox)
        controls_layout.addWidget(self.create_table_button)
        controls_layout.addWidget(self.solve_button)

        self.layout.addLayout(controls_layout)

        self.setLayout(self.layout)

    def create_table(self):
        city_count = self.city_count_spinbox.value()

        # Создание случайной симметричной матрицы расстояний
        self.distance_matrix = [
            [0 if i == j else random.randint(10, 100) for j in range(city_count)]
            for i in range(city_count)
        ]

        for i in range(city_count):
            for j in range(i + 1, city_count):
                self.distance_matrix[i][j] = self.distance_matrix[j][i]

        # Создание таблицы для отображения расстояний
        if hasattr(self, 'table'):
            self.layout.removeWidget(self.table)
            self.table.deleteLater()

        self.table = QTableWidget(city_count, city_count)
        self.table.setHorizontalHeaderLabels([f"Город {i + 1}" for i in range(city_count)])
        self.table.setVerticalHeaderLabels([f"Город {i + 1}" for i in range(city_count)])

        for i in range(city_count):
            for j in range(city_count):
                item = QTableWidgetItem(str(self.distance_matrix[i][j]))
                self.table.setItem(i, j, item)

        self.layout.addWidget(self.table)

    def solve_tsp(self):
        if not hasattr(self, 'distance_matrix'):
            QMessageBox.warning(
                self, "Ошибка", "Сначала создайте таблицу"
            )
            return

        city_count = len(self.distance_matrix)

        # Жадный алгоритм ближайшего соседа
        unvisited = set(range(city_count))
        current_city = 0
        path = [current_city]
        unvisited.remove(current_city)

        while unvisited:
            next_city = min(
                unvisited,
                key=lambda x: self.distance_matrix[current_city][x]
            )
            path.append(next_city)
            unvisited.remove(next_city)
            current_city = next_city

        path.append(path[0])  # Возвращаемся к начальному городу

        # Преобразование пути в строку
        path_str = " -> ".join([f"Город {x + 1}" for x in path])

        # Отображение полного маршрута в одном окне без деталей
        result_box = QMessageBox()
        result_box.setWindowTitle("Решение задачи коммивояжера")
        result_box.setText(f"Оптимальный путь: {path_str}")
        result_box.setIcon(QMessageBox.Icon.Information)
        result_box.exec()

class TransportProblemGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор транспортной задачи")
        self.setGeometry(100, 100, 400, 300)  # Установка размера окна

        layout = QVBoxLayout()

        self.rows_label = QLabel("Количество поставщиков:")
        layout.addWidget(self.rows_label)

        self.rows_input = QLineEdit()
        layout.addWidget(self.rows_input)

        self.cols_label = QLabel("Количество потребителей:")
        layout.addWidget(self.cols_label)

        self.cols_input = QLineEdit()
        layout.addWidget(self.cols_input)

        self.generate_button = QPushButton("Создать таблицу")
        self.generate_button.clicked.connect(self.create_table)
        layout.addWidget(self.generate_button)

        self.auto_fill_button = QPushButton("Автозаполнение")
        self.auto_fill_button.clicked.connect(self.generate_transport_problem)
        layout.addWidget(self.auto_fill_button)

        self.solve_button = QPushButton("Решить задачу")
        self.solve_button.clicked.connect(self.solve_transport_problem)
        layout.addWidget(self.solve_button)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.result_window = None

    def create_table(self):
        rows = int(self.rows_input.text())
        cols = int(self.cols_input.text())

        self.table.setRowCount(rows + 1)  # +1 для строки потребностей
        self.table.setColumnCount(cols + 1)  # +1 для столбца потребностей

        # Заполняем случайные потребности и запасы
        for i in range(rows):
            supply = randint(rows*10, (rows)*20)
            item = QTableWidgetItem(str(supply))
            self.table.setItem(i, cols, item)

        for j in range(cols):
            demand = randint(cols*10, cols*20)
            item = QTableWidgetItem(str(demand))
            self.table.setItem(rows, j, item)

    def generate_transport_problem(self):
        rows = self.table.rowCount() - 1  # Исключаем строку с потребностями
        cols = self.table.columnCount() - 1  # Исключаем столбец с потребностями

        for i in range(rows):
            for j in range(cols):
                cost = randint(1, 10)
                item = QTableWidgetItem(str(cost))
                self.table.setItem(i, j, item)

    def solve_transport_problem(self):
        rows = self.table.rowCount() - 1  # Исключаем строку с потребностями
        cols = self.table.columnCount() - 1  # Исключаем столбец с потребностями
        costs = []
        supplies = []
        demands = []

        # Получаем стоимости перевозок
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(int(self.table.item(i, j).text()))
            costs.append(row)

        # Получаем запасы и потребности
        for i in range(rows):
            supplies.append(int(self.table.item(i, cols).text()))
        for j in range(cols):
            demands.append(int(self.table.item(rows, j).text()))

        # Решаем транспортную задачу методом наименьшей стоимости
        total_cost = 0
        allocation = [[0] * cols for _ in range(rows)]
        while True:
            # Ищем клетку с наименьшей стоимостью
            min_cost = float('inf')
            min_i, min_j = -1, -1
            for i in range(rows):
                for j in range(cols):
                    if costs[i][j] < min_cost:
                        min_cost = costs[i][j]
                        min_i, min_j = i, j

            # Если все клетки дороже 0, то заканчиваем распределение
            if min_cost == float('inf'):
                break

            # Выполняем перевозку
            quantity = min(supplies[min_i], demands[min_j])
            allocation[min_i][min_j] = quantity
            supplies[min_i] -= quantity
            demands[min_j] -= quantity
            costs[min_i][min_j] = float('inf')  # Метим клетку как "использованную"

            # Обновляем общую стоимость
            total_cost += quantity * min_cost

        # Отображаем результат
        self.result_window = ResultWindow(total_cost)
        self.result_window.show()


class OptimizationTaskGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор задач")
        self.setGeometry(100, 100, 800, 600)  # Установка размера окна
        self.init_ui()
        self.task_windows = []

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Кнопка для транспортной задачи
        btn_transport_problem = QPushButton("Транспортная задача")
        btn_transport_problem.setFixedSize(300, 50)
        btn_transport_problem.clicked.connect(self.open_transport_problem_window)
        layout.addWidget(btn_transport_problem)

        # Кнопка для задачи коммивояжера
        btn_tsp = QPushButton("Задача коммивояжера")
        btn_tsp.setFixedSize(300, 50)
        btn_tsp.clicked.connect(self.open_tsp_window)
        layout.addWidget(btn_tsp)

        # Кнопка для задачи о рюкзаке
        btn_knapsack = QPushButton("Задача о рюкзаке")
        btn_knapsack.setFixedSize(300, 50)
        btn_knapsack.clicked.connect(self.open_knapsack_window)
        layout.addWidget(btn_knapsack)

        # Кнопка для задачи о линейном программировании
        btn_linear_programming = QPushButton("Задача о линейном программировании")
        btn_linear_programming.setFixedSize(300, 50)
        btn_linear_programming.clicked.connect(self.open_linear_programming_window)
        layout.addWidget(btn_linear_programming)

        self.setLayout(layout)

    def open_transport_problem_window(self):
        # Предполагаем, что у вас есть класс TransportProblemGenerator
        transport_problem_window = TransportProblemGenerator()
        transport_problem_window.show()
        self.task_windows.append(transport_problem_window)

    def open_tsp_window(self):
        # Предполагаем, что у вас есть класс TSPGenerator
        tsp_window = TSPGenerator()
        tsp_window.show()
        self.task_windows.append(tsp_window)

    def open_knapsack_window(self):
        # Здесь можно открыть окно или выполнить задачу о рюкзаке
        knapsack_window = KnapsackProblemGenerator()  # Предположим, что у вас есть такой класс
        knapsack_window.show()
        self.task_windows.append(knapsack_window)

    def open_linear_programming_window(self):
        # Здесь можно открыть окно или выполнить задачу о линейном программировании
        linear_programming_window = LinearProgrammingGenerator()  # Если у вас есть такой класс
        linear_programming_window.show()
        self.task_windows.append(linear_programming_window)

def main():
    app = QApplication(sys.argv)
    window = OptimizationTaskGenerator()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
