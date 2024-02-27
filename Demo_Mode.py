########################################################
## Demo_Mode.py: Self Playing Demo mode. Replaces old Video based demo
########################################################
## Author: Paul Anderson
## Version: 2.0.0
## Status: Modified Run_Game to conrol it's own movement logic as a demo during idle time.
########################################################

import pygame
import Points
from Collision import collide_rect_polygon
from math import ceil
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
def demo_mode(screen, clock, SPRITE):
    
    def resize_game():
        nonlocal width, height, screen, BASE_OBJECT_SPEED, OBJECT_SPEED, SPEED_MULTIPLIER, BORDER_HEIGHT
        nonlocal Y_UPPER_LIMIT, Y_LOWER_LIMIT, BACKGROUND_WIDTH, background, player, PLAYER_Y
        BASE_OBJECT_SPEED = screen.get_width() / 195
        OBJECT_SPEED = int(BASE_OBJECT_SPEED * 3 * SPEED_MULTIPLIER)
        BORDER_HEIGHT = int(screen.get_height() / 20)
        Y_UPPER_LIMIT = BORDER_HEIGHT
        Y_LOWER_LIMIT = screen.get_height()-BORDER_HEIGHT
        BACKGROUND_WIDTH = screen.get_width()
        background = pygame.transform.smoothscale(background, screen.get_size())
       
        x_scale = screen.get_width()/width
        y_scale = screen.get_height()/height
        width = screen.get_width()
        height = screen.get_height()

        player.resize(x_scale, y_scale)
        Y_LOWER_LIMIT -= player.rectangle.h
        points.resize(x_scale, y_scale, width, height, Y_UPPER_LIMIT, Y_LOWER_LIMIT+player.rectangle.h)

        PLAYER_Y = int(PLAYER_Y * y_scale)
    ################################################################################################
    #   Initialization of variables for running game. all adjustments to the numbers of the game 
    #   should be made in this section.
    ################################################################################################
    BASE_OBJECT_SPEED = screen.get_width() / 195      #How Quickly the Background Scrolls and how fast obstacles move
    OBJECT_SPEED = BASE_OBJECT_SPEED * 3
    SPEED_MULTIPLIER = 1.0                     #A Scaling Multiplier to make the game more difficult as it goes.
    
    width = screen.get_width()
    height = screen.get_height()

    FPS = 30                                   #Only works when this is fairly low on raspberry pi
    BORDER_HEIGHT = int(screen.get_height() / 20)   #Width of the upper and lower border edges
    PLAYER_X = 25
    PLAYER_Y = screen.get_height() / 2         #Player starting Y
    PLAYER_RATIO = 10                          #Ratio of player Height to screen Height
    
    EXPLOSION_RATIO = 8

    #Y_UPPER_LIMIT and Y_LOWER_LIMIT define the absolute boundaries that the player can fly to on
    #the y axis
    Y_UPPER_LIMIT = BORDER_HEIGHT
    Y_LOWER_LIMIT = screen.get_height()-BORDER_HEIGHT #will be adjusted based on the height of the player
    
    #A measure of how wide the gaps between top and bottom will be. Given as ratios of screen height
    GAP_MIN = 0.35 
    GAP_MAX = 0.50
    
    #These variables measure the distance on the y axis between designated gaps. given as a range
    #for some variability given as ratios of screen height
    DISTANCE_MIN = 0.1
    DISTANCE_MAX = 0.125
    
    ################################################################################################
    #   Initialization of various non-variable type assets such as the game clock, the screen, 
    #   and the various image assets used
    ################################################################################################

    #Initialize the background image
    background = pygame.image.load("./img/background_cave_blue.png").convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    BACKGROUND_WIDTH = screen.get_width()

    ####################################################################################################
    #A helper class to hold the player img, location, and hitbox
    #	inputs:
    #		img: the sprite of the player object.
    ####################################################################################################
    class Player:
        def __init__(self, img):
            self.img = img
            self.img_up = pygame.transform.rotozoom(self.img, 10, 1.0)
            self.img_down = pygame.transform.rotozoom(self.img,-10, 1.0)
            self.rectangle = pygame.Rect(PLAYER_X, PLAYER_Y, self.img.get_width(), self.img.get_height())
            self.collide_rectangle = pygame.Rect(PLAYER_X, PLAYER_Y, self.rectangle.w *0.4, self.rectangle.h * 0.2)
            self.collide_rectangle.center = self.rectangle.center
        def move(self, y):
            self.rectangle = self.rectangle.move(0, y)
            self.collide_rectangle.center = self.rectangle.center
        def sprite_straight(self):
            return self.img
        def sprite_up(self):
            return self.img_up
        def sprite_down(self):
            return self.img_down
        def get_rectangle(self):
            return self.rectangle
        def get_collide_rectangle(self):
            return self.collide_rectangle
        def resize(self, x_scale, y_scale):
            nonlocal PLAYER_RATIO, SPRITE
            player_sprite = pygame.image.load(SPRITE).convert_alpha()
            scale = screen.get_height() / (PLAYER_RATIO * player_sprite.get_height())
            player_sprite = pygame.transform.rotozoom(player_sprite, 0, scale)
            self.img = player_sprite
            self.img_up = pygame.transform.rotozoom(self.img, 10, 1.0)
            self.img_down = pygame.transform.rotozoom(self.img,-10, 1.0)

            self.rectangle.x = self.rectangle.x * x_scale
            self.rectangle.y = self.rectangle.y * y_scale
            self.rectangle.h = self.rectangle.h * y_scale
            self.rectangle.w = self.rectangle.w * x_scale
            self.collide_rectangle = pygame.Rect(PLAYER_X, PLAYER_Y, self.rectangle.w *0.4, self.rectangle.h * 0.2)
            self.collide_rectangle.center = self.rectangle.center
    
    #initialize the Player Sprite
    player_sprite = pygame.image.load(SPRITE).convert_alpha()
    
    #generates a percentage to scale the player image based on a ratio to screen size
    scale = screen.get_height() / (PLAYER_RATIO * player_sprite.get_height())
    player_sprite = pygame.transform.rotozoom(player_sprite, 0, scale)
    
    #player object that contains the player sprite and rectangle for collisions
    player = Player(player_sprite)
    
    #Adjust lower limit so the player sprite stops at the lower limit and doesnt go through
    Y_LOWER_LIMIT -= player.rectangle.h 

    #Custom data type to keep track of the y points of the upper and lower boudaries. 
    points = Points.Points(screen.get_width(), screen.get_height(), Y_UPPER_LIMIT, Y_LOWER_LIMIT+player.rectangle.h,
                           GAP_MIN, GAP_MAX, DISTANCE_MIN, DISTANCE_MAX, True)

    #Logic for running the game loop
    running = True
    frames = 0    
    moving_down = False
    moving_up = False
    PLAYER_SPEED = 0
    AWAKE = False
    QUIT = False
    ################################################################################################
    #   Game Loop and Logic
    ################################################################################################
    #the background image loops, this tracks where we're at
    background_x = 0
    while running and not AWAKE:
        screen.fill("purple") #Used to wipe away anything drawn last loop, making visuals smoother
        
        #Scroll the Background
        background_x -= int(BASE_OBJECT_SPEED)
        if background_x <= -BACKGROUND_WIDTH:
            background_x = 0
        
        #logic to keep the background scrolling
        screen.blit(background, (background_x, 0))
        screen.blit(background, (background_x + BACKGROUND_WIDTH, 0))
        
        if frames < 300:
            top_target = points.y_points[1].get_top_y()
            bottom_target = points.y_points[1].get_bottom_y()
            mid_y = (top_target + bottom_target) // 2
            dis = ceil((points.y_points[1].get_x() - (PLAYER_X + player.collide_rectangle.width)) / OBJECT_SPEED)
            if dis == 0:
                PLAYER_SPEED = 0
            else:
                PLAYER_SPEED = (mid_y-PLAYER_Y)//dis
            if PLAYER_SPEED < 0:
                moving_up = True
                moving_down = False
            elif PLAYER_SPEED > 0:
                moving_up = False
                moving_down = True
            else:
                moving_up = moving_down = False
        if frames == 300:
            PLAYER_SPEED = 0
            moving_up = moving_down = False

        #Move the Sprite
        PLAYER_Y += PLAYER_SPEED
        player.move(PLAYER_SPEED)

        if running:
            if moving_up:
                screen.blit(player.sprite_up(), player.get_rectangle())
            elif moving_down:
                screen.blit(player.sprite_down(), player.get_rectangle())
            else:
                screen.blit(player.sprite_straight(), player.get_rectangle())
            
            points.update_points(OBJECT_SPEED)
            top_points = [(0,0)] + points.get_top_points() + [(screen.get_width(), 0)]
            bottom_points = [(0, screen.get_height())] + points.get_bottom_points() + [(screen.get_width(), screen.get_height())]
            pygame.draw.polygon(screen, (0,0,0), top_points)
            pygame.draw.polygon(screen, (0,0,0), bottom_points)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    AWAKE = True
                    QUIT = True
                if event.type == pygame.WINDOWRESIZED:
                    resize_game()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    AWAKE = True
            
            player_rect = player.get_collide_rectangle()
            if collide_rect_polygon(player_rect, bottom_points) or collide_rect_polygon(player_rect, top_points):
                running = False
            if running:
                frames += 1
            clock.tick(FPS)
    ### END OF GAME LOOP ########################################################################################

    ##########################################################################################
    # the frames for the player object explosion
    ##########################################################################################
    explosion1 = pygame.image.load("./img/explosion_frame_1.png").convert_alpha()
    explosion2 = pygame.image.load("./img/explosion_frame_2.png").convert_alpha()
    explosion3 = pygame.image.load("./img/explosion_frame_3.png").convert_alpha()
    explosion4 = pygame.image.load("./img/explosion_frame_4.png").convert_alpha()
    scale = screen.get_height() / (EXPLOSION_RATIO * explosion1.get_height())
    explosion1 = pygame.transform.rotozoom(explosion1, 0, scale)
    scale = screen.get_height() / (EXPLOSION_RATIO * explosion2.get_height())
    explosion2 = pygame.transform.rotozoom(explosion2, 0, scale)
    scale = screen.get_height() / (EXPLOSION_RATIO * explosion3.get_height())
    explosion3 = pygame.transform.rotozoom(explosion3, 0, scale)
    scale = screen.get_height() / (EXPLOSION_RATIO * explosion4.get_height())
    explosion4 = pygame.transform.rotozoom(explosion4, 0, scale)
    
    explosions = [explosion1, explosion2, explosion3, explosion4]
    explosion_i = 0
    
    #####Loop to display the explosion frames to the screen
    frames = 0
    while frames < 90 and not AWAKE:
        screen.fill("purple") 
        
        #background stays where it's at
        screen.blit(background, (background_x, 0))
        screen.blit(background, (background_x + BACKGROUND_WIDTH, 0))
        
        if explosion_i < 4:
            screen.blit(explosions[explosion_i], player.get_rectangle())
            if frames % 5 == 0:
                explosion_i += 1
        
        top_points = [(0,0)] + points.get_top_points() + [(screen.get_width(), 0)]
        bottom_points = [(0, screen.get_height())] + points.get_bottom_points() + [(screen.get_width(), screen.get_height())]
        pygame.draw.polygon(screen, (0,0,0), top_points)
        pygame.draw.polygon(screen, (0,0,0), bottom_points)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                AWAKE = True
                QUIT = True
            if event.type == pygame.WINDOWRESIZED:
                resize_game()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                AWAKE = True
        
        pygame.display.update()
        frames += 1
        clock.tick(30)
        ###End of Explosion Loop
    
    return AWAKE, QUIT

#####################################################################################################################
#	This is for testing purposes so the game loop can be called from this file. In operation the game shouldn't be
#	called from here
#####################################################################################################################
import screeninfo
if __name__ == "__main__":
    from random import choice
    import pathlib
    
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
    
    sprites_path = pathlib.Path("./img/sprites")
    SPRITES = [path for path in sprites_path.iterdir() if path.is_file()]
    
    demo_mode(scrn, clk, choice(SPRITES))
    pygame.display.quit()
  
