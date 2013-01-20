import random
from abc import ABCMeta, abstractmethod
import pdb, itertools

class Board:
    """ The board class contains a 2d array initialized to blanks
    and a board size parameter
    """

    def __init__(self, size):
        self.boardSize = size
        self.board = []
        for i in range(size):
            self.board.append([' ' for j in range(size)])

    def get(self, t):
        return self.board[t[0]][t[1]]

    def isEmpty(self, t):
        return self.get(t) == ' '

    def put(self, s, r, c):
        if self.board[r][c] == ' ':
            self.board[r][c] = s
            return True
        else:
            return False 

    def __getitem__(self, i):
        return self.board[i]

    def __str__(self):
        str = '\n'
        for i in self.board:
            str += '|'
            for j in i:
                str += j + '|' 
            str += '\n'
        return str

class Player:
    """ This is the abstract base class for any Player.
    It has an abstract method getMove which needs to be overridden by derived classes
    """
    __metaclass__ = ABCMeta
    def __init__(self, name):
        self.symbol = ' '
        self.name = name
        
    @abstractmethod
    def getMove(self, b):
        pass

class Bot (Player):
    """ Bot class contains the methods all bots can use
    """
    __metaclass__ = ABCMeta
    def getOpponentSymbol(self, b):
        #find the symbol of opponent
        opponentSymbol = ''
        for i in b:
            t = [j for j in i if j != self.symbol and j != ' ']
            if len(t) > 0:
                opponentSymbol = t[0] 
                break
        return opponentSymbol
                
    def isBoardEmpty(self, b):
        """ Checks whether the board is empty or not
        """
        for i in b:
            if i.count(' ') != b.boardSize:
                return False
        return True

    def getCenter(self, b):
        return int(b.boardSize/2),int(b.boardSize/2)

    def getFinishingMove(self, b, symbol):
        """ Checks whether just one more move can finish the game,
        returns that move
        """
        isBreak = False
        for i in range(b.boardSize): #checking all rows
            if (b[i].count(symbol), b[i].count(' ')) == (2, 1): 
                isBreak = True
                break
        if(isBreak): #if found return
            return (i, b[i].index(' '))
        c = []
        for i in range(b.boardSize): #checking all columns
            c = [b[j][i] for j in range(b.boardSize)]
            if (c.count(symbol), c.count(' ')) == (2, 1): 
                isBreak = True
                break
        if(isBreak): #if found return
            return (c.index(' '), i)

        d = [b[i][i] for i in range(b.boardSize)] #checking 1st diagonal
        if (d.count(symbol), d.count(' ')) == (2, 1): 
            return (d.index(' '), d.index(' ')) #if found return

        d = [b[b.boardSize-1-i][i] for i in range(b.boardSize)] #checking 2nd diagonal
        if (d.count(symbol), d.count(' ')) == (2, 1): 
            return (b.boardSize-1-d.index(' '), d.index(' ')) #if found return            

        return (-1, -1) 

    def getRandomMove(self, b):
        coords = range(b.boardSize)
        while True:
            r,c = random.choice(coords),random.choice(coords)
            if b[r][c] == ' ':
                return r,c

class StupidBot (Bot):

    def getMove(self, b):
        return self.getRandomMove(b)

class NiceBot (Bot):

    def getMove(self, b):
        #checking whether there are any nearly finished row/col/diag so as to put a single mark to win
        (r, c) = self.getFinishingMove(b, self.symbol)        
        if (r, c) != (-1, -1):
            return r, c
        
        opponentSymbol = self.getOpponentSymbol(b)
        #checking whether opposition is nearly finished and therefore stopping him/her
        (r, c) = self.getFinishingMove(b, opponentSymbol)
        if (r, c) != (-1, -1):
            return r, c

        if b[1][1] == ' ': #if center is empty, fill that first
            return 1, 1
        else:
            if b[1][1] == self.symbol and self.getEmptyNonCorner(b) != (-1, -1): #if center is ours and non corner is free put there
                return self.getEmptyNonCorner(b)
                    
            if self.getEmptyCorner(b) != (-1, -1): #if corner is empty, put there
                return self.getEmptyCorner(b)
                
        #if nothing else works, just go with a random value
        return self.getRandomMove(b)

    def getEmptyCorner(self, b):
        """ Return the first empty corner of the board
        """
        corners = list(itertools.product([0,2],[0,2]))
        for corner in corners:
            if b[corner[0]][corner[1]] == ' ':
                return corner
        return -1, -1
                
    def getEmptyNonCorner(self, b):
        """ Returns the first empty non corner of the board
        """
        if b[0][1] == ' ' and b[2][1] == ' ':
            return 0, 1
        if b[1][0] == ' ' and b[1][2] == ' ':
            return 1, 0
        return -1, -1

class MyBot (Bot):

    def getMove(self, b):
        #checking whether there are any nearly finished row/col/diag so as to put a single mark to win
        (r, c) = self.getFinishingMove(b, self.symbol)        
        if (r, c) != (-1, -1):
            return r, c
        
        opponentSymbol = self.getOpponentSymbol(b)
        #checking whether opposition is nearly finished and therefore stopping him/her
        (r, c) = self.getFinishingMove(b, opponentSymbol)
        if (r, c) != (-1, -1):
            return r, c

        if b.get(self.getCenter(b)) == ' ': #if center is empty, fill that first
            return self.getCenter(b)
        else:
                    
            if self.getRandomEmptyCorner(b) != (-1, -1): #if corner is empty, put there
                return self.getRandomEmptyCorner(b)
                
        #if nothing else works, just go with a random value
        return self.getRandomMove(b)

    def getRandomEmptyCorner(self, b):
        """ Return a random empty corner of the board
        """
        maxIndex = b.boardSize - 1 
        corners = list(itertools.product([0,maxIndex],[0,maxIndex]))
        emptyCorners = [corner for corner in corners if b.get(corner) == ' ']
        if len(emptyCorners)>0:
            return random.choice(emptyCorners)
        return -1, -1
                
class Human (Player):

    def getMove(self, b):
        r,c = raw_input("Enter move for "+self.name+" : ").split()
        return int(r),int(c)

class Game:
    """ The Game class has composition. Contains a board object and 2 player objects
    """

    def __init__(self, p1, p2):
        self.b = Board(3)
        self.p1 = p1
        self.p2 = p2
        self.p1.symbol = 'X'
        self.p2.symbol = 'O'
        self.currentPlayer = random.choice([p1, p2])
        print self.currentPlayer.name+" starts the game!\n"

    def play(self):
        while True:
            r,c = self.currentPlayer.getMove(self.b)
            if self.b.put(self.currentPlayer.symbol, r, c):
                print self.b
                if self.gameOver(r, c):
                    if(self.gameWon(r, c)):
                        print "!!~~WINNER~~!!\n"+self.currentPlayer.name+"\n"
                    else:
                        print "..Match Drawn.."
                    break
                self.currentPlayer = self.currentPlayer==self.p1 and self.p2 or self.p1
            else:
                print "\nInvalid move, try again!\n"   

    def gameOver(self, r, c):
        return self.gameDrawn() or self.gameWon(r, c)

    def gameDrawn(self):
        draw = True
        for i in range(self.b.boardSize):
            draw = draw and (not ' ' in self.b[i])
        return draw

    def gameWon(self, r, c):
        """ This function determines whether the game is won at any point.
        It iterates through that row, column and if needed the diagonal from the position a mark is given
        """
        size = self.b.boardSize
        cell = self.b[r][c]
        row = [i for i in range(size) if self.b[i][c] == cell]
        if len(row) == size:
            return True
 
        col = [i for i in range(size) if self.b[r][i] == cell]
        if len(col) == size:
            return True

        if self.needDiag(r, c): #checking if diagonal needs to be checked because unless they are corner cells, diagonal need not be checked
            diag1 = [i for i in range(size) if self.b[i][i] == cell]
            diag2 = [i for i in range(size) if self.b[size-1-i][i] == cell]
            if len(diag1) == size or len(diag2) == size:
                return True

        return False

    def needDiag(self, r, c):
        return r==c or (r+c+1)==self.b.boardSize

if __name__ == "__main__":
    p1 = MyBot(raw_input("Enter player 1's name: "))
    p2 = NiceBot(raw_input("Enter player 2's name: "))    
    g = Game(p1, p2)
    g.play()

