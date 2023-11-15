########################################################
## Run_Game.py: Runs the game loop
########################################################
## Author: Paul Anderson
## Version: 1.2.0
## Status: Effects for high scores updated, idle behavior implemented
########################################################

import pygame
import Points
from Collision import collide_rect_polygon
####################################################################################################
#Controls the normal operation of the game. There are 2 main divisions in this function:the init of  
#variables and objects, and the game loop and logic.
#	inputs:
#		screen: the screen object to display to.
#		clock: the game clock necessary to update the screen.
#		difficulty: a key that gets running data from the levels dict to init game difficulty.
#	outputs:
#		QUIT: a boolean flag that lets the calling function know if the player opted to quit the game.
#		score: the score the player got to this round. In the case of the player quitting, returns 0.
####################################################################################################
def run_game(screen, clock, difficulty):
    
    def resize_game():
        nonlocal width, height, screen, PLAYER_SPEED, OBJECT_SPEED, BORDER_HEIGHT, Y_UPPER_LIMIT, Y_LOWER_LIMIT
        nonlocal BACKGROUND_WIDTH, background, player, font, text, text_box, PLAYER_Y
        PLAYER_SPEED = screen.get_height() / 75
        OBJECT_SPEED = screen.get_width() / 65
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
        
        font = pygame.font.SysFont(pygame.font.get_default_font(), BORDER_HEIGHT)
        text = font.render('Score: ' + str(frames*29).zfill(8), False, (255,255,255))
        text_box = text.get_rect()
        text_box.right = screen.get_width()
        text_box.bottom = BORDER_HEIGHT
        PLAYER_Y = int(PLAYER_Y * y_scale)

    ################################################################################################
    #   Initialization of variables for running game. all adjustments to the numbers of the game 
    #   should be made in this section.
    ################################################################################################
    levels = {"Easy": [0.25, 0.55, 0.075, 0.175, 0.0175], #GAP_MIN, GAP_MAX, DISTANCE_MIN, DISTANCE_MAX, MULTILIER_GROWTH_RATE
              "Normal": [0.25, 0.5, 0.1, 0.175, 0.025],
              "Hard": [0.25, 0.45, 0.1, 0.2, 0.0325]}
    
    PLAYER_SPEED = screen.get_height() / 75    #How Quickly the Player can move up and down
    OBJECT_SPEED = screen.get_width() / 65     #How Quickly the Background Scrolls and how fast obstacles move
    SPEED_MULTIPLIER = 1.0                     #A Scaling Multiplier to make the game more difficult as it goes.
    
    width = screen.get_width()
    height = screen.get_height()

    FPS = 30                                   #Only works when this is fairly low on raspberry pi
    BORDER_HEIGHT = int(screen.get_height() / 20)   #Width of the upper and lower border edges
    PLAYER_X = 25
    PLAYER_Y = screen.get_height() / 2         #Player starting Y
    PLAYER_RATIO = 12                          #Ratio of player Height to screen Height
    
    EXPLOSION_RATIO = 8
    
    SCORE_MULTIPLIER = 29                      #SCORE = SCORE_MULTIPLIER * frames
    MULTIPLIER_GROWTH_RATE = levels[difficulty][4]
    SCORE = 0                                  #Variable to hold current score
    
    #Y_UPPER_LIMIT and Y_LOWER_LIMIT define the absolute boundaries that the player can fly to on
    #the y axis
    Y_UPPER_LIMIT = BORDER_HEIGHT
    Y_LOWER_LIMIT = screen.get_height()-BORDER_HEIGHT #will be adjusted based on the height of the player
    
    #A measure of how wide the gaps between top and bottom will be. Given as ratios of screen height
    GAP_MIN = levels[difficulty][0]   
    GAP_MAX = levels[difficulty][1]
    
    #These variables measure the distance on the y axis between designated gaps. given as a range
    #for some variability given as ratios of screen height
    DISTANCE_MIN = levels[difficulty][2]
    DISTANCE_MAX = levels[difficulty][3]

    #Logic for running the game loop
    running = True
    frames = 0    
    
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
            nonlocal PLAYER_RATIO
            player_sprite = pygame.image.load("./img/pixel_fighter.png").convert_alpha()
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
    player_sprite = pygame.image.load("./img/pixel_fighter.png").convert_alpha()
    
    #generates a percentage to scale the player image based on a ratio to screen size
    scale = screen.get_height() / (PLAYER_RATIO * player_sprite.get_height())
    player_sprite = pygame.transform.rotozoom(player_sprite, 0, scale)
    
    #player object that contains the player sprite and rectangle for collisions
    player = Player(player_sprite)
    
    #Adjust lower limit so the player sprite stops at the lower limit and doesnt go through
    Y_LOWER_LIMIT -= player.rectangle.h 

    #Custom data type to keep track of the y points of the upper and lower boudaries. 
    points = Points.Points(screen.get_width(), screen.get_height(), Y_UPPER_LIMIT, Y_LOWER_LIMIT+player.rectangle.h,
                           GAP_MIN, GAP_MAX, DISTANCE_MIN, DISTANCE_MAX)
    
    pygame.font.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), BORDER_HEIGHT)
    
    text = font.render('Score: ' + str(frames*29).zfill(8), False, (255,255,255))
    text_box = text.get_rect()
    text_box.right = screen.get_width()
    text_box.bottom = BORDER_HEIGHT

    ################################################################################################
    #   Game Loop and Logic 
    #  
    ################################################################################################
    #the background image loops, this tracks where we're at
    background_x = 0
    while running:
        screen.fill("purple") #Used to wipe away anything drawn last loop, making visuals smoother
        
        #Scroll the Background
        background_x -= int(OBJECT_SPEED * SPEED_MULTIPLIER)
        if background_x <= -BACKGROUND_WIDTH:
            background_x = 0
        
        #logic to keep the background scrolling
        screen.blit(background, (background_x - BACKGROUND_WIDTH, 0))
        screen.blit(background, (background_x, 0))
        screen.blit(background, (background_x + BACKGROUND_WIDTH, 0))
    
        moving_down = False
        moving_up = False
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            if PLAYER_Y < Y_LOWER_LIMIT:
                moving_down = True
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            if PLAYER_Y > Y_UPPER_LIMIT:
                moving_up = True
        if pressed[pygame.K_ESCAPE]:
            running = False
            return True, 0
            
        #Logic of moving the player Jet
        if moving_down and moving_up:
            moving_up = moving_down = False
        elif moving_down:
            PLAYER_Y += int(PLAYER_SPEED * SPEED_MULTIPLIER)
            player_movement = int(PLAYER_SPEED * SPEED_MULTIPLIER)
            if PLAYER_Y > Y_LOWER_LIMIT:
                player_movement = int(PLAYER_SPEED * SPEED_MULTIPLIER) - (PLAYER_Y-Y_LOWER_LIMIT)
                PLAYER_Y = Y_LOWER_LIMIT
            player.move(player_movement)
        
        elif moving_up:
            PLAYER_Y -= int(PLAYER_SPEED * SPEED_MULTIPLIER)
            player_movement = -int(PLAYER_SPEED * SPEED_MULTIPLIER)
            if PLAYER_Y < Y_UPPER_LIMIT:
                player_movement = -(int(PLAYER_SPEED * SPEED_MULTIPLIER) - (Y_UPPER_LIMIT - PLAYER_Y))
                PLAYER_Y = Y_UPPER_LIMIT
            player.move(player_movement)
        
        if running:
            if moving_up:
                screen.blit(player.sprite_up(), player.get_rectangle())
            elif moving_down:
                screen.blit(player.sprite_down(), player.get_rectangle())
            else:
                screen.blit(player.sprite_straight(), player.get_rectangle())
            
            points.update_points(int(OBJECT_SPEED * SPEED_MULTIPLIER))
            top_points = [(0,0)] + points.get_top_points() + [(screen.get_width(), 0)]
            bottom_points = [(0, screen.get_height())] + points.get_bottom_points() + [(screen.get_width(), screen.get_height())]
            pygame.draw.polygon(screen, (0,0,0), top_points)
            pygame.draw.polygon(screen, (0,0,0), bottom_points)
            
            text = font.render('Score: ' + str(frames*29).zfill(8), False, (255,255,255))
            screen.blit(text,text_box)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return True, 0
                if event.type == pygame.WINDOWRESIZED:
                    resize_game()
            
            player_rect = player.get_collide_rectangle()
            if collide_rect_polygon(player_rect, bottom_points) or collide_rect_polygon(player_rect, top_points):
                running = False
            if running:
                SCORE += SCORE_MULTIPLIER
                frames += 1
                if frames % 100 == 0:
                    SPEED_MULTIPLIER += MULTIPLIER_GROWTH_RATE
            
            clock.tick(FPS)
    ### END OF GAME LOOP ########################################################################################
    
    score = frames * SCORE_MULTIPLIER
    #A logic check making sure that the score was calculated correctly
    if score != SCORE:
        SCORE = score
        
    text = font.render('Score: ' + str(SCORE).zfill(8), False, (255,255,255))

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
    while frames < 60:
        screen.fill("purple") 
        
        #background stays where it's at
        screen.blit(background, (background_x - BACKGROUND_WIDTH, 0))
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
        
        screen.blit(text, text_box)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return True, 0
            if event.type == pygame.WINDOWRESIZED:
                resize_game()
        
        pygame.display.update()
        frames += 1
        clock.tick(30)
        ###End of Explosion Loop
    
    return False, score

#####################################################################################################################
#	This is for testing purposes so the game loop can be called from this file. In operation the game shouldn't be
#	called from here
#####################################################################################################################
import screeninfo
if __name__ == "__main__":
    for m in screeninfo.get_monitors():
        if m.is_primary:
            monitor = m
    
    WIDTH = int(monitor.width * 0.8)
    HEIGHT = int(monitor.height * 0.8)
    INITIAL_SIZE = (WIDTH,HEIGHT) #Initial Screen size

    scrn = pygame.display.set_mode(INITIAL_SIZE, pygame.RESIZABLE)
    clk = pygame.time.Clock()
    run_game(scrn, clk, "Easy")
    pygame.display.quit()
  