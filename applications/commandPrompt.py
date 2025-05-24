from applications.application import Application

class CommandPrompt(Application):
    icon = "command_icon.png"

    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent.new_window(self, (400, 300), "Command Prompt", "command_icon.png")

    def update(self, parent, event):
        return super().update(parent, event)