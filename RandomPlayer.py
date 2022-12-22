import Board
import random

class RandomPlayer:
    def __init__(self, side, board: Board.Board):
        self.side = side
        self.otherSide = 3 - side
        self.board = board
        self.INTIFY = 1000
        self.bestMove = (0, 0)

    def makeMove(self):
        canMove = self.findAvailableMoves()
        if len(canMove) == 0:
            return False
        return random.choice(canMove)

    def findAvailableMoves(self):
        canMove = []
        for i in range(25):
            for j in range(25):
                if self.board.checkValidMove(i, j, self.side):
                    canMove.append((i, j))
        return canMove
        
        

      