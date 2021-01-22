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
    with open("experimental_config.json") as file:
        data = file.read()
    s = json.loads(data)
    width = s["x_resolution"]
    height = s["y_resolution"]
    dot = s["pixel_size"]
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
    width = 600
    height = 600
    dot = 10
    grid_toggle = True
    help_toggle = True
    timestep = 30
    refresh_rate = 60
    key_repeat = 50
    dot_colour = colours["black"]
    bg_colour = colours["white"]
    grid_colour = colours["light_grey"]

gif_mode = False # gotta initialise this for global use.

# global components. resizable window is a REAL pain to deal with.
pygame.init()
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
clock = pygame.time.Clock()

def saveBoard(filename: str, dot: int, x_dots: int, y_dots: int, gameboard: set):
    with open(filename, "w") as overwrite:
        overwrite.write("")
    with open(filename, "a") as file:
        for y in range(y_dots):
            for x in range(x_dots):
                if (x,y) not in gameboard:
                    file.write("0")
                else:
                    file.write("1")
            file.write("\n")

def loadBoard(filename: str):
    gameboard = set()
    with open(filename) as file:
        lines = file.readlines()
    y_dots = len(lines)
    x_dots = len(lines[0].strip())
    for y in range(y_dots):
        for x in range(x_dots):
            if lines[y][x] == "1":
                gameboard.add((x,y))
    return x_dots, y_dots, gameboard

def randomBoard(dot: int):
    density = choice([(0,1), (0,0,1), (0,0,0,1)]) # 50%, 33%, or 25% population of the board at random.
    n_dots = (width // dot) * (height // dot)
    gameboard = {((randint(0, width // dot - 1), randint(0, height // dot - 1))) for x in range(n_dots) if choice(density) == 1}
    return gameboard

def infoSplash():
    x_pos = (width - 400) // 2 # the splash image is 400 x 399.
    y_pos = (height - 399) // 2
    try:
        screen.blit(pygame.image.load("extras/infosplash.png"), (x_pos, y_pos))
    except:
        font = pygame.font.SysFont("courier bold", 30)
        text_drawing = font.render("infosplash.png not found!", True, (0,0,0))
        screen.blit(text_drawing, (x_pos, y_pos))

def countNeighbors(x: int, y: int, x_dots: int, y_dots: int, gameboard: set):
    neighbors = 0
    for (dx, dy) in {(-1,-1), (-1,1), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (1,0)}:
        if ((x + dx) % x_dots, (y + dy) % y_dots) in gameboard:
            neighbors += 1
            if neighbors > 3:
                return neighbors
    return neighbors

def chooseFate(x: int, y: int, x_dots: int, y_dots, gameboard: set):
    neighbors = countNeighbors(x, y, x_dots, y_dots, gameboard)
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

def iterate(dot: int, x_dots: int, y_dots: int, gameboard: set):
    fates = set()
    for (x,y) in gameboard:
        fates.add(chooseFate(x, y, x_dots, y_dots, gameboard))
        for (dx, dy) in {(-1,-1), (-1,1), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (1,0)}:
            fates.add(chooseFate((x + dx) % x_dots, (y + dy) % y_dots, x_dots, y_dots, gameboard))
    try:
        fates.remove(0)
        return fates
    except:
        return fates

def drawGrid(dot: int, x_dots: int, y_dots: int, width: int, height: int):
    for x in range(0, x_dots):
        pygame.draw.line(screen, grid_colour, (x * dot, 0), (x * dot, height), 1)
    for y in range(0, y_dots):
        pygame.draw.line(screen, grid_colour, (0, y * dot), (width, y * dot), 1)

def repeatKey(countdown: int, looper: int, direction: int, dot: int):
    looper = (looper + 1) % (refresh_rate * key_repeat // 1000)
    if looper == 0 and direction == "right":
        countdown -= 1 if countdown > 0 else 0
        dot += 1
    elif looper % key_repeat == 0 and direction == "left":
        countdown -= 1 if countdown > 0 else 0
        dot -= 1 if dot > 1 else 0
    return (dot, looper)

def getMouseXY(dot: int, width: int, height: int):
    pos = pygame.mouse.get_pos()
    x = floor(pos[0]/ dot)
    y = floor(pos[1]/ dot)
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

def pauseScreen(dot: int, x_dots: int, y_dots: int, gameboard: set):

    global width
    global height
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
            pygame.draw.rect(screen, dot_colour, (x * dot, y * dot, dot, dot))
        if grid_toggle:
            drawGrid(dot, x_dots, y_dots, width, height)
        if help_toggle:
            infoSplash()

        # all the event handling happens here.
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                # Play
                if event.key == pygame.K_SPACE:
                    help_toggle = False
                    game(dot, x_dots, y_dots, gameboard)

                # increase square count
                elif event.key == pygame.K_RIGHT:
                    k_dir = "right"
                    dot += 1
                    x_dots = width // dot
                    y_dots = height // dot
                    gameboard = set()

                # decrease square count
                elif event.key == pygame.K_LEFT:
                    k_dir = "left"
                    dot -= 1 if dot > 1 else 0
                    x_dots = width // dot
                    y_dots = height // dot
                    gameboard = set()

                elif event.key == pygame.K_g:
                    grid_toggle ^= True
                
                elif event.key == pygame.K_h:
                    help_toggle ^= True

                elif event.key == pygame.K_s:
                    saveBoard("board.sav", dot, x_dots, y_dots, gameboard)
                    
                elif event.key == pygame.K_l:
                    try:
                        data = loadBoard("board.sav")
                        x_dots, y_dots, gameboard = data[0], data[1], data[2]       
                        dot = ceil(width / x_dots) # size based on width, not height.
                    except Exception as e: # this should be impossible.
                        print(f"{e}.")     # error handling is already done in loadBoard().

                elif event.key == pygame.K_x:
                    gameboard = set()

                elif event.key == pygame.K_r:
                    gameboard = randomBoard(dot)

                # toggle gif mode, change titlebar text, import libraries.
                elif event.key == pygame.K_i:
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

            # these next three if blocks handle the drag drawing logic.
            elif event.type == pygame.KEYUP:
                k_countdown, k_looper, k_dir = refresh_rate // 3, 0, ""

            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x,y) = getMouseXY(dot, width, height)
                gameboard ^= {(x,y)}
                last_click = (x,y)
                click_toggle = True
                click_repeat = True

            elif event.type == pygame.MOUSEBUTTONUP:
                click_toggle = False
                click_repeat = False

            elif event.type == pygame.VIDEORESIZE:
                gameboard = set()
                width, height = event.w, event.h
                x_dots, y_dots = width // dot, height // dot

            elif event.type == pygame.QUIT:
                exit()

        # check if on a new square from previous click and that the mouse button is down.
        if click_repeat == False and getMouseXY(dot, width, height) != last_click and click_toggle == True:
            click_repeat = True
        else:
            (x,y) = getMouseXY(dot, width, height)
            if (x,y) != last_click and click_toggle == True:
                gameboard ^= {(x,y)}
                last_click = (x,y)

        # if left or right is depressed, start counting down.
        if k_dir in ["right", "left"]:
            k_countdown -= 1 if k_countdown > 0 else 0
            
        # once the countdown is 0, start actually repeating the key.
        if k_countdown == 0:
            data = repeatKey(k_countdown, k_looper, k_dir, dot)
            dot, k_looper = data[0], data[1]
            gameboard = set()

        pygame.display.flip()
        clock.tick(refresh_rate)


def game(dot: int, x_dots: int, y_dots: int, gameboard: set):

    global width
    global height
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
            pygame.draw.rect(screen, dot_colour, (x * dot, y * dot, dot, dot))
        if grid_toggle:
            drawGrid(dot, x_dots, y_dots, width, height)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    if gif_mode == True and filename > 1:
                        makeGif()
                    pauseScreen(dot, x_dots, y_dots, gameboard)

                elif event.key == pygame.K_UP:
                    timestep -= floor(timestep / 3) if timestep > 2 else 0

                elif event.key == pygame.K_DOWN:
                    timestep += ceil(timestep / 3)

                elif event.key == pygame.K_g:
                    grid_toggle ^= True

                elif event.key == pygame.K_x:
                    gameboard = set()
                    pauseScreen(dot, x_dots, y_dots, gameboard)

                elif event.key == pygame.K_ESCAPE:
                    exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                gameboard ^= {getMouseXY(dot, width, height)}

            elif event.type == pygame.VIDEORESIZE:
                gameboard = set()
                width, height = event.w, event.h
                x_dots, y_dots = width // dot, height // dot

            # always deal with gif generation before quitting.
            elif event.type == pygame.QUIT:
                if gif_mode == True and filename > 1:
                    makeGif()
                exit()

        if timer == 0:
            gameboard = iterate(dot, x_dots, y_dots, gameboard)
            if gif_mode == True:
                pygame.image.save(screen, "extras/gifs/" + str(filename) + ".png")
                filename += 1

        pygame.display.flip()
        clock.tick(refresh_rate)

if __name__ == "__main__":

    pauseScreen(dot, width // dot, height // dot, set())