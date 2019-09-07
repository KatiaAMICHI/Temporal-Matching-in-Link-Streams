import csv
import time, os

from algos.mainClass.DPV2 import *
from algos.mainClass.LS import MatchingN
from algos.mainClass.greedy_algorithm import Matching
from algos.mainClass.BBR19 import MatchingBBR19

path_enron = "../res/enron400/test_enron/"
path_rollernet = "../res/rollernet/test_rollernet/"


# TODO les fichiers .input < 140 n'ont pas la ligne (n, T, d)
# on peut la récupérer dans les fihciers .position

def test_methods_file():
    path = "../res/"
    file = "antoine_link_streams_deco.linkstream"
    fileAR = "antoine_link_streams_decoAR.linkstream"

    if fileAR.endswith('AR.linkstream'):
        # algo BBR19
        print(" *************** ", fileAR, "***************")
        g_mV2 = MatchingBBR19(gamma, path + fileAR)
        link_stream = g_mV2.linkStream()

        g_edges = g_mV2.gamma_edges(link_stream, gamma)
        print("gamma_E : ", len(g_edges))

        M = g_mV2.greedy_gamma_matching(g_edges, gamma)
        print("nb gamma_matching : ", len(M))

    if file.endswith('.linkstream'):
        print(" *************** ", file, "***************")
        # algo with neighbour

        g_m = Matching(gamma, path + file)

        g_m_n = MatchingN(gamma, path + file)
        link_streamList = g_m_n.linkStreamList()
        G_edges = g_m_n.G_edgesMatching(link_streamList, gamma)
        print("gamma_E : ", G_edges["max_matching"])

        nb_gmLS = g_m_n.gammaMatchingG_edges_avancer(G_edges, gamma)
        print("nb gamma_matching : ", nb_gmLS)


def tocsvForeachDir():
    pathF1 = '../res'
    files = collections.defaultdict(int)  # key : "nom du fichier" , value : "nb" le nb fois q'il et present
    fileOutPutTimes = '../outPutFile/gen_test/executionTimesG2.csv'
    fileOutPutNbGM = '../outPutFile/gen_test/NBGammaMatchingG2.csv'

    csv_Times = open(fileOutPutTimes, mode='w')
    csv_NbGM = open(fileOutPutNbGM, mode='w')

    fieldnamesTimes = ['File', '|V|', '|T|', '|E|', 'G_edges', 'BBR19', 'varBBR19', 'LS', 'varLS', "DecFF", 'DP',
                       'varDP']

    writerTimes = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimes)
    writerTimes.writeheader()

    fieldnamesNbGM = ['File', 'G_edges', 'BBR19', 'varBBR19', 'LS', 'varLS', "DecFF", 'DP', 'varDP']
    writerNbGM = csv.DictWriter(csv_NbGM, fieldnames=fieldnamesNbGM)
    writerNbGM.writeheader()

    timesOutPut = collections.defaultdict(int)
    timesOutPut['V'] = 0
    timesOutPut['T'] = 0
    timesOutPut['E'] = 0
    timesOutPut['G_edges'] = 0
    timesOutPut['end_time_BBR19'] = 0
    timesOutPut['end_time_LS'] = 0
    timesOutPut['end_time_DP'] = 0

    nbGMoutPut = {'G_edges': 0, 'nb_gmBBR19': 0, 'varBBR19': 0, 'nb_gmLS': 0, 'varLS': 0, 'nb_gmDP': 0, 'varDP': 0}

    for f1 in os.listdir(pathF1):
        pathF2 = pathF1 + "/" + f1
        nb_file = 0

        R1BB19 = []
        R2BB19 = []

        R1LS = []
        R2LS = []
        G_edges_filesDP = collections.defaultdict(int)

        R1DP = []
        R2DP = []  # vu qu'on ne peut pas avoir le G_edges pour les fichier .posiyion on sauvegarde les nom du fichier puis on le smap avec les result des .linkstream
        filesDP = []
        if 'gen_test' not in pathF2:
            continue
        for f2 in os.listdir(pathF2):
            path = pathF2 + "/" + f2 + "/"

            if os.path.isdir(path):

                for file in os.listdir(path):
                    print("******************************", file, "******************************")
                    if file.endswith('sort.linkstream'):
                        # algo BBR19

                        g_mV2 = MatchingBBR19(gamma, path + file)
                        link_stream = g_mV2.linkStream()

                        g_edges = g_mV2.gamma_edges(link_stream, gamma)
                        nb_g_edges = len(g_edges)

                        start_time = time.time()
                        M = g_mV2.greedy_gamma_matching(g_edges, gamma)
                        end_time_BBR19 = time.time() - start_time

                        timesOutPut['end_time_BBR19'] += end_time_BBR19
                        nb_gmBBR19 = len(M)
                        nbGMoutPut['nb_gmBBR19'] += nb_gmBBR19

                        print(nb_gmBBR19, nb_g_edges)
                        R1BB19.append(nb_gmBBR19)
                        R2BB19.append(nb_g_edges)

                    elif file.endswith('.linkstream'):
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

                        R1DP.append(nb_gmDP)
                        filesDP.append(str(path + file).replace('.position', ''))

        R2DP = list(map(lambda x: G_edges_filesDP[x], filesDP))

        # calcule de la variance et de l'ecart-type
        nbGMoutPut['varBBR19'] = var(R1BB19, R2BB19)
        nbGMoutPut['varLS'] = var(R1LS, R2LS)
        nbGMoutPut['varDP'] = var(R1DP, R2DP)

        # ecriture dans le outPutFile a la fin de chaque parcour d'un dossier
        files[f1] += nb_file
        print()
        print("je vais écrir !!")

        writerTimes.writerow({'File': f1, '|V|': round(timesOutPut['V'] / nb_file, 2),
                              '|T|': round(timesOutPut['T'] / nb_file, 2),
                              '|E|': round(timesOutPut['E'] / nb_file, 2),
                              'G_edges': round(timesOutPut['G_edges'] / nb_file, 2),
                              "BBR19": round(timesOutPut['end_time_BBR19'] / nb_file, 2),
                              "LS": round(timesOutPut['end_time_LS'] / nb_file, 4),
                              "DecFF": 0, 'DP': round(timesOutPut['end_time_DP'] / nb_file, 2)})

        writerNbGM.writerow({'File': f1,
                             'G_edges': round(nbGMoutPut['G_edges'] / nb_file, 2),
                             'BBR19': round(nbGMoutPut['nb_gmBBR19'] / nb_file, 2), 'varBBR19': nbGMoutPut['varBBR19'],
                             'LS': round(nbGMoutPut['nb_gmLS'] / nb_file, 2), 'varLS': nbGMoutPut['varLS'],
                             'DecFF': 0,
                             'DP': round(nbGMoutPut['nb_gmDP'] / nb_file, 2), 'varDP': nbGMoutPut['varDP']})


def moyenne(R1, R2):
    result = round(sum(map(lambda x: x[0] * x[1], zip(R1, R2))), 6)
    sumR2 = sum(R2)
    return None if sumR2 == 0 else round(result / sumR2, 6)


def var(R1, R2):
    """

    :param list_result: matrice 2D (R[0] -> #g_M | R[1] -> G_edges)
    :return: la variance
    """

    if not R1 or not R2:
        return 0
    xb = moyenne(R1, R2)
    return 0 if not xb else round(sum(map(lambda x: x[1] * (x[0] - xb) * (x[0] - xb), zip(R1, R2))) / sum(R2), 6)