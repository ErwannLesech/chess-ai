import copy

from const import *
from square import Square
from piece import *
from move import Move
class Board:
    def __init__(self):
        self.squares = [[0 for _ in range(8)] for col in range(COLS)]
        self.last_move = None
        self.create()
        self.add_pieces("black")
        self.add_pieces("white")

    def move(self, piece, move):
        initial = move.initial
        final = move.final
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if piece.name == "pawn":
            self.check_promotion(piece, final)

        if piece.name == "king":
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        piece.moved = True
        piece.clear_moves()
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.possible_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False

    def possible_moves(self, piece, row, col, bool=True):

        def pawn_moves():
            steps = 1 if piece.moved else 2
            start = row + piece.direction
            end = row + (piece.direction * (1 + steps))
            for possible_row in range(start, end, piece.direction):
                if Square.is_inside(possible_row):
                    if not self.squares[possible_row][col].has_piece():
                        initial = Square(row, col)
                        final = Square(possible_row, col)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    else:
                        break
                else:
                    break
            possible_row = row + piece.direction
            possible_cols = [col-1, col+1]
            for possible_col in possible_cols:
                if Square.is_inside(possible_row, possible_col):
                    if self.squares[possible_row][possible_col].has_rival(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_row][possible_col].piece
                        final = Square(possible_row, possible_col, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

        def knight_moves():
            possibles = [
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row - 1, col + 2),
                (row - 1, col - 2),
                (row + 1, col + 2),
                (row + 1, col - 2),
            ]

            for possible in possibles:
                possible_row, possible_col = possible
                if Square.is_inside(possible_row, possible_col):
                    if self.squares[possible_row][possible_col].is_empty_or_rival(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_row][possible_col].piece
                        final = Square(possible_row, possible_col, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:break
                        else:
                            piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_row = row + row_incr
                possible_col = col + col_incr
                while True:
                    if Square.is_inside(possible_row, possible_col):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_row][possible_col].piece
                        final = Square(possible_row, possible_col, final_piece)
                        move = Move(initial, final)
                        if not self.squares[possible_row][possible_col].has_piece():
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                        elif self.squares[possible_row][possible_col].has_rival(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break
                        elif self.squares[possible_row][possible_col].has_mate(piece.color):
                            break
                    else:
                        break
                    possible_row = possible_row + row_incr
                    possible_col = possible_col + col_incr

        def king_moves():
            adjs = [
                (row - 1, col),
                (row - 1, col + 1),
                (row - 1, col - 1),
                (row + 1, col - 1),
                (row + 1, col + 1),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
            ]

            for adj in adjs:
                possible_row = adj[0]
                possible_col = adj[1]

                if Square.is_inside(possible_row, possible_col):
                    if self.squares[possible_row][possible_col].is_empty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_row, possible_col)
                        move = Move(initial, final)
                        piece.add_move(move)

            if not piece.moved:
                left_rook = self.squares[row][0].piece
                if left_rook.name == "rook":
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                piece.left_rook = left_rook
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)
                                left_rook.add_move(move)
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        left_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)

                right_rook = self.squares[row][7].piece
                if right_rook.name == "rook":
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                piece.right_rook = right_rook
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)
                                right_rook.add_move(move)
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        right_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK)


        match piece.name:
            case "pawn":
                pawn_moves()
            case "knight":
                knight_moves()
            case "bishop":
                straightline_moves([(-1, 1), (-1, -1), (1, 1), (1, -1)])
            case "rook":
                straightline_moves([(-1, 0), (0, 1), (0, -1), (1, 0)])
            case "queen":
                straightline_moves([(-1, 1), (-1, -1), (1, 1), (1, -1),
                                    (-1, 0), (0, 1), (0, -1), (1, 0)])
            case "king":
                king_moves()

    def create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        self.squares[row_other][0] = Square(row_pawn, 0, Rook(color))
        self.squares[row_other][1] = Square(row_pawn, 1, Knight(color))
        self.squares[row_other][2] = Square(row_pawn, 2, Bishop(color))
        self.squares[row_other][3] = Square(row_pawn, 3, Queen(color))
        self.squares[row_other][4] = Square(row_pawn, 4, King(color))
        self.squares[row_other][5] = Square(row_pawn, 5, Bishop(color))
        self.squares[row_other][6] = Square(row_pawn, 6, Knight(color))
        self.squares[row_other][7] = Square(row_pawn, 7, Rook(color))

board = Board()
board.create()