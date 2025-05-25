import pygame as p

from systemFiles.assets.font import Font
from systemFiles.assets.textEngine.cursor import Cursor

class TextDisplay:
    def __init__(self, text = "", pos = (0, 0), size = (800, 600), margin = (10, 10), spacing = (0.6, 1.2),
                 font = "lucon", font_size = 14, background = (0, 0, 0), colour = (255, 255, 255)):
        self.text = text
        self.font = Font(font_size, font)

        self.surface = p.Surface(size)
        self.rect = self.surface.get_rect()
        self.rect.topleft = pos
        self.abs = None
        self.margin = margin
        self.spacing = spacing

        self.background = background
        self.colour = colour

        self.grid = []

    def valid_mouse_position(self, position):
        if (self.abs[0] < position[0] < self.abs[0] + self.rect.width and
            self.abs[1] < position[1] < self.abs[1] + self.rect.height):
            return True
        return False

    def display(self, text, index, position):
        coord = (self.margin[0] + position[0] * self.font.size * self.spacing[0],
                 self.margin[1] + position[1] * self.font.size * self.spacing[1])
        if text != '\n':
            self.font.render(self.surface, text, coord, self.colour)

    def get_grid(self):
        row, column = 0, 0
        self.grid = []
        for n, i in enumerate(self.text):
            if i == '\n':
                self.grid.append(column)
                column = 0
                row += 1
            else:
                column += 1
        self.grid.append(column)
        return self.grid

    def update(self, parent, event):
        self.abs = parent.abs[0] + self.rect.x, parent.abs[1] + self.rect.y

        self.surface.fill(self.background)

        row, column = 0, 0
        self.grid = []

        for n, i in enumerate(self.text):
            self.display(i, n, (column, row))
            if i == '\n':
                self.grid.append(column)
                column = 0
                row += 1
            else:
                column += 1
        self.grid.append(column)

        parent.surface.blit(self.surface, self.rect)


class TextEditor(TextDisplay):
    def __init__(self, text = "", pos = (0, 0), size = (800, 600), margin = (10, 10), spacing = (0.6, 1.2),
                 font = "lucon", font_size = 14, background = (0, 0, 0), colour = (255, 255, 255)):
        super().__init__(text, pos, size, margin, spacing, font, font_size, background, colour)

        from systemFiles.assets.textEngine.action import Action
        from systemFiles.assets.textEngine.keyboard import keyboard
        self.action = Action(self, keyboard)
        self.cursor = Cursor(0)
        self.highlight = Cursor()

    def get_coordinates(self, pos):
        if pos < 0:
            return 0, 0
        total = 0
        for i, j in enumerate(self.grid):
            total += j + 1
            if pos < total:
                return pos - total + j + 1, i
        return self.get_coordinates(len(self.text))

    def get_position(self, coord):
        column = max(coord[0], 0)
        row = max(coord[1], 0)
        pos = sum(self.grid[:row]) + row + min(self.grid[row], column)
        return min(len(self.text), max(0, pos))

    def get_mouse_coordinates(self, coord):
        column = round((coord[0] - self.abs[0] - self.margin[0]) / self.spacing[0] / self.font.size)
        row = min(int((coord[1] - self.abs[1] - self.margin[1]) / self.spacing[1] / self.font.size), len(self.grid) - 1)
        return column, row

    def display(self, text, index, position):
        coord = (self.margin[0] + position[0] * self.font.size * self.spacing[0],
                 self.margin[1] + position[1] * self.font.size * self.spacing[1])
        highlighted = (self.highlight.position is not None and min(self.cursor.position, self.highlight.position) <=
                       index < max(self.cursor.position, self.highlight.position))

        if highlighted:
            p.draw.rect(self.surface, (67, 67, 156),
                        (coord[0], coord[1],
                         (int(self.font.size * self.spacing[0]) + 1 if text != '\n' else
                          self.rect.x + self.rect.width - coord[0] - self.margin[0]),
                        int(self.font.size * self.spacing[1]) + 1))
        if text != '\n':
            self.font.render(self.surface, text, coord, self.colour)

    def update(self, parent, event, active = True):
        super().update(parent, event)

        if self.highlight.position is None:
            coord = self.get_coordinates(self.cursor.position)
            self.cursor.update(self.surface, self.font, coord,
                               (self.margin[0], self.margin[1]), self.spacing)

        if active:
            self.action.update(event)

        if self.valid_mouse_position(event.mouse_pos):
            p.mouse.set_cursor(p.SYSTEM_CURSOR_IBEAM)
        else:
            p.mouse.set_cursor(p.SYSTEM_CURSOR_ARROW)

        parent.surface.blit(self.surface, self.rect)

    def append(self, txt):
        if self.highlight.position is None:
            self.text = self.text[:self.cursor.position] + txt + self.text[self.cursor.position:]
            self.cursor.position += len(txt)
        else:
            self.text = (self.text[:min(self.cursor.position, self.highlight.position)] + txt +
                         self.text[max(self.cursor.position, self.highlight.position):])
            self.cursor.position = min(self.cursor.position, self.highlight.position) + len(txt)
        self.highlight.position = None

    def delete(self):
        if self.highlight.position is not None:
            self.text = (self.text[:min(self.cursor.position, self.highlight.position)] +
                         self.text[max(self.cursor.position, self.highlight.position):])
            self.cursor.position = min(self.cursor.position, self.highlight.position)
        elif self.cursor.position > 0:
            self.text = self.text[:self.cursor.position - 1] + self.text[self.cursor.position:]
            self.cursor.position -= 1
        self.highlight.position = None

    def cursor_left(self):
        if self.highlight.position is not None:
            self.cursor.position = min(self.cursor.position, self.highlight.position)
            self.highlight.position = None
        elif self.cursor.position > 0:
            self.cursor.position -= 1
        self.cursor.blink = 0

    def cursor_right(self):
        if self.highlight.position is not None:
            self.cursor.position = max(self.cursor.position, self.highlight.position)
            self.highlight.position = None
        elif self.cursor.position < len(self.text):
            self.cursor.position += 1
        self.cursor.blink = 0

    def cursor_down(self):
        if self.highlight.position is not None:
            self.cursor.position = max(self.cursor.position, self.highlight.position)
            self.highlight.position = None
        column, row = self.get_coordinates(self.cursor.position)
        self.cursor.position = len(self.text) if row == len(self.grid) - 1 else self.get_position((row + 1, column))
        self.cursor.blink = 0

    def cursor_up(self):
        if self.highlight.position is not None:
            self.cursor.position = min(self.cursor.position, self.highlight.position)
            self.highlight.position = None
        column, row = self.get_coordinates(self.cursor.position)
        self.cursor.position = 0 if row == 0 else self.get_position((row - 1, column))
        self.cursor.blink = 0

    def highlight_left(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        if self.cursor.position > 0:
            self.cursor.position -= 1
        self.cursor.blink = 0

    def highlight_right(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        if self.cursor.position < len(self.text):
            self.cursor.position += 1
        self.cursor.blink = 0

    def highlight_down(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        column, row = self.get_coordinates(self.cursor.position)
        self.cursor.position = len(self.text) if row == len(self.grid) - 1 else self.get_position((row + 1, column))
        self.cursor.blink = 0

    def highlight_up(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        column, row = self.get_coordinates(self.cursor.position)
        self.cursor.position = 0 if row == 0 else self.get_position((row - 1, column))
        self.cursor.blink = 0

    def select_all(self):
        self.highlight.position = 0
        self.cursor.position = len(self.text)

    def indent(self):
        self.append("    ")