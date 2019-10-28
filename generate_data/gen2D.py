import random
import sys
import numpy

#
n = int(sys.argv[1])
T = int(sys.argv[2])
d = int(sys.argv[3])

# xposition[i] = [x,y,vx,vy]

xposition = numpy.zeros((n, 4)).astype(float)

fort = 0.9
vent = 1

x_max = n
y_max = n

for t in range(T):

    for i in range(n):
        if random.randint(0, 2) == 0:
            xposition[i][2] += vent
        if random.randint(0, 2) == 0:
            xposition[i][3] += vent

        a = random.randint(0, n)
        xposition[i][2] += vent * a / 10
        xposition[i][3] += vent * a / 10

        if xposition[i][0] < 0:
            xposition[i][0] = (-1)
        if xposition[i][1] < 0:
            xposition[i][1] *= (-1)

        xposition[i][2] *= fort  # vx *= fort
        xposition[i][3] *= fort  # vy *= fort
        xposition[i][0] += xposition[i][2]  # x += vx
        xposition[i][1] += xposition[i][3]  # y += vy

    print(t, list(map(lambda x: [x[0], x[1]], xposition)))

    for i in range(n):
        for j in range(i + 1, n):
            if (xposition[i][0] - xposition[j][0]) * (xposition[i][0] - xposition[j][0]) + (
                    xposition[i][1] - xposition[j][1]) * (xposition[i][1] - xposition[j][1]) <= d * d:
                print(t, i, j)