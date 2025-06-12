import pygame as p
import random
from systemFiles.assets import base

from applications.application import Application

class Snek(Application):
    icon = "default.png"

    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent.new_window(self, (900, 600), "Snek gaem", self.icon)

        self.snake = [(20 + i, 10) for i in range(5)]
        self.apples = [(30, 10)]
        self.direction = p.K_d
        self.pendingDirection = p.K_d
        self.speed = 3
        self.tick = 0

    def movement(self):
        self.direction = self.pendingDirection
        x, y = self.snake[-1]
        if self.direction == p.K_d:
            new = x + 1, y
        elif self.direction == p.K_a:
            new = x - 1, y
        elif self.direction == p.K_s:
            new = x, y + 1
        else:
            new = x, y - 1
        self.snake.append((new[0] % 45, new[1] % 30))

    def generate(self):
        attempt = random.randint(0, 44), random.randint(0, 29)
        if attempt in self.snake:
            return self.generate()
        self.apples.append(attempt)

    def update(self, parent, event):
        self.window.surface.fill(base.BLACK)

        key = event.key_down()
        if ((key == p.K_w and self.direction != p.K_s) or
                (key == p.K_a and self.direction != p.K_d) or
                (key == p.K_s and self.direction != p.K_w) or
                (key == p.K_d and self.direction != p.K_a)):
            self.pendingDirection = key

        self.tick -= 1
        if self.tick <= 0:
            self.tick = self.speed
            self.movement()
            if self.snake[-1] in self.apples:
                i = self.apples.index(self.snake[-1])
                del self.apples[i]
                amount = min(random.randint(1, len(self.snake) // 20 + 1), 1350 - len(self.snake) + len(self.apples))
                print(amount)
                for _ in range(amount):
                    self.generate()
            else:
                del self.snake[0]

        for i in self.snake:
            p.draw.rect(self.window.surface, base.WHITE, (*[j * 20 for j in i], 20, 20))
        for i in self.apples:
            p.draw.rect(self.window.surface, base.RED, (*[j * 20 for j in i], 20, 20))

        return super().update(parent, event)