import pygame as p
import icon

class ButtonTemplate:
    def __init__(self, position = (0, 0), size = (19, 19),
                 colour = (228, 239, 250), highlight_colour = (242, 247, 254)):
        self.surface = p.Surface(size)
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = position
        self.abs = None

        self.colour = colour
        self.highlightColour = highlight_colour

    def get_rect(self, parent):
        self.abs = parent.abs[0] + self.rect.x, parent.abs[1] + self.rect.y

    def mechanic(self, parent, event):
        self.get_rect(parent)
        if self.valid_mouse_position(event.mouse_pos):
            self.surface.fill(self.highlightColour)
            if event.detect(p.MOUSEBUTTONDOWN):
                return True
        else:
            self.surface.fill(self.colour)
        return False

    def update(self, parent, event):
        action = self.mechanic(parent, event)
        parent.surface.blit(self.surface, self.rect)
        return action

    def valid_mouse_position(self, position):
        if (self.abs[0] < position[0] < self.abs[0] + self.rect.width and
            self.abs[1] < position[1] < self.abs[1] + self.rect.height):
            return True
        return False

class ImageButton(ButtonTemplate):
    def __init__(self, position = (0, 0), image = "home_icon.png", size = (40, 40),
                 colour = (228, 239, 250), highlight_colour = (242, 247, 254), image_size = (28, 28)):
        self.image = icon.Image(image, image_size)
        super().__init__(position, size, colour, highlight_colour)

    def update(self, parent, event):
        action = super().mechanic(parent, event)
        self.image.display(self.surface, (self.rect.width / 2, self.rect.height / 2))
        parent.surface.blit(self.surface, self.rect)
        return action

'''
class IconButton(ButtonTemplate):
    def __init__(self, parent, command, position = (0, 0), size = (19, 19), instruction = icon.x,
                 colour = (45, 45, 55), highlight_colour = (55, 55, 65)):
        super().__init__(parent, command, position, size, colour, highlight_colour)
        self.icon = icon.Icon(instruction)

    def update(self, screen):
        action = super().update(screen)
        self.icon.display(screen, (self.absX, self.absY))
        return action


class TextButton(ButtonTemplate):
    def __init__(self, parent, command, position = (0, 0), text = "Ok", fontSize = 13,
                 colour = (55, 55, 65), highlight_colour = (45, 45, 55)):
        self.text = text
        self.font = Font(size = fontSize, bold = True)
        self.status = True
        super().__init__(parent, command, position, self.get_size(), colour, highlight_colour)

    def get_size(self):
        return [i + 10 for i in self.font.get_size(self.text)]

    def update(self, screen):
        action = None
        if self.status:
            action = super().update(screen)
        screen.surface.blit(self.font.render(self.text, ((255, 255, 255) if self.status else (150, 150, 150))), (self.absX + 5, self.absY + 5))
        return action
'''