from applications.application import Application

class Start(Application):
    icon = "start_icon.png"

    def __init__(self, parent):
        super().__init__(parent)

        self.window = parent.new_window(self)

    def update(self, parent, event):
        super().update(parent, event)