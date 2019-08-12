import random
import sys

n = int(sys.argv[1])
T = int(sys.argv[2])
d = int(sys.argv[3])

xposition = [0] * n

for t in range(T):
    print(t, xposition)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(xposition[i] - xposition[j]) <= d:
                print(t, i, j)
    for i in range(n):
        if random.randint(0, 9) < 1 and xposition[i] > 0:
            xposition[i] -= 1
        else:
            xposition[i] += random.randint(0, 4)
