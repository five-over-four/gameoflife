import pygame
import json
from math import ceil
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
    refresh_rate = s["screen_refresh_rate"]
    key_repeat = s["key_repeat_interval"]
    gif_speed = float(s["gif_speed"])
    dot_colour = colours[s["dot_colour"]]
    bg_colour = colours[s["bg_colour"]]
    grid_colour = colours[s["grid_colour"]]
except:
    refresh_rate = 60
    key_repeat = 50
    dot_colour = colours["black"]
    bg_colour = colours["white"]
    grid_colour = colours["light_grey"]

# this class deals with the movement of the board and all of its 'physical' attributes
# such as resolution, dot size, dot count, toggles. struct.
class Board():
    def __init__(self):
        try:
            with open("config.json") as file:
                data = file.read()
            s = json.loads(data)
            self.width = s["x_resolution"]
            self.height = s["y_resolution"]
            self.dot = s["pixel_size"]
            self.timestep = s["default_timestep"]
            self.grid_toggle = bool(s["default_show_grid"])
            self.help_toggle = bool(s["show_controls_at_launch"])
        except:
            self.width = 600
            self.height = 400
            self.dot = 10
            self.grid_toggle = True
            self.help_toggle = True
            self.timestep = 30
        self.x_dots = self.width // self.dot
        self.y_dots = self.height // self.dot
        self.gameboard = set()
        self.gif_mode = False

    # generate 'random' board layout.
    def random(self):
        density = choice([(0,1), (0,0,1), (0,0,0,1)]) # 50%, 33%, or 25% population of the board at random.
        n_dots = self.x_dots * self.y_dots
        self.gameboard = {((randint(0, self.width // self.dot - 1), randint(0, self.height // self.dot - 1))) for x in range(n_dots) if choice(density) == 1}

    def set_dots(self):
        self.x_dots = self.width // self.dot
        self.y_dots = self.height // self.dot
        self.gameboard = set()

    def save(self):
        with open("board.sav", "w") as overwrite:
            overwrite.write("")
        with open("board.sav", "a") as file:
            for y in range(self.y_dots):
                for x in range(self.x_dots):
                    if (x,y) not in selrf.gameboard:
                        file.write("0")
                    else:
                        file.write("1")
                file.write("\n")
                
    def load(self):
        try:
            with open("board.sav") as file:
                lines = file.readlines()
            self.gameboard = set()
            self.y_dots = len(lines)
            self.x_dots = len(lines[0].strip())
            for y in range(self.y_dots):
                for x in range(self.x_dots):
                    if lines[y][x] == "1":
                        self.gameboard.add((x,y))
            self.dot = ceil(self.width / self.x_dots)
        except Exception as e:
            print(e)

    def iterate(self):
        fates = set()
        for (x,y) in self.gameboard:
            fates.add(chooseFate(x, y, self))
            for (dx, dy) in {(-1,-1), (-1,1), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (1,0)}:
                fates.add(chooseFate((x + dx) % self.x_dots, (y + dy) % self.y_dots, self))
        try:
            fates.remove(0)
            self.gameboard = fates
        except:
            self.gameboard = fates

# these standalone functions could've been also built-in to the Board class, but i felt
# that it would be a bit excessive, and not necessarily make the code any more readable.

# display the controls page at the *center* of the screen.
def infoSplash(board: Board):
    x_pos = (board.width - 400) // 2 # the splash image is 400 x 399.
    y_pos = (board.height - 399) // 2
    try:
        screen.blit(pygame.image.load("extras/infosplash.png"), (x_pos, y_pos))
    except:
        font = pygame.font.SysFont("courier bold", 30)
        text_drawing = font.render("extras/infosplash.png not found!", True, (0,0,0))
        screen.blit(text_drawing, (0, 0))

def countNeighbors(x: int, y: int, board: Board):
    neighbors = 0
    for (dx, dy) in {(-1,-1), (-1,1), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (1,0)}:
        if ((x + dx) % board.x_dots, (y + dy) % board.y_dots) in board.gameboard: # loop around edges.
            neighbors += 1
            if neighbors > 3: # save some time in busy areas.
                return neighbors
    return neighbors

def chooseFate(x: int, y: int, board: Board):
    neighbors = countNeighbors(x, y, board)
    if (x,y) not in board.gameboard:
        if neighbors == 3:
            return (x,y)
        else:
            return 0
    else:
        if neighbors < 2 or neighbors > 3:
            return 0
        else:
            return (x,y)

def drawGrid(board: Board):
    for x in range(0, board.x_dots):
        pygame.draw.line(screen, grid_colour, (x * board.dot, 0), (x * board.dot, board.height), 1)
    for y in range(0, board.y_dots):
        pygame.draw.line(screen, grid_colour, (0, y * board.dot), (board.width, y * board.dot), 1)

def repeatKey(countdown: int, looper: int, direction: int, dot: int):
    looper = (looper + 1) % (refresh_rate * key_repeat // 1000)
    if looper == 0 and direction == "right":
        countdown -= 1 if countdown > 0 else 0
        dot += 1
    elif looper % key_repeat == 0 and direction == "left":
        countdown -= 1 if countdown > 0 else 0
        dot -= 1 if dot > 1 else 0
    return (dot, looper)

def getMouseXY(board: Board):
    pos = pygame.mouse.get_pos()
    x = pos[0] // board.dot
    y = pos[1] // board.dot
    return (x,y)

def makeGif(): # take .png files, generate .gif, then delete every .png
    import os
    import imageio
    dir = "extras/gifs/"
    image_folder = os.fsencode(dir)
    gif_name = 0 # iterate through names 0.gif, 1.gif, ...
    files = []

    for filename in os.listdir(dir): # find .png filenames.
        if filename.endswith(".png"):
            files.append(filename)
        elif filename.endswith(".gif"):
            gif_name += 1

    files = sorted(files, key = lambda x: int(x.split(".")[0])) # make .gif.
    images = list(map(lambda filename: imageio.imread(dir + filename), files))
    imageio.mimsave(os.path.join(dir + str(gif_name) + ".gif"), images, duration = gif_speed)

    for filename in os.listdir(dir): # delete .png files.
        if filename.endswith(".png"):
            os.remove(dir + filename)

def pause(board: Board):

    k_countdown, k_looper, k_dir = refresh_rate // 3, 0, "no direction"
    click_repeat = False # to allow dragging. reset whenever passing over a new square.
    click_toggle = False # is the mouse button depressed or not?
    last_click = (None, None) # keep track of last clicked square.

    if board.gif_mode == True:
        pygame.display.set_caption("Conway's Game of Life (GIF MODE) (PAUSED)")
    else:
        pygame.display.set_caption("Conway's Game of Life (PAUSED)")

    while True:

        # grid, dots, help splash.
        screen.fill(bg_colour)
        for (x,y) in board.gameboard:
            pygame.draw.rect(screen, dot_colour, (x * board.dot, y * board.dot, board.dot, board.dot))
        if board.grid_toggle:
            drawGrid(board)
        if board.help_toggle:
            infoSplash(board)

        # all the event handling happens here.
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                # Play
                if event.key == pygame.K_SPACE:
                    board.help_toggle = False
                    game(board)

                # increase square count
                elif event.key == pygame.K_RIGHT:
                    k_dir = "right"
                    board.dot += 1
                    board.set_dots()

                # decrease square count
                elif event.key == pygame.K_LEFT:
                    k_dir = "left"
                    board.dot -= 1 if board.dot > 1 else 0
                    board.set_dots()

                elif event.key == pygame.K_g:
                    board.grid_toggle ^= True
                
                elif event.key == pygame.K_h:
                    board.help_toggle ^= True

                elif event.key == pygame.K_s:
                    board.save()
                    
                elif event.key == pygame.K_l:
                    board.load()

                elif event.key == pygame.K_x:
                    board.gameboard = set()

                elif event.key == pygame.K_r:
                    board.random()

                # toggle gif mode, change titlebar text, import libraries.
                elif event.key == pygame.K_i:
                    try: 
                        import imageio # needs imageio to work.
                        gif_mode ^= True
                        if gif_mode == True:
                            pygame.display.set_caption("Conway's Game of Life (GIF MODE) (PAUSED)")
                        else:
                            pygame.display.set_caption("Conway's Game of Life (PAUSED)")
                    except:
                        print("imageio is required for gif mode to work.\nInstall with 'pip install imageio'.\nProceeding with normal mode.")

                if event.key == pygame.K_ESCAPE:
                    exit()

            elif event.type == pygame.KEYUP:
                k_countdown, k_looper, k_dir = refresh_rate // 3, 0, ""

            # placing a new dot by clicking.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x,y) = getMouseXY(board)
                board.gameboard ^= {(x,y)}
                last_click = (x,y)
                click_toggle = True
                click_repeat = True

            # persistent memory of whether click is depressed.
            elif event.type == pygame.MOUSEBUTTONUP:
                click_toggle = False
                click_repeat = False

            elif event.type == pygame.VIDEORESIZE:
                board.width, board.height = event.w, event.h
                board.set_dots()

            elif event.type == pygame.QUIT:
                exit()

        # check if on a new square from previous click and that the mouse button is down.
        if click_repeat == False and getMouseXY(board) != last_click and click_toggle == True:
            click_repeat = True
        else:
            (x,y) = getMouseXY(board)
            if (x,y) != last_click and click_toggle == True:
                board.gameboard ^= {(x,y)}
                last_click = (x,y)

        # if left or right is depressed, start counting down.
        if k_dir in ["right", "left"]:
            k_countdown -= 1 if k_countdown > 0 else 0
            
        # once the countdown is 0, start actually repeating the key.
        if k_countdown == 0:
            data = repeatKey(k_countdown, k_looper, k_dir, board.dot)
            board.dot, k_looper = data[0], data[1]
            board.set_dots()

        pygame.display.flip()
        clock.tick(refresh_rate)

def game(board):

    timer = 0
    filename = 0 # if gif_mode == True, then generate 0.png, 1.png, 2.png, ...

    if board.gif_mode == True:
        pygame.display.set_caption("Conway's Game of Life (GIF MODE) (PLAYING)")
    else:
        pygame.display.set_caption("Conway's Game of Life (PLAYING)")
    
    while True:

        timer = (timer + 1) % board.timestep

        # grid and dots.
        screen.fill(bg_colour)
        for (x,y) in board.gameboard:
            pygame.draw.rect(screen, dot_colour, (x * board.dot, y * board.dot, board.dot, board.dot))
        if board.grid_toggle:
            drawGrid(board)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    if board.gif_mode == True and filename > 1:
                        makeGif()
                    pause(board)

                elif event.key == pygame.K_UP:
                    board.timestep -= board.timestep // 3 if board.timestep > 2 else 0

                elif event.key == pygame.K_DOWN:
                    board.timestep += ceil(board.timestep / 3)

                elif event.key == pygame.K_g:
                    board.grid_toggle ^= True

                elif event.key == pygame.K_x:
                    board.gameboard = set()
                    pause(board)

                elif event.key == pygame.K_ESCAPE:
                    exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.gameboard ^= {getMouseXY(board)}

            elif event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                board.set_dots()

            # always deal with gif generation before quitting.
            elif event.type == pygame.QUIT:
                if gif_mode == True and filename > 1:
                    makeGif()
                exit()

        if timer == 0:
            board.iterate()
            if board.gif_mode == True:
                pygame.image.save(screen, "extras/gifs/" + str(filename) + ".png")
                filename += 1

        pygame.display.flip()
        clock.tick(refresh_rate)

if __name__ == "__main__":
    board = Board()
    pygame.init()
    screen = pygame.display.set_mode((board.width, board.height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pause(board)