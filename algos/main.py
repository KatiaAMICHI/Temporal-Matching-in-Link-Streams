import collections
import os
import time
import pprint

from algos.greedy_algorithm import Matching
from algos.greedy_algorithmV2 import MatchingV2
from algos.algoN import MatchingN
from algos.DpGammaMatching import *
import csv

from algos.testdynpmethod import gammaMatchig1DSort

gamma = 2
path_enron = "../res/enron/test_enron/"
path_rollernet = "../res/rollernet/test_rollernet/"


def tocsv():
    with open('../outPutFile/file2.csv', mode='w') as csv_file:
        fieldnames = ['File', '|V|', '|T|', '|E|', 'E_gamma', 'ARgreedyA', 'algoN']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for path in path_rollernet, path_enron:
            print("path : ", path)
            for file in os.listdir(path):
                # greedy algo V22 AR
                # if file.endswith('_sort'):
                #
                #     g_mV2 = MatchingV2(gamma, path + file)
                #     link_stream = g_mV2.linkStream()
                #     print("L : ( V:", link_stream["V"], ", T:", link_stream["T"], ", E:", len(link_stream["E"]), ")")
                #
                #     g_edges = g_mV2.gamma_edges(link_stream, gamma)
                #
                #     min_M = len(link_stream["E"])
                #     max_M = -1
                #
                #     start_time = time.time()
                #     M = g_mV2.greedy_gamma_matching(g_edges, gamma)
                #     end_time_ar = time.time() - start_time
                #
                #     print("max : ", max_M, "   min : ", min_M)
                #     print("g_edges::: ", g_edges)
                # else:

                print("file : ", file)

                # link_stream
                g_m = Matching(gamma, path + file)
                link_stream = g_m.linkStream()

                # algo with neighbour
                g_m_n = MatchingN(gamma, path + file)
                link_streamList = g_m_n.linkStreamList()
                E_gamma = g_m_n.E_gammaMatching(link_streamList, gamma)
                start_time = time.time()
                g_m_n.gammaMatchingE_gamma_avancer(E_gamma, gamma)
                end_time_n = time.time() - start_time

                print("je vais écrir !!")
                print({'File': file, '|V|': link_stream["V"], '|T|': link_stream["T"], '|E|': len(link_stream["E"]),
                       'E_gamma': len(E_gamma),
                       "ARgreedyA": 0, "algoN": round(end_time_n, 2)})

                writer.writerow(
                    {'File': file, '|V|': link_stream["V"], '|T|': link_stream["T"], '|E|': len(link_stream["E"]),
                     'E_gamma': len(E_gamma),
                     "ARgreedyA": 0, "algoN": round(end_time_n, 2)})


def tocsvForeachFolder():
    pathF1 = '../res'
    files = collections.defaultdict(int)  # key : "nom du fichier" , value : "nb" le nb foit q'il et present
    fileOutPutTimes = '../outPutFile/executionTimes.csv'
    fileOutPutNbGM = '../outPutFile/NBGammaMatching.csv'

    csv_Times = open(fileOutPutTimes, mode='w')
    csv_NbGM = open(fileOutPutNbGM, mode='w')

    fieldnamesTimes = ['File', '|V|', '|T|', '|E|', 'E_gamma', 'BBR19', 'LS', "DecFF", 'DP']
    writerTimes = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimes)
    writerTimes.writeheader()

    fieldnamesNbGM = ['File', 'E_gamma', 'BBR19', 'LS', "DecFF", 'DP']
    writerNbGM = csv.DictWriter(csv_NbGM, fieldnames=fieldnamesNbGM)
    writerNbGM.writeheader()

    timesOutPut = collections.defaultdict(int)
    timesOutPut['V'] = 0
    timesOutPut['T'] = 0
    timesOutPut['E'] = 0
    timesOutPut['E_gamma'] = 0
    timesOutPut['end_time_BBR19'] = 0
    timesOutPut['end_time_LS'] = 0
    timesOutPut['end_time_DP'] = 0

    nbGMoutPut = {'E_gamma': 0, 'nb_gmBBR19': 0, 'nb_gmLS': 0, 'nb_gmDP': 0}

    for f1 in os.listdir(pathF1):
        pathF2 = pathF1 + "/" + f1
        nb_file = 0

        for f2 in os.listdir(pathF2):
            path = pathF2 + "/" + f2 + "/"

            if os.path.isdir(path):
                for file in os.listdir(path):
                    print("******************************", file, "******************************")
                    if file.endswith('sort.linkstream'):
                        # algo BBR19

                        g_mV2 = MatchingV2(gamma, path + file)
                        link_stream = g_mV2.linkStream()
                        print("L : ( V:", link_stream["V"], ", T:", link_stream["T"], ", E:", len(link_stream["E"]),
                              ")")

                        g_edges = g_mV2.gamma_edges(link_stream, gamma)

                        start_time = time.time()
                        M = g_mV2.greedy_gamma_matching(g_edges, gamma)
                        end_time_BBR19 = time.time() - start_time
                        nb_gmBBR19 = len(M)

                        timesOutPut['end_time_BBR19'] += nb_gmBBR19

                        nbGMoutPut['nb_gmBBR19'] += end_time_BBR19

                        print(">>>>>>>>>>>> max : ", nb_gmBBR19)
                        print(">>>>>>>>>>>> g_edges::: ", len(g_edges))

                    elif file.endswith('.linkstream'):
                        # algo with neighbour

                        nb_file += 1
                        g_m = Matching(gamma, path + file)
                        link_stream = g_m.linkStream()

                        g_m_n = MatchingN(gamma, path + file)
                        link_streamList = g_m_n.linkStreamList()
                        E_gamma = g_m_n.E_gammaMatching(link_streamList, gamma)
                        start_time = time.time()
                        nb_gmLS = g_m_n.gammaMatchingE_gamma_avancer(E_gamma, gamma)
                        end_time_LS = time.time() - start_time

                        timesOutPut['V'] += link_stream['V']
                        timesOutPut['T'] += link_stream['T']
                        timesOutPut['E'] += len(link_stream['E'])
                        timesOutPut['E_gamma'] += len(E_gamma)
                        timesOutPut['end_time_LS'] += end_time_LS

                        nbGMoutPut['E_gamma'] += len(E_gamma)
                        nbGMoutPut['nb_gmLS'] += nb_gmLS

                    elif file.endswith('.nb_matching'):
                        pass
                    elif file.endswith('.position'):
                        pass
                        # dp method

                        n, tmax, d, x = refactorData(path + file)
                        dgGM = DpGammaMatching1D(n, tmax, d, x)
                        start_time = time.time()
                        nb_gmDP = dgGM.gammaMatchig1DSort()
                        end_time_DP = time.time() - start_time

                        timesOutPut['end_time_DP'] += end_time_DP

                        nbGMoutPut['nb_gmDP'] += nb_gmDP

        # ecriture dans le outPutFile a la fin de chaque parcour d'un dossier
        files[f1] += nb_file
        print()
        print("je vais écrir !!")

        # print("Times : ", {'File': f1, '|V|': round(timesOutPut['V'] / nb_file, 2),
        #                    '|T|': round(timesOutPut['T'] / nb_file, 2),
        #                    '|E|': round(timesOutPut['E'] / nb_file, 2),
        #                    'E_gamma': round(timesOutPut['E_gamma'] / nb_file, 2),
        #                    "BBR19": round(timesOutPut['end_time_BBR19'] / nb_file, 2),
        #                    "LS": round(timesOutPut['end_time_LS'] / nb_file, 4),
        #                    "DecFF": 0, 'DP': round(timesOutPut['end_time_DP'] / nb_file, 2)})
        print()
        # writerTimes.writerow({'File': f1, '|V|': round(timesOutPut['V'] / nb_file, 2),
        #                       '|T|': round(timesOutPut['T'] / nb_file, 2),
        #                       '|E|': round(timesOutPut['E'] / nb_file, 2),
        #                       'E_gamma': round(timesOutPut['E_gamma'] / nb_file, 2),
        #                       "BBR19": round(timesOutPut['end_time_BBR19'] / nb_file, 2),
        #                       "LS": round(timesOutPut['end_time_LS'] / nb_file, 4),
        #                       "DecFF": 0, 'DP': round(timesOutPut['end_time_DP'] / nb_file, 2)})

        print()

        print("NB GM: ", {'File': f1,
                          'BBR19': nbGMoutPut['nb_gmBBR19'],
                          'LS': nbGMoutPut['nb_gmLS'], "DecFF": 0, 'DP': nbGMoutPut['nb_gmDP']})
        writerNbGM.writerow({'File': f1,
                             'E_gamma': round(nbGMoutPut['E_gamma'] / nb_file, 2),
                             'BBR19': round(nbGMoutPut['nb_gmBBR19'] / nb_file, 2),
                             'LS': round(nbGMoutPut['nb_gmLS'] / nb_file, 2),
                             'DecFF': 0,
                             'DP': round(nbGMoutPut['nb_gmDP'] / nb_file, 2)})


if __name__ == '__main__':
    # tocsv()
    tocsvForeachFolder()
