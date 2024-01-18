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
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.strow][move.stcol] = "--"
        self.board[move.endrow][move.endcol] = move.piecemoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove


class Move():

    ranks_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_ranks = {v: k for k, v in ranks_rows.items()}
    files_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_files = {v: k for k, v in files_cols.items()}

    def __init__(self, stsq, endsq, board) -> None:
        self.strow = stsq[0]
        self.stcol = stsq[1]
        self.endrow = endsq[0]
        self.endcol = endsq[1]
        self.piecemoved = board[self.strow][self.stcol]
        self.piececap = board[self.endrow][self.endcol]

    def chess_notation(self):
        return self.rank_file(self.strow, self.stcol) + self.rank_file(self.endrow, self.endcol)
    
    def rank_file(self, r, c):
        return self.cols_files[c] + self.rows_ranks[r]