import collections, pprint
from collections import defaultdict
import csv

class GammaMach:
    def __init__(self, t, u, v):
        self.t = t
        self.u = u
        self.v = v
        self.neighbours = set()
        self.nb_neighbours = 0

    def __repr__(self):
        return "GammaMach(t:" + str(self.t) + ", u:" + str(self.u) + ",v: " + str(self.v) + ", nb_neighbours :" + str(self.nb_neighbours) + ")"


class MatchingN:

    def __init__(self, gamma, file):
        self.gamma = gamma
        self.file = file

    def estCompatible(self, gammaMatching: GammaMach, M: dict) -> bool:
        t = gammaMatching.t
        if gammaMatching in M["elements"]:
            return True

        for gammaMatchingM in M["elements"]:

            if gammaMatching.u == gammaMatchingM.u and gammaMatching.v == gammaMatchingM.v and gammaMatching.t == gammaMatchingM.t:
                return True

            tM = gammaMatchingM.t
            if gammaMatching.u == gammaMatchingM.u or gammaMatching.v == gammaMatchingM.v or \
                    gammaMatching.u == gammaMatchingM.v or gammaMatching.v == gammaMatchingM.u:

                t_check = range(tM, tM + self.gamma)

                if t in t_check:
                    return True
        return False

    def contient(self, P: [tuple], gamma: int, u, v, t: int) -> bool:
        nb_gammma = 1
        for (tP, uP, vP) in P:
            t_check = t + 1

            if uP != u or vP != v or tP != t_check:
                continue

            nb_gammma += 1
            t += 1
            if nb_gammma == gamma:
                return True

        return False

    def linkStream(self) -> dict:
        link_stream = {"V": 0, "T": 0, "E": []}
        max_node = -1
        t_max = -1

        with open(self.file) as f:
            for line in f:
                line_split = line.split()
                t = int(line_split[0])
                u = int(line_split[1])
                v = int(line_split[2])

                link_stream["E"].append((t, u, v))  # ajout du tuple (t, u, v)

                if max_node < max(u, v):
                    max_node = max(u, v)

                if t_max < t:
                    t_max = t

                link_stream["V"] = max_node + 1
                link_stream["T"] = t_max + 1

        return link_stream

    def gamma_edgesAR(self, gamma, link_stream):
        P = link_stream["E"].copy()
        result = {"gamma": gamma, "max_matching": 0, "elements": defaultdict(list)}

        last_u = -1
        last_v = -1
        last_t = link_stream["T"]
        gamma_cpt = 0

        for i in range(len(P)):
            (t, u, v) = P[i]

            if u == last_u and v == last_v and t == last_t + 1:
                gamma_cpt += 1
            else:
                gamma_cpt = 0

            if gamma_cpt >= gamma - 1:
                t_starting = t - gamma + 1
                gamma_e = GammaMach(t_starting, u, v)
                # ajout des voisin
                for t_check in range(t_starting - gamma + 1, t_starting + gamma):
                    if t_check < 0:
                        continue
                    idx_g_e = 0
                    for g_e in result['elements'][t_check]:
                        if gamma_e.t == g_e.t and gamma_e.u == g_e.u and gamma_e.v == g_e.v:
                            continue
                        if g_e.u == u or g_e.v == v or g_e.u == v or g_e.v == u:
                            gamma_e.neighbours.add(g_e)
                            gamma_e.nb_neighbours += 1
                            result['elements'][t_check][idx_g_e].neighbours.add(gamma_e)
                            result['elements'][t_check][idx_g_e].nb_neighbours += 1

                        idx_g_e += 1

                result["elements"][t_starting].append(gamma_e)

                result["max_matching"] += 1

            last_u = u
            last_v = v
            last_t = t

        return result

    def G_edges(self, link_stream: dict, gamma: int) -> dict:
        """
        G_edges = {"gamma" : int,
                    "nb_gamma_matching" = int,
                    " elements" : [gammaMatching] }

        :param link_stream:
        :param gamma:
        :return G_edges: l'ensemble de gamma_matching disponible
        """

        G_edges = {"gamma": gamma, "max_matching": 0, "elements": defaultdict(list)}
        P = link_stream["E"].copy()

        while len(P) != 0:
            (t, u, v) = P.pop(0)

            if t in G_edges["elements"] and (u, v) in G_edges["elements"][t]:
                continue

            if not self.contient(P, gamma, u, v, t):
                continue

            newGammaMach = GammaMach(t, u, v)

            for tE in range(t - gamma + 1, t + gamma):
                i = 0
                for gammMatchingE in G_edges["elements"][tE]:

                    if gammMatchingE.u == v or gammMatchingE.v == u or gammMatchingE.u == u or gammMatchingE.v == v:
                        newGammaMach.neighbours.add(gammMatchingE)
                        newGammaMach.nb_neighbours += 1
                        G_edges["elements"][tE][i].neighbours.add(newGammaMach)
                        G_edges["elements"][tE][i].nb_neighbours += 1
                    i += 1
            G_edges["elements"][t].append(newGammaMach)
            G_edges["max_matching"] += 1
        return G_edges

    def gammaMatching(self, GE: dict, gamma: int) -> (int, []):
        M = {"gamma": gamma, "max_matching": 0, "elements": []}
        G_edges = GE.copy()

        resultsT = collections.defaultdict(list)
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
                            continue
                        nb_g_m_n_neighbour = G_edges["max_matching"] - g_m_n_neighbour.nb_neighbours
                        if nb_g_m < nb_g_m_n_neighbour:
                            gammaMaching_to_add = gammaMaching
                            break

                # ajout de gammaMathcing
                if not self.estCompatible(gammaMaching_to_add, M):
                    M["elements"].append(gammaMaching_to_add)
                    resultsT[t].append(gammaMaching_to_add)
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

        return M["max_matching"], resultsT
