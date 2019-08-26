from collections import defaultdict


class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v
        self.neighbours = []
        self.nb_neighbours = 0

    def __repr__(self):
        return "Edge(u:" + self.u + ", v:" + self.v + ", nb_neighbours:" + str(self.nb_neighbours) + ")"


class GammaMach:
    def __init__(self, t, u, v):
        self.t = t
        self.u = u
        self.v = v
        self.neighbours = []
        self.nb_neighbours = 0

    def __repr__(self):
        return "GammaMach(t:" + str(self.t) + ", u:" + str(self.u) + ",v: " + self.v + ", nb_neighbours :" + str(
            self.nb_neighbours) + ")"


class MatchingN:
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

    def contientL_sort(self, E: dict, gamma: int, edge: Edge, t: int) -> bool:
        nb_gammma = 1
        for tP, edgeP_list in E.items():
            if tP == t:
                continue
            if self.REVERSE:
                t_check = t - 1
            else:
                t_check = t + 1

            if tP != t_check:
                continue

            for edgeP in edgeP_list:
                if edgeP.u != edge.u or edgeP.v != edge.v:
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

    def G_edgesMatching(self, link_stream: dict, gamma: int) -> dict:
        """
        G_edges = {"gamma" : int,
                    "nb_gamma_matching" = int,
                    " elements" : [gammaMatching] }

        :param link_stream:
        :param gamma:
        :return G_edges: l'ensemble de gamma_matchin disponible
        """

        G_edges = {"gamma": gamma, "max_matching": 0, "elements": defaultdict(list)}
        P = link_stream["E"].copy()
        if self.REVERSE:
            P.reverse()

        while len(P) != 0:
            (t, edge) = P.pop(0)
            u = edge.u
            v = edge.v

            if t in G_edges["elements"] and edge in G_edges["elements"][t]:
                continue

            if not self.contient(P, gamma, edge, t):
                continue

            newGammaMach = GammaMach(t, u, v)

            for tE, gammMatchingEList in G_edges["elements"].items():
                for gammMatchingE in gammMatchingEList:
                    if self.REVERSE:
                        t_check = range(tE - self.gamma, tE)
                    else:
                        t_check = range(tE, tE + self.gamma)

                    if t in t_check:
                        if gammMatchingE.u == v or gammMatchingE.v == u or gammMatchingE.u == u or gammMatchingE.v == v:
                            newGammaMach.neighbours.append(gammMatchingE)
                            newGammaMach.nb_neighbours += 1
                            gammMatchingE.neighbours.append(newGammaMach)
                            gammMatchingE.nb_neighbours += 1

            G_edges["elements"][t].append(newGammaMach)
            G_edges["max_matching"] += 1
        return G_edges

    def gammaMatching_L_sort(self, link_stream: dict, gamma: int) -> dict:
        M = {"gamma": gamma, "max_matching": 0, "elements": []}

        for t in link_stream['E']:
            link_stream['E'][t].sort(key=lambda x: x.nb_neighbours, reverse=False)

        for t, P in link_stream['E'].items():
            for edge in P:
                u = edge.u
                v = edge.v
                if not self.estCompatible(edge, t, M):
                    continue
                if not self.contientL_sort(link_stream['E'], gamma, edge, t):
                    continue
                M["elements"].append((t, edge))  # ajout du couple (t, uv)
                M["max_matching"] += 1
                nb_gamma = 0

                t_check = range(t + 1, t + gamma)
                for t_gamma in t_check:
                    for e in link_stream['E'][t_gamma]:
                        if e.u == u and e.v == v:
                            nb_gamma += 1
                            link_stream['E'][t_gamma].remove(e)
                            # passer au suivant
                            break

        return M