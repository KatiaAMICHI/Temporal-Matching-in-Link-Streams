from collections import defaultdict
import time


class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v
        self.neighbours = []
        self.nb_neighbours = 0

    def __repr__(self):
        return "Edge(u:" + self.u + ", v:" + self.v + ", nb_neighbours:" + str(self.nb_neighbours) + ")"


# TODO laisser ou enlever t
class GammaMach:
    def __init__(self, t, u, v, nb_neighbours=None):
        self.t = t
        self.u = u
        self.v = v
        self.nb_neighbours = nb_neighbours

    def __repr__(self):
        return "GammaMach(t:" + str(self.t) + ", u:" + str(self.u) + ",v: " + self.v + ", nb_neighbours :" + str(
            self.nb_neighbours) + ")"


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

    def linkStreamList(self) -> dict:
        link_stream = {"V": 0, "T": 0, "E": []}
        max_node = -1
        t_max = -1

        with open(self.file) as f:
            for line in f:
                line_split = line.split()
                t = int(line_split[0])
                u = line_split[1]
                v = line_split[2]

                link_stream["E"].append((int(t), Edge(u=u, v=v)))  # ajout du tuple (t, uv)

                if max_node < max(int(u), int(v)):
                    max_node = max(int(u), int(v))

                if t_max < int(t):
                    t_max = int(t)

                link_stream["V"] = max_node + 1
                link_stream["T"] = t_max + 1

        return link_stream

    def gammaMatching(self, link_stream: dict, gamma: int) -> dict:
        M = {"gamma": gamma, "max_matching": 0, "elements": []}
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
            M["elements"].append((t, edge))  # ajout du couple (t, uv)
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

    def linkStreamDict(self) -> dict:
        link_stream = {"V": 0, "T": 0, "E": defaultdict(list)}
        max_node = -1
        t_max = -1

        with open(self.file) as f:
            for line in f:
                line_split = line.split()
                t = int(line_split[0])
                u = line_split[1]
                v = line_split[2]

                new_edge = Edge(u=u, v=v)
                if len(link_stream["E"][t]) > 0:
                    for edge in link_stream["E"][t]:
                        if edge.u == u and edge.v == v:
                            continue

                        if edge.u == v or edge.v == u:
                            edge.neighbours.append(new_edge)
                            edge.nb_neighbours += 1
                            new_edge.neighbours.append(edge)
                            new_edge.nb_neighbours += 1

                link_stream["E"][t].append(new_edge)  # ajout du tuple (t, uv)

                if max_node < max(int(u), int(v)):
                    max_node = max(int(u), int(v))

                if t_max < int(t):
                    t_max = int(t)

                link_stream["V"] = max_node + 1
                link_stream["T"] = t_max + 1

        return link_stream

    def E_gamma_matching(self, link_stream: dict, gamma: int) -> dict:
        """
        E_gamma = {"gamma" : int,
                    "nb_gamma_matching" = int,
                    " elements" : [gammaMatching] }

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

            E_gamma["elements"][t].append(GammaMach(t, u, v))

            # ajout des voisin

            E_gamma["max_matching"] += 1

        return E_gamma

    def gamma_matching_with_E_gamma(self, E_gamma: dict, gamma: int) -> dict:
        M = {"gamma": gamma, "max_matching": 0, "elements": []}
        P_gamma = E_gamma["elements"].copy()  # contient la liste des gamma_matching possible
        # P_gamma.reverse()

        while len(P_gamma) != 0:
            pass
        return M


if __name__ == '__main__':
    gamma = 3
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

    g_m = Matching(gamma, file_test3)

    print("*********************** testing link_stream method ***********************")
    start_time = time.time()
    link_stream = g_m.linkStreamDict()
    print("Temps d execution link_stream : %s secondes ---" % (time.time() - start_time))
    print("L : ( V:", link_stream["V"], ", T:", link_stream["T"], ", E:", len(link_stream["E"]), ")")
    print("elements E :", link_stream["E"])
    print()

    print("***************************** gamma_matching *****************************")
    # M = g_m.gammaMatching(link_stream, gamma)
    # print("gammaMatching: ", M["max_matching"])

    print("**************************** E_gamma_matching ****************************")
    start_time = time.time()
    E_gamma = g_m.E_gamma_matching(link_stream, gamma)
    print("Temps d execution : %s secondes ---\n" % (time.time() - start_time))
    print("E_gamma", E_gamma["max_matching"], ", elements : ", E_gamma["elements"])
