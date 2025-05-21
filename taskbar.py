import pygame as p
from base import time, date
from font import Font
from button import ImageButton

class Taskbar:
    def __init__(self, height = 50, colour = (228, 239, 250), font_size = 13):
        self.height = height
        self.colour = colour

        self.surface = p.Surface((1, 1))
        self.rect = self.surface.get_rect()
        self.abs = None

        self.font = Font(font_size)
        self.applications = {}
        self.add_app("home", "home_icon.png")
        self.add_app("command_prompt", "command_icon.png")

    def add_app(self, name, icon):
        self.applications[ImageButton((0, 0), icon)] = name

    def get_rect(self, parent):
        self.surface = p.transform.scale(self.surface, (parent.rect.width, self.height))
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = 0, parent.rect.bottom - self.height
        self.abs = parent.abs[0] + self.rect.x, parent.abs[1] + self.rect.y

    def update(self, parent, event):
        self.get_rect(parent)
        self.surface.fill(self.colour)

        self.font.render(self.surface, time(),
                         (self.rect.right - self.font.get_size(time())[0] - 20, 6))
        date_size = self.font.get_size(date())
        self.font.render(self.surface, date(),
                         (self.rect.right - date_size[0] - 20, self.height - date_size[1] - 7))

        amount = len(self.applications.items())
        for i, j in enumerate(self.applications.keys()):
            j.rect.center = self.rect.width / 2 - (amount - 1) * 30 + i * 50, self.rect.height / 2
            if j.update(self, event):
                print(self.applications[j])

        parent.surface.blit(self.surface, self.rect)