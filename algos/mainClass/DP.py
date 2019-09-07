import numpy
import copy
import pprint

gamma = 2


class DpGammaMatching1DORIGINE:
    def __init__(self, n, tmax, d, xInput):
        self.n = n
        self.tmax = tmax
        self.d = d
        self.xInput = xInput

    def gammaMatchig1DSort(self):
        """
            OK
            :param n: nb sommet
            :param d: distance
            :param xInput: toutes les positions pour chaque sommets pour chaque t
            :return:
        """

        M = numpy.zeros((self.n + 1, self.tmax + 1)).astype(int)
        A = {}
        B = {}

        for i in range(self.tmax + 1):
            A[i] = []
            B[i] = []

        x = self.xInput.copy()
        argsort = list(numpy.argsort(x)) + [self.n]
        nb_matching_b = 0

        for i in range(2, self.n + 1):
            M[i][1] = M[i - 1][self.tmax]
            print("i : ", i)
            print("        <<< M[", i, "][", 0, "] : ", M[i][0])
            print("        <<< M[", i, "][", 1, "] : ", M[i][1])

            for j in range(2, self.tmax + 1):
                print("     j : ", j)

                if abs(x[i][argsort[i][j]] - x[i - 1][argsort[i][j]]) <= self.d and abs(
                        x[i][argsort[i][j - 1]] - x[i - 1][argsort[i][j - 1]]) <= self.d:
                    # ok
                    print("**************** A *******************")
                    pprint.pprint(A)
                    print("1 **************** B *******************")
                    pprint.pprint(B)
                    print("**************************************")
                    bool_inter, nb_inter, nb_matching_b, Bp = self.intersectionA(A, B.copy(), j, i, i - 1,
                                                                                 nb_matching_b)
                    if bool_inter:
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
                            if not self.intersectionB(B, j, i, i - 1):
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
                        M[i][j] = max(M[i - 2][j - 2], M[i - 2][j], M[i][j - 2]) + 1
                        A[j].append((i, i - 1))  # ajout de (u,v)
                        if not self.intersectionB(B, j, i, i - 1):
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

            M[i][0] = M[i][self.tmax]
            print("******************print A*********************")
            pprint.pprint(A)
            print("**********************************************")
            print()
            print("Résult DP ")
            # print(numpy.matrix(M))
            print("nb_matching_A :", M[self.n][self.tmax])
            print("nb_matching_B : ", nb_matching_b)

        max_A = M[self.n][self.tmax]
        max_B = nb_matching_b

        print("nb_matching_A :", M[self.n][self.tmax])
        pprint.pprint(A)
        print("nb_matching_B : ", nb_matching_b)
        pprint.pprint(B)

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
        bool_inter = False
        B = copy.deepcopy(Bp)
        for i in range(t - gamma + 1, t + gamma):
            if i not in range(len(A)):
                break
            for edge in A[i]:
                if u in edge or v in edge:
                    bool_inter = True
                    if t in range(t - gamma - 1, t - 1) or (u > edge[0] and v == edge[0]) or (
                            u == edge[0] and v > edge[0]):
                        if edge in B[i]:
                            B[i].remove(edge)
                            nb_matching_b -= 1
                        nb_inter += 1
        return bool_inter, nb_inter, nb_matching_b, B

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
                    if t in range(t - gamma - 1, t - 1) or (u > edge[0] and v == edge[0]) or (
                            u == edge[0] and v > edge[0]):
                        return True
        return False


def refactorData(file):
    with open(file, 'r') as f:
        tmax, n, d = list(map(int, f.readline().split()))
        # x = [[0] * (tmax + 1)] * (n + 1)
        x = [[0] * (tmax)] * (n)
        i = 1
        for line in f.read().splitlines():
            if line == '':
                continue
            # x[i] = [0] + list(map(int, line.replace("]", "").split("[")[1].split(",")))
            x[i] = list(map(int, line.replace("]", "").split("[")[1].split(",")))
            i += 1

    return n, tmax, d, x
