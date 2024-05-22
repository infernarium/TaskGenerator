import numpy as np


# коментарии к переменным
# a - массив коэфицентов(a_i) для переменных x_i
# b - массив коэфицентов(b_i) для переменных x̄_i
# k - правая часть общего линейного псевдобулего уравнения

# y - массив документов для переменных y_j, где
# iter - какому x_i равна переменная y_j после преобразования T (iter = i)
# inv - какому x равна переменная y после преобразования T (y_j = либо x̄_i, либо x_i)(inv = либо 1, либо 0)
# coef - коэфицент(c_j) для переменной y_j
# d - правая часть уравнения после преобразования T

# функция преобразования T (шаг 1)
def transformation_t(a, b, k):
    y = []
    d = k
    for i in range(len(a)):
        if a[i] > b[i]:
            y.append({'iter': i,
                      'inv': 0,
                      'coef': a[i] - b[i]})
            d -= b[i]
        else:
            y.append({'iter': i,
                      'inv': 1,
                      'coef': b[i] - a[i]})
            d -= a[i]

    y.sort(key=lambda item: item['coef'], reverse=True)
    return y, d


def equation_solution(y, d):
    # случий 1
    if d < 0:
        return [list(np.repeat(None, len(y)))]

    # случий 2
    if d == 0:
        return [list(np.repeat(0, len(y)))]

    # случий 3
    if d > 0 and not all(y[i]['coef'] <= d for i in range(len(y))):
        p = len(y)
        solutions = []
        for i in range(len(y)):
            if y[i]['coef'] <= d:
                p = i
                break

        if p < len(y):
            prefix = list(np.repeat(0, p))
            for answer in equation_solution(y[p:len(y)], d):
                solutions.append(list(np.concatenate((prefix, answer))))

        return solutions

    # случий 4
    if d > 0 and not all(y[i]['coef'] < d for i in range(len(y))):
        # 1
        p = len(y)
        solutions = []
        for i in range(len(y)):
            if y[i]['coef'] == d:
                solutions.append(list(np.repeat(0, len(y))))
                solutions[-1][i] = 1
            else:
                p = i
                break
        # 2
        if len(y) > p > 0:
            prefix = list(np.repeat(0, p))
            for answer in equation_solution(y[p:len(y)], d):
                solutions.append(list(np.concatenate((prefix, answer))))

        return solutions

    # случий 5
    if d > 0 and all(y[i]['coef'] < d for i in range(len(y))) and np.sum([y[i]['coef'] for i in range(len(y))]) < d:
        # вот это плохо, если нет решения выводяться пустые значения
        return [list(np.repeat(None, len(y)))]

    # случий 6
    if 0 < d == np.sum([y[i]['coef'] for i in range(len(y))]) and all(y[i]['coef'] < d for i in range(len(y))):
        return [list(np.repeat(1, len(y)))]

    # случий 7
    if 0 < d < np.sum(
            [y[i]['coef'] for i in range(len(y))]) and all(y[i]['coef'] < d for i in range(len(y))) \
            and np.sum([y[i]['coef'] for i in range(1, len(y))]) < d:
        solutions = []
        for answer in equation_solution(y[1:len(y)], d - y[0]['coef']):
            solutions.append(list(np.concatenate(([1], answer))))
        return solutions

    # случий 8
    if 0 < d < np.sum(
            [y[i]['coef'] for i in range(len(y))]) and all(y[i]['coef'] < d for i in range(len(y))) \
            and np.sum([y[i]['coef'] for i in range(1, len(y))]) >= d:
        solutions = []
        # a
        for answer in equation_solution(y[1:len(y)], d - y[0]['coef']):
            solutions.append(list(np.concatenate(([1], answer))))
        # b
        for answer in equation_solution(y[1:len(y)], d):
            solutions.append(list(np.concatenate(([0], answer))))
        return solutions

    # не случий
    return [list(np.repeat(None, len(y)))]


# функция преобразования T^-1 (шаг 3)
def iverted_transformation_t(y, y_solutions):
    x_solutions = []
    for solution in y_solutions:
        x_solutions.append(list(np.repeat('-', len(solution))))
        for i in range(len(y)):
            if solution[i] == '-':
                x_solutions[-1][y[i]['iter']] = '-'
            else:
                x_solutions[-1][y[i]['iter']
                                ] = int(not solution[i]) if y[i]['inv'] else solution[i]
    return x_solutions


# функция решения задачи
def solve_equation_problem(a, b, k):
    # Шаг 1 (Преобразование T)
    y, d = transformation_t(a, b, k)
    # Шаг 2 (Решения уровнения 5.7)
    y_solutions = equation_solution(y, d)
    # строим семейство решений
    # for solution in y_solutions:
    #  for i in reversed(range(len(solution))):
    #    if solution[i] == 0:
    #      solution[i] = '-'
    #    else:
    #      break
    # Шаг 3 (Обратное преобразование T)
    x_solutions = iverted_transformation_t(y, y_solutions)

    x_solutions_copy = []

    # убераем решения, которых нет
    for item in x_solutions:
        if None not in item:
            x_solutions_copy.append(item)

    # возврашаем ответ
    return x_solutions_copy
