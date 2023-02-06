#modules
import pygame
import sys

from const import *
from game import Game

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess game')
        self.game = Game()

    def mainloop(self):
        while True:
            self.game.draw_grid(self.screen)
            self.game.draw_pieces(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #update the dislay
            pygame.display.update()

main = Main()
main.mainloop()