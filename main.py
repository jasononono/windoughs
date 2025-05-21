import pygame as p
from taskbar import Taskbar

class Event:
    def __init__(self):
        self.event = ()
        self.key = ()
        self.mouse = ()
        self.mouse_pos = ()
        self.update()

    def update(self):
        self.event = p.event.get()
        self.key = p.key.get_pressed()
        self.mouse = p.mouse.get_pressed
        self.mouse_pos = p.mouse.get_pos()

    def detect(self, event):
        for e in self.event:
            if e.type == event:
                return True
        return False

    def keydown(self, key):
        return self.key[key]


class Screen:
    def __init__(self, background = "background.png"):
        p.init()
        p.display.set_caption("Windoes 12 Version 0.1")

        size = p.display.get_desktop_sizes()[0]
        self.surface = p.display.set_mode(size, p.RESIZABLE)
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.abs = self.rect.x, self.rect.y

        self.event = Event()
        self.execute = True

        self.background_image = p.image.load(background)
        self.background = None
        self.background_rect = None
        self.get_background()

        self.taskbar = Taskbar()

    def get_background(self):
        size = self.background_image.get_size()
        if size[0] / self.rect.width > size[1] / self.rect.height:
            size = size[0] / size[1] * self.rect.height, self.rect.height
        else:
            size = self.rect.width, size[1] / size[0] * self.rect.width
        self.background = p.transform.smoothscale(self.background_image, size)
        self.background_rect = self.background.get_rect()
        self.background_rect.center = self.rect.center

    def update(self):
        self.event.update()
        if self.event.detect(p.QUIT):
            self.execute = False

        self.rect = self.surface.get_rect()
        self.get_background()

        self.surface.blit(self.background, self.background_rect)

        self.taskbar.update(self, self.event)

        p.display.flip()


screen = Screen()

while screen.execute:
    screen.update()
p.quit()