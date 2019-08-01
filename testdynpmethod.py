import time, os, pprint
import random
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
            M = [[0] * t_max] * (n + 1)
            A = [False] * n
            B = [False] * n

            xx = pos.copy()

            for t in range(gamma - 1, t_max):
                xx[t].sort()
                x = xx[t].copy()
                xInput = pos[t].copy()

                for i in range(2, n + 1):
                    check = True
                    if abs(xx[t][i] - xx[t][i - 1]) <= d and check:

                        trouve = False
                        if x[i] in xInput[1::]:
                            ii = xInput[1::].index(x[i])
                            temp = xInput[ii + 1]
                            xInput[ii + 1] = -1
                            if x[i - 1] in xInput[1::]:
                                trouve = True
                                iii = xInput[1::].index(x[i - 1])
                                xInput[iii + 1] = -1
                                # Edges.append((ii, iii))

                            M[t][ii] = M[t][xInput[1::].index(i - 2)] + 1
                        if not trouve:
                            xInput[ii + 1] = temp




                    else:
                        pass





    else:
        os.remove(file)


def mathing_dp_2D(file):
    with open(file, 'r') as f:
        n, y, d = list(map(int, f.readline().split()))
        i = 0
        x = [[0] * (n + 1)] * (y + 1)

        for line in f.readlines():
            print(line)
            x[i] = list(map(int, line.split(",")))
            i += 1
        print("************print X *********************")
        pprint.pprint(x)
        print("**************************************")
        print(machingDP_t_2D(int(n), int(y), d, x))
        print("**************************************")


def machingDP_t_2D(n, y, d, xInput):
    x = xInput.copy()

    M = [[0] * (n + 1)] * (y + 1)

    for i in range(2, y + 1):
        for j in range(2, n + 1):

            if abs(x[i][j] - x[i - 1][j]) <= d and abs(x[i][j - 1] - x[i - 1][j - 1]) <= d:
                M[i][j] = M[i - 2][j] + 1
                print("M[", i, "][", j, "]=", M[i][j])
            else:
                M[i][j] = M[i - 1][j]

    print("!!!!!!!!!!!!!!!!!!!!!")
    pprint.pprint(M)


def mathing_dp(file):
    with open(file, 'r') as f:
        n, d = list(map(int, f.readline().split()))
        x = list(map(int, f.readline().split(",")))
        print(matchingDP_t(n, d, x))


def matchingDP_t(n, d, xInput):
    x = xInput.copy()
    x.sort()
    M = [0] * (n + 1)  # M[i] est le matching max en n'utilisant que les sommets 0,1,2,3,...,i-1

    Edges = []

    for i in range(2, n + 1):
        if abs(x[i] - x[i - 1]) <= d:

            trouve = False
            if x[i] in xInput[1::]:
                ii = xInput[1::].index(x[i])
                temp = xInput[ii + 1]
                xInput[ii + 1] = -1
                if x[i - 1] in xInput[1::]:
                    trouve = True
                    iii = xInput[1::].index(x[i - 1])
                    xInput[iii + 1] = -1
                    Edges.append((ii, iii))
                M[i] = M[i - 2] + 1
            if not trouve:
                xInput[ii + 1] = temp
                M[i] = M[i - 2] + 1

        else:
            M[i] = M[i - 1]
    return M, Edges


def genGammaEdges():
    path = "/home/katia/Bureau/testbed/tests/"
    for file in os.listdir(path):
        file_output = path + file.replace(".position", ".nb_matching")
        if file.endswith('.position'):
            with open(path + file) as f:
                print("file : ", file)
                n, t_max, d = list(map(int, f.readline().split()))
                x = [[]] * t_max
                M = [0] * t_max
                with open(file_output, "+w") as f_outPut:
                    f_outPut.write(str(n) + " " + str(t_max) + " " + str(d) + "\n")
                    for line in f:
                        t, pos = line.split("[")
                        t = int(t)
                        x[t] = list(map(int, pos.replace("]", "").replace(",", " ").split()))
                        M[t], edges = matchingDP_t(n, d, [0] + x[t])
                        f_outPut.write(str(M[t][-1]) + " " + str(edges) + "\n")
                        # f_outPut.write(str(t) + " " + str(x[t]) + " " + str(M[t][-1]) + " " + str(edges) + "\n")
                pprint.pprint(M)


def gammaMatchig1DV0(n, tmax, d, xInput):
    print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
    """

        :param n: nb sommet
        :param d: distance
        :param xInput: toutes les positions pour chaque sommets pour chaque t
        :return:
        """

    M = np.zeros((n + 1, tmax + 1)).astype(int)

    x = xInput.copy()

    for i in range(2, n + 1):

        M[i][1] = M[i - 1][tmax]

        print("i : ", i)
        print("        <<< M[", i, "][", 0, "] : ", M[i][0])
        print("        <<< M[", i, "][", 1, "] : ", M[i][1])
        # x[i].sort()
        for j in range(2, tmax + 1):
            print("     j : ", j)
            print("    x[", i, "][", j - 1, "] - x[", i - 1, "][", j - 1, " ] : ", x[i][j - 1] - x[i - 1][j - 1])
            print("    x[", i, "][", j - 1, "] : ", x[i][j - 1], " - x[", i - 1, "][", j - 1, " ] : ", x[i - 1][j - 1])
            if abs(x[i][j] - x[i - 1][j]) <= d and abs(x[i][j - 1] - x[i - 1][j - 1]) <= d:
                # ok
                M[i][j] = max(M[i - 2][j - 2], M[i - 2][j]) + 1
                print("        [IF] M[", i, "][", j, "] : ", M[i][j])
                print("        [IF](i-2,j-2) M[", i - 2, "][", j - 2, "] : ", M[i - 2][j - 2])
            else:
                # ko
                M[i][j] = M[i - 1][j - 1]
                print("         [else] M[", i, "][", j, "] : ", M[i][j])
        M[i][0] = M[i][tmax]
        print("******************print M*********************")
        pprint.pprint(M)
        print("**********************************************")
    return M


def gammaMatchig1D(n, tmax, d, xInput):
    print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
    """

        :param n: nb sommet
        :param d: distance
        :param xInput: toutes les positions pour chaque sommets pour chaque t
        :return:
        """

    M = np.zeros((n + 1, tmax + 1)).astype(int)
    A = {"0": [],
         "1": [],
         "2": [],
         "3": [],
         "4": []}
    x = xInput.copy()

    for i in range(2, n + 1):

        M[i][1] = M[i - 1][tmax]

        print("i : ", i)
        print("        <<< M[", i, "][", 0, "] : ", M[i][0])
        print("        <<< M[", i, "][", 1, "] : ", M[i][1])
        # x[i].sort()
        for j in range(2, tmax + 1):
            print("     j : ", j)
            oui = False
            if abs(x[i][j] - x[i - 1][j]) <= d and abs(x[i][j - 1] - x[i - 1][j - 1]) <= d:
                # ok
                if oui:
                    # TODO il faut apslument le vecteur de présence
                    # si y a une intersection alors on fait ce qu'on doit faire ici
                    pass

                else:
                    M[i][j] = max(M[i - 2][j - 2], M[i - 2][j], M[i][j - 2]) + 1
                print("        [IF] M[", i, "][", j, "] : ", M[i][j])
                print("        [IF](i-2,j-2) M[", i - 2, "][", j - 2, "] : ", M[i - 2][j - 2])
                print("        [IF](i-2,j) M[", i - 2, "][", j, "] : ", M[i - 2][j])
                print("        [IF](i,j-2) M[", i, "][", j - 2, "] : ", M[i][j - 2])
            else:
                # ko
                M[i][j] = M[i - 1][j - 1]
                print("         [else] M[", i, "][", j, "] : ", M[i][j])
        M[i][0] = M[i][tmax]
        # print("******************print M*********************")
        # pprint.pprint(M)
        print("**********************************************")
    return M


def unzip(ls):
    if isinstance(ls, list):
        if not ls:
            return [], []
        else:
            xs, ys = zip(*ls)

        return list(xs), list(ys)
    else:
        raise TypeError


def test_unzip():
    xs = [4, 2, 6, 9, 0]
    print("AVANT arr : ", xs)
    i_xs = [(x, i) for (i, x) in enumerate(xs)]
    s = sorted(i_xs)
    sorted_xs, index_lst = unzip(s)

    # quickSort(index, arr, 0, n - 1)
    print("APRES arr : ", sorted_xs)
    print("    index : ", index_lst)


if __name__ == '__main__':
    file = "testformuleDP"
    with open(file, 'r') as f:
        n, tmax, d = list(map(int, f.readline().split()))
        x = [[0] * (tmax + 1)] * (n + 1)
        i = 0
        for line in f.readlines():
            x[i] = list(map(int, line.split(",")))
            i += 1

        print("*********************print x*******************************")
        pprint.pprint(x)
        print("***********************************************************")
        pprint.pprint(gammaMatchig1D(n, tmax, d, x))
    # genGammaEdges()

# xMax=20
# d=1
# n=10
# #
# position=list(map(lambda x:random.randint(0,xMax-1),[0]*n))
# # print(position)
# #
# # position.sort()
# # position = [0, 0, 0, 0, 0, 0]
# print(position)
#
# print(matchingDP_t(n, d, [0] + position))
