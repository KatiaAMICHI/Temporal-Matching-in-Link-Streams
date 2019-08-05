gamma = 2


def max_t_matching(list_pos_matching):
    max_matching = (0, [])
    idx_max_matching = -1
    i = 0
    for x in list_pos_matching:
        if max_matching[0] < x[0]:
            max_matching = x
            idx_max_matching = i
        i += 1
    return max_matching, idx_max_matching


def update_list_pos_matching(list_pos_matching, max_matching, idx_max_matching):
    for edge in max_matching:
        for i in range(idx_max_matching - gamma + 1, idx_max_matching + gamma - 1):
            for elem in list_pos_matching[i]:
                for edge_p in elem[1]:
                    if edge_p[0] == edge[0] or edge_p[1] == edge[0] or edge_p[0] == edge[1] or edge_p[1] == edge[1]:
                        elem[1].remove(edge_p)
                        elem[0] -= 1
    list_pos_matching.remove(max_matching)
    return list_pos_matching


def nb_gamma_matching_decomposition(list_pos_matching, nb_matching, M):
    # TODO ajout un point d'arret !!!!!
    max_matching, idx_max_matching = max_t_matching(list_pos_matching)
    M.append(max_matching[1])  # ajout des gamma_matching
    nb_matching += max_matching[0]
    update_list_pos_matching(list_pos_matching, max_matching, idx_max_matching)
    nb_gamma_matching_decomposition(list_pos_matching[0:idx_max_matching], nb_matching, M)
    nb_gamma_matching_decomposition(list_pos_matching[idx_max_matching::])


if __name__ == '__main__':
    pass