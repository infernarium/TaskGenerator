import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, \
    QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt
from random import randint
from scipy.optimize import linprog

class ResultWindow(QWidget):
    def __init__(self, result):
        super().__init__()
        self.setWindowTitle("Результат")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        result_label = QLabel(f"Результат: {result}")
        layout.addWidget(result_label)

        self.setLayout(layout)



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
        self.setGeometry(100, 100, 400, 300)  # Установка размера окна
        self.init_ui()
        self.task_windows = []

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Выравнивание по центру

        # Создание кнопок для различных видов задач
        btn_transport_problem = QPushButton("Транспортная задача")
        btn_transport_problem.setFixedSize(200, 50)  # Установка размеров кнопки
        btn_transport_problem.clicked.connect(self.open_transport_problem_window)
        layout.addWidget(btn_transport_problem)

        self.setLayout(layout)

    def open_transport_problem_window(self):
        transport_problem_window = TransportProblemGenerator()
        transport_problem_window.show()
        self.task_windows.append(transport_problem_window)


def main():
    app = QApplication(sys.argv)
    window = OptimizationTaskGenerator()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
