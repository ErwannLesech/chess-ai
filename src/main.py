#modules
import pygame
import sys

from const import *
from game import Game
from dragger import Dragger

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess game')
        self.game = Game()

    def mainloop(self):
        screen = self.screen
        game = self.game
        dragger = self.game.dragger
        board = self.game.board
        while True:
            game.draw_grid(self.screen)
            game.draw_possible_moves(screen)
            game.draw_pieces(self.screen)
            if dragger.piece:
                dragger.update_blit(screen)
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // CELL_WIDTH
                    clicked_col = dragger.mouseX // CELL_HEIGHT

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        board.possible_moves(piece, clicked_row, clicked_col)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)
                        game.draw_grid(screen)
                        game.draw_possible_moves(screen)
                        game.draw_pieces(screen)

                elif event.type == pygame.MOUSEMOTION:
                    if dragger.piece:
                        dragger.update_mouse(event.pos)
                        game.draw_possible_moves(screen)
                        dragger.update_blit(screen)
                        # game.draw_pieces(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #update the dislay
            pygame.display.update()

main = Main()
main.mainloop()