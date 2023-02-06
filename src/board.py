from const import *
from square import Square
from piece import *
from move import Move
class Board:
    def __init__(self):
        self.squares = [[0 for _ in range(8)] for col in range(COLS)]
        self.create()
        self.add_pieces("black")
        self.add_pieces("white")

    def possible_moves(self, piece, row, col):

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
                        final = Square(possible_row, possible_col)
                        move = Move(initial, final)
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
                        final = Square(possible_row, possible_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_row = row + row_incr
                possible_col = col + col_incr
                while True:
                    if Square.is_inside(possible_row, possible_col):
                        initial = Square(row, col)
                        final = Square(possible_row, possible_col)
                        move = Move(initial, final)
                        if not self.squares[possible_row][possible_col].has_piece():
                            piece.add_move(move)
                        if self.squares[possible_row][possible_col].has_rival(piece.color):
                            piece.add_move(move)
                            break
                        if self.squares[possible_row][possible_col].has_mate(piece.color):
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