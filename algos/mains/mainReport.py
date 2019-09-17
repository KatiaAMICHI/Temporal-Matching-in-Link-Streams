import csv
import os
import time

from algos.mainClass.BBR19 import MatchingBBR19
from algos.mainClass.DC import *
from algos.mainClass.LS import MatchingN
from algos.maxMAtchingGraph import getNbMatchingT


def resultsT_to_csv(algo, resultsT):
    dataTocsv = list(map(lambda x: [x[0], len(x[1]), x[1]], list(resultsT.items())))
    with open(algo + 'Result.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(dataTocsv)


def main():
    path = '../../FilesRapport/'

    # fileResultNB = path + 'ResultRapportNBSTest'
    # fwNB = open(fileResultNB, 'w+')
    # fwNB.write("File & |V| & |T| & |E| & V_living & G_Edges & BBR19 & LS & LSsort & DC\n")
    #
    # fileResultTime = path + 'ResultRapportTimeSTest'
    # fwT = open(fileResultTime, 'w+')
    # fwT.write("File & |V| & |T| & |E| & G_Edges & BBR19 & LS & LSsort & DC\n")

    gamma = 2
    nb_file = 0
    for f1 in os.listdir(path):
        pathF1 = path + f1 + '/'
        print(pathF1)
        if 'B2' in pathF1:
            continue
        if os.path.isdir(pathF1):
            for f2 in os.listdir(pathF1):
                pathF2 = pathF1 + f2 + '/'
                print('pathF2 : ', pathF2)
                if os.path.isdir(pathF2):
                    for file in os.listdir(pathF2):
                        pathFile = pathF2 + file
                        if file.endswith('.linkstream'):
                            print("******************************", gamma, file, "******************************")
                            nb_file += 1

                            # LS
                            start_time = time.time()
                            g_m_n = MatchingN(gamma, pathFile)
                            link_stream = g_m_n.linkStream()
                            G_edges2 = g_m_n.G_edges(link_stream, gamma)
                            nb_gmLS, resultsTLS = g_m_n.gammaMatching(G_edges2, gamma)
                            timeLS = round(time.time() - start_time, 4)

                            file = file.replace('linkstream', 'linkstreamAR')
                            pathFile = pathF2 + file

                            # DC
                            start_time = time.time()
                            # it replaces the .nb_matchingAR file
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
                            nb_gmBBR19, resultsT = g_mV2.greedy_gamma_matching(g_edges)
                            timeBBR19 = round(time.time() - start_time, 4)

                            # LSsort
                            start_time = time.time()
                            g_m_n = MatchingN(gamma, pathFile)
                            link_streamAR = g_m_n.linkStream()
                            g_edges = g_m_n.gamma_edges_sort(gamma, link_streamAR)
                            nb_gmLSsort, resultsT = g_m_n.gammaMatching(g_edges, gamma)
                            timeLSsort = round(time.time() - start_time, 4)

                            # resultsT_to_csv('LSsort', resultsT)

                            print(f1 + file.replace('.linkstreamAR', '') + ' & ' +
                                  str(timeDC) + '\n')

                            print(f1 + file.replace('.linkstreamAR', '') + ' & ' +
                                  str(nb_gmDC) + '\n')


main()
