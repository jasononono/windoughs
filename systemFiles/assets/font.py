import pygame as p
from systemFiles.assets import base


class Font:
    def __init__(self, name, size, bold = False, italic = False, colour = base.BLACK):
        self.name = name
        self.size = size
        self.template = p.font.Font(name, size)
        self.template.set_bold(bold)
        self.template.set_italic(italic)
        self.colour = colour

    def get_size(self, text):
        return self.template.size(text)

    def render(self, surface, text = '', position = (0, 0), colour = None, background = None):
        surface.blit(self.template.render(text, True, self.colour if colour is None else colour,
                                          background), position)


class SysFont(Font):
    def __init__(self, size, bold = False, italic = False, colour = base.BLACK):
        modifier = ("z" if italic else "b") if bold else ("i" if italic else "")
        super().__init__(f"systemFiles/systemFont/segoeui{modifier}.ttf", size, bold, italic, colour)