import Board


class AIPlayer:
    def __init__(self, side, board: Board.Board):
        self.side = side
        self.otherSide = 3 - side
        self.board = board
        self.INTIFY = 1000
        self.bestMove = (0, 0)

    def makeMove(self):
        canMove = self.findAvailableMoves(self.side)
        if len(canMove) == 0:
            return False
        bestMove = canMove[0]
        bestEval = -999999
        for move in canMove:
            self.board.move(move[0], move[1], self.side)
            eval = self.minimax(2, False, -999999, 999999)
            self.board.undoMove()
            if eval > bestEval:
                bestEval = eval
                bestMove = move
        return bestMove


    def minimax(self, depth, isMaximizing, alpha, beta):
        if depth == 0:
            return self.evaluate()
        if isMaximizing:
            maxEval = -999999
            for move in self.findAvailableMoves(self.side):
                self.board.move(move[0], move[1], self.side)
                eval = self.minimax(depth - 1, False, alpha, beta)
                self.board.undoMove()
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = 999999
            for move in self.findAvailableMoves(self.otherSide):
                self.board.move(move[0], move[1], self.otherSide)
                eval = self.minimax(depth - 1, True, alpha, beta)
                self.board.undoMove()
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def findAvailableMoves(self, side):
        canMove = []
        for i in range(25):
            for j in range(25):
                if self.board.checkValidMove(i, j, side):
                    canMove.append((i, j))
        return canMove

    def evaluate(self):
        return self.board.countPiece(self.side) - self.board.countPiece(self.otherSide)
