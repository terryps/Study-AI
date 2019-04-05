import numpy as np

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
    
    def getState(self):
        """
        get node's state
        """
        return self.state
    
    def getBoard(self):
        return self.state.board
    
    def getParent(self):
        """
        get parent node
        """
        return self.parent
    
    def getChild(self):
        """
        get child nodes
        """
        return self.child

    def getUntriedAction(self):
        s = self.state
        a = s.randomPlay() # get possible random action from state s       
        while 1:
            untried = True
            r, c = a
            for ch in self.child:
                chb = ch.getBoard()
                if chb[r][c] != 0:
                    untried = False
                    break
            
            if untried:
                break
            else:
                a = s.randomPlay()       
        return a 


class State(object):
    def __init__(self, board=None, player=0, N=0, Q=0):
        self.board = board
        self.player = player
        self.N = N # times it has been visited
        self.Q = Q # total reward of all playouts that corresponds to this state                  
    def getBoard(self):
        return self.board
    
    def getPlayer(self):
        return self.player
    
    def getN(self):
        return self.N
    
    def getQ(self):
        return self.Q
    
    def getPossibleStates(self):
        """
        constructs a list of all possible states from current state
        """
        board = self.board
        emptyPos = self.getEmptyPosition()
        possibleStates = []
        opponent = 3 - self.player
        
        for r, c in emptyPos:
            nextBoard = list(map(list, board))
            nextBoard[r][c] = opponent
            possibleStates.append(State(nextBoard, opponent))
        return possibleStates
    
    def randomPlay(self):
        """
        get a list of all possible positions on the board and play a random move
        output : random possible action from current state
        """
        empty = self.getEmptyPosition()
        n = len(empty)
        prob = np.random.uniform(0,1) # choose random uniform prob
        for i in range(n):
            if prob < (1/n)*(i+1):
                move = empty[i]
                break
        return move
    
    def move(self, action):
        """
        s' = a(s)
        input  : one of possible action a from state s (tuple)
        output : next state s' reached by doing a from s (state)
        """
        r, c = action
        opponent = 3 - self.player
        nextBoard = list(map(list, self.board))
        nextBoard[r][c] = opponent
        nextState = State(nextBoard, opponent)
        return nextState
    
    def getEmptyPosition(self):
        """
        output : empty positions (list of tuple)
        """
        size = len(self.board[0])
        empty = []
        for r in range(size):
            for c in range(size):
                if self.board[r][c] == 0:
                    empty.append((r,c))
        return empty
    
    def render(self):
        """
        render state
        """
        size = len(self.board[0])
        for r in range(size):
            lst=[]
            for c in range(size):
                if self.board[r][c]==0:
                    lst.append('[ ]')
                elif self.board[r][c]==1:
                    lst.append('[O]')
                else:
                    lst.append('[X]')
            print(lst)