########################################################
## Collision.py: Functions for detecting collision in game
########################################################
## Author: Paul Anderson
## Version: 2.0.0
## Status: No major changes to collision detection. Adjustments in other Areas
########################################################

import pygame
############################################################################################################
#A helper function that will detect if there's a collision between 2 lines
#	inputs:
#		l1_p1: point 1 of line 1
#		l1_p2: point 2 of line 1
#		l2_p1: point 1 of line 2
#		l2_p2: point 2 of line 2
#	outputs:
#		COLLISION: boolean value indicating whether or not there was a collision
############################################################################################################
def collideLineLine(l1_p1, l1_p2, l2_p1, l2_p2):
    #normalized direction of the lines and start of the lines
    P = pygame.math.Vector2(*l1_p1)
    line1_vec = pygame.math.Vector2(*l1_p2)-P
    R = line1_vec.normalize()
    Q = pygame.math.Vector2(*l2_p1)
    line2_vec = pygame.math.Vector2(*l2_p2)-Q
    S = line2_vec.normalize()
    
    #normal vectors to the lines
    RNV = pygame.math.Vector2(R[1], -R[0])
    SNV = pygame.math.Vector2(S[1], -S[0])
    RdotSVN = R.dot(SNV)
    if RdotSVN == 0:
        return False
    
    #distance to the intersection point
    QP = Q-P
    t = QP.dot(SNV) / RdotSVN
    u = QP.dot(RNV) / RdotSVN
    
    return t > 0 and u > 0 and t*t < line1_vec.magnitude_squared() and u*u < line2_vec.magnitude_squared()

############################################################################################################
#A helper function that will detect if there's a collision between a line and a rectangle
#	inputs:
#		rect: a pygame rectangle object consisting of 4 points
#       p1: point 1 of the line we are checking collision on
#       p2: point 2 of the line we are checking collision on
#	outputs:
#		COLLISION: boolean value indicating whether or not there was a collision
############################################################################################################
def collide_rect_line(rect, p1, p2):
    return (collideLineLine(p1, p2, rect.topleft, rect.bottomleft) or
           collideLineLine(p1, p2, rect.bottomleft, rect.bottomright) or
           collideLineLine(p1, p2, rect.bottomright, rect.topright) or
           collideLineLine(p1, p2, rect.topright, rect.topleft))

############################################################################################################
#Our final function that checks for collision between a polygon and a rectangle
#	inputs:
#		rect: a pygame rectangle object consisting of 4 points
#       poly: a series of points that define a polygon
#	outputs:
#		COLLISION: boolean value indicating whether or not there was a collision
############################################################################################################
def collide_rect_polygon(rect, poly):
    for i in range(len(poly)-1):
        if collide_rect_line(rect, poly[i], poly[i+1]):
            return True
    return False
