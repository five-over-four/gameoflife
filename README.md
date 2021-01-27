# Conway's Game of Life (pygame)
A simple implementation based on an 'adjacency' algorithm. We only keep track of the live cells and each iteration check the cells adjacent to them. This means that only the number of dots matters, not the size of the board.

* Click to add 'live' dots to the gameboard. Drawing by dragging is now supported!

* The window is fully resizable: there's complete support for any size!

* A newly added GIF mode will allow you to easily save your animations as GIFs with ease! (this uses imageio)

* Change the style of dots on the board by pressing Enter.

## Controls
    Space      -  Play/Pause  
    Up/Down    -  Slow down/Speed up animation  
    Left/Right -  Decrease/Increase dot size (1 pixel increments).  
    G          -  Toggle grid on/off  
    H          -  Toggle the help menu on/off.  
    I          -  Toggle GIF mode on/off. Only works while paused.
    S/L        -  Save or Load a gameboard. Only works while paused.  
    X          -  Clear the board.  
    R          -  Create random noise.  
    Enter      -  Switch dot style.
    Esc        -  Exit.

## Colours
In config.json, the bottom three settings let you choose your own colour scheme. The currently available colours are black, white, light grey, grey, dark grey, red, green, blue, purple, yellow, dark red, dark green, dark blue,grey. Behold! Make these yourself with the GIF mode.

| Green, Dark Green | Red, Yellow |
| --- | --- |
| ![](https://i.imgur.com/CY5lPSD.gif) | ![](https://i.imgur.com/MtR1k8K.gif) |

## GIF mode
By pressing 'I' while paused, every time you start playing, you will get a new animated .gif file in your extras/gifs directory! Just draw a shape, load an existing board, or randomise it, press play, and once you pause, a new animation awaits. The setting "gif_speed" in config.json determines how much time passes (in seconds) between each frame in the final animation. Press 'I' again to disable GIF mode.

## Config.json
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

You can also save your game states into a file or even import a file of your own. The only conditions are that the file consists of 0s and 1s in a rectangular grid.

## Features
* The colours are (reasonably) fully customisable!
* The built-in GIF mode will allow you to share your patterns with others easily!
* The window is resizable at any time.
* You can draw by holding down the mouse button while paused.
* The dot size, style, and speed of animation are completely controllable.

![](https://i.imgur.com/OakHazR.gif)