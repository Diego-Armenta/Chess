import pygame as p
from Chess import ChessEngine


#initialize game
p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = WIDTH // DIMENSION
MAX_FPS = 15
playableSquares = []
IMAGES = {}
DOT = {}

"""
Initialize global dictionary of images
"""

def loadImages():
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
    DOT[0] = p.transform.scale(p.image.load("images/dot.png"), (SQUARE_SIZE, SQUARE_SIZE)) #load in dot
    for(piece) in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece +".png"), (SQUARE_SIZE, SQUARE_SIZE))
    #We can access images by IMAGES['wp']

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("yellow"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    sqSelect = ()
    playerClicks = []
    playableSquares = []
    while(running):
        for(e) in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                    mouse_pos = p.mouse.get_pos()

                    #Find  x and y coords of square that was clicked on then transform them into their corresponding indicies on the board matrix
                    col = mouse_pos[0]//SQUARE_SIZE
                    row = mouse_pos[1]//SQUARE_SIZE
                    loop = True
                    skip = False
                    while(loop is True):
                        loop = False
                        if sqSelect == (row, col) and skip is False: #undo function if user clicks back on starting square
                            sqSelect = ()
                            playerClicks = []
                            skip = False

                            """
                        In the else it takes users selection, and if it is the source square and not end square, it does 
                        a validity check that it is not
                        a blank square
                        a white piece on blacks turn
                        a black piece on whites turn
                        or else it will flush the select and clicks
                        
                        if it is the source square and valid, program will retrieve the valid moves from that piece
                        """

                        else:
                            sqSelect = (row, col)
                            playerClicks.append(sqSelect)
                            if(len(playerClicks) == 1):
                                piece = gs.board[(playerClicks[0])[0]][(playerClicks[0])[1]]
                                if ( piece == "--"
                                    or (piece[0] == 'w' and gs.whiteToMove is False)
                                    or (piece[0] == 'b' and gs.whiteToMove is True)
                                    ):
                                    sqSelect = ()
                                    playerClicks = []
                                else:
                                    playableSquares = gs.getValidMoves(playerClicks[0])
                                    p.draw.rect(screen, "red",
                                                p.Rect(row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)

                        if len(playerClicks) == 2:
                            if playerClicks[1] in playableSquares:
                                move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                                gs.makeMove(move)
                                print(move.getChessNotation(gs))
                                sqSelect = ()
                                playerClicks = []
                            elif (
                                    (gs.board[(playerClicks[1])[0]][(playerClicks[1])[1]])
                                == "--"
                            ):
                                sqSelect = playerClicks[0]
                                playerClicks = []
                                playerClicks.append(sqSelect)

                            elif (
                                    (gs.board[(playerClicks[1])[0]][(playerClicks[1])[1]])[0]
                                == (gs.board[(playerClicks[0])[0]][(playerClicks[0])[1]])[0]
                            ):
                                """
                                Checks if source piece and selected piece are same team. 
                                If so it will automatically switch source piece to the second click instead of acting as undo
                                """
                                loop = True
                                skip = True
                                playerClicks = []
                            print(gs.enPassantable)





        drawGameState(screen, gs, playerClicks, playableSquares)
        clock.tick(MAX_FPS)
        p.display.flip()




'''
Responsible for populating graphics of the board
'''

def drawGameState(screen, gs, playerClicks, playableSquares):
    drawBoard(screen)
    drawPieces(screen, gs.board)
    if len(playerClicks) == 1:
        drawViableMoves(screen, playableSquares, gs.board)






'''
Draws board before pieces populate. Top left square always light.
'''
def drawBoard(screen):
    colors = [p.Color("pink"), p.Color("midnightblue")]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[((i+j) % 2)]
            p.draw.rect(screen, color, p.Rect(j*SQUARE_SIZE, i*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

'''
Draws pieces according to gamestate
'''
def drawPieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(j*SQUARE_SIZE, i*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawViableMoves(screen, playableSquares, board):
    for i in playableSquares:
        if (board[i[0]][i[1]]) != "--":
            (DOT[0]).set_alpha(30)
            p.draw.circle(screen, (80, 80, 80),
                          ((i[1] * SQUARE_SIZE + SQUARE_SIZE / 2), (i[0] * SQUARE_SIZE) + SQUARE_SIZE / 2),
                          SQUARE_SIZE / 2, 4)
        else:
            (DOT[0]).set_alpha(60)
            screen.blit(DOT[0], p.Rect(i[1] * SQUARE_SIZE, i[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



    

if __name__ == '__main__':
    main()