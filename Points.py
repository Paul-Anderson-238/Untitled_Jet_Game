#####################################################
## Points.py: A custom class to track top and bottom
## y coordinates as well as their cooresponding x coordinate
#####################################################
## Author: Paul Anderson
## Version: 1.2.0
## Status: Effects for high scores updated, idle behavior implemented
#####################################################

from random import randint, getrandbits
import math

######################################################
## Inner class that contains a single x coordinate and
## the 2 coorisponding y's. Handles logic for moving x
## coordinates
######################################################
class Point:
    def __init__(self, x, y_top, y_bottom):
        self.x = x
        self.y_top = y_top
        self.y_bottom = y_bottom
        
    def get_x(self):
        return self.x
    
    def get_top_y(self):
        return self.y_top
        
    def get_bottom_y(self):
        return self.y_bottom
    
    #Adjusts the x coordinate to the left
    def adjust_x_left(self, adjustment):
        self.x -= adjustment

    #Adjusts the x coordinate to the right
    def adjust_x_right(self, adjustment):
        self.x += adjustment
        
    def get_top(self):
        return (self.x, self.y_top)
    
    def get_bottom(self):
        return (self.x, self.y_bottom)
    
    def print_points(self):
        return f"x={self.x} y_top={self.y_top} y_bottom={self.y_bottom}"

######################################################
## Wrapper class that the game object will interact with
## Initializes level to be straight at first, then semi
## randomly adds new coordinates. Makes adjustments to
## all individual points    
######################################################
class Points:
    def __init__(self, screen_width, screen_height, top, bottom, gap_min, gap_max, distance_min, distance_max):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.y_points = [Point(i*(screen_width/8), top, bottom) for i in range((math.ceil(screen_width/(screen_width/8)) * 2))]
        self.top = top
        self.bottom = bottom
        self.gap_min = gap_min
        self.gap_max = gap_max
        self.distance_min = distance_min
        self.distance_max = distance_max
    
    def update_points(self, speed):
        for point in self.y_points:
            point.adjust_x_left(speed)
        if self.y_points[1].get_x() < 0:
            self.y_points.pop(0)
        end = self.y_points[len(self.y_points)-1]
        if end.get_x() < self.screen_width:
            self.add_point(end)
    
    def add_point(self, end_point):
        #adjusts the new y points and gap based on the top y point
        def adjust_top(old_y, r, top, bottom):
            new_y = max(old_y - r, top)
            new_y2 = min(new_y + randint(int(self.gap_min * self.screen_height), int(self.gap_max * self.screen_height)), bottom)
            return (new_y, new_y2)
        #adjusts the new y points and gap based on the bottom y point
        def adjust_bottom(old_y, r, top, bottom):
            new_y2 = min(old_y + r, bottom)
            new_y = max(new_y2 - randint(int(self.gap_min * self.screen_height), int(self.gap_max * self.screen_height)), top)
            return (new_y, new_y2)
        
        new_range = randint(int(self.distance_min * self.screen_height), int(self.distance_max * self.screen_height)) #the adjustment to the gap the player is expected to go through 
        choice  = getrandbits(1) # a simple randomization variable for some random elements of play
        
        if choice:
            if not end_point.get_top_y() - new_range < self.top: #will the gap go beyond the max allowed y range at the top
                new_ys = adjust_top(end_point.get_top_y(), new_range, self.top, self.bottom)
                new_point = Point(end_point.get_x() + randint(int(self.screen_width/8), int(self.screen_width/4)), new_ys[0], new_ys[1])
            else:
                new_ys = adjust_bottom(end_point.get_bottom_y(), new_range, self.top, self.bottom)
                new_point = Point(end_point.get_x() + randint(int(self.screen_width/8), int(self.screen_width/4)), new_ys[0], new_ys[1])
        
        else:
            if not end_point.get_bottom_y() + new_range > self.bottom: #will the gap go beyond the max allowed y range at the bottom
                new_ys = adjust_bottom(end_point.get_bottom_y(), new_range, self.top, self.bottom)
                new_point = Point(end_point.get_x() + randint(int(self.screen_width/8), int(self.screen_width/4)), new_ys[0], new_ys[1])
            else:
                new_ys = adjust_top(end_point.get_top_y(), new_range, self.top, self.bottom)
                new_point = Point(end_point.get_x() + randint(int(self.screen_width/8), int(self.screen_width/4)), new_ys[0], new_ys[1])

        self.y_points.append(new_point) 
    
    #returns the list of points for the top of the screen
    def get_top_points(self):
        return [point.get_top() for point in self.y_points]
    
    #returns the list of points for the bottom of the screen
    def get_bottom_points(self):
        return [point.get_bottom() for point in self.y_points]
            
    def resize(self, x_scale, y_scale, screen_width, screen_height, top, bottom):
        new_points = []
        for point in self.y_points:
            new_x = int(point.get_x() * x_scale)
            new_top_y = int(point.get_top_y() * y_scale)
            new_bot_y = int(new_top_y + ((point.get_bottom_y() - point.get_top_y()) * y_scale))
            new_points.append(Point(new_x, new_top_y, new_bot_y))
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.y_points = new_points
        self.top = top
        self.bottom = bottom

#################################################################################################
# Running this file as a script: If running this file as a script, it will test the function with 
#                                test values. Feel free to tweak and test from here. 
#################################################################################################
if __name__ == "__main__":
    TOP = 100
    BOTTOM = 500
    min_distance = 0.1
    max_distance = 0.3
    GAP_MIN = 75
    GAP_MAX = 150
    test_point = (200, 300)
    
    points = Points(1200, 900, TOP, BOTTOM, GAP_MIN, GAP_MAX, min_distance, max_distance)
    print(points.get_top_points())
    print(points.get_bottom_points())

    for _ in range(50):
        points.update_points(50)
        print(points.get_top_points())
 
