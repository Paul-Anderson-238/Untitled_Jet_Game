########################################################
## Collision.py: Functions for detecting collision in game
########################################################
## Author: Paul Anderson
## Version: 1.1.0
## Status: Alpha Complete, Screen Scaling Added.
########################################################

import pygame
####################################################################################################
#    This is a helper function to detect collision between 2 line segments. This will detect if the
#    player object collides with the polygons that make up the top and bottom borders.
####################################################################################################
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

####################################################################################################
#   Uses the above Line collision function to see if a line intersects with a given rectangle.
####################################################################################################
def collide_rect_line(rect, p1, p2):
    return (collideLineLine(p1, p2, rect.topleft, rect.bottomleft) or
           collideLineLine(p1, p2, rect.bottomleft, rect.bottomright) or
           collideLineLine(p1, p2, rect.bottomright, rect.topright) or
           collideLineLine(p1, p2, rect.topright, rect.topleft))

####################################################################################################
#   Uses the above 2 functions to detect a collision between the player rectangle and the border polygons
####################################################################################################
def collide_rect_polygon(rect, poly):
    for i in range(len(poly)-1):
        if collide_rect_line(rect, poly[i], poly[i+1]):
            return True
    return False
