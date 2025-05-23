import pygame as p

from systemFiles.taskbar import Taskbar
from systemFiles.window import Window
from systemFiles.start import Start

from applications.commandPrompt import CommandPrompt
from applications.defaultApplication import DefaultApplication


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
        self.mouse = p.mouse.get_pressed()
        self.mouse_pos = p.mouse.get_pos()

    def detect(self, event):
        for e in self.event:
            if e.type == event:
                return True
        return False

    def keydown(self, key):
        return self.key[key]

    def mouse_down(self):
        return self.detect(p.MOUSEBUTTONDOWN)


class Screen:
    def __init__(self, background = "default.png"):
        p.init()
        p.display.set_caption("Windoughs 12 Version 0.3")

        size = p.display.get_desktop_sizes()[0]
        self.surface = p.display.set_mode(size, p.RESIZABLE)
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.abs = self.rect.x, self.rect.y

        self.event = Event()
        self.execute = True

        self.taskbar = Taskbar()
        self.taskbar.add_app(Start)
        self.taskbar.add_app(CommandPrompt)
        self.taskbar.add_app(DefaultApplication)

        self.dragged = None
        self.active = False
        self.windows = []
        self.applications = []

        self.background_image = p.image.load("systemFiles/backgrounds/" + background)
        self.background = None
        self.background_rect = None
        self.bound = None
        self.get_rect()

    def get_rect(self):
        self.rect = self.surface.get_rect()
        self.bound = self.rect.copy()
        self.bound.height -= self.taskbar.height

        size = self.background_image.get_size()
        if size[0] / self.rect.width > size[1] / self.rect.height:
            size = size[0] / size[1] * self.rect.height, self.rect.height
        else:
            size = self.rect.width, size[1] / size[0] * self.rect.width
        self.background = p.transform.smoothscale(self.background_image, size)
        self.background_rect = self.background.get_rect()
        self.background_rect.center = self.rect.center

    def activate(self, item):
        self.windows.append(self.windows.pop(item))
        self.applications.append(self.applications.pop(item))

    def new_window(self, application):
        app = application()
        self.applications.append(application)
        self.windows.append(Window(app, (self.rect.centerx - app.size[0] / 2, self.rect.centery - app.size[1] / 2)))

    def update(self):
        self.event.update()
        if self.event.detect(p.QUIT):
            self.execute = False

        self.get_rect()
        self.surface.blit(self.background, self.background_rect)

        action = self.taskbar.update(self, self.event)
        if action is Start:
            print("start")
        elif action is not None:
            self.active = True
            if action in self.applications:
                self.activate(self.applications.index(action))
            else:
                self.new_window(action)

        if self.dragged is not None:
            self.dragged.follow_cursor(self.event.mouse_pos)
        activation_queue = []

        for i in range(len(self.windows)):
            if self.windows[i].update(self, self.event) and self.windows[-1] is self.windows[i]:
                del(self.windows[i])
                del(self.applications[i])
                break
            if self.windows[i].get_dragged(self, self.event):
                self.dragged = self.windows[i]
            elif self.dragged is self.windows[i]:
                self.dragged = None
            if self.event.mouse_down() and self.windows[i].valid_window_position(self.event.mouse_pos):
                activation_queue.append(i)

        if self.event.mouse_down():
            if len(activation_queue) == 0:
                self.active = False
            else:
                self.active = True
                self.activate(activation_queue[-1])

        p.display.flip()