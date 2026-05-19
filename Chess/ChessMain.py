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
    select = False
    toMoveX = 0
    toMoveY = 0
    destX = 0
    destY = 0
    running = True
    while(running):
        for(e) in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if select is False:
                    mouse_pos = p.mouse.get_pos()
                    #Find  x and y coords of square that was clicked on then transform them into their correspoding indicies on the board matrix
                    toMoveX = int(mouse_pos[0]/(DIMENSION**2))
                    toMoveY = int(mouse_pos[1]/(DIMENSION**2))
                    select = True
                    print(toMoveX, " ", toMoveY)
                elif select:
                    mouse_pos = p.mouse.get_pos()
                    # Find  x and y coords of square that was clicked on then transform them into their correspoding indicies on the board matrix
                    destX = int(mouse_pos[0] / (DIMENSION ** 2))
                    destY = int(mouse_pos[1] / (DIMENSION ** 2))
                    print(destY, " " , destX, "Dest")
                    select = False
                    piece = gs.board[toMoveY][toMoveX]
                    gs.board[toMoveY][toMoveX] = '--'
                    gs.board[destY][destX] = piece





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
    colors = [p.Color("cornsilk2"), p.Color("midnightblue")]
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