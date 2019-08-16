import random
import sys

n = int(sys.argv[1])
T = int(sys.argv[2])
d = int(sys.argv[3])

# xposition[i] = [x,y,vx,vy]
xposition = [[0, 0, 0, 0]] * n

fort = 0.6
vent = 1

x_max = n * 2
y_max = n * 2

for t in range(T):

    print(t, list(map(lambda x: [round(x[0], 3), round(x[1], 2)], xposition)))

    for i in range(n):
        for j in range(i + 1, n):
            if (xposition[i][0] - xposition[j][0]) * (xposition[i][0] - xposition[j][0]) + (
                    xposition[i][1] - xposition[j][1]) * (xposition[i][1] - xposition[j][1]) <= d * d:
                print(t, i, j)

    for i in range(n):
        xposition[i][0] += xposition[i][2]  # x += vx
        xposition[i][1] += xposition[i][3]  # y += vy
        xposition[i][2] += fort  # vx *= fort
        xposition[i][3] += fort  # vy *= fort

        if random.randint(0, 2) == 0:
            a = random.randint(0, n)
            xposition[i][2] += vent * a / 10
        if random.randint(0, 4) == 0:
            a = random.randint(0, n)
            xposition[i][3] += vent * a / 10

        if random.randint(0, 4) < 1 and xposition[i][0] > 10:
            xposition[i][0] -= random.randint(1, 10)
            xposition[i][2] -= random.randint(0, int(xposition[i][2]) + 1)

        if random.randint(0, 4) < 1 and xposition[i][1] > 10:
            xposition[i][1] -= random.randint(1, 10)
            xposition[i][3] -= random.randint(0, int(xposition[i][3]) + 1)

        if xposition[i][0] >= x_max:
            xposition[i][0] -= xposition[i][2]
        if xposition[i][1] >= y_max:
            xposition[i][1] -= xposition[i][3]
