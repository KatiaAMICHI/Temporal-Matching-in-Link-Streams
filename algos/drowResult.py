"""
Bar chart demo with pairs of bars grouped for easy comparison.
"""
import os

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import csv, pprint
import pandas as pd

gamma = 2

path = 'Result'

base = 'enron'

fileT = '../Results/datasetTG2.csv'
fileNB = '../Results/datasetNBG2.csv'

dataT = pd.read_csv(fileT)
dataNB = pd.read_csv(fileNB)


def plot1_2Results(title, ylabel, data):
    # ('BBR19', 'LS', 'DEC')

    n_groups = 4

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.15

    opacity = 0.3
    error_config = {'ecolor': '0.3'}

    rects1 = plt.bar(index - bar_width, data["Enron"], bar_width,
                     alpha=opacity,
                     color='b',
                     yerr=data["Enron_var"],
                     error_kw=error_config,
                     label='GenEnron')

    rects2 = plt.bar(index, data["Rollernet"], bar_width,
                     alpha=opacity,
                     color='r',
                     yerr=data["Rollernet_var"],
                     error_kw=error_config,
                     label='GenRollernet')

    rects3 = plt.bar(index + bar_width, data["B1"], bar_width,
                     alpha=opacity,
                     color='g',
                     yerr=data["B1_var"],
                     error_kw=error_config,
                     label='B1')

    rects4 = plt.bar(index + 2 * bar_width, data["B2"], bar_width,
                     alpha=opacity,
                     color='m',
                     yerr=data["B2_var"],
                     error_kw=error_config,
                     label='B2')

    plt.xlabel('Algos')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(index + bar_width / 2, ('BBR19', 'LS', 'LSAR', 'DEC'))
    plt.legend()

    plt.tight_layout()
    plt.show()


def main1(dataT, dataNB):
    dataTimes = {"Enron": (dataT['BBR19'][0], dataT['LS'][0], dataT['LSAR'][0], dataT['DEC'][0]),
                 "Enron_var": (
                     dataT['varNbGMTBBR19'][0], dataT['varNbGMTLS'][0], dataT['varNbGMTLSAR'][0],
                     dataT['varNbGMTDEC'][0]),
                 "Rollernet": (dataT['BBR19'][1], dataT['LS'][1], dataT['LSAR'][1], dataT['DEC'][1]),
                 "Rollernet_var": (
                     dataT['varNbGMTBBR19'][1], dataT['varNbGMTLS'][1], dataT['varNbGMTLSAR'][1],
                     dataT['varNbGMTDEC'][1]),

                 "B1": (dataT['BBR19'][2], dataT['LS'][2], dataT['LSAR'][2], dataT['DEC'][2]),
                 "B1_var": (
                     dataT['varNbGMTBBR19'][2], dataT['varNbGMTLS'][2], dataT['varNbGMTLSAR'][2],
                     dataT['varNbGMTDEC'][2]),

                 "B2": (dataT['BBR19'][3], dataT['LS'][3], dataT['LSAR'][3], dataT['DEC'][3]),
                 "B2_var": (
                     dataT['varNbGMTBBR19'][3], dataT['varNbGMTLS'][3], dataT['varNbGMTLSAR'][3],
                     dataT['varNbGMTDEC'][3])}

    dataNbGM = {"Enron": (dataNB['BBR19'][0], dataNB['LS'][0], dataNB['LSAR'][0], dataNB['DEC'][0]),
                "Enron_var": (
                    dataNB['varNbGMBBR19'][0], dataNB['varNbGMLS'][0], dataNB['varNbGMLSAR'][0],
                    dataNB['varNbGMDEC'][0]),
                "Rollernet": (dataT['BBR19'][1], dataNB['LS'][1], dataNB['LSAR'][1], dataNB['DEC'][1]),
                "Rollernet_var": (
                    dataNB['varNbGMBBR19'][1], dataNB['varNbGMLS'][1], dataNB['varNbGMLSAR'][1],
                    dataNB['varNbGMDEC'][1]),

                "B1": (dataNB['BBR19'][2], dataNB['LS'][2], dataNB['LSAR'][2], dataNB['DEC'][2]),
                "B1_var": (
                    dataNB['varNbGMBBR19'][2], dataNB['varNbGMLS'][2], dataNB['varNbGMLSAR'][2],
                    dataNB['varNbGMDEC'][2]),

                "B2": (dataNB['BBR19'][3], dataNB['LS'][3], dataNB['LSAR'][3], dataNB['DEC'][3]),
                "B2_var": (
                    dataNB['varNbGMBBR19'][3], dataNB['varNbGMLS'][3], dataNB['varNbGMLSAR'][3],
                    dataNB['varNbGMDEC'][3])}

    dataCoverRate = {"Enron": (
        dataNB['BBR19'][0] * gamma * 2 * 100 / dataNB['V_living'][0],
        dataNB['LS'][0] * gamma * 2 * 100 / dataNB['V_living'][0],
        dataNB['LSAR'][0] * gamma * 2 * 100 / dataNB['V_living'][0],
        dataNB['DEC'][0] * gamma * 2 * 100 / dataNB['V_living'][0]),
        "Enron_var": (0.0, 0.0, 0.0, 0.0),

        "Rollernet": (dataNB['BBR19'][1] * gamma * 2 * 100 / dataNB['V_living'][1],
                      dataNB['LS'][1] * gamma * 2 * 100 / dataNB['V_living'][1],
                      dataNB['LSAR'][1] * gamma * 2 * 100 / dataNB['V_living'][1],
                      dataNB['DEC'][1] * gamma * 2 * 100 / dataNB['V_living'][1]),
        "Rollernet_var": (0.0, 0.0, 0.0, 0.0),

        "B1": (dataNB['BBR19'][2] * gamma * 2 * 100 / dataNB['V_living'][2],
               dataNB['LS'][2] * gamma * 2 * 100 / dataNB['V_living'][2],
               dataNB['LSAR'][2] * gamma * 2 * 100 / dataNB['V_living'][2],
               dataNB['DEC'][2] * gamma * 2 * 100 / dataNB['V_living'][2]),
        "B1_var": (0.0, 0.0, 0.0, 0.0),

        "B2": (dataNB['BBR19'][3] * gamma * 2 * 100 / dataNB['V_living'][3],
               dataNB['LS'][3] * gamma * 2 * 100 / dataNB['V_living'][3],
               dataNB['LSAR'][3] * gamma * 2 * 100 / dataNB['V_living'][3],
               dataNB['DEC'][3] * gamma * 2 * 100 / dataNB['V_living'][3]),
        "B2_var": (0.0, 0.0, 0.0, 0.0)
    }

    # 1 plot results Times
    plot1_2Results("Result Time Execution", "Times (s)", dataTimes)

    # 2 plot results NbGammaMatching
    plot1_2Results("Result Nb Gamma Matching", "NbGammaMatching", dataNbGM)

    # 4 plot results Cover Rate
    plot1_2Results("Result Nb vertices cover rate", "NbVertices (%)", dataCoverRate)


def v2(title, ylabel,xlabel, x, yLS=None, yBBR19=None, yDEC=None, yLSAR=None):
    size = [6] * len(x)

    if yLS:
        plt.scatter(x, yLS, s=size, c='green', label='LS')
    if yBBR19:
        plt.scatter(x, yBBR19, s=size, c='red', label='BBR19')
    if yDEC:
        plt.scatter(x, yDEC, s=size, c='blue', label='DEC')
    if yLSAR:
        plt.scatter(x, yLSAR, s=size, c='m', label='LSAR')

    plt.legend()

    # plt.yscale('log')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig('../png/' + title + '.png')

    plt.show()


def time_exect_algos_delta():
    # for evalution of number of gamma-edges with delta

    base = 'enron'
    EnronNBFilesG2 = '../Results/' + base + '/ResultsFilesNBG2.csv'
    EnronTimesFilesG2 = '../Results/' + base + '/ResultsFilesTimeG2.csv'

    file = EnronTimesFilesG2

    cmd = "awk -F',' '{print $1}' " + file + " |  sed -e \"s/" + base +"/$replace/g\" "
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    xs = list(map(float, listData))

    cmd = "awk -F',' '{print $7}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysBBBR19 = list(map(float, listData))

    cmd = "awk -F',' '{print $8}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysLS = list(map(float, listData))

    cmd = "awk -F',' '{print $9}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysLSAR = list(map(float, listData))

    cmd = "awk -F',' '{print $10}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysDEC = list(map(float, listData))

    title = base + " execution time delta"
    ylabel = 'execution time(s)'
    xlabel = 'γ-edges'
    v2(title, ylabel,xlabel, xs, yLS=ysLS, yBBR19=ysBBBR19, yDEC=ysDEC, yLSAR=ysLSAR)


def time_exect_algos_g_edges():
    # for evalution of number of gamma-edges with delta

    base = 'rollernet'
    EnronNBFilesG2 = '../Results/' + base + '/ResultsFilesNBG2.csv'
    EnronTimesFilesG2 = '../Results/' + base + '/ResultsFilesTimeG2.csv'

    file = EnronTimesFilesG2

    cmd = "awk -F ',' {'print $6'} " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    xs = list(map(float, listData))

    cmd = "awk -F',' '{print $7}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysBBBR19 = list(map(float, listData))

    cmd = "awk -F',' '{print $8}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysLS = list(map(float, listData))

    cmd = "awk -F',' '{print $9}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysLSAR = list(map(float, listData))

    cmd = "awk -F',' '{print $10}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysDEC = list(map(float, listData))

    title = base + " execution time"
    ylabel = 'execution time(s)'
    xlabel = 'γ-edges'
    v2(title, ylabel,xlabel, xs, yLS=ysLS, yBBR19=ysBBBR19, yDEC=ysDEC, yLSAR=ysLSAR)


def gamma_edges_algos_delta():
    # for evalution of number of gamma-edges with delta
    EnronG2 = '../outPutFileHp/outPutFile/enron400/resultEnronG2Sort'
    RollernetG2 = '../outPutFileHp/outPutFile/rollernet/resultRollernetG2'
    enronOrigin = [0, 7]  # time, G-edges
    rollernetOrigin = [0, 43]  # time, G-edges
    titleE = "Enron"
    titleR = "Rollernet"

    # plot evalution of execution time for finding gamma-matching and number gamma-edges

    EnronTimesFilesG2 = '../Results/enron/ResultsFilesTimeG2.csv'

    EnronNBFilesG2 = '../Results/enron/ResultsFilesNBG2.csv'

    file = EnronNBFilesG2

    cmd = "awk -F ',' {'print $7'} " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    xs = list(map(int, listData))

    cmd = "awk -F',' '{print $8}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysBBBR19 = list(map(float, listData))

    cmd = "awk -F',' '{print $9}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysLS = list(map(float, listData))

    cmd = "awk -F',' '{print $10}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysLSAR = list(map(float, listData))

    cmd = "awk -F',' '{print $11}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysDEC = list(map(float, listData))

    v2(titleE + " delta variation", 'number of γ−edges', 'δ−compression (s)', xs, yLS=ysLS, yBBR19=ysBBBR19, yDEC=ysDEC, yLSAR=ysLSAR)


def plot3(xBBR19, yBBR19, xLS, yLS, xLSAR, yLSAR, xDEC, yDEC):
    # LS
    # (markerLines, stemLines, baseLines) = plt.stem(xLS, yLS, use_line_collection=True)
    # plt.setp(markerLines, color='red', markeredgewidth=3)
    # plt.setp(stemLines, color='red', linewidth=3, linestyle='dashdot')
    # plt.setp(baseLines, color='black', linewidth=2, linestyle='dashed')
    # plt.margins(0.1, 0.1)
    #
    # # LSAR
    # (markerLines, stemLines, baseLines) = plt.stem(xLSAR, yLSAR, use_line_collection=True)
    # plt.setp(markerLines, color='blue', markeredgewidth=3)
    # plt.setp(stemLines, color='blue', linewidth=3, linestyle='dashdot')
    # plt.setp(baseLines, color='black', linewidth=2, linestyle='dashed')
    # plt.margins(0.1, 0.1)

    # DEC
    (markerLines, stemLines, baseLines) = plt.stem(xDEC, yDEC, use_line_collection=True)
    plt.setp(markerLines, color='green', markeredgewidth=3)
    plt.setp(stemLines, color='green', linewidth=3, linestyle='dashdot')
    plt.setp(baseLines, color='black', linewidth=2, linestyle='dashed')

    # # BBR19
    # (markerLines, stemLines, baseLines) = plt.stem(xBBR19, yBBR19, use_line_collection=True)
    # plt.setp(markerLines, color='red', markeredgewidth=3)
    # plt.setp(stemLines, color='red', linewidth=3, linestyle='dashdot')

    plt.margins(0.1, 0.1)
    plt.title('stem avec configuration detaillee')
    plt.ylabel('valeurs')
    plt.show()


def main3():
    pathRoot = '../res'

    result3LS = {'enron': defaultdict(int), 'rollernet': defaultdict(int), 'B1': defaultdict(int),
                 'B2': defaultdict(int)}
    result3BBR19 = {'enron': defaultdict(int), 'rollernet': defaultdict(int), 'B1': defaultdict(int),
                    'B2': defaultdict(int)}
    result3LSAR = {'enron': defaultdict(int), 'rollernet': defaultdict(int), 'B1': defaultdict(int),
                   'B2': defaultdict(int)}
    result3DEC = {'enron': defaultdict(int), 'rollernet': defaultdict(int), 'B1': defaultdict(int),
                  'B2': defaultdict(int)}

    for f in os.listdir(pathRoot):
        if not os.path.isdir(pathRoot + '/' + f):
            continue
        for fileIn in os.listdir(pathRoot + '/' + f):
            if os.path.isdir(pathRoot + '/' + f + '/' + fileIn):
                continue

            base = fileIn.split('Max')[0]
            path = '../Results/' + base + '/'

            for file in os.listdir(path):
                if 'BBR19' in file:
                    fr = open(path + file, 'r')
                    for line in fr.readlines():
                        t, nb = map(float, line.split(','))
                        result3BBR19[base][t] = nb

                    fr = open(pathRoot + '/' + f + '/' + fileIn, 'r')
                    for line in fr.readlines():
                        t, nb = map(float, line.split(','))
                        result3BBR19[base][t] /= nb

                elif 'LSAR' in file:
                    fr = open(path + file, 'r')
                    for line in fr.readlines():
                        t, nb = map(float, line.split(','))
                        result3LSAR[base][t] = nb
                    fr = open(pathRoot + '/' + f + '/' + fileIn, 'r')
                    for line in fr.readlines():
                        t, nb = map(float, line.split(','))
                        result3LSAR[base][t] /= nb

                elif 'LS' in file:
                    fr = open(path + file, 'r')
                    for line in fr.readlines():
                        t, nb = map(float, line.split(','))
                        result3LS[base][t] = nb
                    fr = open(pathRoot + '/' + f + '/' + fileIn, 'r')
                    for line in fr.readlines():
                        t, nb = map(float, line.split(','))
                        result3LS[base][t] /= nb

                elif 'DEC' in file:
                    fr = open(path + file, 'r')
                    for line in fr.readlines():
                        t, nb = map(float, line.split(','))
                        result3DEC[base][t] = nb
                    fr = open(pathRoot + '/' + f + '/' + fileIn, 'r')
                    for line in fr.readlines():
                        t, nb = map(float, line.split(','))
                        result3DEC[base][t] *= 100 / nb

    xBBR19 = result3BBR19['enron'].keys()  # le temps
    yBBR19 = result3BBR19['enron'].values()  # les valeurs

    xLS = result3LS['enron'].keys()  # le temps
    yLS = result3LS['enron'].values()  # les valeurs

    xLSAR = result3LSAR['enron'].keys()  # le temps
    yLSAR = result3LSAR['enron'].values()  # les valeurs

    xDEC = result3DEC['enron'].keys()  # le temps
    yDEC = result3DEC['enron'].values()  # les valeurs

    pprint.pprint(result3DEC['enron'].items())

    plot3(xBBR19, yBBR19, xLS, yLS, xLSAR, yLSAR, xDEC, yDEC)


# main1(dataT, dataNB)
time_exect_algos_g_edges()
# gamma_edges_algos_delta()
# main3()
