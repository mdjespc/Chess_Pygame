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

        self.chessboard = chess.Board(8, 8)
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
        b = self.chessboard.board
 
        '''
        Check if there is a piece currently selected. If there is not, then update 'self.current_selected' to the clicked piece.
        Otherwise, if there is a piece currently selected, then the clicked obj can either be another piece from the same team, 
        a tile that the currently selected piece can move into, or none of the above.
        '''
        print(self.current_selected)
        if self.current_selected == None:
            #Storing the clicked piece on a variable. Ignore the selection if turn color does not match piece color
            try:
                self.current_selected = b[i][j] if b[i][j].color == self.turn else None
                self.current_selected.selected = True
                self.current_selected.update_valid_moves(self.chessboard.board)
            except AttributeError as err:
                print("Attribute error:", err)
                return
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
                new_action =  self.create_action(self.current_selected, (i, j))
                new_action.color = self.turn
                if b[i][j] != 0:
                    new_action.capture = True
                    self.chessboard.remove_piece(i, j)
                self.chessboard.move_piece((self.current_selected.row, self.current_selected.column), (i, j))
                print(new_action)
                self.main_log.append(new_action)

                self.current_selected.selected = False
                self.current_selected = None

                #After declaring a move, pass the turn to the other team
                
                self.alternate_turns()

            #Clicked on an irrelevant tile -> clear 'self.current_selected'
            else:
                self.current_selected.selected = False
                self.current_selected = None


    '''
    Takes in a board state, a moving piece, a destination coordinate, and the player taking the action.

    Returns a 'log.Action' object by describing the type of action that's being taken (includes origin, destination, whether an enemy is
    being captured or not, and who's taking the action). This action can then be appended to a 'log.ActionLog' that can be used to update the state
    of the board.
    '''
    def create_action(self, piece : pieces.Piece, destination):
        new_action = ''.join([self.chessboard.rows[piece.row], self.chessboard.columns[piece.column],
                          self.chessboard.rows[destination[0]], self.chessboard.columns[1]])
        new_action = log.Action(new_action)
        return new_action
    
    def alternate_turns(self):
        self.turn = "w" if self.turn == "b" else "b"
        print(f"Alternating turn to {self.turn}")

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click_event()

            self.win.blit(self.board_img, (0, 0))
            self.chessboard.draw(self.win, self.turn)
            pygame.display.update()
            self.clock.tick(30)    



if __name__ == "__main__":
    game = Game()
    game.main_loop()