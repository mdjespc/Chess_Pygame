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

'''
Takes in a board state, a moving piece, a destination coordinate, and the player taking the action.

Returns a 'log.Action' object by describing the type of action that's being taken (includes origin, destination, whether an enemy is
being captured or not, and who's taking the action). This action can then be appended to a 'log.ActionLog' that can be used to update the state
the board.
'''
def createAction(b: chess.Board, o: pieces.Piece, dest: tuple, plr: str) -> log.Action:
    assert plr == turn, AssertionError('Unable to create action -- It is %s team\'s action' %('White' if turn == 'w' else 'Black'))
    assert o.color == plr, AssertionError('Unable to create action -- It is %s team\'s action' %('White' if turn == 'w' else 'Black'))
    #Get string coordinate from o
    str_o = ''.join([b.str_xCoordinates[o.row], b.str_yCoordinates[o.column]])
    str_d = ''.join([b.str_xCoordinates[dest[0]],  b.str_yCoordinates[dest[1]]]) 
    dest_obj = b.board[dest[0]][dest[1]]
    A = log.Action(''.join([str_o, str_d]))
    if dest_obj == 0:
        A.capture = False
        
    elif dest_obj.color == ('b' if o.color == 'w' else 'w'):
        b.delete(dest[0], dest[1])
        A.capture = True
        
    A.color = plr
    b.move((o.row, o.column), (dest[0], dest[1]))
    return A


#MAIN LOOP ↓ ↓ ↓
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:

            i, j=click(pygame.mouse.get_pos())

            '''
            Check if there is a piece currently selected. If there is not, then update 'current_selected' to the clicked piece.
            Otherwise, if there is a piece currently selected, then the clicked obj can either be another piece from the same team, 
            a tile that the currently selected piece can move into, or none of the above.
            '''
            if current_selected == None:
                current_selected = b.board[i][j] #Storing the clicked piece on a variable
                current_selected.selected = True
                current_selected.update_valid_moves(b.board)
            #There is a currently selected piece
            else:
                #Clicked on a different piece -> switch 'current_selected' to that piece
                if isinstance(b.board[i][j], pieces.Piece) and b.board[i][j].color == turn:
                    current_selected.selected = False
                    current_selected = b.board[i][j] 
                    current_selected.selected = True
                    current_selected.update_valid_moves(b.board)
                #Clicked on a tile that our currently selected piece can move into
                elif (j, i) in current_selected.move_list:
                    main_log.append(createAction(b, current_selected, (i, j), turn))
                    current_selected.selected = False
                    current_selected = None
                #Clicked on an irrelevant tile -> clear 'current_selected'
                else:
                    current_selected.selected = False
                    current_selected = None
            

 


    win.blit(board_img, (0, 0))
    b.draw(win, color)
    pygame.display.update()
    clock.tick(30)