import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
from tkinter import *
import random
import minesweeperAI1 
import minesweeperAI2
import json
import argparse

# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, testcase_filename, master=None):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.outcome = 0

        with open(testcase_filename) as fp:
            data = json.load(fp)
        
        boardSize = data['dim'].split(',')
        safe = data['safe'].split(',')

        # game variables that can be accessed in any method in the class. For example, to access the number of rows, use "self.numRows"         
        self.numRows = int(boardSize[0])
        self.numCols = int(boardSize[1])
        self.numBombs = int(data['bombs'])
        self.safeSquare = (int(safe[0]), int(safe[1]))
        self.gridInput = data['board']

        print(self.numRows, self.numCols, self.numBombs, self.safeSquare, self.gridInput)

        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget      
        self.master.title("Minesweeper")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        
        self.button = []
        for row in range(self.numRows):
            curRow = []
            for col in range(self.numCols):
                curRow.append(Button(self, bg="gray", width=2, height=1, command=lambda rw=row, cl=col: self.open_button(rw, cl)))
                curRow[col].grid(row=row, column=col)
            self.button.append(curRow)

        self.create_board()
        AIAlgo1Button = Button(self, bg="blue", text="AI 1", width=6, height=5, command=self.AIAlgo1)
        AIAlgo1Button.place(x=600, y=150)
        self.AI1 = minesweeperAI1.AI1(self.numRows, self.numCols, self.numBombs, self.safeSquare)

        AIAlgo2Button = Button(self, bg="blue", text="AI 2", width=6, height=5, command=self.AIAlgo2)
        AIAlgo2Button.place(x=600, y=350)
        self.AI2 = minesweeperAI2.AI2(self.numRows, self.numCols, self.numBombs, self.safeSquare)

        self.highlight_button(self.safeSquare)

    # (DO NOT MODIFY): uncover a square and perform appriopriate action based on game rule
    def open_button(self, r, c):

        if not self.squareInBounds(r, c):
            return

        self.button[r][c].config(state="disabled")
        if self.ans[r][c] != 9:
            self.button[r][c]["text"] = self.ans[r][c]
            self.button[r][c]["bg"] = "white"
        else:
            self.button[r][c]["text"] = self.ans[r][c]
            self.button[r][c]["bg"] = "red"

    # (helper function): return true if and only if all non-bomb squares have been uncovered (game is won) 
    def isGameWon(self):
        cnt = 0
        for row in range(self.numRows):
            for col in range(self.numCols):
                if self.button[row][col]['state'] != 'disabled': cnt += 1
        return cnt == self.numBombs

    # (helper function): return true if and only if a square (r, c) is within the game grid
    def squareInBounds(self, r, c):
        return r >= 0 and c >= 0 and r < self.numRows and c < self.numCols

    # (helper function): return true if and only if the board has all covered (unopened) squares
    def isNewBoard(self):
        for row in range(self.numRows):
            for col in range(self.numCols):
                if self.button[row][col]['state'] == 'disabled':
                    return False
        return True   

    # (helper function): change the color of specified square to blue to indicate this is the square you will select next
    def highlight_button(self, square):
        if self.squareInBounds(square[0], square[1]):
            self.button[square[0]][square[1]]["bg"] = "blue"  

    # (helper function): get the current board state from player POV. Note -1 represents unknown square
    def getBoardState(self):
        board = np.full((self.numRows, self.numCols), -1)
        for row in range(self.numRows):
            for col in range(self.numCols):
                value = 0
                if self.button[row][col]['state'] == 'disabled':
                    if self.button[row][col]["text"] != "":
                        value = int(self.button[row][col]["text"])
                    board[row][col] = value
        return board

    # generate a board based on test case input
    def create_board(self):

        self.ans = np.full((self.numRows, self.numCols), 0)
        self.bombLocations = []
        # Add numbers 0-8 to the ans grid 
        for row in range(self.numRows):
            for col in range(self.numCols):
                self.ans[row][col] = self.gridInput[row * self.numCols + col]
                if self.ans[row][col] == 9:
                    self.bombLocations.append((row, col))

        print(f"starting board\n{self.ans}")
        print(f"location of bombs: {self.bombLocations}")

    # parse the user's command and perform the appropriate action.
    def parseAIAlgo(self, userCommand):
        if type(userCommand) is not tuple:
            print("cannot parse command")
        elif "open_square" in userCommand[0]:
            self.nextSquareToOpen = userCommand[1]
            self.highlight_button(self.nextSquareToOpen)
        elif "final_answer" in userCommand[0]:
            userAnswer = userCommand[1]
            self.numDigs = np.count_nonzero(self.getBoardState() != -1)
            if set(self.bombLocations) == set(userAnswer):
                self.outcome = 1
                print(f"CORRECT BOMB LIST! You performed {self.numDigs} digs")
            else:
                self.outcome = -1
                print(f"WRONG BOMB LIST. expected: {self.bombLocations}, received: {userAnswer}. You performed {self.numDigs} digs")


    def DFS(self, boardState, visited, mines, x, y):
        if (len(mines) == self.numBombs): 
            return mines
    
        # add currently selected square to visited set
        visited.add((x, y))
        # uncover the currently selected square
        if (x, y) != self.safeSquare:
            # mark one dig
            boardState = self.getBoardState()
            self.open_button(x, y)
        
        # retrieve the value of the opened selected square
        label = self.ans[x][y]
        
        if label == 9: 
            mines.append((x, y))

        dx = [-1, 1, -1, 0, 1, -1, 0, 1]
        dy = [0, 0, -1, -1, -1, 1, 1, 1]

        for i in range(len(dx)):
            safe, uncovered = self.AI1.isSafeAndUncovered((x + dx[i], y + dy[i]), visited)
            if safe and uncovered:
                self.DFS(boardState, visited, mines, x + dx[i], y + dy[i])

        if (len(mines) == self.numBombs): 
            return mines


    """
    Each time you click the button, We would recommend you to perform the following loop in your algorithm:
    1) uncover the best square computed last iteration using `self.open_button(r, c)`. Note a safe square is given for the first iteration
    2) perform your algorithm to find the best square using performAI1()
    3) visually display the square you will select on the next iteration (blue square) using self.highlight_button(r, c)
    """
    def AIAlgo1(self):
        if self.outcome != 0:
            return # game is already over (won or loss)

        if self.isNewBoard():
            self.open_button(self.safeSquare[0], self.safeSquare[1])
        else:
            self.open_button(self.nextSquareToOpen[0], self.nextSquareToOpen[1])

        if self.outcome != 0:
            return # game is already over (won or loss)
        
        boardState = self.getBoardState()
        visited_set = set()
        mines = []
        mines = self.DFS(boardState, visited_set, mines, self.safeSquare[0], self.safeSquare[1])
        self.parseAIAlgo(self.AI1.submit_final_answer_format(mines))

    def AIAlgo2(self):
        if self.outcome != 0:
            return # game is already over (won or loss)

        # marks one dig/click of the AI2 button
        boardState = self.getBoardState()

        if self.isNewBoard():
            self.open_button(self.safeSquare[0], self.safeSquare[1])
            # find all the unopened squares
            unopenedSquares = []
            for row in range(self.numRows):
                for col in range(self.numCols):
                    if boardState[row][col] == -1:
                        unopenedSquares.append((row, col))
            # if the number of unopened squares is equal to the number of bombs, all squares must be bombs
            if len(unopenedSquares) == self.numBombs:
                print(f"List of bombs is {unopenedSquares}")
                self.parseAIAlgo(self.AI2.submit_final_answer_format(unopenedSquares))
        else:
            self.open_button(self.nextSquareToOpen[0], self.nextSquareToOpen[1])
        
        if self.outcome != 0:
            return # game is already over (won or loss)

        print(boardState)
        mines = []
        open = [self.safeSquare]
        clear = []
        squares_left = []

        # while there is a square to explore 
        while len(open) != 0:
            if (len(mines) == self.numBombs):
                self.parseAIAlgo(self.AI2.submit_final_answer_format(mines))
                return
            
            # find all the unopened squares
            unopenedSquares = []
            for row in range(self.numRows):
                for col in range(self.numCols):
                    if boardState[row][col] == -1:
                        unopenedSquares.append((row, col))
    
            # select a square
            centerSquare = open.pop() 
            print(f"Square currently open is {centerSquare}")
            print(f"Square currently open is {centerSquare[0], centerSquare[1]}")

            # uncover the currently selected square
            if centerSquare != self.safeSquare:
                # mark one dig
                boardState = self.getBoardState()
                self.open_button(centerSquare[0], centerSquare[1])

            # find the value of the uncovered square
            label = self.ans[centerSquare[0]][centerSquare[1]]
            print(f"Label of square currently open is {label}")

            # find the effective label of the uncovered square = value of the uncovered square minus the numer of neighboring mines already accounted for
            effectiveLabel = label - self.AI2.find_num_nearby_mines(centerSquare, boardState)
            print(f"Effective label of square currently open is {effectiveLabel}")

            # find all unopened squares that are neighbors of the given centerSquare
            neighbors = self.AI2.find_unopened_neighbors(centerSquare, boardState)
            print(f"Neighbors of square currently open are {neighbors}")

            # the opened selected square is a mine
            if label == 9:
                mines.append(centerSquare)

            # the opened selected square has no mines nearby  
            if label == 0:
                for n in neighbors:
                    clear.append(n)
                    if n in open:
                        open.remove(n)

            # if the label of the opened selected square is equal to the number of mines already marked around it
            if effectiveLabel == 0: 
                # mark all other unopened squares around it as clear
                for n in neighbors:
                    clear.append(n)
                    if n in open:
                        open.remove(n)
                
            # if the effective label of the opened selected square is equal to the number of unopened squares immediately around it
            if effectiveLabel == self.AI2.find_num_nearby_unmarked(centerSquare, boardState):
                # mark all unopened squares around the opened selected square as mines
                for n in neighbors:
                    mines.append(n)
                    if n in open:
                        open.remove(n)

            print(f"Clear Squares: {clear}")
            print(f"Mines: {mines}")
            print(f"Unopened Squares: {unopenedSquares}")

            # make a list of remaining squares that could be mines
            squares_left = [square for square in unopenedSquares if square not in clear] # list(set(unopenedSquares) - set(clear))
            squares_left = [square for square in squares_left if square not in mines] # list(set(unopenedSquares) - set(mines))
            print(f"Squares to be considered possibly are {squares_left}")
            
            # update list of uncovered neighboring squares to the opened selected square that could be mines
            neighbors = [square for square in neighbors if square not in mines] # list(set(neighbors) - set(mines))
            print(f"Neighbors of square currently open are {neighbors}")

            if len(squares_left) != 0:
                # if the label of the opened selected square was not 0, add its unopened neighbors to open
                if label != 0 and effectiveLabel != 0: 
                    if len(neighbors) != 0: 
                        for n in neighbors:
                            open.append(n)
                    else: 
                        # if there are no unopened neighbors, make a completely random choice
                        squareToOpen = random.choice(squares_left)
                        print(f"FIRST ELSE: Square to open next is {squareToOpen}")
                        open.append(squareToOpen)
                else: 
                    # make a completely random choice from non-neighbors set of squares 
                    squares_left = [square for square in squares_left if square not in neighbors]
                    squareToOpen = random.choice(squares_left)
                    print(f"SECOND ELSE: Square to open next is {squareToOpen}")
                    open.append(squareToOpen)
            else:
                # there are no squares left to dig
                self.parseAIAlgo(self.AI2.submit_final_answer_format(mines))
                return
                










root = Tk()
root.geometry("800x800")

parser = argparse.ArgumentParser()
parser.add_argument('-f', default = 'test_board.json', type=str, help='the filename (or filepath) of the minesweeper board')
args = parser.parse_args()

app = Window(testcase_filename = args.f, master = root)

root.mainloop()