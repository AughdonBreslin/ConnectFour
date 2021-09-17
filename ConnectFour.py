# Aughdon Breslin #
# Connect Four AI #
# May 2019 #


##############
# Make Board #
##############
import numpy as np
import random

mainboard = np.array
mainboard = [[0] * 7 for x in range(6)]

def printBoard(board):
    for i in board:
        print(i)


##################
# Game Mechanics #
##################

# checks if top spot in each column is open
def eligibleColumns(board):
    ele = []
    for c in range(0, 7):
        if board[0][c] == 0:
            ele.append(c)
    return ele


# figures out what row to drop based on column
def openRow(column, board):
    for r in range(0, len(board)):
        if board[len(board) - 1 - r][column] == 0:
            return (len(board) - 1 - r)
    return 0


# put a specified piece in a specified spot
def dropPiece(color, column, row, board):
    board[row][column] = color  # fix column


# gets move and checks if valid, then makes move
def playerTurn(color, board):
    print("Pick a column, Player ", color)
    move = int(input())
    while not move - 1 in eligibleColumns(mainboard):
        print("Invalid input. Pick a valid column, Player ", color)
        move = int(input())
    dropPiece(color, move - 1, openRow(move - 1, mainboard), mainboard)
    # switch between the players, printing updated board

# Start up the whole game
def playGame():
    # Create the board
    printBoard(mainboard)
    # While the game's not over
    while (won(2, mainboard) == False):
        # Start with player 1
        playerTurn(1, mainboard)
        printBoard(mainboard)
        
        # Stats
        print("threes: " + str(findThrees(1, mainboard)))
        print("twos: " + str(findTwos(1, mainboard)))
        print("mids: " + str(numMiddles(1, mainboard)))
        print ("score: " + str(scoreBoard(1, 2, mainboard)))

        # If the games not over, go to AI's turn
        if (won(1, mainboard) == False):
            AiTurn(2, mainboard)
            printBoard(mainboard)
        else:
            break


##################
# Win Conditions #
##################

def checkHorizontal(color, board):
    for r in range(0, 6):
        for c in range(0, 4):
            if (board[r][c] == color and board[r][c + 1] == board[r][c] and board[r][c + 2] == board[r][c] and board[r][
                c + 3] == board[r][c]):
                return True
    return False


def checkVertical(color, board):
    for r in range(0, 3):
        for c in range(0, 7):
            if (board[r][c] == color and board[r + 1][c] == board[r][c] and board[r + 2][c] == board[r][c] and
                    board[r + 3][c] == board[r][c]):
                return True
    return False


def checkPosDiag(color, board):
    for r in range(3, 6):
        for c in range(0, 4):
            if (board[r][c] == color and board[r - 1][c + 1] == board[r][c] and board[r - 2][c + 2] == board[r][c] and
                    board[r - 3][c + 3] == board[r][c]):
                return True
    return False


def checkNegDiag(color, board):
    for r in range(0, 3):
        for c in range(0, 4):
            if (board[r][c] == color and board[r + 1][c + 1] == board[r][c] and board[r + 2][c + 2] == board[r][c] and
                    board[r + 3][c + 3] == board[r][c]):
                return True
    return False


def won(color, board):
    # or board is full
    if (checkHorizontal(color, board) or checkVertical(color, board) or checkPosDiag(color, board) or checkNegDiag(
            color, board)):
        return True
    return False


#############
# AI's Turn #
#############

def AiTurn(color, boardy):
    column, score = miniMax(boardy, 5, True, -999999999, 9999999999)  ##ITS WINNING AT 5 FeelsBad/GoodMan##
    dropPiece(color, column, openRow(column, boardy), boardy)


################
# Check Threes #
################

# bonus points for double edged threes/twos
def findHorThrees(color, board):
    threes = 0
    for r in range(0, 6):  # Check horizontally
        for c in range(0, 4):
            em = 0
            chips = 0
            for x in range(c, c + 4):
                if board[r][x] == 0:
                    em = em + 1
                elif board[r][x] == color:
                    chips = chips + 1
            if chips == 3 and em == 1:
                threes = threes + 1
    return threes


def findVertThrees(color, board):
    threes = 0
    for r in range(0, 3):
        for c in range(0, 7):
            em = 0
            chips = 0
            for x in range(r, r + 4):
                if board[x][c] == 0:
                    em = em + 1
                elif board[x][c] == color:
                    chips = chips + 1
            if chips == 3 and em == 1:
                threes = threes + 1
    return threes


def findDiagThrees(color, board):
    threes = 0
    # Positive diagonal
    for r in range(3, 6):
        for c in range(0, 4):
            em = 0
            chips = 0
            for x in range(0, 4):
                if board[r - x][c + x] == 0:
                    em = em + 1
                elif board[r - x][c + x] == color:
                    chips = chips + 1
            if chips == 3 and em == 1:
                threes = threes + 1

    # Negative diagonal
    for r in range(0, 3):
        for c in range(0, 4):
            em = 0
            chips = 0
            for x in range(0, 4):
                if board[r + x][c + x] == 0:
                    em = em + 1
                elif board[r + x][c + x] == color:
                    chips = chips + 1
            if chips == 3 and em == 1:
                threes = threes + 1
    return threes

# Accumulate
def findThrees(color, board):
    blank = []
    for tup in str(findHorThrees(color, board)):
        if not tup in blank:
            blank.append(tup)
    for tup in str(findVertThrees(color, board)):
        if not tup in blank:
            blank.append(tup)
    for tup in str(findDiagThrees(color, board)):
        if not tup in blank:
            blank.append(tup)
    
    return findDiagThrees(color, board) * 16 + findVertThrees(color, board) * 10 + findHorThrees(color, board) * 14


########
# Twos #
########
def findHorTwos(color, board):
    twos = 0
    for r in range(0, 6):  # Check horizontally
        for c in range(0, 4):
            em = 0
            chips = 0
            for x in range(c, c + 4):
                if board[r][x] == 0:
                    em = em + 1
                elif board[r][x] == color:
                    chips = chips + 1
            if chips == 2 and em == 2:
                twos = twos + 1

    return twos


def findVertTwos(color, board):
    twos = 0
    for r in range(0, 3):
        for c in range(0, 7):
            em = 0
            chips = 0
            for x in range(r, r + 4):
                if board[x][c] == 0:
                    em = em + 1
                elif board[x][c] == color:
                    chips = chips + 1
            if chips == 2 and em == 2:
                twos = twos + 1

    return twos


def findDiagTwos(color, board):
    twos = 0
    for r in range(3, 6):
        for c in range(0, 4):
            em = 0
            chips = 0
            for x in range(0, 4):
                if board[r - x][c + x] == 0:
                    em = em + 1
                elif board[r - x][c + x] == color:
                    chips = chips + 1
            if chips == 2 and em == 2:
                twos = twos + 1

    for r in range(0, 3):
        for c in range(0, 4):
            em = 0
            chips = 0
            for x in range(0, 4):
                if board[r + x][c + x] == 0:
                    em = em + 1
                elif board[r + x][c + x] == color:
                    chips = chips + 1
            if chips == 2 and em == 2:
                twos = twos + 1
    return twos


def findTwos(color, board):
    return findDiagTwos(color, board) * 4 + findVertTwos(color, board) * 1 + findHorTwos(color, board) * 3


###################
# Prioritizations #
###################
def numMiddles(color, board):
    c = 3
    mids = 0
    for r in range(0, 6):
        if board[r][c] == color:
            mids = mids + 1
    return mids


#######################
# Adding up the Score #
#######################
def scoreBoard(color, oppColor, board):
    s = 0
    # Check AI Score
    s = s + numMiddles(color, board)
    s = s + findTwos(color, board)  # Checks two in a rows
    s = s + findThrees(color, board)  # Check three in a rows
    # Check Human Score
    s = s - numMiddles(oppColor, board)
    s = s - findTwos(oppColor, board)  # Checks two in a rows
    s = s - findThrees(oppColor, board)  # Check three in a rows

    # Check four in a rows
    if won(color, board):
        s = s + 1000

    # Check four in a rows
    if won(oppColor, board):
        s = s - 1000
    # Check Center Pieces
    return s


##############
# MiniMaxing #
##############

def miniMax(board, depth, maximizingPlayer, alpha, beta):
    # Reached recursion depth or game is over
    if depth == 0 or won(1, board) or won(2, board) or eligibleColumns(board) == []:
        # if we're done because the game is over
        if won(1, board) or won(2, board) or eligibleColumns(board) == []:
            if won(1, board):
                return None, -999999999
            elif won(2, board):
                return None, 999999999
            elif eligibleColumns(board) == []:
                return None, 0
        else:  # if done with recursion but the game is not over
            return None, scoreBoard(2, 1, board)
    # if the game is not over and we are not done with recursion,
    # find the best possible move
    elif maximizingPlayer:  
        value = -999999999  # start with horrible position rating
        # Start with a random column of the board
        position = random.randint(0, len(eligibleColumns(board)))
        for columns in eligibleColumns(board):
            # Make a copy of the boardstate
            copy = [[0] * 7 for x in range(6)]
            for row in range(0, len(board)):
                for col in range(0, len(board[row])):
                    copy[row][col] = board[row][col]
            # Play on the copy
            row = openRow(columns, copy)
            dropPiece(2, columns, row, copy)
            # Find the score of the position 
            newScore = miniMax(copy, depth - 1, False, alpha, beta)[1]
            # If the score is good, update
            if newScore > value:
                value = newScore
                position = columns
            # Update alpha
            if value > alpha:
                alpha = value
            if alpha >= beta:
                break
        return position, value
    else:
        value = 999999999  # start with horrible rating (from opponent's perspective)
        # Do the same but minimizing the player score (simulating the opponent's goal)
        position = random.randint(0, len(eligibleColumns(board)))
        for columns in eligibleColumns(board):
            copy = [[0] * 7 for x in range(6)]
            for row in range(0, len(board)):
                for col in range(0, len(board[row])):
                    copy[row][col] = board[row][col]
            row = openRow(columns, copy)
            dropPiece(1, columns, row, copy)
            newScore = miniMax(copy, depth - 1, True, alpha, beta)[1]
            if newScore < value:
                value = newScore
                position = columns
            if value < beta:
                beta = value
            if alpha >= beta:
                break
        return position, value

# Run the game!
playGame()



