import time
import os
from algos.mainClass.BBR19 import MatchingBBR19
from algos.mainClass.DEC import *
from algos.mainClass.LS import MatchingN
from algos.mainClass.TrucCommain import SommetsVivant
from algos.mains.mainLSTest import gamma_edges_neighbours
from algos.maxMAtchingGraph import getNbMatchingT
from algos.LSTest import MatchingNV2


def main():
    path = '../../FilesRapport/'

    fileResultNB = path + 'ResultRapportNB'
    fwNB = open(fileResultNB, 'w+')
    fwNB.write("File & |V| & |T| & |E| & V_living & G_Edges & BBR19 & LS & LSAR & DEC\n")

    fileResultTime = path + 'ResultRapportTime'
    fwT = open(fileResultTime, 'w+')
    fwT.write("File & |V| & |T| & |E| & G_Edges & BBR19 & LS & LSAR & DEC\n")

    gamma = 2
    nb_file = 0
    for f1 in os.listdir(path):
        pathF1 = path + f1 + '/'
        if os.path.isdir(pathF1):
            for f2 in os.listdir(pathF1):
                pathF2 = pathF1 + f2 + '/'

                if os.path.isdir(pathF2):
                    for file in os.listdir(pathF2):
                        pathFile = pathF2 + file
                        if nb_file > 0:
                            break
                        if file.endswith('.linkstream'):
                            print("******************************", gamma, file, "******************************")
                            V_living = SommetsVivant(pathFile)
                            nb_file += 1

                            # LS
                            start_time = time.time()

                            g_m_n = MatchingN(gamma, pathFile)
                            link_stream = g_m_n.linkStream()
                            G_edges2 = g_m_n.G_edges(link_stream, gamma)
                            nb_gmLS = g_m_n.gammaMatching(G_edges2, gamma)

                            timeLS = round(time.time() - start_time, 4)

                            file = file.replace('linkstream', 'linkstreamAR')
                            pathFile = pathF2 + file

                            # DEC
                            start_time = time.time()

                            # ça replace ce qu'il y a dans le fichier .nb_matchingAR
                            results = getNbMatchingT(gamma, pathFile)
                            dec = DecomposeGreedy()
                            list_pos_matching = dec.get_list_pos_matching_from_list(results)
                            nb_gmDEC, M = dec.nb_gamma_matching_decomposition(list_pos_matching, nb_matching=0,
                                                                              M=[])

                            timeDEC = round(time.time() - start_time, 4)

                            # algo BBR19
                            start_time = time.time()

                            g_mV2 = MatchingBBR19(gamma, pathFile)
                            link_stream = g_mV2.linkStream()
                            g_edges = g_mV2.gamma_edges(link_stream)
                            nb_gmBBR19 = len(g_mV2.greedy_gamma_matching(g_edges))

                            timeBBR19 = round(time.time() - start_time, 4)

                            # LS AR
                            start_time = time.time()

                            g_m_n = MatchingN(gamma, pathFile)
                            link_streamAR = g_m_n.linkStream()
                            g_edges = g_m_n.gamma_edgesAR(gamma, link_streamAR)
                            nb_gmLSAR = g_m_n.gammaMatching(g_edges, gamma)

                            timeLSAR = round(time.time() - start_time, 4)

                            fwT.write(file.replace('.linkstreamAR', '') + ' & ' +
                                      str(link_stream['V']) + ' & ' +
                                      str(link_stream['T']) + ' & ' +
                                      str(len(link_stream['E'])) + ' & ' +
                                      str(len(g_edges)) + ' & ' +
                                      str(timeBBR19) + ' & ' +
                                      str(timeLS) + ' & ' +
                                      str(timeLSAR) + ' & ' +
                                      str(timeDEC) + '\n')

                            fwNB.write(file.replace('.linkstreamAR', '') + ' & ' +
                                       str(link_stream['V']) + ' & ' +
                                       str(link_stream['T']) + ' & ' +
                                       str(len(link_stream['E'])) + ' & ' +
                                       str(V_living) + ' & ' +
                                       str(nb_gmBBR19) + ' & ' +
                                       str(nb_gmLS) + ' & ' +
                                       str(nb_gmLSAR) + ' & ' +
                                       str(nb_gmDEC) + '\n')


main()
