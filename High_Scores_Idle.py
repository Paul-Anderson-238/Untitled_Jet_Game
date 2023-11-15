########################################################
## Display_High_Scores.py: Controls the High Score game state
########################################################
## Author: Paul Anderson
## Version: 1.2.0
## Effects for high scores updated, idle behavior implemented
########################################################

import json
import pygame
from os.path import exists
from Reset_High_Scores import create_score_file
############################################################################################################
#The function called from main to display the high scores
#	inputs:
#		screen: the screen object to display to.
#		clock: the game clock so we can update and change what's on the screen.
#	outputs:
#		QUIT: a boolean that indicates if the player decided to quit while on this state. 
#       AWAKE: a boolean that lets calling function know if player input awoke the program.
############################################################################################################
def high_scores_idle(screen, clock):  
    ############################################################################################################
    #A function to control the resizing logic should the player resize the window. Resizes all elements that 
    #appear on the screen according to ratios that have already been calculated.
    #	inputs:
    #	outputs:
    ############################################################################################################
    def resize_high_scores():
        nonlocal y_divs, x_divs, font, title_font, background, highscore_text_box, texts, highscores
        y_divs = screen.get_height()/8
        x_divs= screen.get_width()/4
        title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/16))
        font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
        background = pygame.transform.smoothscale(background, screen.get_size())
        
        texts = []

        highscore_text = title_font.render("HIGHSCORES", False, WHITE)
        highscore_text_box = highscore_text.get_rect()
        highscore_text_box.centerx = screen.get_width()/2
        highscore_text_box.bottom = y_divs
        texts.append((highscore_text, highscore_text_box))

        for i in range(len(highscores)):
            title = title_font.render(highscores[i][0], False, WHITE)
            title_box = title.get_rect()
            title_box.centerx = (x_divs * (i+1))
            title_box.bottom = y_divs * 2
            texts.append((title, title_box))
            for j in range(len(highscores[i][1])):
                texts.append(generate_score_text((x_divs * (i+1)), (y_divs * (j + 3)), highscores[i][1][j], WHITE))
    

    
    high_score_tables = {"Easy": "./high_scores/Easy_high_scores.json",
                         "Normal": "./high_scores/Normal_high_scores.json",
                         "Hard": "./high_scores/Hard_high_scores.json"} 

    #Prep the background image
    background = pygame.image.load("./img/background_cave_blue.png").convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    
    #initialize the fonts we're using
    pygame.font.init()
    title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/16))
    font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
    
    #######################################################################################################
    # Helper function to create a text box object
    #	Inputs:
    #		i: position in the highscores list the score text is located
    #		color: the RGB tuple of the desired color of the text
    #	Output:
    #		Tuple: The first is the text object, the second is the text box for position on screen
    #	Notes:
    #		This function relies on the previously stated font object and highscores table so this function
    #		has limited portablility
    #######################################################################################################
    def generate_score_text(x_cent, y_bot, score, color):
        score_text = font.render(score[0] + ":   " + str(score[1]), False, color)
        score_text_box = score_text.get_rect()
        score_text_box.centerx = x_cent
        score_text_box.bottom = y_bot
        return(score_text, score_text_box)
    
    WHITE = (255,255,255) #Define the Color white for the text
    
    #Write the top 5 high scores to the screen
    y_divs = screen.get_height()/8
    x_divs = screen.get_width()/4
    
    texts = []
    highscore_text = title_font.render("HIGHSCORES", False, WHITE)
    highscore_text_box = highscore_text.get_rect()
    highscore_text_box.centerx = screen.get_width()/2
    highscore_text_box.bottom = y_divs
    texts.append((highscore_text, highscore_text_box))
    
    highscores = []

    for key in high_score_tables.keys():
        path = high_score_tables[key]
        if not exists(path):
            create_score_file(path)
        with open(path, "r") as openfile:
            highscore = json.load(openfile)
        highscores.append((key, highscore))

    for i in range(len(highscores)):
        title = title_font.render(highscores[i][0], False, WHITE)
        title_box = title.get_rect()
        title_box.centerx = (x_divs * (i+1))
        title_box.bottom = y_divs * 2
        texts.append((title, title_box))
        for j in range(len(highscores[i][1])):
            texts.append(generate_score_text((x_divs * (i+1)), (y_divs * (j + 3)), highscores[i][1][j], WHITE))
    
    frames = 0
    RUN_HIGHSCORE = True

    delay_frames = 1000000000

    ready = False
    alpha = 0
    for text in texts:
        text[0].set_alpha(alpha)

    QUIT = False
    AWAKE = False
    while RUN_HIGHSCORE and not QUIT and not AWAKE:
        screen.fill("purple")
        screen.blit(background, (0,0))
        if not ready:
            alpha += 5
            if alpha >= 255:
                alpha = 255
                ready = True
                delay_frames = frames + 300
            for text in texts:
                text[0].set_alpha(alpha)

        for text in texts:
            screen.blit(text[0], text[1])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QUIT = True
            if event.type == pygame.WINDOWRESIZED:
                resize_high_scores()
            #Exit screen early at any key press
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                AWAKE = True
        
        frames += 1
        #At FPS of 15, we'll stay on this screen for 8 seconds before automatically cycling to the main menu
        if delay_frames == frames:
            RUN_HIGHSCORE = False
        pygame.display.update()
        clock.tick(30)
    ### End of Highscore display loop
    return QUIT

#################################################################################################
# Running this file as a script: If running this file as a script, it will test the function with 
#                                test values. Feel free to tweak and test from here. 
#################################################################################################
import screeninfo
if __name__ == "__main__":
    for m in screeninfo.get_monitors():
        if m.is_primary:
            monitor = m

    INITIAL_SIZE = (int(monitor.width * 0.8), int(monitor.height * 0.8)) #Initial Screen size
    
    scrn = pygame.display.set_mode(INITIAL_SIZE, pygame.RESIZABLE)
    clk = pygame.time.Clock()
    
    high_scores_idle(scrn, clk)
    pygame.display.quit()
    