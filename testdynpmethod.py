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

                        # Edges = matchingMax(CEdges)  # <--- utiliser une bibliotheque existiante, p.e. tryalgo: pip install tryalgo

                        # M[0][t] += len(Edges)

                        # for i,j in Edges:
                        #     B[i] = True
                        #     B[j] = True

                    else:

                        M[x][t] = M[x - 1][t]

                        C = filter(lambda i: not A[i] and pos[i][t] == x, range(n))

                        CEdges = filter(lambda i, j: abs(pos[i][t - 1] - pos[j][t - 1]) <= d,
                                        list(itertools.product(C, C)))
                        # CEdges = []
                        # for i in C:
                        #     for j in C:
                        #         if abs(pos[i][t-1] - pos[j][t-1])<=d:
                        #             CEdges.append((i,j))

                        # Edges = matchingMax(CEdges)  # <--- utiliser une bibliotheque existiante, p.e. tryalgo: pip install tryalgo
                        #
                        # M[x][t] += len(Edges)
                        #
                        # if M[x][t] > cas2:
                        #     for i,j in Edges:
                        #         B[i] = True
                        #         B[j] = True
                        # else:
                        #     if cas2 > M[x][t]:
                        #         M[x][t] = MDuCas2
                        #         mettreAJourBPourCas2
                        #     else:
                        #         ????????
                        #

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


def matchingDPT(file):
    print("je suis la ")
    with open(file, 'r') as f:
        n, d = f.readline().split()
        x = list(map(int, f.readline().split(',')))
        M = []
        M[0] = 0
        M[1] = 0
    print("x : ", x)


def nb_gamma_edge(n, t, d, pos):
    x = pos.copy()
    nb_g_edge = 0
    g_edge = True
    for pos_u in x[t]:
        idx_u = x[t].index(pos_u)
        for pos_v in x[t]:
            if x[t].index(pos_u) <= x[t].index(pos_v):
                continue
            idx_v = x[t].index(pos_v)
            if abs(pos_u - pos_v) <= d:
                for t_g in range(t - 1, t - gamma + 1):
                    if abs(x[t_g][idx_u] - x[t_g][idx_v]) > d:
                        g_edge = False
                        break
                if g_edge:
                    nb_g_edge += 1
    if nb_g_edge > n:
        nb_g_edge = n - 1
    return int(nb_g_edge / 2)


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
    file = "test_one_t"
    matchingDPT(file)
