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

    def E_gammaMatching_mu(self, link_stream: dict, gamma: int) -> dict:
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

            # trouver et ajouter les voisins juste sur un t
            for tE, gammMatchingEList in E_gamma["elements"].items():
                for gammMatchingE in gammMatchingEList:
                    if gammMatchingE.t == t and (
                            gammMatchingE.u == v or gammMatchingE.v == u or gammMatchingE.u == u or gammMatchingE.v == v):
                        newGammaMach.neighbours.append(gammMatchingE)
                        newGammaMach.nb_neighbours += 1
                        gammMatchingE.neighbours.append(newGammaMach)
                        gammMatchingE.nb_neighbours += 1

            E_gamma["elements"][t].append(newGammaMach)
            E_gamma["max_matching"] += 1

        return E_gamma

    def gammaMatchingE_gamma(self, E_gamma: dict, gamma: int) -> dict:
        M = {"gamma": gamma, "max_matching": 0, "elements": []}
        E_gamma_copy = E_gamma.copy()
        for t, gammaMachingList in E_gamma_copy["elements"].items():
            while gammaMachingList:
                gammaMaching = gammaMachingList.pop()
                gammaMaching_to_add = gammaMaching
                nb_g_m = E_gamma_copy["max_matching"] - gammaMaching.nb_neighbours

                for g_m_neighbour in gammaMaching.neighbours:
                    nb_g_m_neighbour = E_gamma_copy["max_matching"] - g_m_neighbour.nb_neighbours
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
                                index_n_g_m_neighbour_in_E_gamma = E_gamma_copy["elements"][n_g_m_neighbour.t].index(
                                    n_g_m_neighbour)
                                E_gamma_copy["elements"][n_g_m_neighbour.t][
                                    index_n_g_m_neighbour_in_E_gamma].nb_neighbours -= 1
                                del E_gamma_copy["elements"][n_g_m_neighbour.t][
                                    index_n_g_m_neighbour_in_E_gamma].neighbours[
                                    index_g_m_neighbour_in_n_g_m_neighbour]
                            except:
                                pass

                        # suppression du voisins dans E_gamma_copy
                        try:
                            index_g_m_neighbour_in_E_gamma_element = E_gamma_copy["elements"][g_m_neighbour.t].index(
                                g_m_neighbour)
                            del E_gamma_copy["elements"][g_m_neighbour.t][index_g_m_neighbour_in_E_gamma_element]
                        except:
                            pass

                    # suppremer le gamma_matchinc dans E_gamma
                    try:
                        index_gamma_matching_to_add = E_gamma_copy["elements"][gammaMaching_to_add.t].index(
                            gammaMaching_to_add)
                        del E_gamma_copy["E"][gammaMaching_to_add.t][index_gamma_matching_to_add]
                    except:
                        pass

                    E_gamma_copy["max_matching"] = E_gamma_copy["max_matching"] - 1 - gammaMaching_to_add.nb_neighbours

        return M

    def gammaMatchingE_gamma_avancer(self, E_gamma: dict, gamma: int) -> dict:
        M = {"gamma": gamma, "max_matching": 0, "elements": []}

        for t, gammaMachingList in E_gamma["elements"].items():
            # print("***************************** t = ", t, "*****************************")
            while gammaMachingList:
                gammaMaching = gammaMachingList.pop()
                # print(">>>> : ", gammaMaching)
                gammaMaching_to_add = gammaMaching
                nb_g_m = E_gamma["max_matching"] - gammaMaching.nb_neighbours
                change = False
                gammaMaching_bis = None
                for g_m_neighbour in gammaMaching.neighbours:
                    nb_g_m_neighbour = E_gamma["max_matching"] - g_m_neighbour.nb_neighbours
                    if nb_g_m < nb_g_m_neighbour:
                        change = True
                        nb_g_m = nb_g_m_neighbour
                        gammaMaching_to_add = g_m_neighbour
                        gammaMaching_bis = g_m_neighbour

                # alors on doit vérifier les voisins de g_m_neighbour qui est le new gammaMaching_to_add
                if change:
                    for g_m_n_neighbour in gammaMaching_bis.neighbours:
                        nb_g_m_n_neighbour = E_gamma["max_matching"] - g_m_n_neighbour.nb_neighbours
                        if nb_g_m < nb_g_m_n_neighbour:
                            gammaMaching_to_add = gammaMaching

                # ajout de gammaMathcing
                if not self.estCompatibleE_gamma(gammaMaching_to_add, M):
                    # print("je vais ajouter :", gammaMaching_to_add)
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


def main():
    gamma = 3
    path_enron = "./res/enron/test_enron/"
    path_rollernet = "./res/rollernet/test_rollernet/"

    for file in os.listdir(path_rollernet):
        print("\n ...............................................", file,
              "...............................................")
        g_m = Matching(gamma, path_rollernet + file)

        print("*********************** testing link_stream method ***********************")
        link_stream_list = g_m.linkStreamList()
        link_stream_dict = g_m.linkStreamDict()

        print("L : ( V:", link_stream_list["V"], ", T:", link_stream_list["T"], ", E:", len(link_stream_list["E"]), ")")

        print("**************************** E_gamma nb_matching ****************************")
        link_streamList = g_m.linkStreamList()
        E_gamma = g_m.E_gammaMatching(link_streamList, gamma)

        print("**************************** E_gamma max_matching ****************************")
        start_time = time.time()
        gamma_matching_with_E_gamma = g_m.gammaMatchingE_gamma(E_gamma, gamma)
        print("gamma_matching_with_E_gamma - Temps d execution : %s secondes ---" % (time.time() - start_time))
        gammaMatching_L_sort = g_m.gammaMatching_L_sort(link_stream_dict, gamma)
        gamma_matching_with_E_gamma_avancer = g_m.gammaMatchingE_gamma_avancer(E_gamma, gamma)

        M = g_m.gammaMatchingE_gamma_avancer(E_gamma, gamma)
        print("E_gamma : ", E_gamma["max_matching"])
        print("algo - max_matching: ", M["max_matching"])

        print("E_avancer : ", gamma_matching_with_E_gamma_avancer["max_matching"])
        print(E_gamma["max_matching"], " & 0 & 0 & ", gamma_matching_with_E_gamma["max_matching"], " & ",
              gammaMatching_L_sort['max_matching'], " & ", gamma_matching_with_E_gamma_avancer["max_matching"])


def test_method():
    gamma = 3

    file_test2 = r"./res/test_local/file_test2.txt"
    file_test3 = r"./res/test_local/file_tes3.txt"
    file_test6 = r"./res/test_local/file_test6.txt"
    file_test4 = r"./res/test_local/file_test4.txt"
    file_test5 = r"./res/test_local/file_test5.txt"
    file_test_mu = r"./res/test_local/test_mu.txt"

    file_test_tab = r"./res/test_local/test_tab.txt"
    file_test_bis = r"./res/test_local/test_bis.txt"

    rollernetClean30min = r"./res/rollernet/test_rollernet/rollernetClean15mins"
    rollernetClean30minTO = r"./res/rollernet/test_rollernet/rollernetClean30minsT0"
    path_rollernet = "./res/rollernet/test_rollernet/"

    for file in os.listdir(path_rollernet):
        print("\n ...............................................", file,
              "...............................................")
        g_m = Matching(gamma, path_rollernet + file)

        print("****************** testing link_stream method ******************")
        link_streamList = g_m.linkStreamList()

        E_gamma = g_m.E_gammaMatching(link_streamList, gamma)

        print("************************ gamma_matching ************************")
        print("E_gamma : ", E_gamma["max_matching"])

        start_time = time.time()
        M = g_m.gammaMatchingE_gamma_avancer(E_gamma, gamma)
        print("Temps d execution gamma_matching : %s secondes ---" % (time.time() - start_time))
        print("algo - max_matching: ", M["max_matching"])


def result():
    gamma = 2
    path = "./res/enron/test_enron/"
    path_rollernet = "./res/rollernet/test_rollernet/"

    for file in os.listdir(path_rollernet):
        print("\n ...............................................", file,
              "...............................................")
        g_m = Matching(gamma, path_rollernet + file)

        print("*********************** testing link_stream method ***********************")
        link_stream = g_m.linkStreamList()

        print("**************************** E_gamma nb_matching ****************************")
        E_gamma = g_m.E_gammaMatching(link_stream, gamma)

        print("**************************** E_gamma max_matching ****************************")
        start_time = time.time()
        gamma_matching_with_E_gamma_avancer = g_m.gammaMatchingE_gamma_avancer(E_gamma, gamma)
        print("Temps d execution : %s secondes ---" % (time.time() - start_time))
        print("gammaMatchingE_gamma- max_matching : ", gamma_matching_with_E_gamma_avancer["max_matching"])

    for file in os.listdir(path):
        print("\n ...............................................", file,
              "...............................................")
        g_m = Matching(gamma, path + file)

        print("*********************** testing link_stream method ***********************")
        link_stream = g_m.linkStreamList()

        print("**************************** E_gamma nb_matching ****************************")
        E_gamma = g_m.E_gammaMatching(link_stream, gamma)

        print("**************************** E_gamma max_matching ****************************")
        start_time = time.time()
        gamma_matching_with_E_gamma = g_m.gammaMatchingE_gamma(E_gamma, gamma)
        # gamma_matching_with_E_gamma_avancer = g_m.gammaMatchingE_gamma_avancer(E_gamma, gamma)
        print("Temps d execution : %s secondes ---" % (time.time() - start_time))
        print("gammaMatchingE_gamma- max_matching : ", gamma_matching_with_E_gamma["max_matching"])
        # print("gammaMatchingE_gamma_avancer - max_matching : ", gamma_matching_with_E_gamma_avancer["max_matching"])


def test_file():
    gamma = 3
    file = "./res/test_local/fileTest.txt"

    print("\n ...............................................", file,
          "...............................................")
    g_m = Matching(gamma, file)

    print("*********************** testing link_stream method ***********************")
    link_stream = g_m.linkStreamList()

    print("**************************** E_gamma nb_matching ****************************")
    E_gamma = g_m.E_gammaMatching(link_stream, gamma)

    print("**************************** E_gamma max_matching ****************************")
    start_time = time.time()
    gamma_matching_with_E_gamma_avancer = g_m.gammaMatchingE_gamma_avancer(E_gamma, gamma)
    print("Temps d execution : %s secondes ---" % (time.time() - start_time))
    print("gammaMatchingE_gamma- max_matching : ", gamma_matching_with_E_gamma_avancer["max_matching"])
    pprint.pprint(gamma_matching_with_E_gamma_avancer["elements"])


if __name__ == '__main__':
    # main()
    # test_method()
    test_file()
