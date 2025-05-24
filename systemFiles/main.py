import pygame as p

from systemFiles.taskbar import Taskbar
from systemFiles.window import Window
from applications.start import Start

from applications.commandPrompt import CommandPrompt
from applications.application import Application


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
        p.display.set_caption("Windoughs 12 Version 0.4")

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
        self.taskbar.add_app(Application)

        self.dragged = None
        self.active = False
        self.windows = []
        self.applications = []
        self.requestedUpdates = []

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

    def activate(self, window):
        del self.windows[self.windows.index(window)]
        self.windows.append(window)

    def destroy(self, window):
        del self.windows[self.windows.index(window)]

    def activate_application(self, launcher):
        for i in self.windows:
            if isinstance(i.application, launcher):
                self.activate(i)

    def open_application(self, launcher):
        self.applications.append(launcher(self))

    def quit_application(self, application):
        self.applications.remove(application)
        for i, w in enumerate(self.windows):
            if w.application is application:
                del(self.windows[i])

    def new_window(self, application, size = (400, 300), title = "Window", icon = None):
        self.windows.append(Window(application, (self.rect.centerx - size[0] / 2, self.rect.centery - size[1] / 2),
                                   size, title, icon = icon))

    def is_application(self, launcher):
        for i in self.applications:
            if type(i) is launcher:
                return True
        return False

    def topmost_launcher(self):
        if len(self.windows) == 0:
            return None
        return type(self.windows[-1].application)

    def topmost_window(self, window = None):
        if window is None:
            return self.windows[-1]
        return True if self.windows[-1] is window else False

    def get_windows(self, application = None):
        if application is None:
            return self.windows
        return [i for i in self.windows if i.application is application]

    def update(self):
        self.event.update()
        if self.event.detect(p.QUIT):
            self.execute = False

        self.get_rect()
        self.surface.blit(self.background, self.background_rect)

        # TASKBAR
        action = self.taskbar.update(self, self.event)
        if action is Start:
            print("start")
        elif action is not None:
            self.active = True
            if self.is_application(action):
                self.activate_application(action)
            else:
                self.open_application(action)

        # DRAGGING
        if self.dragged is not None:
            self.dragged.follow_cursor(self.event.mouse_pos)

        # APPLICATIONS
        self.requestedUpdates = []
        for i in self.applications:
            i.update(self, self.event)

        # WINDOWS
        activation_queue = []
        for i, w in enumerate(self.windows):
            if w in self.requestedUpdates and w.update(self, self.event):
                self.destroy(w)
                break
            if w.get_dragged(self, self.event):
                self.dragged = w
            elif self.dragged is w:
                self.dragged = None
            if self.event.mouse_down() and w.valid_window_position(self.event.mouse_pos):
                activation_queue.append(w)

        if self.event.mouse_down() and not self.taskbar.valid_mouse_position(self.event.mouse_pos):
            if len(activation_queue) == 0:
                self.active = False
            else:
                self.active = True
                self.activate(activation_queue[-1])

        p.display.flip()