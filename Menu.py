########################################################
## Menu.py: Creates the menu and decides which game state to enter
########################################################
## Author: Paul Anderson
## Version: 1.1.0
## Status: Alpha Complete, Screen Scaling Added.
########################################################
import screeninfo
import pygame
from Run_Game import run_game
from Display_High_Scores import display_high_scores
from High_Scores_Idle import high_scores_idle

def menu(screen, clock):
    def resize_window():
        nonlocal title_font, font, background
        title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/16))
        font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
        background = pygame.transform.smoothscale(background, screen.get_size())
    
    difficulties = ["Easy", "Normal", "Hard"] #Acceptable Difficulty Settings
    DIFF_KEY = 1                      #Tracks which difficulty the player is currently selecting
    
    background = pygame.image.load("./img/background_cave_blue.png").convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    
    pygame.font.init()
    title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/16))
    font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
    
    WHITE = (255,255,255)
    ORANGE = (255,200,0)
    
    
    RUN_MENU = True

    delay_frames = 300
    frames = 0

    while RUN_MENU:
        screen.fill("purple")
        screen.blit(background, (0,0))
        text_boxes = []
        
        select_text = title_font.render("SELECT DIFFICULTY:", False, WHITE)
        select_text_box = select_text.get_rect()
        select_text_box.centerx = int(screen.get_width() / 2) 
        select_text_box.bottom = int(screen.get_height() / 3)
        
        text_boxes.append((select_text, select_text_box))
        
        i = 0 #index for text boxes list
        for _ in difficulties:
            difficulty_text = font.render(f"{difficulties[i]}", False, WHITE if i != DIFF_KEY else ORANGE)
            difficulty_text_box = difficulty_text.get_rect()
            anchor = (text_boxes[i][1].midbottom)
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
                end_game, score = run_game(screen, clock, difficulties[DIFF_KEY])
                if end_game:
                    RUN_MENU = False
                    pygame.display.quit()
                else:
                    end_game = display_high_scores(screen, clock, score, difficulties[DIFF_KEY])
                    #Re-scale font and screen sizes in case one of the other states changed the size
                    title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/16))
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
                    end_game, score = run_game(screen, clock, difficulties[DIFF_KEY])
                    if end_game:
                        RUN_MENU = False
                        pygame.display.quit()
                    else:
                        end_game = display_high_scores(screen, clock, score, difficulties[DIFF_KEY])
                        #Re-scale font and screen sizes in case one of the other states changed the size
                        title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/16))
                        font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
                        background = pygame.transform.smoothscale(background, screen.get_size())
                    if end_game:
                        RUN_MENU = False
                        pygame.display.quit()
        
        #delay_frames is a mark to track if no activity has been detected in 10 seconds
        if delay_frames <= frames:
            #returns False unless player opted to close the game.
            if high_scores_idle(screen, clock):
                RUN_MENU = False
                pygame.display.quit()
            delay_frames = frames + 300

        frames += 1
        clock.tick(30)

if __name__ == "__main__":
    for m in screeninfo.get_monitors():
        if m.is_primary:
            monitor = m
    INITIAL_SIZE = (int(monitor.width * 0.8), int(monitor.height * 0.8)) #Initial Screen size
    screen = pygame.display.set_mode(INITIAL_SIZE, pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Untitled Jet Game")
    menu(screen, clock)