#modules
import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

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
            game.draw_last_move(self.screen)
            game.draw_possible_moves(self.screen)
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
                        if piece.color == game.next_player:
                            board.possible_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            game.draw_grid(screen)
                            game.draw_last_move(screen)
                            game.draw_possible_moves(screen)
                            game.draw_pieces(screen)

                elif event.type == pygame.MOUSEMOTION:
                    game.set_over(event.pos[1] // CELL_WIDTH, event.pos[0] // CELL_WIDTH)
                    game.draw_over(screen)
                    if dragger.piece:
                        dragger.update_mouse(event.pos)

                        game.draw_possible_moves(screen)
                        # game.draw_pieces(screen)
                        game.draw_over(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.piece:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // CELL_WIDTH
                        released_col = dragger.mouseX // CELL_HEIGHT
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)
                            game.play_sound(captured)
                            game.draw_grid(screen)
                            game.draw_last_move(screen)
                            game.draw_pieces(screen)
                            game.next_turn()
                    dragger.undrag_piece()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        game.change_theme()
                    if event.key == pygame.K_r:
                        game.reset() 
                        game = self.game
                        dragger = self.game.dragger
                        board = self.game.board
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #update the dislay
            pygame.display.update()

main = Main()
main.mainloop()