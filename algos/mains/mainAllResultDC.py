import csv
import os
import time

from math import sqrt

from algos.mainClass.DC import DecomposeGreedy

def main():
    path = '../../res/'
    base = 'B1'

    # resultsTimes = '../../Results/' + base + '/DC/resultsTimesG10V2.csv'
    # csv_Times = open(resultsTimes, mode='w')
    # fieldnamesTimes = ["File", "Gamma", "DC", "varNbGMTDC"]
    # writerTimes = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimes)
    # writerTimes.writeheader()

    timesOutPut = {'V': 0, 'T': 0, 'E': 0, 'G_Edges': 0, 'BBR19': 0, 'LS': 0, 'LSsort': 0,
                   'DC': 0, 'varNbGMTLS': 0, 'varNbGMTDC': 0, 'varNbGMTBBR19': 0, 'varNbGMTLSsort': 0}

    # resultsNB = '../../Results/' + base + '/DC/resultsNBG10V2.csv'
    # csv_Times = open(resultsNB, mode='w')
    # fieldnamesNB = ["File", "Gamma", "DC", "varNbGMDC"]
    # writerNbGM = csv.DictWriter(csv_Times, fieldnames=fieldnamesNB)
    # writerNbGM.writeheader()

    nbGMoutPut = {'V': 0, 'T': 0, 'E': 0, 'V_living': 0, 'G_Edges': 0, 'BBR19': 0, 'LS': 0, 'LSsort': 0,
                  'DC': 0, 'varNbGMDC': 0}

    for gamma in range(2, 3):
        for f1 in os.listdir(path):
            nb_file = 0
            pathF1 = path + f1 + '/'
            if base not in pathF1:
                continue

            # fileResultNB = '../../Results/' + base + '/DC/ResultsFilesNBG10V2.csv'
            # csv_fileNB = open(fileResultNB, mode='w')
            # fieldnamesFilesNB = ["File", "Gamma", "DC"]
            # fwNB = csv.DictWriter(csv_fileNB, fieldnames=fieldnamesFilesNB)
            # fwNB.writeheader()
            #
            # fileResultTime = '../../Results/' + base + '/DC/ResultsFilesTimeG10V2.csv'
            # csv_fileTime = open(fileResultTime, mode='w')
            # fieldnamesFilesTime = ["File", "Gamma", "DC"]
            # fwT = csv.DictWriter(csv_fileTime, fieldnames=fieldnamesFilesTime)
            # fwT.writeheader()

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

                            if file.endswith('.nb_matching'):
                                print("******************************", gamma, f2, "******************************")
                                # V_living = SommetsVivant(pathFile)
                                nb_file += 1

                                # file = file.replace('linkstream', 'nb_matching')
                                #  pathFile = pathF2 + file

                                # DC
                                start_time = time.time()
                                # ça replace ce qu'il y a dans le fichier .nb_matchingAR
                                # results = getNbMatchingT(gamma, pathFile)
                                results = open(pathFile, 'r').readlines()

                                DC = DecomposeGreedy(gamma)
                                list_pos_matching = DC.get_list_pos_matching_from_list(results)
                                nb_gmDC, M = DC.nb_gamma_matching_decomposition(list_pos_matching, nb_matching=0,
                                                                                M=[])
                                timeDC = round(time.time() - start_time, 4)

                                listNbGMDC.append(nb_gmDC)
                                listNbGMTimeDC.append(timeDC)

                                timesOutPut['DC'] += timeDC

                                print({'File': f2, 'Gamma': gamma,
                                       'DC': timeDC})

                                nbGMoutPut['DC'] += nb_gmDC

                                print({'File': f2, 'Gamma': gamma,
                                       'DC': nb_gmDC})

                # ecriture dans le outPutFile a la fin de chaque parcour d'un dossier
                print()
                print("je vais écrir !!", nb_file)

                # calcule de l'écart type
                # DC
                avgNbGMTimeDC = round(timesOutPut['DC'] / nb_file, 4)
                varNbGMTDC = sqrt(
                    sum(map(lambda x: x * x - avgNbGMTimeDC * avgNbGMTimeDC, listNbGMTimeDC)) / nb_file)

                avgNbGMDC = round(nbGMoutPut['DC'] / nb_file, 4)
                varNbGMDC = sqrt(sum(map(lambda x: x * x - avgNbGMDC * avgNbGMDC, listNbGMDC)) / nb_file)

                print({'File': f1, 'Gamma': gamma,
                       'DC': round(timesOutPut['DC'] / nb_file, 4),
                       'varNbGMTDC': round(varNbGMTDC, 4)})

                print({'File': f1, 'Gamma': gamma,
                       'DC': round(nbGMoutPut['DC'] / nb_file, 4),
                       'varNbGMDC': round(varNbGMDC, 4)})


main()
