import numpy as np
from Tree import *
from math import *

SIZE = 3
Bingo = 3

def UCTSearch(state):
    ######################################################################
    # return action 'a' that leads to the best child of the root node v0 #
    # input  : current game state                                        #
    # output : optimal action which has high win probability             #
    # v0 : root node                                                     #
    # vl : the last node reached during the tree policy                  #
    # R : reward for the terminal state reached by running the default   #
    #     policy from state                                              #
    #                                                                    #
    # 1. keep going down until reach leaf node vl (TreePolicy)           #
    # 2. from the leaf node, caculate the reward (DefaultPolicy)         #
    # 3. update win score and visit score while traversing (BackUp)      #
    # repeat 1~3 until we use all computational budget                   #
    ######################################################################
    v0 = Node(state)
    
    computational_budget = 2000
    while computational_budget:
        vl = TreePolicy(v0)
        R = DefaultPolicy(vl.getState())
        BackUp(vl, R)
        computational_budget -= 1

    return optimalAction(v0)



def TreePolicy(node):
    ######################################################################
    # Select or create a leaf node from the nodes already contained      #
    # within the search tree (selection and expansion)                   #
    # 1. when v is not fully expanded, expand unvisited child            #
    # 2. when v is fully expanded, choose the Best child                 #
    ######################################################################
    v = node
    s = v.getState()
    while not is_terminate(s):        
        if len(v.child) != len(s.getPossibleStates()):
            v = Expand(v)
        else:
            v = BestChild(v)
        s = v.getState()
    
    return v


def Expand(node):
    ######################################################################
    # v : current node which is not fully expanded                       #
    # s : current state                                                  #
    # a : choose untried action a from node v                            #
    # next_s : next state when doing action a from state s               #
    # add a new child next_v to v                                        #
    ######################################################################
    v = node
    s = v.getState()
    a = v.getUntriedAction()
    next_s = s.move(a)
    next_v = Node(next_s, v)
    v.add(next_v)
    return next_v
    

def BestChild(v, c = 0.7):
    ######################################################################
    # return the child with the highest reward                           #
    # c can be adjusted to lower or increase the amount of exploration   #
    # performed                                                          #
    # Q / N : win probability                                            #
    ######################################################################
    s = v.getState()
    vN = s.getN()
    
    max_value = -100
    argmax_v = None
    for child in v.child:
        ch_s = child.getState()
        chQ = ch_s.Q
        chN = ch_s.N
        value = chQ / chN + c * sqrt(2 * log(vN) / chN)

        if max_value < value:
            max_value = value
            argmax_v = child
    return argmax_v


def DefaultPolicy(state):
    ######################################################################
    # Play out the domain from a given non-terminal state to produce a   #
    # value estimate (simulation).                                       #
    ######################################################################
    s = state
    while not is_terminate(s): # reach terminate state by random play
        a = s.randomPlay()
        s = s.move(a)

    R = Reward(s)
    return R



def Reward(state):    
    s = state
    player = s.player
    opponent = 3 - player
    
    if checkBingo(s, player):
        return 1
    elif checkBingo(s, opponent):
        return -1
    return 0
    


def BackUp(node, reward):
    ######################################################################
    # The simulation result is "backed up" (i.e. backpropagated) through #
    # the selected nodes to update their statistics.                     #
    ######################################################################
    v = node
    while v is not None:
        s = v.getState()
        s.N += 1
        s.Q += reward
        reward *= -1
        v = v.getParent()



def checkBingo(state, player):
    board = state.getBoard()
    
    for r in range(SIZE):
        for c in range(SIZE - Bingo + 1):
            flag = True
            # horizontal
            for i in range(Bingo):
                if board[r][c+i] != player:
                    flag = False
            if flag:
                return True
    
    for r in range(SIZE - Bingo + 1):
        for c in range(SIZE):
            flag = True
            # vertical
            for i in range(Bingo):
                if board[r+i][c] != player:
                    flag = False
            if flag:
                return True
            
    for r in range(SIZE - Bingo + 1):
        for c in range(SIZE - Bingo + 1):
            flag = True
            # diagonal left top to right bottom
            for i in range(Bingo):
                if board[r+i][c+i] != player:
                    flag = False
            if flag:
                return True
            
            flag = True
            # diagonal left bottom to right top
            for i in range(Bingo):
                if board[r+i][SIZE-c-1-i] != player:
                    flag = False
            if flag:
                return True
    
    return False



def is_terminate(state):
    s = state
    player = s.getPlayer()
    opponent = 3 - player
    
    if checkBingo(s, player):
        return True
    elif checkBingo(s, opponent):
        return True
    
    cnt = 0
    for r in range(SIZE):
        for c in range(SIZE):
            if s.board[r][c] != 0:
                cnt += 1
    if cnt == SIZE*SIZE:
        return True
    
    return False



def optimalAction(node):
    v = node
    v_board = v.getBoard()
    opt_board = BestChild(v, 0).getBoard()
    for r in range(SIZE):
        for c in range(SIZE):
            if v_board[r][c] != opt_board[r][c]:
                return (r,c)
    return (0, 0)



def main():
    
    board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    s = State(board, 1)
    
    while not is_terminate(s):
        player = s.getPlayer()
        a = UCTSearch(s)
        r, c = a
        board[r][c] = player
        s.render()
        print()
        s = State(board, 3 - player)

if __name__=="__main__":
    main()