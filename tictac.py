import random

class Board:

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

class Person:

    def __init__(self, name):
        self.symbol = ' '
        self.name = name

    def getMove(self):
        r,c = raw_input("Enter move for "+self.name+" : ").split()
        return r,c

class Game:

    def __init__(self, p1, p2):
        self.b = Board(3)
        self.p1 = p1
        self.p2 = p2
        self.p1.symbol = 'X'
        self.p2.symbol = 'O'
        self.currentPlayer = self.p1

    def play(self):
        while True:
            r, c = self.currentPlayer.getMove()
            r, c = int(r), int(c)
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
        size = self.b.boardSize
        cell = self.b[r][c]
        row = [i for i in range(size) if self.b[i][c] == cell]
        if len(row) == size:
            return True
 
        col = [i for i in range(size) if self.b[r][i] == cell]
        if len(col) == size:
            return True

        if self.needDiag(r, c):
            diag1 = [i for i in range(size) if self.b[i][i] == cell]
            diag2 = [i for i in range(size) if self.b[size-1-i][i] == cell]
            if len(diag1) == size or len(diag2) == size:
                return True

        return False

    def needDiag(self, r, c):
        cells = [(0,2),(2,0)]
        if r==c or (r,c) in cells:
            return True
        else:
            return False

if __name__ == "__main__":
    name1 = raw_input("Enter player 1's name: ")
    name2 = raw_input("Enter player 2's name: ")
    p1 = Person(name1)
    p2 = Person(name2)
    if random.choice([True, False]):
        p1, p2 = p2, p1
    print p1.name+" starts the game!\n"
    g = Game(p1, p2)
    g.play()

