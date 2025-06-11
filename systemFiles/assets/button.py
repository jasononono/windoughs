import pygame as p
from systemFiles.assets import base

from systemFiles.assets import icon
from systemFiles.assets.font import Font


class ButtonTemplate:
    def __init__(self, position = (0, 0), size = (19, 19),
                 colour = base.TINTED_GREY2, highlight_colour = base.WHITE):
        self.surface = p.Surface(size)
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = position
        self.abs = None

        self.pressed = False
        self.status = True

        self.colour = colour
        self.highlightColour = highlight_colour

    def mechanic(self, parent, event, enabled, status):
        self.abs = parent.abs[0] + self.rect.x, parent.abs[1] + self.rect.y

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
                 colour = base.TINTED_GREY2, highlight_colour = base.WHITE, image_size = (25, 25)):
        self.image = icon.ImageIcon(image, image_size)
        super().__init__(position, size, colour, highlight_colour)

    def update(self, parent, event, enabled = None, status = None):
        action = super().mechanic(parent, event, enabled, status)
        self.image.display(self.surface, (self.rect.width / 2, self.rect.height / 2))
        parent.surface.blit(self.surface, self.rect)
        return action


class IconButton(ButtonTemplate):
    def __init__(self, position = (0, 0), instruction = icon.x, size = (40, 40),
                 colour = base.WHITE, highlight_colour = base.WHITE,
                 foreground = (48, 53, 61), highlight_foreground = None, skipped_parent = False):
        super().__init__(position, size, colour, highlight_colour)
        self.icon = icon.Icon(instruction, [min(size)] * 2)
        self.foreground = foreground
        self.highlightForeground = foreground if highlight_foreground is None else highlight_foreground
        self.skippedParent = skipped_parent

    def update(self, parent, event, enabled = None, status = None):
        action = super().update(parent, event, enabled, status)
        self.icon.display(parent,
                          [(self.abs[i] if self.skippedParent else 0) + self.rect.size[i] / 2 for i in range(2)],
                          self.highlightForeground if (self.valid_mouse_position(event.mouse_pos) and
                                                       self.status) or enabled else self.foreground)
        return action


class TextButton(ButtonTemplate):
    def __init__(self, position = (0, 0), text = "OK", size = None,
                 colour = base.GREY2, highlight_colour = base.WHITE,
                 foreground = base.BLACK, highlight_foreground = None, font = "segoeui", font_size = 15):
        self.font = Font(font_size, font)
        self.text = text
        self.size = self.font.get_size(self.text)
        if size is None:
            size = self.size[0] + 30, self.size[1] + 15
        super().__init__(position, size, colour, highlight_colour)

        self.position = [(self.rect.size[i] - self.size[i]) / 2 for i in range(2)]
        self.foreground = foreground
        self.highlightForeground = foreground if highlight_foreground is None else highlight_foreground

    def update(self, parent, event, enabled = None, status = None):
        action = super().mechanic(parent, event, enabled, status)
        self.font.render(self.surface, self.text, self.position,
                         self.highlightForeground if (self.valid_mouse_position(event.mouse_pos) and self.status)
                                                     or enabled else self.foreground)
        parent.surface.blit(self.surface, self.rect)
        return action