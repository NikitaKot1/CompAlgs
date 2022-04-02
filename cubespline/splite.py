import numpy as np
import matplotlib
import matplotlib.pyplot as plt

table = []
tab = []
htab = []
allx = []
ally = []
n = 0
koeff = []
c0 = 0
ck = 0

def read_table():
    f = open("D:/vichAlg/cubespline/spl.txt", "r")
    table_lines = [line.strip() for line in f]
    for l in table_lines:
        table.append(list(map(float, l.split())))
    for i in table:
        allx.append(i[0])
        ally.append(i[1])
    f.close()

def nuoton(xs, liness):
    trgl = []
    intr = [[]]
    n = len(xs)
    for i in range(n):
        intr[0].append(liness[i])
    for i in range(n):
        intr.append([])
        for j in range(n - i - 1):
            intr[i + 1].append((intr[i][j + 1] - intr[i][j]) / (xs[j + i + 1] - xs[j]))
    for i in range(n):
        trgl.append(intr[i][0])
    return trgl


def hi(i):
    return allx[i] - allx[i - 1]

def fi(i):
    return 3 * ((ally[i] - ally[i - 1]) / hi(i) - (ally[i - 1] - ally[i - 2]) / hi(i -1))

def koefss():
    eps = [0, 0]
    nuo = [0, 0]
    c = [ck]
    epsl0 = 0
    nuol0 = 0
    for i in range(2, len(allx)):
        k = hi(i-1) * epsl0 + 2 * (hi(i-1) + hi(i))
        epsl = - hi(i) / k
        nuol = (fi(i) - hi(i-1) * nuol0) / k
        epsl0 = epsl
        nuol0 = nuol
        eps.append(epsl)
        nuo.append(nuol)

    for i in range(len(allx), 1, -1):
        c.insert(0, eps[i-1] * c[0] + nuo[i-1])
    #c[0] = c0

    a = []
    for i in range(len(allx)):
        a.append(ally[i])

    b = []
    d = []
    for i in range(1, len(allx)-1):
        bi = (ally[i] - ally[i-1]) / hi(i) - hi(i) * (c[i] - 2*c[i-1]) / 3
        b.append(bi)

        di = (c[i] + c[i-1]) / hi(i) / 3
        d.append(di)
    b.append((ally[n] - ally[n-1]) / hi(n) - hi(n) * (ck - 2*c[n-1]) / 3)
    d.append((ck + c[n-1]) / hi(n) / 3)

    return a, b, c, d


def funcspline(a, b, c, d, i, x):
    x = x - allx[i+1]
    return a[i+1] + b[i] * x + c[i] * x**2 + d[i] * x**3

def func1(trgl, x, arrx):
    k = 0
    n = len(trgl) - 1
    for i in range(n + 1):
        zn = trgl[i]
        for j in range(i):
            zn = zn * (x - arrx[j])
        k += zn
    return k

def df(trgl, x, arrx):
    x1 = func1(trgl, x, arrx)
    x2 = func1(trgl, x+0.000001, arrx)
    return (x2 - x1) / 0.000001

def ddf(trgl, x, arrx):
    dx1 = df(trgl, x, arrx)
    dx2 = df(trgl, x+0.000002, arrx)
    return (dx2 - dx1) / 0.000002

read_table()
n = len(allx) - 1

xpl = []
ypl = []
trgl = nuoton(allx, ally)
xnu = []
for i in range(0, len(allx)-1):
    for j in np.arange(allx[i], allx[i+1], 0.01):
        xnu.append(func1(trgl, j, allx))

# ck = ddf(trgl, n, allx)
# print(ck)
a, b, c, d = koefss()

for i in range(0, len(allx)-1):
    for j in np.arange(allx[i], allx[i+1], 0.01):
        ypl.append(j)
        xpl.append(funcspline(a, b, c, d, i, j))
        



plt.figure(1)

plt.plot(ypl, xpl, label='spline')
plt.plot(ypl, xnu, label='nuoton')
plt.plot(allx, ally, 'ro')
plt.show()
