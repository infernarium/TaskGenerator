from pylatex import Document, Section, Subsection, Command, LineBreak, Package, NewLine


def GenerateLatex(save_path: str = "Транспортные задачи", hlines: bool = False):
    doc = Document(document_options="a4paper,12pt", fontenc=None, lmodern=None, textcomp=None, page_numbers=None)
    
    doc.packages.append(Package("fontenc", options="T2A")) #удалить если будет вызывать ошибки
    doc.packages.append(Package("babel", options="russian"))
    
    with doc.create(Section('Транспортные задачи', label=False, numbering=False)):
        doc.append("Цель задачи - составление оптимального плана перевозок из пунктов доставки в пункты выдачи.")
        doc.append(Command("\\"))
        doc.append("Этапы решения: построение начального опорного плана, расчёт потенциалов, расчёт матриц, проверка оптимальности.")
        doc.append(Command("\\"))
        
        if hlines:
            doc.append(Command('noindent'))
            doc.append(Command('rule{\\linewidth}{0.4pt}'))
        
        for i in range(5):
            with doc.create(Subsection(f'Вариант {i}', label=False, numbering=False)):
                doc.append("asdasdasdasd")
                doc.append(LineBreak())
                
    doc.generate_tex(save_path)

if __name__ == "__main__":
    GenerateLatex(hlines=True)