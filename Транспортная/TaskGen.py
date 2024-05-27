import numpy as np
import TaskSolver as Solver
import TransLatex as Latex
import os
import subprocess


class ParameterRandomizer:
    """
    Класс для создания случайных значений вектора потребностей,
    запасов и цен перевозок
    """

    def __init__(self):
        """
        Инициализация диапазонов значений по умолчанию.
        """
        self.needs_range = (100, 200)
        self.stocks_range = (100, 200)
        self.cost_range = (1, 10)

    def validate_negative_parameters(self, num_departure_points: int,
                                     num_destination: int) -> None:
        """
        Проверка входных параметров на отрицательность.

        :param num_departure_points: количество пунктов отправления
        :param num_destination: количество пунктов назначения
        :raises ValueError: если параметры неверные
        """
        if num_departure_points <= 0 or num_destination <= 0:
            raise ValueError("Количество пунктов отправления и назначения\
             должно быть положительным.")

        if self.needs_range[0] <= 0 or self.needs_range[1] <= 0:
            raise ValueError("Значения потребностей не должно быть \
            отрицательным")

        if self.stocks_range[0] <= 0 or self.stocks_range[1] <= 0:
            raise ValueError("Значение запасов не должно быть отрицательным")

        if self.cost_range[0] <= 0 or self.cost_range[1] <= 0:
            raise ValueError("Значение цен перевозок не должно \
            быть отрицательным")

    def set_ranges(self, needs_range: tuple[int, int],
                   stocks_range: tuple[int, int],
                   cost_range: tuple[int, int]) -> None:
        """
        Установка диапазонов значений для генерации потребностей,
         запасов и стоимости перевозок.
        :param needs_range: диапазон значений для потребностей (min, max)
        :param stocks_range: диапазон значений для запасов (min, max)
        :param cost_range: диапазон значений для стоимости перевозок (min, max)
        """
        self.needs_range = needs_range
        self.stocks_range = stocks_range
        self.cost_range = cost_range

    def validate_range_parameters(self):
        """
        Функция для проверки промежутка между значениями
        :return: ValueError: если параметры неверные
        """
        if self.needs_range[0] >= self.needs_range[1]:
            raise ValueError("Значение промежутка у потребностей \
            должно быть больше одного")
        if self.stocks_range[0] >= self.stocks_range[1]:
            raise ValueError("Значение промежутка у запасов \
            должно быть больше одного")
        if self.cost_range[0] >= self.cost_range[1]:
            raise ValueError("Значение промежутка у цен \
            на перевозки должно быть больше одного")

    def generate_task(self, num_departure_points, num_destination):
        """
        Генерация задачи транспортировки

        :param num_departure_points: количество пунктов отправления
        :param num_destination: количество пунктов назначения
        :return: кортеж из матрицы стоимости перевозок и векторов потребностей
         и запасов
        """
        # Проверка значений на отрицательность
        self.validate_negative_parameters(num_departure_points,
                                          num_destination)
        self.validate_range_parameters()

        # Генерация случайных значений потребностей
        vector_needs = np.random.randint(self.needs_range[0],
                                         self.needs_range[1] + 1,
                                         num_destination) // 10 * 10

        # Генерация случайных значений запасов для всех элементов,
        # кроме последнего
        vector_stocks = np.random.randint(self.stocks_range[0],
                                          self.stocks_range[1] + 1,
                                          num_departure_points - 1) // 10 * 10

        # Подсчет суммы потребностей
        sum_needs = np.sum(vector_needs)
        sum_stocks = np.sum(vector_stocks)

        # Вычисление последнего элемента вектора запасов,
        # чтобы суммы были равны
        last_stock = sum_needs - sum_stocks
        vector_stocks = np.append(vector_stocks, last_stock)

        # Генерация матрицы цен перевозок
        matrix_transport_cost = np.random.randint(self.cost_range[0],
                                                  self.cost_range[1] + 1,
                                                  (num_departure_points,
                                                   num_destination))

        return (
            matrix_transport_cost,
            vector_needs,
            vector_stocks
        )


def generate_tex_file(number_students, number_departure, number_destinations,
                      link):
    result = None
    tex_path = os.path.expanduser(link)
    pdf_path = tex_path.replace(".tex", ".pdf")
    test = ParameterRandomizer()
    data = []
    task_list = []
    answer_list = []
    tr_latex = Latex.LatexTransport()
    for i in range(number_students):
        while result is None:
            data = test.generate_task(number_departure,
                                      number_destinations)
            result = Solver.solve_transport_problem(data[2], data[1], data[0])
        task_list.append(tr_latex.generate_conditions(data))
        answer_list.append(tr_latex.generate_answer(result))
    tex_file = tr_latex.generate_file(task_list, answer_list)
    try:
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(tex_file)
        print(f"LaTeX файл успешно создан: {tex_path}")
    except IOError as e:
        print(f"Ошибка записи LaTeX файла: {e}")
        return

    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"LaTeX файл успешно скомпилирован в PDF: {pdf_path}")
        print(f"stdout: {result.stdout.decode()}")
        print(f"stderr: {result.stderr.decode()}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при компиляции LaTeX: {e.stderr.decode()}")
        print(f"stdout: {e.stdout.decode()}")
    except FileNotFoundError:
        print("Ошибка: pdflatex не найден. Убедитесь, что LaTeX установлен и доступен в PATH.")
    except Exception as e:
        print(f"Непредвиденная ошибка: {str(e)}")

    for ext in [".aux", ".log", ".out"]:
        temp_file = tex_path.replace(".tex", ext)
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print(f"Удален временный файл: {temp_file}")
            except Exception as e:
                print(f"Не удалось удалить временный файл {temp_file}: {str(e)}")


if __name__ == "__main__":
    path_file = "C:\\Users\\reino\\python\\TaskGenerator\\Транспортная\\file_name"
    path = f"{path_file}.tex"
    generate_tex_file(5, 4, 5, path)
