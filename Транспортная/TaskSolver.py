import cvxpy as cp
import numpy as np


def is_integer_solution(solution):
    return np.all(np.equal(np.mod(solution, 1), 0))


def solve_transport_problem(A, B, C):

    num_departure_points = len(A)
    num_destination_points = len(B)

    # Переменная решения размером
    # [num_departure_points, num_destination_points]
    X = cp.Variable((num_departure_points, num_destination_points),
                    integer=True)

    # Ограничения на количество отправляемого груза из каждого пункта
    constraints = []
    constraints.extend(
        [cp.sum(X[i, :]) <= A[i] for i in range(num_departure_points)])
    # Ограничения на количество получаемого груза каждым пунктом назначения
    constraints.extend(
        [cp.sum(X[:, j]) >= B[j] for j in range(num_destination_points)])
    # Ограничения на неотрицательность переменной
    constraints.extend(
        [X[i, j] >= 0 for i in range(num_departure_points) for j in
         range(num_destination_points)])

    # Целевая функция - минимизация стоимости перевозок
    objective = cp.Minimize(cp.sum(cp.multiply(C, X)))

    # Постановка задачи линейного программирования
    problem = cp.Problem(objective, constraints)

    # Решение задачи
    problem.solve()

    solution = X.value

    integer_solution = np.abs(np.rint(solution).astype(int))
    # Проверка на целочисленность решения

    return integer_solution, problem.value
