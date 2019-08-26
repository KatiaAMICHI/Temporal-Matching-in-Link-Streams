import csv
import os
import time

from algos.BBR19 import MatchingV2
from algos.main import var


# TODO lancer le 26 à 15h28
# TODO changer gen_B2 y a trop de lien !!!!
def mainBBR19():
    pathF1 = '../res'
    fileOutPutTimes = '../outPutFile/BBR19/executionTimes.csv'
    fileOutPutNbGM = '../outPutFile/BBR19/NBGammaMatching.csv'

    pathResult = '../outPutFile/BBR19/result'  # on écrit tt les données pour le calcule de la variance

    csv_Times = open(fileOutPutTimes, mode='w')
    csv_NbGM = open(fileOutPutNbGM, mode='w')

    fieldnamesTimes = ['File', "Gamma", 'G_edges', 'BBR19', 'varBBR19']

    writerTimes = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimes)
    writerTimes.writeheader()

    fieldnamesNbGM = ['File', "Gamma", 'G_edges', 'BBR19', 'varBBR19']
    writerNbGM = csv.DictWriter(csv_NbGM, fieldnames=fieldnamesNbGM)
    writerNbGM.writeheader()

    timesOutPut = {'G_edges': 0, 'end_time_BBR19': 0, 'varBBR19': 0}

    nbGMoutPut = {'G_edges': 0, 'nb_gmBBR19': 0, 'varBBR19': 0}

    for f1 in os.listdir(pathF1):
        pathF2 = pathF1 + "/" + f1
        nb_file = 0

        R1BB19 = []
        R2BB19 = []
        RT1BB19 = []
        RT2BB19 = []

        if 'gen_rollernet' not in pathF2:
            continue

        fileResult = pathResult + f1
        csv_result = open(fileResult, mode='w')
        fieldnamesResult = ['File', "Gamma", 'V', 'T', 'E', 'TG_edges', 'Tnb_gmBBR19', 'G_edges', 'nb_gmBBR19']
        writerResult = csv.DictWriter(csv_result, fieldnames=fieldnamesResult)
        writerResult.writeheader()

        for gamma in range(2, 401):
            for f2 in os.listdir(pathF2):
                path = pathF2 + "/" + f2 + "/"
                if os.path.isdir(path):
                    for file in os.listdir(path):
                        # print("******************************", gamma, f2, "******************************")
                        print("******************************", gamma, file, "******************************")
                        if file.endswith('linkstreamAR'):
                            # algo BBR19

                            nb_file += 1

                            g_mV2 = MatchingV2(gamma, path + file)
                            link_stream = g_mV2.linkStream()

                            if link_stream['T'] < gamma:
                                nb_gmBBR19 = 0
                                nb_g_edges = 0
                                end_time_BBR19NbGM = 0
                                end_time_BBR19G_edges = 0

                            else:
                                start_time = time.time()
                                g_edges = g_mV2.gamma_edges(link_stream, gamma)
                                end_time_BBR19G_edges = round(time.time() - start_time, 8)
                                timesOutPut['G_edges'] += end_time_BBR19G_edges
                                nb_g_edges = len(g_edges)
                                nbGMoutPut['G_edges'] += nb_g_edges

                                start_time = time.time()
                                M = g_mV2.greedy_gamma_matching(g_edges, gamma)
                                end_time_BBR19NbGM = round(time.time() - start_time, 8)
                                timesOutPut['end_time_BBR19'] += end_time_BBR19NbGM

                                nb_gmBBR19 = len(M)
                                nbGMoutPut['nb_gmBBR19'] += nb_gmBBR19

                            R1BB19.append(nb_gmBBR19)
                            R2BB19.append(nb_g_edges)

                            RT1BB19.append(end_time_BBR19NbGM)
                            RT2BB19.append(end_time_BBR19G_edges)

                            if "enron" in f1 or "rollernet" in f1:
                                fileOutPutResult = file.replace(".linkstreamAR", "")
                            else:
                                fileOutPutResult = f2

                            writerResult.writerow({'File': fileOutPutResult, "Gamma": gamma,
                                                   'V': link_stream['V'],
                                                   'T': link_stream['T'],
                                                   'E': len(link_stream['E']),
                                                   'TG_edges': end_time_BBR19G_edges,
                                                   'Tnb_gmBBR19': end_time_BBR19NbGM,
                                                   'G_edges': nb_g_edges,
                                                   'nb_gmBBR19': nb_gmBBR19})

            # calcule de la variance et de l'ecart-type
            timesOutPut['varBBR19'] = var(RT1BB19, RT2BB19)
            nbGMoutPut['varBBR19'] = var(R1BB19, R2BB19)

            # ecriture dans le outPutFile a la fin de chaque parcour d'un dossier
            print()
            print("je vais écrir !!")

            writerTimes.writerow({'File': f1, "Gamma": gamma,
                                  'G_edges': round(timesOutPut['G_edges'] / nb_file, 4),
                                  "BBR19": round(timesOutPut['end_time_BBR19'] / nb_file, 4),
                                  'varBBR19': timesOutPut['varBBR19']})

            writerNbGM.writerow({'File': f1, "Gamma": gamma,
                                 'G_edges': round(nbGMoutPut['G_edges'] / nb_file, 4),
                                 'BBR19': round(nbGMoutPut['nb_gmBBR19'] / nb_file, 4),
                                 'varBBR19': nbGMoutPut['varBBR19']})


mainBBR19()
