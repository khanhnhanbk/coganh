import copy

# maskGO
'''Tat ca cac truong hop co the xay ra trong game. 
Danh dau tu huong 12h di theo thuan chieu kim dong ho

00 01 02 03 04
05 06 07 08 09
10 11 12 13 14
15 16 17 18 19
20 21 22 23 24

100 là không đi được.
+1 tức là từ ô đó đi được +1 (1 -> 2)
-1 tức là đi tới ô đó -1 (2 -> 1)
'''
maskGo = [
    [100, 100, 1, 6, 5, 100, 100, 100],     # 0
    [100, 100, 1, 6, 5, 4, -1, 100],   # 2 giong nhau
    [100, 100, 100, 100, 5, 4, -1, 100],    # 4
    [-5, -4, 1, 6, 5, 100, 100, 100],  # 10
    [-5, -4, 1, 6, 5, 4, -1, -6],  # 6,8,12,16,18 giong nhau
    [-5, 0, 0, 0, 5, 4, -1, -6],  # 14
    [-5, -4, 1, 100, 100, 100, 100, 100],  # 20
    [-5, -4, 1, 100, 100, 100, -1, -6],  # 22
    [-5, 0, 0, 100, 100, 100, -1, -6],  # 24
    [100, 100, 1, 100, 5, 100, -1, 100],        # 1 3 giong nhau
    [-5, 100, 1, 100, 5, 100, 100, 100],  # 5 15 giong nhau
    [-5, 100, 1, 100, 5, 100, -1, 100],  # 7,11,13,17 giong nhau
    [-5, 100, 100, 100, 5, 100, -1, 100],  # 9,19 giong nhau
    [-5, 100, 1, 100, 100, 100, -1, 100]  # 21,23 giong nhau

]

reference = [0, 9, 1, 9, 2,
             10, 4, 11, 4, 12,
             3, 11, 4, 11, 5,
             10, 4, 11, 4, 12,
             6, 13, 7, 13, 8]

class State:
    def __init__(self, board, focusTo, isFocus) -> None:
        self.board = copy.deepcopy(board)
        self.focusTo = focusTo
        self.isFocus = isFocus

class Board:
    def __init__(self):
        self.board = [1, 1, 1, 1, 1,
                      1, 0, 0, 0, 1,
                      1, 0, 0, 0, 2,
                      2, 0, 0, 0, 2,
                      2, 2, 2, 2, 2]
        self.isFocus = False
        self.focusTo = -1
        self.visited = [False] * 25
        self.isDead = [False] * 25
        self.arrayLoad = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
        self.saveMove = []

    def printBoard(self):
        for i in range(0, 25):
            if i % 5 == 0:
                print()
            print(self.board[i], end=" ")
        print()

    def checkValidMove(self, x_from, x_to, side):
        if self.isFocus:
            if x_to != self.focusTo:
                return False
        if self.board[x_from] != side:
            return False
        if self.board[x_to] != 0:
            return False
        if (x_to - x_from) in maskGo[reference[x_from]]:
            return True
        return False

    def move(self, x_from, x_to, side):
        if not self.checkValidMove(x_from, x_to, side):
            return False
        otherSide = 3 - side
        self.board[x_to] = side
        self.board[x_from] = 0

        # kiem tra ganh
        self.checkLoad(x_to, side)
        for i in range(0, 4):
            if self.arrayLoad[i][0] != -1:
                self.board[self.arrayLoad[i][0]] = side
                self.board[self.arrayLoad[i][1]] = side

        # check die piece
        diePiece = self.checkDiePiece(otherSide)
        for i in diePiece:
            self.board[i] = side
        self.focusTo = -1
        self.isFocus = False
        self.checkIsFocus(x_from, side)

        self.saveMove.append(State(self.board, self.focusTo, self.isFocus))
        return True

    def checkWin(self, side):
        otherSide = 3 - side
        otherSizePiece = self.countPiece(otherSide)
        if otherSizePiece == 0:
            return True
        if otherSizePiece > 2:
            return False
        for i in range(0, 25):
            if self.board[i] == otherSide:
                for j in range(0, 8):
                    if maskGo[reference[i]][j] != 100:
                        if self.board[i + maskGo[reference[i]][j]] == 0:
                            return False
        return True

    def countPiece(self, side):
        count = 0
        for i in range(0, 25):
            if self.board[i] == side:
                count += 1
        return count

    def spreadNoDeadPiece(self, x, side):
        ''' Khi mot quan song khi cac quan xung quanh cua no song'''
        self.isDead[x] = False
        if self.visited[x]:
            return
        self.visited[x] = True
        for i in range(0, 8):
            if maskGo[reference[x]][i] != 100:
                if self.board[x + maskGo[reference[x]][i]] == side:
                    self.isDead[x] = False
                    self.spreadNoDeadPiece(x + maskGo[reference[x]][i], side)

    def checkDiePiece(self, side):
        '''kiem tra cac quan co bi chet'''
        self.visited = [False] * 25
        self.isDead = [True] * 25
        for i in range(0, 25):
            if self.board[i] == 0:
                self.isDead[i] = False
                self.spreadNoDeadPiece(i, side)
        diePiece = []
        for i in range(0, 25):
            if self.board[i] == side and self.isDead[i]:
                diePiece.append(i)
        return diePiece

    def checkLoad(self, x, side):
        '''kiem tra co ganh duoc hay khong'''
        # result use for is focus
        result = False
        otherSide = 3 - side
        self.arrayLoad = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
        for i in range(0, 4):
            if (maskGo[reference[x]][i] != 100) and (maskGo[reference[x]][i+4]!= 100):
                if (self.board[x + maskGo[reference[x]][i]] == otherSide) and (self.board[x + maskGo[reference[x]][i+4]] == otherSide):
                    y1 = x + maskGo[reference[x]][i]
                    y2 = x + maskGo[reference[x]][i+4]
                    if self.board[y1] == otherSide and self.board[y2] == otherSide:
                        self.arrayLoad[i][0] = y1
                        self.arrayLoad[i][1] = y2
                        result = True
        return result

    def checkIsFocus(self,x ,side):
        '''kiem tra co phai la focus hay khong'''
        otherSide = 3 - side
        if self.checkLoad(x,otherSide):
            # kiem tra xung quanh co quan cua doi thua
            for i in range(0, 8):
                if maskGo[reference[x]][i] != 100:
                    if self.board[x + maskGo[reference[x]][i]] == otherSide:
                        self.isFocus = True
                        self.focusTo = x
                        return True
        return False
            
    def undoMove(self):
        if len(self.saveMove) == 0:
            return
        state = self.saveMove.pop()
        self.board = state.board
        self.focusTo = state.focusTo
        self.isFocus = state.isFocus


