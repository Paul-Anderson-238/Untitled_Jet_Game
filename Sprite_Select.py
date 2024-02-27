########################################################
## Demo_Mode.py: Self Playing Demo mode. Replaces old Video based demo
########################################################
## Author: Paul Anderson
## Version: 2.0.0
## Status: Modified Run_Game to conrol it's own movement logic as a demo during idle time.
########################################################

import pygame
import pathlib
import re
####################################################################################################
#Controls the normal operation of the game. There are 2 main divisions in this function:the init of  
#variables and objects, and the game loop and logic.
#	inputs:
#		screen: the screen object to display to.
#		clock: the game clock necessary to update the screen.
#	outputs:
#		AWAKE: A boolean flag to signal to the calling function if the player pressed a key to wake the game up.
#		QUIT: a boolean flag that lets the calling function know if the player opted to quit the game.
####################################################################################################
def sprite_select(screen, clock):
    def resize_game():
        nonlocal width, height, screen, BORDER_HEIGHT, title_font, sprite_font, title_text, title_text_box
        nonlocal Y_UPPER_LIMIT, Y_LOWER_LIMIT, BACKGROUND_WIDTH, background, PLAYER_Y, sprite_text, sprite_text_box
        BORDER_HEIGHT = int(screen.get_height() / 20)
        Y_UPPER_LIMIT = BORDER_HEIGHT
        Y_LOWER_LIMIT = screen.get_height()-BORDER_HEIGHT
        BACKGROUND_WIDTH = screen.get_width()
        background = pygame.transform.smoothscale(background, screen.get_size())
        title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/12))
       
        x_scale = screen.get_width()/width
        y_scale = screen.get_height()/height
        width = screen.get_width()
        height = screen.get_height()

        PLAYER_Y = int(PLAYER_Y * y_scale)
        title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/12))
        sprite_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
        
        title_text = title_font.render("SELECT SPRITE", False, WHITE)
        title_text_box = title_text.get_rect()
        title_text_box.centerx = int(screen.get_width() / 2)
        title_text_box.bottom = int(screen.get_height() / 4)
        
        sprite_rect.midtop = title_text_box.midbottom
        
        sprite_text = sprite_font.render(find_sprite_name(), False, ORANGE)
        sprite_text_box = sprite_text.get_rect()
        sprite_text_box.midtop = sprite_rect.midbottom

        screen.blit(background, (0, 0))
        screen.blit(player_sprite, sprite_rect)
        screen.blit(title_text, title_text_box)
        screen.blit(sprite_text, sprite_text_box)
    ################################################################################################
    #   Initialization of variables for running game. all adjustments to the numbers of the game 
    #   should be made in this section.
    ################################################################################################  
    width = screen.get_width()
    height = screen.get_height()

    FPS = 30                                   #Only works when this is fairly low on raspberry pi
    BORDER_HEIGHT = int(screen.get_height() / 20)   #Width of the upper and lower border edges
    PLAYER_X = 25
    PLAYER_Y = screen.get_height() / 2         #Player starting Y
    PLAYER_RATIO = 6                           #Ratio of player Height to screen Height
    #Y_UPPER_LIMIT and Y_LOWER_LIMIT define the absolute boundaries that the player can fly to on
    #the y axis
    Y_UPPER_LIMIT = BORDER_HEIGHT
    Y_LOWER_LIMIT = screen.get_height()-BORDER_HEIGHT #will be adjusted based on the height of the player

    
    ################################################################################################
    #   Initialization of various non-variable type assets such as the game clock, the screen, 
    #   and the various image assets used
    ################################################################################################

    def find_sprite_name():
        nonlocal SPRITES, sprite_i
        sprite_name = str(SPRITES[sprite_i]).split(".", 1)
        sprite_name = sprite_name[0]
        sprite_name = re.split(r'[\\{+}|/{+}]', sprite_name)
        sprite_name = sprite_name[-1]
        return sprite_name

    #Initialize the background image
    background = pygame.image.load("./img/background_cave_blue.png").convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    BACKGROUND_WIDTH = screen.get_width()
    
    sprites_path = pathlib.Path("./img/sprites")
    SPRITES = [path for path in sprites_path.iterdir() if path.is_file()]
    sprite_i = 0
    
    player_sprite = pygame.image.load(SPRITES[sprite_i])
    scale = screen.get_height() / (PLAYER_RATIO * player_sprite.get_height())
    player_sprite = pygame.transform.rotozoom(player_sprite, 0, scale)

    sprite_rect = pygame.Rect(PLAYER_X, PLAYER_Y, player_sprite.get_width(), player_sprite.get_height())

    #Logic for running the game loop
    running = True
    frames = 0    
    QUIT = False
    
    WHITE = (255,255,255)
    ORANGE = (255,200,0)
    
    pygame.font.init()
    title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/12))
    sprite_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
    
    title_text = title_font.render("SELECT SPRITE", False, WHITE)
    title_text_box = title_text.get_rect()
    title_text_box.centerx = int(screen.get_width() / 2)
    title_text_box.bottom = int(screen.get_height() / 4)
    
    sprite_rect.midtop = title_text_box.midbottom
    
    sprite_text = sprite_font.render(find_sprite_name(), False, ORANGE)
    sprite_text_box = sprite_text.get_rect()
    sprite_text_box.midtop = sprite_rect.midbottom
    
    SPRITE = ""
    screen.fill("purple")
    screen.blit(background, (0, 0))
    screen.blit(player_sprite, sprite_rect)
    screen.blit(title_text, title_text_box)
    screen.blit(sprite_text, sprite_text_box)
    ################################################################################################
    #   Game Loop and Logic
    ################################################################################################
    #the background image loops, this tracks where we're at
    background_x = 0
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                QUIT = True
                SPRITE = ""
            if event.type == pygame.WINDOWRESIZED:
                resize_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    sprite_i = (sprite_i+1) % len(SPRITES)
                    player_sprite = pygame.image.load(SPRITES[sprite_i])
                    player_sprite = pygame.transform.rotozoom(player_sprite, 0, scale)
                    sprite_text = sprite_font.render(find_sprite_name(), False, ORANGE)
                    
                    screen.fill("purple")
                    screen.blit(background, (0, 0))
                    screen.blit(player_sprite, sprite_rect)
                    screen.blit(title_text, title_text_box)
                    screen.blit(sprite_text, sprite_text_box)
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    sprite_i = (sprite_i-1) % len(SPRITES)
                    player_sprite = pygame.image.load(SPRITES[sprite_i])
                    player_sprite = pygame.transform.rotozoom(player_sprite, 0, scale)
                    sprite_text = sprite_font.render(find_sprite_name(), False, ORANGE)
                    
                    screen.fill("purple")
                    screen.blit(background, (0, 0))
                    screen.blit(player_sprite, sprite_rect)
                    screen.blit(title_text, title_text_box)
                    screen.blit(sprite_text, sprite_text_box)
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    running = False
                    SPRITE = SPRITES[sprite_i]
                if event.key == pygame.K_ESCAPE:
                    running = False
                    QUIT = True
                    SPRITE = ""
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
                SPRITE = SPRITES[sprite_i]
                
        if running:
            frames += 1
        clock.tick(FPS)
    ### END OF GAME LOOP ########################################################################################
    return QUIT, SPRITE

#####################################################################################################################
#	This is for testing purposes so the game loop can be called from this file. In operation the game shouldn't be
#	called from here
#####################################################################################################################
import screeninfo
if __name__ == "__main__":
    for m in screeninfo.get_monitors():
        if m.is_primary:
            monitor = m
    
    WIDTH = int(monitor.width * 0.5)
    HEIGHT = int(monitor.height * 0.5)
    INITIAL_SIZE = (WIDTH,HEIGHT) #Initial Screen size
    FLAGS = pygame.DOUBLEBUF | pygame.RESIZABLE

    scrn = pygame.display.set_mode(INITIAL_SIZE, FLAGS, 8)
    clk = pygame.time.Clock()
    
    pygame.event.set_allowed([pygame.QUIT, pygame.WINDOWRESIZED])
    sprite_select(scrn, clk)
    pygame.display.quit()
  
