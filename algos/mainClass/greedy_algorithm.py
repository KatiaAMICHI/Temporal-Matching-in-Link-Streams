from algos.mainClass.commonObjects import Edge


class Matching:
    """
    Greedy algorithm to find a gamma-matching
    """

    def __init__(self, gamma, file):
        self.gamma = gamma
        self.file = file

    def isCompatible(self, edge: Edge, t: int, M: dict) -> bool:
        """
        Check if a gamma-edge is present in gamma-matching M

        :param edge: edge to check if it already present in M
        :param t: instance t we need to check
        :param M: the list of edges that represents the gamma-matching
        :return: true if it not present in M, False else
        """

        if (t, edge) in M["elements"]:
            return False

        for (tM, edgeM) in M["elements"]:
            if edgeM.u == edge.u or edgeM.v == edge.v or \
                    edgeM.u == edge.v or edgeM.v == edge.u:

                t_check = range(tM, tM + self.gamma)

                if t in t_check:
                    return False
        return True

    def contains(self, P: [Edge], gamma: int, edge: Edge, t: int) -> bool:
        """
        Check if edge is gamma-edge in P

        :param P: link stream
        :param gamma: an integer
        :param edge: an Edge
        :param t:
        :return: True if edge is an gamma-edge, False else
        """
        nb_gammma = 1
        for (tP, edgeP) in P:
            t_check = t + 1

            if edgeP.u != edge.u or edgeP.v != edge.v or tP != t_check:
                continue

            nb_gammma += 1
            t += 1
            if nb_gammma == gamma:
                return True

        return False

    def linkStream(self) -> dict:
        """
        Read file ans return a link stream

        :return: link stream; dictionary of number of vertices, a discretized time instant, and list of edges
        """

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
        """
        Finding a gamma-matching

        :param link_stream: a link stream L = (V,T,E)
        :param gamma: an integer
        :return: set of gamma-edge
        """

        M = {"gamma": gamma, "max_matching": 0, "elements": []}
        P = link_stream["E"].copy()

        while len(P) != 0:
            (t, edge) = P.pop(0)
            u = edge.u
            v = edge.v
            if not self.isCompatible(edge, t, M):
                continue
            if not self.contains(P, gamma, edge, t):
                continue
            M["elements"].append((t - gamma + 1, edge))  # ajout du couple (t, uv)
            M["max_matching"] += 1
            change = False
            nb_change = 0
            nb_gamma = 0

            for (i_t, i) in P:
                if change:
                    nb_change += 1

                t_check = t + nb_change + 1

                if i_t == t_check and i.u == u and i.v == v:
                    nb_gamma += 1
                    P.remove((i_t, i))
                    change = True
                if nb_gamma == gamma:
                    break
        return M
