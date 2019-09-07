import csv
import os
import time

from algos.LS import MatchingN
from algos.greedy_algorithm import Matching
from algos.main import var


# !!!!!!! TODO je dois lancer de mainLS avec B1 sur mon pc ce soir !!!!

# TODO lancement de mainLS avec enron sur hp
# TODO lancement de mainLS avec rollernet sur dell
# TODO lancement de mainBB19 avec B2 sur dell
# TODO relancement de mainLS avec gamma=4 sur 1003 fichier un peu avant 17h40
# 1h30 je viens de le lancer a partir de gamma = 3
def mainLS():
    pathF1 = '../res'
    fileOutPutTimes = '../outPutFile/LS/executionTimesG6_9.csv'
    fileOutPutNbGM = '../outPutFile/LS/NBGammaMatchingG6_9.csv'

    pathResult = '../outPutFile/LS/resultG6_9'  # on écrit tt les données pour le calcule de la variance

    csv_Times = open(fileOutPutTimes, mode='w')
    csv_NbGM = open(fileOutPutNbGM, mode='w')

    fieldnamesTimes = ['File', 'Gamma', '|V|', '|T|', '|E|', 'G_edges', 'LS', 'varLS']
    writerTimes = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimes)
    writerTimes.writeheader()

    fieldnamesNbGM = ['File', 'Gamma', 'G_edges', 'LS', 'varLS']
    writerNbGM = csv.DictWriter(csv_NbGM, fieldnames=fieldnamesNbGM)
    writerNbGM.writeheader()

    timesOutPut = {'V': 0, 'T': 0, 'E': 0, 'G_edges': 0, 'end_time_LS': 0}

    nbGMoutPut = {'G_edges': 0, 'nb_gmLS': 0, 'varLS': 0}

    for f1 in os.listdir(pathF1):

        pathF2 = pathF1 + "/" + f1
        nb_file = 0

        R1LS = []
        R2LS = []

        RT1LS = []
        RT2LS = []

        if 'gen_rollernet' not in pathF2:
            continue

        fileResult = pathResult + f1
        csv_result = open(fileResult, mode='w')
        fieldnamesResult = ['File', "Gamma", 'V', 'T', 'E', 'TG_edges', 'Tnb_gmLS', 'G_edges', 'nb_gmLS']
        writerResult = csv.DictWriter(csv_result, fieldnames=fieldnamesResult)
        writerResult.writeheader()

        for gamma in range(6, 9):
            for f2 in os.listdir(pathF2):
                path = pathF2 + "/" + f2 + "/"
                if os.path.isdir(path):
                    if "1003_inf" in path:
                        continue
                    for file in os.listdir(path):
                        if file.endswith('.linkstream'):
                            print("******************************", gamma, file, "******************************")
                            # algo with neighbour LS
                            nb_file += 1
                            g_m_n = MatchingN(gamma, path + file)
                            link_stream = g_m_n.linkStreamList()

                            if link_stream['T'] < gamma:
                                end_time_LS_edges = 0
                                end_time_LS_NbGM = 0
                                nb_gmLS = 0
                                nb_g_edgesLs = 0
                            else:

                                start_time = time.time()
                                G_edges = g_m_n.G_edgesMatching(link_stream, gamma)
                                end_time_LS_edges = round(time.time() - start_time, 4)
                                nb_g_edgesLs = G_edges["max_matching"]

                                nbGMoutPut['G_edges'] += nb_g_edgesLs

                                start_time = time.time()
                                nb_gmLS = g_m_n.gammaMatchingG_edges_avancer(G_edges, gamma)
                                end_time_LS_NbGM = round(time.time() - start_time, 4)

                            timesOutPut['V'] += link_stream['V']
                            timesOutPut['T'] += link_stream['T']
                            timesOutPut['E'] += len(link_stream['E'])
                            timesOutPut['G_edges'] += end_time_LS_edges
                            timesOutPut['end_time_LS'] += end_time_LS_NbGM

                            nbGMoutPut['nb_gmLS'] += nb_gmLS

                            R1LS.append(nb_gmLS)
                            R2LS.append(nb_g_edgesLs)

                            RT1LS.append(end_time_LS_NbGM)
                            RT2LS.append(end_time_LS_edges)
                            if "enron" in f1 or "rollernet" in f1:
                                fileOutPutResult = file.replace(".linkstream", "")
                            else:
                                fileOutPutResult = f2

                            writerResult.writerow({'File': fileOutPutResult, "Gamma": gamma,
                                                   'V': link_stream['V'],
                                                   'T': link_stream['T'],
                                                   'E': len(link_stream['E']),
                                                   'TG_edges': end_time_LS_edges,
                                                   'Tnb_gmLS': end_time_LS_NbGM,
                                                   'G_edges': nb_g_edgesLs,
                                                   'nb_gmLS': nb_gmLS})

            # calcule de la variance et de l'ecart-type
            timesOutPut['varLS'] = var(RT1LS, RT2LS)
            nbGMoutPut['varLS'] = var(R1LS, R2LS)

            # ecriture dans le outPutFile a la fin de chaque parcour d'un dossier
            print()
            print("je vais écrir !!")
            writerTimes.writerow({'File': f1, 'Gamma': gamma,
                                  '|V|': round(timesOutPut['V'] / nb_file, 4),
                                  '|T|': round(timesOutPut['T'] / nb_file, 4),
                                  '|E|': round(timesOutPut['E'] / nb_file, 4),
                                  'G_edges': round(timesOutPut['G_edges'] / nb_file, 4),
                                  "LS": round(timesOutPut['end_time_LS'] / nb_file, 4),
                                  'varLS': nbGMoutPut['varLS']})

            writerNbGM.writerow({'File': f1, 'Gamma': gamma,
                                 'G_edges': round(nbGMoutPut['G_edges'] / nb_file, 4),
                                 'LS': round(nbGMoutPut['nb_gmLS'] / nb_file, 4),
                                 'varLS': nbGMoutPut['varLS']})


def mainLSFile():
    gamma = 2
    path = "../res/gen_B2/test0000/"
    file = "test.linkstream"

    if file.endswith('.linkstream'):
        print("******************************", file, "******************************")
        # algo with neighbour LS
        g_m_n = MatchingN(gamma, path + file)
        link_streamList = g_m_n.linkStreamList()

        start_time = time.time()
        G_edges = g_m_n.G_edgesMatching(link_streamList, gamma)
        end_time_LS_edges = round(time.time() - start_time, 4)
        nb_g_edgesLs = G_edges["max_matching"]
        print("end_time_LS_edges : ", end_time_LS_edges)
        print("nb_g_edgesLs : ", nb_g_edgesLs)

        start_time = time.time()
        nb_gmLS = g_m_n.gammaMatchingG_edges_avancer(G_edges, gamma)
        end_time_LS_NbGM = round(time.time() - start_time, 4)
        print("nb_gmLS : ", nb_gmLS)
        print("end_time_LS_NbGM  : ", end_time_LS_NbGM)


mainLS()
