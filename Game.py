import Board
import RandomPlayer
import myAIPlayer


class Game:
    def __init__(self, board, player1, player2):
        self.board = board
        self.turn = 0
        self.winner = None
        self.player1 = player1
        self.player2 = player2

    def printBoard(self):
        self.board.printBoard()

    def checkWinner(self):
        if self.board.board.count(1) == 0:
            self.winner = 2
        if self.board.board.count(2) == 0:
            self.winner = 1
    def move(self, x_from, x_to, side):
        if self.board.move(x_from, x_to, side):
            self.checkWinner()
            return True
        return False

    def play(self):
        while self.winner is None and self.turn < 100:
            self.printBoard()
            x_from, x_to = 0, 0
            if self.turn % 2 == 0:
                print("Player 1's turn")
                x_from, x_to = self.player1.makeMove()
            else:
                print("Player 2's turn")
                x_from, x_to = self.player2.makeMove()
            if self.move(x_from, x_to, self.turn % 2 + 1):
                print("Move from {} to {}".format(x_from, x_to))
            self.turn += 1
            self.printBoard()
            self.checkWinner()
            # pause
            # input()
        

if __name__ == "__main__":
    board = Board.Board()
    player1 = RandomPlayer.RandomPlayer(1, board)
    player2 = myAIPlayer.AIPlayer(2, board)
    game = Game(board, player1, player2)
    game.play()
    if game.winner is None:
        print("Draw")
    else:
        print("Player {} win".format(game.winner))
