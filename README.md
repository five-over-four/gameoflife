# Conway's Game of Life
A simple implementation in pygame based on an 'adjacency' algorithm that only keeps track of the 'alive' dots. This means that only the number of dots matters for performance and the size of the board is largely irrelevant.

* GIF mode (press 'I') will allow you to save and share your patterns easily.

* Change your board colour scheme in `config.json`

* Cycle through different dot styles by pressing Enter.

* Custom dot textures as .png files. Sample files included, press 'P' to enable/disable.

## Controls
    Space      -  Play/Pause  
    Up/Down    -  Slow down/Speed up animation  
    Left/Right -  Decrease/Increase dot size (1 pixel increments).  
    G          -  Toggle grid on/off  
    H          -  Toggle the help menu on/off.  
    P          -  Toggle custom texture mode on/off.  
    I          -  Toggle GIF mode on/off. Only works while paused.
    S/L        -  Save or Load a gameboard. Only works while paused.  
    X          -  Clear the board.  
    R          -  Create random board.  
    Enter      -  Switch dot style.  
    Esc        -  Exit.

## Colours
In `config.json`, the bottom three settings let you choose your own colour scheme. The currently available colours are black, white, light grey, grey, dark grey, red, green, blue, purple, yellow, dark red, dark green, dark blue,grey. Behold! Make these yourself with GIF mode.

| Green, Dark Green | Red, Yellow |
| --- | --- |
| ![](https://i.imgur.com/CY5lPSD.gif) | ![](https://i.imgur.com/MtR1k8K.gif) |

## GIF mode
By pressing 'I' while paused, every time you start playing, you will get a new animated .gif file in your extras/gifs directory upon pausing! The setting "gif_speed" in `config.json` determines how much time passes in seconds between each frame in the final animation. The default is 0.2 (5 fps) Press 'I' again to disable GIF mode.

## config.json
While many of these settings can be changed during play, these will always be loaded at startup.

    "x_resolution"            - Horizontal window resolution.  
    "y_resolution"            - Vertical window resolution.  
    "pixel_size"              - Size of each individual dot.  
    "show_controls_at_launch" - Toggles the help menu on/off.  
    "default_show_grid"       - Show/hide grid by default.  
    "default_timestep"        - Number of frames per iteration.  
    "screen_refresh_rate"     - Your monitor's refresh rate. Default 60.  
    "key_repeat_interval"     - Number of milliseconds between held-down key-repeats.  
    "gif_speed"               - Number of seconds between each GIF frame.  
    "dot_colour"              - Colour of each 'live' dot.  
    "bg_colour"               - Colour of the background.  
    "grid_colour"             - Colour of the toggleable grid.

## Features
* The colours are (reasonably) fully customisable!
* The built-in GIF mode will allow you to share your patterns with others easily!
* You can use custom textures for the dots by placing a (square-shaped) alive.png and dead.png in the main directory.
* The window is resizable at any time.
* You can draw by holding down the mouse button while paused.
* The dot size, style, and speed of animation are completely controllable.

![](https://i.imgur.com/OakHazR.gif)