import csv
import os
import time

from math import sqrt

from algos.mainClass.BBR19 import MatchingBBR19
from algos.mainClass.DEC import *
from algos.mainClass.LS import MatchingN
from algos.mainClass.TrucCommain import SommetsVivant
from algos.maxMAtchingGraph import getNbMatchingT


def main():
    path = '../../res/'
    base = 'rollernet'

    resultsTimes = '../../Results/' + base + '/resultsTimesG2.csv'
    csv_Times = open(resultsTimes, mode='w')
    fieldnamesTimes = ["File", "Gamma", "V", "T", "E", "G_Edges", "BBR19", "LS", "LSAR", "DEC", "varNbGMTLS",
                       "varNbGMTDEC", "varNbGMTBBR19", "varNbGMTLSAR"]
    writerTimes = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimes)
    writerTimes.writeheader()

    timesOutPut = {'V': 0, 'T': 0, 'E': 0, 'G_Edges': 0, 'BBR19': 0, 'LS': 0, 'LSAR': 0,
                   'DEC': 0, 'varNbGMTLS': 0, 'varNbGMTDEC': 0, 'varNbGMTBBR19': 0, 'varNbGMTLSAR': 0}

    resultsNB = '../../Results/' + base + '/resultsNBG2.csv'
    csv_Times = open(resultsNB, mode='w')
    fieldnamesNB = ["File", "Gamma", "V", "T", "E", "V_living", "G_Edges", "BBR19", "LS", "LSAR", "DEC", "varNbGMLS",
                    "varNbGMDEC",
                    "varNbGMBBR19", "varNbGMLSAR"]
    writerNbGM = csv.DictWriter(csv_Times, fieldnames=fieldnamesNB)
    writerNbGM.writeheader()

    nbGMoutPut = {'V': 0, 'T': 0, 'E': 0, 'V_living': 0, 'G_Edges': 0, 'BBR19': 0, 'LS': 0, 'LSAR': 0,
                  'DEC': 0, 'varNbGMLS': 0, 'varNbGMDEC': 0, 'varNbGMBBR19': 0, 'varNbGMLSAR': 0}

    print("je suis la")

    for gamma in range(2, 3):
        for f1 in os.listdir(path):
            nb_file = 0
            pathF1 = path + f1 + '/'
            if base not in pathF1:
                continue

            fileResultNB = '../../Results/' + base + '/ResultsFilesNBG2.csv'
            csv_fileNB = open(fileResultNB, mode='w')
            fieldnamesFilesNB = ["File", "Gamma", "V", "T", "E", "V_living", "G_Edges", "BBR19", "LS", "LSAR", "DEC"]
            fwNB = csv.DictWriter(csv_fileNB, fieldnames=fieldnamesFilesNB)
            fwNB.writeheader()

            fileResultTime = '../../Results/' + base + '/ResultsFilesTimeG2.csv'
            csv_fileTime = open(fileResultTime, mode='w')
            fieldnamesFilesTime = ["File", "Gamma", "V", "T", "E", "G_Edges", "BBR19", "LS", "LSAR", "DEC"]
            fwT = csv.DictWriter(csv_fileTime, fieldnames=fieldnamesFilesTime)
            fwT.writeheader()

            listNbGMLS = []
            listNbGMTimeLS = []

            listNbGMBBR19 = []
            listNbGMTimeBBR19 = []

            listNbGMLSAR = []
            listNbGMTimeLSAR = []

            listNbGMDEC = []
            listNbGMTimeDEC = []

            if os.path.isdir(pathF1):
                for f2 in os.listdir(pathF1):
                    pathF2 = pathF1 + f2 + '/'
                    if os.path.isdir(pathF2):
                        if "1003_inf" in pathF2:
                            continue
                        for file in os.listdir(pathF2):
                            pathFile = pathF2 + file

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

                                listNbGMLS.append(nb_gmLS)
                                listNbGMTimeLS.append(timeLS)

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

                                listNbGMDEC.append(nb_gmDEC)
                                listNbGMTimeDEC.append(timeDEC)

                                # algo BBR19
                                start_time = time.time()
                                g_mV2 = MatchingBBR19(gamma, pathFile)
                                link_stream = g_mV2.linkStream()
                                g_edges = g_mV2.gamma_edges(link_stream)
                                nb_gmBBR19 = len(g_mV2.greedy_gamma_matching(g_edges))
                                timeBBR19 = round(time.time() - start_time, 4)

                                listNbGMBBR19.append(nb_gmBBR19)
                                listNbGMTimeBBR19.append(timeBBR19)

                                # LS AR
                                start_time = time.time()
                                g_m_n = MatchingN(gamma, pathFile)
                                link_streamAR = g_m_n.linkStream()
                                g_edges = g_m_n.gamma_edgesAR(gamma, link_streamAR)
                                nb_g_edges = g_edges['max_matching']
                                nb_gmLSAR = g_m_n.gammaMatching(g_edges, gamma)
                                timeLSAR = round(time.time() - start_time, 4)

                                listNbGMLSAR.append(nb_gmLSAR)
                                listNbGMTimeLSAR.append(timeLSAR)

                                timesOutPut['V'] += link_stream['V']
                                timesOutPut['T'] += link_stream['T']
                                timesOutPut['E'] += len(link_stream['E'])
                                timesOutPut['G_Edges'] += nb_g_edges
                                timesOutPut['BBR19'] += timeBBR19
                                timesOutPut['LS'] += timeLS
                                timesOutPut['LSAR'] += timeLSAR
                                timesOutPut['DEC'] += timeDEC

                                fwT.writerow({'File': file.replace('.linkstreamAR', ''), 'Gamma': gamma,
                                              'V': link_stream['V'],
                                              'T': link_stream['T'],
                                              'E': len(link_stream['E']),
                                              'G_Edges': nb_g_edges,
                                              'BBR19': timeBBR19,
                                              'LS': timeLS,
                                              'LSAR': timeLSAR,
                                              'DEC': timeDEC})

                                nbGMoutPut['V'] += link_stream['V']
                                nbGMoutPut['T'] += link_stream['T']
                                nbGMoutPut['E'] += len(link_stream['E'])
                                nbGMoutPut['V_living'] += V_living
                                nbGMoutPut['G_Edges'] += nb_g_edges
                                nbGMoutPut['BBR19'] += nb_gmBBR19
                                nbGMoutPut['LS'] += nb_gmLS
                                nbGMoutPut['LSAR'] += nb_gmLSAR
                                nbGMoutPut['DEC'] += nb_gmDEC

                                fwNB.writerow({'File': file.replace('.linkstreamAR', ''), 'Gamma': gamma,
                                               'V': link_stream['V'],
                                               'T': link_stream['T'],
                                               'E': len(link_stream['E']),
                                               'V_living': V_living,
                                               'G_Edges': g_edges['max_matching'],
                                               'BBR19': nb_gmBBR19,
                                               'LS': nb_gmLS,
                                               'LSAR': nb_gmLSAR,
                                               'DEC': nb_gmDEC})

                # ecriture dans le outPutFile a la fin de chaque parcour d'un dossier
                print()
                print("je vais écrir !!", nb_file)

                # calcule de l'écart type
                # LS
                avgNbGMTimeLS = round(timesOutPut['LS'] / nb_file, 4)
                varNbGMTLS = sqrt(sum(map(lambda x: x * x - avgNbGMTimeLS * avgNbGMTimeLS, listNbGMTimeLS))) / nb_file

                avgNbGMLS = round(nbGMoutPut['LS'] / nb_file, 4)
                varNbGMLS = sqrt(sum(map(lambda x: x * x - avgNbGMLS * avgNbGMLS, listNbGMLS))) / nb_file

                # DEC
                avgNbGMTimeDEC = round(timesOutPut['DEC'] / nb_file, 4)
                varNbGMTDEC = sqrt(
                    sum(map(lambda x: x * x - avgNbGMTimeDEC * avgNbGMTimeDEC, listNbGMTimeDEC))) / nb_file

                avgNbGMDEC = round(nbGMoutPut['DEC'] / nb_file, 4)
                varNbGMDEC = sqrt(sum(map(lambda x: x * x - avgNbGMDEC * avgNbGMDEC, listNbGMDEC))) / nb_file

                # BBR19
                avgNbGMTimeBBR19 = round(timesOutPut['BBR19'] / nb_file, 4)
                varNbGMTBBR19 = sqrt(
                    sum(map(lambda x: x * x - avgNbGMTimeBBR19 * avgNbGMTimeBBR19, listNbGMTimeBBR19))) / nb_file

                avgNbGMBBR19 = round(nbGMoutPut['BBR19'] / nb_file, 4)
                varNbGMBBR19 = sqrt(sum(map(lambda x: x * x - avgNbGMBBR19 * avgNbGMBBR19, listNbGMBBR19))) / nb_file

                # LSAR
                avgNbGMTimeLSAR = round(timesOutPut['LSAR'] / nb_file, 4)
                varNbGMTLSAR = sqrt(
                    sum(map(lambda x: x * x - avgNbGMTimeLSAR * avgNbGMTimeLSAR, listNbGMTimeLSAR))) / nb_file

                avgNbGMLSAR = round(nbGMoutPut['LSAR'] / nb_file, 4)
                varNbGMLSAR = sqrt(sum(map(lambda x: x * x - avgNbGMLSAR * avgNbGMLSAR, listNbGMLSAR))) / nb_file

                writerTimes.writerow({'File': f1, 'Gamma': gamma,
                                      'V': round(timesOutPut['V'] / nb_file, 4),
                                      'T': round(timesOutPut['T'] / nb_file, 4),
                                      'E': round(timesOutPut['E'] / nb_file, 4),
                                      'G_Edges': round(timesOutPut['G_Edges'] / nb_file, 4),
                                      'BBR19': round(timesOutPut['BBR19'] / nb_file, 4),
                                      'LS': round(timesOutPut['LS'] / nb_file, 4),
                                      'LSAR': round(timesOutPut['LSAR'] / nb_file, 4),
                                      'DEC': round(timesOutPut['DEC'] / nb_file, 4),
                                      'varNbGMTLS': round(varNbGMTLS, 4),
                                      'varNbGMTDEC': round(varNbGMTDEC, 4),
                                      'varNbGMTBBR19': round(varNbGMTBBR19, 4),
                                      'varNbGMTLSAR': round(varNbGMTLSAR, 4)})

                writerNbGM.writerow({'File': f1, 'Gamma': gamma,
                                     'V': round(nbGMoutPut['V'] / nb_file, 4),
                                     'T': round(nbGMoutPut['T'] / nb_file, 4),
                                     'E': round(nbGMoutPut['E'] / nb_file, 4),
                                     'V_living': round(nbGMoutPut['V_living'] / nb_file, 4),
                                     'G_Edges': round(nbGMoutPut['G_Edges'] / nb_file, 4),
                                     'BBR19': round(nbGMoutPut['BBR19'] / nb_file, 4),
                                     'LS': round(nbGMoutPut['LS'] / nb_file, 4),
                                     'LSAR': round(nbGMoutPut['LSAR'] / nb_file, 4),
                                     'DEC': round(nbGMoutPut['DEC'] / nb_file, 4),
                                     'varNbGMLS': round(varNbGMLS, 4),
                                     'varNbGMDEC': round(varNbGMDEC, 4),
                                     'varNbGMBBR19': round(varNbGMBBR19, 4),
                                     'varNbGMLSAR': round(varNbGMLSAR, 4)})


main()
