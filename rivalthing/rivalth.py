
import random
import matplotlib
from matplotlib import ticker
import matplotlib.pyplot as plt
import numpy as np
#from matplotlib.ticker import LinearLocator
import matplotlib.ticker
from matplotlib import cm

ymax = 5
ymin = -5
table1 = []
N = 6

def create_table(N):
    f = open("D:/vichAlg/rivalthing/bulshit1.txt", "w")
    y0 = 0
    for i in range(N):
        y = y0 + random.random() * (ymax - ymin) + ymin
        y0 = y
        arr = [i, y, 1]
        f.write("%d %f %d\n" % (i, y, 1))
        table1.append(arr)

def matr_for_gauss(table, n):
    sum_x = []
    for i in range(n * 2):
        sum_xi = 0
        for j in range(N):
            sum_xi += table[j][0] ** i * table[j][2]
        sum_x.append(sum_xi)
    sum_x_y = []
    for i in range(n):
        sum_yi = 0
        for j in range(N):
            sum_yi += table[j][0] ** i * table[j][2] * table[j][1]
        sum_x_y.append(sum_yi)

    gmatr = []
    for i in range(n):
        gstr = []
        for j in range(n):
            gstr.append(sum_x[i+j])
        gstr.append(sum_x_y[i])
        gmatr.append(gstr)
    return gmatr

def gauss(gmatr, n):
    for i in range(n):
        for j in range(i+1, n):
            k = -(gmatr[j][i] / gmatr[i][i])
            for l in range(i, n+1):
                gmatr[j][l] += k * gmatr[i][l]
    
    a = [0 for i in range(n)]
    for i in range(n-1, -1, -1):
        for j in range(n-1, i, -1):
            gmatr[i][n] -= a[j] * gmatr[i][j]
        a[i] = gmatr[i][n] / gmatr[i][i]
    return a

def f(arrx, arra):
    rez = []
    for j in range(len(arrx)):
        rezi = 0
        for i in range(len(arra)):
            rezi += arra[i]*(arrx[j]**i)
        rez.append(rezi)
    return rez



create_table(N)
n = int(input("Введите n: "))
vect = []
for ni in range(1, n+1):
    gmatr = matr_for_gauss(table1, ni)
    a = gauss(gmatr, ni)
    xpl = np.arange(table1[0][0], table1[len(table1)-1][0], 0.01)
    ypl = f(xpl, a)
    vect.append([xpl, ypl])

xd = []
yd = []
for i in range(N):
    xd.append(table1[i][0])
    yd.append(table1[i][1])

plt.figure(1)
for i in range(n):
    plt.plot(vect[i][0], vect[i][1], label='n = %d'%(i+1))
plt.plot(xd, yd, 'ro')
plt.legend()
plt.show()

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)
surf = ax.plot_surface(X, Y, Z)
plt.show()
