########################################################
## Display_High_Scores.py: Controls the High Score game state
########################################################
## Author: Paul Anderson
## Version: 1.1.0
## Alpha Complete, Screen Scaling Added.
########################################################

import json
import pygame

############################################################################################################
#A helper function that will update the scoreboard both in the storage json file and locally
#	inputs:
#		screen: the screen object to display to.
#		clock: the clock object so we can update what is being displayed.
#		path: the file path to the correct high score JSON.
#		scoreboard: the list of high scores and names.
#		score: the new score to add to the list.
#	outputs:
#		scoreboard: the updated list of high scores
############################################################################################################
def add_score(screen, clock, path, scoreboard, score):

    def resize_score():
        nonlocal background, title_font, font, congrats_text_box, prompt_text_box
        title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/16))
        font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
        background = pygame.transform.smoothscale(background, screen.get_size())
        congrats_text_box.centerx = int(screen.get_width() / 2) 
        congrats_text_box.bottom = int(screen.get_height() / 3)
        anchor = congrats_text_box.midbottom
        anchor = (anchor[0], anchor[1]+20)
        prompt_text_box.midtop = anchor

    background = pygame.image.load("./img/background_cave_blue.png").convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    
    pygame.font.init()
    title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/16))
    font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
    
    #Generate the text objects and position them
    WHITE = (255,255,255)
    name = ""
    congrats_text = title_font.render("HIGHSCORE!!!", False, WHITE)
    congrats_text_box = congrats_text.get_rect()
    congrats_text_box.centerx = int(screen.get_width() / 2) 
    congrats_text_box.bottom = int(screen.get_height() / 3)
    #text.append(congrats_text, congrats_text_box)
    prompt_text = font.render("Enter Name: " + name, False, WHITE)
    prompt_text_box = prompt_text.get_rect()
    anchor = congrats_text_box.midbottom
    anchor = (anchor[0], anchor[1]+20)
    prompt_text_box.midtop = anchor

    #Loop to display text to the screen
    RUN_PROMPT = True
    while RUN_PROMPT:
        screen.fill("purple")
        congrats_text = title_font.render("HIGHSCORE!!!", False, WHITE)
        prompt_text = font.render("Enter Name: " + name, False, WHITE) #update the text on screen
        screen.blit(background, (0,0))
        screen.blit(congrats_text, congrats_text_box)
        screen.blit(prompt_text, prompt_text_box)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN_PROMPT = False
                return True, scoreboard, name
            if event.type == pygame.WINDOWRESIZED:
                resize_score()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True, scoreboard, name
                if (pygame.K_a <= event.key <= pygame.K_z):
                    char = chr(event.key - 32)
                    name += char
                if (event.key == pygame.K_PERIOD) or event.key == pygame.K_SPACE:
                    char = chr(event.key)
                    name += char
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                if event.key == pygame.K_RETURN:
                    if name != "":
                        RUN_PROMPT = False
        pygame.display.update()
        clock.tick(15)
    ### End of Loop 
 
    #Update the scoreboard
    scoreboard += [[name, score]]
    scoreboard = sorted(scoreboard, key=lambda score: score[1], reverse=True)
    del(scoreboard[len(scoreboard)-1])
    
    #Update the Scoreboard in Storage
    json_highscores = json.dumps(scoreboard, indent=4)
    with open(path, "w") as outfile:
        outfile.write(json_highscores)
    return False, scoreboard, name

############################################################################################################
#The function called from main to display the high scores
#	inputs:
#		screen: the screen object to display to.
#		clock: the game clock so we can update and change what's on the screen.
#		new_score: the score from the player's last game. It will be checked to see if it goes into the high score
#		difficulty: the difficulty level the player played. Used to access the correct scoreboard.
#	outputs:
#		QUIT: a boolean that indicates if the player decided to quit while on this state. 
############################################################################################################
def display_high_scores(screen, clock, new_score, difficulty):
    
    def resize_high_scores():
        nonlocal divs, cent, font, title_font, background, highscore_text_box, texts
        divs = screen.get_height()/7
        cent = screen.get_width()/2
        title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/16))
        font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
        background = pygame.transform.smoothscale(background, screen.get_size())
        
        highscore_text_box.centerx = cent
        highscore_text_box.bottom = divs
        first = True
        i = 0
        new_texts = []
        for text in texts:
            if first:
                new_text = title_font.render("HIGHSCORES", False, WHITE)
                new_rect = new_text.get_rect()
                new_rect.centerx = cent
                new_rect.bottom = divs
                new_texts.append((new_text, new_rect))
                first = False
                continue
            new_texts.append(generate_text(i,WHITE))
            i += 1
        texts = new_texts
    
    high_score_tables = {"Normal": "./high_scores/Normal_high_scores.json",
                         "Hard": "./high_scores/Hard_high_scores.json"} 
    
    with open(high_score_tables[difficulty], "r") as openfile:
        highscores = json.load(openfile)
    
    #Find the minimum score in the high scores, then test to see if current score makes the cut 
    score = 100000000000
    min_i = 0
    i = 0
    for _, value in highscores:
        if value < score:
            score = value
            min_i = i
        i += 1
    
    QUIT = False #A boolean flag indicating if the user has pressed the escape key to quit
    
    NEW_HIGHSCORE = False
    highscore_name = ""
    #Did the new score make the cut to be put in the highscore table?
    if highscores[min_i][1] < new_score:
        QUIT, highscores, highscore_name = add_score(screen, clock, high_score_tables[difficulty], highscores, new_score)
        NEW_HIGHSCORE = True
    
    #Prep the background image
    background = pygame.image.load("./img/background_cave_blue.png").convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    
    #initialize the fonts we're using
    pygame.font.init()
    title_font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/16))
    font = pygame.font.SysFont(pygame.font.get_default_font(), int(screen.get_height()/20))
    
    WHITE = (255,255,255) #Define the Color white for the text
    ORANGE = (255,200,0)  #Define the Color orange for displaying texts
    
    #Write the top 5 high scores to the screen
    divs = screen.get_height()/7
    cent = screen.get_width()/2
    
    texts = []
    highscore_text = title_font.render("HIGHSCORES", False, WHITE)
    highscore_text_box = highscore_text.get_rect()
    highscore_text_box.centerx = cent
    highscore_text_box.bottom = divs
    texts.append((highscore_text, highscore_text_box))
    
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
    def generate_text(i, color):
        score_text = font.render(highscores[i][0] + ":   " + str(highscores[i][1]), False, color)
        score_text_box = score_text.get_rect()
        score_text_box.centerx = cent
        score_text_box.bottom = divs * (i+2)
        return(score_text, score_text_box)
    
    new_score_i = 0
    for i in range(len(highscores)):
        #####NOTE: This logic has a small bug. In the case that the new score and name exactly matches the name
        #####      and score of an existing entry of the scoreboard, both scores will be colored Orange and only the second will flash.
        #####      Since score is based on the number of frames run, this bug should be extremely unlikely to occur   
        if highscores[i][1] == new_score and highscore_name == highscores[i][0]:
            texts.append(generate_text(i, ORANGE))
            new_score_i = i+1
        else:
            texts.append(generate_text(i, WHITE))
    
    #The loop for displaying the high scores
    color_i = 0
    COLOR_LOOP = [WHITE, ORANGE]
    frames = 0
    RUN_HIGHSCORE = True
    while RUN_HIGHSCORE and not QUIT:
        #We want a slight flashing effect for their current attempt's high score
        if frames % 15 == 0 and NEW_HIGHSCORE:
            texts[new_score_i] = generate_text(new_score_i-1, COLOR_LOOP[color_i])
            color_i = (color_i + 1)%len(COLOR_LOOP)
        
        screen.blit(background, (0,0))
        for text in texts:
            screen.blit(text[0], text[1])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QUIT = True
            if event.type == pygame.WINDOWRESIZED:
                resize_high_scores()
            #Exit screen early at any key press
            if event.type == pygame.KEYDOWN: 
               RUN_HIGHSCORE = False
        
        frames += 1
        #At FPS of 15, we'll stay on this screen for 8 seconds before automatically cycling to the main menu
        if frames == 120:
            RUN_HIGHSCORE = False
        pygame.display.update()
        clock.tick(15)
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
    
    display_high_scores(scrn, clk, 49000, "Normal")
    pygame.display.quit()
    