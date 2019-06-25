from collections import defaultdict
import time
import numpy as np
import pandas as pd

class Edge:
    def __init__(self, u, v, nb_neighbours=0):
        self.u = u
        self.v = v
        self.nb_neighbours = nb_neighbours

    def __repr__(self):
        return "Edge(u:" + self.u + ", v:" + self.v + ", nb_neighbours:" + str(self.nb_neighbours) + ")"


class GammaMach:
    def __init__(self, u, v, nb_neighbours=None):
        self.u = u
        self.v = v
        self.nb_neighbours = nb_neighbours

    def __repr__(self):
        return "Node(u:" + str(self.u) + ",v: " + self.v + ", nb_neighbours :" + self.nb_neighbours + ")"


# TODO lancer les calcule ce soir
class Matching:
    REVERSE = False

    def __init__(self, gamma, file):
        self.gamma = gamma
        self.file = file

    def estCompatible(self, edge: Edge, t: int, M: dict) -> bool:
        if (t, edge) in M["elements"]:
            return False

        for (tM, edgeM) in M["elements"]:
            if edgeM.u == edge.u or edgeM.v == edge.v or \
                    edgeM.u == edge.v or edgeM.v == edge.u:

                if self.REVERSE:
                    t_check = range(tM - self.gamma, tM)
                else:
                    t_check = range(tM, tM + self.gamma)

                if t in t_check:
                    return False
        return True

    def contient(self, P: [Edge], gamma: int, edge: Edge, t: int) -> bool:
        nb_gammma = 1
        for (tP, edgeP) in P:
            if self.REVERSE:
                t_check = t - 1
            else:
                t_check = t + 1

            if edgeP.u != edge.u or edgeP.v != edge.v or tP != t_check:
                continue

            nb_gammma += 1
            if self.REVERSE:
                t -= 1
            else:
                t += 1
            if nb_gammma == gamma:
                return True

        return False

    def linkStream(self) -> dict:
        link_stream = {"V": 0, "T": 0, "E": np.array([])}
        max_node = -1
        t_max = -1

        with open(self.file) as f:
            for line in f:
                line_split = line.split()
                t = int(line_split[0])
                u = line_split[1]
                v = line_split[2]

                np.append(link_stream["E"], [(int(t), Edge(u=u, v=v))])  # ajout du tuple (t, uv)
                print("len de E : ", len(link_stream["E"]))
                if max_node < max(int(u), int(v)):
                    max_node = max(int(u), int(v))

                if t_max < int(t):
                    t_max = int(t)

                link_stream["V"] = max_node + 1
                link_stream["T"] = t_max + 1

        return link_stream

    def gammaMatching(self, link_stream: dict, gamma: int) -> dict:
        M = {"gamma": gamma, "max_matching": 0, "elements": np.array([])}
        P = link_stream["E"].copy()
        del link_stream

        if self.REVERSE:
            P.reverse()

        while len(P) != 0:
            (t, edge) = P.pop(0)
            u = edge.u
            v = edge.v
            if not self.estCompatible(edge, t, M):
                continue
            if not self.contient(P, gamma, edge, t):
                continue
            np.append(M["elements"], [(t, edge)])  # ajout du couple (t, uv)
            M["max_matching"] += 1
            change = False
            nb_change = 0
            nb_gamma = 0

            for (i_t, i) in P:
                if change:
                    nb_change += 1

                if self.REVERSE:
                    t_check = t - nb_change - 1
                else:
                    t_check = t + nb_change + 1

                if i_t == t_check and i.u == u and i.v == v:
                    nb_gamma += 1
                    P.remove((i_t, i))
                    change = True
                if nb_gamma == gamma:
                    break
        return M

    def E_gamma_matching(self, link_stream: dict, gamma: int) -> dict:
        """
        E_gamma = {"gamma" : int,
                    "nb_gamma_matching" = int,
                    " elements" :


        :param link_stream:
        :param gamma:
        :return E_gamma: un dictionnaire où on a une liste de tous les gamma_matchin disponible
        """
        E_gamma = {"gamma": gamma, "max_matching": 0, "elements": defaultdict(list)}
        P = link_stream["E"].copy()
        if self.REVERSE:
            P.reverse()

        while len(P) != 0:
            (t, edge) = P.pop(0)
            u = edge.u
            v = edge.v

            if t in E_gamma["elements"] and edge in E_gamma["elements"][t]:
                continue

            if not self.contient(P, gamma, edge, t):
                continue

            np.append(E_gamma["elements"][t], [GammaMach(u, v)])
            E_gamma["max_matching"] += 1

        return E_gamma

    def gamma_matching_with_E_gamma(self, E_gamma: dict, gamma: int) -> dict:
        M = {"gamma": gamma, "max_matching": 0, "elements": np.array([])}
        P_gamma = E_gamma["elements"].copy()  # contient la liste des gamma_matching possible
        # P_gamma.reverse()

        while len(P_gamma) != 0:
            pass
        return M


if __name__ == '__main__':
    gamma = 2
    file_enron_clean = r"./res/enronClean"
    file_enron_clean_rename = r"./res/enronCleanRename"
    file_enron_clean_rename_3days = r"./res/enronCleanRename3days"
    file_enron_clean_rename_6days = r"./res/enronCleanRename6days"
    file_enronCleanDeco1h = r"./res/enronCleanDeco1h"
    file_enronCleanDeco3h = r"./res/enronCleanDeco3h"
    file_enronCleanDeco1day = r"./res/enronCleanDeco1day"

    file_test = r"./res/renameData.txt"
    file_test2 = r"./res/file_test2.txt"
    file_test3 = r"./res/file_tes3.txt"

    file_bis = r"./res/file_test2.txt"
    g_m2 = Matching(gamma, file_enronCleanDeco1h)
    link_stream = g_m2.linkStream()

    start_time = time.time()
    M2 = g_m2.gammaMatching(link_stream, gamma)
    print("Temps d execution : %s secondes --- \n" % (time.time() - start_time))

    print("V:", link_stream["V"], ", T:", link_stream["T"], ", E:", len(link_stream["E"]))
    # print("file_test3 : ", M2["max_matching"])

    # M = g_m2.E_gamma_matching(link_stream, gamma)
    # print("nb ensemble_gamma_matching: ", M["max_matching"])
    # print("ensemble_gamma_matching: ", M["elements"])

    pd.array(['a', 'b'], dtype=str)