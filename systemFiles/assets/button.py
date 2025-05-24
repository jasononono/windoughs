import pygame as p
from systemFiles.assets import icon


class ButtonTemplate:
    def __init__(self, position = (0, 0), size = (19, 19),
                 colour = (228, 239, 250), highlight_colour = (250, 250, 255),):
        self.surface = p.Surface(size)
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = position
        self.abs = None

        self.pressed = False
        self.status = True

        self.colour = colour
        self.highlightColour = highlight_colour

    def get_rect(self, parent):
        self.abs = parent.abs[0] + self.rect.x, parent.abs[1] + self.rect.y

    def mechanic(self, parent, event, enabled, status):
        self.get_rect(parent)
        if status is not None:
            self.status = status

        if self.valid_mouse_position(event.mouse_pos) and self.status:
            if event.mouse[0]:
                self.pressed = True
        else:
            self.pressed = False

        if enabled is not None:
            self.surface.fill(self.highlightColour if enabled else self.colour)
        elif self.valid_mouse_position(event.mouse_pos) and self.status:
            self.surface.fill(self.highlightColour)
        else:
            self.surface.fill(self.colour)

        if self.pressed and event.detect(p.MOUSEBUTTONUP):
            return True
        return False

    def update(self, parent, event, enabled = None, status = None):
        action = self.mechanic(parent, event, enabled, status)
        parent.surface.blit(self.surface, self.rect)
        return action

    def valid_mouse_position(self, position):
        if (self.abs[0] < position[0] < self.abs[0] + self.rect.width and
            self.abs[1] < position[1] < self.abs[1] + self.rect.height):
            return True
        return False


class ImageButton(ButtonTemplate):
    def __init__(self, position = (0, 0), image = None, size = (40, 40),
                 colour = (228, 239, 250), highlight_colour = (250, 250, 255), image_size = (25, 25)):
        self.image = icon.ImageIcon(image, image_size)
        super().__init__(position, size, colour, highlight_colour)

    def update(self, parent, event, enabled = None, status = None):
        action = super().mechanic(parent, event, enabled, status)
        self.image.display(self.surface, (self.rect.width / 2, self.rect.height / 2))
        parent.surface.blit(self.surface, self.rect)
        return action


class IconButton(ButtonTemplate):
    def __init__(self, position = (0, 0), instruction = icon.x, size = (40, 40),
                 colour = (255, 255, 255), highlight_colour = (250, 250, 255),
                 foreground = (48, 53, 61), highlight_foreground = None):
        super().__init__(position, size, colour, highlight_colour)
        self.icon = icon.Icon(instruction, [min(size)] * 2)
        self.foreground = foreground
        self.highlightForeground = foreground if highlight_foreground is None else highlight_foreground

    def update(self, parent, event, enabled = None, status = None):
        action = super().update(parent, event, enabled, status)
        self.icon.display(parent, [self.abs[i] + self.rect.size[i] / 2 for i in range(2)],
                          self.highlightForeground if (self.valid_mouse_position(event.mouse_pos) and
                                                       self.status) or enabled else self.foreground)
        return action


'''
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