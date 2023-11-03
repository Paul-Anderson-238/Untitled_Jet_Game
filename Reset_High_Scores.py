########################################################
## Reset_High_Scores.py: Initializes and resets high score tables
########################################################
## Author: Paul Anderson
## Version: 1.1.0
## Status: Alpha Complete, Screen Scaling Added.
########################################################

import json

#################################################################################################
# WARNING: This file was created for testing and management purposes. Running this script will 
#          RESET ALL high scores. Make sure that is what you want to do before running this script 
#################################################################################################

def reset_high_scores():
    high_score_tables = {"Normal": "./high_scores/Normal_high_scores.json",
                         "Hard": "./high_scores/Hard_high_scores.json"}
    highscores = [("A. EARHART", 40000),
                  ("R. BARON", 35000),
                  ("C. LINDBERGH", 30000),
                  ("O. WRIGHT", 25000),
                  ("MAVERICK", 20000)]


    json_highscores = json.dumps(highscores, indent=4)
    for _, path in high_score_tables.items():
        with open(path, "w") as outfile:
            outfile.write(json_highscores)
    
if __name__ == "__main__":
    reset_high_scores()