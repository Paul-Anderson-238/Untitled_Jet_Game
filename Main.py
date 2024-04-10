########################################################
## Main.py: Launch Point of the Program
########################################################
## Author: Paul Anderson
## Version: 2.0.0
## Status: Various changes to sprite selection
########################################################
## This program was created for STEM outreach of Hill AFB
## There is no copyright on any of the code. As primary
## author of the code, I don't care and authorize anyone
## who wishes to use and adjust code at will and without
## crediting me. In other words, if you get your hands on
## any of this code, have fun. :)
########################################################
from Menu import menu
from screeninfo import get_monitors
import pygame

if __name__ == "__main__":
    for m in get_monitors():
        if m.is_primary:
            monitor = m
    INITIAL_SIZE = (int(monitor.width/2), int(monitor.height/2)) #Initial Screen size
    screen = pygame.display.set_mode(INITIAL_SIZE, pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Untitled Jet Game")
    pygame.event.set_allowed([pygame.QUIT, pygame.WINDOWRESIZED, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN])
    menu(screen, clock)
