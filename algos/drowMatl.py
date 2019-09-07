"""
Bar chart demo with pairs of bars grouped for easy comparison.
"""
import os

import numpy as np
import matplotlib.pyplot as plt

gamma = 2


def plot1_2Results(title, ylabel, data):
    # ('BBR19', 'LS', 'DEC')

    n_groups = 3

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
    plt.xticks(index + bar_width / 2, ('BBR19', 'LS', 'DEC'))
    plt.legend()

    plt.tight_layout()
    plt.show()


def main1():
    # TIME
    # "Rollernet_var": (27.9226, 212.6308, 0.0),
    # "B1_var": (0.1253, 1202.1945, 0.0),
    #             "B2_var": (0.4573, 1410.2809, 0.0)}

    # NB
    #             "Rollernet_var": (1344.3931, 1676.9743, 0.0),

    # ('BBR19', 'LS', 'DEC')
    dataTimes = {"Enron": (0.0235 + 0.0043 + 0.0844, 0.0235 + 3.0556 + 0.1251, 0.0),
                 "Enron_var": (0.1224, 3.7058, 4),
                 "Rollernet": (3.003 + 0.0425 + 3.4138, 3.003 + 75.0334 + 5.3638, 0.0),
                 "Rollernet_var": (27.9226, 212.6308, 0.0),

                 "B1": (0.1163 + 0.0071 + 0.0844, 0.1163 + 65.6036 + 0.0955, 0.0842287 + 0.0396),
                 "B1_var": (0.1253, 1202.1945, 0.0229),

                 "B2": (0.0822 + 0.0369 + 0.7149, 0.0822 + 103.125 + 4.04443, 0.0),
                 "B2_var": (0.4573, 0.0, 0.0)}

    dataNbGM = {"Enron": (277.763, 345.072, 0.0),
                "Enron_var": (234.8343, 268.7305, 0.0),

                "Rollernet": (565.132, 696.716, 0.0),
                "Rollernet_var": (1344.3931, 53.026, 0.0),

                "B1": (607.7225, 612.6278, 836.4656),
                "B1_var": (365.0174, 367.1667, 312.0858),

                "B2": (300.78, 353.3584, 0.0),
                "B2_var": (78.4839, 96.0719, 0.0)}

    dataCoverRate = {"Enron": (
        277.763 * gamma * 2 * 100 / 2548.086, 345.072 * gamma * 2 * 100 / 2548.086, 0.0 * gamma * 2 * 100 / 2548.086),
        "Enron_var": (0.0, 0.0, 0.0),

        "Rollernet": (565.132 * gamma * 2 * 100 / 3266.58, 696.716 * gamma * 2 * 100 / 3266.58,
                      0.0 * gamma * 2 * 100 / 3266.58),
        "Rollernet_var": (0.0, 0.0, 0.0),

        "B1": (
            607.7225 * gamma * 2 * 100 / 25708.1915,
            612.6278 * gamma * 2 * 100 / 25708.1915,
            836.4656 * gamma * 2 * 100 / 25708.1915),
        "B1_var": (0.0, 0.0, 0.0),

        "B2": (300.78 * gamma * 2 * 100 / 1442.2153, 353.3584 * gamma * 2 * 100 / 1442.2153,
               0.0 * gamma * 2 * 100 / 1442.2153),
        "B2_var": (0.0, 0.0, 0.0)}

    # 1 plot results Times
    plot1_2Results("Result Time Execution", "Times (s)", dataTimes)

    # 2 plot results NbGammaMatching
    plot1_2Results("Result Nb Gamma Matching", "NbGammaMatching", dataNbGM)

    # 4 plot results Cover Rate
    plot1_2Results("Result Nb vertices cover rate", "NbVertices (%)", dataCoverRate)


def v2(title, x, y):
    size = [6] * len(x)

    plt.scatter(x, y, s=size, c='blue')

    plt.legend()

    plt.xlabel('δ−compression (s)')
    plt.ylabel('number of γ−edges')
    plt.title(title + " delta variation")
    plt.savefig('../png/'+title+'DeltaVariation.png')

    plt.show()


def main2():
    EnronG2 = '../outPutFileHp/outPutFile/enron400/resultEnronG2Sort'
    enronOrigin = [0, 7]  # time, G-edges
    titleE = "Enron"

    RollernetG2 = '../outPutFileHp/outPutFile/rollernet/resultRollernetG2'

    titleR = "Rollernet"

    file = EnronG2

    cmd = "awk -F',' '{print $1}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    xs = [0] + list(map(int, listData))

    cmd = "awk -F',' '{print $8}' " + file
    listData = os.popen(cmd).read().split('\n')[1::]
    del listData[-1]
    ys = [43] + list(map(int, listData))

    v2(titleE, xs, ys)


main1()
