import collections
import csv
import time

from algos.DpGammaMatching import *
from algos.algoN import MatchingN
from algos.greedy_algorithm import Matching
from algos.main import var


def mainLS():
    pathF1 = '../res'
    fileOutPutTimes = '../outPutFile/LS/executionTimes.csv'
    fileOutPutNbGM = '../outPutFile/LS/NBGammaMatching.csv'

    csv_Times = open(fileOutPutTimes, mode='w')
    csv_NbGM = open(fileOutPutNbGM, mode='w')

    fieldnamesTimes = ['File', '|V|', '|T|', '|E|', 'G_edges', 'LS']

    writerTimes = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimes)
    writerTimes.writeheader()

    fieldnamesNbGM = ['File', 'G_edges', 'LS', 'varLS']
    writerNbGM = csv.DictWriter(csv_NbGM, fieldnames=fieldnamesNbGM)
    writerNbGM.writeheader()

    timesOutPut = {'V': 0, 'T': 0, 'E': 0, 'G_edges': 0, 'end_time_LS': 0}

    nbGMoutPut = {'G_edges': 0, 'nb_gmLS': 0, 'varLS': 0}

    for f1 in os.listdir(pathF1):
        pathF2 = pathF1 + "/" + f1
        nb_file = 0

        R1LS = []
        R2LS = []

        G_edges_filesDP = collections.defaultdict(int)

        if 'gen_B2' in pathF2 or 'gen_test' in pathF2:
            continue
        for f2 in os.listdir(pathF2):
            path = pathF2 + "/" + f2 + "/"

            if os.path.isdir(path):

                for file in os.listdir(path):
                    print("******************************", file, "******************************")

                    if file.endswith('.linkstream'):
                        # algo with neighbour LS
                        nb_file += 1
                        g_m = Matching(gamma, path + file)
                        link_stream = g_m.linkStream()

                        g_m_n = MatchingN(gamma, path + file)
                        link_streamList = g_m_n.linkStreamList()
                        G_edges = g_m_n.G_edgesMatching(link_streamList, gamma)
                        nb_g_edgesLs = G_edges["max_matching"]

                        nbGMoutPut['G_edges'] += G_edges["max_matching"]

                        start_time = time.time()
                        nb_gmLS = g_m_n.gammaMatchingG_edges_avancer(G_edges, gamma)
                        end_time_LS = time.time() - start_time

                        timesOutPut['V'] += link_stream['V']
                        timesOutPut['T'] += link_stream['T']
                        timesOutPut['E'] += len(link_stream['E'])
                        timesOutPut['G_edges'] += len(G_edges)
                        timesOutPut['end_time_LS'] += end_time_LS

                        nbGMoutPut['nb_gmLS'] += nb_gmLS

                        R1LS.append(nb_gmLS)
                        R2LS.append(nb_g_edgesLs)
                        G_edges_filesDP[str(path + file).replace('.linkstream', '')] = nb_g_edgesLs

        # calcule de la variance et de l'ecart-type
        nbGMoutPut['varLS'] = var(R1LS, R2LS)

        # ecriture dans le outPutFile a la fin de chaque parcour d'un dossier
        print()
        print("je vais écrir !!")
        writerTimes.writerow({'File': f1,
                              '|V|': round(timesOutPut['V'] / nb_file, 4),
                              '|T|': round(timesOutPut['T'] / nb_file, 4),
                              '|E|': round(timesOutPut['E'] / nb_file, 4),
                              'G_edges': round(timesOutPut['G_edges'] / nb_file, 4),
                              "LS": round(timesOutPut['end_time_LS'] / nb_file, 4)})

        writerNbGM.writerow({'File': f1,
                             'G_edges': round(nbGMoutPut['G_edges'] / nb_file, 4),
                             'LS': round(nbGMoutPut['nb_gmLS'] / nb_file, 4),
                             'varLS': nbGMoutPut['varLS']})


mainLS()
