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
            pygame.draw.rect(win, (255, 0, 0), (x, y, 62, 62), 4)
            x_offset = 45
            y_offset = 45
            if self.move_list != None:
                for coor in self.move_list:
                    coorx=(self.board_co[2]/6)*coor[0] + 8 + x_offset #(4-z[0])+round(113+(z[0]*525/6))-42
                    coory=(self.board_co[2]/6)*coor[1] + 8 + y_offset #3+round(113+(z[1]*525/6))-138
                    pygame.draw.circle(win, "#eb344c", (coorx, coory), 28)


        win.blit(draw_this, (x, y))
    def update_valid_moves(self, board):
        self.move_list=self.valid_moves(board)

    def delete(self):
        self.live = False

    def toString(self):
        return 0
    
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
        #valid moves for white
        if self.color=="w":
            try:
                if board[i + 1][j] == 0:
                    moves.append((j, i + 1))
            except IndexError:
                pass
            try:
                if board[i + 2][j] == 0 and self.first:
                    moves.append((j, i + 2))
            except IndexError:
                pass
            
            #Test if there is an enemy piece diagonal to pawn
            try:
                if board[i + 1][j - 1] != 0 and board[i + 1][j - 1].color == 'b':
                    moves.append((j - 1, i + 1))
            except IndexError:
                pass
            try:
                if board[i + 1][j + 1] != 0 and board[i + 1][j + 1].color == 'b':
                    moves.append((j + 1, i + 1))
            except IndexError:
                pass
                
        #valid moves for black
        else:
            pass
        return moves
    
    def toString(self):
        return 'P'
class Bishop(Piece):
    img=1
    def valid_moves(self, board):
        i=self.row
        j=self.column
        moves=[]
        #valid moves for white
        if self.color=="w":
            #Direction 1 (top left)
            for d in range(7):
                try:
                    if isinstance(board[i + d + 1][j - d -1], Piece):
                        if board[i + d + 1][j - d -1].color == 'b':
                            moves.append((j - d - 1, i + d +1))
                        break
                    else:
                        moves.append((j - d - 1, i + d + 1))                  

                except IndexError:
                    break
            #Direction 2 (top right)
            for d in range(7):
                try:
                    if isinstance(board[i + d + 1][j + d + 1], Piece):
                        if board[i + d + 1][j + d + 1].color == 'b':
                            moves.append((j + d + 1, i + d +1))
                        break
                    else:
                        moves.append((j + d + 1, i + d + 1))
                except IndexError:
                    break
            #Direction 3 (bottom right)
            for d in range(7):
                try:
                    if isinstance(board[i - d - 1][j + d + 1], Piece):
                        if board[i - d - 1][j + d + 1].color == 'b':
                            moves.append((j + d + 1, i - d - 1))
                        break
                    else:
                        moves.append((j + d + 1, i - d - 1))
                except IndexError:
                    break
            #Direction 4 (bottom left)
            for d in range(7):
                try:
                    if isinstance(board[i - d - 1][j - d -1], Piece):
                        if board[i - d - 1][j - d -1].color == 'b':
                            moves.append((j - d - 1, i - d - 1))
                        break
                    else:
                        moves.append((j - d - 1, i - d - 1))
                except IndexError:
                    break
        #valid moves for black   
        else:
            pass
        return moves
    def toString(self):
        return 'B'
class Queen(Piece):
    img=2
    def valid_moves(self, board):
        i=self.row
        j=self.column
        moves=[]
        if self.color == "w":
            #Direction 1
            for d in range(7):
                try:
                    if isinstance(board[i + d + 1][j], Piece):
                        if board[i + d + 1][j].color == 'b':
                            moves.append((j, i + d +1))
                        break
                    else:
                        moves.append((j, i + d + 1))
                except IndexError:
                    break
            #Direction 2
            for d in range(7):
                try:
                    if isinstance(board[i - d - 1][j], Piece):
                        if board[i - d - 1][j].color == 'b':
                            moves.append((j, i - d - 1))
                        break
                    else:
                        moves.append((j, i - d - 1))
                except IndexError:
                    break
            #Direction 3
            for d in range(7):
                try:
                    if isinstance(board[i][j - d -1], Piece):
                        if board[i][j - d -1].color == 'b':
                            moves.append((j - d - 1, i))
                        break
                    else:
                        moves.append((j - d - 1, i))
                except IndexError:
                    break
            #Direction 4
            for d in range(7):
                try:
                    if isinstance(board[i][j + d + 1], Piece):
                        if board[i][j + d + 1].color == 'b':
                            moves.append((j + d + 1, i))
                        break
                    else:
                        moves.append((j + d + 1, i))
                except IndexError:
                    break

            #Direction 5 (top left)
            for d in range(7):
                try:
                    if isinstance(board[i + d + 1][j - d -1], Piece):
                        if board[i + d + 1][j - d -1].color == 'b':
                            moves.append((j - d - 1, i + d +1))
                        break
                    else:
                        moves.append((j - d - 1, i + d + 1))                  

                except IndexError:
                    break
            #Direction 6 (top right)
            for d in range(7):
                try:
                    if isinstance(board[i + d + 1][j + d + 1], Piece):
                        if board[i + d + 1][j + d + 1].color == 'b':
                            moves.append((j + d + 1, i + d +1))
                        break
                    else:
                        moves.append((j + d + 1, i + d + 1))
                except IndexError:
                    break
            #Direction 7 (bottom right)
            for d in range(7):
                try:
                    if isinstance(board[i - d - 1][j + d + 1], Piece):
                        if board[i - d - 1][j + d + 1].color == 'b':
                            moves.append((j + d + 1, i - d - 1))
                        break
                    else:
                        moves.append((j + d + 1, i - d - 1))
                except IndexError:
                    break
            #Direction 8 (bottom left)
            for d in range(7):
                try:
                    if isinstance(board[i - d - 1][j - d -1], Piece):
                        if board[i - d - 1][j - d -1].color == 'b':
                            moves.append((j - d - 1, i - d - 1))
                        break
                    else:
                        moves.append((j - d - 1, i - d - 1))
                except IndexError:
                    break
        #valid moves for black
        else:
            pass

        return moves
    def toString(self):
        return 'Q'
class King(Piece):
    img=3
    def valid_moves(self, board):
        i=self.row
        j=self.column
        moves=[]

        if self.color == 'w':
            try:
                if board[i][j - 1] == 0 or board[i][j - 1].color == 'b':
                    moves.append((j - 1, i))
            except IndexError:
                pass
            try:
                if board[i + 1][j - 1] == 0 or board[i + 1][j - 1].color == 'b':
                    moves.append((j - 1, i + 1))
            except IndexError:
                pass
            try:
                if board[i + 1][j] == 0 or board[i + 1][j].color == 'b':
                    moves.append((j, i + 1))
            except IndexError:
                pass
            try:
                if board[i + 1][j + 1] == 0 or board[i + 1][j + 1].color == 'b':
                    moves.append((j + 1, i + 1))
            except IndexError:
                pass
            try:
                if board[i][j + 1] == 0 or board[i][j + 1].color == 'b':
                    moves.append((j + 1, i))
            except IndexError:
                pass
            try:
                if board[i - 1][j + 1] == 0 or board[i - 1][j + 1].color == 'b':
                    moves.append((j + 1, i - 1))
            except IndexError:
                pass
            try:
                if board[i - 1][j] == 0 or board[i - 1][j].color == 'b':
                    moves.append((j, i - 1))
            except IndexError:
                pass
            try:
                if board[i - 1][j - 1] == 0 or board[i - 1][j - 1].color == 'b':
                    moves.append((j - 1, i - 1))
            except IndexError:
                pass
        else:
            pass
        return moves
    def toString(self):
        return 'K'
class Rook(Piece):
    img=4
    def valid_moves(self, board):
        i=self.row
        j=self.column
        moves=[]

        if self.color == "w":
            #Direction 1
            for d in range(7):
                try:
                    if isinstance(board[i + d + 1][j], Piece):
                        if board[i + d + 1][j].color == 'b':
                            moves.append((j, i + d +1))
                        break
                    else:
                        moves.append((j, i + d + 1))
                except IndexError:
                    break
            #Direction 2
            for d in range(7):
                try:
                    if isinstance(board[i - d - 1][j], Piece):
                        if board[i - d - 1][j].color == 'b':
                            moves.append((j, i - d - 1))
                        break
                    else:
                        moves.append((j, i - d - 1))
                except IndexError:
                    break
            #Direction 3
            for d in range(7):
                try:
                    if isinstance(board[i][j - d -1], Piece):
                        if board[i][j - d -1].color == 'b':
                            moves.append((j - d - 1, i))
                        break
                    else:
                        moves.append((j - d - 1, i))
                except IndexError:
                    break
            #Direction 4
            for d in range(7):
                try:
                    if isinstance(board[i][j + d + 1], Piece):
                        if board[i][j + d + 1].color == 'b':
                            moves.append((j + d + 1, i))
                        break
                    else:
                        moves.append((j + d + 1, i))
                except IndexError:
                    break
        #valid moves for black
        else:
            pass

        return moves
    def toString(self):
        return 'R'
class Knight(Piece):
    img=5
    def valid_moves(self, board):
        i=self.row
        j=self.column
        moves=[]
        #Valid moves for Knight
        if self.color == 'w':
            try:
                if board[i + 1][j - 2] == 0 or board[i + 1][j - 2].color == 'b':
                    moves.append((j - 2, i + 1))
            except IndexError:
                pass
            try:
                if board[i + 2][j - 1] == 0 or board[i + 2][j - 1].color == 'b':
                    moves.append((j - 1, i + 2))
            except IndexError:
                pass
            try:
                if board[i + 2][j + 1] == 0 or board[i + 2][j + 1].color == 'b':
                    moves.append((j + 1, i + 2))
            except IndexError:
                pass
            try:
                if board[i + 1][j + 2] == 0 or board[i + 1][j + 2].color == 'b':
                    moves.append((j + 2, i + 1))
            except IndexError:
                pass
            try:
                if board[i - 1][j + 2] == 0 or board[i - 1][j + 2].color == 'b':
                    moves.append((j + 2, i - 1))
            except IndexError:
                pass
            try:
                if board[i - 2][j + 1] == 0 or board[i - 2][j + 1].color == 'b':
                    moves.append((j + 1, i - 2))
            except IndexError:
                pass
            try:
                if board[i - 2][j - 1] == 0 or board[i - 2][j - 1].color == 'b':
                    moves.append((j - 1, i - 2))
            except IndexError:
                pass
            try:
                if board[i - 1][j - 2] == 0 or board[i - 1][j - 2].color == 'b':
                    moves.append((j - 2, i - 1))
            except IndexError:
                pass
        else:
            pass

        return moves
    def toString(self):
        return 'k'



