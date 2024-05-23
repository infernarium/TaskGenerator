from pylatex import Document, Section, Subsection, Command, LineBreak, Package, NewLine, NoEscape, Math
import subprocess
from os import unlink

# def GenerateLatex(questions = [""],
#                   use_answers: bool = False,
#                   answers = ["",""],
#                   save_path: str = "Транспортные задачи",
#                   description: bool = True,
#                   student_mark: bool = True):
from TaskGenerator.Транспортная.TaskSolver import solve_transport_problem

"""
Функция создания tex и pdf документа для задач.

Args
----
use_answers: `bool`
    Использовать присланные ответы или нет.
answers: `array[str]`
    Массив выводимых ответов.
save_path: `str`
    Путь по которому будут созданы нужные файлы
description: 'bool'
    Добавлять описание задачи с этапами решения или нет?
"""
    
    # count = len(questions)
    #
    # if len(questions) != len(answers):
    #     raise Exception("Количество ответов с вопросами не совпадает")
    #
    # doc = Document(document_options="a4paper,12pt", fontenc=None, lmodern=None, textcomp=None, page_numbers=None)
    # doc.packages.append(Package("babel", options="russian"))
    #
    # with doc.create(Section('Транспортные задачи', label=False, numbering=False)):
    #     doc.append("Цель задачи - составление оптимального плана перевозок из пунктов доставки в пункты выдачи.")
    #     doc.append(Command("\\"))
    #     doc.append("Этапы решения: построение начального опорного плана, расчёт потенциалов, расчёт матриц, проверка оптимальности.")
    #     doc.append(Command("\\"))
    #
    #     doc.append(Command('noindent'))
    #     doc.append(Command('rule{\\linewidth}{0.4pt}'))
    #
    #     for i in range(count):
    #         with doc.create(Subsection(f'Вариант {i}', label=False, numbering=False)):
    #             doc.append(Command("\\"))
    #             doc.append("Решить уравнение")
    #             doc.append(Command("\\"))
    #             doc.append(NoEscape("$" + questions[i] + "$"))
    #
    #             doc.append(Command("\\"))
    #             doc.append(Command("\\"))
    #
    #             if student_mark:
    #                 doc.append(NoEscape("Студент \\rule{100pt}{0.2pt} дата сдачи \\rule{70pt}{0.2pt}"))
    #
    # if use_answers:
    #     doc.append(Command('newpage'))
    #     with doc.create(Section('Ответы', label=False, numbering=False)):
    #         for i in range(count):
    #             with doc.create(Subsection(f'Вариант {i}', label=False, numbering=False)):
    #                 doc.append(Command("\\"))
    #                 doc.append(NoEscape("Ответ: " + answers[i]))
    #
    #
    # doc.generate_tex(save_path)
    # cmd = ['pdflatex', '-interaction', 'nonstopmode', save_path]
    # proc = subprocess.Popen(cmd)
    # proc.communicate()
    # unlink(f'{save_path}.log')
    # unlink(f'{save_path}.aux')
class GenerateLatex:
    def __init__(self, road_matrix, time_matrix):
        self.road_matrix = road_matrix
        self.time_matrix = time_matrix
        print("3")

    def export_to_latex(self, filename):
        print("3")
        with open(filename, 'w', encoding="utf-8") as f:
            f.write("\\documentclass{article}\n")
            f.write("\\usepackage{amsmath}\n\n")
            f.write("\\usepackage[russian]{babel}\n\n")
            f.write("\\begin{document}\n\n")
            print("3")
            f.write("Матрица дорог:\n")
            f.write("\\[\n")
            f.write("\\begin{matrix}\n")
            for row in self.road_matrix:
                f.write("  & ".join(str(cell) for cell in row) + " \\\\\n")
            f.write("\\end{matrix}\n")
            f.write("\\]\n\n")
            print("3")
            f.write("Матрица времени в пути:\n")
            f.write("\\[\n")
            f.write("\\begin{matrix}\n")
            for row in self.time_matrix:
                f.write("  & ".join(str(cell) for cell in row) + " \\\\\n")
            f.write("\\end{matrix}\n")
            f.write("\\]\n\n")

            # Решение задачи и генерация LaTeX-строк
            # f.write("Решение задачи:\n")
            # solution, cost = solve_transport_problem(, self.time_matrix)
            # f.write("\\begin{itemize}\n")
            # for i, row in enumerate(solution):
            #     f.write(f"  \\item Город {i + 1}: " + ", ".join(str(x) for x in row) + "\n")
            # f.write(f"  \\item Общая стоимость: {cost}\n")
            # f.write("\\end{itemize}\n\n")

            f.write("\\end{document}\n")

        print("Данные успешно экспортированы в файл {} в формате LaTeX.".format(filename))

