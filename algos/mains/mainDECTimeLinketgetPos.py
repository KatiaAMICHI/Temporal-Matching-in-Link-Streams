import csv
import time

from algos.mainClass.DEC import *

gamma = 2


def tocsvForeachDir():
    pathF1 = '../res'
    fileOutPutTimes = '../outPutFile/DEC/TimesDECQuiManqueG2.csv'

    pathResult = '../outPutFile/DEC/resultTimesDECQuiManqueG2'  # on écrit tt les données pour le calcule de la variance

    csv_Times = open(fileOutPutTimes, mode='w')

    fieldnamesTimes = ['File', 'Gamma', 'end_time_ListPos']
    writerTimes = csv.DictWriter(csv_Times, fieldnames=fieldnamesTimes)
    writerTimes.writeheader()

    timesOutPut = {'end_time_ListPos': 0}

    for f1 in os.listdir(pathF1):
        pathF2 = pathF1 + "/" + f1
        nb_file = 0

        if 'gen_B1' not in pathF2:
            continue

        fileResult = pathResult + f1
        csv_result = open(fileResult, mode='w')
        fieldnamesResult = ['File', "Gamma", 'end_time_ListPos']
        writerResult = csv.DictWriter(csv_result, fieldnames=fieldnamesResult)
        writerResult.writeheader()

        for f2 in os.listdir(pathF2):
            path = pathF2 + "/" + f2 + "/"

            if os.path.isdir(path):

                for file in os.listdir(path):
                    if file.endswith('.nb_matching'):
                        print("******************************", f2, "******************************")

                        start_time = time.time()
                        dec = DecomposeGreedy()
                        dec.get_list_pos_matching(path + file)
                        end_time_ListPos = round(time.time() - start_time, 4)

                        timesOutPut['end_time_ListPos'] += end_time_ListPos

                fileOutPutResult = f2

                writerResult.writerow({'File': fileOutPutResult, "Gamma": gamma,
                                       'end_time_ListPos': end_time_ListPos})

        # ecriture dans le outPutFile a la fin de chaque parcour d'un dossier
        print()
        print("je vais écrir !!")

        writerTimes.writerow({'File': f1, 'Gamma': gamma,
                              "end_time_ListPos": round(timesOutPut['end_time_ListPos'] / nb_file, 4)})


tocsvForeachDir()
