import random


class MatchingBBR19:

    def linkStream(self, file) -> dict:
        link_stream = {"V": 0, "T": 0, "E": []}
        max_node = -1
        t_max = -1

        with open(file) as f:
            for line in f:
                line_split = line.split()
                t = int(line_split[0])
                u = line_split[1]
                v = line_split[2]

                link_stream["E"].append((int(t), u, v))  # ajout du tuple (t, uv)

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
            (t, u, v) = P[i]

            if u == last_u and v == last_v and t == last_t + 1:
                gamma_cpt += 1
            else:
                gamma_cpt = 0

            if gamma_cpt >= gamma - 1:
                result.append((t - gamma + 1, u, v))
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
