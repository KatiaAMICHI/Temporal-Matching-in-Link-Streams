import copy
import os
from functools import reduce
import numpy
import pprint

gamma = 2


def mathing_dp(file):
    with open(file, 'r') as f:
        n, d = list(map(int, f.readline().split()))
        x = list(map(int, f.readline().split(",")))
        print(matchingDP_t(n, d, x))


def matchingDP_t(n, d, t, xInput):
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
                    Edges.append((t, ii, iii))
                M[i] = M[i - 2] + 1
            if not trouve:
                xInput[ii + 1] = temp
                M[i] = M[i - 2] + 1

        else:
            M[i] = M[i - 1]
    return M, Edges


def dpstatic(n, d, t, xInput):
    x = xInput.copy()
    print(" x : ", x)
    argsort = list(numpy.argsort(x)) + [n]
    M = [0] * (n + 1)
    firstSeen = [True] * n
    # print(">> Proceeding DP for maximum matching:")
    edges = []
    for i in range(1, n):
        if abs(x[argsort[i]] - x[argsort[i - 1]]) <= d:
            M[argsort[i]] = M[argsort[i - 2]] + 1
            if firstSeen[argsort[i]] and firstSeen[argsort[i - 1]]:
                # print("  ...found vertices:", argsort[i], argsort[i - 1], "; x-positions:", x[argsort[i]],
                #    x[argsort[i - 1]])
                edges.append((t, argsort[i], argsort[i - 1]))
                firstSeen[argsort[i]] = False
                firstSeen[argsort[i - 1]] = False
        else:
            M[argsort[i]] = M[argsort[i - 1]]
    max_matching = reduce(max, M)
    print("--> Maximum matching size:", reduce(max, M))
    return max_matching, edges


def genGammaEdges():
    path = r"./testbed/tests/"

    result = []
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
                        max_matching, edges = dpstatic(n, d, t, x[t])
                        # M[t], edges = matchingDP_t(n, d, t, [0] + x[t])
                        result.append((max_matching, edges))  # ajout du tuple (nb_matching, [les matching])
                        f_outPut.write(str(max_matching) + " " + str(edges) + "\n")
                        # f_outPut.write(str(t) + " " + str(x[t]) + " " + str(M[t][-1]) + " " + str(edges) + "\n")
    return result


def gammaMatchig1D(n, tmax, d, xInput):
    print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
    """
        OK
        :param n: nb sommet
        :param d: distance
        :param xInput: toutes les positions pour chaque sommets pour chaque t
        :return:
        """

    M = numpy.zeros((n + 1, tmax + 1)).astype(int)
    A = {}
    B = {}

    for i in range(tmax + 1):
        A[i] = []
        B[i] = []

    # A = [[]] * (tmax+1)
    x = xInput.copy()
    nb_matching_b = 0
    for i in range(2, n + 1):

        M[i][1] = M[i - 1][tmax]

        print("i : ", i)
        print("        <<< M[", i, "][", 0, "] : ", M[i][0])
        print("        <<< M[", i, "][", 1, "] : ", M[i][1])
        # x[i].sort()
        for j in range(2, tmax + 1):
            print("     j : ", j)
            if abs(x[i][j] - x[i - 1][j]) <= d and abs(x[i][j - 1] - x[i - 1][j - 1]) <= d:
                # ok
                print("**************** A *******************")
                pprint.pprint(A)
                print("1 **************** B *******************")
                pprint.pprint(B)
                print("**************************************")
                bool_inter, nb_inter, nb_matching_b, Bp = intersectionA(A, B.copy(), j, i, i - 1, nb_matching_b)
                if bool_inter:
                    # si y a une intersection alors on fait ce qu'on doit faire ici
                    if j - 2 == 0:
                        M[i][j] = max(M[i - 2][j - 2], M[i - 2][j], (M[i - 1][j - 2] - nb_inter)) + 1

                    else:
                        M[i][j] = max(M[i - 2][j - 2], M[i - 2][j], (M[i][j - 2] - nb_inter)) + 1
                    if nb_inter == 1 and M[i][j] <= M[i][j - 1]:
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        print("2 **************** B *******************")
                        pprint.pprint(B)
                        print("**************************************")
                        B = Bp
                        if not intersectionB(B, j, i, i - 1):
                            nb_matching_b += 1
                            B[j].append((i, i - 1))
                    M[i][j] = max(M[i][j], M[i][j - 1])
                    print("3 **************** B *******************")
                    pprint.pprint(B)
                    print("**************************************")
                    print("        [IF][IF] M[", i, "][", j, "] : ", M[i][j])
                    print("        [IF][IF](i-2,j-2) M[", i - 2, "][", j - 2, "] : ", M[i - 2][j - 2])
                    print("        [IF][IF](i-2,j) M[", i - 2, "][", j, "] : ", M[i - 2][j])
                    print("        [IF][IF](i,j-2) M[", i, "][", j - 2, "] : ", M[i][j - 2])
                else:
                    # je viens de rajouter le verre
                    M[i][j] = max(M[i - 2][j - 2], M[i - 2][j], M[i][j - 2]) + 1
                    # j où c'est la fin de notre gammamatching, il faut tester sur [j,j-gamma+1]
                    A[j].append((i, i - 1))  # ajout de (u,v)
                    if not intersectionB(B, j, i, i - 1):
                        B[j].append((i, i - 1))  # ajout de (u,v)
                        nb_matching_b += 1

                    print("je rajoute:", i, i - 1)
                    print("        [IF][else] M[", i, "][", j, "] : ", M[i][j])
                    print("        [IF][else](i-2,j-2) M[", i - 2, "][", j - 2, "] : ", M[i - 2][j - 2])
                    print("        [IF][else](i-2,j) M[", i - 2, "][", j, "] : ", M[i - 2][j])
            else:
                # ko
                M[i][j] = max(M[i - 1][j - 1], M[i][j - 1])
                print("         [else] M[", i, "][", j, "] : ", M[i][j])
        M[i][0] = M[i][tmax]
        print("******************print A*********************")
        pprint.pprint(A)
        print("**********************************************")
        print()
        print("Résult DP ")
        # print(numpy.matrix(M))
        print("nb_matching_A :", M[n][tmax])
        print("nb_matching_B : ", nb_matching_b)

    return M


def intersectionA(A, Bp, t, u, v, nb_matching_b):
    """
    OK
    :param A:
    :param Bp:
    :param t:
    :param u:
    :param v:
    :param nb_matching_b:
    :return:
    """
    gamma = 2
    nb_inter = 0
    bool_inter = False
    B = copy.deepcopy(Bp)
    for i in range(t - gamma + 1, t + gamma):
        if i not in range(len(A)):
            break
        for edge in A[i]:
            if u in edge or v in edge:
                bool_inter = True
                if t in range(t - gamma - 1, t - 1) or (u > edge[0] and v == edge[0]) or (u == edge[0] and v > edge[0]):
                    if edge in B[i]:
                        B[i].remove(edge)
                        nb_matching_b -= 1
                    nb_inter += 1
    print(">>>>>>>>>>>>>>>>>>>>>>><<<<<<<><<<<>><<<<<<<>> nb_inter :", nb_inter)
    return bool_inter, nb_inter, nb_matching_b, B


def intersectionB(B, t, u, v):
    """
    Ok
    :param B:
    :param t:
    :param u:
    :param v:
    :return:
    """
    gamma = 2

    # on vérifie sur t-1 que par ce que ici on travaille avec gamma=2
    if (u, v) in B[t] or (u, v) in B[t - 1]:
        return True
    for i in range(t - gamma + 1, t + gamma):
        if i not in range(len(B)):
            break
        for edge in B[i]:
            if u in edge or v in edge:
                print("t:", t, " edge : ", edge)
                print("u:", u, "v:", v)
                bool_inter = True
                if t in range(t - gamma - 1, t - 1) or (u > edge[0] and v == edge[0]) or (u == edge[0] and v > edge[0]):
                    return True
    return False


def unzip(ls):
    """
    OK
    Pour trier une list et save les indexs
    :param ls:
    :return:
    """
    if isinstance(ls, list):
        if not ls:
            return [], []
        else:
            xs, ys = zip(*ls)

        return list(xs), list(ys)
    else:
        raise TypeError


def test_unzip():
    """
    OK
    :return:
    """
    xs = [4, 2, 6, 9, 0]
    print("AVANT arr : ", xs)
    i_xs = [(x, i) for (i, x) in enumerate(xs)]
    s = sorted(i_xs)
    sorted_xs, index_lst = unzip(s)

    # quickSort(index, arr, 0, n - 1)
    print("APRES arr : ", sorted_xs)
    print("    index : ", index_lst)


def mainResultDP():
    # TODO faut encore rajouter le truc du trie sinon ne fonctionne pas pour le moment
    file = "testformuleDP5"
    file_output = r"./testbed/tests/test0001.position"
    file_output = r"./testbed/tests/test0001.linkstreamToPosition"

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
        gammaMatchig1D(n, tmax, d, x)


if __name__ == '__main__':
    # test_unzip()
    genGammaEdges()
