import pygame

class Robot:
    def __init__(self, window):
        self.speed = 0
        self.max_speed = 60
        self.turn_speed = 0
        self.direction = 0
        self.window = window

        self.gyro = 0
        self.us = [0] * 6
        
    
    def draw(self):
        pygame.draw.rect(self.window.screen, (217, 217, 217), (175, 340, 100, 190), border_radius=20)
        if self.us[0] < 150:
            pygame.draw.line(self.window.screen, (217, 217, 217), (170-self.us[0], 435), (175, 435), 2)
            pygame.draw.circle(self.window.screen, (217, 217, 217), (170-self.us[0], 435), 5)
        else:
            pygame.draw.line(self.window.screen, (217, 217, 217), (20, 435), (175, 435), 2)
            pygame.draw.circle(self.window.screen, (217, 217, 217), (20, 435), 5)

        if self.us[1] < 150:
            pygame.draw.line(self.window.screen, (217, 217, 217), (275, 435), (280+self.us[1], 435), 2)
            pygame.draw.circle(self.window.screen, (217, 217, 217), (280+self.us[1], 435), 5)
        else:
            pygame.draw.line(self.window.screen, (217, 217, 217), (275, 435), (430, 435), 2)
            pygame.draw.circle(self.window.screen, (217, 217, 217), (430, 435), 5)
        
        if self.us[2] < 150:
            pygame.draw.line(self.window.screen, (217, 217, 217), (225, 530), (225, 535+self.us[2]), 2)
            pygame.draw.circle(self.window.screen, (217, 217, 217), (225, 535+self.us[2]), 5)
        else:
            pygame.draw.line(self.window.screen, (217, 217, 217), (225, 530), (225, 685), 2)
            pygame.draw.circle(self.window.screen, (217, 217, 217), (225, 685), 5)

        
