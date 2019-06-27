from collections import defaultdict
import time, os


class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v
        self.neighbours = []
        self.nb_neighbours = 0

    def __repr__(self):
        return "Edge(u:" + self.u + ", v:" + self.v + ", nb_neighbours:" + str(self.nb_neighbours) + ")"


# TODO laisser ou enlever t
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


# TODO lancer les calcule ce soir
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
        #  print("....... je suis dans estCompatibleE_gamma ......... je suis : ", gammaMatching)
        t = gammaMatching.t
        if gammaMatching in M["elements"]:
            #  print("return True")
            return True

        for gammaMatchingM in M["elements"]:

            if gammaMatching.u == gammaMatchingM.u and gammaMatching.v == gammaMatchingM.v and gammaMatching.t == gammaMatchingM.t:
                print("return True")
                return True

            tM = gammaMatchingM.t
            if gammaMatching.u == gammaMatchingM.u or gammaMatching.v == gammaMatchingM.v or \
                    gammaMatching.u == gammaMatchingM.v or gammaMatching.v == gammaMatchingM.u:

                # print(">>>>>>>>  gammaMatching : ", gammaMatching)
                if self.REVERSE:
                    t_check = range(tM - self.gamma, tM)
                else:
                    t_check = range(tM, tM + self.gamma)

                if t in t_check:
                    #   print("return True")
                    return True
        #  print("return False")
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

    def E_gamma_matching(self, link_stream: dict, gamma: int) -> dict:
        """
        E_gamma = {"gamma" : int,
                    "nb_gamma_matching" = int,
                    " elements" : [gammaMatching] }

        :param link_stream:
        :param gamma:
        :return E_gamma: un dictionnaire où on a une liste de tous les gamma_matchin disponible
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
                        # if gammMatchingE.u == u and gammMatchingE.v == v:
                        if gammMatchingE.u == v or gammMatchingE.v == u or gammMatchingE.u == u or gammMatchingE.v == v:
                            newGammaMach.neighbours.append(gammMatchingE)
                            newGammaMach.nb_neighbours += 1
                            gammMatchingE.neighbours.append(newGammaMach)
                            gammMatchingE.nb_neighbours += 1

            E_gamma["elements"][t].append(newGammaMach)
            E_gamma["max_matching"] += 1

        return E_gamma

    def gamma_matching_with_E_gamma(self, E_gamma: dict, gamma: int) -> dict:
        M = {"gamma": gamma, "max_matching": 0, "elements": []}
        # P_gamma.reverse()

        for t, gammaMachingList in E_gamma["elements"].items():
            # print("t : ", t,
            #    ".........................................................................................")
            while gammaMachingList:
                gammaMaching = gammaMachingList.pop()
                # print("<<<<<<<<<<<<<gammaMaching  pop : ", gammaMaching)
                # print("mes voisins : ", gammaMaching.neighbours)
                gammaMaching_to_add = gammaMaching
                max_nb_g_maching = E_gamma["max_matching"] - gammaMaching.nb_neighbours
                # print("max_nb_g_maching : ", max_nb_g_maching)
                for g_m_neighbour in gammaMaching.neighbours:
                    nb_g_maching = E_gamma["max_matching"] - g_m_neighbour.nb_neighbours
                    # print("nb_g_maching  : ", nb_g_maching)
                    if max_nb_g_maching < nb_g_maching:
                        # print("++++++ je suis : ", g_m_neighbour)
                        gammaMaching_to_add = g_m_neighbour

                if not self.estCompatibleE_gamma(gammaMaching_to_add, M):
                    # print(">>>>>>>>>>>>>>> je vais ajouter : ", gammaMaching_to_add)
                    M["elements"].append(gammaMaching_to_add)
                    M["max_matching"] += 1

                    # il faut supprimer ces voinsins !! et décrémonter le nombre des voinins de ces voisins
                    for g_m_neighbour in gammaMaching_to_add.neighbours:
                        if g_m_neighbour == gammaMaching_to_add:
                            continue
                        # print("********************* je vais supprimer : ", g_m_neighbour)

                        # supprimer le voisins dans ses voisins
                        # pour chaque voisins le truver et le supprimer et décrimenter le nb_voisins
                        for n_g_m_neighbour in g_m_neighbour.neighbours:
                            if n_g_m_neighbour == gammaMaching_to_add:
                                continue
                            # print("$$ je suis le voisin du voisin | n_g_m_neighbour : ", n_g_m_neighbour)

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
                                # print("je pense il a déja été suprimer")

                        # supprission du voisin dans E-gamma
                        try:
                            index_g_m_neighbour_in_E_gamma_element = E_gamma["elements"][g_m_neighbour.t].index(
                                g_m_neighbour)
                            del E_gamma["elements"][g_m_neighbour.t][index_g_m_neighbour_in_E_gamma_element]
                        except:
                            pass
                            # print("???????????????????????")
                    # enfin le suprimer dans la liste des gamma_matchings
                    try:
                        index_gamma_matching_to_add = E_gamma["elements"][gammaMaching_to_add.t].index(
                            gammaMaching_to_add)
                        del E_gamma["E"][gammaMaching_to_add.t][index_gamma_matching_to_add]
                    except:
                        pass
                        # print("???????????????????????")
                    E_gamma["max_matching"] = E_gamma["max_matching"] - 1 - gammaMaching_to_add.nb_neighbours

        return M


def main():
    gamma = 2
    # path = "./res/to_test/"
    path = "./res/test_local/"

    for file in os.listdir(path):
        print("\n ...............................................", file,
              "...............................................")
        g_m = Matching(gamma, path + file)

        print("*********************** testing link_stream method ***********************")
        start_time = time.time()
        link_stream = g_m.linkStreamList()
        print("Temps d execution link_stream : %s secondes ---" % (time.time() - start_time))
        print("L : ( V:", link_stream["V"], ", T:", link_stream["T"], ", E:", len(link_stream["E"]), ")")
        print()

        print("**************************** E_gamma nb_matching ****************************")
        start_time = time.time()
        E_gamma = g_m.E_gamma_matching(link_stream, gamma)
        print("Temps d execution : %s secondes ---" % (time.time() - start_time))
        print("E_gamma nb_matching : ", E_gamma["max_matching"])
        print()

        print("**************************** E_gamma max_matching ****************************")
        start_time = time.time()
        E_gamma_matching = g_m.gamma_matching_with_E_gamma(E_gamma, gamma)
        print("Temps d execution : %s secondes ---" % (time.time() - start_time))
        print("algo + - max_matching : ", E_gamma_matching["max_matching"])


if __name__ == '__main__':
    main()
