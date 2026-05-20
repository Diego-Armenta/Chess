import pygame as p
from Chess import ChessEngine


#initialize game
p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = WIDTH // DIMENSION
MAX_FPS = 15
IMAGES = {}

"""
Initialize global dictionary of images
"""

def loadImages():
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
    for(piece) in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece +".png"), (SQUARE_SIZE, SQUARE_SIZE))
    #We can access images by IMAGES['wp']

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    sqSelect = ()
    playerClicks = []
    while(running):
        for(e) in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                    mouse_pos = p.mouse.get_pos()
                    #Find  x and y coords of square that was clicked on then transform them into their correspoding indicies on the board matrix
                    col = mouse_pos[0]//SQUARE_SIZE
                    row = mouse_pos[1]//SQUARE_SIZE

                    if sqSelect == (row, col): #undo function
                        sqSelect = ()
                        playerClicks = []

                    else:
                        sqSelect = (row, col)
                        playerClicks.append(sqSelect)
                        if(len(playerClicks) == 1):
                            if gs.board[(playerClicks[0])[0]][(playerClicks[0])[1]] == "--":
                                sqSelect = ()
                                playerClicks = []
                            else:
                                print(gs.getAllMoves(playerClicks[0]))

                    if len(playerClicks) == 2 and gs.board[(playerClicks[0])[0]][(playerClicks[0])[1]] != "--":
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        gs.makeMove(move)
                        sqSelect = ()
                        playerClicks = []






        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()




'''
Responsible for populating graphics of the board
'''

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)



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


    

if __name__ == '__main__':
    main()