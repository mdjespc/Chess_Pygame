import pygame
import os
import time
import chess
import pieces
import log

pygame.init()
clock = pygame.time.Clock()

width = 750
height = 750
color = "w"
turn = "w"
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Game")
board_img = pygame.transform.scale(pygame.image.load(os.path.join("chessPieces", "board.png")), (750, 750))
chessbg = pygame.image.load(os.path.join("chessPieces", "bg.png"))

rect = (16, 16, 555, 555)

b = chess.Board(8, 8)
main_log = log.ActionLog()
current_selected: pieces.Piece = None

def click(pos):
    x=pos[0]
    y=pos[1]
    if (rect[0]<x<height):
        if rect[1]<y<width:
            div_x=x-rect[0]/2
            div_y=y-rect[1]/2
            i=int(div_y/(rect[2]/6))
            j=int(div_x/(rect[3]/6))
            return i, j
    return -1, -1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            quit()
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:

            i, j=click(pygame.mouse.get_pos())
            print(b.board[i][j], i, j)  #Testing if the position is filled with an actual piece
            #Case 1: Selecting a tile with a piece
            if b.board[i][j] != 0:
                #Hard coding black pieces as enemy for now.
                if b.board[i][j].color == 'b' and current_selected != None and (j, i) in current_selected.move_list:
                    #Deleting the piece and moving the selected piece on its place
                    b.delete(i, j)
                    b.move((current_selected.row, current_selected.column), (i, j))
                    print(b.captured_pieces)
                    current_selected.selected = False
                    current_selected = None
                    break



                if isinstance(current_selected, pieces.Piece): current_selected.selected = False
                current_selected = b.board[i][j] #Storing the clicked piece on a variable
                current_selected.selected = True
                current_selected.update_valid_moves(b.board)
                print(current_selected.move_list)
            #Case 2: Selecting an empty tile - is it a valid move for a previously selected piece?
            elif b.board[i][j] == 0 and current_selected != None:
                if (j, i) in current_selected.move_list:
                    main_log.append(log.Action(b.str_xCoordinates[current_selected.column] + b.str_yCoordinates[current_selected.row] + b.str_xCoordinates[j] + b.str_yCoordinates[i]))
                    b.move((current_selected.row, current_selected.column), (i, j))
                    print('ACTION LOG ->', main_log)
                    current_selected.selected = False
                    current_selected = None
            #Case 3: Selecting an empty tile with no tasks available - no piece selected
            else:
                pass



    win.blit(board_img, (0, 0))
    b.draw(win, color)
    pygame.display.update()
    clock.tick(30)