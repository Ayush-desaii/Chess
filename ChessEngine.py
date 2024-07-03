class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = () #square where en-passant can happen
        self.enpassantPossibleLog = [self.enpassantPossible]
        #castling rights
        self.currentCastlingRight = castleRights(True, True, True, True)
        self.castleRightsLog = [castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    def makeMove(self, move):
        self.board[move.strow][move.stcol] = "--"
        self.board[move.endrow][move.endcol] = move.piecemoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        #update king's position
        if move.piecemoved == 'wK':
            self.whiteKingLocation = (move.endrow, move.endcol)
        elif move.piecemoved == 'bK':
            self.blackKingLocation = (move.endrow, move.endcol)

        if move.isPawnPromotion:
            self.board[move.endrow][move.endcol] = move.piecemoved[0] + "Q"

        #update board after enpassant move
        if move.isEnpassantMove:
            self.board[move.strow][move.endcol] = "--"

        #if pawn moved twice, next move can capture enpassant
        if move.piecemoved[1] == "P" and abs(move.strow - move.endrow) == 2:
            self.enpassantPossible = ((move.strow + move.endrow)//2, move.stcol)
        else:
            self.enpassantPossible = ()

        #update board after castle move
        if move.isCastleMove:
            if move.endcol - move.stcol == 2:
                self.board[move.endrow][move.endcol-1] = self.board[move.endrow][move.endcol+1]
                self.board[move.endrow][move.endcol+1] = "--"
            else:
                self.board[move.endrow][move.endcol+1] = self.board[move.endrow][move.endcol-2]
                self.board[move.endrow][move.endcol-2] = "--"
        
        self.enpassantPossibleLog.append(self.enpassantPossible)

        #update castling rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.strow][move.stcol] = move.piecemoved #put piece on starting square
            self.board[move.endrow][move.endcol] = move.piececap #put back captured piece
            self.whiteToMove = not self.whiteToMove #switch turns

            #update kings position
            if move.piecemoved == 'wK':
                self.whiteKingLocation = (move.strow, move.stcol)
            elif move.piecemoved == 'bK':
                self.blackKingLocation = (move.strow, move.stcol)

            #undo enpassant
            if move.isEnpassantMove:
                self.board[move.endrow][move.endcol] = "--" #remove the moved pawn
                self.board[move.strow][move.endcol] = move.piececap #put the pawn back

            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

            #get back enpassant right if pawn was moved 2 square
            if move.piecemoved[1] == "P" and abs(move.strow - move.endrow) == 2:
                self.enpassantPossible = ()

            #undo castle rights
            self.castleRightsLog.pop()
            newR = self.castleRightsLog[-1]
            self.currentCastlingRight = castleRights(newR.wks, newR.bks, newR.wqs, newR.bqs)
            if move.isCastleMove:
                if move.endcol - move.stcol == 2: #king side
                    self.board[move.endrow][move.endcol+1] = self.board[move.endrow][move.endcol-1] #move rook
                    self.board[move.endrow][move.endcol-1] = "--" #rook was
                else:
                    self.board[move.endrow][move.endcol-2] = self.board[move.endrow][move.endcol+1] #move rook
                    self.board[move.endrow][move.endcol+1] = "--" #rook was

            self.checkMate = False
            self.staleMate = False


    def updateCastleRights(self, move):
        if move.piecemoved == "wK":
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.piecemoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.piecemoved == "wR":
            if move.strow == 7:
                if move.stcol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.stcol == 7:
                    self.currentCastlingRight.wks = False
        elif move.piecemoved == "bR":
            if move.strow == 0:
                if move.stcol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.stcol == 7:
                    self.currentCastlingRight.bks = False

        #if rook is captured
        if move.piececap == "wR" and move.endrow == 7:
            if move.endcol == 0:
                self.currentCastlingRight.wqs = False
            elif move.endcol == 7:
                self.currentCastlingRight.wks = False

        if move.piececap == "bR" and move.endrow == 0:
            if move.endcol == 0:
                self.currentCastlingRight.bqs = False
            elif move.endcol == 7:
                self.currentCastlingRight.bks = False

        


    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        moves =  self.getAllMoves()
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endrow == r and move.endcol == c:
                return True
        return False


    def getAllMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassantMove=True))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove=True))

        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassantMove=True))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassantMove=True))

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))



    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(r, c, moves)

    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))

class castleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():

    ranks_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_ranks = {v: k for k, v in ranks_rows.items()}
    files_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_files = {v: k for k, v in files_cols.items()}

    def __init__(self, stsq, endsq, board, isEnpassantMove=False, isCastleMove=False):
        self.strow = stsq[0]
        self.stcol = stsq[1]
        self.endrow = endsq[0]
        self.endcol = endsq[1]
        self.piecemoved = board[self.strow][self.stcol]
        self.piececap = board[self.endrow][self.endcol]
        self.isPawnPromotion = (self.piecemoved == "wP" and self.endrow == 0) or (self.piecemoved == "bP" and self.endrow == 7)
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.piececap = "wP" if self.piecemoved == "bP" else "bP"
        self.isCastleMove = isCastleMove

        self.moveID = self.strow * 1000 + self.stcol * 100 + self.endrow * 10 + self.endcol
        
    def __eq__(self, other) -> bool:
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def chess_notation(self):
        return self.rank_file(self.strow, self.stcol) + self.rank_file(self.endrow, self.endcol)
    
    def rank_file(self, r, c):
        return self.cols_files[c] + self.rows_ranks[r]