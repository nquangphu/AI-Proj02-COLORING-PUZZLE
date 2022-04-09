from itertools import combinations
import time

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

def printSolution(mark):
    for i in range(m):
        for j in range(n):
            if mark[i][j] == True:
                f.write("1 ")
            else:
                f.write("0 ")
        f.write('\n')


def BruteForce(path=[]):
    if len(path) == len(POSITIONS):
        for pos in path:
            color_zone = [
                [pos[0] + row, pos[1] + col]
                for row in range(-1, 2)
                for col in range(-1, 2)
                if 0 <= pos[0] + row < N_ROW and 0 <= pos[1] + col < N_COL
            ]
            count = 0
            for color_pos in color_zone:
                if COLOR_BOARD[color_pos[0]][color_pos[1]]:
                    count += 1
            if count != a[pos[0]][pos[1]]:
                return False
        return True

    else:
        pos = next((i for i in POSITIONS if i not in path))
        path.append(pos)
        color_zone = [
            [pos[0] + row, pos[1] + col]
            for row in range(-1, 2)
            for col in range(-1, 2)
            if 0 <= pos[0] + row < N_ROW and 0 <= pos[1] + col < N_COL
        ]
        colored_pos = [i for i in color_zone if COLOR_BOARD[i[0]][i[1]]]  # xoa
        count = len(colored_pos)  # xoa
        if count == a[pos[0]][pos[1]]:  # xoa
            if BruteForce(path):  # xoa
                return True  # xoa
        elif count < a[pos[0]][pos[1]]:  # xoa
            uncolored_pos = [
                i for i in color_zone if not COLOR_BOARD[i[0]][i[1]]
            ]  # xoa
            combine_zone = combinations(
                uncolored_pos, a[pos[0]][pos[1]] - count
            )  # thay uncolored_pos thanh color_zone

            for combination in combine_zone:
                for i in combination:
                    COLOR_BOARD[i[0]][i[1]] = True
                if BruteForce(path):
                    return True
                for i in combination:
                    COLOR_BOARD[i[0]][i[1]] = False
        path.pop()
        return False


filename = "input.txt"
[a, m, n] = readfile(filename)
nameoutp = "output.txt"
f = open(nameoutp, 'w')
start_time = time.time()
N_ROW, N_COL = m, n
COLOR_BOARD = [[False for _ in row] for row in a]
POSITIONS = [
    [i, k] for i, row in enumerate(a) for k, col in enumerate(row) if col > -1
]

kt = BruteForce()

if kt == True:
    printSolution(COLOR_BOARD)
else:
    f.write("NO SOLUTION")
print("--------------------------------")
end_time = time.time()
print("total run-time: %f s" % ((end_time - start_time)))
print("--------------------------------")
f.close()