import pygame as p
import os

from applications.application import Application

from systemFiles.assets.font import Font
from systemFiles.assets import base
from systemFiles.assets.button import ButtonTemplate, TextButton
from systemFiles.assets.icon import ImageIcon

class FileExplorer(Application):
    icon = "fileExplorer_icon.png"

    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent.new_window(self, (600, 400), "File Explorer", self.icon, resizable = False)
        self.image_windows = {}

        self.font = Font(15)
        self.title = Font(20)
        self.path = []
        self.pathName = ""
        self.undo = TextButton((10, 10), "<", (40, 40), base.WHITE, base.GREY1,
                               font = "lucon", font_size = 30)
        self.buttons = []
        self.selected = -1
        self.items = []

        self.icons = {dir: ImageIcon("folder_icon.png", (20, 20)),
                      None: ImageIcon("default.png", (20, 20))}

    def update(self, parent, event):
        self.window.surface.fill(base.WHITE)

        self.sync_items(parent, event)
        if len(self.path) > 0 and self.undo.update(self.window, event):
            self.path.pop()
        p.draw.rect(self.window.surface, base.GREY3, (60, 10, 520, 40), 2)
        self.title.render(self.window.surface, self.pathName, (70, 15))

        for i, j in self.image_windows.items():
            j.surface.blit(i, (0, 0))

        return super().update(parent, event)

    def sync_items(self, parent, event):
        self.pathName = "files/" + '/'.join(self.path)
        self.items = sorted([i for i in os.listdir(self.pathName) if i[0] != '.'])
        length = len(self.buttons)
        if len(self.items) >= length:
            for i in range(len(self.items) - length):
                self.buttons.append(ButtonTemplate((40, 60 + length * 30), (550, 30),
                                                   base.WHITE, base.GREY1))
                length += 1
        else:
            for i in range(length - len(self.items)):
                self.buttons.pop()

        mouse_down = False
        for j, (i, b) in enumerate(zip(self.items, self.buttons)):
            b.text = i
            extension = self.extension(i)

            if b.update(self.window, event, self.selected == j):
                mouse_down = True
                if self.selected == j:
                    self.open(parent, i, extension)
                else:
                    self.selected = j

            self.icons[self.extension(i) if extension in self.icons.keys() else None].display(self.window.surface,
                                                                                              (20, b.rect.top + 15))
            self.font.render(self.window.surface, i, [j + 5 for j in b.rect.topleft])
        if not mouse_down and event.detect(p.MOUSEBUTTONUP):
            self.selected = -1

    def extension(self, file):
        if file.find('.') == -1:
            return dir
        return file.split('.')[-1]

    def open(self, parent, file, extension):
        if extension is dir:
            self.path.append(file)
            self.selected = -1
        elif extension in ("png", "jpg", "jpeg"):
            image = p.image.load(self.pathName + '/' + file)
            image = p.transform.smoothscale_by(image, 0.25)
            self.image_windows[image] = parent.new_window(self, [max(i, j) for i, j in
                                                                 zip(image.get_size(), (400, 300))],
                                                          file, "default.png", resizable = False)