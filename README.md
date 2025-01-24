# Tetris-with-Pygame
A simple version of Tetris made using the Pygame module for python. This was submitted as my final project for CS121P Intro to Programming.

**Controls:**
Use arrow keys for movement and rotation, C for holding pieces, and SPACE for hard drops. 
ESC is used to pause the game.
Different color palettes are accessible using the number keys(1-7).

Additional Features of Note: 
- When holding a movement key, the first two moves have a longer delay to allow for more precise movement
- The level counter increases per every 10 times the starting level number of lines cleared (starting level must be changed manually).
- The rate at which pieces fall increases based on the current level (the specific formula is based on the one used for tetris worlds).
- Higher scores earned based on number of lines cleared at once, the score earned is multiplied by the current level.
