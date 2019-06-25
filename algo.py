class Edge:
    def __init__(self, t, u, v):
        self.t = int(t)
        self.u = u
        self.v = v

    def __repr__(self):
        return "Edge(t:" + str(self.t) + ", u:" + self.u + ", v:" + self.v + ")"


class Matching:
    REVERSE = True

    def __init__(self, gamma, file):
        self.gamma = gamma
        self.file = file

    def estCompatible(self, edge: Edge, M: dict) -> bool:
        if edge in M["element"]:
            return False

        for edgeM in M["element"]:
            if edgeM.u == edge.u or edgeM.v == edge.v or \
                    edgeM.u == edge.v or edgeM.v == edge.u:

                if self.REVERSE:
                    t_check = range(edgeM.t - self.gamma, edgeM.t)
                else:
                    t_check = range(edgeM.t, edgeM.t + self.gamma)

                if edge.t in t_check:
                    return False
        return True

    def contient(self, P: [Edge], gamma: int, edge: Edge) -> bool:
        t = edge.t
        nb_gammma = 1
        for edgeP in P:
            if self.REVERSE:
                t_check = t - 1
            else:
                t_check = t + 1

            if edgeP.u != edge.u or edgeP.v != edge.v or edgeP.t != t_check:
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
                t = line_split[0]
                u = line_split[1]
                v = line_split[2]

                link_stream["E"].append(Edge(t=t, u=u, v=v))

                if max_node < max(int(u), int(v)):
                    max_node = max(int(u), int(v))

                if t_max < int(t):
                    t_max = int(t)

                link_stream["V"] = max_node + 1
                link_stream["T"] = t_max
        return link_stream

    def gammaMatching(self, link_stream: dict, gamma: int) -> dict:
        M = {"gamma": gamma, "max_matching": 0, "element": []}
        P = link_stream["E"].copy()
        P.reverse()

        while len(P) != 0:
            edge = P.pop(0)
            t = edge.t
            u = edge.u
            v = edge.v
            if not self.estCompatible(edge, M):
                continue
            if not self.contient(P, gamma, edge):
                continue
            M["element"].append(edge)
            changer = False
            nb_change = 0
            nb_gamma = 0
            for i in P:
                if changer:
                    nb_change += 1

                if self.REVERSE:
                    t_check = t - nb_change - 1
                else:
                    t_check = t + nb_change + 1

                if i.t == t_check and i.u == u and i.v == v:
                    nb_gamma += 1
                    P.remove(i)
                    changer = True
                if nb_gamma == gamma:
                    break
        M["max_matching"] = len(M["element"])
        return M

    def ensemble_gamma_matching(self, link_stream: dict, gamma: int) -> dict:
        M = {"gamma": gamma, "max_matching": 0, "element": []}
        P = link_stream["E"].copy()
        P.reverse()

        while len(P) != 0:
            edge = P.pop(0)
            t = edge.t
            u = edge.u
            v = edge.v
            if edge in M["element"]:
                continue
            if not self.contient(P, gamma, edge):
                continue
            M["element"].append(edge)
            changer = False
            nb_change = 0
            nb_gamma = 0
            for i in P:
                if changer:
                    nb_change += 1

                if self.REVERSE:
                    t_check = t - nb_change - 1
                else:
                    t_check = t + nb_change + 1

                if i.t == t_check and i.u == u and i.v == v:
                    nb_gamma += 1
                    P.remove(i)
                    changer = True
                if nb_gamma == gamma:
                    break
        M["max_matching"] = len(M["element"])
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
    g_m2 = Matching(gamma, file_test3)
    link_stream2 = g_m2.linkStream()
    M2 = g_m2.gammaMatching(link_stream2, gamma)
    print("file_test3 : ", M2["max_matching"])
    M = g_m2.ensemble_gamma_matching(link_stream2, gamma)
    print("nb ensemble_gamma_matching: ", M["max_matching"])
    print("ensemble_gamma_matching: ", M["element"])
