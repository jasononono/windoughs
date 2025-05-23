import pygame as p

class Font:
    def __init__(self, name, size, bold = False, italic = False):
        self.name = name
        self.size = size
        self.template = p.font.Font(name, size)
        self.template.set_bold(bold)
        self.template.set_italic(italic)

    def get_size(self, text):
        return self.template.size(text)

    def render(self, surface, text = '', position = (0, 0), colour = (0, 0, 0), background = None):
        surface.blit(self.template.render(text, True, colour, background), position)


class SysFont(Font):
    def __init__(self, size, bold = False, italic = False):
        modifier = ("z" if italic else "b") if bold else ("i" if italic else "")
        super().__init__(f"defaultFont/segoeui{modifier}.ttf", size, bold, italic)