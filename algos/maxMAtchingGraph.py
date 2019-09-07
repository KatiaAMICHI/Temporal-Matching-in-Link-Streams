import networkx as nx
import networkx.algorithms.matching


def linkStream(file):
    link_stream = {"V": 0, "T": 0, "E": []}
    max_node = -1
    t_max = -1

    with open(file) as f:
        for line in f:
            t, u, v = list(map(int, line.split()))

            link_stream["E"].append((t, u, v))  # ajout du tuple (t, uv)

            if max_node < max(int(u), int(v)):
                max_node = max(int(u), int(v))

            if t_max < int(t):
                t_max = int(t)

            link_stream["V"] = max_node + 1
            link_stream["T"] = t_max + 1

    return link_stream


def getVerticesLive(file):
    link_stream = {"V": 0, "T": 0, "E": []}
    max_node = -1
    t_max = -1

    with open(file) as f:
        for line in f:
            t, u, v = list(map(int, line.split()))

            link_stream["E"].append((t, u, v))  # ajout du tuple (t, uv)

            if max_node < max(int(u), int(v)):
                max_node = max(int(u), int(v))

            if t_max < int(t):
                t_max = int(t)

            link_stream["V"] = max_node + 1
            link_stream["T"] = t_max + 1

    return link_stream


def gamma_edges(gamma, link_stream):
    P = link_stream["E"].copy()

    last_u = -1
    last_v = -1
    last_t = link_stream["T"]
    gamma_cpt = 0

    result = []
    for i in range(len(P)):
        (t, u, v) = P[i]

        if u == last_u and v == last_v and t == last_t + 1:
            gamma_cpt += 1
        else:
            gamma_cpt = 0

        if gamma_cpt >= gamma - 1:
            result.append((t - gamma + 1, u, v))
        last_u = u
        last_v = v
        last_t = t

    return result


def getNbMatchingT(gamma, pathFile):
    result = []
    if not pathFile.endswith('.linkstreamAR'):
        return result

    # print("********", fileIn, "***********")
    last_t = 0

    G = nx.Graph()

    link_stream = linkStream(pathFile)

    g_edges = gamma_edges(gamma, link_stream)
    g_edges = sorted(g_edges, key=lambda tup: tup[0])

    for line in g_edges:
        t, u, v = line

        if last_t != t:
            n = len(networkx.maximal_matching(G))
            a = networkx.maximal_matching(G)
            edges = list(map(lambda x: (0, x[0], x[1]), a))
            G = nx.Graph()
            last_t = t
            result.append(str(n) + ' ' + str(edges))

        G.add_edge(u, v)

    n = len(networkx.maximal_matching(G))
    a = networkx.maximal_matching(G)
    edges = list(map(lambda x: (0, x[0], x[1]), a))
    result.append(str(n) + ' ' + str(edges))

    return result
