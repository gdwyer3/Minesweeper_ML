import numpy as np
import random

class AI2():

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

    # returns the list of unopened neighbors to the given centerSquare
    def find_unopened_neighbors(self, centerSquare, boardState):
        neighbors = []
        for i in range(centerSquare[0] - 1, centerSquare[0] + 2): 
            for j in range(centerSquare[1] - 1, centerSquare[1] + 2):
                # Ignore the center square itself
                if (i, j) == centerSquare:
                    continue
                if 0 <= i < self.numRows and 0 <= j < self.numCols: 
                    if boardState[i][j] == -1:
                        neighbors.append((i, j))
        return neighbors

    # returns the number of squares that have been flagged as mines from the set of squares 
    # immediately surrounding the given centerSquare
    def find_num_nearby_mines(self, centerSquare, boardState):
        count = 0
        for i in range(centerSquare[0] - 1, centerSquare[0] + 2): 
            for j in range(centerSquare[1] - 1, centerSquare[1] + 2):
                # Ignore the center square itself
                if (i, j) == centerSquare:
                    continue
                if 0 <= i < self.numRows and 0 <= j < self.numCols:
                    if boardState[i][j] == 9: 
                        count += 1
        return count

    # returns the number of squares that are unopened from the set of squares 
    # immediately surrounding the given centerSquare
    def find_num_nearby_unmarked(self, centerSquare, boardState):
        count = 0
        for i in range(centerSquare[0] - 1, centerSquare[0] + 2): 
            for j in range(centerSquare[1] - 1, centerSquare[1] + 2):
                # Ignore the center square itself
                if (i, j) == centerSquare:
                    continue
                if 0 <= i < self.numRows and 0 <= j < self.numCols:
                    if boardState[i][j] == -1: 
                        count += 1
        return count

    # marks the squares that are unmarked around the given CenterSquare as mines
    def mark_as_mine(self, centerSquare, unopenedSquares, boardState):
        for i in range(centerSquare[0] - 1, centerSquare[0] + 2): 
            for j in range(centerSquare[1] - 1, centerSquare[1] + 2):
                # Ignore the center square itself
                if (i, j) == centerSquare:
                    continue
                if 0 <= i < self.numRows and 0 <= j < self.numCols: 
                    if boardState[i][j] == -1:
                       boardState[i][j] = 9 
                       unopenedSquares.remove((i, j))
        return unopenedSquares

    # return the square (r, c) you want to open based on the given boardState
    # the boardState will contain the value (0-8 inclusive) of the square, or -1 if that square is unopened
    # an AI example that returns a random square (r, c) that you want to open
    # TODO: implement a better algorithm
    def performAI(self, boardState):
        print(boardState)

        mines = []
        open = [self.safeSquare]
        clear = []

        # while there is a square to explore 
        while open:
            # find all the unopened squares
            unopenedSquares = []
            for row in range(self.numRows):
                for col in range(self.numCols):
                    if boardState[row][col] == -1:
                        unopenedSquares.append((row, col))
            
            # if the number of unopened squares is equal to the number of bombs, all squares must be bombs, and we can submit our answer
            if len(unopenedSquares) == self.numBombs:
                print(f"List of bombs is {unopenedSquares}")
                return self.submit_final_answer_format(unopenedSquares)
            else:
                centerSquare = open.pop() 
                print(f"Square currently open is {centerSquare}")

                if centerSquare != self.safeSquare:
                    self.open_button(centerSquare[0], centerSquare[1])

                # find the value of the uncovered square
                labelCenter = self.boardState[centerSquare[0]][centerSquare[1]]
                print(f"Label of square currently open is {labelCenter}")

                # find the effective label of the uncovered square = value of the uncovered square minus the numer of neighboring mines already accounted for
                effectiveLabelCenter = labelCenter - self.find_num_nearby_mines(centerSquare)
                print(f"Effective label of square currently open is {effectiveLabelCenter}")

                # find all unopened squares that are neighbors of the given centerSquare
                neighbors = self.find_unopened_neighbors(centerSquare)
                print(f"Neighbors of square currently open are {neighbors}")

                if labelCenter == 9:
                    mines.append(centerSquare)
                    
                if labelCenter == 0:
                    clear.append(centerSquare)
                    for n in neighbors:
                        clear.append(n)

                # if the label of the opened centerSquare is equal to the number of mines already marked around it
                if effectiveLabelCenter == 0: 
                    # mark all other unopened squares around it as clear
                    for n in neighbors:
                        clear.append(n)
                
                # if the value in the opened centerSquare is equal to the number of unopened squares immediately around it
                if effectiveLabelCenter == self.find_num_nearby_unmarked(centerSquare):
                    # mark all other unopened squares around it as mines
                    for n in neighbors:
                        mines.append(n)

                # update choice list of remaining squares that could be mines
                squares_left = np.setdiff1d(unopenedSquares, clear)
                squares_left = np.setdiff1d(squares_left, mines)
                # update list of neighbors that could be mines
                neighbors = np.setdiff1d(neighbors, mines)

                # pick a square from the list of remaining squares that could be mines and open it  
                if squares_left:
                    # if the centerSquare was not 0, pick an unopened neighbor
                    if labelCenter > 0: 
                        if neighbors: 
                            neighborsToOpen = neighbors
                            for n in neighborsToOpen:
                                open.append(n)
                    else: 
                        squareToOpen = random.choice(squares_left)
                        print(f"Square to open next is {squareToOpen}")
                        # open.append(squareToOpen)
                else:
                    return self.submit_final_answer_format(mines)    
                
        return self.open_square_format(squareToOpen)