from collections import defaultdict
import time, os
import pprint


class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v
        self.neighbours = []
        self.nb_neighbours = 0

    def __repr__(self):
        return "Edge(u:" + self.u + ", v:" + self.v + ", nb_neighbours:" + str(self.nb_neighbours) + ")"


# TODO laisser ou enlever t ?
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

    def estCompatibleE_gamma(self, gammaMatching: GammaMach, M: dict) -> bool:
        t = gammaMatching.t
        if gammaMatching in M["elements"]:
            return True

        for gammaMatchingM in M["elements"]:

            if gammaMatching.u == gammaMatchingM.u and gammaMatching.v == gammaMatchingM.v and gammaMatching.t == gammaMatchingM.t:
                print("return True")
                return True

            tM = gammaMatchingM.t
            if gammaMatching.u == gammaMatchingM.u or gammaMatching.v == gammaMatchingM.v or \
                    gammaMatching.u == gammaMatchingM.v or gammaMatching.v == gammaMatchingM.u:

                if self.REVERSE:
                    t_check = range(tM - self.gamma, tM)
                else:
                    t_check = range(tM, tM + self.gamma)

                if t in t_check:
                    return True
        return False

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

    def contient__L_sort(self, E: dict, gamma: int, edge: Edge, t: int) -> bool:
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

    def E_gammaMatching(self, link_stream: dict, gamma: int) -> dict:
        """
        E_gamma = {"gamma" : int,
                    "nb_gamma_matching" = int,
                    " elements" : [gammaMatching] }

        :param link_stream:
        :param gamma:
        :return E_gamma: l'ensemble de gamma_matchin disponible
        """

        E_gamma = {"gamma": gamma, "max_matching": 0, "elements": defaultdict(list)}
        P = link_stream["E"].copy()
        if self.REVERSE:
            P.reverse()

        while len(P) != 0:
            (t, edge) = P.pop(0)
            u = edge.u
            v = edge.v

            if t in E_gamma["elements"] and edge in E_gamma["elements"][t]:
                continue

            if not self.contient(P, gamma, edge, t):
                continue

            newGammaMach = GammaMach(t, u, v)

            # trouver et ajouter les voisins
            for tE, gammMatchingEList in E_gamma["elements"].items():
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

            E_gamma["elements"][t].append(newGammaMach)
            E_gamma["max_matching"] += 1

        return E_gamma

    def gammaMatching_E_gamma(self, E_gamma: dict, gamma: int) -> dict:
        M = {"gamma": gamma, "max_matching": 0, "elements": []}

        for t, gammaMachingList in E_gamma["elements"].items():
            while gammaMachingList:
                gammaMaching = gammaMachingList.pop()
                gammaMaching_to_add = gammaMaching
                nb_g_m = E_gamma["max_matching"] - gammaMaching.nb_neighbours

                for g_m_neighbour in gammaMaching.neighbours:
                    nb_g_m_neighbour = E_gamma["max_matching"] - g_m_neighbour.nb_neighbours
                    if nb_g_m < nb_g_m_neighbour:
                        gammaMaching_to_add = g_m_neighbour

                # ajout de gammaMathcing
                if not self.estCompatibleE_gamma(gammaMaching_to_add, M):
                    M["elements"].append(gammaMaching_to_add)
                    M["max_matching"] += 1

                    # supprimer ses voisins et décrémenter le nb_neighbour des voisins de leurs voisins
                    for g_m_neighbour in gammaMaching_to_add.neighbours:
                        if g_m_neighbour == gammaMaching_to_add:
                            continue

                        # supprimer ce voisin dans leurs voisins
                        # pour chaque voisins le truver et le supprimer et décrimenter le nb_voisins
                        for n_g_m_neighbour in g_m_neighbour.neighbours:
                            if n_g_m_neighbour == gammaMaching_to_add:
                                continue
                            try:
                                index_g_m_neighbour_in_n_g_m_neighbour = n_g_m_neighbour.neighbours.index(g_m_neighbour)
                                index_n_g_m_neighbour_in_E_gamma = E_gamma["elements"][n_g_m_neighbour.t].index(
                                    n_g_m_neighbour)
                                E_gamma["elements"][n_g_m_neighbour.t][
                                    index_n_g_m_neighbour_in_E_gamma].nb_neighbours -= 1
                                del E_gamma["elements"][n_g_m_neighbour.t][index_n_g_m_neighbour_in_E_gamma].neighbours[
                                    index_g_m_neighbour_in_n_g_m_neighbour]
                            except:
                                pass

                        # suppression du voisins dans E_gamma
                        try:
                            index_g_m_neighbour_in_E_gamma_element = E_gamma["elements"][g_m_neighbour.t].index(
                                g_m_neighbour)
                            del E_gamma["elements"][g_m_neighbour.t][index_g_m_neighbour_in_E_gamma_element]
                        except:
                            pass

                    # suppremer le gamma_matchinc dans E_gamma
                    try:
                        index_gamma_matching_to_add = E_gamma["elements"][gammaMaching_to_add.t].index(
                            gammaMaching_to_add)
                        del E_gamma["E"][gammaMaching_to_add.t][index_gamma_matching_to_add]
                    except:
                        pass

                    E_gamma["max_matching"] = E_gamma["max_matching"] - 1 - gammaMaching_to_add.nb_neighbours

        return M

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
                if not self.contient__L_sort(link_stream['E'], gamma, edge, t):
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

    def mu_max_matching(self, L: dict, E_gamma: dict, gamma: int):
        M = {"gamma": gamma, "max_matching": 0, "elements": []}

        for t, P in L['E'].items():
            while P:
                element_max_y_matching = []
                max_y_matching = -1
                nb_y_matching = len(P)

                for edge in P:
                    # d'abor trouver tt les gamma_arete possible dans l'interal [t, t+gamma-&]
                    u = edge.u
                    v = edge.v
                    if not self.estCompatible(edge, t, M):
                        continue
                    if not self.contient__L_sort(L['E'], gamma, edge, t):
                        continue

                # ajout du résultat finale le le y_matchin maximum
                M["elements"].extend(max_y_matching)
                M["max_matching"] += 1
                nb_gamma = 0

                t_check = range(t + 1, t + gamma)
                for t_gamma in t_check:
                    for e in L['E'][t_gamma]:
                        if e.u == u and e.v == v:
                            nb_gamma += 1
                            L['E'][t_gamma].remove(e)
                            break


def main():
    gamma = 3
    path = "./res/enron/test_enron/"
    path_rollernet = "./res/rollernet/test_rollernet/"

    for file in os.listdir(path_rollernet):
        print("\n ...............................................", file,
              "...............................................")
        g_m = Matching(gamma, path_rollernet + file)

        print("*********************** testing link_stream method ***********************")
        start_time = time.time()
        link_stream = g_m.linkStreamList()
        print("Temps d execution link_stream : %s secondes ---" % (time.time() - start_time))
        print("L : ( V:", link_stream["V"], ", T:", link_stream["T"], ", E:", len(link_stream["E"]), ")")
        print()

        print("**************************** E_gamma nb_matching ****************************")
        start_time = time.time()
        E_gamma = g_m.E_gammaMatching(link_stream, gamma)
        print("Temps d execution : %s secondes ---" % (time.time() - start_time))
        print("E_gamma nb_matching : ", E_gamma["max_matching"])
        print()

        print("**************************** E_gamma max_matching ****************************")
        start_time = time.time()
        gamma_matching_with_E_gamma = g_m.gammaMatching_E_gamma(E_gamma, gamma)
        print("Temps d execution : %s secondes ---" % (time.time() - start_time))
        print("algo + - max_matching : ", gamma_matching_with_E_gamma["max_matching"])


def test_gammaMatching_L_sort():
    file_enron_clean = r"./res/enronClean"
    file_enron_clean_rename = r"./res/enronCleanRename"
    file_enron_clean_rename_3days = r"./res/enronCleanRename3days"
    file_enron_clean_rename_6days = r"./res/enronCleanRename6days"
    file_enronCleanDeco1h = r"./res/enronCleanDeco1h"
    file_enronCleanDeco3h = r"./res/enronCleanDeco3h"
    file_enronCleanDeco1day = r"./res/enronCleanDeco1day"

    file_test2 = r"./res/test_local/file_test2.txt"
    file_test3 = r"./res/test_local/file_tes3.txt"
    file_test6 = r"./res/test_local/file_test6.txt"
    file_test4 = r"./res/test_local/file_test4.txt"
    file_test5 = r"./res/test_local/file_test5.txt"

    gamma = 2
    path_enron = "./res/enron/test_enron/"
    path_rollernet = "./res/rollernet/test_rollernet/"

    for file in os.listdir(path_rollernet):
        print("\n ...............................................", file,
              "...............................................")
        g_m = Matching(gamma, path_rollernet + file)

        link_stream = g_m.linkStreamDict()

        gammaMatching_L_sort = g_m.gammaMatching_L_sort(link_stream, gamma)

        print(gammaMatching_L_sort['max_matching'])

    print("\nFIN")


def test_method():
    gamma = 3

    file_test2 = r"./res/test_local/file_test2.txt"
    file_test3 = r"./res/test_local/file_tes3.txt"
    file_test6 = r"./res/test_local/file_test6.txt"
    file_test4 = r"./res/test_local/file_test4.txt"
    file_test5 = r"./res/test_local/file_test5.txt"

    g_m = Matching(gamma, file_test5)

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


if __name__ == '__main__':
    #   test_gammaMatching_L_sort()
    main()
