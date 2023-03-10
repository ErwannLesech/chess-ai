class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece is not None

    def has_rival(self, color):
        return self.has_piece() and color != self.piece.color

    def has_mate(self, color):
        return self.has_piece() and color == self.piece.color
    def is_empty_or_rival(self, color):
        return (not self.has_piece()) or (self.has_piece() and color != self.piece.color)

    @staticmethod
    def is_inside(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    @staticmethod
    def get_alphacol(col):
        ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return ALPHACOLS[col]
