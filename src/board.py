from const import *
from square import Square
from piece import *
class Board:
    def __init__(self):
        self.squares = [[0 for _ in range(8)] for col in range(COLS)]
        self.create()
        self.add_pieces("black")
        self.add_pieces("white")

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