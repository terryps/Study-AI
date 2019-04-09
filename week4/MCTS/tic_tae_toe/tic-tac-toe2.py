from math import *
import numpy as np

SIZE = 4
Bingo = 3
EXPAND_NUM = 30

class Node(object):
    def __init__(self, state=None, parent=None):
        self.state = state
        self.parent = parent
        self.child = []
        
    def add(self, node):
        """
        add child node
        """
        self.child.append(node)
        

class State(object):
    def __init__(self, board=None, player=0, N=0, W=0):
        self.board = board
        self.player = player
        self.N = N
        self.W = W
        
    def getPossibleStates(self):
        opponent = 3 - self.player
        lst = []
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] == 0:
                    nextBoard = list(map(list, self.board))
                    nextBoard[r][c] = opponent
                    lst.append(State(nextBoard, opponent))
        return lst
    
    def randomPlay(self):
        """
        return next random state
        """
        opponent = 3 - self.player
        empty = [(r,c) if self.board[r][c]==0 else None for r in range(SIZE) for c in range(SIZE)]
        empty = [x for x in empty if x is not None]
        action_idx = np.random.choice(np.arange(len(empty)))
        
        action = empty[action_idx]
        
        return self.move(action)
    
    def move(self, action):
        r, c = action
        opponent = 3 - self.player
        nextBoard = list(map(list, self.board))
        nextBoard[r][c] = opponent
        nextState = State(nextBoard, opponent)
        return nextState
    
    def render(self):
        for r in range(SIZE):
            lst = []
            for c in range(SIZE):
                if self.board[r][c] == 0:
                    lst.append('[ ]')
                elif self.board[r][c] == 1:
                    lst.append('[O]')
                else:
                    lst.append('[X]')
            print(lst)
############################################################
    
def UCTSearch(state):
    v_root = Node(state)
    computational_budget = 1000
    
    while computational_budget:
        simluation_num = 1
        v_leaf = Selection(v_root)
        while simluation_num:
            v_last = Simulation(v_leaf)
            R = Reward(v_root.state, v_last.state)
            BackUp(v_root, v_last, R)
            simluation_num -= 1
        v_leaf.child = []
        computational_budget -= 1
      
    for ch in v_root.child:
        for r in range(SIZE):
            for c in range(SIZE):
                if ch.state.board[r][c] != v_root.state.board[r][c]:
                    print(r, c, 'W:', ch.state.W, 'N:', ch.state.N)
    
    return optimalAction(v_root)

def Selection(node):
    v = node
    s = v.state
    while not is_terminate(s):
        if s.N > EXPAND_NUM-1:
            v = BestChild(v)
            s = v.state
        else:
            if v.child == []:
                Expand(v)
            v = BestChild(v)
            break
                
    return v

def Expand(node):
    v = node
    s = v.state
    for next_s in s.getPossibleStates():
        v.add(Node(next_s, v))

def Simulation(node):
    """
    Select leaf node
    """
    v = node
    s = v.state
    while not is_terminate(s):
        next_s = s.randomPlay()
        next_v = Node(next_s, v)
        v = next_v
        s = next_s
        
    return v

def BackUp(root_node, last_node, reward):
    v = last_node
    cur_player = root_node.state.player

    while v is not None:
        s = v.state
        s.N += 1
        # Compute reward
        if cur_player == s.player:
            s.W += reward
        else:
            s.W += (1 - reward)
        v = v.parent
        
def BestChild(node, c_puct=2.4):
    v = node
    s = v.state
    v_n = s.N
    max_value = -100
    argmax_v = None

    for c in v.child:
        ch_w = c.state.W
        ch_n = c.state.N
        
        ch_q = ch_w / (ch_n + 1)
        ch_u = sqrt(2 * log(v_n + 1) / (1 + ch_n))
        
        value = ch_q + c_puct * ch_u
        #print('value:%f root_visit:%d'%(value,v_n))

        
        if max_value < value:
            max_value = value
            argmax_v = c
            max_N = ch_n
        
    
    return argmax_v

def Reward(root_state, leaf_state):    
    player = root_state.player
    opponent = 3 - player
    
    is_player_win = checkBingo(leaf_state, player)
    is_opponent_win = checkBingo(leaf_state, opponent)
    
    if is_player_win == True:
        if player == leaf_state.player:
            reward = 1
        else:
            reward = 0
            
    elif checkBingo(leaf_state, opponent) == True:
        if player == leaf_state.player:
            reward = 1
        else:
            reward = 0
            
    else:
        reward = 0
        
    #print('root_player',player,end=' ')
    #print('leaf_player',leaf_state.player, end=' ')
    #print(is_player_win, is_opponent_win, reward)
        
    return reward


def is_terminate(state):
    s = state
    player = s.player
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

def checkBingo(state, player):
    board = state.board
    
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

def optimalAction(node):
    v = node
    board = v.state.board
    opt_board = BestChild(v, 0).state.board
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] != opt_board[r][c]:
                return (r, c)
    return (-1,-1)

def main():
    board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    s = State(board, 1)
    while not is_terminate(s):
        player = s.player
        a = UCTSearch(s)
        r, c = a
        board[r][c] = player
        s.render()
        print()
        s = State(board, 3 - player)
        
if __name__=="__main__":
    main()
    

    
    """
     
    ### Test Case 1
    board = [[1,1,1,2], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    print(checkBingo(State(board, 1), 1))
    
    ### Test Case 2
    board = [[2,1,1,2], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    print(checkBingo(State(board, 1), 1))
    
    ### Test Case 3
    board = [[1,1,1,2], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    print(checkBingo(State(board, 1), 1))
    
    ### Test Case 4
    board = [[1,1,1,2], [0,1,0,0], [0,0,1,0], [0,0,0,0]]
    print(checkBingo(State(board, 1), 1))
    
    ### Test Case 5
    board = [[1,0,1,2], [0,1,0,0], [0,0,1,0], [0,0,0,1]]
    print(checkBingo(State(board, 1), 1))
    
    ### Test Case 6
    board = [[1,2,2,2], [1,0,0,0], [0,0,0,0], [0,0,0,0]]
    print(checkBingo(State(board, 1), 1))
    """
