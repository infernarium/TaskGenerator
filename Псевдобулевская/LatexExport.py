from pylatex import Document, Section, Subsection, Command, LineBreak, Package, NewLine, NoEscape, Math
import subprocess
from os import unlink


def GenerateLatex(save_path: str,
                  variants_count: int = 2,
                  questions=["niger", "niger"],
                  use_answers: bool = False,
                  answers=["niger", "niger"],
                  description: bool = True,
                  student_mark: bool = True):
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

        for i in range(1, variants_count):
            with doc.create(Subsection(f'Вариант {i}', label=False, numbering=False)):
                doc.append(Command("\\"))
                doc.append("Решить уравнение")
                doc.append(Command("\\"))
                doc.append(NoEscape("$" + questions[i] + "$"))

                doc.append(Command("\\"))
                doc.append(Command("\\"))

                if student_mark:
                    doc.append(
                        NoEscape("Студент \\rule{100pt}{0.2pt} дата сдачи \\rule{70pt}{0.2pt}"))

    if use_answers:
        doc.append(Command('newpage'))
        with doc.create(Section('Ответы', label=False, numbering=False)):
            for i in range(1, variants_count):
                with doc.create(Subsection(f'Вариант {i}', label=False, numbering=False)):
                    doc.append(Command("\\"))
                    doc.append(NoEscape("Ответ: " + answers[i]))

    doc.generate_tex(save_path + "/Транспортные задачи")
    cmd = ['pdflatex', '-interaction', 'nonstopmode', f'-output-directory={save_path}',
           save_path + "/Транспортные задачи.tex"]
    proc = subprocess.Popen(cmd)
    proc.communicate()
    unlink(f'{save_path}/Транспортные задачи.log')
    unlink(f'{save_path}/Транспортные задачи.aux')


if __name__ == "__main__":
    GenerateLatex(save_path="C:/Users/markt/Desktop/TaskGenerator",
                  questions=["x_1+x_2=5", "x_3=1"],
                  answers=["(1,0,0,1)", "(1,2,3,4)"],
                  use_answers=True)
