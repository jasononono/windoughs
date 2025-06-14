import pygame as p
from systemFiles.assets import base

from systemFiles.icons import iconOptions


class Instruction:
    def __init__(self):
        self.template = []

    def draw_line(self, start, end, width = 2):
        self.template.append((Icon.draw_line, (start, end, width)))


class Icon:
    def __init__(self, instruction, size = (19, 19)):
        self.size = size
        self.instruction = instruction

    def display(self, parent, position = (0, 0), colour = base.BLACK):
        for i, j in self.instruction.template:
            i(self, parent.surface, position, colour, *j)

    def draw_line(self, surface, position, colour, start, end, width):
        p.draw.line(surface, colour,
                    [position[i] + (start[i] - 0.5) * self.size[i] for i in range(2)],
                    [position[i] + (end[i] - 0.5) * self.size[i] for i in range(2)], width)


class ImageIcon:
    def __init__(self, image = None, size = (28, 28)):
        if image is None:
            image = "default.png"
        self.image = p.image.load("systemFiles/icons/" + image)
        image_size = self.image.get_size()
        if image_size[0] / size[0] < image_size[1] / size[1]:
            image_size = image_size[0] / image_size[1] * size[1], size[1]
        else:
            image_size = size[0], image_size[1] / image_size[0] * size[0]
        if image in iconOptions.smoothIcons:
            self.image = p.transform.smoothscale(self.image, image_size)
        else:
            self.image = p.transform.scale(self.image, image_size)
        self.rect = self.image.get_rect()

    def display(self, surface, position):
        self.rect.center = position
        surface.blit(self.image, self.rect)


x = Instruction()
x.draw_line((0.35, 0.35), (0.65, 0.65), 2)
x.draw_line((0.35, 0.65), (0.65, 0.35), 2)

square = Instruction()
square.draw_line((0.35, 0.35), (0.65, 0.35))
square.draw_line((0.65, 0.35), (0.65, 0.65))
square.draw_line((0.65, 0.65), (0.35, 0.65))
square.draw_line((0.35, 0.65), (0.35, 0.35))

hLine = Instruction()
hLine.draw_line((0.35, 0.5), (0.65, 0.5), 2)