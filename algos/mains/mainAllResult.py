import csv
import os
import time

from math import sqrt

from algos.mainClass.BBR19 import MatchingBBR19
from algos.mainClass.DC import *
from algos.mainClass.LS import MatchingN
from algos.mainClass.commonObjects import SommetsVivant
from algos.maxMAtchingGraph import getNbMatchingT


def dataToCsv(file, result):
    with open(file, "w+") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(result.items())


def main():
    path = '../../res/'
    base = 'B1'

    resultsTimes = '../../Results/' + base + '/resultsTimesG2.csv'
    csv_Times = open(resultsTimes, mode='w')
    fieldnamesTimes = ["File", "Gamma", "V", "T", "E", "G_Edges", "BBR19", "LS", "LSsort", "DC", "varNbGMTLS",
                       "varNbGMTDC", "varNbGMTBBR19", "varNbGMTLSsort"]
    writerTimes = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimes)
    writerTimes.writeheader()

    timesOutPut = {'V': 0, 'T': 0, 'E': 0, 'G_Edges': 0, 'BBR19': 0, 'LS': 0, 'LSsort': 0,
                   'DC': 0, 'varNbGMTLS': 0, 'varNbGMTDC': 0, 'varNbGMTBBR19': 0, 'varNbGMTLSsort': 0}

    resultsNB = '../../Results/' + base + '/resultsNBG2.csv'
    csv_Times = open(resultsNB, mode='w')
    fieldnamesNB = ["File", "Gamma", "V", "T", "E", "V_living", "G_Edges", "BBR19", "LS", "LSsort", "DC", "varNbGMLS",
                    "varNbGMDC",
                    "varNbGMBBR19", "varNbGMLSsort"]
    writerNbGM = csv.DictWriter(csv_Times, fieldnames=fieldnamesNB)
    writerNbGM.writeheader()

    nbGMoutPut = {'V': 0, 'T': 0, 'E': 0, 'V_living': 0, 'G_Edges': 0, 'BBR19': 0, 'LS': 0, 'LSsort': 0,
                  'DC': 0, 'varNbGMLS': 0, 'varNbGMDC': 0, 'varNbGMBBR19': 0, 'varNbGMLSsort': 0}

    for gamma in range(2, 3):
        for f1 in os.listdir(path):
            nb_file = 0
            pathF1 = path + f1 + '/'
            if base not in pathF1:
                continue

            fileResultNB = '../../Results/' + base + '/ResultsFilesNBG2.csv'
            csv_fileNB = open(fileResultNB, mode='w')
            fieldnamesFilesNB = ["File", "Gamma", "V", "T", "E", "V_living", "G_Edges", "BBR19", "LS", "LSsort", "DC"]
            fwNB = csv.DictWriter(csv_fileNB, fieldnames=fieldnamesFilesNB)
            fwNB.writeheader()

            fileResultTime = '../../Results/' + base + '/ResultsFilesTimeG2.csv'
            csv_fileTime = open(fileResultTime, mode='w')
            fieldnamesFilesTime = ["File", "Gamma", "V", "T", "E", "G_Edges", "BBR19", "LS", "LSsort", "DC"]
            fwT = csv.DictWriter(csv_fileTime, fieldnames=fieldnamesFilesTime)
            fwT.writeheader()

            listNbGMLS = []
            listNbGMTimeLS = []

            listNbGMBBR19 = []
            listNbGMTimeBBR19 = []

            listNbGMLSsort = []
            listNbGMTimeLSsort = []

            listNbGMDC = []
            listNbGMTimeDC = []

            if os.path.isdir(pathF1):
                for f2 in os.listdir(pathF1):
                    pathF2 = pathF1 + f2 + '/'
                    if os.path.isdir(pathF2):
                        if "1003_inf" in pathF2:
                            continue
                        for file in os.listdir(pathF2):
                            pathFile = pathF2 + file

                            if file.endswith('.linkstream'):
                                print("******************************", gamma, f2, "******************************")
                                V_living = SommetsVivant(pathFile)
                                nb_file += 1

                                # LS
                                start_time = time.time()
                                g_m_n = MatchingN(gamma, pathFile)
                                link_stream = g_m_n.linkStream()
                                G_edges2 = g_m_n.G_edges(link_stream, gamma)
                                nb_gmLS, resultsTLS = g_m_n.gammaMatching(G_edges2, gamma)
                                timeLS = round(time.time() - start_time, 4)

                                listNbGMLS.append(nb_gmLS)
                                listNbGMTimeLS.append(timeLS)
                                # End LS

                                file = file.replace('linkstream', 'linkstreamAR')
                                pathFile = pathF2 + file

                                # DC
                                start_time = time.time()
                                # ça replace ce qu'il y a dans le fichier .nb_matchingAR
                                results = getNbMatchingT(gamma, pathFile)
                                dc = DecomposeGreedy(gamma)
                                list_pos_matching = dc.get_list_pos_matching_from_list(results)
                                nb_gmDC, M = dc.nb_gamma_matching_decomposition(list_pos_matching, nb_matching=0, M=[])
                                timeDC = round(time.time() - start_time, 4)

                                listNbGMDC.append(nb_gmDC)
                                listNbGMTimeDC.append(timeDC)
                                # End DC

                                # BBR19
                                start_time = time.time()
                                g_mV2 = MatchingBBR19(gamma, pathFile)
                                link_stream = g_mV2.linkStream()
                                g_edges = g_mV2.gamma_edges(link_stream)
                                nb_gmBBR19, resultsTBBR19 = g_mV2.greedy_gamma_matching(g_edges)
                                timeBBR19 = round(time.time() - start_time, 4)

                                listNbGMBBR19.append(nb_gmBBR19)
                                listNbGMTimeBBR19.append(timeBBR19)
                                # End BBR19

                                # LSsort
                                start_time = time.time()
                                g_m_n = MatchingN(gamma, pathFile)
                                link_streamAR = g_m_n.linkStream()
                                g_edges = g_m_n.gamma_edges_sort(gamma, link_streamAR)
                                nb_g_edges = g_edges['max_matching']
                                nb_gmLSsort, resultsTLSsort = g_m_n.gammaMatching(g_edges, gamma)
                                timeLSsort = round(time.time() - start_time, 4)

                                listNbGMLSsort.append(nb_gmLSsort)
                                listNbGMTimeLSsort.append(timeLSsort)
                                # End LSsort

                                timesOutPut['V'] += link_stream['V']
                                timesOutPut['T'] += link_stream['T']
                                timesOutPut['E'] += len(link_stream['E'])
                                timesOutPut['G_Edges'] += nb_g_edges
                                timesOutPut['BBR19'] += timeBBR19
                                timesOutPut['LS'] += timeLS
                                timesOutPut['LSsort'] += timeLSsort
                                timesOutPut['DC'] += timeDC

                                fwT.writerow({'File': f2, 'Gamma': gamma,
                                              'V': link_stream['V'],
                                              'T': link_stream['T'],
                                              'E': len(link_stream['E']),
                                              'G_Edges': nb_g_edges,
                                              'BBR19': timeBBR19,
                                              'LS': timeLS,
                                              'LSsort': timeLSsort,
                                              'DC': timeDC})

                                nbGMoutPut['V'] += link_stream['V']
                                nbGMoutPut['T'] += link_stream['T']
                                nbGMoutPut['E'] += len(link_stream['E'])
                                nbGMoutPut['V_living'] += V_living
                                nbGMoutPut['G_Edges'] += nb_g_edges
                                nbGMoutPut['BBR19'] += nb_gmBBR19
                                nbGMoutPut['LS'] += nb_gmLS
                                nbGMoutPut['LSsort'] += nb_gmLSsort
                                nbGMoutPut['DC'] += nb_gmDC

                                fwNB.writerow({'File': f2, 'Gamma': gamma,
                                               'V': link_stream['V'],
                                               'T': link_stream['T'],
                                               'E': len(link_stream['E']),
                                               'V_living': V_living,
                                               'G_Edges': g_edges['max_matching'],
                                               'BBR19': nb_gmBBR19,
                                               'LS': nb_gmLS,
                                               'LSsort': nb_gmLSsort,
                                               'DC': nb_gmDC})

                # write to the outPutFile at the end of each path in a folder
                print()
                print("I will write the result for ", f1, ' with the number of files: ', nb_file)

                # calculates standard deviation
                # LS
                avgNbGMTimeLS = round(timesOutPut['LS'] / nb_file, 4)
                varNbGMTLS = sqrt(sum(map(lambda x: x * x - avgNbGMTimeLS * avgNbGMTimeLS, listNbGMTimeLS)) / nb_file)

                avgNbGMLS = round(nbGMoutPut['LS'] / nb_file, 4)
                varNbGMLS = sqrt(sum(map(lambda x: x * x - avgNbGMLS * avgNbGMLS, listNbGMLS)) / nb_file)

                # DC
                avgNbGMTimeDC = round(timesOutPut['DC'] / nb_file, 4)
                varNbGMTDC = sqrt(
                    sum(map(lambda x: x * x - avgNbGMTimeDC * avgNbGMTimeDC, listNbGMTimeDC)) / nb_file)

                avgNbGMDC = round(nbGMoutPut['DC'] / nb_file, 4)
                varNbGMDC = sqrt(sum(map(lambda x: x * x - avgNbGMDC * avgNbGMDC, listNbGMDC)) / nb_file)

                # BBR19
                avgNbGMTimeBBR19 = round(timesOutPut['BBR19'] / nb_file, 4)
                varNbGMTBBR19 = sqrt(
                    sum(map(lambda x: x * x - avgNbGMTimeBBR19 * avgNbGMTimeBBR19, listNbGMTimeBBR19)) / nb_file)

                avgNbGMBBR19 = round(nbGMoutPut['BBR19'] / nb_file, 4)
                varNbGMBBR19 = sqrt(sum(map(lambda x: x * x - avgNbGMBBR19 * avgNbGMBBR19, listNbGMBBR19)) / nb_file)

                # LSsort
                avgNbGMTimeLSsort = round(timesOutPut['LSsort'] / nb_file, 4)
                varNbGMTLSsort = sqrt(
                    sum(map(lambda x: x * x - avgNbGMTimeLSsort * avgNbGMTimeLSsort, listNbGMTimeLSsort)) / nb_file)

                avgNbGMLSsort = round(nbGMoutPut['LSsort'] / nb_file, 4)
                varNbGMLSsort = sqrt(
                    sum(map(lambda x: x * x - avgNbGMLSsort * avgNbGMLSsort, listNbGMLSsort)) / nb_file)

                writerTimes.writerow({'File': f1, 'Gamma': gamma,
                                      'V': round(timesOutPut['V'] / nb_file, 4),
                                      'T': round(timesOutPut['T'] / nb_file, 4),
                                      'E': round(timesOutPut['E'] / nb_file, 4),
                                      'G_Edges': round(timesOutPut['G_Edges'] / nb_file, 4),
                                      'BBR19': round(timesOutPut['BBR19'] / nb_file, 4),
                                      'LS': round(timesOutPut['LS'] / nb_file, 4),
                                      'LSsort': round(timesOutPut['LSsort'] / nb_file, 4),
                                      'DC': round(timesOutPut['DC'] / nb_file, 4),
                                      'varNbGMTLS': round(varNbGMTLS, 4),
                                      'varNbGMTDC': round(varNbGMTDC, 4),
                                      'varNbGMTBBR19': round(varNbGMTBBR19, 4),
                                      'varNbGMTLSsort': round(varNbGMTLSsort, 4)})

                writerNbGM.writerow({'File': f1, 'Gamma': gamma,
                                     'V': round(nbGMoutPut['V'] / nb_file, 4),
                                     'T': round(nbGMoutPut['T'] / nb_file, 4),
                                     'E': round(nbGMoutPut['E'] / nb_file, 4),
                                     'V_living': round(nbGMoutPut['V_living'] / nb_file, 4),
                                     'G_Edges': round(nbGMoutPut['G_Edges'] / nb_file, 4),
                                     'BBR19': round(nbGMoutPut['BBR19'] / nb_file, 4),
                                     'LS': round(nbGMoutPut['LS'] / nb_file, 4),
                                     'LSsort': round(nbGMoutPut['LSsort'] / nb_file, 4),
                                     'DC': round(nbGMoutPut['DC'] / nb_file, 4),
                                     'varNbGMLS': round(varNbGMLS, 4),
                                     'varNbGMDC': round(varNbGMDC, 4),
                                     'varNbGMBBR19': round(varNbGMBBR19, 4),
                                     'varNbGMLSsort': round(varNbGMLSsort, 4)})


main()
