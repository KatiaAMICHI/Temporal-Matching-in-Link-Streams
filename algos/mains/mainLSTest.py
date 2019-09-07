import csv
import os
import time, pprint
from collections import defaultdict

from algos.LSTest import MatchingNV2, GammaMach
from algos.mains.main import var


def mainLS():
    fileFaitG2B2 = '../outPutFile/LS/failFaitB2G2'
    f = open(fileFaitG2B2, 'r')
    filesFait = f.read().split('\n')
    print("filesFait : ", filesFait)
    pathF1 = '../res'
    fileOutPutTimes = '../outPutFile/LS/executionTimesG2B2.csv'
    fileOutPutNbGM = '../outPutFile/LS/NBGammaMatchingG2B2.csv'

    pathResult = '../outPutFile/LS/resultG2B2Suit'  # on écrit tt les données pour le calcule de la variance

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

        for gamma in range(2, 3):
            for f2 in os.listdir(pathF2):
                path = pathF2 + "/" + f2 + "/"
                if os.path.isdir(path):
                    if "1003_inf" in path:
                        continue
                    for file in os.listdir(path):
                        if file.endswith('.linkstream'):
                            if f2 in filesFait:
                                continue

                            print("******************************", gamma, f2, "******************************")
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
                            if "enron400" in f1 or "rollernet" in f1:
                                fileOutPutResult = file.replace(".linkstream", "")
                            else:
                                fileOutPutResult = f2

                            print({'File': fileOutPutResult, "Gamma": gamma,
                                   'V': link_stream['V'],
                                   'T': link_stream['T'],
                                   'E': len(link_stream['E']),
                                   'TG_edges': end_time_LS_edges,
                                   'Tnb_gmLS': end_time_LS_NbGM,
                                   'G_edges': nb_g_edgesLs,
                                   'nb_gmLS': nb_gmLS})

                            # writerResult.writerow({'File': fileOutPutResult, "Gamma": gamma,
                            #                        'V': link_stream['V'],
                            #                        'T': link_stream['T'],
                            #                        'E': len(link_stream['E']),
                            #                        'TG_edges': end_time_LS_edges,
                            #                        'Tnb_gmLS': end_time_LS_NbGM,
                            #                        'G_edges': nb_g_edgesLs,
                            #                        'nb_gmLS': nb_gmLS})

            # calcule de la variance et de l'ecart-type
            timesOutPut['varLS'] = var(RT1LS, RT2LS)
            nbGMoutPut['varLS'] = var(R1LS, R2LS)

            # ecriture dans le outPutFile a la fin de chaque parcour d'un dossier
            print()
            print("je vais écrir !!")
            # writerTimes.writerow({'File': f1, 'Gamma': gamma,
            #                       '|V|': round(timesOutPut['V'] / nb_file, 4),
            #                       '|T|': round(timesOutPut['T'] / nb_file, 4),
            #                       '|E|': round(timesOutPut['E'] / nb_file, 4),
            #                       'G_edges': round(timesOutPut['G_edges'] / nb_file, 4),
            #                       "LS": round(timesOutPut['end_time_LS'] / nb_file, 4),
            #                       'varLS': timesOutPut['varLS']})
            #
            # writerNbGM.writerow({'File': f1, 'Gamma': gamma,
            #                      'G_edges': round(nbGMoutPut['G_edges'] / nb_file, 4),
            #                      'LS': round(nbGMoutPut['nb_gmLS'] / nb_file, 4),
            #                      'varLS': nbGMoutPut['varLS']})


def gamma_edges_neighbours(gamma, link_stream):
    P = link_stream["E"].copy()
    result = {"gamma": gamma, "max_matching": 0, "elements": defaultdict(list)}

    last_u = -1
    last_v = -1
    last_t = link_stream["T"]
    gamma_cpt = 0

    for i in range(len(P)):
        (t, u, v) = P[i]

        if u == last_u and v == last_v and t == last_t + 1:
            gamma_cpt += 1
        else:
            gamma_cpt = 0

        if gamma_cpt >= gamma - 1:
            t_starting = t - gamma + 1
            gamma_e = GammaMach(t_starting, u, v)
            # ajout des voisin
            for t_check in range(t_starting - gamma + 1, t_starting + gamma):
                if t_check < 0:
                    continue
                idx_g_e = 0
                for g_e in result['elements'][t_check]:
                    if gamma_e.t == g_e.t and gamma_e.u == g_e.u and gamma_e.v == g_e.v:
                        continue
                    if g_e.u == u or g_e.v == v or g_e.u == v or g_e.v == u:
                        gamma_e.neighbours.add(g_e)
                        gamma_e.nb_neighbours += 1
                        result['elements'][t_check][idx_g_e].neighbours.add(gamma_e)
                        result['elements'][t_check][idx_g_e].nb_neighbours += 1

                    idx_g_e += 1

            result["elements"][t_starting].append(gamma_e)
            result["max_matching"] += 1

        last_u = u
        last_v = v
        last_t = t

    return result


def truc():
    gamma = 2
    file = '/home/katia/Documents/Temporal-Matching-in-Link-Streams/res/gen_rollernet/decoData/fileTruc2.linkstream'
    fileAR = '/home/katia/Documents/Temporal-Matching-in-Link-Streams/res/gen_rollernet/decoData/fileTruc2.linkstreamAR'
    file = '../res/gen_enron/decoData/enron1000000.linkstream'
    fileAR = '../res/gen_enron/decoData/enron1000000.linkstreamAR'

    print("***************** Link Stream *****************")
    g_m_n = MatchingNV2(gamma, fileAR)
    link_streamAR = g_m_n.linkStreamList()

    g_m_n = MatchingNV2(gamma, file)
    link_stream = g_m_n.linkStreamList()

    print("******************* BBR19   *******************")
    start_time = time.time()
    g_edges = gamma_edges_neighbours(gamma, link_streamAR)
    end_time_LS_NbGM = round(time.time() - start_time, 4)

    print(g_edges['max_matching'])

    print("end_time_LS_NbGM  : ", end_time_LS_NbGM)

    print("******************* G_edges  *******************")
    start_time = time.time()
    G_edges = g_m_n.G_edgesMatching(link_stream, gamma)
    end_time_LS_NbGM = round(time.time() - start_time, 4)
    print(G_edges['max_matching'])
    print("end_time_LS_NbGM  : ", end_time_LS_NbGM)
    # pprint.pprint(len(G_edges['elements']))
    # pprint.pprint(G_edges['elements'])

    print("******************* 2 G_edges  *******************")
    start_time = time.time()
    G_edges2 = g_m_n.G_edgesMatchingV2(link_stream, gamma)
    end_time_LS_NbGM = round(time.time() - start_time, 4)
    pprint.pprint(G_edges2['max_matching'])
    print("end_time_LS_NbGM  : ", end_time_LS_NbGM)
    # pprint.pprint(G_edges2['elements'])

    print("******************* G_edges  *******************")
    nb_gmLS = g_m_n.gammaMatchingG_edges_avancer(g_edges, gamma)
    print(nb_gmLS)

    nb_gmLS = g_m_n.gammaMatchingG_edges_avancer(G_edges, gamma)
    print(nb_gmLS)

    nb_gmLS = g_m_n.gammaMatchingG_edges_avancer(G_edges2, gamma)
    print(nb_gmLS)