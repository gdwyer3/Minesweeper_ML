import numpy as np
import random

class AI1():

    # Define settings upon initialization. Here you can specify
    def __init__(self, numRows, numCols, numBombs, safeSquare):   

        # game variables that can be accessed in any method in the class. For example, to access the number of rows, use "self.numRows" 
        self.numRows = numRows
        self.numCols = numCols
        self.numBombs = numBombs
        self.safeSquare = safeSquare

    def open_square_format(self, squareToOpen):
        return ("open_square", squareToOpen)

    def submit_final_answer_format(self, listOfBombs):
        return ("final_answer", listOfBombs)

    def isValid(x, y): 
        return (x >= 0 and y >= 0 and x <= self.numRows and y <= self.numColumns)

    def isSafeAndUncovered(self, position, uncovered_set): 
        safe = True 
        unexplored = True

        if (position[0] < 0) or (position[0] > self.numCols - 1): #make sure x coordinate w/in bounds
            safe = False

        if (position[1] < 0) or (position[1] > self.numRows - 1): #make sure y coordinate w/in bounds
            safe = False

        if position in uncovered_set:
            unexplored = False

        return safe, unexplored