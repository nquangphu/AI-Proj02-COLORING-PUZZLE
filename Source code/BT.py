import os
import math
from copy import deepcopy
import random
import time

hx = [0, 1, 0, -1, -1, -1, 0, 1, 1]
hy = [0, -1, -1, -1, 0, 1, 1, 1, 0]

#=================================== READ FILE ===================================#

def readfile(filename):
    f = open(filename, 'r')
    s = f.readline()
    [m, n] = s.split(" ")
    [m, n] = [int(m), int(n)]

    a = []
    for i in range(m):
        s = f.readline()
        l = s.split(" ")
        if l[-1].count('\n') != 0:
            l[-1] = l[-1].strip('\n')
        if l.count("") != 0:
            l.remove("")
        int_map = map(int, l)
        a.append(list(int_map))
    f.close()
    return [a, m, n]

#=================================== BACKTRACKING ===================================#
def CountCellisTrue(x, y, cl):                    #Dem so o BLUE xung quang o(x,y)
    count = 0
    for k in range(9):
        tx = hx[k] + x
        ty = hy[k] + y
        if tx >= 0 and ty >= 0 and tx < m and ty < n:
            if cl[tx][ty] == True:
                count = count + 1

    return count

def printSolution(mark):
    for i in range(m):
        for j in range(n):
            if mark[i][j] == True:
                f.write("1 ")
            else:
                f.write("0 ")
        f.write('\n')

def Accomplished(brd, cl):            #Kiem tra xem ket qua dung chua?
    for i in range(m):
        for j in range(n):
            if brd[i][j] != -1:
                count = CountCellisTrue(i, j, cl)
                if (count != brd[i][j]):
                    return False
    return True

def isColoring(x, y, cl):        #Kiem tra xem o (x, y) to mau duoc hay khong?
    for k in range(9):
        tx = hx[k] + x
        ty = hy[k] + y
        if (tx >= 0) and (ty >= 0) and (tx < m) and (ty < n) and (a[tx][ty] != -1):
            t = CountCellisTrue(tx, ty, cl)
            if t >= a[tx][ty]:
                return False
    return True

def backtracking_solve(x, y, result):               #Ham backtracking tu vi tri (x, y) trong matrix a(mxn), bang to mau mark(mxn)
    cur_time = time.time()
    total_time = (cur_time - start_time)/60
    if total_time > 10:
        result[0] = -1
        return
    if (Accomplished(a, mark) == False) and result[0] == 0:
        for k in range(9):
            tx = hx[k] + x
            ty = hy[k] + y
            if ((result[0] == 0) and (tx >= 0) and (ty >= 0) and (tx < m) and (ty < n) and (mark[tx][ty] == False)):
                if isColoring(tx, ty, mark) == True:
                    mark[tx][ty] = True
                    if Accomplished(a, mark) == True:
                        result[0] = 1
                        return
                    backtracking_solve(tx, ty, result)
                    if result[0] == 0:
                        mark[tx][ty] = False
                    else:
                        break
    else:
        if (Accomplished(a, mark) == True):
            result[0] = 1
            return

filename = "input.txt"
[a, m, n] = readfile(filename)
nameoutp = "output.txt"
f = open(nameoutp, 'w')
mark = []
for i in range(m):
    l = []
    for j in range(n):
        l.append(False)
    mark.append(l)
print("--------------------------------")

kt = True
result = [0]
start_time = time.time()
for i in range(m):
    if result[0] == -1:
        f.write("Run time is too large (> 10 minutes).")
        print("Run time is too large (> 10 minutes).")
        kt = False
        break
    if kt == False:
        break
    for j in range(n):
        if result[0] == -1:
            break
        if kt == True:
            if (a[i][j] != -1) and (CountCellisTrue(i, j, mark) < a[i][j]) and (mark[i][j] == False):
                backtracking_solve(i, j, result)
                if result[0] == 1:
                    kt = False
                    printSolution(mark)
                    break
        else:
            break

end_time = time.time()
print("total run-time: %f s" % ((end_time - start_time)))
if (kt == True):
    f.write("NO SOLUTION")

print("--------------------------------")
f.close()