import pygame as p

from applications.application import Application
from systemFiles.assets.textEngine.text import TextEditor

class CommandPrompt(Application):
    icon = "command_icon.png"

    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent.new_window(self, (800, 600), "Command Prompt", "command_icon.png")
        self.editor = TextEditor("", size = (800, 600), font_size = 15)

    def update(self, parent, event):
        self.editor.update(self.window, event, parent.topmost_window(self.window))

        return super().update(parent, event)