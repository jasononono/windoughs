import pygame as p

from systemFiles.assets.base import time, date
from systemFiles.assets.font import SysFont
from systemFiles.assets.button import ImageButton


class Taskbar:
    def __init__(self, height = 50, colour = (228, 239, 250), font_size = 13):
        self.height = height
        self.colour = colour

        self.surface = p.Surface((1, 1))
        self.rect = self.surface.get_rect()
        self.abs = 0, 0

        self.font = SysFont(font_size)
        self.applications = {}

    def add_app(self, name):
        self.applications[ImageButton(image = name.icon)] = name

    def valid_mouse_position(self, position):
        if (self.abs[0] < position[0] < self.abs[0] + self.rect.width and
            self.abs[1] < position[1] < self.abs[1] + self.rect.height):
            return True
        return False

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

        action = None
        amount = len(self.applications.items())
        for i, j in enumerate(self.applications.keys()):
            j.rect.center = self.rect.width / 2 - (amount - 1) * 30 + i * 50, self.rect.height / 2
            enabled = parent.is_application(self.applications[j])
            if j.update(self, event, True if enabled else None):
                action = self.applications[j]
            if enabled:
                if self.applications[j] is parent.topmost_launcher() and parent.active:
                    p.draw.line(self.surface, (95, 141, 214),
                                (j.rect.centerx - 7, j.rect.bottom - 5),
                                (j.rect.centerx + 7, j.rect.bottom - 5), 3)
                else:
                    p.draw.line(self.surface, (112, 121, 146),
                                (j.rect.centerx - 3, j.rect.bottom - 5),
                                (j.rect.centerx + 3, j.rect.bottom - 5), 3)

        parent.surface.blit(self.surface, self.rect)
        return action