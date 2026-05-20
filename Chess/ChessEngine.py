class GameState():
    def __init__(self):
        self.board=[
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def getAllMoves(self, start):
        piece = self.board[start[0]][start[1]]
        moves = []
        match piece:
                case 'wP':
                    if(start[0] == 6):
                        moves.append((4, start[1]))
                    moves.append((start[0]-1, start[1]))
                    return moves

                case 'bP':
                    if (start[0] == 1):
                        moves.append((3, start[1]))
                    moves.append((start[0] + 1, start[1]))
                    return moves

                case _ if 'R' in piece:
                    for i in range(8):
                        if i is not start[0]:
                            moves.append((i, start[1]))
                        if i is not start[1]:
                            moves.append((start[0], i))
                    return moves

                case _ if 'N' in piece:
                    for i in range(8):
                        for j in range(8):
                            differenceX = start[0] - i
                            differenceY = start[1] - j
                            if (abs(differenceX) == 2 and abs(differenceY) == 1 or
                                abs(differenceX) == 1 and abs(differenceY) == 2):
                                moves.append((i,j))
                    return moves

                case _ if 'B' in piece:
                    for i in range(8):
                        for j in range(8):
                            differenceX = start[0] - i
                            differenceY = start[1] -j
                            if abs(differenceX) == abs(differenceY) and differenceX != 0:
                                moves.append((i,j))
                    return moves

                case _ if 'Q' in piece:
                    for i in range(8):
                        if i is not start[0]:
                            moves.append((i, start[1]))
                        if i is not start[1]:
                            moves.append((start[0], i))
                        for j in range(8):
                                differenceX = start[0] - i
                                differenceY = start[1] - j
                                if abs(differenceX) == abs(differenceY) and differenceX != 0:
                                    moves.append((i, j))
                    return moves

                case _ if 'K' in piece:
                    for i in range(8):
                        for j in range(8):
                            differenceX = start[0] - i
                            differenceY = start[1] - j
                            if abs(differenceX) <= 1 and abs(differenceY) <= 1:
                                if differenceX !=0 or differenceY != 0:
                                    moves.append((i,j))
                    return moves

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"h": 7, "g": 6, "f": 5, "e": 4,
                   "d": 3, "c": 2, "b": 1, "a": 0}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    groupPieces = {
        "": ['wP', 'bP'],
        "R":['wR', 'bR'],
        "N": ["wN", "bN"],
        "B": ["wB", "bB"],
        "Q": ["wQ", "bQ"],
        "K": ['wK', "bK"]
    }
    piecesToNames = {
                    key:value
                    for value, keys in groupPieces.items()
                    for key in keys
    }

    def __init__(self, startSq, endSq, board):
            self.startRow = startSq[0]
            self.startCol = startSq[1]
            self.endRow = endSq[0]
            self.endCol = endSq[1]
            self.pieceMoved = board[self.startRow][self.startCol]
            self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
            return f"{self.piecesToNames[self.pieceMoved]}{self.getRankFile(self.endRow, self.endCol)}"

    def getRankFile(self, r, c):
            return self.colsToFiles[c] + self.rowsToRanks[r]






