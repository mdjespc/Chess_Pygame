import pygame
import os
import time
import chess
import pieces
import log

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.width = 750
        self.height = 750
        self.color = "w"
        self.turn = "w"
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Chess Game")
        self.board_img = pygame.transform.scale(pygame.image.load(os.path.join("chessPieces", "board.png")), (self.width, self.height))
        self.rect = (16, 16, 555, 555)

        self.chess_board = chess.Board(8, 8)
        self.main_log = log.ActionLog()
        self.current_selected = None

    def get_click_coordinates(self, pos):
        x=pos[0]
        y=pos[1]
        if (self.rect[0] < x < self.height):
            if self.rect[1] < y < self.width:
                div_x = x - self.rect[0]/2
                div_y = y - self.rect[1]/2
                i = int(div_y/(self.rect[2]/6))
                j = int(div_x/(self.rect[3]/6))
                return i, j
        return -1, -1

    def handle_click_event(self):
        i, j = self.get_click_coordinates(pygame.mouse.get_pos())
        b = self.chess_board.board
        '''
        Check if there is a piece currently selected. If there is not, then update 'self.current_selected' to the clicked piece.
        Otherwise, if there is a piece currently selected, then the clicked obj can either be another piece from the same team, 
        a tile that the currently selected piece can move into, or none of the above.
        '''
        if self.current_selected == None:
            self.current_selected = b[i][j] #Storing the clicked piece on a variable
            self.current_selected.selected = True
            self.current_selected.update_valid_moves(self.chess_board.board)
        #There is a currently selected piece
        else:
            #Clicked on a different piece -> switch 'self.current_selected' to that piece
            if isinstance(b[i][j], pieces.Piece) and b[i][j].color == self.turn:
                self.current_selected.selected = False
                self.current_selected = b[i][j] 
                self.current_selected.selected = True
                self.current_selected.update_valid_moves(b)
            #Clicked on a tile that our currently selected piece can move into
            elif (i, j) in self.current_selected.move_list:
                self.main_log.append(self.create_action(self.current_selected, (i, j)))
                self.current_selected.selected = False
                self.current_selected = None
            #Clicked on an irrelevant tile -> clear 'self.current_selected'
            else:
                self.current_selected.selected = False
                self.current_selected = None


    '''
    Takes in a board state, a moving piece, a destination coordinate, and the player taking the action.

    Returns a 'log.Action' object by describing the type of action that's being taken (includes origin, destination, whether an enemy is
    being captured or not, and who's taking the action). This action can then be appended to a 'log.ActionLog' that can be used to update the state
    the board.
    '''
    def create_action(self, origin, dest):
        #assert self.plr == self.turn, AssertionError('Unable to create action -- It is %s team\'s action' %('White' if self.turn == 'w' else 'Black'))
        #assert origin.color == self.plr, AssertionError('Unable to create action -- It is %s team\'s action' %('White' if self.turn == 'w' else 'Black'))
        #Get string coordinate from o
        str_o = ''.join([self.chess_board.str_xCoordinates[origin.row], self.chess_board.str_yCoordinates[origin.column]])
        str_d = ''.join([self.chess_board.str_xCoordinates[dest[0]],  self.chess_board.str_yCoordinates[dest[1]]]) 
        dest_obj = self.chess_board.board[dest[0]][dest[1]]
        A = log.Action(''.join([str_o, str_d]))
        if dest_obj == 0:
            A.capture = False
            
        elif dest_obj.color == ('b' if origin.color == 'w' else 'w'):
            self.chess_board.delete(dest[0], dest[1])
            A.capture = True
            
        #A.color = self.plr
        self.chess_board.move((origin.row, origin.column), (dest[0], dest[1]))
        print(A)
        return A

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click_event()

            self.win.blit(self.board_img, (0, 0))
            self.chess_board.draw(self.win, self.color)
            pygame.display.update()
            self.clock.tick(30)    



if __name__ == "__main__":
    game = Game()
    game.main_loop()