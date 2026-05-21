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

    def traceSpots(self, pos, rowChange, colChange, team, moves):
        pos = (pos[0] + rowChange, pos[1] + colChange)
        if (pos[0] >= 0 and pos[0] <= 7) and (pos[1] >= 0 and pos[1] <= 7):
            if team in self.board[pos[0]][pos[1]]:
                return

            moves.append((pos[0], pos[1]))

            if self.board[pos[0]][pos[1]] == "--":
                self.traceSpots(pos, rowChange, colChange, team, moves)

    def pawnMoves(self, pos, dir, moves, piece):

        posInFront = (pos[0] + dir, pos[1])
        posLeftDiag = (posInFront[0], posInFront[1] - 1)
        leftDiagPiece = self.board[posLeftDiag[0]][posLeftDiag[1]]
        posRightDiag = (posInFront[0], posInFront[1] + 1)
        rightDiagPiece = self.board[posRightDiag[0]][posRightDiag[1]]

        if (posLeftDiag[0] >= 0 and posLeftDiag[0] <= 7) and (posLeftDiag[1] >= 0 and posLeftDiag[1] <= 7):
            if self.checkIfOccupied(posLeftDiag) is True and self.checkIfEnemy(piece, leftDiagPiece) :
                moves.append(posLeftDiag)

        if (posRightDiag[0] >= 0 and posRightDiag[0] <= 7) and (posRightDiag[1] >= 0 and posRightDiag[1] <= 7):
            if self.checkIfOccupied(posRightDiag) is True and self.checkIfEnemy(piece, rightDiagPiece) :
                moves.append(posRightDiag)


        if (posInFront[0] >= 0 and posInFront[0] <= 7) and (posInFront[1] >= 0 and posInFront[1] <= 7):
            if self.checkIfOccupied(posInFront) is True:
                return

            moves.append(posInFront)

            doubleJump = (posInFront[0] + dir, posInFront[1])
            if self.hasBeenMoved(pos,'P') is False:
                if self.checkIfOccupied(doubleJump) is False:
                    moves.append(doubleJump)
            return




    def hasBeenMoved(self, pos, piece):
        """
        Checks if piece has been moved but needs different implementation for pawns, vs Kings and Rooks, as they can return to their OG square
        """
        if 'P' in piece:
            startBoard = board=[
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]
            if startBoard[pos[0]][pos[1]] == self.board[pos[0]][pos[1]]:
                return False
            else:
                return True









    def getAllMoves(self, start):
        piece = self.board[start[0]][start[1]]
        moves = []
        match piece:
                case 'wP':
                    self.pawnMoves(start, -1, moves, 'wP')
                    return moves

                case 'bP':
                    self.pawnMoves(start, 1, moves, 'bP')
                    return moves

                case _ if 'R' in piece:
                    team = piece[0]
                    self.traceSpots(start, 0, 1, team, moves)
                    self.traceSpots(start, 1, 0, team, moves)
                    self.traceSpots(start, 0, -1, team, moves)
                    self.traceSpots(start, -1, 0, team, moves)
                    return moves

                case _ if 'N' in piece:
                    for i in range(8):
                        for j in range(8):
                            differenceX = start[0] - i
                            differenceY = start[1] - j
                            if (abs(differenceX) == 2 and abs(differenceY) == 1 or
                                abs(differenceX) == 1 and abs(differenceY) == 2):
                                if self.checkIfOccupied((i,j)) is False or self.checkIfEnemy(piece, self.board[i][j]) is True:
                                    moves.append((i,j))
                    return moves

                case _ if 'B' in piece:
                    team = piece[0]
                    self.traceSpots(start, 1, 1, team, moves)
                    self.traceSpots(start, 1, -1, team, moves)
                    self.traceSpots(start, -1, 1, team, moves)
                    self.traceSpots(start, -1, -1, team, moves)
                    return moves

                case _ if 'Q' in piece:
                    team = piece[0]
                    self.traceSpots(start, 0, 1, team, moves)
                    self.traceSpots(start, 1, 0, team, moves)
                    self.traceSpots(start, 0, -1, team, moves)
                    self.traceSpots(start, -1, 0, team, moves)
                    self.traceSpots(start, 1, 1, team, moves)
                    self.traceSpots(start, 1, -1, team, moves)
                    self.traceSpots(start, -1, 1, team, moves)
                    self.traceSpots(start, -1, -1, team, moves)
                    return moves

                case _ if 'K' in piece:
                    for i in range(8):
                        for j in range(8):
                            differenceX = start[0] - i
                            differenceY = start[1] - j
                            if abs(differenceX) <= 1 and abs(differenceY) <= 1:
                                if differenceX !=0 or differenceY != 0:
                                    if self.checkIfOccupied((i, j)) is False or self.checkIfEnemy(piece, self.board[i][j]) is True:
                                        moves.append((i,j))
                    return moves

    def checkIfOccupied(self, newSquare):
        newSquarePiece = self.board[newSquare[0]][newSquare[1]]
        if newSquarePiece != "--":
            return True
        else:
            return False

    def checkIfEnemy(self, piece, otherPiece):
        if piece[0] != otherPiece[0]:
            return True
        else:
            return False

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






