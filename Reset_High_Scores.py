########################################################
## Reset_High_Scores.py: Initializes and resets high score tables
########################################################
## Author: Paul Anderson
## Version: 1.2.0
## Status: Effects for high scores updated, idle behavior implemented
########################################################

import json
###################################################################################################
# Takes file path and creates or resets the values for that score table
#   inputs:
#       path: the file path that stores the score
#   outputs:
###################################################################################################
def create_score_file(path):
    highscores = [("A A A", 500),
                  ("B B B", 400),
                  ("C C C", 300),
                  ("D D D", 200),
                  ("E E E", 100)]
    json_highscores = json.dumps(highscores, indent=4)
    with open(path, "w") as outfile:
        outfile.write(json_highscores)

#################################################################################################
# WARNING: This file was created for testing and management purposes. Running this script will 
#          RESET ALL high scores. Make sure that is what you want to do before running this script 
#   input:
#   output:
#################################################################################################
def reset_high_scores():
    high_score_tables = {"Easy": "./high_scores/Easy_high_scores.json",
                         "Normal": "./high_scores/Normal_high_scores.json",
                         "Hard": "./high_scores/Hard_high_scores.json"}
    for path in high_score_tables.values():
        create_score_file(path)

#################################################################################################
# Running this file as a script: This will reset the high scores. This may be desirable but be 
#                                be careful. 
#################################################################################################
if __name__ == "__main__":
    reset_high_scores()