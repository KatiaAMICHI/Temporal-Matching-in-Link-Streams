import os
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import sqrt

gamma = 2
path = 'Result'


# base = 'enron'


def autolabel(ax, rects, percentage=False):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = int(rect.get_height())
        if height < 1:
            continue
        value = height
        if percentage:
            value = str(height) + '%'

        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * int(height),
                value,
                ha='center', va='bottom')


def plot1_2Results(title, ylabel, data, var=True, path='', percentage=False):
    # ('BBR19', 'LS', 'DC')

    n_groups = 4

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.15

    opacity = 0.3
    error_config = {'ecolor': '0.3'}

    print(data["Rollernet_var"])
    if not var:
        data["Enron_var"] = 0
        data["Rollernet_var"] = 0
        data["B1_var"] = 0
        data["B2_var"] = 0

    rects1 = plt.bar(index - bar_width, data["Enron"], bar_width,
                     alpha=opacity,
                     color='b',
                     yerr=data["Enron_var"],
                     error_kw=error_config,
                     label='ExtractEnron')

    rects2 = plt.bar(index, data["Rollernet"], bar_width,
                     alpha=opacity,
                     color='r',
                     yerr=data["Rollernet_var"],
                     error_kw=error_config,
                     label='ExtractRollernet')

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

    plt.xlabel('Algorithms')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(index + bar_width / 2, ('BBR19', 'LS', 'LSsort', 'DC'))
    plt.legend()

    plt.tight_layout()

    if 'Size of γ-matching' in title:
        plt.ylim(0, 750)
        plt.xlim(-1, 5)
    if percentage:
        plt.ylim(0, 100)
        plt.xlim(-1, 5.5)
        autolabel(ax, rects1, percentage)
        autolabel(ax, rects2, percentage)
        autolabel(ax, rects3, percentage)
        autolabel(ax, rects4, percentage)

    plt.savefig('../png/' + path + title.replace(' ', '_').replace('γ', 'G') + '.png')

    plt.show()


def main1():
    fileT = '../Results/datasetTG' + str(gamma) + '.csv'
    fileNB = '../Results/datasetNBG' + str(gamma) + '.csv'

    dataT = pd.read_csv(fileT)
    dataNB = pd.read_csv(fileNB)

    dataTimes = {"Enron": (dataT['BBR19'][0], dataT['LS'][0], dataT['LSsort'][0], dataT['DC'][0]),
                 "Enron_var": (
                     dataT['varNbGMTBBR19'][0] * sqrt(1000),
                     0.0,
                     dataT['varNbGMTLSsort'][0] * sqrt(1000),
                     dataT['varNbGMTDC'][0] * sqrt(1000)),
                 "Rollernet": (dataT['BBR19'][1], dataT['LS'][1], dataT['LSsort'][1], dataT['DC'][1]),
                 "Rollernet_var": (
                     dataT['varNbGMTBBR19'][1] * sqrt(1000),
                     0.0,
                     dataT['varNbGMTLSsort'][1] * sqrt(1000),
                     dataT['varNbGMTDC'][1] * sqrt(1000)),

                 "B1": (dataT['BBR19'][2], dataT['LS'][2], dataT['LSsort'][2], dataT['DC'][2]),
                 "B1_var": (
                     dataT['varNbGMTBBR19'][2] * sqrt(1000),
                     0.0,
                     dataT['varNbGMTLSsort'][2] * sqrt(1000),
                     dataT['varNbGMTDC'][2] * sqrt(1000)),

                 "B2": (dataT['BBR19'][3], dataT['LS'][3], dataT['LSsort'][3], dataT['DC'][3]),
                 "B2_var": (
                     dataT['varNbGMTBBR19'][3] * sqrt(1000),
                     0.0,
                     dataT['varNbGMTLSsort'][3] * sqrt(1000),
                     dataT['varNbGMTDC'][3] * sqrt(1000))}

    dataNbGM = {"Enron": (dataNB['BBR19'][0], dataNB['LS'][0], dataNB['LSsort'][0], dataNB['DC'][0]),
                "Enron_var": (
                    dataNB['varNbGMBBR19'][0] * sqrt(1000),
                    0.0,
                    dataNB['varNbGMLSsort'][0] * sqrt(1000),
                    dataNB['varNbGMDC'][0] * sqrt(1000)),
                "Rollernet": (dataNB['BBR19'][1], dataNB['LS'][1], dataNB['LSsort'][1], dataNB['DC'][1]),
                "Rollernet_var": (
                    dataNB['varNbGMBBR19'][1] * sqrt(1000),
                    0.0,
                    dataNB['varNbGMLSsort'][1] * sqrt(1000),
                    dataNB['varNbGMDC'][1] * sqrt(1000)),

                "B1": (dataNB['BBR19'][2], dataNB['LS'][2], dataNB['LSsort'][2], dataNB['DC'][2]),
                "B1_var": (
                    dataNB['varNbGMBBR19'][2] * sqrt(1000),
                    0.0,
                    dataNB['varNbGMLSsort'][2] * sqrt(1000),
                    dataNB['varNbGMDC'][2] * sqrt(1000)),

                "B2": (dataNB['BBR19'][3], dataNB['LS'][3], dataNB['LSsort'][3], dataNB['DC'][3]),
                "B2_var": (
                    dataNB['varNbGMBBR19'][3] * sqrt(1000),
                    0.0,
                    dataNB['varNbGMLSsort'][3] * sqrt(1000),
                    dataNB['varNbGMDC'][3] * sqrt(1000))}

    dataCoverRate = {"Enron": (
        dataNB['BBR19'][0] * gamma * 2 * 100 / dataNB['V_living'][0],
        dataNB['LS'][0] * gamma * 2 * 100 / dataNB['V_living'][0],
        dataNB['LSsort'][0] * gamma * 2 * 100 / dataNB['V_living'][0],
        dataNB['DC'][0] * gamma * 2 * 100 / dataNB['V_living'][0]),
        "Enron_var": (0.0, 0.0, 0.0, 0.0),

        "Rollernet": (dataNB['BBR19'][1] * gamma * 2 * 100 / dataNB['V_living'][1],
                      dataNB['LS'][1] * gamma * 2 * 100 / dataNB['V_living'][1],
                      dataNB['LSsort'][1] * gamma * 2 * 100 / dataNB['V_living'][1],
                      dataNB['DC'][1] * gamma * 2 * 100 / dataNB['V_living'][1]),
        "Rollernet_var": (0.0, 0.0, 0.0, 0.0),

        "B1": (dataNB['BBR19'][2] * gamma * 2 * 100 / dataNB['V_living'][2],
               dataNB['LS'][2] * gamma * 2 * 100 / dataNB['V_living'][2],
               dataNB['LSsort'][2] * gamma * 2 * 100 / dataNB['V_living'][2],
               dataNB['DC'][2] * gamma * 2 * 100 / dataNB['V_living'][2]),
        "B1_var": (0.0, 0.0, 0.0, 0.0),

        "B2": (dataNB['BBR19'][3] * gamma * 2 * 100 / dataNB['V_living'][3],
               dataNB['LS'][3] * gamma * 2 * 100 / dataNB['V_living'][3],
               dataNB['LSsort'][3] * gamma * 2 * 100 / dataNB['V_living'][3],
               dataNB['DC'][3] * gamma * 2 * 100 / dataNB['V_living'][3]),
        "B2_var": (0.0, 0.0, 0.0, 0.0)
    }

    # 1 plot results Times
    plot1_2Results("Result Time Execution  γ = " + str(gamma), "Times (s)", dataTimes, var=False, path='Discussion/')

    # 2 plot results NbGammaMatching
    plot1_2Results("Size of γ-matching with γ = " + str(gamma), "size of γ-matching", dataNbGM, var=False,
                   path='Discussion/')

    # 3
    coverRateOf_Edges()

    # 4 plot results Cover Rate
    plot1_2Results("Cover rate of vertices γ = " + str(gamma), "rate of vartices", dataCoverRate, var=False,
                   percentage=True, path='Discussion/')


def v2(title, ylabel, xlabel, x, yLS=None, yBBR19=None, yDC=None, yLSsort=None, log=False):
    size = [6] * len(x)

    if yLS:
        plt.scatter(x, yLS, s=size, c='blue', label='LS')
    if yBBR19:
        plt.scatter(x, yBBR19, s=size, c='red', label='BBR19')
    if yDC:
        plt.scatter(x, yDC, s=size, c='green', label='DC')
    if yLSsort:
        plt.scatter(x, yLSsort, s=size, c='m', label='LSsort')

    plt.legend()

    if log:
        plt.yscale('log')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    # plt.xlim(0, 1)
    plt.ylim(0, 500)
    plt.savefig('../png/' + title.replace(' ', '_') + '.png')

    plt.show()


def time_exect_algos_delta():
    # for evalution of number of gamma-edges with delta

    base = 'enron'
    EnronNBFilesG2 = '../Results/' + base + '/ResultsFilesNBG2.csv'
    EnronTimesFilesG2 = '../Results/' + base + '/ResultsFilesTimeG2.csv'

    file = EnronTimesFilesG2

    cmd = "awk -F',' '{print $1}' " + file + " |  sed -e \"s/" + base + "/$replace/g\" "
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
    ysLSsort = list(map(float, listData))

    cmd = "awk -F',' '{print $10}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysDC = list(map(float, listData))

    title = base + " execution time delta"
    ylabel = 'execution time(s)'
    xlabel = 'γ-edges'
    v2(title, ylabel, xlabel, xs, yLS=ysLS, yBBR19=ysBBBR19, yDC=ysDC, yLSsort=ysLSsort)


def time_exect_algos_g_edges():
    # for variation of execution time and gamm-edges

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
    print('LS : ', max(ysLS))

    cmd = "awk -F',' '{print $9}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysLSsort = list(map(float, listData))
    print("*** : ", max(ysLSsort))
    cmd = "awk -F',' '{print $10}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysDC = list(map(float, listData))

    title = base + " execution time"
    ylabel = 'execution time(s)'
    xlabel = 'γ-edges'
    v2(title, ylabel, xlabel, xs, yLS=ysLS, yBBR19=ysBBBR19, yDC=ysDC, yLSsort=ysLSsort)


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
    ysLSsort = list(map(float, listData))

    cmd = "awk -F',' '{print $11}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    print(listData)
    ysDC = list(map(float, listData))

    v2(titleE + " delta variation", 'number of γ−edges', 'δ−compression (s)', xs, yLS=ysLS, yBBR19=ysBBBR19, yDC=ysDC,
       yLSsort=ysLSsort)


def data_execution_time_LS(base):
    EnronTimesFilesG2 = '../Results/' + base + '/ResultsFilesTimeG2.csv'
    EnronNBFilesG2 = '../Results/' + base + '/ResultsFilesNBG2.csv'

    file = EnronTimesFilesG2

    cmd = "awk -F ',' {'print $6'} " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    xs = list(map(int, listData))

    cmd = "awk -F',' '{print $10}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    ysLS = list(map(float, listData))
    return xs, ysLS


def execution_time_LS():
    xE, yE = data_execution_time_LS('enron')
    xR, yR = data_execution_time_LS('rollernet')

    maxy = max(max(yE), max(yR))
    v2('Execution time LS (Enron)', 'time(s)', 'γ-edges', xE, yLS=yE, log=True)
    # v2('Execution time LS', 'time(s)', 'γ-edges', xR, yLS=yR, log=True)


def coverRateOf_Edges():
    base = 'B2'
    path = '../res/'

    fileT = '../Results/datasetTG' + str(gamma) + '.csv'
    fileNB = '../Results/datasetNBG' + str(gamma) + '.csv'

    dataT = pd.read_csv(fileT)
    dataNB = pd.read_csv(fileNB)

    results = defaultdict(int)

    for f1 in os.listdir(path):
        nb_file = 0
        pathF1 = path + f1 + '/'
        if os.path.isdir(pathF1):
            for f2 in os.listdir(pathF1):
                pathF2 = pathF1 + f2 + '/'
                if os.path.isdir(pathF2):
                    for file in os.listdir(pathF2):
                        pathFile = pathF2 + file

                        if file.endswith('.nb_matchingNetworkx'):
                            nb_file += 1
                            cmd = "awk -F ' ' '{sum+=$1;}END{print sum;}' " + pathFile
                            results[f1] += int(os.popen(cmd).read())

            results[f1] /= nb_file
    print("results : ", results)

    dataNbGM = {"Enron": (dataNB['BBR19'][0] * gamma * 100 / results['gen_enron'],
                          dataNB['LS'][0] * gamma * 100 / results['gen_enron'],
                          dataNB['LSsort'][0] * gamma * 100 / results['gen_enron'],
                          dataNB['DC'][0] * gamma * 100 / results['gen_enron']),
                "Enron_var": (0.0, 0.0, 0.0, 0.0),
                "Rollernet": (dataNB['BBR19'][1] * gamma * 100 / results['gen_rollernet'],
                              dataNB['LS'][1] * gamma * 100 / results['gen_rollernet'],
                              dataNB['LSsort'][1] * gamma * 100 / results['gen_rollernet'],
                              dataNB['DC'][1] * gamma * 100 / results['gen_rollernet']),
                "Rollernet_var": (0.0, 0.0, 0.0, 0.0),
                "B1": (dataNB['BBR19'][2] * gamma * 100 / results['gen_B1'],
                       dataNB['LS'][2] * gamma * 100 / results['gen_B1'],
                       dataNB['LSsort'][2] * gamma * 100 / results['gen_B1'],
                       dataNB['DC'][2] * gamma * 100 / results['gen_B1']),
                "B1_var": (0.0, 0.0, 0.0, 0.0),
                "B2": (dataNB['BBR19'][3] * gamma * 100 / results['gen_B2'],
                       dataNB['LS'][3] * gamma * 100 / results['gen_B2'],
                       dataNB['LSsort'][3] * gamma * 100 / results['gen_B2'],
                       dataNB['DC'][3] * gamma * 100 / results['gen_B2']),
                "B2_var": (0.0, 0.0, 0.0, 0.0)}

    print(dataNbGM)
    # 2 plot results NbGammaMatching
    plot1_2Results("Cover rate of edges " + str(gamma), "rate of edges", dataNbGM, path='Discussion/', percentage=True)


main1()
# time_exect_algos_g_edges()
# gamma_edges_algos_delta()
# main3()
# execution_time_LS()
