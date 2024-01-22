import pygame
import os
path=os.path.join("chessPieces", "whitePieces")
wpawn=pygame.image.load(os.path.join(path, "pawn.png"))
wbishop=pygame.image.load(os.path.join(path, "bishop.png"))
wqueen=pygame.image.load(os.path.join(path, "queen.png"))
wking=pygame.image.load(os.path.join(path, "king.png"))
wrook=pygame.image.load(os.path.join(path, "rook.png"))
wknight=pygame.image.load(os.path.join(path, "knight.png"))

path=os.path.join("chessPieces", "blackPieces")
bpawn=pygame.image.load(os.path.join(path, "pawn1.png"))
bbishop=pygame.image.load(os.path.join(path, "bishop1.png"))
bqueen=pygame.image.load(os.path.join(path, "queen1.png"))
bking=pygame.image.load(os.path.join(path, "king1.png"))
brook=pygame.image.load(os.path.join(path, "rook1.png"))
bknight=pygame.image.load(os.path.join(path, "knight1.png"))

b=[bpawn, bbishop, bqueen, bking, brook, bknight]
B=[]
w=[wpawn, wbishop, wqueen, wking, wrook, wknight]
W=[]

for image in b:
    B.append(pygame.transform.scale(image, (70, 70)))
for image in w:
    W.append(pygame.transform.scale(image, (70, 70)))
class Piece:
    img=-1
    board_co=(16, 16, 555, 555)
    startx=board_co[0]
    starty=board_co[1]
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.selected = False #USE it to know whether a piece is eligible to move
        self.move_list = [] 
        self.king = False
        self.pawn = False
        self.live = True
    def draw(self, win, color):
        if self.color=="w":
            draw_this=W[self.img]
        else:
            draw_this=B[self.img]
        #(4-column)+(113+(column*525/6))
        x=(4-self.column)+round(self.startx+(self.column*self.board_co[2]/6))
        y=3+round(self.starty+(self.row*self.board_co[3]/6))
        if self.selected and self.color==color:
            pygame.draw.rect(win, '#1ae016', (x, y, 62, 62), 4)
            x_offset = 45
            y_offset = 45
            if self.move_list != None:
                for coor in self.move_list:
                    coorx=(self.board_co[2]/6)*coor[1] + 8 + x_offset #(4-z[0])+round(113+(z[0]*525/6))-42
                    coory=(self.board_co[2]/6)*coor[0] + 8 + y_offset #3+round(113+(z[1]*525/6))-138
                    pygame.draw.circle(win, "#C0C0C0", (coorx, coory), 28)


        win.blit(draw_this, (x, y))
    def update_valid_moves(self, board):
        self.move_list=self.valid_moves(board)

    def delete(self):
        self.live = False

    def toString(self):
        return '0'
    
class Pawn(Piece):
    img=0
    def __init__(self, row, column, color):
        super().__init__(row, column, color)
        self.first=True
        self.pawn=True
    def valid_moves(self, board):
        i=self.row
        j=self.column
        moves=[]
        
        pos_to_check = [(i + 1, j), (i + 2, j)] if self.first else [(i + 1, j)]
        for pos in pos_to_check:
              #Check if the calculated position exists on the board
            try: 
                piece_at_pos = board[pos[0]][pos[1]]
                diag_1 = board[i + 1][j - 1]
                diag_2 = board[i + 1][j + 1]
            except IndexError:
                continue
            #If the position exists, test if it is taken by an allied piece, an enemy piece, or if it's empty
            if not isinstance(piece_at_pos, Piece):
                moves.append(pos)

            if isinstance(diag_1, Piece) and diag_1.color != self.color:
                moves.append((diag_1.row, diag_1.column))
            if isinstance(diag_2, Piece) and diag_2.color != self.color:
                moves.append((diag_2.row, diag_2.column))
        return moves
    
    def toString(self):
        return 'P'
class Bishop(Piece):
    img=1
    def valid_moves(self, board):
        i = self.row
        j = self.column
        moves = []

        i_direction = (1, 1, -1, -1)
        j_direction = (1, -1, -1, 1)
        for direction in zip(i_direction, j_direction):
            for k in range(len(board) - 1):
                #Given a direction and a length of path k, calculate a possible position for the piece to move into
                row_offset, column_offset = (k + 1) * direction[0], (k + 1) * direction[1]
                pos = (i + row_offset, j + column_offset)
                #Check if the calculated position exists on the board
                try: 
                    piece_at_pos = board[pos[0]][pos[1]]
                except IndexError:
                    break
                #If the position exists, test if it is taken by an allied piece, an enemy piece, or if it's empty
                if not isinstance(piece_at_pos, Piece) or piece_at_pos.color != self.color:
                    moves.append(pos)
                if isinstance(piece_at_pos, Piece):
                    break
        return moves

    def toString(self):
        return 'B'
class Queen(Piece):
    img=2
    def valid_moves(self, board):
        i = self.row
        j = self.column
        moves = []

        i_direction = (1, 1, 0, -1, -1, -1, 0, 1)
        j_direction = (0, 1, 1, 1, 0, -1, -1, -1)
        for direction in zip(i_direction, j_direction):
            for k in range(len(board) - 1):
                #Given a direction and a length of path k, calculate a possible position for the piece to move into
                row_offset, column_offset = (k + 1) * direction[0], (k + 1) * direction[1]
                pos = (i + row_offset, j + column_offset)
                #Check if the calculated position exists on the board
                try: 
                    piece_at_pos = board[pos[0]][pos[1]]
                except IndexError:
                    break
                #If the position exists, test if it is taken by an allied piece, an enemy piece, or if it's empty
                if not isinstance(piece_at_pos, Piece) or piece_at_pos.color != self.color:
                    moves.append(pos)
                if isinstance(piece_at_pos, Piece):
                    break
        return moves
    def toString(self):
        return 'Q'
class King(Piece):
    img=3

    def valid_moves(self, board):
        i = self.row
        j = self.column
        moves = []

        pos_to_check = [(i + 1, j), 
                        (i, j + 1),
                        (i - 1, j),
                        (i, j - 1), 
                        (i + 1, j + 1),
                        (i - 1, j + 1),
                        (i - 1, j - 1),
                        (i + 1, j - 1)]
        for pos in pos_to_check:
            #Check if the calculated position exists on the board
            try: 
                piece_at_pos = board[pos[0]][pos[1]]
            except IndexError:
                continue
            #If the position exists, test if it is taken by an allied piece, an enemy piece, or if it's empty
            if not isinstance(piece_at_pos, Piece) or piece_at_pos.color != self.color:
                moves.append(pos)

        return moves

    
    def toString(self):
        return 'K'
class Rook(Piece):
    img=4
    def valid_moves(self, board):
        i = self.row
        j = self.column
        moves = []

        i_direction = (1, 0, -1, 0)
        j_direction = (0, 1, 0, -1)
        for direction in zip(i_direction, j_direction):
            for k in range(len(board) - 1):
                #Given a direction and a length of path k, calculate a possible position for the piece to move into
                row_offset, column_offset = (k + 1) * direction[0], (k + 1) * direction[1]
                pos = (i + row_offset, j + column_offset)
                #Check if the calculated position exists on the board
                try: 
                    piece_at_pos = board[pos[0]][pos[1]]
                except IndexError:
                    break
                #If the position exists, test if it is taken by an allied piece, an enemy piece, or if it's empty
                if not isinstance(piece_at_pos, Piece) or piece_at_pos.color != self.color:
                    moves.append(pos)
                if isinstance(piece_at_pos, Piece):
                    break
        return moves

    def toString(self):
        return 'R'
class Knight(Piece):
    img=5
    def valid_moves(self, board):
        i = self.row
        j = self.column
        moves = []

        pos_to_check = [(i + 2, j + 1), (i + 1, j + 2), 
                        (i - 1, j + 2), (i - 2, j + 1),
                        (i - 2, j - 1), (i - 1, j - 2),
                        (i + 1, j - 2), (i + 2, j - 1)]
        for pos in pos_to_check:
            #Check if the calculated position exists on the board
            try: 
                piece_at_pos = board[pos[0]][pos[1]]
            except IndexError:
                continue
            #If the position exists, test if it is taken by an allied piece, an enemy piece, or if it's empty
            if not isinstance(piece_at_pos, Piece) or piece_at_pos.color != self.color:
                moves.append(pos)

        return moves
    def toString(self):
        return 'N'



