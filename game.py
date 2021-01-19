import pygame
import json
from math import floor, ceil
from random import randint, choice

# If config.json exists, take persistent settings. Otherwise defaults.
try:
    with open("config.json") as file:
        data = file.read()
    settings = json.loads(data)
    resolution = settings["default_resolution"]
    granularity = settings["default_granularity"]
    timestep = settings["default_timestep"]
    grid_toggle = bool(settings["default_show_grid"])
    help_toggle = bool(settings["show_controls_at_launch"])
    refresh_rate = settings["screen_refresh_rate"]
    key_repeat = settings["key_repeat_interval"]
except:
    resolution = 600
    granularity = 70
    grid_toggle = False
    help_toggle = True
    timestep = 30
    refresh_rate = 60
    key_repeat = 50

# global components
pygame.init()
screen = pygame.display.set_mode((resolution, resolution))
clock = pygame.time.Clock()
pygame.display.set_caption("Conway's Game of Life (PAUSED)")
pixel = resolution / granularity
gameboard = set()

def saveBoard(filename: str, granularity: int, gameboard: list):
    with open(filename, "w") as overwrite:
        overwrite.write("")
    with open(filename, "a") as file:
        for y in range(granularity):
            for x in range(granularity):
                if (x,y) not in gameboard:
                    file.write("0")
                else:
                    file.write("1")
            file.write("\n")

def loadBoard(filename: str):
    gameboard = set()
    with open(filename) as file:
        lines = file.readlines()
    for y in range(len(lines)):
        for x in range(len(lines)):
            if lines[y][x] == "1":
                gameboard.add((x,y))
    return gameboard

def randomBoard(granularity: int):
    density = choice([[0,1], [0,0,1], [0,0,0,1]])
    gameboard = {((randint(0, granularity), randint(0, granularity))) for x in range(granularity**2) if choice(density) == 1}
    return (granularity, gameboard)

def infoSplash():
    pos = (resolution - 300) // 2
    try:
        splash = pygame.image.load("extras\\infosplash.png")
        screen.blit(splash, (pos, pos))
    except:
        font = pygame.font.SysFont("courier bold", 30)
        text_drawing = font.render("infosplash.png not found!", True, [0,0,0])
        screen.blit(text_drawing, (pos,pos))

def countNeighbors(x: int, y: int, granularity: int, gameboard: set):
    neighbors = 0
    for (dx, dy) in {(-1,-1), (-1,1), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (1,0)}:
            if ((x + dx) % granularity, (y + dy) % granularity) in gameboard:
                neighbors += 1
                if neighbors > 3:
                    return neighbors
    return neighbors

def chooseFate(x: int, y: int, granularity: int, gameboard: list):
    neighbors = countNeighbors(x, y, granularity, gameboard)
    if (x,y) not in gameboard:
        if neighbors == 3:
            return (x,y)
        else:
            return 0
    else:
        if neighbors < 2 or neighbors > 3:
            return 0
        else:
            return (x,y)

def drawGrid(granularity: int, pixel: int):
    colour = [200, 200, 200]
    for x in range(0, granularity):
        pygame.draw.line(screen, colour, (x * pixel, 0), (x * pixel, resolution), 1)
    for y in range(0, granularity):
        pygame.draw.line(screen, colour, (0, y * pixel), (resolution, y * pixel), 1)

def iterate(granularity: int, gameboard: set):
    fates = set()
    for (x,y) in gameboard:
        fates.add(chooseFate(x, y, granularity, gameboard))
        for (dx, dy) in {(-1,-1), (-1,1), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (1,0)}:
            fates.add(chooseFate((x + dx) % granularity, (y + dy) % granularity, granularity, gameboard))
    try:
        fates.remove(0)
        return fates
    except:
        return fates

def drawingScreen(granularity: int, pixel: int, gameboard: set):

    pygame.display.set_caption("Conway's Game of Life (PAUSED)")
    global grid_toggle
    global help_toggle
    key_held_timer = [refresh_rate / 3, 0, ""] # countdown to repetition, then looping counter, then "left" or "right".

    while True:

        # grid, dots, help splash.
        screen.fill((255,255,255))
        for (x,y) in gameboard:
            pygame.draw.rect(screen, [0,0,0], (x * pixel, y * pixel, ceil(resolution/granularity), ceil(resolution/granularity)))
        if grid_toggle:
            drawGrid(granularity, pixel)
        if help_toggle:
            infoSplash()

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    help_toggle = False
                    game(granularity, pixel, gameboard)
                if event.key == pygame.K_RIGHT: # increase square count
                    key_held_timer[2] = "right"
                    granularity += 1
                    pixel = resolution / granularity
                    gameboard = set()
                if event.key == pygame.K_LEFT: # decrease square count
                    key_held_timer[2] = "left"
                    granularity -= 1 if granularity > 1 else 0
                    pixel = resolution / granularity
                    gameboard = set()
                if event.key == pygame.K_g:
                    grid_toggle ^= True
                if event.key == pygame.K_s:
                    saveBoard("board.sav", granularity, gameboard)
                if event.key == pygame.K_l:
                    try:
                        gameboard = loadBoard("board.sav")
                        with open("board.sav") as file:
                            line = file.readline()
                        granularity = len(line.strip())
                        pixel = resolution / granularity
                    except Exception as e:
                        print(f"{e}.")
                if event.key == pygame.K_x:
                    gameboard = set()
                if event.key == pygame.K_r:
                    data = randomBoard(granularity)
                    granularity = data[0]
                    pixel = resolution / granularity
                    gameboard = data[1]
                if event.key == pygame.K_h:
                    help_toggle ^= True
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x = floor(pos[0]/resolution * granularity)
                y = floor(pos[1]/resolution * granularity)
                gameboard ^= {(x,y)}

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYUP:
                key_held_timer = [refresh_rate / 3, 0, ""]

        # if left or right has been pressed, count down and start repeating the key.
        if key_held_timer[2] in ["right", "left"]:
            key_held_timer[0] -= 1 if key_held_timer[0] > 0 else 0
            
        if key_held_timer[0] == 0:
            key_held_timer[1] = (key_held_timer[1] + 1) % (refresh_rate * key_repeat // 1000)
            if key_held_timer[1] == 0 and key_held_timer[2] == "right":
                key_held_timer[0] -= 1 if key_held_timer[0] > 0 else 0
                granularity += 1
            elif key_held_timer[1] % key_repeat == 0 and key_held_timer[2] == "left":
                key_held_timer[0] -= 1 if key_held_timer[0] > 0 else 0
                granularity -= 1 if granularity > 1 else 0
            pixel = resolution / granularity
            gameboard = set()

        pygame.display.flip()
        clock.tick(refresh_rate)


def game(granularity: int, pixel: int, gameboard: set):

    pygame.display.set_caption("Conway's Game of Life (PLAYING)")
    timer = 0
    global timestep
    global grid_toggle
    
    while True:

        timer = (timer + 1) % timestep

        # grid and dots.
        screen.fill((255,255,255))
        for (x,y) in gameboard:
            pygame.draw.rect(screen, [0,0,0], (x * pixel, y * pixel, ceil(pixel), ceil(pixel)))
        if grid_toggle:
            drawGrid(granularity, pixel)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    drawingScreen(granularity, pixel, gameboard)
                if event.key == pygame.K_DOWN:
                    timestep += ceil(timestep / 3)
                if event.key == pygame.K_UP:
                    timestep -= floor(timestep / 3) if timestep > 2 else 0
                if event.key == pygame.K_g:
                    grid_toggle ^= True
                if event.key == pygame.K_x:
                    gameboard = set()
                    drawingScreen(granularity, pixel, gameboard)
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x = floor(pos[0]/resolution * granularity)
                y = floor(pos[1]/resolution * granularity)
                gameboard ^= {(x,y)}

            if event.type == pygame.QUIT:
                exit()

        if timer == 0:
            gameboard = iterate(granularity, gameboard)

        pygame.display.flip()
        clock.tick(refresh_rate)

if __name__ == "__main__":
    drawingScreen(granularity, pixel, gameboard)