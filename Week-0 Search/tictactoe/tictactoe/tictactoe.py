"""
Tic Tac Toe Player
"""

import math
import random
import copy

X = "X"
O = "O"
EMPTY = None

#added_helping_functions
def get_horizontal_winner(board):
    winner_val = None
    len_board = len(board)

    for i in range(len_board):
        winner_val = board[i][0]
        for j in range(len_board):
            if board[i][j] != winner_val:
                winner_val = None
        if winner_val:
            return winner_val
    return winner_val

def get_vertical_winner(board):
    winner_val = None
    len_board = len(board)

    for i in range(len_board):
        winner_val = board[0][i]
        for j in range(len_board):
            if board[j][i] != winner_val:
                winner_val = None
        if winner_val:
            return winner_val
    return winner_val

def get_diagonal_winner(board):
    winner_val = None
    len_board = len(board)
    winner_val = board[0][0]
    for i in range(len_board):
            if board[i][i] != winner_val:
                winner_val = None
    if winner_val:
        return winner_val
    
    winner_val = board[0][len_board -1]
    for i in range(len_board):
        j= len_board -1 -i
        if board[i][j] != winner_val:
            winner_val = None
    return winner_val



def min_max_value(board,player,alpha,beta):
    #fto get minimum/maximum value
    if terminal(board):
        return utility(board)
    if player== X:
        v= -math.inf
        for action in actions(board):
            v=max(v,min_max_value(result(board,action),O,alpha,beta))
            alpha=max(v,alpha)
            if alpha >= beta:
                break
        return v
    else:

        v= math.inf
        for action in actions(board):
            v=min(v,min_max_value(result(board,action),X, alpha, beta))
            beta=min(v,beta)
            if alpha >= beta:
                break
        return v

#existing tictactoe functions
def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for row in board:
        for cell in row:
            if cell:
                count += 1
    if count % 2 != 0:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    
    
    for i, row in enumerate(board):
        if EMPTY in row:
            for j, space in enumerate(row):
                if space is EMPTY:
                    result.add((i,j))
    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if terminal(board):
        raise ValueError("GAME OVER")
    else:
        result_board = copy.deepcopy(board)
        current_player = player(result_board)
        (i, j) = action
        result_board[i][j]=current_player
    
    return result_board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner_val = get_horizontal_winner(board) or get_vertical_winner(board) or get_diagonal_winner(board)
    return winner_val


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    for row in board:
        for cell  in row:
            if cell == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    return 0




def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if board == initial_state():
       return(random.randint(0,2), random.randint(0,2))
    current_player = player(board)
    alpha = -math.inf
    beta  = math.inf
    action_to_return = None
    if current_player == X:
        val = -(math.inf)
        
        for action in actions(board):
            result_minvalue= min_max_value(result(board,action),O,alpha,beta)
            alpha= max(result_minvalue,val)
            if val < result_minvalue:
                val = result_minvalue
                action_to_return = action
    elif current_player == O:
        val = math.inf
        action_to_return = None
        for action in actions(board):
            result_maxvalue= min_max_value(result(board,action),X,alpha,beta)
            beta= min(val,result_maxvalue)
            if val > result_maxvalue:
                val = result_maxvalue
                action_to_return = action
    
    return action_to_return

