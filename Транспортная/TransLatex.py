from pylatex import Document, Section, Subsection, Command, LineBreak, Package, \
    NewLine, NoEscape, Math
import subprocess
from os import unlink


class LatexTransport:
    def __init__(self):
        pass

    def generate_conditions(self, task_conditions):
        m = len(task_conditions[2])
        vector_stocks = task_conditions[2]
        n = len(task_conditions[1])
        vector_needs = task_conditions[1]
        matrix = task_conditions[0]
        condition_tab = self.generate_table(vector_stocks, vector_needs,
                                            matrix, n, m)
        return condition_tab

    def generate_table(self, first_vec=None, second_vec=None,
                       matrix=None, n=0, m=0, max_sum=None):
        if matrix is None:
            matrix = [0]
        latex_matrix = self.make_layout(n, max_sum)
        for i in range(m):
            latex_matrix += r"\multicolumn{3}{|c|}{$A_%i$}" % i
            for j in range(n):
                latex_matrix += f" & {matrix[i][j]}"
                pass
            if first_vec is not None:
                latex_matrix += f" & \\multicolumn{{3}}{{|c|}}{{{first_vec[i]}}} \\\\ \\hline \n"
            else:
                latex_matrix += "\\\\ \\hline \n"
        if second_vec is not None:
            latex_matrix += r"\multicolumn{3}{|c|}{\textbf{Потребности}} &"
            for i in range(n):
                latex_matrix += f" {second_vec[i]} &"
        if max_sum is None:
            latex_matrix += fr"\multicolumn{{3}}{{|c|}}{{{sum(second_vec)}}} \\ \hline"
            latex_matrix += r"""
\end{tabular}
\end{table}
        """
        else:
            latex_matrix += fr"""
\end{{tabular}}
\end{{table}}
Максимальная прибыль : {max_sum}
        """
        return latex_matrix

    def generate_answer(self, task_answers):
        matrix = task_answers[0]
        max_sum = task_answers[1]
        n = len(task_answers[0][0])
        m = len(task_answers[0])
        answer_tab = self.generate_table(None, None,
                                         matrix, n, m, max_sum)
        return answer_tab

    @staticmethod
    def make_layout(n, answer):
        if answer is None:
            table_frmt = "|c|c|c|c|c|c|" + "c|" * n
            hat = "&"
            for i in range(n):
                hat += f"$B_{i + 1}$ &"
            layout = (
                fr"""
\begin{{table}}[H] 
\centering 
\begin{{tabular}}{{{table_frmt}}}
\hline
\multicolumn{{3}}{{|c|}}{{\textbf{{Пункты}}}} & \multicolumn{{{n}}}{{c|}}{{\textbf{{Пункты назначения}}}} &
\multicolumn{{3}}{{c|}}{{\textbf{{Запасы}}}} \\ \cline{{4-{3 + n}}}
\multicolumn{{3}}{{|c|}}{{\textbf{{отправления}}}} {hat} \multicolumn{{3}}{{|c|}}{{\textbf{{(конт.)}}}} \\ \hline
""")
            return layout
        else:
            table_frmt = "|c|c|c|c|c|c|" + "c|" * n
            hat = ""
            for i in range(n):
                hat += f"& $B_{i + 1}$"
            layout = (
                fr"""
\begin{{table}}[H] 
\begin{{tabular}}{{{table_frmt}}}
\hline
\multicolumn{{3}}{{|c|}}{{\textbf{{Пункты}}}} & \multicolumn{{{n}}}{{c|}}{{\textbf{{Пункты назначения}}}} \\ \cline{{4-{3 + n}}}
\multicolumn{{3}}{{|c|}}{{\textbf{{отправления}}}} {hat} \\ \hline
""")
            return layout

    @staticmethod
    def generate_file(tex_tasks, tex_answers):
        task_counter = 0
        answer_counter = 0
        file = r"""
\documentclass[12pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[english, russian]{babel}
\usepackage{array}
\usepackage{float}
\usepackage{booktabs}
\begin{document}
\section*{Транспортная задача}
        """
        for task in tex_tasks:
            task_counter += 1
            file += f"""
\\centering
\\section*{{Задача №{task_counter}}}
            """
            file += "\n" + task
        file += "\\newpage"
        for answer in tex_answers:
            answer_counter += 1
            file += f"""
\\centering
\\section*{{Ответ №{answer_counter}}}
            """
            file += "\n" + answer
        file += "\n \\end{document}"
        return file


if __name__ == "__main__":
    latex = LatexTransport()
    latex.generate_table([1, 2], [3, 4])
