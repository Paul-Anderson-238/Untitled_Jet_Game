########################################################
## Menu.py: Creates the menu and decides which game state to enter
########################################################
## Author: Paul Anderson
## Version: 2.0.0
## Status: Replaced the old video based demo mode to new self playing version, Added Title Banner
########################################################
import screeninfo
import pygame
from Run_Game import run_game
from Display_High_Scores import display_high_scores
from High_Scores_Idle import high_scores_idle
from Demo_Mode import demo_mode
from Sprite_Select import sprite_select
from random import choice 
import pathlib

def menu(screen, clock):
    ############################################################################################################
    #A function to control the resizing logic should the player resize the window. Resizes all elements that 
    #appear on the screen according to ratios that have already been calculated.
    #	inputs:
    #	outputs:
    ############################################################################################################
    def resize_window():
        nonlocal title_font, difficulty_font, font, background
        title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/12))
        difficulty_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/16))
        font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
        background = pygame.transform.smoothscale(background, screen.get_size())
    
    TITLE = "Hill STEM Jet Game"
    
    sprites_path = pathlib.Path("./img/sprites")
    SPRITES = [path for path in sprites_path.iterdir() if path.is_file()]
    
    difficulties = ["Easy", "Normal", "Hard"] #Acceptable Difficulty Settings
    DIFF_KEY = 1                      #Tracks which difficulty the player is currently selecting
    
    background = pygame.image.load("./img/background_cave_blue.png").convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    
    pygame.font.init()
    title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/12))
    difficulty_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
    font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/24))
    
    WHITE = (255,255,255)
    ORANGE = (255,200,0)
    
    
    RUN_MENU = True

    delay_frames = 300
    frames = 0

    while RUN_MENU:
        screen.fill("purple")
        screen.blit(background, (0,0))
        text_boxes = []
        
        if (frames // 30) % 2 == 0:
            title_text = title_font.render(TITLE, False, ORANGE)
        else:
            title_text = title_font.render(TITLE, False, WHITE)
        title_text_box = title_text.get_rect()
        title_text_box.centerx = int(screen.get_width() / 2)
        title_text_box.bottom = int(screen.get_height() / 4)
        
        text_boxes.append((title_text, title_text_box))
        
        difficulty_text = difficulty_font.render("SELECT DIFFICULTY:", False, WHITE)    
        difficulty_text_box = difficulty_text.get_rect()
        difficulty_text_box.centerx = int(screen.get_width() / 2) 
        difficulty_text_box.bottom = int(screen.get_height() / 3)
        
        text_boxes.append((difficulty_text, difficulty_text_box))
        
        i = 0 #index for text boxes list
        for _ in difficulties:
            difficulty_text = font.render(f"{difficulties[i]}", False, WHITE if i != DIFF_KEY else ORANGE)
            difficulty_text_box = difficulty_text.get_rect()
            anchor = (text_boxes[i+1][1].midbottom)
            anchor = (anchor[0], anchor[1] + 20)
            difficulty_text_box.midtop = anchor
            i += 1
            text_boxes.append((difficulty_text, difficulty_text_box))
        
        for text in text_boxes:
            screen.blit(text[0], text[1])
        
        pygame.display.update()
        for event in pygame.event.get():
            delay_frames = frames + 300
            if event.type == pygame.QUIT:
                RUN_MENU = False
                pygame.display.quit()

            if event.type == pygame.WINDOWRESIZED:
                resize_window()

            if event.type == pygame.MOUSEBUTTONDOWN:
                end_game, sprite = sprite_select(screen, clock)
                if not end_game:
                    end_game, score = run_game(screen, clock, difficulties[DIFF_KEY], sprite)
                if end_game:
                    RUN_MENU = False
                    pygame.display.quit()
                else:
                    end_game = display_high_scores(screen, clock, score, difficulties[DIFF_KEY])
                    #Re-scale font and screen sizes in case one of the other states changed the size
                    difficulty_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/16))
                    font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
                    background = pygame.transform.smoothscale(background, screen.get_size())
                if end_game:
                    RUN_MENU = False
                    pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    DIFF_KEY = (DIFF_KEY+1) % len(difficulties)
                if event.key == pygame.K_w or event.key == pygame.K_UP:  
                    DIFF_KEY = (DIFF_KEY-1) % len(difficulties)
                if event.key == pygame.K_ESCAPE:
                    RUN_MENU = False
                    pygame.display.quit()
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    end_game, sprite = sprite_select(screen, clock)
                    if not end_game:
                        end_game, score = run_game(screen, clock, difficulties[DIFF_KEY], sprite)
                    if end_game:
                        RUN_MENU = False
                        pygame.display.quit()
                    else:
                        end_game = display_high_scores(screen, clock, score, difficulties[DIFF_KEY])
                        #Re-scale font and screen sizes in case one of the other states changed the size
                        difficulty_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/16))
                        font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
                        background = pygame.transform.smoothscale(background, screen.get_size())
                    if end_game:
                        RUN_MENU = False
                        pygame.display.quit()
        
        #delay_frames is a mark to track if no activity has been detected in 10 seconds
        if delay_frames <= frames:
            AWAKE, QUIT = demo_mode(screen, clock, choice(SPRITES))
            if QUIT:
                RUN_MENU = False
                pygame.display.quit()
            #returns False unless player opted to close the game.
            elif not AWAKE:
                if high_scores_idle(screen, clock):
                    RUN_MENU = False
                    pygame.display.quit()
            delay_frames = frames + 300
            difficulty_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/16))
            font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
            background = pygame.transform.smoothscale(background, screen.get_size())

        #some logic so the frames number doesn't get too big. keep the math simple
        if frames >= 100000:
            diff = delay_frames - frames
            frames = 0
            delay_frames = diff

        frames += 1
        clock.tick(30)

#################################################################################################
# Running this file as a script: If running this file as a script, it will test the function with 
#                                test values. Feel free to tweak and test from here. 
#################################################################################################
if __name__ == "__main__":
    for m in screeninfo.get_monitors():
        if m.is_primary:
            monitor = m
    INITIAL_SIZE = (int(monitor.width * 0.5), int(monitor.height * 0.5)) #Initial Screen size
    screen = pygame.display.set_mode(INITIAL_SIZE, pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Untitled Jet Game")
    menu(screen, clock)
