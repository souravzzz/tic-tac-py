import random
from abc import ABCMeta, abstractmethod
import pdb

class Board:
    """ The board class contains a 2d array initialized to blanks
    and a board size parameter
    """

    def __init__(self, size):
        self.boardSize = size
        self.board = []
        for i in range(size):
            self.board.append([' ' for j in range(size)])

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

class StupidBot (Player):

    def getMove(self, b):
        while True:
            r,c = random.choice([0,1,2]),random.choice([0,1,2])
            if b[r][c] == ' ':
                return r,c

            
class NiceBot (Player):
    def getMove(self, b):
        #checking whether there are any nearly finished row/col/diag so as to put a single mark to win
        (r, c) = self.check_for_finish(b, self.symbol)        
        if (r, c) != (-1, -1):
            return r, c
        
        #find the symbol of opponent
        symbol_opponent = ''
        for i in b:
            t = [j for j in i if j != self.symbol and j != ' ']
            if len(t) > 0:
                symbol_opponent = t[0] 
                break
                
        #checking whether opposition is nearly finished and therefore stopping him/her
        (r, c) = self.check_for_finish(b, symbol_opponent)
        if (r, c) != (-1, -1):
            return r, c

        while True:
            r,c = random.choice(range(b.boardSize)),random.choice(range(b.boardSize))
            if b[r][c] == ' ':
                return r, c                       

    def check_for_finish(self, b, symbol):
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
    p1 = Human(raw_input("Enter player 1's name: "))
    p2 = NiceBot(raw_input("Enter player 2's name: "))    
    g = Game(p1, p2)
    g.play()

