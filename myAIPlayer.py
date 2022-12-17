import Board


class AIPlayer:
    def __init__(self, side, board: Board.Board):
        self.side = side
        self.otherSide = 3 - side
        self.board = board
        self.INTIFY = 1000
        self.bestMove = (0, 0)

    def makeMove(self):
        if self.board.isFocus:
            return self.makeMoveFocus()
        else:
            return self.makeMoveNotFocus()

    def makeMoveFocus(self):
        x_to = self.board.focusTo
        for i in range(0, 25):
            if self.board.checkValidMove(i, x_to, self.side):
                return (i, x_to)

    def minimax(self, alpha, beta, depth, side):
        if depth == 0:
            return self.evaluate()
    
        canMove = []
        best = -self.INTIFY
        value = 0
        for i in range(0, 25):
            if self.board.board[i] == side:
                for j in range(0, 25):
                    if self.board.checkValidMove(i, j, side):
                        canMove.append((i, j))

        if len(canMove) == 0:
            return self.evaluate()
        
        for move in canMove:
            if best >= alpha:
                alpha = best
            if (self.board.move(move[0], move[1], side)):
                value = -self.minimax(-beta, -alpha, depth - 1, 3 - side)
                self.board.undo()
            if value > best:
                best = value
                if depth == 3:
                    self.bestMove = move
        return best
     


   
    def evaluate(self):
        c = self.board.countSide(self.otherSide)
        return 10 * (2 * c - 16)

    def makeMoveNotFocus(self):
        self.minimax(-self.INTIFY, self.INTIFY, 3,self.side)
        return self.bestMove
