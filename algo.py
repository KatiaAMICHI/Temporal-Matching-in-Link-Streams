from collections import defaultdict
import time
import os


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

    def linkStream(self) -> dict:
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


def main():
    gamma = 2
    path_enron = "./res/test_enron/"

    path_rollernet = "./res/rollernet/test_rollernet/"

    for file in os.listdir(path_rollernet):
        print("\n ...............................................", file,
              "...............................................")
        g_m = Matching(gamma, path_rollernet + file)

        print("****************** testing link_stream method ******************")
        start_time = time.time()
        link_stream = g_m.linkStream()
        print("Temps d execution link_stream : %s secondes ---" % (time.time() - start_time))
        print("L : ( V:", link_stream["V"], ", T:", link_stream["T"], ", E:", len(link_stream["E"]), ")")
        print()

        print("************************ gamma_matching ************************")
        start_time = time.time()
        M = g_m.gammaMatching(link_stream, gamma)
        print("Temps d execution gamma_matching : %s secondes ---" % (time.time() - start_time))
        print("algo - max_matching: ", M["max_matching"])

    print("\nFIN")


if __name__ == '__main__':
    main()
