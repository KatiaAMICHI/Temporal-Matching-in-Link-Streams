import os, pprint, numpy
import collections
from functools import reduce

path = "./testbed/tests/"
gamma = 2


def dic_voisins(file):
    with open(path + file, 'r') as f:
        n, tmax, d = list(map(int, f.readline().split()))
        data_voisins = collections.defaultdict(list)
        data_file = f.read().split('\n')

        for line in data_file:
            if line == '':
                continue
            t, u, v = list(map(int, line.split()))
            data_voisins.setdefault(str(t) + str(u), []).append(v)
            data_voisins.setdefault(str(t) + str(v), []).append(u)

        pprint.pprint(data_voisins)
    return data_file, data_voisins


def linkStreamToPosition():
    for file in os.listdir(path):

        file = r"test0008.linkstream"

        file_output = path + file.replace(".linkstream", "linkstreamToPosition.position")

        if file.endswith('.linkstream'):
            print("************* ", file, "*************")
            data_file, data_voisins = dic_voisins(file)
            current_data_t = collections.defaultdict(list)
            with open(path + file, 'r') as f:
                with open(file_output, "+w") as f_outPut:
                    n, tmax, d = list(map(int, f.readline().split()))

                    f_outPut.write(str(n) + " " + str(tmax) + " " + str(d) + "\n")

                    last_t = 0
                    max_pos = -2
                    pos = list(range(-n, 0))

                    for line in f.readlines():
                        t, u, v = list(map(int, line.split()))
                        print("   *** t, u, v : ", t, u, v)
                        if last_t + 1 == t:
                            print("     je vais écrir !! ")
                            # chagement de t
                            pos = list(map(lambda x: x if x >= 0 else max_pos + gamma + 2 * n + x, pos))
                            print(">>> ", str(t - 1) + " " + str(pos) + "\n")
                            f_outPut.write(str(t - 1) + " " + str(pos) + "\n")
                            # pos = [-2] * int(n)
                            pos = list(range(-n * 2, 0, gamma))
                            max_pos = -2
                            current_data_t = collections.defaultdict()

                        if pos[u] < 0 and pos[v] >= 0:
                            tmp = u
                            u = v
                            v = tmp
                        if pos[u] < 0:
                            # u jamais vu :
                            pos[u] = max_pos + 2
                            pos[v] = pos[u]
                            current_data_t.setdefault(pos[u], []).append(u)
                            current_data_t.setdefault(pos[v], []).append(v)
                        else:
                            # u déja vu
                            oui = True
                            for v_u in zip(current_data_t[pos[u] - 1], current_data_t[pos[u]],
                                           current_data_t[pos[u + 1]]):
                                if v_u == v:
                                    continue
                                if v not in data_voisins[str(t) + str(v_u)]:
                                    oui = False
                                    break
                            if oui:
                                print("         oui")
                                try:
                                    current_data_t.setdefault(pos[v], []).remove(v)
                                except:
                                    pass
                                pos[v] = pos[u]
                                current_data_t.setdefault(pos[v], []).append(v)

                            else:
                                print("         non")
                                try:
                                    current_data_t.setdefault(pos[u], []).remove(u)
                                except:
                                    pass
                                pos[u] += 2
                                current_data_t.setdefault(pos[u], []).append(u)

                                while len(zip(current_data_t[pos[u] - 1], current_data_t[pos[u]],
                                              current_data_t[pos[u + 1]])) > 0:
                                    # for s in current_data_t[pos[u] - 2]:
                                    s = current_data_t[pos[u] - 2][0]
                                    current_data_t.setdefault(pos[u] - 2, []).remove(s)
                                    print("         1 pos[", s, "] : ", pos[s])
                                    pos[s] = pos[u] + 1
                                    print("         2 pos[", s, "] : ", pos[s])
                                    current_data_t.setdefault(pos[s], []).append(s)
                                    print("         2 current_data_t[pos[u] - 2] : ", current_data_t[pos[u] - 2])

                                try:
                                    current_data_t.setdefault(pos[v], []).remove(v)
                                except:
                                    pass

                                pos[v] = pos[u] - 1
                                current_data_t.setdefault(pos[v], []).append(v)

                        print("         a la fin : ", str(t) + " " + str(pos))

                        if max_pos < max(pos[u], pos[v]):
                            max_pos = max(pos[u], pos[v])

                        last_t = t

                    # chagement de t
                    pos = list(map(lambda x: x if x >= 0 else max_pos + gamma + 2 * n + x, pos))
                    print(">>> ", str(t - 1) + " " + str(pos))

                    f_outPut.write(str(t) + " " + str(pos) + "\n")

        break


linkStreamToPosition()
file = r"test0006.linkstream"

# dic_voisins(file)
