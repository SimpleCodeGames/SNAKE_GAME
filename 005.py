# Proper Collision Added
import pygame
import sys
import random
import threading
import time

BACKGROUND = (30, 30, 30)
LOCKED = (120, 120, 120)
ACTIVE = (0, 255, 255)
RED = (255, 0, 0)
HEAD = [200, 200, 200]

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
spn_cnt = 0
plyr = [[7, 1], [7, 2], [7, 3]]
bf_slthr = [[0, 0], [0, 0], [0, 0]]
lock = threading.Lock()

# Direction Variables
# drct clock angles: 3, 6, 9, 12
drct = 3

#---------------------
# Game Over
gm_ovr = 0
def check_l(): #moving +1
    return plyr[plyr_sz - 1][1] < board_x - 1
def check_r(): #moving -1
    return plyr[plyr_sz - 1][1] > 0
def check_u(): #moving +1 up
    return plyr[plyr_sz - 1][0] > 0
def check_d(): #moving +1 down
    return plyr[plyr_sz - 1][0] < board_y - 1
def game_over():
    return (gm_ovr == 0)
#---------------------

# Screen Factors
scrn_to_brd = 10
screen_y = board_y * scrn_to_brd
screen_x = board_x * scrn_to_brd
screen_grid = []
for y in range(screen_y):
    screen_grid.append([0] * screen_x)

def mk_scrn():
    for y in range(board_y):
        for x in range(board_x):
            screen_grid[y][x] = 1
            screen_grid[y + 1][x] = 1
            screen_grid[y][x + 1] = 1
            screen_grid[y + 1][x + 1] = 1

def spawn():
    global spn_cnt
    if spn_cnt >= plyr_sz//10 + 2:
        return
    for i in range(plyr_sz//10 + 1):
        empty = [(y, x) for y in range(board_y) for x in range(board_x) if board[y][x] == 0 and (y <= plyr[plyr_sz - 1][0] - 2 or y >= plyr[plyr_sz - 1][0] + 2) and (x <= plyr[plyr_sz - 1][1] - 2 or x >= plyr[plyr_sz - 1][1] + 2)]
        if empty: 
            y, x = random.choice(empty)
            board[y][x] = 3
            spn_cnt += 1

def eat():
    global plyr, plyr_sz, spn_cnt
    dy = plyr[plyr_sz - 1][0] - plyr[plyr_sz - 2][0]
    dx = plyr[plyr_sz - 1][1] - plyr[plyr_sz - 2][1]
    plyr.append([plyr[plyr_sz - 1][0] + dy, plyr[plyr_sz - 1][1] + dx])
    bf_slthr.append([plyr[plyr_sz - 1][0] + dy, plyr[plyr_sz - 1][1] + dx])
    plyr_sz += 1
    spn_cnt -= 1

def slither():
    global gm_ovr, drct
    while True:
        time.sleep(0.2)
        with lock:
            if gm_ovr == 0:
                to_brd(0)
                # Body
                for i in range(plyr_sz):
                    bf_slthr[i] = list(plyr[i])
                for i in range(plyr_sz - 1):
                    plyr[i][0] = bf_slthr[i + 1][0]
                    plyr[i][1] = bf_slthr[i + 1][1]
                # Head
                ny, nx = plyr[plyr_sz - 1][0], plyr[plyr_sz - 1][1]
                if drct == 3 and check_l():
                    nx += 1
                elif drct == 6 and check_d():
                    ny += 1
                elif drct == 9 and check_r():
                    nx -= 1
                elif drct == 12 and check_u():
                    ny -= 1
                else:
                    gm_ovr = 1
                
                if gm_ovr == 0:
                    if [ny, nx] in plyr[:-1]:
                        gm_ovr = 1
                    else:
                        plyr[plyr_sz - 1][0] = ny
                        plyr[plyr_sz - 1][1] = nx
                        if board[ny][nx] == 3:
                            eat()
                            spawn()

                to_brd(1)

def to_brd(state):
    for i in range(plyr_sz):
        board[plyr[i][0]][plyr[i][1]] = state
    board[plyr[plyr_sz - 1][0]][plyr[plyr_sz - 1][1]] = 4

def draw_on_screen(screen):
    with lock:
        for y in range(board_y):
            for x in range(board_x):
                X = x * (length + gap) + gap
                Y = y * (length + gap) + gap

                if board[y][x] == 0:
                    pygame.draw.rect(screen, BACKGROUND, [X, Y, length, length], border_radius = 5)
                if board[y][x] == 1:
                    pygame.draw.rect(screen, LOCKED, [X, Y, length, length], border_radius = 5)
                if board[y][x] == 2:
                    pygame.draw.rect(screen, ACTIVE, [X, Y, length, length], border_radius = 5)
                if board[y][x] == 3:
                    pygame.draw.rect(screen, RED, [X, Y, length, length], border_radius = 5)
                if board[y][x] == 4:
                    pygame.draw.rect(screen, HEAD, [X, Y, length, length], border_radius = 5)

def main():
    global drct, gm_ovr, plyr, plyr_sz, bf_slthr, spn_cnt, board
    pygame.init()
    pygame.display.set_caption("Snake 005")
    screen = pygame.display.set_mode((tab_x, tab_y))
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 50)
    
    bg_thread = threading.Thread(target=slither, daemon=True)
    bg_thread.start()
    
    while True:
        with lock:
            board = [[0] * board_x for _ in range(board_y)]
            plyr_sz = 3
            spn_cnt = 0
            plyr = [[7, 1], [7, 2], [7, 3]]
            bf_slthr = [[0, 0], [0, 0], [0, 0]]
            gm_ovr = 0
            drct = 3
            spawn()
            eat()
            to_brd(1)

        while game_over():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and drct != 3:
                        drct = 9
                    if event.key == pygame.K_RIGHT and drct != 9:
                        drct = 3
                    if event.key == pygame.K_DOWN and drct != 12:
                        drct = 6
                    if event.key == pygame.K_UP and drct != 6:
                        drct = 12
            
            screen.fill((10, 10, 10))
            draw_on_screen(screen)
            pygame.display.flip()
            clock.tick(30)

        while not game_over():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        gm_ovr = 0
                        break
            
            screen.fill((10, 10, 10))
            draw_on_screen(screen)
            
            overlay = pygame.Surface((tab_x, tab_y), pygame.SRCALPHA)
            overlay.fill((120, 120, 120, 150))
            screen.blit(overlay, (0, 0))
            txt = font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(txt, (tab_x // 2 - txt.get_width() // 2, tab_y // 2 - txt.get_height() // 2))
            
            pygame.display.flip()
            clock.tick(30)
            
            if gm_ovr == 0:
                break

if __name__ == '__main__':
    main()