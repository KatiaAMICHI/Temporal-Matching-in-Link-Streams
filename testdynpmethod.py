import time, os, pprint
import numpy as np

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
            M = [[[[0] * (2 ** x_max)] * (2 ** x_max)] * t_max] * x_max
            # pprint.pprint(M)

            for x in range(x_max):
                print("x : ", x)
                for t in range(gamma - 1, t_max):
                    print("t : ", t)
                    for a in range(2 ** x_max):
                        for b in range(2 ** x_max):
                            if x == 0:
                                # print("nb_g_edge : ", nb_gamma_edge(n, t, d, pos))
                                M[0][t][a][b] = M[x_max - 1][t - 1][a][b] + nb_gamma_edge(n, t, d, pos)
                            M[x][t][a][b] = M[x-1][t][a][b]
                            for pos_u in pos[t]:
                                idx_u = pos[t].index(pos_u)
                                for pos_v in pos[t]:
                                    if pos[t].index(pos_u) <= pos[t].index(pos_v):
                                        continue
                                    idx_v = pos[t].index(pos_v)
                                    if pos[t][idx_u] == x and pos[t][idx_v] == x -1 :
                                        pass



    else:
        os.remove(file)


"""
la méthode rnvoie le nombre de gamma edge pour un t passé en paramètre              
"""


def nb_gamma_edge(n, t, d, pos):
    x = pos.copy()
    nb_g_edge = 0
    g_edge = True
    # print("x[t] : ", x[t])
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


path = "/home/katia/Bureau/testbed/tests/"
for file in os.listdir(path):
    if file.endswith('.position'):
        with open(path + file) as f:
            print("file : ", file)
            n, t_max, d = list(map(int, f.readline().split()))
            x = [[]] * t_max
            for line in f:
                t, pos = line.split("[")
                t = int(t)
                x[t] = list(map(int, pos.replace("]", "").replace(",", " ").split()))
            pprint.pprint(x)

            matchingDP(n, t_max, d, x, path + file.replace("position", "resultDP"))
