import os
import math
from copy import deepcopy
import random
import numpy as np
from pysat.solvers import Glucose3
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

#=================================== GEN & SOLVE CNFs ===================================#

def gen_board_num(row,col):
    count=1
    matrix=[]

    for i in range(row):
        tmp=[]
        for j in range(col):
            tmp.append(count)
            count+=1
        matrix.append(tmp)

    return matrix

def is_same_utility(tap_hop_1,tap_hop_2):

    if len(tap_hop_1) != len(tap_hop_2):
        return False
    
    tap_hop_1=sorted(deepcopy(tap_hop_1))
    tap_hop_2=sorted(deepcopy(tap_hop_2))

    for i in range(len(tap_hop_2)):
        if tap_hop_2[i] != tap_hop_1[i]:
            return False
    
    return True

def is_same(to_hop,tap_hop):

    if len(to_hop) == 0 or len(tap_hop) == 0:
        return False
    for i in to_hop:
        if is_same_utility(tap_hop,i):
            return True
    return False

def is_same_small(lst,num):

    if len(lst) == 0:
        return False

    for i in lst:
        if i == num:
            return True

    return False

def get_to_hop(adj_list,k,loop_times):

    to_hop=[]   
    for _ in range(loop_times):
        tmp=[]
        for _ in range(k):
            t=random.choice(adj_list)
            
            while is_same_small(tmp,t):
                t=random.choice(adj_list)

            tmp.append(t)

        while is_same(to_hop,tmp):
            tmp=[]
            for _ in range(k):
                t=random.choice(adj_list)
                
                while is_same_small(tmp,t):
                    t=random.choice(adj_list)

                tmp.append(t)

        to_hop.append(tmp)
    
    return to_hop
        
def get_adj_lst(i,j):
    adj_lst=[]

    if i-1 >= 0:
        adj_lst.append(board_num[i-1][j])
    if i+1 < len(a):
        adj_lst.append(board_num[i+1][j])
    if j-1 >= 0:
        adj_lst.append(board_num[i][j-1])
    if j+1 < len(a[0]):
        adj_lst.append(board_num[i][j+1])
    if i-1 >= 0 and j-1 >= 0:
        adj_lst.append(board_num[i-1][j-1])
    if i-1 >= 0 and j+1 < len(a[0]):
        adj_lst.append(board_num[i-1][j+1])
    if i+1 < len(a) and j-1 >= 0:
        adj_lst.append(board_num[i+1][j-1])
    if i+1 < len(a) and j+1 < len(a[0]):
        adj_lst.append(board_num[i+1][j+1])
    
    return adj_lst

def get_clauses(i,j):
    
    cell=board_num[i][j]
    adj_list=get_adj_lst(i,j)
    n=len(adj_list)
    k=a[i][j]
    
    clauses=[]
    # CELL : GREEN
    if k > 0 and (k <= n or (k-n) == 1):
        if k == 1:
            for e in adj_list:
                clauses.append([-cell,-e])
            tmp=deepcopy(adj_list)
            tmp.append(cell)
            clauses.append(tmp)
        else:
            loop_times=int(math.factorial(n)/(math.factorial(k-1)*math.factorial(n-k+1)))
            
            to_hop=get_to_hop(adj_list,k-1,loop_times)

            for tap in to_hop:
                # CHIEU THUAN
                con_lai=[]
                for e in adj_list:
                    if not e in tap:
                        con_lai.append(e)
                tmp=[]
                tmp.append(-cell)
                for m in tap:
                    tmp.append(-m)
                for e in con_lai:
                    tmp_=deepcopy(tmp)
                    tmp_.append(-e)
                    clauses.append(tmp_)
                # CHIEU NGUOC
                tmp_=deepcopy(con_lai)
                tmp_.append(cell)
                clauses.append(tmp_)

                for m in tap:
                    tmp_=deepcopy(con_lai)
                    tmp_.append(m)
                    clauses.append(tmp_)

    # CELL : RED
    if k <= n:
        if k == 0:
            clauses.append([-cell])
            for e in adj_list:
                clauses.append([-e])
        else:  
            loop_times=int(math.factorial(n)/(math.factorial(k)*math.factorial(n-k)))
            to_hop=get_to_hop(adj_list,k,loop_times)

            for tap in to_hop:
                #CHIEU THUAN
                con_lai=[]
                for e in adj_list:
                    if not e in tap:
                        con_lai.append(e)
                tmp=[]
                # tmp.append(cell)
                for m in tap:
                    tmp.append(-m)
                tmp_=deepcopy(tmp)
                tmp_.append(-cell)
                clauses.append(tmp_)

                for e in con_lai:
                    tmp_=deepcopy(tmp)
                    tmp_.append(-e)
                    clauses.append(tmp_)
                #CHIEU NGUOC
                tmp_=deepcopy(con_lai)
                tmp_.append(cell)
                # clauses.append(tmp_)

                for m in tap:
                    tmp__=deepcopy(tmp_)
                    tmp__.append(m)
                    clauses.append(tmp__)

    return clauses

#=================================== A* ===================================#
def CountCellisTrue(x, y, cl):                    #Dem so o BLUE xung quang o(x,y)
    count = 0
    for k in range(9):
        tx = hx[k] + x
        ty = hy[k] + y
        if tx >= 0 and ty >= 0 and tx < m and ty < n:
            if cl[tx][ty] == True:
                count = count + 1

    return count

def isColoringofAS(x, y, b):        #Kiem tra xem o (x, y) to mau duoc hay khong?
    if a[x][y] == -1 and colr[x][y] == True:
        return True

    tmp = deepcopy(b)

    for k in range(9):
        tx = hx[k] + x
        ty = hy[k] + y
        if (tx >= 0) and (ty >= 0) and (tx < m) and (ty < n) and (a[tx][ty] != -1):
            tmp[tx][ty] = tmp[tx][ty] - 1
            if tmp[tx][ty] < a[tx][ty]:
                return False
    return True

def isColoringMatrix(b):
    for i in range(m):
        for j in range(n):
            if a[i][j] != -1 and b[i][j] != a[i][j]:
                ktr = False
                for k in range(9):
                    tx = hx[k] + i
                    ty = hy[k] + j
                    if (tx >= 0) and (ty >= 0) and (tx < m) and (ty < n) and (colr[tx][ty] == True):
                        if isColoringofAS(tx, ty, b) == True:
                            ktr = True
                            break
                if ktr == False:
                    return False
    return True

def printSolution(mark):
    for i in range(m):
        for j in range(n):
            if mark[i][j] == True:
                f.write("1 ")
            else:
                f.write("0 ")
        f.write('\n')

def CountCellsUnsatisfied(cur, goal):                     #Dem so o chua thoa man yeu cau
    c = 0
    for i in range(m):
        for j in range(n):
            if goal[i][j] != -1:
                if cur[i][j] != goal[i][j]:
                    c = c + 1
    return c

def matrixSatisfied(cur):
    for i in range(m):
        for j in range(n):
            if a[i][j] != -1:
                if a[i][j] != cur[i][j]:
                    ktr = False
                    for k in range(9):
                        tx = hx[k] + i
                        ty = hy[k] + j
                        if (tx >= 0) and (ty >= 0) and (tx < m) and (ty < n) and (colr[tx][ty] == True):
                            if isColoringofAS(tx, ty, cur) == True:
                                ktr = True
                                break
                    if ktr == False:
                        return False
    return True

def CountTotalCosttoGoal(cur, goal):                    #Dem tong su chenh lech so voi goal
    c = 0
    if matrixSatisfied(cur) == False:
        return 10000
    for i in range(m):
        for j in range(n):
            if goal[i][j] != -1 and cur[i][j] != goal[i][j]:
                c = c + (cur[i][j] - goal[i][j])
    return c

def CountHofACell(x, y, start):                #Tinh heuristic cua o(x, y)
    if start[x][y] == a[x][y]:
        return 10000
    b = deepcopy(start)
    for k in range(9):
        tx = hx[k] + x
        ty = hy[k] + y
        if (tx >= 0 and ty >= 0 and tx < m and ty < n):
            b[tx][ty] = b[tx][ty] - 1
    
    count = CountCellsUnsatisfied(b, a)
    count = count + CountTotalCosttoGoal(b, a)

    return count

def GenHeuristic(start, colr):                  #Tinh heuristic va tim min
    h = deepcopy(start)
    for i in range(m):
        for j in range(n):
            if (start[i][j] == a[i][j]) or (isColoringofAS(i, j, start) == False):
                h[i][j] = 10000
            else:
                h[i][j] = CountHofACell(i, j, start)
    x = 0
    y = 0
    min = 10000000
    for i in range(m):
        for j in range(n):
            if h[i][j] < min and colr[i][j] == True:
                min = h[i][j]
                x = i
                y = j
    
    return [x, y]

def EqualtoGoal(cur, goal):
    for i in range(m):
        for j in range(n):
            if goal[i][j] != -1 and cur[i][j] != goal[i][j]:
                return False

    return True

def AStar(start, colr):
    cur_time = time.time()
    if (cur_time - start_time)/60 > 5:
        f.write("Run time is too large (> 10 minutes).")
        print("Run time is too large (> 10 minutes).")
        return -1
    for i in range(m):                                      #Dem so o mau xanh lien ke voi o (i,j)
        for j in range(n):
            start[i][j] = CountCellisTrue(i, j, colr)

    if isColoringMatrix(start) == False:
        f.write("NO SOLUTION")
        return 1
    if EqualtoGoal(start, a) == False:
        [x, y] = GenHeuristic(start, colr)
        colr[x][y] = False
        AStar(start, colr)
    else:
        printSolution(colr)
        return 1

#=================================== MAIN ===================================#

nameinp = "input.txt"
nameoutp = "output.txt"
f = open(nameoutp, 'w')
[a, m, n] = readfile(nameinp)
colr = []
for i in range(m):
    li = []
    for j in range(n):
        li.append(True)
    colr.append(li)

print("--------------------------------")
board_num=gen_board_num(m, n)
clauses=[]
for i in range(len(a)):
    for j in range(len(a[0])):
        if a[i][j] > -1:
            clauses+=get_clauses(i,j)
print("Number of CNFs generated: ", len(clauses))
f.write("Number of CNFs generated: ")
f.write(str(len(clauses)))
f.write('\n')

g = Glucose3()
for it in clauses:
    g.add_clause([int(k) for k in it])

f.write("\nUse pysat:\n")
kt = g.solve()
model = g.get_model()
if kt == True:
    print(model)
    c = 0
    for i in range(m):
        for j in range(n):
            if model[c] > 0:
                f.write("1 ")
            else:
                f.write("0 ")
            c = c + 1
        f.write('\n')
else:
    f.write("NO SOLUTION\n")
    print(model)

start_time = time.time()
f.write("\nUse A*:\n")
if kt == True:
    start = deepcopy(a)
    AStar(start, colr)
else:
    f.write("NO SOLUTION")
end_time = time.time()
print("A*:  total run-time: %f s" % ((end_time - start_time)))
print("--------------------------------")
f.close()