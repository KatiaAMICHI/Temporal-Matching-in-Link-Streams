import csv
import time

from algos.DpGammaMatching import *
from algos.greedy_algorithmV2 import MatchingV2
from algos.main import moyenne, var


def mainBBR19():
    pathF1 = '../res'
    fileOutPutTimes = '../outPutFile/BBR19/executionTimes.csv'
    fileOutPutNbGM = '../outPutFile/BBR19/NBGammaMatching.csv'

    csv_Times = open(fileOutPutTimes, mode='w')
    csv_NbGM = open(fileOutPutNbGM, mode='w')

    fieldnamesTimes = ['File', 'G_edges', 'BBR19']

    writerTimes = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimes)
    writerTimes.writeheader()

    fieldnamesNbGM = ['File', 'G_edges', 'BBR19', 'varBBR19']
    writerNbGM = csv.DictWriter(csv_NbGM, fieldnames=fieldnamesNbGM)
    writerNbGM.writeheader()

    timesOutPut = {'G_edges': 0, 'end_time_BBR19': 0}

    nbGMoutPut = {'G_edges': 0, 'nb_gmBBR19': 0, 'varBBR19': 0}

    for f1 in os.listdir(pathF1):
        pathF2 = pathF1 + "/" + f1
        nb_file = 0

        R1BB19 = []
        R2BB19 = []

        if 'gen_test' in pathF2 or 'gen_B2' in pathF2:
            continue

        for f2 in os.listdir(pathF2):
            path = pathF2 + "/" + f2 + "/"

            if os.path.isdir(path):

                for file in os.listdir(path):
                    print("******************************", file, "******************************")
                    if file.endswith('linkstreamAR'):
                        # algo BBR19

                        nb_file += 1

                        g_mV2 = MatchingV2(gamma, path + file)
                        link_stream = g_mV2.linkStream()

                        start_time = time.time()
                        g_edges = g_mV2.gamma_edges(link_stream, gamma)
                        end_time_BBR19 = time.time() - start_time
                        timesOutPut['G_edges'] += end_time_BBR19
                        nb_g_edges = len(g_edges)
                        nbGMoutPut['G_edges'] += nb_g_edges

                        start_time = time.time()
                        M = g_mV2.greedy_gamma_matching(g_edges, gamma)
                        end_time_BBR19 = time.time() - start_time
                        timesOutPut['end_time_BBR19'] += end_time_BBR19

                        nb_gmBBR19 = len(M)
                        nbGMoutPut['nb_gmBBR19'] += nb_gmBBR19

                        R1BB19.append(nb_gmBBR19)
                        R2BB19.append(nb_g_edges)

        # calcule de la variance et de l'ecart-type
        nbGMoutPut['varBBR19'] = var(R1BB19, R2BB19)

        # ecriture dans le outPutFile a la fin de chaque parcour d'un dossier
        print()
        print("je vais écrir !!")

        writerTimes.writerow({'File': f1,
                              'G_edges': round(timesOutPut['G_edges'] / nb_file, 4),
                              "BBR19": round(timesOutPut['end_time_BBR19'] / nb_file, 4)})

        writerNbGM.writerow({'File': f1,
                             'G_edges': round(nbGMoutPut['G_edges'] / nb_file, 4),
                             'BBR19': round(nbGMoutPut['nb_gmBBR19'] / nb_file, 4), 'varBBR19': nbGMoutPut['varBBR19']})


mainBBR19()
