import pygame
from math import sqrt
from lib.ui import Window

class Robot:
    def __init__(self, window: Window):
        self.speed = 0
        self.max_speed = 60
        self.turn_speed = 0
        self.direction = 0
        self.window = window

        self.gyro = 0
        self.us = [200] * 6
        self.us_max_dist = 200
        
    
    def draw(self):
        pygame.draw.rect(self.window.screen, (217, 217, 217), (175, 255, 100, 190), border_radius=20)

        self.window.draw_line((200, 255), -45, self.us[0] if self.us[0] < self.us_max_dist else self.us_max_dist)
        self.window.draw_line((225, 255), 0, self.us[1] if self.us[1] < self.us_max_dist else self.us_max_dist)
        self.window.draw_line((250, 255), 45, self.us[2] if self.us[2] < self.us_max_dist else self.us_max_dist)
        self.window.draw_line((175, 350), -90, self.us[3] if self.us[3] < self.us_max_dist else self.us_max_dist)
        self.window.draw_line((275, 350), 90, self.us[4] if self.us[4] < self.us_max_dist else self.us_max_dist)
        self.window.draw_line((225, 445), 180, self.us[5] if self.us[5] < self.us_max_dist else self.us_max_dist)
