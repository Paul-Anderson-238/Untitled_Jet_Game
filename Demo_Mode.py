########################################################
## Demo_Mode.py: Functions for detecting collision in game
########################################################
## Author: Paul Anderson
## Version: 1.2.0
## Status: Alpha Complete, Screen Scaling Added.
########################################################

import pygame
import screeninfo
import cv2
from os import listdir
from os.path import isfile, join
from random import choice
############################################################################################################
#This function simply plays a video clip to the screen. 
#	inputs:
#		screen: the screen object we are displaying the video on
#       clock: the clock object so the screen can update
#       WIDTH: the width of the screen so the video can be scaled properly. also used for resizing
#       HEIGHT: the height of the screen so the video can be scaled properly. also used for resizing
#	outputs:
#		AWAKE: a boolean value indicating if the player pressed a key or mousebutton to wake the game up
#       QUIT: a boolean value indicating if the player gave the command to close the game
############################################################################################################
def demo_mode(screen, clock, WIDTH, HEIGHT):
    video_file_file = "img/idle_videos/"
    paths = [f for f in listdir(video_file_file) if isfile(join(video_file_file, f))]

    video = cv2.VideoCapture(video_file_file + choice(paths))
    success, video_image = video.read()
    fps = video.get(cv2.CAP_PROP_FPS)

    QUIT = False
    AWAKE = False
    run = success
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                QUIT = True
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                AWAKE = True
            if event.type == pygame.WINDOWRESIZED:
                x_scale = screen.get_width() / WIDTH
                y_scale = screen.get_height() / HEIGHT
                WIDTH *= x_scale
                HEIGHT *= y_scale
            
        success, video_image = video.read()
        if success:
            video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
        else:
            run = False
        video_surf = pygame.transform.smoothscale(video_surf, (WIDTH, HEIGHT))

        screen.blit(video_surf, (0,0))
        clock.tick(fps)
        pygame.display.update()

    
    ##### Delay 2 seconds before returning ###################################################################
    target = fps * 2
    counter = 0
    while counter < target:
        clock.tick(fps)
        counter+=1

    return AWAKE, QUIT

if __name__ == "__main__":
    for m in screeninfo.get_monitors():
        if m.is_primary:
            monitor = m
    INITIAL_SIZE = (int(monitor.width * 0.8), int(monitor.height * 0.8)) 
    WIDTH = INITIAL_SIZE[0]
    HEIGHT = INITIAL_SIZE[1]
    
    screen = pygame.display.set_mode(INITIAL_SIZE, pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Untitled Jet Game")
    demo_mode(screen, clock, WIDTH, HEIGHT)
    pygame.quit()
    exit()