import ast


class DecomposeGreedy:
    def __init__(self, gamma):
        self.gamma = gamma

    def get_list_pos_matching(self, file: str) -> list:
        """
        read file and save the data in list

        :param file: file data
        :return: list with the data read from the file
        """
        result = []
        t = 0
        with open(file, 'r') as f:
            for line in f.readlines():
                data = line.split('[')
                if int(data[0]) == 0:
                    continue
                max_matching, elements = int(data[0]), list(ast.literal_eval(data[1].replace(']', '')))
                if isinstance(elements[0], int):
                    # we have only one edge in our list
                    result.append([max_matching, [(elements[0], elements[1], elements[2])]])
                else:
                    result.append([max_matching, elements])
                t += 1

        return result

    def get_list_pos_matching_from_list(self, listData) -> list:
        """
        save data from list

        :param listData:
        :return:
        """
        result = []
        t = 0
        for line in listData:
            data = line.split('[')
            if int(data[0]) == 0:
                continue
            max_matching, elements = int(data[0]), list(ast.literal_eval(data[1].replace(']', '')))
            if isinstance(elements[0], int):
                # we have only one edge in our list
                result.append([max_matching, [(elements[0], elements[1], elements[2])]])
            else:
                result.append([max_matching, elements])
            t += 1

        return result

    def max_t_matching(self, list_pos_matching: [[]]) -> (list, int):
        """
        To find the index that contains the maximum of gamma-matching

        :param list_pos_matching: list for each t, the number the list of gamma-edges
        :return: the number of gamma-edges fiond, the index that was fond
        """
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
        """
        update the list_pos_matching by deleting the elements in max_matching

        :param list_pos_matching: list that contains for each t, the number the list of gamma-edges
        :param max_matching: the line which contains the maximum matching
        :param idx_max_matching: index of the maximum matching
        :return: the list where we removed the list of gamma-edges present in max_matching
        """

        for edge in max_matching[1]:
            begin = idx_max_matching - self.gamma + 1
            end = idx_max_matching + self.gamma

            for i in range(max(0, begin), min(end, len(list_pos_matching))):
                if i == idx_max_matching:
                    continue

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
        """
        find a gamma-matching

        :param list_pos_matching: list that contains for each t, the number the list of gamma-edges
        :param nb_matching: the size of M (gamma-matching)
        :param M: gamma-matching
        :return:
        """
        if len(list_pos_matching) < 1:
            return nb_matching, M

        max_matching, idx_max_matching = self.max_t_matching(list_pos_matching)

        M = M + max_matching[1]
        nb_matching += max_matching[0]

        list_pos_matching = self.update_list_pos_matching(list_pos_matching, max_matching, idx_max_matching)

        nb_matching, M = self.nb_gamma_matching_decomposition(list_pos_matching[0:idx_max_matching], nb_matching, M)
        nb_matching, M = self.nb_gamma_matching_decomposition(list_pos_matching[idx_max_matching::], nb_matching, M)

        return nb_matching, M
