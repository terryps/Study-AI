from math import *
import numpy as np

SIZE = 5
Bingo = 4
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
    """
    player: current state player
    N : visit count for state
    W : win count for state
    """
    def __init__(self, board=None, player=0, N=0, W=0):
        self.board = board
        self.player = player
        self.N = N
        self.W = W
        
    def __get_possible_states__(self):
        """
        get all possible next states from current state 
        """
        next_states = []
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] == 0:
                    next_states.append(self.__move__((r,c)))
        return next_states
    
    def __rollout__(self):
        """
        return random next state
        """
        next_states = self.__get_possible_states__()
        action_idx = np.random.choice(np.arange(len(next_states)))
        
        return next_states[action_idx]
    
    def __move__(self, action):
        """
        get action tuple (row, col), return next state
        """
        r, c = action
        opponent = 3 - self.player
        next_board = list(map(list, self.board))
        next_board[r][c] = self.player
        next_state = State(next_board, opponent)
        return next_state
    
    def __render__(self):
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




def UCTSearch(state):
    root = Node(state)
    computational_budget = 1000
        
    while computational_budget:
        # select until meet leaf node
        leaf = selection(root)
        simulation_num = 40
        
        while simulation_num:
            last = simulation(leaf)
            backup(root, last)            
            simulation_num -= 1
        # below leaf node is not an actual leaf node, it's 'true leaf node's child node'
        # so, when simulation for auxiliary leaf node is done, we should erase its child nodes and initialize its state
        leaf.child = []
        leaf.state.Q = 0
        leaf.state.N = 0
        computational_budget -= 1

    return optimal_action(root)

        
def selection(node):
    state = node.state
    while not is_done(state):
        # if node is upper bound for expand threshold, just choose best child
        if state.N > EXPAND_NUM-1:
            node = best_child(node)
            state = node.state
        # else expand leaf node
        else:
            if len(node.child)==0:
                expand(node)
            node = best_child(node)
            break

    return node

def expand(node):
    state = node.state
    next_states = state.__get_possible_states__()
    for next_state in next_states:
        node.add(Node(next_state, node))

def best_child(node, c_puct=2.4):
    """
    choose max-value child
    """
    state = node.state
    curr_n = state.N
    max_value = -1000
    max_child = None

    for child in node.child:
        ch_w = child.state.W
        ch_n = child.state.N
        ch_q = ch_w / (ch_n + 1)
        ch_u = sqrt(2 * log(curr_n + 1) / (ch_n + 1))
        
        action_value = ch_q + c_puct*ch_u
        if max_value < action_value:
            max_value = action_value
            max_child = child
    return max_child
        
def simulation(node):
    """
    rollout until done and return the terminal node
    """
    state = node.state
    while not is_done(state):
        next_state = state.__rollout__()
        next_node = Node(next_state, parent=node)
        
        state = next_state
        node = next_node
    
    # print("simulation: ")
    # node.state.__render__()
    return node

def backup(root, curr):
    state = curr.state
    root_player = root.state.player
    curr_player = curr.state.player
    # print('root_player: ', root_player, 'curr_player: ', curr_player)
    reward = 1
    is_curr_win = check_bingo(state, curr_player)
    is_curr_lose = check_bingo(state, 3-curr_player)
    is_draw = False

    # print('is_curr_win:', is_curr_win, 'is_draw', is_draw)
    if is_curr_win:
            reward = 0
    if is_curr_win==is_curr_lose:
        is_draw = True
    
    while curr is not None:
        state = curr.state
        state.N += 1
        if is_draw:
            state.W += 0
        else:
            state.W += reward
            reward = 1 - reward
        curr = curr.parent
                
    
def is_done(state):
    """
    terminate when there is bingo or no possible next state
    """
    if check_bingo(state, 1):
        return True
    elif check_bingo(state, 2):
        return True
    
    next_states = state.__get_possible_states__()
    if len(next_states) == 0:
        return True
    
    return False

def check_bingo(state, player):
    """
    return true if current state's board has the input player's bingo
    """
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

def optimal_action(node):
    board = node.state.board
    opt_board = best_child(node, 0).state.board
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] != opt_board[r][c]:
                return (r, c)
    return (-1,-1)

def main():
    board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    state = State(board, 1)
    while not is_done(state):
        opt_action = UCTSearch(state)
        r, c = opt_action
        board[r][c] = state.player
        state.__render__()
        print()
        state = State(board, 3 - state.player)
    
if __name__=="__main__":
    main()
