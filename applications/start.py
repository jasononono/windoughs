import pygame as p
import data
from systemFiles.assets import base

from applications.application import Application
from systemFiles.assets.font import SysFont

class Start(Application):
    icon = "start_icon.png"

    def __init__(self, parent):
        super().__init__(parent)

        self.window = parent.new_window(self, (630, 260), "About This Totally Legit Operating System",
                                        self.icon, (10, 10))
        self.titleFont = SysFont(70, colour = base.BLUE1)
        self.titleFontBold = SysFont(70, True, colour = base.BLUE1)
        self.font = SysFont(20, colour = base.BLUE2)
        self.fontBold = SysFont(25, True, colour = base.BLUE2)
        self.image = p.image.load("systemFiles/icons/start_icon.png")
        self.image = p.transform.scale(self.image, (80, 80))

    def update(self, parent, event):
        self.window.surface.fill(base.GREY1)

        self.window.surface.blit(self.image, (30, 30))
        self.titleFont.render(self.window.surface, "Windoughs", (140, 20))
        self.titleFontBold.render(self.window.surface, "12", (510, 20))
        p.draw.line(self.window.surface, base.BLUE1, (30, 140), (600, 140), 5)

        self.font.render(self.window.surface, "Now redesigned in", (40, 160))
        self.fontBold.render(self.window.surface, "Pygame", (210, 155))
        self.font.render(self.window.surface, "Version", (140, 200))
        self.fontBold.render(self.window.surface, data.VERSION, (210, 195))

        return super().update(parent, event)