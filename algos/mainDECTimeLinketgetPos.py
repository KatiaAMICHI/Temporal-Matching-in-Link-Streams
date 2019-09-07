import collections
import csv
import time

from algos.BBR19 import MatchingV2
from algos.decGammaMatching import *
from algos.main import var

gamma = 2


def tocsvForeachDir():
    pathF1 = '../res'
    files = collections.defaultdict(int)  # key : "nom du fichier" , value : "nb" le nb fois q'il et present
    fileOutPutTimes = '../outPutFile/DEC/executionTimesG2.csv'
    fileOutPutNbGM = '../outPutFile/DEC/NBGammaMatchingG2.csv'

    pathResult = '../outPutFile/DEC/resultG2'  # on écrit tt les données pour le calcule de la variance

    csv_Times = open(fileOutPutTimes, mode='w')
    csv_NbGM = open(fileOutPutNbGM, mode='w')

    fieldnamesTimes = ['File', 'Gamma', 'DEC', 'varDEC']
    writerTimes = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimes)
    writerTimes.writeheader()

    fieldnamesNbGM = ['File', 'Gamma', 'DEC', 'varDEC']
    writerNbGM = csv.DictWriter(csv_NbGM, fieldnames=fieldnamesNbGM)
    writerNbGM.writeheader()

    timesOutPut = {'end_time_DEC': 0}

    nbGMoutPut = {'nb_gmDEC': 0, 'varDEC': 0}

    for f1 in os.listdir(pathF1):
        pathF2 = pathF1 + "/" + f1
        nb_file = 0

        G_edges_filesDEC = collections.defaultdict(int)

        R1DEC = []
        filesDEC = []

        if 'gen_B1' not in pathF2:
            continue

        fileResult = pathResult + f1
        csv_result = open(fileResult, mode='w')
        fieldnamesResult = ['File', "Gamma", 'Tnb_gmDEC', 'nb_gmDEC']
        writerResult = csv.DictWriter(csv_result, fieldnames=fieldnamesResult)
        writerResult.writeheader()

        for f2 in os.listdir(pathF2):
            path = pathF2 + "/" + f2 + "/"

            if os.path.isdir(path):

                for file in os.listdir(path):
                    if file.endswith('.linkstream'):
                        print("******************************", path + file, "******************************")
                        nb_file += 1

                        g_mV2 = MatchingV2(gamma, path + file)
                        link_stream = g_mV2.linkStream()

                        nb_g_edgesLs = len(g_mV2.gamma_edges(link_stream, gamma))

                        G_edges_filesDEC[str(path + file).replace('.linkstream', '')] = nb_g_edgesLs

                    elif file.endswith('.nb_matching'):
                        dec = DecomposeGreedy()
                        list_pos_matching = dec.get_list_pos_matching(path + file)

                        start_time = time.time()
                        nb_gmDEC, M = dec.nb_gamma_matching_decomposition(list_pos_matching, nb_matching=0, M=[])
                        end_time_DEC_NbGM = round(time.time() - start_time, 4)

                        R1DEC.append(nb_gmDEC)
                        filesDEC.append(str(path + file).replace('.nb_matching', ''))

                        timesOutPut['end_time_DEC'] += end_time_DEC_NbGM
                        nbGMoutPut['nb_gmDEC'] += nb_gmDEC

                fileOutPutResult = f2

                writerResult.writerow({'File': fileOutPutResult, "Gamma": gamma,
                                       'Tnb_gmDEC': end_time_DEC_NbGM,
                                       'nb_gmDEC': nb_gmDEC})

        R2DEC = list(map(lambda x: G_edges_filesDEC[x], filesDEC))
        # calcule de la variance et de l'ecart-type
        nbGMoutPut['varDEC'] = var(R1DEC, R2DEC)

        # ecriture dans le outPutFile a la fin de chaque parcour d'un dossier
        files[f1] += nb_file
        print()
        print("je vais écrir !!")

        writerTimes.writerow({'File': f1, 'Gamma': gamma,
                              "DEC": round(timesOutPut['end_time_DEC'] / nb_file, 4),
                              'varDEC': nbGMoutPut['varDEC']})

        writerNbGM.writerow({'File': f1, 'Gamma': gamma,
                             'DEC': round(nbGMoutPut['nb_gmDEC'] / nb_file, 4),
                             'varDEC': nbGMoutPut['varDEC']})


tocsvForeachDir()
