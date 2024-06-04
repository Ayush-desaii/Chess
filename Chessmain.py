import pygame as p 
"""import sys
print(sys.path)
"""
import ChessEngine

HEIGHT = WIDTH = 400
DIMENSION = 8
SQ_SIZE = int(HEIGHT / DIMENSION)
MAX_FPS = 15
IMAGES = {}

def load_images():
    pieces = ["bP", "bR", "bN", "bB", "bQ", "bK", "wP", "wR", "wN", "wB", "wQ", "wK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("pieces/"+ piece +".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((HEIGHT, WIDTH))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    MoveMade = False
    
    load_images()
    running = True
    sqSelected = ()
    clicks = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    clicks = []
                else:
                    sqSelected = (row, col)
                    clicks.append(sqSelected)
                if len(clicks) == 2:
                    move = ChessEngine.Move(clicks[0], clicks[1], gs.board)
                    print(move.chess_notation(), validMoves)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            MoveMade = True
                            sqSelected = ()
                            clicks = []
                    if not MoveMade:
                        clicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    MoveMade = True

        if MoveMade:
            validMoves = gs.getValidMoves()
            MoveMade = False

        draw_game_state(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()

# square selection to show moves
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #check if sq selected can move 
            #highlight sq
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #trasperancy
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight moves from that sq
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.strow == r and move.stcol == c:
                    screen.blit(s, (move.endcol*SQ_SIZE, move.endrow*SQ_SIZE))

def draw_game_state(screen, gs, validMoves, sqSelected):
    draw_board(screen) #draw sq on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    draw_pieces(screen, gs.board) #draw pieces on the top of the sq

def draw_board(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
