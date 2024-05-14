from ctypes import Array
import numpy as np
import random
from Solver import solve_equation_problem


def unison_shuffled_copies(a: Array[int], b: Array[int]):
    shuffled_indices = list(range(len(a)))
    random.shuffle(shuffled_indices)

    shuffled_a = [a[i] for i in shuffled_indices]
    shuffled_b = [b[i] for i in shuffled_indices]

    return shuffled_a, shuffled_b


def task_generator(num_variants: int, number_of_parameters: int):
    vlist = []
    dlist = []

    for v in range(num_variants):
        glist = []
        slist = []
        a = []
        b = []
        k = 0
        answers = []

        if number_of_parameters == 2:
            a = []
            b = []
            a.append(random.randint(1, 10))
            if bool(random.getrandbits(1)):
                a[-1] = -a[-1]
            a.append(random.randint(1, 10))
            if bool(random.getrandbits(1)):
                a[-1] = -a[-1]
            k = np.sum(a)
            b.append(random.randint(1, 10))
            if bool(random.getrandbits(1)):
                b[-1] = -b[-1]
            b.append(0)

        if number_of_parameters > 2:
            k = random.randint(1, 5)
            if bool(random.getrandbits(1)):
                k = -k
            for j in range((number_of_parameters - 1) // 2):
                answers.append(random.randint(1, 10))
                if bool(random.getrandbits(1)) or answers[-1] == k:
                    answers[-1] = -answers[-1]
                answers.append(k - answers[-1])
            answers.append(0)

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
        a, b = unison_shuffled_copies(a, b)
        glist.append([a, b, k])
        slist.append(solve_equation_problem(
            glist[-1][0], glist[-1][1], glist[-1][2]))
        vlist.append(glist)
        dlist.append(slist)

    return vlist, dlist


if __name__ == "__main__":
    a, b = task_generator(3, 5)
    print(a)
    print('---------------------------------------------------------------------------------')
    print(b)
