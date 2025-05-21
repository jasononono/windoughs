import pygame as p

class Font:
    def __init__(self, size, bold = False, italic = False, name = None):
        self.name = name
        self.size = size
        if name is None:
            modifier = ("z" if italic else "b") if bold else ("i" if italic else "")
            self.template = p.font.Font(f"defaultFont/segoeui{modifier}.ttf", size)
        else:
            self.template = p.font.Font(name, size)
            self.template.set_bold(bold)
            self.template.set_italic(italic)

    def get_size(self, text):
        return self.template.size(text)

    def render(self, surface, text = '', position = (0, 0), colour = (0, 0, 0), background = None):
        surface.blit(self.template.render(text, True, colour, background), position)