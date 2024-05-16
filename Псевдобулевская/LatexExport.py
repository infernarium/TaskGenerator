from ctypes import Array
from pylatex import Document, Section, Subsection, Command, LineBreak, Package, NewLine, NoEscape, Math
import subprocess
from os import unlink
import os


def convert_task(task: Array):
    # вход: [[[-3, -6, 1, 9, 2], [0, 0, 2, 0, 4], 3]]
    ret = ""
    i = 0
    for Ai, Bi in zip(task[0][0], task[0][1]):
        if Ai > 0:
            ret += '+ ' + str(Ai) + 'x_{' + str(i + 1) + '} '
        if Ai < 0:
            ret += '- ' + str(Ai)[1] + 'x_{' + str(i + 1) + '} '

        if Bi > 0:
            ret += '+ ' + str(Bi) + r'\bar{x}_{' + str(i + 1) + '} '
        if Bi < 0:
            ret += '- ' + str(Bi)[1] + r'\bar{x}_{' + str(i + 1) + '} '
        i += 1

    ret += "= " + str(task[0][2])

    if (task[0][0][0] > 0) or ((task[0][0][0] == 0) and (task[0][0][0] > 0)):
        return ret[1:]
    else:
        return ret


def GenerateLatex(save_path: str,
                  variants_count: int,
                  questions=["niger", "niger"],
                  use_answers: bool = False,
                  answers=["niger", "niger"],
                  description: bool = True,
                  student_mark: bool = True,
                  delete_temp: bool = True):
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
    variants_count += 1

    doc = Document(document_options="a4paper,12pt", fontenc=None,
                   lmodern=None, textcomp=None, page_numbers=None)
    doc.packages.append(Package("babel", options="russian"))

    with doc.create(Section('Транспортные задачи', label=False, numbering=False)):
        doc.append(
            "Цель задачи - составление оптимального плана перевозок из пунктов доставки в пункты выдачи.")
        doc.append(Command("\\"))
        doc.append(
            "Этапы решения: построение начального опорного плана, расчёт потенциалов, расчёт матриц, проверка оптимальности.")
        doc.append(Command("\\"))

        doc.append(Command('noindent'))
        doc.append(Command('rule{\\linewidth}{0.4pt}'))

        for i in range(0, variants_count - 1):
            with doc.create(Subsection(f'Вариант {i + 1}', label=False, numbering=False)):
                doc.append(Command("\\"))
                doc.append("Решить уравнение")
                doc.append(Command("\\"))

                doc.append(NoEscape("$" + convert_task(questions[i]) + "$"))

                doc.append(Command("\\"))
                doc.append(Command("\\"))

                if student_mark:
                    doc.append(
                        NoEscape("Студент \\rule{100pt}{0.2pt} дата сдачи \\rule{70pt}{0.2pt}"))

    if use_answers:
        doc.append(Command('newpage'))
        with doc.create(Section('Ответы', label=False, numbering=False)):
            for i in range(0, variants_count - 1):
                with doc.create(Subsection(f'Вариант {i + 1}', label=False, numbering=False)):
                    doc.append(Command("\\"))
                    doc.append(NoEscape("Возможные варианты ответа: \\\\"))

                    for answer in answers[i][0]:
                        answ_str = '('
                        for num in answer:
                            answ_str += str(num) + ', '
                        answ_str = answ_str[:-2]
                        answ_str += ') '
                        doc.append(NoEscape(answ_str))

    doc.generate_tex(os.path.join(save_path, "Транспортные задачи"))
    cmd = ['pdflatex',
           '-interaction',
           'nonstopmode',
           f'-output-directory={save_path}',
           os.path.join(save_path, "Транспортные задачи.tex")]
    proc = subprocess.Popen(cmd)
    proc.communicate()

    if delete_temp:
        unlink(os.path.join(save_path, 'Транспортные задачи.log'))
        unlink(os.path.join(save_path, 'Транспортные задачи.aux'))


if __name__ == "__main__":
    GenerateLatex(save_path="C:/Users/markt/Desktop/TaskGenerator",
                  variants_count=2,
                  questions=[[[[12, -11, -6, 5, 10], [0, -17, 0, 0, 4], -1]],
                             [[[-5, 7, 6, -6, 8], [0, 0, 0, -1, -3], 2]]],
                  answers=[[[[0, 1, 0, 0, 1], [1, 0, 0, 0, 0], [0, 1, 1, 1, 1]]],
                           [[[0, 1, 0, 1, 1], [1, 1, 0, 0, 0], [0, 0, 1, 0, 0]]]],
                  use_answers=True)
    # print(convert_task([[[-3, -6, 1, 9, 2], [0, 0, 2, 0, 4], 3]]))

    # answers = [[[[1, 1, 0, 0, 0], [1, 1, 0, 0, 1], [0, 0, 0, 1, 0]]],
    #           [[[1, 1, 0, 0, 0], [0, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 1, 1]]]]
