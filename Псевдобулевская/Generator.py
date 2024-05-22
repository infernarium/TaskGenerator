from ctypes import Array, Union
import numpy as np
import random
from TaskGenerator.Псевдобулевская.Solver import solve_equation_problem
from Solver import solve_equation_problem


def generate_random_number(max_value, allow_negative=True):
    num = random.randint(1, max_value)
    return -num if allow_negative and random.getrandbits(1) else num


def join_shuffeling(a: Array[int], b: Array[int]):
    shuffled_indices = list(range(len(a)))
    random.shuffle(shuffled_indices)

    shuffled_a = [a[i] for i in shuffled_indices]
    shuffled_b = [b[i] for i in shuffled_indices]

    return shuffled_a, shuffled_b


def task_generator(num_variants: int, number_of_parameters: int):
    vlist = []
    dlist = []

    # Проходимся по всем вариантам
    for v in range(num_variants):
        glist = []
        slist = []
        a = []
        b = []
        k = 0
        answers = []

        # Если количество x_i = 2
        if number_of_parameters == 2:
            a = [generate_random_number(10, True) for _ in range(2)]
            k = np.sum(a)
            b = [generate_random_number(10, True), 0]

        # Если количество x_i > 2
        if number_of_parameters > 2:
            k = generate_random_number(5, True)
            for j in range((number_of_parameters - 1) // 2):
                answers.append(random.randint(1, 10))
                if bool(random.getrandbits(1)) or answers[-1] == k:
                    answers[-1] = -answers[-1]
                answers.append(k - answers[-1])
            answers.append(0)

            # Если i чётное
            if number_of_parameters % 2 == 0:
                answers.append(random.randint(1, 5))
                if bool(random.getrandbits(1)) or answers[-1] == k:
                    answers[-1] = -answers[-1]
                answers.append(random.randint(1, 5))

                if bool(random.getrandbits(1)) or answers[-1] == k:
                    answers[-1] = -answers[-1]

                if answers[-1] == answers[0]:
                    answers[-1] = k - answers[0]

                if answers[-1] + answers[-2] == k or answers[-1] + answers[-2] == 0:
                    answers[-1] += k + answers[0]

                answers[-3] = k - answers[-1] - answers[-2]

            # Если i не чётное
            else:
                answers.append(random.randint(1, 5))
                if bool(random.getrandbits(1)) or answers[-1] == k:
                    answers[-1] = -answers[-1]

                if answers[-1] == answers[0]:
                    answers[-1] = k - answers[0]

                answers.append(random.randint(1, 5))
                if bool(random.getrandbits(1)) or answers[-1] == k:
                    answers[-1] = -answers[-1]

                if answers[-1] == answers[1]:
                    answers[-1] = k - answers[1]

                if answers[-1] + answers[-2] == k or answers[-1] + answers[-2] == 0:
                    answers[-1] += k + answers[1]

                answers[-3] = k - answers[-1] - answers[-2]
            a = answers[0:number_of_parameters]
            b = answers[number_of_parameters:]
            b = list(np.concatenate(
                (b, list(np.repeat(0, number_of_parameters - len(b))))))
        a, b = join_shuffeling(a, b)
        glist.append([a, b, k])
        slist.append(solve_equation_problem(
            glist[-1][0], glist[-1][1], glist[-1][2]))
        vlist.append(glist)
        dlist.append(slist)

    return vlist, dlist


if __name__ == "__main__":
    a, b = task_generator(2, 5)
    print(a)
    print('---------------------------------------------------------------------------------')
    print(b)
