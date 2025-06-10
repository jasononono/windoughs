import pygame as p
from systemFiles.assets import base


class Font:
    def __init__(self, size, name = "segoeui", bold = False, italic = False, colour = base.BLACK):
        self.modifier = ("both" if italic else "bold") if bold else ("italic" if italic else "default")
        self.name = name
        self.size = size
        self.template = p.font.Font(f"systemFiles/systemFont/{name}/{self.modifier}.ttf", size)
        self.colour = colour

    def get_size(self, text):
        return self.template.size(text)

    def render(self, surface, text = '', position = (0, 0), colour = None, background = None):
        surface.blit(self.template.render(text, True, self.colour if colour is None else colour,
                                          background), position)
