import pygame as p
from systemFiles.assets import base

from systemFiles.main import Screen


screen = Screen()
clock = p.time.Clock()

while screen.execute:
    clock.tick(60)
    screen.update()
p.quit()