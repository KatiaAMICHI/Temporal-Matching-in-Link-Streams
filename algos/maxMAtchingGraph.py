import networkx as nx
import os
from collections import defaultdict
import csv
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
            edges = list(map(lambda x: (last_t, x[0], x[1]), a))
            G = nx.Graph()
            last_t = t
            result.append(str(n) + ' ' + str(edges))

        G.add_edge(u, v)

    n = len(networkx.maximal_matching(G))
    a = networkx.maximal_matching(G)
    edges = list(map(lambda x: (t, x[0], x[1]), a))
    result.append(str(n) + ' ' + str(edges))

    return result


def generateNbMAtchingAR():
    pathE = '../res/gen_enron/'
    pathB2 = '../res/gen_B2/'
    pathB1 = '../res/gen_B1/'
    pathR = '../res/gen_rollernet/'

    path = pathB2

    nbFile = 0
    for f in os.listdir(path):
        if os.path.isfile(path + f):
            continue
        for fileIn in os.listdir(path + f):
            if fileIn.endswith('.linkstream'):
                nbFile += 1
                print("********", f, fileIn, "***********")
                last_t = 0

                # fileOutPut = path + fileIn.replace('linkstream', 'nb_matching')
                fileOutPut = path + f + '/' + fileIn.replace('linkstream', 'nb_matchingNetworkx')

                fw = open(fileOutPut, '+w')
                G = nx.Graph()

                # link_stream = linkStream(path + fileIn)
                link_stream = linkStream(path + f + '/' + fileIn)

                for line in link_stream['E']:
                    t, u, v = line

                    if last_t != t:
                        n = len(networkx.maximal_matching(G))
                        a = networkx.maximal_matching(G)
                        edges = list(map(lambda x: (last_t, x[0], x[1]), a))
                        G = nx.Graph()
                        last_t = t
                        fw.writelines(str(n) + ' ' + str(edges) + '\n')

                    G.add_edge(u, v)

                n = len(networkx.maximal_matching(G))
                a = networkx.maximal_matching(G)
                edges = list(map(lambda x: (t, x[0], x[1]), a))
                fw.writelines(str(n) + ' ' + str(edges) + '\n')
                print("Fin d'écriture dans ", fileOutPut)


def generateNbMAtchingARG_edges():
    pathE = '../res/gen_enron/decoData/'
    pathR = '../res/gen_rollernet/decoData/'
    pathB1 = '../res/gen_B1/'
    pathB2 = '../res/gen_B2/'

    path = pathB2
    nbFile = 0
    gamma = 2
    for f in os.listdir(path):
        for fileIn in os.listdir(path + f):
            if fileIn.endswith('.linkstreamAR'):
                nbFile += 1
                print("********", fileIn, "***********")
                last_t = 0

                # fileOutPut = path + fileIn.replace('linkstream', 'nb_matching')
                fileOutPut = path + f + '/' + fileIn.replace('linkstream', 'nb_matching')

                fw = open(fileOutPut, '+w')
                G = nx.Graph()

                # link_stream = linkStream(path + fileIn)
                link_stream = linkStream(path + f + '/' + fileIn)

                g_edges = gamma_edges(gamma, link_stream)
                g_edges = sorted(g_edges, key=lambda tup: tup[0])

                for line in g_edges:
                    t, u, v = line

                    if last_t != t:
                        n = len(networkx.maximal_matching(G))
                        a = networkx.maximal_matching(G)
                        edges = list(map(lambda x: (t, x[0], x[1]), a))
                        G = nx.Graph()
                        last_t = t
                        fw.writelines(str(n) + ' ' + str(edges) + '\n')

                    G.add_edge(u, v)
                n = len(networkx.maximal_matching(G))
                a = networkx.maximal_matching(G)
                edges = list(map(lambda x: (t, x[0], x[1]), a))
                fw.writelines(str(n) + ' ' + str(edges) + '\n')
                print("Fin d'écriture dans ", fileOutPut)


def generateMaxGammaMatchingAllfiles():
    path = '../res/'
    for f in os.listdir(path):
        if not os.path.isdir(path + '/' + f):
            continue
        results = defaultdict(lambda: defaultdict(int))

        for fileIn in os.listdir(path + f):
            if not os.path.isdir(path + f + '/' + fileIn):
                continue
            for file in os.listdir(path + f + '/' + fileIn):
                if file.endswith('.nb_matchingAR'):
                    print(" ********************* ", file, '*********************')
                    fr = open(path + f + '/' + fileIn + '/' + file, 'r')
                    t = 0
                    for line in fr.readlines():
                        results[t]['sum'] += int(line.split(' ')[0])
                        results[t]['nb'] += 1
                        t += 1
        a = list(map(lambda x: (x[0], x[1]['sum'] / x[1]['nb']), results.items()))

        fileOUT = path + '/' + f + '/MaxGammaMatchingG2'
        with open(fileOUT, "w+") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(a)

# generateNbMAtchingAR()
# generateMaxGammaMatchingAllfiles()
