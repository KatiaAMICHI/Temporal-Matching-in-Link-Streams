import ast
import os
import pprint
from contextlib import suppress

gamma = 2


class DecomposeGreedy:
    def __init__(self, path="./testbed/tests/"):
        self.path = path

    def max_t_matching(self, list_pos_matching: [[]]) -> (list, int):
        max_matching = (0, [])
        idx_max_matching = -1
        i = 0
        for x in list_pos_matching:
            if max_matching[0] < x[0]:
                max_matching = x
                idx_max_matching = i
            i += 1
        return max_matching, idx_max_matching

    def update_list_pos_matching(self, list_pos_matching: [[]], max_matching: (int, list), idx_max_matching: int) -> [
        []]:
        for edge in max_matching[1]:
            begin = idx_max_matching + 1 if idx_max_matching == 0 else idx_max_matching - gamma + 1
            end = idx_max_matching + 1 if idx_max_matching + 1 == len(list_pos_matching) else idx_max_matching + gamma

            if begin == len(list_pos_matching):
                break

            for i in range(begin, end):
                for edge_p in list_pos_matching[i][1]:
                    if edge_p[0] == edge[0] or edge_p[1] == edge[0] or edge_p[0] == edge[1] or edge_p[1] == edge[1]:
                        list_pos_matching[i][1].remove(edge_p)
                        list_pos_matching[i][0] -= 1

        if max_matching in list_pos_matching:
            list_pos_matching.remove(max_matching)
        if [0, []] in list_pos_matching:
            # with suppress(ValueError, AttributeError):
            list_pos_matching.remove([0, []])

        return list_pos_matching

    def nb_gamma_matching_decomposition(self, list_pos_matching: list, nb_matching: int, M) -> (list, int):
        if len(list_pos_matching) < 1:
            return nb_matching, M

        max_matching, idx_max_matching = self.max_t_matching(list_pos_matching)

        M = M + max_matching[1]  # ajout des gamma_matching
        nb_matching += max_matching[0]

        self.update_list_pos_matching(list_pos_matching, max_matching, idx_max_matching)

        self.nb_gamma_matching_decomposition(list_pos_matching[0:idx_max_matching], nb_matching, M)
        nb_matching2, M = self.nb_gamma_matching_decomposition(list_pos_matching[idx_max_matching::], nb_matching, M)
        return nb_matching2, M

    def get_list_pos_matching(self, file: str) -> list:
        result = []
        t = 0
        with open(file, 'r') as f:
            n, tmax, d = list(map(int, f.readline().split()))
            for line in f.readlines():
                data = line.split('[')
                max_matching, elements = int(data[0]), list(ast.literal_eval(data[1].replace(']', '')))
                if isinstance(elements[0], int):
                    # on a qu'une seule arrete dans notre list
                    result.append([max_matching, [(elements[0], elements[1])]])
                else:
                    result.append([max_matching, elements])
                t += 1

        return result

    def main(self):
        for file in os.listdir(self.path):
            if file.endswith('.nb_matching'):
                print("****************", file, "****************")
                list_pos_matching = self.get_list_pos_matching(self.path + file)
                pprint.pprint(list_pos_matching)
                nb_matching, M = self.nb_gamma_matching_decomposition(list_pos_matching, nb_matching=0, M=[])
                print(file, " : ", nb_matching, M)

    def linkStreamToPosition(self):
        file_output = r"./testbed/tests/linkstreamToPosition.position"

        for file in os.listdir(self.path):
            file_output = self.path + file.replace(".linkstream", "linkstreamToPosition.position")
            if file.endswith('.linkstream'):
                with open(self.path + file, 'r') as f:
                    with open(file_output, "+w") as f_outPut:
                        n, tmax, d = list(map(int, f.readline().split()))
                        f_outPut.write(str(n) + " " + str(tmax) + " " + str(d) + "\n")
                        last_t = -1
                        max_pos = -2
                        pos = [-2] * int(n)

                        for line in f.readlines():
                            t, u, v = list(map(int, line.split()))

                            if t == 0:
                                pos[u] = 0
                                pos[v] = 0

                            elif pos[u] != -2 and pos[v] != -2 and last_t + 1 != t and abs(pos[u] - pos[v]) <= d:
                                pass
                            else:
                                if last_t + 1 == t:
                                    # chagement de t
                                    pos = list(map(lambda x: x if x != -2 else max_pos + gamma, pos))
                                    # print(">>> ", str(t - 1) + " " + str(pos))
                                    f_outPut.write(str(t - 1) + " " + str(pos) + "\n")
                                    pos = [-2] * int(n)
                                    max_pos = -2
                                    voisins = {}

                                # on est tjr avec le mm t
                                if pos[u] == -2:
                                    # print("     je suis la : ", max_pos)
                                    pos[u] = max_pos + 2
                                    pos[v] = pos[u]
                                    if u not in voisins:
                                        voisins[u] = []
                                    voisins[u].append(v)
                                else:
                                    # print("     ici aussi ")
                                    if pos[v] == -2:
                                        pos[u] += 1
                                        pos[v] = pos[u] + 1
                                        if u not in voisins:
                                            voisins[u] = []
                                        voisins[u].append(v)

                                    else:
                                        nb = 0
                                        sup = False
                                        while abs(pos[u] - pos[v]) > d:
                                            if pos[u] > pos[v]:
                                                sup = True
                                                pos[u] -= 1
                                            else:
                                                pos[u] += 1

                                            nb += 1
                                        if u in voisins:
                                            for v in voisins[u]:
                                                if abs(pos[u] - pos[v]) > d:
                                                    if sup:
                                                        pos[v] -= nb
                                                    else:
                                                        pos[v] += nb

                                # print("a la fin : ", str(t - 1) + " " + str(pos))

                            if max_pos < max(pos[u], pos[v]):
                                max_pos = max(pos[u], pos[v])

                            last_t = t

                        # chagement de t
                        pos = list(map(lambda x: x if x != -2 else max_pos + gamma, pos))
                        # print(">>> ", str(t - 1) + " " + str(pos))
                        f_outPut.write(str(t) + " " + str(pos) + "\n")


if __name__ == '__main__':
    dg = DecomposeGreedy()
    # dg.linkStreamToPosition()
    dg.main()
