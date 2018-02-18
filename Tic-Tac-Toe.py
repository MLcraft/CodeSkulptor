"""
Tic-Tac-Toe AI Player 
Made by MLcraft
"""

import codeskulptor
import random
import poc_ttt_gui
import poc_ttt_provided as provided
# Test suite for individual functions
#import user35_ofAHGrBJ3a_2 as wopr

codeskulptor.set_timeout(200)
# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 50    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player

DICT = {1:{None:0, 2:0, 3:0, 4:0}, 2:{None:0, 2:MCMATCH, 3:-MCOTHER, 4:0}, 3:{None:0, 2:-MCMATCH, 3:MCOTHER, 4:0}, 4:{None:0, 2:0, 3:0, 4:0}}

# Add your functions here.
def max_scores(scores):
    """
    Return list of index and value of 
    maximum scores.
    """
    maxscores = []
    for idx in range(len(scores)):
        item = scores[idx]
        if (len(maxscores) == 0):
            maxscores.append((idx, item))
        elif item == maxscores[0][1]:
            maxscores.append((idx, item))
        elif item > maxscores[0][1]:
            maxscores = [(idx, item)]
    return maxscores
def mc_trial(board, player = provided.PLAYERX):
    """
    Plays a game starting with the given player using random moves.
    The board will be modified to contain the game state.
    """

    #newboard = board.clone()
    pla = player
    while len(board.get_empty_squares()) > 0:
        #print board.check_win()
        #print board.get_empty_squares()
        #print str(board)
        if board.check_win() == None:
            if len(board.get_empty_squares()) > 0:
                square = random.choice(board.get_empty_squares())
                board.move(square[0], square[1], pla)
                pla = provided.switch_player(pla)
        else:
            break
def mc_update_scores(scores, board, player):
    """
    Scores the given boards and updates the scores grid.
    """
    winner = board.check_win()
    for dui in range(len(scores)):
        for duj in range(len(scores[dui])):
            pla = board.square(dui, duj)
            #print pla
            scores[dui][duj] += DICT[pla][winner]
    #print scores
    #print str(board)
def get_best_move(board, scores):
    """
    Gets the best valid move.
    """
    maxsquares = []
    scorelist = []
    empty_scores = []
    empty = board.get_empty_squares()
    for dui in scores:
        for duj in dui:
            scorelist.append(duj)
    for dui in empty:
        empty_scores.append(scores[dui[0]][dui[1]])
    #print "Scores for empty squares:", empty_scores
    for dui in max_scores(empty_scores):
        maxsquares.append(empty[dui[0]])
       
#    for dui in maxsquares:
#        if dui in board.get_empty_squares():
#            valid_squares.append(dui)
        
    #print "empty_squares ", board.get_empty_squares()             
    #print "score " ,scores        
    #print "maxsquares", maxsquares
#    print "valid_squares", valid_squares
    if len(maxsquares) > 0:
        square = random.choice(maxsquares)
        #print "Square: " + str(square)
        return square
def mc_move(board, player, trials):
    """
    Makes a move.
    """
    grid_size = board.get_dim()
    scores = [[0 for dummy_i in range(grid_size)] for dummy_j in range(grid_size)]
    pla = player
    for dui in scores:
        for dummy_j in dui:
            if board.check_win() == None:
                for dummy_i in range(trials):
                    new_board = board.clone()
                    mc_trial(new_board, player)
                    mc_update_scores(scores, new_board, player)
                    #print "Scores: " + str(scores)
                    #print str(board)
                move = get_best_move(board, scores)
                pla = provided.switch_player(pla)
                return move

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

#print "mc_trial"
#wopr.test_mc_trial(mc_trial)
#print "mc_update_scores"
#wopr.test_mc_update_scores(mc_update_scores)
#print "get_best_move"
#wopr.test_get_best_move(get_best_move)
#print "mc_move"
#wopr.test_mc_move(mc_move)
#print mc_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]), provided.PLAYERX, NTRIALS) 
