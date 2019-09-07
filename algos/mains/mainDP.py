from algos.mains.main import *


def mainDP():
    path = "../res/gen_B1/test0001/"
    path = "../res/gen_test/test0000/"
    fileP = "test.position"

    if fileP.endswith('.position'):
        n, tmax, d, x, r = refactorData(path + fileP)
        dgGM = DpGammaMatching1D(n, tmax, d, x, r)

        nb_gmDP = dgGM.gammaMatchig1DSort()
        print("nb_gmDP : ", nb_gmDP)


def mainLS():
    path = "../res/gen_B1/test0001/"
    path = "../res/gen_test/test0000/"
    file = "test.linkstream"

    if file.endswith('.linkstream'):
        print("******************************", file, "******************************")
        # algo with neighbour LS

        g_m_n = MatchingN(gamma, path + file)
        link_streamList = g_m_n.linkStreamList()

        G_edges = g_m_n.G_edgesMatching(link_streamList, gamma)

        nb_gmLS = g_m_n.gammaMatchingG_edges_avancer(G_edges, gamma)
        print("nb_gmLS : ", nb_gmLS)


mainDP()
mainLS()

# n = 3
# tmax = 2
#
# x = numpy.zeros((n + 1, tmax + 1)).astype(int)
#
# lines = [[0, 1, 2], [4, 5, 6]]
# pprint.pprint(lines)
#
# j = 1
# for l in lines:
#     for i in range(1, n + 1):
#         x[i][j] = l[i-1]
#         pprint.pprint(x)
#     j += 1
# pprint.pprint(x)
