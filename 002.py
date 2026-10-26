# Movement Analysis Added
import pygame
import sys
import random
import threading
import time

# Board Variables
board_y = 15
board_x = 17
board = []
for y in range(board_y):
    board.append([0] * board_x)

# Screen
length = 25
gap = 5

tab_y = board_y * length + board_y * gap + gap
tab_x = board_x * length + board_x * gap + gap

# Spawn & Pieces & Coords [y][x]
plyr_sz = 3
plyr = [[7, 1], [7, 2], [7, 3]]
bf_slthr = [[0, 0], [0, 0], [0, 0]]
lock = threading.Lock()

# Direction Variables
# drct clock angles: 3, 6, 9, 12
drct = 0

#---------------------
# Game Over
gm_ovr = 0
def check_l(): #moving +1
    return all(plyr[i][1] <= board_x - 2 for i in range(plyr_sz))
def check_r(): #moving -1
    return all(0 <= plyr[i][1] - 1 for i in range(plyr_sz))
def check_u(): #moving +1 up
    return all(0 <= plyr[i][0] - 1 for i in range(plyr_sz))
def check_d(): #moving +1 down
    return all(plyr[i][0] <= board_y - 2 for i in range(plyr_sz))
def game_over():
    return (gm_ovr == 0)
#---------------------

def eat():
    global plyr, plyr_sz
    dy = plyr[plyr_sz - 1][0] - plyr[plyr_sz - 2][0]
    dx = plyr[plyr_sz - 1][1] - plyr[plyr_sz - 2][1]
    plyr.append([plyr[plyr_sz - 1][0] + dy, plyr[plyr_sz - 1][1] + dx])
    bf_slthr.append([0, 0])
    plyr_sz += 1

def slither(drct):
    global gm_ovr
    for i in range(plyr_sz):
        bf_slthr[i] = plyr[i]
    for i in range(plyr_sz - 1):
        dy = bf_slthr[i + 1][0] - bf_slthr[i][0]
        dx = bf_slthr[i + 1][1] - bf_slthr[i][1]
        plyr[i][0] += dy
        plyr[i][1] += dx
    if drct == 3:
        if check_l():
            plyr[plyr_sz - 1][1] += 1
        else:
            gm_ovr = 1
    elif drct == 6:
        if check_d():
            plyr[plyr_sz - 1][0] -= 1
        else:
            gm_ovr = 1
    elif drct == 9:
        if check_r():
            plyr[plyr - 1][1] -= 1
        else:
            gm_ovr = 1
    elif drct == 12:
        if check_u():
            plyr[plyr - 1][0] += 1
        else:
            gm_ovr = 1

def main():
    eat()
    while game_over():
        print(plyr)
        slither(3)
    else:
        print("Game Over")
    #bg_thread = threading.Thread(target=spawn, daemon=True)
    #bg_thread.start()

if __name__ == '__main__':
    main()