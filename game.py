import pygame
import json
from math import floor, ceil
from random import randint, choice

# colour standards. customise your own in config.json.
colours = { "black": (0,0,0), "white": (255,255,255), "light_grey": (180,180,180), \
            "red": (255,0,0), "green": (0,255,0), "blue": (0,0,255), "purple": (170,0,255), \
            "yellow": (255,255,0), "dark_red": (100,0,0), "dark_green": (0,100,0), \
            "dark_blue": (0,0,150), "grey": (130,130,130), "dark_grey": (60,60,60)
          }

# this loads the settings from config.json, or defaults below.
try:
    with open("config.json") as file:
        data = file.read()
    s = json.loads(data)
    resolution = s["default_resolution"]
    granularity = s["default_granularity"]
    timestep = s["default_timestep"]
    grid_toggle = bool(s["default_show_grid"])
    help_toggle = bool(s["show_controls_at_launch"])
    refresh_rate = s["screen_refresh_rate"]
    key_repeat = s["key_repeat_interval"]
    gif_speed = float(s["gif_speed"])
    dot_colour = colours[s["dot_colour"]]
    bg_colour = colours[s["bg_colour"]]
    grid_colour = colours[s["grid_colour"]]
except:
    resolution = 600
    granularity = 50
    grid_toggle = True
    help_toggle = True
    timestep = 30
    refresh_rate = 60
    key_repeat = 50
    dot_colour = colours["black"]
    bg_colour = colours["white"]
    grid_colour = colours["light_grey"]

# this setting is now toggleable in-game, instead of the .json file.
gif_mode = False

# global components
pygame.init()
screen = pygame.display.set_mode((resolution, resolution))
clock = pygame.time.Clock()

def saveBoard(filename: str, granularity: int, gameboard: set):
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
    density = choice([(0,1), (0,0,1), (0,0,0,1)]) # 50%, 33%, or 25% population of the board at random.
    gameboard = {((randint(0, granularity), randint(0, granularity))) for x in range(granularity**2) if choice(density) == 1}
    return (granularity, gameboard)

def infoSplash():
    pos = (resolution - 400) // 2
    try:
        screen.blit(pygame.image.load("extras/infosplash.png"), (pos, pos))
    except:
        font = pygame.font.SysFont("courier bold", 30)
        text_drawing = font.render("infosplash.png not found!", True, (0,0,0))
        screen.blit(text_drawing, (pos,pos))

def countNeighbors(x: int, y: int, granularity: int, gameboard: set):
    neighbors = 0
    for (dx, dy) in {(-1,-1), (-1,1), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (1,0)}:
            if ((x + dx) % granularity, (y + dy) % granularity) in gameboard:
                neighbors += 1
                if neighbors > 3:
                    return neighbors
    return neighbors

def chooseFate(x: int, y: int, granularity: int, gameboard: set):
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
    for x in range(0, granularity):
        pygame.draw.line(screen, grid_colour, (x * pixel, 0), (x * pixel, resolution), 1)
    for y in range(0, granularity):
        pygame.draw.line(screen, grid_colour, (0, y * pixel), (resolution, y * pixel), 1)

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

def repeatKey(countdown: int, looper: int, direction: int, granularity: int):
    looper = (looper + 1) % (refresh_rate * key_repeat // 1000)
    if looper == 0 and direction == "right":
        countdown -= 1 if countdown > 0 else 0
        granularity += 1
    elif looper % key_repeat == 0 and direction == "left":
        countdown -= 1 if countdown > 0 else 0
        granularity -= 1 if granularity > 1 else 0
    pixel = resolution / granularity
    return (pixel, granularity, looper)

def getMouseXY(granularity: int):
    pos = pygame.mouse.get_pos()
    x = floor(pos[0]/resolution * granularity)
    y = floor(pos[1]/resolution * granularity)
    return (x,y)

def makeGif(): # take .png files, generate .gif, then delete every .png
    dir = "extras/gifs/"
    image_folder = os.fsencode(dir)
    gif_name = 0 # iterate through names.
    files = []

    for filename in os.listdir(dir):
        if filename.endswith(".png"):
            files.append(filename)
        elif filename.endswith(".gif"):
            gif_name += 1

    files = sorted(files, key = lambda x: int(x.split(".")[0]))
    images = list(map(lambda filename: imageio.imread(dir + filename), files))
    imageio.mimsave(os.path.join(dir + str(gif_name) + ".gif"), images, duration = gif_speed)

    for filename in os.listdir(dir): # delete .png files.
        if filename.endswith(".png"):
            os.remove(dir + filename)

def globallyImportModules(): # this is some voodoo.
    global os
    global imageio
    os = __import__("os", globals(), locals())
    imageio = __import__("imageio", globals(), locals())

def pauseScreen(granularity: int, pixel: int, gameboard: set):

    global gif_mode
    global grid_toggle
    global help_toggle
    k_countdown, k_looper, k_dir = refresh_rate // 3, 0, "no direction"
    click_repeat = False # to allow dragging. reset whenever passing over a new square.
    click_toggle = False # is the mouse button depressed or not?
    last_click = (None, None) # keep track of last clicked square.

    if gif_mode == True:
        pygame.display.set_caption("Conway's Game of Life (GIF MODE) (PAUSED)")
    else:
        pygame.display.set_caption("Conway's Game of Life (PAUSED)")

    while True:

        # grid, dots, help splash.
        screen.fill(bg_colour)
        for (x,y) in gameboard:
            pygame.draw.rect(screen, dot_colour, (x * pixel, y * pixel, ceil(resolution/granularity), ceil(resolution/granularity)))
        if grid_toggle:
            drawGrid(granularity, pixel)
        if help_toggle:
            infoSplash()

        # all the event handling happens here.
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                # Play
                if event.key == pygame.K_SPACE:
                    help_toggle = False
                    game(granularity, pixel, gameboard)

                # increase square count
                if event.key == pygame.K_RIGHT:
                    k_dir = "right"
                    granularity += 1
                    pixel = resolution / granularity
                    gameboard = set()

                # decrease square count
                if event.key == pygame.K_LEFT:
                    k_dir = "left"
                    granularity -= 1 if granularity > 1 else 0
                    pixel = resolution / granularity
                    gameboard = set()

                if event.key == pygame.K_g:
                    grid_toggle ^= True
                
                if event.key == pygame.K_h:
                    help_toggle ^= True

                if event.key == pygame.K_s:
                    saveBoard("board.sav", granularity, gameboard)
                    
                if event.key == pygame.K_l:
                    try:
                        gameboard = loadBoard("board.sav")
                        with open("board.sav") as file:
                            line = file.readline()
                        granularity = len(line.strip())
                        pixel = resolution / granularity
                    except Exception as e: # this should be impossible.
                        print(f"{e}.")     # error handling is already done in loadBoard().

                if event.key == pygame.K_x:
                    gameboard = set()

                if event.key == pygame.K_r:
                    data = randomBoard(granularity)
                    granularity = data[0]
                    pixel = resolution / granularity
                    gameboard = data[1]

                # toggle gif mode, change titlebar text, import libraries.
                if event.key == pygame.K_i:
                    try: # needs imageio to work.
                        globallyImportModules()
                        gif_mode ^= True
                        if gif_mode == True:
                            pygame.display.set_caption("Conway's Game of Life (GIF MODE) (PAUSED)")
                        else:
                            pygame.display.set_caption("Conway's Game of Life (PAUSED)")
                    except:
                        print("imageio is required for gif mode to work.\nInstall with 'pip install imageio'.\nProceeding with normal mode.")

                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.QUIT:
                exit()

            # these next three if blocks handle the drag drawing logic.
            if event.type == pygame.KEYUP:
                k_countdown, k_looper, k_dir = refresh_rate // 3, 0, ""

            if event.type == pygame.MOUSEBUTTONDOWN:
                (x,y) = getMouseXY(granularity)
                gameboard ^= {(x,y)}
                last_click = (x,y)
                click_toggle = True
                click_repeat = True

            if event.type == pygame.MOUSEBUTTONUP:
                click_toggle = False
                click_repeat = False

        # check if on a new square from previous click and that the mouse button is down.
        if click_repeat == False and getMouseXY(granularity) != last_click and click_toggle == True:
            click_repeat = True
        else:
            (x,y) = getMouseXY(granularity)
            if (x,y) != last_click and click_toggle == True:
                gameboard ^= {(x,y)}
                last_click = (x,y)

        # if left or right is depressed, start counting down.
        if k_dir in ["right", "left"]:
            k_countdown -= 1 if k_countdown > 0 else 0
            
        # once the countdown is 0, start actually repeating the key.
        if k_countdown == 0:
            data = repeatKey(k_countdown, k_looper, k_dir, granularity)
            pixel, granularity, k_looper = data[0], data[1], data[2]
            gameboard = set()

        pygame.display.flip()
        clock.tick(refresh_rate)


def game(granularity: int, pixel: int, gameboard: set):

    global gif_mode
    global timestep
    global grid_toggle
    timer = 0
    filename = 0 # if gif_mode == True, then generate 0.png, 1.png, 2.png, ...

    if gif_mode == True:
        pygame.display.set_caption("Conway's Game of Life (GIF MODE) (PLAYING)")
    else:
        pygame.display.set_caption("Conway's Game of Life (PLAYING)")
    
    while True:

        timer = (timer + 1) % timestep

        # grid and dots.
        screen.fill(bg_colour)
        for (x,y) in gameboard:
            pygame.draw.rect(screen, dot_colour, (x * pixel, y * pixel, ceil(pixel), ceil(pixel)))
        if grid_toggle:
            drawGrid(granularity, pixel)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    if gif_mode == True and filename > 1:
                        makeGif()
                    pauseScreen(granularity, pixel, gameboard)

                if event.key == pygame.K_DOWN:
                    timestep += ceil(timestep / 3)

                if event.key == pygame.K_UP:
                    timestep -= floor(timestep / 3) if timestep > 2 else 0

                if event.key == pygame.K_g:
                    grid_toggle ^= True

                if event.key == pygame.K_x:
                    gameboard = set()
                    pauseScreen(granularity, pixel, gameboard)

                if event.key == pygame.K_ESCAPE:
                    exit()
            # always deal with gif generation before quitting.
            if event.type == pygame.QUIT:
                if gif_mode == True and filename > 1:
                    makeGif()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = floor(pos[0]/resolution * granularity)
                y = floor(pos[1]/resolution * granularity)
                gameboard ^= {(x,y)}

        if timer == 0:
            gameboard = iterate(granularity, gameboard)
            if gif_mode == True:
                pygame.image.save(screen, "extras/gifs/" + str(filename) + ".png")
                filename += 1

        pygame.display.flip()
        clock.tick(refresh_rate)

if __name__ == "__main__":

    pauseScreen(granularity, resolution / granularity, set())