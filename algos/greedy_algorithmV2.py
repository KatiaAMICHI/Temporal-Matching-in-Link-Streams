from collections import defaultdict
import time
import os, pprint
import random


class Edge:
    def __init__(self, u, v):
        self.u = int(u)
        self.v = int(v)
        self.neighbours = []
        self.nb_neighbours = 0

    def __repr__(self):
        return "Edge(u:" + str(self.u) + ", v:" + str(self.v) + ", nb_neighbours:" + str(self.nb_neighbours) + ")"


class MatchingV2:
    REVERSE = False

    def __init__(self, gamma, file):
        self.gamma = gamma
        self.file = file

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

    def gamma_edges(self, link_stream: dict, gamma: int) -> []:
        P = link_stream["E"].copy()

        last_u = -1
        last_v = -1
        last_t = link_stream["T"]
        gamma_cpt = 0

        result = []
        for i in range(len(P)):
            (t, edge) = P[i]
            u = edge.u
            v = edge.v

            if u == last_u and v == last_v and t == last_t + 1:
                gamma_cpt += 1
            else:
                gamma_cpt = 0

            if gamma_cpt >= gamma - 1:
                result.append((t - gamma + 1, Edge(u, v)))
            last_u = u
            last_v = v
            last_t = t

        return result

    def greedy_gamma_matching(self, L, gamma):
        result = []
        interdi = []
        P = L.copy()
        random.shuffle(P)

        while len(P):
            (t, edge) = P.pop(0)
            result.append((t, edge))
            u = edge.u
            v = edge.v
            i = 0

            while i < len(P):
                (t_p, edge_p) = P[i]
                u_p = edge_p.u
                v_p = edge_p.v
                if (u_p == u or v_p == v or u_p == v or v_p == u) and (t_p in range(t - gamma + 1, t + gamma)):
                    P.pop(i)
                    i -= 1
                    interdi.append((t_p, edge_p))
                i += 1

        return result

    def gamma_edges_best(self, link_stream: dict, gamma: int) -> []:
        """
        g_edges = {"gamma" : int,
                    "nb_gamma_matchingV2" = int,
                    " elements" : [gammaMatchingV2] }

        :param link_stream:
        :param gamma:
        :return g_edges: l'ensemble de gamma_matchin disponible
        """

        P = link_stream["E"].copy()

        last_u = -1
        last_v = -1
        last_t = link_stream["T"]
        gamma_cpt = 0

        result = []
        for i in range(len(P)):
            (t, edge) = P[i]
            u = edge.u
            v = edge.v

            if u == last_u and v == last_v and t == last_t + 1:
                gamma_cpt += 1
            else:
                gamma_cpt = 0

            if gamma_cpt >= gamma - 1:
                result.append([t - gamma + 1, u, v, 0])
            last_u = u
            last_v = v
            last_t = t

        return result

    def greedy_gamma_matching_best(self, L, gamma):
        result = []
        P = L.copy()
        for i in range(len(P)):
            t = P[i][0]
            u = P[i][1]
            v = P[i][2]

            for j in range(len(P)):
                t_p = P[j][0]
                u_p = P[j][1]
                v_p = P[j][2]

                if (u_p == u or v_p == v or u_p == v or v_p == u) and (t_p in range(t - gamma + 1, t + gamma)):
                    P[i][3] += 1
            P[i][3] -= 1
        sorted(P, key=lambda x: x[3])

        while len(P):
            elem = P.pop(0)
            t = elem[0]
            u = elem[1]
            v = elem[2]
            result.append(elem)
            i = 0

            while i < len(P):
                t_p = P[i][0]
                u_p = P[i][1]
                v_p = P[i][2]

                if (u_p == u or v_p == v or u_p == v or v_p == u) and (t_p in range(t, t + gamma)):
                    P.pop(i)
                    i -= 1
                i += 1

        return result


def main():
    gamma = 3
    path_rollernet = "../res/rollernet/test_rollernet/rollernetClean15mins_sort.linkstream"
    file = "/home/katia/Bureau/file_sort"

    g_m = MatchingV2(gamma, path_rollernet)
    link_stream = g_m.linkStream()
    print("L : ( V:", link_stream["V"], ", T:", link_stream["T"], ", E:", len(link_stream["E"]), ")")

    g_edges = g_m.gamma_edges(link_stream, gamma)
    print("g_edges : ", len(g_edges))
    min_M = len(link_stream["E"])
    max_M = -1

    M = g_m.greedy_gamma_matching(g_edges, gamma)

    tmp_M_max = M
    tmp_M_min = M
    for i in range(10):
        M = g_m.greedy_gamma_matching(g_edges, gamma)
        if min_M > len(M):
            tmp_M_min = M
            min_M = len(M)
        if max_M < len(M):
            tmp_M_max = M
            max_M = len(M)

    print("max : ", max_M, "   min : ", min_M)


if __name__ == '__main__':
    main()
