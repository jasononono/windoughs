import pygame as p
from systemFiles.assets import base

class Cursor:
    def __init__(self, position = None, colour = base.WHITE):
        self.position = position
        self.blinkRate = 30
        self.blink = 0
        self.colour = colour

    def update(self, surface, font, coord, offset, spacing):
        self.tick()
        if self.blink < self.blinkRate:
            p.draw.rect(surface, self.colour, (offset[0] + coord[0] * font.size * spacing[0],
                                               offset[1] + coord[1] * font.size * spacing[1], 1, font.size))

    def oneline_update(self, surface, font, text, offset):
        self.tick()
        if self.blink < self.blinkRate:
            size = font.get_size(text)
            p.draw.rect(surface, self.colour, (offset[0] + size[0], offset[1], 1, font.size))

    def tick(self):
        self.blink = (self.blink + 1) % (self.blinkRate * 2)
