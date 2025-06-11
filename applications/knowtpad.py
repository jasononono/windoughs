from systemFiles.assets import base

from applications.application import Application
from systemFiles.assets.textEngine.text import TextEditor

class Knowtpad(Application):
    icon = "knowtpad_icon.png"

    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent.new_window(self, (400, 300), "Knowtpad", self.icon)
        self.editor = TextEditor("", size = (400, 300), font_size = 16,
                                 background = base.GREY1, colour = base.BLACK, highlight_colour = base.HIGHLIGHT2)

    def update(self, parent, event):
        self.editor.update(self.window, event, parent.topmost_window(self.window))

        return super().update(parent, event)