import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from TaskGenerator.Псевдобулевская.Interface import PseudoBoolWindow
from TaskGenerator.Транспортная.Interface import MainWindow


class OptimizationTaskGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор задач")
        self.setGeometry(100, 100, 400, 200)
        self.init_ui()
        self.task_windows = []

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_pseudo_boolean = QPushButton("Псевдобулевская задача")
        btn_pseudo_boolean.setFixedSize(300, 50)
        btn_pseudo_boolean.clicked.connect(self.open_pseudo_boolean_window)
        layout.addWidget(btn_pseudo_boolean)

        btn_transport_problem = QPushButton("Транспортная задача")
        btn_transport_problem.setFixedSize(300, 50)
        btn_transport_problem.clicked.connect(
            self.open_transport_problem_window)
        layout.addWidget(btn_transport_problem)

        self.setLayout(layout)

    def open_pseudo_boolean_window(self):
        pseudo_boolean_window = PseudoBoolWindow()
        pseudo_boolean_window.show()
        self.task_windows.append(pseudo_boolean_window)

    def open_transport_problem_window(self):
        transport_problem_window = MainWindow()
        transport_problem_window.show()
        self.task_windows.append(transport_problem_window)


def main():
    app = QApplication(sys.argv)
    window = OptimizationTaskGenerator()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
