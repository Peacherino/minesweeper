# Minesweeper
This is a Minesweeper game written in python with a GUI made using pyFLTK.

## Screenshot of Gameplay

## About Project:
One of the greatest focuses of this project is about using recursion to reveal neighbouring
squares in a grid, checking for all blocks that touch a bomb.

I made this project to improve my understanding of recursive functions, for future projects, since
it's a very useful tool when working with multiple connected elements.

## How it works:
The game starts out with a 10 x 10 square grid with 10 randomly placed, hidden bombs.

A player clicks on a square in the grid. If that square is safe, the program checks how many of its
eight possible surrounding squares are bombs. The clicked square then displays the number of bombs
the program counted surrounding it.

If the program does not fing any neighbouring bombs on a surrounding tile, it will recursively reveal
the surrounding squares until it finds squares that border bombs. It skips squares that
have already been revealed so as not to repeatedly reveal them.

The player must use the clues given from the numbers displayed on the squares bordering bombs to
avoid clicking a bomb. To aid in visualizing, players can right-click squares to put flags on suspected
hidden bombs.

## Challenges:
I struggled a lot with figuring out how to implement the recursion process in this project. I
already knew how to use recursion in basic programs, but since this project used a grid and recursed
over everything for every click, it made visualizing what was happening a lot harder.

To get started, I wrote on a paper all of the individual tasks that needed to be completed during
every click of a square so I could mentally organize all of my functions.

## Future improvements:
- Fixing the text display bug so when you resize the window the text doesn't disappear
- Ensuring that the first square clicked is never a bomb
- Keep a record of the player's fastest wins

## How to run it:
#### 1. Start the server
python3 minesweeper.py

#### 2. Gameplay
- Left-click a square to reveal it
- Right-click a square to add/remove a flag
- Reveal all squares that aren't bombs to win
- Lose if a bomb is clicked
- After the game is over, the game displays the completion time
- Game provides option to play again or quit

Resources Used:
- Python
- PyFLTK
- Recursion
- Object-oriented programming
