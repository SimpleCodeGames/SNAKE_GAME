# Eat Apple Added
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
lock = threading.Lock()

def eat():
    global plyr, plyr_sz
    dy = plyr[plyr_sz - 1][0] - plyr[plyr_sz - 2][0]
    dx = plyr[plyr_sz - 1][1] - plyr[plyr_sz - 2][1]
    plyr.append([plyr[plyr_sz - 1][0] + dy, plyr[plyr_sz - 1][1] + dx])
    

def main():
    eat()
    print(plyr)
    #bg_thread = threading.Thread(target=spawn, daemon=True)
    #bg_thread.start()

if __name__ == '__main__':
    main()