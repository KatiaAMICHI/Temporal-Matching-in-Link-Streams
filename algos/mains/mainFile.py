import csv
import time

from algos.mainClass.BBR19 import MatchingBBR19
from algos.mainClass.DC import DecomposeGreedy
from algos.mainClass.LS import MatchingN
from algos.mainClass.commonObjects import SommetsVivant
from algos.maxMAtchingGraph import getNbMatchingT


def dataToCsv(file, result):
    with open(file, "w+") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(result.items())


def main():
    gamma = 2
    pathFile = '../../res/gen_B2/test1029/test.linkstream'
    if pathFile.endswith('.linkstream'):
        print("******************************", gamma, "******************************")
        V_living = SommetsVivant(pathFile)

        # LS
        start_time = time.time()
        g_m_n = MatchingN(gamma, pathFile)
        link_stream = g_m_n.linkStream()
        G_edges2 = g_m_n.G_edges(link_stream, gamma)
        nb_gmLS, resultsTLS = g_m_n.gammaMatching(G_edges2, gamma)
        timeLS = round(time.time() - start_time, 4)
        pathFile = pathFile.replace('linkstream', 'linkstreamAR')

        # DC
        start_time = time.time()
        # ça replace ce qu'il y a dans le fichier .nb_matchingAR
        results = getNbMatchingT(gamma, pathFile)
        dc = DecomposeGreedy(gamma)
        list_pos_matching = dc.get_list_pos_matching_from_list(results)
        nb_gmDC, M = dc.nb_gamma_matching_decomposition(list_pos_matching, nb_matching=0, M=[])
        timeDC = round(time.time() - start_time, 4)

        # BBR19
        start_time = time.time()
        g_mV2 = MatchingBBR19(gamma, pathFile)
        link_stream = g_mV2.linkStream()
        g_edges = g_mV2.gamma_edges(link_stream)
        nb_gmBBR19, resultsTBBR19 = g_mV2.greedy_gamma_matching(g_edges)
        timeBBR19 = round(time.time() - start_time, 4)

        # LSsort
        start_time = time.time()
        g_m_n = MatchingN(gamma, pathFile)
        link_streamAR = g_m_n.linkStream()
        g_edges = g_m_n.gamma_edges_sort(gamma, link_streamAR)
        nb_g_edges = g_edges['max_matching']
        nb_gmLSsort, resultsTLSsort = g_m_n.gammaMatching(g_edges, gamma)
        timeLSsort = round(time.time() - start_time, 4)

        print({'File': pathFile, 'Gamma': gamma,
               'V': link_stream['V'],
               'T': link_stream['T'],
               'E': len(link_stream['E']),
               'G_Edges': nb_g_edges,
               'BBR19': timeBBR19,
               'LS': timeLS,
               'LSsort': timeLSsort,
               'DC': timeDC})

        print({'File': pathFile, 'Gamma': gamma,
               'V': link_stream['V'],
               'T': link_stream['T'],
               'E': len(link_stream['E']),
               'V_living': V_living,
               'G_Edges': g_edges['max_matching'],
               'BBR19': nb_gmBBR19,
               'LS': nb_gmLS,
               'LSsort': nb_gmLSsort,
               'DC': nb_gmDC})


main()
