# minesweeper-final-project
Georgia Tech's CS3510 course offered in the Spring 2021 semester, taught by Constantine Dovrolis, had a programming project in place of a final exam. This final project required students to design and implement two different non-trivial algorithms for the Minesweeper problem. Our team chose to implement this programming project in Python. 

## How to Play
Basic gameplay allows a user to make a move by his or herself or select one of the two AIs to play for themself. 

## Submission Information
Group Members: 
- Rhiannan Wackes (rwackes3@gatech.edu)
- Grace Dwyer (graceyd@gatech.edu)
- Josh George (joshgeorge@gatech.edu)

Date of Submission: Sunday, May 2nd, 2021

### Files Submitted: 
- minesweeperAI1.py: An algorithm that solves the Minesweeper problem using DFS.
- minesweeperAI2.py: An algorithm that solves the Minesweeper problem using the naive single point start approach.
- minesweeperGameEngine.py: A GUI game engine for the Minesweeper game that allows a user to select an AI algorithm to search the grid space for the set of mines.
- minesweeperPerformanceTest.py: A script where you can specify the board size, number of bombs, safe starting square, the type of AI to use (1 or 2), and the number of games to play.
- deterministic_board.json: - An (example) JSON configuration file that can be passed to minesweeperGameEngine.py. 

## Running
Inside the command line terminal, type and enter
```
python3 minesweeperGameEngine.py
```
This line will make the GUI appear and allow the user to play the Minesweeper game upon selecting which algorithm out of the two to use behind the scenes. The default board used is the one in test_board.json. 

You can play on different boards. For example, to play Minesweeper on the board detailed in deterministic_board.json, type and enter
```
python3 minesweeperGameEngine.py -f deterministic_board.json
```

## Known Bugs or Limitations
- None
