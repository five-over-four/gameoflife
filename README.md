# Conway's Game of Life (pygame)
A simple implementation based on an 'adjacency' algorithm. We only keep track of the live cells and each iteration check the cells adjacent to them. This means that the board size is effectively irrelevant, as long as the number of live cells is limited. On larger boards (>1000x1000), I recommend you enter dots via the savefile by directly changing the 0s and 1s.

Click to add 'live' dots to the gameboard.

## Controls
    Space      -  Play/Pause  
    Up/Down    -  Slow down/Speed up animation  
    Left/Right -  Decrease/Increase grid granularity  
    G          -  Toggle grid on/off  
    H          -  Toggle the help menu on/off.  
    S/L        -  Save or Load a gameboard. Only works while paused.  
    X          -  Clear the board.  
    R          -  Create random 50x50 board layout.  
    Esc        -  Exit
    
![A simple fork](https://raw.githubusercontent.com/not-legato/gameoflife/main/extras/sample_animation.gif)

## Config.json
    "default_resolution"      - Determines the size of the window (N x N).  
    "default_granularity"     - The grid density of the board.  
    "show_controls_at_launch" - Toggles the help menu on/off.  
    "default_show_grid"       - Show/hide grid by default.  
    "default_timestep"        - Number of frames per iteration.  
    "screen_refresh_rate"     - Your monitor's refresh rate. Default 60.  
    "key_repeat_interval"     - Number of milliseconds between held-down key-repeats.

You can also save your game states into a file or even import a file of your own. The only conditions are that the file consists of 0s and 1s in an n x n grid with no spaces, where n is a natural number.

## Future plans
* Mouse dragging support, so you can draw more freely, more easily.
* One-button insertion of gliders and other standard structures.

(Note that since the gameboard wraps around the edges, small boards are 'smaller' than you may think.)
