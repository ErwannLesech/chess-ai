import pygame
from const import *
from board import Board
from dragger import Dragger

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
    # Show methods
    def draw_grid(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if not (row + col) % 2:
                    color = (69, 139, 0)  #green
                else:
                    color = (255, 239, 219)  #white
                grid = (col * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                pygame.draw.rect(surface, color, grid)

    def draw_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * CELL_WIDTH + CELL_HEIGHT // 2, row * CELL_HEIGHT + CELL_WIDTH // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def draw_possible_moves(self, surface):
        if self.dragger.piece:
            piece = self.dragger.piece
            for move in piece.moves:
                color = '#CB6464' if (move.final.row + move.final.col) % 2 == 0 else '#CB4646'
                rect = (move.final.col * CELL_WIDTH, move.final.row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                pygame.draw.rect(surface, color, rect)