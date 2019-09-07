import os
import time
from collections import defaultdict


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


class MatchingN:
    REVERSE = False

    def __init__(self, gamma, file):
        self.gamma = gamma
        self.file = file

    def estCompatibleG_edges(self, gammaMatching: GammaMach, M: dict) -> bool:
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

    def G_edgesMatching(self, link_stream: dict, gamma: int) -> dict:
        """
        G_edges = {"gamma" : int,
                    "nb_gamma_matching" = int,
                    " elements" : [gammaMatching] }

        :param link_stream:
        :param gamma:
        :return G_edges: l'ensemble de gamma_matchin disponible
        """

        G_edges = {"gamma": gamma, "max_matching": 0, "elements": defaultdict(list)}
        P = link_stream["E"].copy()
        if self.REVERSE:
            P.reverse()

        while len(P) != 0:
            (t, edge) = P.pop(0)
            u = edge.u
            v = edge.v

            if t in G_edges["elements"] and edge in G_edges["elements"][t]:
                continue

            if not self.contient(P, gamma, edge, t):
                continue

            newGammaMach = GammaMach(t, u, v)

            for tE, gammMatchingEList in G_edges["elements"].items():
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

            G_edges["elements"][t].append(newGammaMach)
            G_edges["max_matching"] += 1
        return G_edges

    def gammaMatchingG_edges_avancer(self, GE: dict, gamma: int) -> int:
        M = {"gamma": gamma, "max_matching": 0, "elements": []}
        G_edges = GE.copy()
        for t, gammaMachingList in G_edges["elements"].items():

            while gammaMachingList:
                gammaMaching = gammaMachingList.pop()
                gammaMaching_to_add = gammaMaching
                nb_g_m = G_edges["max_matching"] - gammaMaching.nb_neighbours
                change = False
                gammaMaching_bis = None

                for g_m_neighbour in gammaMaching.neighbours:
                    nb_g_m_neighbour = G_edges["max_matching"] - g_m_neighbour.nb_neighbours
                    if nb_g_m < nb_g_m_neighbour:
                        change = True
                        nb_g_m = nb_g_m_neighbour
                        gammaMaching_to_add = g_m_neighbour
                        gammaMaching_bis = g_m_neighbour

                # alors on doit vérifier les voisins de g_m_neighbour qui est le new gammaMaching_to_add
                if change:
                    for g_m_n_neighbour in gammaMaching_bis.neighbours:
                        if g_m_n_neighbour == gammaMaching:
                            # ajouter le 23 aout, après le lancement des tests
                            continue
                        nb_g_m_n_neighbour = G_edges["max_matching"] - g_m_n_neighbour.nb_neighbours
                        if nb_g_m < nb_g_m_n_neighbour:
                            gammaMaching_to_add = gammaMaching
                            # TODO ajout d'un break
                            break

                # ajout de gammaMathcing
                if not self.estCompatibleG_edges(gammaMaching_to_add, M):
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
                                index_n_g_m_neighbour_in_G_edges = G_edges["elements"][n_g_m_neighbour.t].index(
                                    n_g_m_neighbour)
                                G_edges["elements"][n_g_m_neighbour.t][
                                    index_n_g_m_neighbour_in_G_edges].nb_neighbours -= 1
                                del G_edges["elements"][n_g_m_neighbour.t][index_n_g_m_neighbour_in_G_edges].neighbours[
                                    index_g_m_neighbour_in_n_g_m_neighbour]
                            except:
                                pass

                        # suppression du voisins dans G_edges
                        try:
                            index_g_m_neighbour_in_G_edges_element = G_edges["elements"][g_m_neighbour.t].index(
                                g_m_neighbour)
                            del G_edges["elements"][g_m_neighbour.t][index_g_m_neighbour_in_G_edges_element]
                        except:
                            pass

                    # supprimer le gamma_matchinc dans G_edges
                    try:
                        index_gamma_matching_to_add = G_edges["elements"][gammaMaching_to_add.t].index(
                            gammaMaching_to_add)
                        del G_edges["E"][gammaMaching_to_add.t][index_gamma_matching_to_add]
                    except:
                        pass

                    G_edges["max_matching"] = G_edges["max_matching"] - 1 - gammaMaching_to_add.nb_neighbours
        # pprint.pprint(M["elements"])
        return M["max_matching"]


def main():
    gamma = 2
    path_enron = "../res/enron400/test_enron/"

    for file in os.listdir(path_enron):
        print("\n .............................", file, ".............................")
        g_m = MatchingN(gamma, path_enron + file)

        print("****************** testing link_stream method ******************")
        link_streamList = g_m.linkStreamList()

        G_edges = g_m.G_edgesMatching(link_streamList, gamma)

        print("************************ gamma_matching ************************")
        print("G_edges : ", G_edges["max_matching"])

        start_time = time.time()
        M = g_m.gammaMatchingG_edges_avancer(G_edges, gamma)
        print("Temps d execution gamma_matching : %s secondes ---" % (time.time() - start_time))
        print("algo - max_matching: ", M)


if __name__ == '__main__':
    main()
