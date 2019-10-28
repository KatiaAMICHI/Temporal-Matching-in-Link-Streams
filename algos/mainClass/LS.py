import collections
from collections import defaultdict

from algos.mainClass.commonObjects import GammaMach


class MatchingN:
    """
    Aproximation algorithm to find a gamma-matching
    """

    def __init__(self, gamma, file):
        self.gamma = gamma
        self.file = file

    def isCompatible(self, gammaMatching: GammaMach, M: dict) -> bool:
        """
        Check if a gamma-edge is present in gamma-matching M

        :param gammaMatching: a GammaMach to check if it already present in M
        :param M: the list of edges that represents the gamma-matching
        :return: true if gammaMatching is present in M, False else
        """
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

    def contains(self, P: [tuple], gamma: int, u, v, t: int) -> bool:
        """
        Check if (t, u, v) in P

        :param P: a link stream
        :param gamma: an integer
        :param u: a vertice
        :param v: a vertice
        :param t:
        :return: True if (t, u, v) in P, False else
        """
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
        """
        Read file ans return a link stream

        :return: link stream; dictionary of number of vertices, a discretized time instant, and list of edges
        """

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

    def G_edges(self, link_stream: dict, gamma: int) -> dict:
        """
        G_edges = {"gamma" : an integer,
                    "nb_gamma_matching" = number of gamma-edges,
                    " elements" : set of gamma-edge}

        :param link_stream: a Link stream sorting according to t
        :param gamma: an integer
        :return G_edges: set of independent gamma-edge
        """

        G_edges = {"gamma": gamma, "max_matching": 0, "elements": defaultdict(list)}
        P = link_stream["E"].copy()

        while len(P) != 0:
            (t, u, v) = P.pop(0)

            if t in G_edges["elements"] and (u, v) in G_edges["elements"][t]:
                continue

            if not self.contains(P, gamma, u, v, t):
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

    def gamma_edges_sort(self, gamma, link_stream):
        """
        G_edges = {"gamma" : an integer,
                    "nb_gamma_matching" = number of gamma-edges,
                    " elements" : set of gamma-edge}

        :param link_stream: a Link stream sorting according to u and v
        :param gamma: an integer
        :return G_edges: set of dependent gamma-edge
        """

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
                # adding of ajout neighbours
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

    def gammaMatching(self, GE: dict, gamma: int) -> (int, []):
        """
        Finding a gamma-matching

        :param GE: set of dependent gamma-edge
        :param gamma: an integer
        :return: set of gamma-edge
        """
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

                # then we have to check the neighbors of g_m neighbor which is the new gammaMaching_to_add
                if change:
                    for g_m_n_neighbour in gammaMaching_bis.neighbours:
                        if g_m_n_neighbour == gammaMaching:
                            continue
                        nb_g_m_n_neighbour = G_edges["max_matching"] - g_m_n_neighbour.nb_neighbours
                        if nb_g_m < nb_g_m_n_neighbour:
                            gammaMaching_to_add = gammaMaching
                            break

                # adding of gammaMathcing
                if not self.isCompatible(gammaMaching_to_add, M):
                    M["elements"].append(gammaMaching_to_add)
                    resultsT[t].append(gammaMaching_to_add)
                    M["max_matching"] += 1

                    # delete neighbors and decrement the neighbor number of neighbors of their neighbors
                    for g_m_neighbour in gammaMaching_to_add.neighbours:
                        if g_m_neighbour == gammaMaching_to_add:
                            continue

                        # delete this neighbor in their neighbors
                        # for each neighbor find it and delete it and decrement the nb_voisins
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

                        # removing neighbors in G_edges
                        try:
                            index_g_m_neighbour_in_G_edges_element = G_edges["elements"][g_m_neighbour.t].index(
                                g_m_neighbour)
                            del G_edges["elements"][g_m_neighbour.t][index_g_m_neighbour_in_G_edges_element]
                        except:
                            pass

                    # delete gammaMaching_to_add in G_edges
                    try:
                        index_gamma_matching_to_add = G_edges["elements"][gammaMaching_to_add.t].index(
                            gammaMaching_to_add)
                        del G_edges["E"][gammaMaching_to_add.t][index_gamma_matching_to_add]
                    except:
                        pass

                    G_edges["max_matching"] = G_edges["max_matching"] - 1 - gammaMaching_to_add.nb_neighbours

        return M["max_matching"], resultsT
