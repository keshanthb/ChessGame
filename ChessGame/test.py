from xml.dom import xmlbuilder
import pygame as p
import ChessEngine

moving = False
screen = p.display.set_mode((512, 512))
rect = p.Rect(64, 64, 64, 64)
running = True
playerClicks = []
gs = ChessEngine.GameState()
validMoves = gs.getValidMoves()
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

        elif event.type == p.MOUSEBUTTONDOWN:
            location = p.mouse.get_pos() #(x,y) position of mouse
            col = location[0] // 64
            row = location[1] // 64
            playerClicks.append((row, col))
            print(playerClicks)
            if rect.collidepoint(event.pos):
                moving = True
                rect.center = p.mouse.get_pos()

        elif event.type == p.MOUSEBUTTONUP:
            mousePos = p.mouse.get_pos()
            x, y = [int(v // 64) for v in mousePos]
            try:
                if x >= 0 and y >= 0 and moving == True: 
                    playerClicks.append((y, x))
                    print(playerClicks)
                    rect = p.Rect(x * 64, y * 64, 64, 64)
                    
                    playerClicks = []
            except IndexError: pass
            moving = False

        elif event.type == p.MOUSEMOTION and moving:
            rect.move_ip(event.rel)
        
    screen.fill(p.Color("GRAY"))
    colours = [p.Color("white"), p.Color("gray")]
    for row in range(8):
        for col in range(8):
            colour = colours[((row + col) % 2)]
            p.draw.rect(screen, colour, p.Rect(col * 64, row * 64, 64, 64))
    
    #p.draw.rect(screen, p.Color("RED"), rect)
    screen.blit(p.image.load("c:/Users/Keshanth/Documents/Chess/Images/wP.png"), rect)
    # if moving:
    #     p.draw.rect(screen, p.Color("BLUE"), rect, 4)
    p.display.flip()

p.quit()