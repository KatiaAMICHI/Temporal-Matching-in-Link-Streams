import numpy
import copy
import pprint

gamma = 2
# TODO faut refaire a la main la méthode
# TODO faut vérifeir si :
# je dois parcourir par raport a la distance ou par rapport au sommets

class DpGammaMatching1D:
    def __init__(self, n, tmax, d, xInput, r):
        self.n = n
        self.tmax = tmax
        self.d = d
        self.xInput = xInput
        self.r = r

    def gammaMatchig1DSort(self):
        """
            OK
            :param n: nb sommet
            :param d: distance
            :param xInput: toutes les positions pour chaque sommets pour chaque t
            :return:
        """

        M = numpy.zeros((self.n, self.tmax)).astype(int)
        A = {}
        B = {}

        for i in range(self.tmax):
            A[i] = []
            B[i] = []

        x = self.xInput.copy()
        argsort = list(numpy.argsort(x.transpose()))
        nb_matching_b = 0

        for i in range(1, self.n):
            M[i][0] = M[i - 1][self.tmax - 1]
            print(".........................................................................................i : ", i)
            for j in range(1, self.tmax):
                print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,j : ", j)
                pprint.pprint(M)
                print("x[", argsort[j][i], "][", j, "] - x[", argsort[j][i - 1], "][", j, "])")

                # loop de i-1 -> 0 où quand al distance > d
                onPeutSup = False
                finSup = False
                if i + 1 < self.n and abs(x[argsort[j][i]][j] - x[argsort[j][i + 1]][j]) <= self.d:
                    # v = i + 1
                    # onPeutSup = True
                    pass
                v = i - 1

                while True:
                    print("1 je suis la ")

                    hasEdges = abs(x[argsort[j][i]][j] - x[argsort[j][v]][j]) <= self.d and abs(
                        x[argsort[j][i]][j - 1] - x[argsort[j][v]][j - 1]) <= self.d

                    bool_interA, nb_inter, nb_matching_b, Bp = self.intersectionA(A, B.copy(), j, argsort[j][i],
                                                                                  argsort[j][v],
                                                                                  nb_matching_b)
                    if (hasEdges and not bool_interA) or abs(x[argsort[j][i]][j] - x[argsort[j][v]][j]) > self.d:
                        print("     22 je suis la ", v)
                        break
                    print("3 je suis la ", v)

                    if not onPeutSup:
                        print("je suis la DDDD", onPeutSup)
                        v -= 1
                    print("4 je suis la ", v)

                    if v < 0:
                        # alors on peut checker pour les truc qui sont au dessus de nous
                        print("je suis la 2 ", hasEdges, v)
                        onPeutSup = True
                        v = i

                    if v + 1 >= self.n:
                        finSup = True
                        print("je suis la ", v)
                    if onPeutSup and not finSup and v >= i and abs(
                            x[argsort[j][i]][j] - x[argsort[j][v + 1]][j]) <= self.d:
                        v += 1
                        print(" onPeutSup !!!!!!!", v)
                    else:
                        break

                    if v < 0 or v > self.n - 1:
                        print("     11 je suis la ")
                        break
                    print("2 je suis la ", v)

                if hasEdges:
                    print('OK')
                    print("**************** A *************")
                    pprint.pprint(A)
                    print("1 **************** B ***********")
                    pprint.pprint(B)
                    print("********************************")

                    bool_interA, nb_inter, nb_matching_b, Bp = self.intersectionA(A, B.copy(), j, argsort[j][i],
                                                                                  argsort[j][v],
                                                                                  nb_matching_b)
                    if bool_interA:
                        print("bool_interA")
                        if j - 2 == 0:
                            M[i][j] = max(M[i - 2][j - 2], M[i - 2][j], (M[i - 1][j - 2] - nb_inter)) + 1
                        else:
                            M[i][j] = max(M[i - 2][j - 2], M[i - 2][j], (M[i][j - 2] - nb_inter)) + 1
                        if nb_inter == 1 and M[i][j] <= M[i][j - 1]:
                            print("2 **************** B ************")
                            pprint.pprint(B)
                            print("*********************************")
                            B = Bp
                            if not self.intersectionB(B, j, argsort[j][i], argsort[j][v]):
                                nb_matching_b += 1
                                print("je rajoute dans B : ", (argsort[j][i], argsort[j][v]))
                                B[j].append((argsort[j][i], argsort[j][v]))
                            # par ce que dès foit quand on fait nb_inter on peut se retrouver avec un résultat pas ouf donc on dois reprednre notre résultat d'avant
                            M[i][j] = max(M[i][j], M[i][j - 1])
                        print("3 **************** B ************")
                        pprint.pprint(B)
                        print("*********************************")
                        print("        [IF][IF] M[", i, "][", j, "] : ", M[i][j])
                        print("        [IF][IF](i-2,j-2) M[", i - 2, "][", j - 2, "] : ", M[i - 2][j - 2])
                        print("        [IF][IF](i-2,j) M[", i - 2, "][", j, "] : ", M[i - 2][j])
                        print("        [IF][IF](i,j-2) M[", i, "][", j - 2, "] : ", M[i][j - 2])

                    else:
                        if j - 2 == -1:
                            M[i][j] = max(M[i - 2][j - 2], M[i - 2][j], M[i - 1][j - 2]) + 1
                        else:
                            M[i][j] = max(M[i - 2][j - 2], M[i - 2][j], M[i][j - 2]) + 1

                        A[j].append((argsort[j][i], argsort[j][v]))  # ajout de (u,v)
                        if not self.intersectionB(B, j, argsort[j][i], argsort[j][v]):
                            B[j].append((argsort[j][i], argsort[j][v]))  # ajout de (u,v)
                            nb_matching_b += 1
                            M[i][j] = max(M[i][j], M[i][j - 1] + 1)

                        print("je rajoute:", argsort[j][i], argsort[j][v])
                        print("        [IF][else] M[", i, "][", j, "] : ", M[i][j])
                        print("        [IF][else](i-2,j-2) M[", i - 2, "][", j - 2, "] : ", M[i - 2][j - 2])
                        print("        [IF][else](i-2,j) M[", i - 2, "][", j, "] : ", M[i - 2][j])
                else:
                    print("ko")
                    M[i][j] = max(M[i - 1][j - 1], M[i][j - 1])
                    print("         [else] M[", i, "][", j, "] : ", M[i][j])

            print("******************print A**************")
            pprint.pprint(A)
            print("******************print B**************")
            pprint.pprint(B)
            print("***************************************")
            print()
            print("Résult DP ")
            print(numpy.matrix(M))
            print("nb_matching_A :", M[i][self.tmax - 1])
            print("nb_matching_B : ", nb_matching_b)

        print("******************print A**************")
        pprint.pprint(A)
        print("******************print B**************")
        pprint.pprint(B)
        print("***************************************")
        print()
        print("Résult DP ")
        print(numpy.matrix(M))

        max_M = M[self.n - 1][self.tmax - 1]
        max_A = sum(len(v) for v in A.values())
        max_B = nb_matching_b

        print("max_M: ", max_M)
        print("max_A: ", max_A)
        print(numpy.matrix(M))
        print("max_B: ", max_B)

        return max(max_A, max_B)

    def gammaMatchig1DSortV2(self):
        """
            OK
            :param n: nb sommet
            :param d: distance
            :param xInput: toutes les positions pour chaque sommets pour chaque t
            :return:
        """

        M = numpy.zeros((self.n, self.tmax)).astype(int)
        A = {}
        B = {}

        for i in range(self.tmax):
            A[i] = []
            B[i] = []

        x = self.xInput.copy()
        argsort = list(numpy.argsort(x.transpose()))
        nb_matching_b = 0

        for i in r:
            M[i][0] = M[i - 1][self.tmax - 1]
            print(".........................................................................................i : ", i)
            for j in range(1, self.tmax):
                print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,j : ", j)
                pprint.pprint(M)
                print("x[", argsort[j][i], "][", j, "] - x[", argsort[j][i - 1], "][", j, "])")

                # loop de i-1 -> 0 où quand al distance > d
                onPeutSup = False
                finSup = False
                if i + 1 < self.n and abs(x[argsort[j][i]][j] - x[argsort[j][i + 1]][j]) <= self.d:
                    # v = i + 1
                    # onPeutSup = True
                    pass
                v = i - 1

                while True:

                    hasEdges = abs(x[argsort[j][i]][j] - x[argsort[j][v]][j]) <= self.d and abs(
                        x[argsort[j][i]][j - 1] - x[argsort[j][v]][j - 1]) <= self.d
                    if v < 0 or v > self.tmax - 1:
                        break

                    if hasEdges or abs(x[argsort[j][i]][j] - x[argsort[j][v]][j]) > self.d:
                        break

                    print("je suis la DDDD", onPeutSup)
                    if not onPeutSup:
                        v -= 1

                    if v < 0 and not hasEdges:
                        # alors on peut checker pour les truc qui sont au dessus de nous
                        print("je suis la 2 ", hasEdges)
                        onPeutSup = True
                        v = i

                    if v + 1 >= self.n:
                        finSup = True
                        print("je suis la ")
                    if onPeutSup and not finSup and v >= i and abs(
                            x[argsort[j][i]][j] - x[argsort[j][v + 1]][j]) <= self.d:
                        v += 1
                        print(" onPeutSup !!!!!!!")

                    # else:
                    #    finSup = True
                    #    v -= 1

                if hasEdges:
                    print('OK')
                    print("**************** A *************")
                    pprint.pprint(A)
                    print("1 **************** B ***********")
                    pprint.pprint(B)
                    print("********************************")

                    bool_interA, nb_inter, nb_matching_b, Bp = self.intersectionA(A, B.copy(), j, argsort[j][i],
                                                                                  argsort[j][v],
                                                                                  nb_matching_b)
                    if bool_interA:
                        print("bool_interA")
                        if j - 2 == 0:
                            M[i][j] = max(M[i - 2][j - 2], M[i - 2][j], (M[i - 1][j - 2] - nb_inter)) + 1
                        else:
                            M[i][j] = max(M[i - 2][j - 2], M[i - 2][j], (M[i][j - 2] - nb_inter)) + 1
                        if nb_inter == 1 and M[i][j] <= M[i][j - 1]:
                            print("2 **************** B ************")
                            pprint.pprint(B)
                            print("*********************************")
                            B = Bp
                            if not self.intersectionB(B, j, argsort[j][i], argsort[j][v]):
                                nb_matching_b += 1
                                print("je rajoute dans B : ", (argsort[j][i], argsort[j][v]))
                                B[j].append((argsort[j][i], argsort[j][v]))
                        M[i][j] = max(M[i][j], M[i][j - 1])
                        print("3 **************** B ************")
                        pprint.pprint(B)
                        print("*********************************")
                        print("        [IF][IF] M[", i, "][", j, "] : ", M[i][j])
                        print("        [IF][IF](i-2,j-2) M[", i - 2, "][", j - 2, "] : ", M[i - 2][j - 2])
                        print("        [IF][IF](i-2,j) M[", i - 2, "][", j, "] : ", M[i - 2][j])
                        print("        [IF][IF](i,j-2) M[", i, "][", j - 2, "] : ", M[i][j - 2])

                    else:
                        if j - 2 == -1:
                            M[i][j] = max(M[i - 2][j - 2], M[i - 2][j], M[i - 1][j - 2]) + 1
                        else:
                            M[i][j] = max(M[i - 2][j - 2], M[i - 2][j], M[i][j - 2]) + 1

                        A[j].append((argsort[j][i], argsort[j][v]))  # ajout de (u,v)
                        if not self.intersectionB(B, j, argsort[j][i], argsort[j][v]):
                            B[j].append((argsort[j][i], argsort[j][v]))  # ajout de (u,v)
                            nb_matching_b += 1
                            M[i][j] = max(M[i][j], M[i][j - 1] + 1)

                        print("je rajoute:", argsort[j][i], argsort[j][v])
                        print("        [IF][else] M[", i, "][", j, "] : ", M[i][j])
                        print("        [IF][else](i-2,j-2) M[", i - 2, "][", j - 2, "] : ", M[i - 2][j - 2])
                        print("        [IF][else](i-2,j) M[", i - 2, "][", j, "] : ", M[i - 2][j])
                else:
                    print("ko")
                    M[i][j] = max(M[i - 1][j - 1], M[i][j - 1])
                    print("         [else] M[", i, "][", j, "] : ", M[i][j])

            print("******************print A**************")
            pprint.pprint(A)
            print("******************print B**************")
            pprint.pprint(B)
            print("***************************************")
            print()
            print("Résult DP ")
            print(numpy.matrix(M))
            print("nb_matching_A :", M[i][self.tmax - 1])
            print("nb_matching_B : ", nb_matching_b)

        print("******************print A**************")
        pprint.pprint(A)
        print("******************print B**************")
        pprint.pprint(B)
        print("***************************************")
        print()
        print("Résult DP ")
        print(numpy.matrix(M))

        max_M = M[self.n - 1][self.tmax - 1]
        max_A = sum(len(v) for v in A.values())
        max_B = nb_matching_b

        print("max_M: ", max_M)
        print("max_A: ", max_A)
        print(numpy.matrix(M))
        print("max_B: ", max_B)

        return max(max_A, max_B)

    def intersectionA(self, A, Bp, t, u, v, nb_matching_b):
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
        nb_inter = 0
        bool_interA = False
        B = copy.deepcopy(Bp)
        for i in range(t - gamma + 1, t + gamma):
            if i not in range(len(A)):
                break
            for edge in A[i]:
                if u in edge or v in edge:
                    bool_interA = True
                    if t in range(t - gamma - 1, t - 1) or \
                            (u > edge[0] and v == edge[0]) or \
                            (u == edge[0] and v > edge[0]) or \
                            u == edge[1] or \
                            v == edge[1] or \
                            u == edge[0] or \
                            v == edge[0]:
                        if edge in B[i]:
                            B[i].remove(edge)
                            nb_matching_b -= 1
                        nb_inter += 1

        return bool_interA, nb_inter, nb_matching_b, B

    def intersectionB(self, B, t, u, v):
        """
            Ok
            :param B:
            :param t:
            :param u:
            :param v:
            :return:
        """

        # on vérifie sur t-1 que par ce que ici on travaille avec gamma=2
        if (u, v) in B[t] or (u, v) in B[t - 1]:
            return True
        for i in range(t - gamma + 1, t + gamma):
            if i not in range(len(B)):
                break
            for edge in B[i]:
                if u in edge or v in edge:
                    if t in range(t - gamma - 1, t - 1) or \
                            (u > edge[0] and v == edge[0]) or \
                            (u == edge[0] and v > edge[0]) or \
                            u == edge[1] or v == edge[1] or \
                            u == edge[0] or v == edge[0]:
                        return True
        return False


import collections


def refactorData(file):
    with open(file, 'r') as f:
        n, tmax, d = list(map(int, f.readline().split()))
        x = numpy.zeros((n, tmax)).astype(int)

        j = 0
        r = [collections.defaultdict(list)] * tmax
        for line in f.read().splitlines():
            r[j] = collections.defaultdict(list)
            if line == '':
                continue
            l = list(map(int, line.replace("]", "").split("[")[1].split(",")))
            for i in range(0, n):
                x[i][j] = l[i]
                r[j][l[i]].append(i)
            j += 1
    pprint.pprint(r)
    return n, tmax, d, x, r
