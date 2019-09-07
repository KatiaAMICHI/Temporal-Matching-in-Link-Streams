import ast

gamma = 2


class DecomposeGreedy:

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
                    if edge_p[1] == edge[1] or edge_p[2] == edge[1] or edge_p[1] == edge[2] or edge_p[2] == edge[2]:
                        list_pos_matching[i][1].remove(edge_p)
                        list_pos_matching[i][0] -= 1

        if max_matching in list_pos_matching:
            list_pos_matching.remove(max_matching)
        if [0, []] in list_pos_matching:
            list_pos_matching.remove([0, []])

        return list_pos_matching

    def nb_gamma_matching_decomposition(self, list_pos_matching: list, nb_matching: int, M) -> (list, int):
        if len(list_pos_matching) < 1:
            return nb_matching, M

        max_matching, idx_max_matching = self.max_t_matching(list_pos_matching)
        M = M + max_matching[1]  # ajout des gamma_matching
        nb_matching += max_matching[0]

        list_pos_matching = self.update_list_pos_matching(list_pos_matching, max_matching, idx_max_matching)

        nb_matching, M = self.nb_gamma_matching_decomposition(list_pos_matching[0:idx_max_matching], nb_matching, M)
        nb_matching, M = self.nb_gamma_matching_decomposition(list_pos_matching[idx_max_matching::], nb_matching, M)

        return nb_matching, M

    def get_list_pos_matching(self, file: str) -> list:
        result = []
        t = 0
        with open(file, 'r') as f:
            for line in f.readlines():
                data = line.split('[')
                if int(data[0]) == 0:
                    continue
                max_matching, elements = int(data[0]), list(ast.literal_eval(data[1].replace(']', '')))
                if isinstance(elements[0], int):
                    # on a qu'une seule arrete dans notre list
                    result.append([max_matching, [(elements[0], elements[1], elements[2])]])
                else:
                    result.append([max_matching, elements])
                t += 1

        return result

    def get_list_pos_matching_from_list(self, listData) -> list:
        result = []
        t = 0
        for line in listData:
            data = line.split('[')
            if int(data[0]) == 0:
                continue
            max_matching, elements = int(data[0]), list(ast.literal_eval(data[1].replace(']', '')))
            if isinstance(elements[0], int):
                # on a qu'une seule arrete dans notre list
                result.append([max_matching, [(elements[0], elements[1], elements[2])]])
            else:
                result.append([max_matching, elements])
            t += 1

        return result