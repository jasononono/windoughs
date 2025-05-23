class CommandPrompt:
    icon = "command_icon.png"

    def __init__(self, parent):
        self.window = parent.new_window(self, (400, 300), "Command Prompt", "command_icon.png")

    def update(self, parent, event):
        for i in parent.get_windows(self):
            parent.requestedUpdates.append(i)
        if len(parent.get_windows(self)) == 0:
            parent.quit_application(self)