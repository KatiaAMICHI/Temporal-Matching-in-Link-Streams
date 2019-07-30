import time, os, pprint
import numpy as np
import itertools

gamma = 2


def matchingDP(n, t_max, d, pos, file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write(str(n) + " " + str(t_max) + " " + str(d) + "\n")
            x_max = -1
            for i in pos:
                for j in i:
                    if x_max < j:
                        x_max = j
            print("x_max : ", x_max)
            M = [[0] * t_max] * x_max
            A = [False] * n
            B = [False] * n

            for x in range(x_max):
                for t in range(gamma - 1, t_max):

                    if x == 0:
                        A = B
                        B = [False] * n

                        M[0][t] = M[x_max - 1][t - 1]

                        C = filter(lambda i: not A[i] and pos[i][t] == 0, range(n))

                        CEdges = filter(lambda i, j: abs(pos[i][t - 1] - pos[j][t - 1]) <= d,
                                        list(itertools.product(C, C)))
                        # CEdges = []
                        # for i in C:
                        #     for j in C:
                        #         if abs(pos[i][t-1] - pos[j][t-1])<=d:
                        #             CEdges.append((i,j))

                    #     Edges = matchingMax(CEdges)  # <--- utiliser une bibliotheque existiante, p.e. tryalgo: pip install tryalgo
                    #
                    #     M[0][t] += len(Edges)
                    #
                    #     for i,j in Edges:
                    #         B[i] = True
                    #         B[j] = True
                    #
                    # else:
                    #
                    #
                    #     M[x][t] = M[x - 1][t]
                    #
                    #     C = filter(lambda i: not A[i] and pos[i][t] == x, range(n))
                    #
                    #     CEdges = filter(lambda i, j: abs(pos[i][t - 1] - pos[j][t - 1]) <= d,
                    #                     list(itertools.product(C, C)))
                    #     # CEdges = []
                    #     # for i in C:
                    #     #     for j in C:
                    #     #         if abs(pos[i][t-1] - pos[j][t-1])<=d:
                    #     #             CEdges.append((i,j))
                    #
                    #     Edges = matchingMax(CEdges)  # <--- utiliser une bibliotheque existiante, p.e. tryalgo: pip install tryalgo
                    #
                    #     M[x][t] += len(Edges)
                    #
                    #     if M[x][t] > cas2:
                    #         for i,j in Edges:
                    #             B[i] = True
                    #             B[j] = True
                    #     else:
                    #         if cas2 > M[x][t]:
                    #             M[x][t] = MDuCas2
                    #             mettreAJourBPourCas2
                    #         else:
                    #             ????????

                    # M[x][t][a][b] = M[x - 1][t][a][b]
                    # for pos_u in pos[t]:
                    #     idx_u = pos[t].index(pos_u)
                    #     for pos_v in pos[t]:
                    #         if pos[t].index(pos_u) <= pos[t].index(pos_v):
                    #             continue
                    #         idx_v = pos[t].index(pos_v)
                    #         if pos[t][idx_u] == x and pos[t][idx_v] == x - 1 and (
                    #                 pos[t - 1][idx_v] == pos[t - 1][idx_u] - 1 or
                    #                 pos[t - 1][idx_u] == pos[t - 1][idx_v] - 1) and \
                    #                 M[x-2][t][...][b] > M[x][t][a][b]:
                    #             M[x][t][a][b] = M[x - 2][t][...][b] + nb_gamma_edge(n, t, d, pos)

    else:
        os.remove(file)


def mathing_dp(file):
    with open(file, 'r') as f:
        n, d = list(map(int, f.readline().split()))
        x = list(map(int, f.readline().split(",")))
        print(mathingDP_t(n, d, x))


def mathing_dp_2D(file):
    with open(file, 'r') as f:
        n, y, d = list(map(int, f.readline().split()))
        i = 0
        x = [[0] * (n + 1)] * (y + 1)

        for line in f.readline():
            x[i] = list(map(int, line.split(",")))
        print("**************************************")
        pprint.pprint(x)
        print("**************************************")
        print(machingDP_t_2D(n, y, d, x))


def machingDP_t_2D(n, y, d, x):
    M = [[0] * (n + 1)] * (n + 1)
    for i in range(2, n + 1):
        for i in range(2, y):
            cond1 = abs(x[i][y] - x[i - 1][y]) <= d
            cond2 = abs(x[i][y] - x[i - 1][y - 1]) <= d

            if cond1 and cond2:
                M[i] = max(M[i - 2][y - 2], M[i - 2][y - 2]) + 1
            elif cond1:
                M[i] = M[i - 2][y - 1] + 1
            elif cond2:
                M[i] = M[i - 1][y - 2] + 1
            else:
                M[i] = M[i - 1][y - 1]


def mathingDP_t(n, d, x):
    M = [0] * (n + 1)

    for i in range(2, n + 1):
        if abs(x[i] - x[i - 1]) <= d:
            M[i] = M[i - 2] + 1

        else:
            M[i] = M[i - 1]
    return M


if __name__ == '__main__':
    # path = "/home/katia/Bureau/testbed/tests/"
    # for file in os.listdir(path):
    #     if file.endswith('.position'):
    #         with open(path + file) as f:
    #             print("file : ", file)
    #             n, t_max, d = list(map(int, f.readline().split()))
    #             x = [[]] * t_max
    #             for line in f:
    #                 t, pos = line.split("[")
    #                 t = int(t)
    #                 x[t] = list(map(int, pos.replace("]", "").replace(",", " ").split()))
    #             pprint.pprint(x)
    #
    #             matchingDP(n, t_max, d, x, path + file.replace("position", "resultDP"))
    file = "test_t2.position"
    machingDP_t_2D(file)
