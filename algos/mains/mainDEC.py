import csv
import time, os

from math import sqrt

from algos.mainClass.DEC import *
from algos.maxMAtchingGraph import getNbMatchingT

gamma = 3


def tocsvForeachDir():
    pathF1 = '../res'
    fileOutPutTimes = '../outPutFile/DEC/enron/executionTimes.csv'
    fileOutPutNbGM = '../outPutFile/DEC/enron/NBGammaMatching.csv'

    pathResult = '../outPutFile/DEC/enron/result'  # on écrit tt les données pour le calcule de la variance

    csv_Times = open(fileOutPutTimes, mode='w')
    csv_NbGM = open(fileOutPutNbGM, mode='w')

    fieldnamesTimes = ['File', 'Gamma', 'dec', 'time_list_pos_m', 'decTotal', 'varDEC']

    writerTimes = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimes)
    writerTimes.writeheader()

    fieldnamesNbGM = ['File', 'Gamma', 'DEC', 'varDEC']
    writerNbGM = csv.DictWriter(csv_NbGM, fieldnames=fieldnamesNbGM)
    writerNbGM.writeheader()

    timesOutPut = {'end_time_DEC': 0, 'end_time_list_pos_m': 0}

    nbGMoutPut = {'nb_gmDEC': 0, 'varDEC': 0}

    for f1 in os.listdir(pathF1):
        pathF2 = pathF1 + "/" + f1
        nb_file = 0

        if 'gen_enron' not in pathF2:
            continue

        fileResult = pathResult + f1
        csv_result = open(fileResult, mode='w')
        fieldnamesResult = ['File', "Gamma", 'Tnb_gmDEC', 'end_time_list_pos_m', 'nb_gmDEC']
        writerResult = csv.DictWriter(csv_result, fieldnames=fieldnamesResult)
        writerResult.writeheader()
        listNbGM = []
        listNbGMTime = []

        for gamma in range(2, 400):
            for f2 in os.listdir(pathF2):
                path = pathF2 + "/" + f2 + "/"

                if os.path.isdir(path):
                    for file in os.listdir(path):
                        if file.endswith('.linkstreamAR'):
                            # ça replace ce qu'il y a dans le fichier .nb_matchingAR
                            result = getNbMatchingT(gamma, path, file)
                            print("******************************", gamma, file, "******************************")
                            nb_file += 1

                            start_time = time.time()
                            dec = DecomposeGreedy()
                            list_pos_matching = dec.get_list_pos_matching_from_list(result)
                            end_time_list_pos_m = round(time.time() - start_time, 4)

                            start_time = time.time()
                            nb_gmDEC, M = dec.nb_gamma_matching_decomposition(list_pos_matching, nb_matching=0, M=[])
                            end_time_DEC_NbGM = round(time.time() - start_time, 4)

                            listNbGM.append(nb_gmDEC)
                            listNbGMTime.append(nb_gmDEC)

                            timesOutPut['end_time_DEC'] += end_time_DEC_NbGM
                            timesOutPut['end_time_list_pos_m'] += end_time_list_pos_m

                            nbGMoutPut['nb_gmDEC'] += nb_gmDEC

                            writerResult.writerow({'File': file.replace("linkstreamAR", ""), "Gamma": gamma,
                                                   'Tnb_gmDEC': end_time_DEC_NbGM,
                                                   'end_time_list_pos_m': end_time_list_pos_m,
                                                   'nb_gmDEC': nb_gmDEC})

            # ecriture dans le outPutFile a la fin de chaque parcour d'un dossier
            print()
            print("je vais écrir !!")
            averageNbGMTime = round((timesOutPut['end_time_DEC'] + timesOutPut['end_time_list_pos_m']) / nb_file, 4)
            averageNbGM = round(nbGMoutPut['nb_gmDEC'] / nb_file, 4)

            varNbGM = sqrt(sum(map(lambda x: x * x - averageNbGM * averageNbGM, listNbGM))) / nb_file
            varNbGMT = sqrt(sum(map(lambda x: x * x - averageNbGMTime * averageNbGMTime, listNbGMTime))) / nb_file

            writerTimes.writerow({'File': f1, 'Gamma': gamma,
                                  "dec": round(timesOutPut['end_time_DEC'] / nb_file, 4),
                                  "time_list_pos_m": round(timesOutPut['end_time_list_pos_m'] / nb_file, 4),
                                  "decTotal": averageNbGMTime,
                                  'varDEC': round(varNbGMT, 4)})

            writerNbGM.writerow({'File': f1, 'Gamma': gamma,
                                 'DEC': averageNbGM,
                                 'varDEC': round(varNbGM, 4)})


tocsvForeachDir()
