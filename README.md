# Conway's Game of Life (pygame)
A simple implementation based on an 'adjacency' algorithm. We only keep track of the live cells and each iteration check the cells adjacent to them. This means that the board size is effectively irrelevant, as long as the number of live cells is limited.

* Click to add 'live' dots to the gameboard. Drawing by dragging is now supported!

* A newly added GIF mode will allow you to easily save your animations as .gifs with ease! (this uses imageio)

## Controls
    Space      -  Play/Pause  
    Up/Down    -  Slow down/Speed up animation  
    Left/Right -  Decrease/Increase grid granularity  
    G          -  Toggle grid on/off  
    H          -  Toggle the help menu on/off.  
    I          -  Toggle GIF mode on/off. Only works while paused.
    S/L        -  Save or Load a gameboard. Only works while paused.  
    X          -  Clear the board.  
    R          -  Create random 50x50 board layout.  
    Esc        -  Exit

## Colours
In config.json, the bottom three settings let you choose your own colour scheme. The currently available colours are black, white, light grey, grey, dark grey, red, green, blue, purple, yellow, dark red, dark green, dark blue,grey. Behold! Make these yourself with the GIF mode.

| Green, Dark Green | Red, Yellow |
| --- | --- |
| ![](https://i.imgur.com/CY5lPSD.gif) | ![woops](https://i.imgur.com/MtR1k8K.gif) |

## GIF mode
By pressing 'I' while paused, every time you start playing, you will get a new animated .gif file in your extras/gifs directory! Just draw a shape, load an existing board, or randomise it, press play, and once you pause, a new animation awaits. The setting "gif_speed" in config.json determines how much time passes (in seconds) between each frame in the final animation. Press 'I' again to disable GIF mode.

## Config.json
    "default_resolution"      - Determines the size of the window (N x N).  
    "default_granularity"     - The grid density of the board.  
    "show_controls_at_launch" - Toggles the help menu on/off.  
    "default_show_grid"       - Show/hide grid by default.  
    "default_timestep"        - Number of frames per iteration.  
    "screen_refresh_rate"     - Your monitor's refresh rate. Default 60.  
    "key_repeat_interval"     - Number of milliseconds between held-down key-repeats.
    "dot_colour"              - Colour of each 'live' dot.
    "bg_colour"               - Colour of the background.
    "grid_colour"             - Colour of the toggleable grid.

You can also save your game states into a file or even import a file of your own. The only conditions are that the file consists of 0s and 1s in an n x n grid with no spaces, where n is a natural number.

## Features
* The colours are (reasonably) fully customisable!
* The built-in GIF mode will allow you to share your patterns with others easily!
* You can draw by holding down the mouse button while paused.
* The board is resizable by holding down either left or right.

## Future plans
* One-button insertion of gliders and other standard structures.
* Possibly dragging the board around.