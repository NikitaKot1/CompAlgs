table = []
coly = 5
linesx = []
linesy = []
linesz = []
newz = []
newx = []
newy = []
newt = []

def get_table(f):
    table_lines = [line.strip() for line in f]
    z = 0
    ys = []
    nnum = []
    nnnum = []
    for line in table_lines:
        if line == "":
            nnnum.append(nnum)
            nnum = []
        elif "z=" in line:
            z = float(line[list(line).index("=") + 1])
            linesz.append(z)
        elif "y" in line:
            xs = list(map(float, line[3:].split()))
            linesx.append(xs)
        else:
            linesnum = list(map(float, line.split()))
            nnum.append(linesnum)
            y = linesnum[0]
            ys.append(y)
            if (len(ys) == coly):
                linesy.append(ys)
                ys = []
            linesnum.pop(0)
    nnnum.append(nnum)
    return nnnum

def blcoord(c, nc, linesc):
    newc = []
    mini = abs(linesc[0] - c)
    blc = 0
    for i in range(len(linesc)):
        if abs(linesc[i] - c) < mini:
            mini = abs(linesc[i] - c)
            blc = i
    start = 0
    end = 0
    if (blc - nc // 2 >= 0):
        start = blc - nc // 2
    if (start == 0):
        end = nc + 1
    else:
        end = blc + nc // 2 + nc % 2 + 1
    if (end > len(linesc)):
        end = len(linesc)
        start = end - nc - 1
    for i in range(start, end):
        newc.append(linesc[i])
    return newc

def table_for_nuoton(x, y, z, nx, ny, nz):
    newz = blcoord(z, nz, linesz)
    newx = []
    for i in newz:
        newx.append(blcoord(x, nx, linesx[linesz.index(i)]))
    newy = []
    for i in newz:
        newy.append(blcoord(y, ny, linesy[linesz.index(i)]))
    
    newt = []
    for i in range(len(newz)):
        newt.append([])
        for j in range(len(newy[i])):
            newt[i].append([])
            for k in range(len(newx[i])):
                zpos = linesz.index(newz[i])
                ypos = linesy[i].index(newy[i][j])
                xpos = linesx[i].index(newx[i][k])
                newt[i][j].append(table[zpos][ypos][xpos])

    return newx, newy, newz, newt

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

def func1(trgl, x, arrx):
    k = 0
    n = len(trgl) - 1
    for i in range(n + 1):
        zn = trgl[i]
        for j in range(i):
            zn = zn * (x - arrx[j])
        k += zn
    return k

def manymer(x, y, z, nx, ny, nz):
    zobsh = []
    for i in range(nz + 1):
        x_for_y = []
        for j in range(ny + 1):
            trgl = nuoton(newx[i], newt[i][j])
            yzn = func1(trgl, x, newx[i])
            x_for_y.append(yzn)
        print(x_for_y)
        trgl = nuoton(newy[i], x_for_y)
        zzn = func1(trgl, y, newy[i])
        zobsh.append(zzn)
    print(zobsh)
    trgl = nuoton(newz, zobsh)
    rez = func1(trgl, z, newz)
    return rez


f = open("lab2.txt", "r")
table = get_table(f)

nx = int(input("nx = "))
ny = int(input("ny = "))
nz = int(input("nz = "))

x = float(input("x = "))
y = float(input("y = "))
z = float(input("z = "))

newx, newy, newz, newt = table_for_nuoton(x, y, z, nx, ny, nz)

rez = manymer(x, y, z, nx, ny, nz)
print()
print(rez)