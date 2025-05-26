import pygame as p
from systemFiles.assets import base

from systemFiles.assets.font import Font
from systemFiles.assets.button import IconButton
from systemFiles.assets.icon import ImageIcon


class Window:
    def __init__(self, application, position = (0, 0), size = (400, 300),
                 title = "Window", title_bar_colour = base.WHITE, title_bar_height = 30,
                 icon = None, icon_size = 20):
        self.application = application

        self.size = [i for i in size]
        self.minSize = (100, 100)
        self.surface = p.Surface(size)
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = position[0], position[1] + title_bar_height
        self.title_bar = self.rect.copy()
        self.title_bar.y -= title_bar_height
        self.title_bar.height = title_bar_height

        self.title = title
        self.title_bar_colour = title_bar_colour
        self.font = Font(13)
        self.iconSize = icon_size
        self.icon = None if icon is None else ImageIcon(icon, [icon_size] * 2)

        self.resizeSide = None
        self.resizeBind = None

        self.exitButton = IconButton(size = (40, self.title_bar.height),
                                     highlight_colour = base.RED, highlight_foreground = base.WHITE)

        self.offset = 0, 0
        self.abs = 0, 0

    def get_rect(self):
        self.surface = p.transform.scale(self.surface, self.size)
        self.rect.width, self.rect.height = self.size
        self.title_bar.width = self.rect.width
        self.rect.x, self.rect.y = self.title_bar.x, self.title_bar.y + self.title_bar.height

        self.exitButton.rect.topleft = self.title_bar.right - 40, self.title_bar.top

    def update(self, parent, event):
        self.fit_to_surface(parent.bound)
        self.get_rect()
        self.abs = parent.abs[0] + self.rect.x, parent.abs[1] + self.rect.y

        # BORDER
        if parent.topmost_window(self):
            p.draw.rect(parent.surface, base.GREY2,
                        (self.rect.left - 2, self.title_bar.top - 2,
                        self.rect.width + 4, self.rect.height + self.title_bar.height + 4))
        else:
            p.draw.rect(parent.surface, base.GREY3,
                        (self.rect.left - 1, self.title_bar.top - 1,
                         self.rect.width + 2, self.rect.height + self.title_bar.height + 2))

        # TITLE BAR
        p.draw.rect(parent.surface, self.title_bar_colour, self.title_bar)

        action = self.exitButton.update(parent, event, status = parent.topmost_window(self))

        if self.icon is not None:
            self.icon.display(parent.surface,
                              (self.title_bar.left + self.iconSize / 2 + 5, self.title_bar.centery))
        size = self.font.get_size(self.title)
        self.font.render(parent.surface, self.title,
                                (self.title_bar.left + (15 if self.icon is None else self.iconSize + 15),
                                 self.title_bar.centery - size[1] / 2))

        self.offset = event.mouse_pos[0] - self.title_bar.x, event.mouse_pos[1] - self.title_bar.y

        # SURFACE
        parent.surface.blit(self.surface, self.rect)

        return action

    def get_dragged(self, parent, event):
        return ((self.valid_drag_position(event.mouse_pos) and event.mouse_down()) or
                (parent.dragged is self and event.mouse[0]))

    def valid_mouse_position(self, position):
        if (self.abs[0] < position[0] < self.abs[0] + self.rect.width and
            self.abs[1] < position[1] < self.abs[1] + self.rect.height):
            return True
        return False

    def valid_drag_position(self, position):
        if (self.abs[0] < position[0] < self.abs[0] + self.title_bar.width - 40 and
            self.abs[1] - self.title_bar.height < position[1] < self.abs[1]):
            return True
        return False

    def valid_window_position(self, position):
        if (self.abs[0] < position[0] < self.abs[0] + self.title_bar.width and
            self.abs[1] - self.title_bar.height < position[1] < self.abs[1] + self.rect.height):
            return True
        return False

    def valid_resize_position(self, position, border = 3):
        start = (self.abs[0], self.abs[1] - self.title_bar.height)
        end = (self.abs[0] + self.title_bar.width, self.abs[1] + self.rect.height)

        top = (start[0] - border < position[0] < end[0] + border and
               start[1] - border < position[1] < start[1] + border)
        bottom = (start[0] - border < position[0] < end[0] + border and
                  end[1] - border < position[1] < end[1] + border)
        left = (start[0] - border < position[0] < start[0] + border and
                start[1] - border < position[1] < end[1] + border)
        right = (end[0] - border < position[0] < end[0] + border and
                 start[1] - border < position[1] < end[1] + border)

        if top and right:
            self.resizeSide = 2
        elif right and bottom:
            self.resizeSide = 4
        elif bottom and left:
            self.resizeSide = 6
        elif left and top:
            self.resizeSide = 8
        elif top:
            self.resizeSide = 1
            self.resizeBind = self.rect.bottom
            #p.mouse.set_cursor(p.SYSTEM_CURSOR_SIZENS)
        elif right:
            self.resizeSide = 3
            self.resizeBind = self.rect.left
            #p.mouse.set_cursor(p.SYSTEM_CURSOR_SIZEWE)
        elif bottom:
            self.resizeSide = 5
            self.resizeBind = self.rect.top
            #p.mouse.set_cursor(p.SYSTEM_CURSOR_SIZENS)
        elif left:
            self.resizeSide = 7
            self.resizeBind = self.rect.right
            #p.mouse.set_cursor(p.SYSTEM_CURSOR_SIZEWE)
        else:
            self.resizeSide = 0
        return self.resizeSide

    def follow_cursor(self, position):
        self.title_bar.x, self.title_bar.y = position[0] - self.offset[0], position[1] - self.offset[1]

    def resize(self, position, bound):
        """
        if self.resizeSide in (1, 2, 8): # top
            self.title_bar.top = max(bound.top, min(self.resizeBind - self.minSize[1] - self.title_bar.height,
                                                    position[1]))
            self.size[1] = self.resizeBind - self.title_bar.bottom

        if self.resizeSide in (4, 5, 6): # bottom
            self.rect.bottom = min(bound.bottom, max(self.resizeBind + self.minSize[1],
                                                     position[1]))
            self.size[1] = self.rect.bottom - self.resizeBind

        if self.resizeSide in (2, 3, 4): # right
            self.title_bar.right = min(bound.right, max(self.resizeBind + self.minSize[0], position[0]))
            self.size[0] = self.title_bar.right - self.resizeBind

        if self.resizeSide in ()
        """

    def fit_to_surface(self, bound):
        self.title_bar.top = max(self.title_bar.top, bound.top)
        self.title_bar.left = max(self.title_bar.left, bound.left)
        self.title_bar.right = min(self.title_bar.right, bound.right)
        self.title_bar.bottom = min(self.title_bar.bottom, bound.bottom - self.rect.height)


