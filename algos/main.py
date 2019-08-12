import os
import time

from algos.greedy_algorithm import Matching
from algos.greedy_algorithmV2 import MatchingV2
from algos.algoN import MatchingN

import csv

gamma = 2
path_enron = "../res/enron/test_enron/"
path_rollernet = "../res/rollernet/test_rollernet/"


def tocsv():
    with open('../outPutFile/file2.csv', mode='w') as csv_file:
        fieldnames = ['File', '|V|', '|T|', '|E|', 'E_gamma', 'ARgreedyA', 'greedyA', 'algoN']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for path in path_rollernet, path_enron:
            print("path : ", path)
            for file in os.listdir(path):
                # greedy algo V22 AR
                # if file.endswith('_sort'):
                #
                #     g_mV2 = MatchingV2(gamma, path + file)
                #     link_stream = g_mV2.linkStream()
                #     print("L : ( V:", link_stream["V"], ", T:", link_stream["T"], ", E:", len(link_stream["E"]), ")")
                #
                #     g_edges = g_mV2.gamma_edges(link_stream, gamma)
                #
                #     min_M = len(link_stream["E"])
                #     max_M = -1
                #
                #     start_time = time.time()
                #     M = g_mV2.greedy_gamma_matching(g_edges, gamma)
                #     end_time_ar = time.time() - start_time
                #
                #     print("max : ", max_M, "   min : ", min_M)
                #     print("g_edges::: ", g_edges)
                # else:

                print("file : ", file)

                # greedy algo
                g_m = Matching(gamma, path + file)
                link_stream = g_m.linkStream()
                start_time = time.time()
                M = g_m.gammaMatching(link_stream, gamma)
                end_time = time.time() - start_time

                # algo with neighbour
                g_m_n = MatchingN(gamma, path + file)
                link_streamList = g_m_n.linkStreamList()
                E_gamma = g_m_n.E_gammaMatching(link_streamList, gamma)
                start_time = time.time()
                MN = g_m_n.gammaMatchingE_gamma_avancer(E_gamma, gamma)
                end_time_n = time.time() - start_time

                print("je vais écrir !!")
                print({'File': file, '|V|': link_stream["V"], '|T|': link_stream["T"], '|E|': len(link_stream["E"]),
                       'E_gamma': len(E_gamma),
                       "ARgreedyA": 0, "greedyA": round(end_time, 2), "algoN": round(end_time_n, 2)})

                writer.writerow(
                    {'File': file, '|V|': link_stream["V"], '|T|': link_stream["T"], '|E|': len(link_stream["E"]),
                     'E_gamma': len(E_gamma),
                     "ARgreedyA": 0, "greedyA": round(end_time, 2), "algoN": round(end_time_n, 2)})


def main():
    for file in os.listdir(path_enron):
        print("\n.................................", file, ".................................")
        g_m = Matching(gamma, path_enron + file)

        print("****************** testing link_stream method ******************")
        link_stream = g_m.linkStream()
        print("L : ( V:", link_stream["V"], ", T:", link_stream["T"], ", E:", len(link_stream["E"]), ")")
        print()

        print("************************ gamma_matching ************************")
        start_time = time.time()
        M = g_m.gammaMatching(link_stream, gamma)
        print("Temps d execution gamma_matching : %s secondes ---" % (time.time() - start_time))
        print("algo - max_matching: ", M["max_matching"])

    for file in os.listdir(path_rollernet):
        print("\n.................................", file, ".................................")
        g_m = Matching(gamma, path_rollernet + file)

        print("****************** testing link_stream method ******************")
        start_time = time.time()
        link_stream = g_m.linkStream()
        print("Temps d execution link_stream : %s secondes ---" % (time.time() - start_time))
        print("L : ( V:", link_stream["V"], ", T:", link_stream["T"], ", E:", len(link_stream["E"]), ")")
        print()

        print("************************ gamma_matching ************************")
        start_time = time.time()
        M = g_m.gammaMatching(link_stream, gamma)
        print("Temps d execution gamma_matching : %s secondes ---" % (time.time() - start_time))
        print("algo - max_matching: ", M["max_matching"])

    print("\nFIN")


if __name__ == '__main__':
    tocsv()
