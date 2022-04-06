import random
import matplotlib.pyplot as plt
import numpy as np

table1 = []
table2 = []
N = 6
N2 = 20

def create_table(N, ymax, ymin):
    f = open("D:/vichAlg/rivalthing/bulshit1.txt", "w")
    y0 = 0
    for i in range(N):
        y = y0 + random.random() * (ymax - ymin) + ymin
        y0 = y
        arr = [i, y, 1]
        f.write("%d %f %d\n" % (i, y, 1))
        table1.append(arr)

def read_table():
    f = open("D:/vichAlg/rivalthing/bulshit1.txt", "r")
    table_lines = [line.strip() for line in f]
    N = 0
    for l in table_lines:
        table1.append(list(map(float, l.split())))
        N += 1
    f.close()

def matr_for_gauss(table, n, len):
    n += 1
    sum_x = []
    for i in range(n * 2):
        sum_xi = 0
        for j in range(len):
            sum_xi += table[j][0] ** i * table[j][2]
        sum_x.append(sum_xi)
    sum_x_y = []
    for i in range(n):
        sum_yi = 0
        for j in range(len):
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
    n+=1
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

####################################

def third_step(table, n, lenn):
    arrx = np.arange(table[0][0], table[lenn-1][0], 0.1)
    newy = []
    for i in range(lenn):
        newy.append(table[i][1])
    table_of_tables = []
    for i in range(lenn):
        new_t = []
        for j in range(lenn):
            new_t.append([table[j][0], table[i][2][j], table[j][3]])
        gmatr = matr_for_gauss(new_t, n, lenn)
        a = gauss(gmatr, n)
        table_of_tables.append(f(arrx, a))
    
    arra = []
    for i in range(arrx.size):
        tab_y = []
        for j in range(lenn):
            tab_y.append([newy[j], table_of_tables[j][i], table[j][3]])
        gmatr = matr_for_gauss(tab_y, n, lenn)
        a = gauss(gmatr, n)
        arra.append(a)
    return arra

####################################

def randran(n, vmin, vmax):
    return (vmax - vmin)*np.random.rand(n) + vmin

#######################################

tag = int(input("Одномерная -- 1\nДвумерная -- 2\n"))
if tag == 1:
    tag = int(input("Сгенерировать точки -- 1\nПрочитать точки -- 2\n"))
    if tag == 1:
        create_table(N, 5, -5)
    else:
        read_table()
    tag = int(input("Вывести графики с 1-й по n-ую степень -- 1\nВывести график n-ой степени -- 2\n"))
    n = int(input("Введите n: "))
    vect = []
    for ni in range(1, n+1):
        gmatr = matr_for_gauss(table1, ni, N)
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
    if tag == 1:
        for i in range(n):
            plt.plot(vect[i][0], vect[i][1], label='n = %d'%(i+1))
    else:
        plt.plot(vect[n-1][0], vect[n-1][1], label='n = %d'%(n))
    plt.plot(xd, yd, 'ro', label='Оригинальные точки')
    plt.legend()
    plt.show()
else:
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    XS = randran(N2, -50, 50)
    XS.sort()
    YS = randran(N2, -50, 50)
    YS.sort()
    XS, YS = np.meshgrid(XS, YS)

    ZS = XS**3 + YS**3


    xxs = XS.tolist()
    yys = YS.tolist()
    zzs = ZS.tolist()
    for i in range(N2):
        table2.append([xxs[0][i], yys[i][0], zzs[i], 1])

    n = int(input("Введите n: "))
    arra = third_step(table2, n, N2)
    dep_x = np.arange(XS.min(), XS.max(), 0.1)
    dep_y = np.arange(YS.min(), YS.max(), (YS.max() - YS.min()) / dep_x.size)
    dep_z = np.array([dep_x for i in range(dep_x.size)])

    for i in range(dep_x.size):
        k = np.array(f(dep_y, arra[i]))
        for j in range(dep_x.size):
            dep_z[i][j] = k[j]

    dep_x, dep_y = np.meshgrid(dep_x, dep_y)
    m = ['o', '^']
    surf = ax.plot_surface(dep_y, dep_x, dep_z)
    ax.scatter(XS, YS, ZS, marker=m[0])
    plt.show()