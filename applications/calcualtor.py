from systemFiles.assets import base

from applications.application import Application
from systemFiles.assets.button import TextButton
from systemFiles.assets.textEngine.text import TextDisplay

class Calcualtor(Application):
    icon = "calculator_icon.png"

    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent.new_window(self, (295, 420), "Calcualtor", "calculator_icon.png")

        self.display = TextDisplay(pos = (10, 10), size = (275, 45), font_size = 30,
                                   background = base.WHITE, colour = base.BLACK)

        self.buttons = []
        for i in range(4):
            for j in range(4):
                self.buttons.append(TextButton((10 + j * 70, 65 + i * 70), "123+456-789*.0^/"[i * 4 + j],
                                               (65, 65), font_size = 30))
        self.clearEntry = TextButton((10, 345), "CE", (65, 65), font_size = 30)
        self.clear = TextButton((80, 345), "C", (65, 65), font_size = 30)
        self.equal = TextButton((150, 345), "=", (135, 65), font_size = 30)

        self.clearOnEntry = False

    def update(self, parent, event):
        self.window.surface.fill(base.GREY1)

        self.display.update(self.window, event)

        for i in self.buttons:
            if i.update(self.window, event):
                if self.clearOnEntry:
                    self.display.text = i.text
                    self.clearOnEntry = False
                else:
                    self.display.text += i.text
        if self.clearEntry.update(self.window, event):
            if self.clearOnEntry:
                self.display.text = ""
                self.clearOnEntry = False
            self.display.text = self.display.text[:-1]
        if self.clear.update(self.window, event):
            self.display.text = ""
        if self.equal.update(self.window, event):
            self.display.text = self.calculate()

        return super().update(parent, event)

    def calculate(self):
        self.clearOnEntry = True
        try:
            result = round(eval(self.display.text.replace('^', "**")), 8)
            return str(result)
        except SyntaxError:
            return "SYNTAX ERROR"
        except ZeroDivisionError:
            return "ERROR"