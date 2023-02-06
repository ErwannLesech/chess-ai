import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

class Game:
    def __init__(self):
        self.next_player = "white"
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
    # Show methods
    def draw_grid(self, surface):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark  #green
                grid = (col * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                pygame.draw.rect(surface, color, grid)
                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(str(ROWS - row), 1, color)
                    lbl_pos = (5, 5 + row * CELL_HEIGHT)
                    surface.blit(lbl, lbl_pos)
                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * CELL_WIDTH + CELL_HEIGHT - 20, HEIGHT - 20)
                    surface.blit(lbl, lbl_pos)

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
        theme = self.config.theme
        if self.dragger.piece:
            piece = self.dragger.piece
            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                rect = (move.final.col * CELL_WIDTH, move.final.row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                pygame.draw.rect(surface, color, rect)

    def draw_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * CELL_WIDTH, pos.row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                pygame.draw.rect(surface, color, rect)

    def draw_over(self, surface):
        if self.hovered_sqr:
            color = (180,180,180)
            rect = (self.hovered_sqr.col * CELL_WIDTH, self.hovered_sqr.row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
            pygame.draw.rect(surface, color, rect, width=3)

    def set_over(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()