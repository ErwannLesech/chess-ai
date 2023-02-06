import pygame
import os
from sound import Sound
from theme import Theme

class Config:
    def __init__(self):
        self.themes = []
        self.add_theme()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.move_sound = Sound(os.path.join("assets/sounds/move.wav"))
        self.capture_sound = Sound(os.path.join("assets/sounds/capture.wav"))

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def add_theme(self):
        green = Theme((69, 139, 0), (255, 239, 219), (244, 247, 116), (172, 195, 51), '#CB6464', '#CB4646')
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#C86464', '#C84646')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), '#C86464', '#C84646')
        gray = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128), '#C86464', '#C84646')

        self.themes = [green, brown, blue, gray]