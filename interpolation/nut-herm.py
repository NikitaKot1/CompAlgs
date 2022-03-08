import numpy as np
import matplotlib
import matplotlib.pyplot as plt

table = []
tab = []
htab = []
allx = []

def read_table():
    f = open("lab1.txt", "r")
    table_lines = [line.strip() for line in f]
    for l in table_lines:
        table.append(list(map(float, l.split())))
    for i in table:
        allx.append(i[0])
    f.close()

def sort_t(x):
    for i in range(len(table)):
        for j in range(len(table)):
            if table[i][0] - x > table[j][0] - x:
                table[i], table[j] = table[j], table[i]

def sort_again(n):
    for i in range(n + 2):
        for j in range(n + 2):
            if table[i][0] < table[j][0]:
                table[i], table[j] = table[j], table[i]

def nuoton_tr(n, tb, xs):
    intr = [[]]
    trgl = []
    for i in xs:
        intr[0].append(i)
    for i in range(n):
        intr.append([])
        for j in range(n - i):
            intr[i + 1].append((intr[i][j + 1] - intr[i][j]) / (tb[j + i + 1] - tb[j]))
    for i in range(n + 1):
        trgl.append(intr[i][0])
    return trgl

def func(n, x, xtab, l):
    k = 0
    for i in range(n + 1):
        zn = xtab[i]
        for j in range(i):
            zn = zn * (x - table[j][l])
        k += zn
    return k

def hfunc(n, x, xtab):
    k = 0
    for i in range(n + 1):
        zn = xtab[i]
        for j in range(i):
            zn = zn * (x - table[j // 2][0])
        k += zn
    return k

def yofx(i1, i2):
    return (table[i1][1] - table[i2][1]) / (table[i1][0] - table[i2][0])

def table_for_nuoton(n):
    intr = []
    tb = []
    for i in range(n + 1):
        intr.append(table[i][1])
        tb.append(table[i][0])
    return nuoton_tr(n, tb, intr)

def revers_nuoton(n):
    intr = []
    tb = []
    for i in range(n + 1):
        intr.append(table[i][0])
        tb.append(table[i][1])
    return nuoton_tr(n, tb, intr)

def table_for_hermin(n):
    intr = [[], []]
    trgl = []
    for i in range(n):
        if (i % 2 == 0):
            intr[1].append(table[i // 2][2])
        else:
            intr[1].append(yofx(i // 2, i // 2 + 1))
        intr[0].append(table[i // 2][1])
        
    for i in range(1, n):
        k = 0
        intr.append([])
        for j in range(n - i):
            intr[i + 1].append((intr[i][j + 1] - intr[i][j]) / (table[k + 1][0] - table[k][0]))
            k += 1
    for i in range(n + 1):
        trgl.append(intr[i][0])
    return trgl

read_table()
x = float(input("x: "))
#n = int(input("n: "))
znach_n = []
print("-----------------")
print("|    Ньютон     |")
print("-----------------")
print("| n |     x     |")
sort_t(x)
for n in range(1, 6):
    sort_again(n)
    tab = table_for_nuoton(n)
    znach_n.append(func(n, x, tab, 0))
    print("| %d | %.7f |" % (n, znach_n[n - 1]))

# plt.figure(1)
# plt.plot(xpl, ypl, 'ro')
# plt.plot(xnut, ynut)
# plt.show()

sort_again(len(table) - 2)
revtab = revers_nuoton(len(table) - 1)
y = func(len(revtab) - 1, 0, revtab, 1)

#n = int(input("n: "))
#x = float(input("x: "))
print("-----------------")
print("|     Эрмит     |")
print("-----------------")
print("| n |     x     |")
sort_t(x)
znach_h = []
for n in range(1, 4):
    sort_again(n)
    htab = table_for_hermin(n * 2)
    znach_h.append(hfunc(n * 2, x, htab))
    print("| %d | %.7f |" % (n, znach_h[n - 1]))

# plt.figure(2)
# plt.plot(xpl, ypl, 'ro')
# plt.plot(xnut1, ynut1)
# plt.show()
print("---------------------------------")
print("|           Сравнение           |")
print("---------------------------------")
print("| Степень |  Ньютон  |   Эрмит  |")
print("|    2    | %.6f | %.6f |" % (znach_n[1], znach_h[0]))
print("|    4    | %.6f | %.6f |" % (znach_n[3], znach_h[1]))

print("\nf(0) = %.6f" % y)