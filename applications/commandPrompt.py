import pygame as p

from applications.application import Application
from systemFiles.assets.textEngine.text import TextEditor

class CommandPrompt(Application):
    icon = "command_icon.png"

    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent.new_window(self, (800, 600), "Command Prompt", "command_icon.png")
        self.editor = TextEditor("", size = (800, 600), font_size = 15)
        self.display(">>> ")

    def update(self, parent, event):
        self.editor.update(self.window, event, parent.topmost_window(self.window))
        if parent.topmost_window(self.window) and event.detect(p.KEYDOWN) and event.key[p.K_RETURN]:
            self.run_command(parent)

        return super().update(parent, event)

    def run_command(self, parent):
        command = self.editor.text[-(self.editor.grid[-1] - 3):][:-1]
        if len(command) == 0 or command.isspace():
            self.display(">>> ")
            return

        arguments = command.split(' ')
        func, arguments = arguments[0], arguments[1:]
        if func == "help":
            self.display("--- List of Commands ---\n"
                         "    echo *args\n"
                         "    quit\n"
                         "    shutdown\n"
                         "-------------------------")
        elif func == "echo":
            self.display(' '.join(arguments))
        elif func == "quit":
            parent.quit_application(self)
        elif func == "shutdown":
            parent.execute = False
        else:
            self.display(f"command not recognized: '{func}'")

        self.display('\n>>> ')

    def display(self, text):
        self.editor.cursor.position = len(self.editor.text)
        self.editor.highlight.position = None
        self.editor.append(text)
        self.editor.lockedZone = self.editor.cursor.position