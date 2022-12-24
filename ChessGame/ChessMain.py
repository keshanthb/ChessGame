import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 128
IMAGES = {}

def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:
        IMAGES[piece] = p.image.load("Images/" + piece + ".png")

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))
        
"""
Responsible for all the graphics within a current game state
""" 
def drawGameState(screen, gs, validMoves, sqSelected, rect):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board, rect, sqSelected)
    
def drawBoard(screen):
    colours = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            colour = colours[((row + col) % 2)]
            p.draw.rect(screen, colour, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
def drawPieces(screen, board, rect, squareSelected):
    ''' if squareSelected:
                    piece2, x, y = getSquareUnderMouse(board)
                    if x != None and piece != "--":
                        screen.blit(IMAGES[piece], rect)
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)) '''
    sx, sy = None, None
    if squareSelected:
        piece, sx, sy = squareSelected
        
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                selected = row == sx and col == sy
                pos = p.Vector2(p.mouse.get_pos())
                screen.blit()
                

def getSquareUnderMouse(board):
    mousePosition = p.Vector2(p.mouse.get_pos())
    x, y = [int(v // SQ_SIZE) for v in mousePosition]
    try:
        if x >= 0 and y >= 0: return (board[y][x], x, y)
    except IndexError: pass
    return None, None, None

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    rect = p.Rect(64, 64, 64, 64)
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    loadImages()
    running = True
    sqSelected = ()
    squareSelected = ()
    playerClicks = []
    moveDisplayCount = 0
    moving = False
    piece, x, y = getSquareUnderMouse(gs.board)
    while(running):
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) position of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                
                rect = p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                if sqSelected == (row, col): #user clicked same square twice
                    sqSelected = ()
                    playerClicks = []
                else:
                    #deselect and clear player clicks
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                    if rect.collidepoint(event.pos):
                        moving = True
                        rect.center = p.mouse.get_pos()
                ''' if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveDisplayCount += 1
                            if moveDisplayCount == 2:
                                print(validMoves[i].getChessNotation())
                                moveDisplayCount = 0
                            else:
                                print(validMoves[i].getChessNotation() + " ", end = "")
                            moveMade = True
                            sqSelected = () # reset user clicks
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected] '''
            elif event.type == p.MOUSEBUTTONUP:
                mousePos = p.mouse.get_pos()
                x, y = [int(v // 64) for v in mousePos]
                try:
                    if x >= 0 and y >= 0 and moving == True: 
                        playerClicks.append((y, x))
                        rect = p.Rect(x * SQ_SIZE, y * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveDisplayCount += 1
                                if moveDisplayCount == 2:
                                    print(validMoves[i].getChessNotation())
                                    moveDisplayCount = 0
                                else:
                                    print(validMoves[i].getChessNotation() + " ", end = "")
                                moveMade = True
                                sqSelected = () # reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
                except IndexError: pass
                moving = False

            elif event.type == p.MOUSEMOTION and moving:
                rect.move_ip(event.rel)
                
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
            
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
                    
        drawGameState(screen, gs, validMoves, sqSelected, rect)
        #Mouse position checker
        piece, x, y = getSquareUnderMouse(gs.board)
        if x != None:
            rect2 = p.Rect(x * SQ_SIZE, y * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, (255, 0, 0, 50), rect2, 2)
            
        clock.tick(MAX_FPS)
        p.display.flip()
            
if __name__ == "__main__":   
    main()
    