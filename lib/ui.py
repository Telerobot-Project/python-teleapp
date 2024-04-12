import pygame
import math


class Mouse:
    def __init__(self):
        self.pos = (0, 0)
        self.left = False
        self.left_down = False
        self.right = False
        self.right_down = False
        self.middle = False
        self.middle_down = False
        self.scroll = 0

    def read(self):
        self.pos = pygame.mouse.get_pos()
        self.left = pygame.mouse.get_pressed()[0]
        self.right = pygame.mouse.get_pressed()[2]
        self.middle = pygame.mouse.get_pressed()[1]
        self.scroll = pygame.mouse.get_rel()[1]

    def get_distance(self, x, y):
        return math.sqrt((self.pos[0] - x) ** 2 + (self.pos[1] - y) ** 2)

    def get_angle(self, x, y):
        return math.degrees(math.atan2(self.pos[0] - x, y - self.pos[1]))

    def is_in_rect(self, x, y, w, h):
        return self.pos[0] > x and self.pos[0] < x + w and self.pos[1] > y and self.pos[1] < y + h

    def is_in_circle(self, x, y, r):
        return self.get_distance(x, y) < r


class Keyboard:
    def __init__(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.space = False
    
    def read(self):
        self.left = pygame.key.get_pressed()[pygame.K_LEFT]
        self.right = pygame.key.get_pressed()[pygame.K_RIGHT]
        self.up = pygame.key.get_pressed()[pygame.K_UP]
        self.down = pygame.key.get_pressed()[pygame.K_DOWN]
        self.space = pygame.key.get_pressed()[pygame.K_SPACE]


class Window:
    def __init__(self, width, height, caption):
        self.width = width
        self.height = height
        self.size = (width, height)
        self.caption = caption
        self.mouse = Mouse()
        self.keyboard = Keyboard()

        self.run = True

    def start(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.font = pygame.font.SysFont('Arial', 15)
        self.clock = pygame.time.Clock()
    
    def read(self):
        self.mouse.left_down = 0
        self.mouse.right_down = 0
        self.mouse.middle_down = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse.left_down = 1
                if event.button == 3:
                    self.mouse.right_down = 1
                if event.button == 2:
                    self.mouse.middle_down = 1
        
        self.mouse.read()
        self.keyboard.read()

    def update(self):
        self.clock.tick(20)
        pygame.display.update()

    def close(self):
        self.run = False
        pygame.quit()

    def fill(self, color):
        self.screen.fill(color)

    def draw_text(self, text, x, y, color):
        self.screen.blit(self.font.render(text, True, color), (x, y))

    def draw_multi_text(self, lines, x, y):
        for i, l in enumerate(lines):
            self.draw_text(l, x, y + 20*i, (217, 217, 217))

    def draw_line(self, start_coord, angle, distance, color = (217, 217, 217), width = 1, dash = 0, end = True):
        angle = math.radians(angle)
        if dash:
            for i in range(math.round(distance / dash)):
                if i % 2 == 0:
                    pygame.draw.line(self.screen, color, start_coord, (start_coord[0] + math.sin(angle) * i * dash, start_coord[1] - math.cos(angle) * i * dash), width)
        else:
            pygame.draw.line(self.screen, color, start_coord, (start_coord[0] + math.sin(angle) * distance, start_coord[1] - math.cos(angle) * distance), width)
        if end:
            pygame.draw.circle(self.screen, color, (start_coord[0] + math.sin(angle) * distance, start_coord[1] - math.cos(angle) * distance), 5)

    def draw_text(self, x1, y1, x2, y2, color):
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), 5)
    
    def draw_video(self, image, x, y):
        self.screen.blit(image, (x, y))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, image.get_width(), image.get_height()), 2)


class Joystick:
    def __init__(self, x, y, r1, r2, color, window):
        self.x = x
        self.y = y
        self.r1 = r1
        self.r2 = r2
        self.color = color
        self.window: Window = window
        self.angle = 0
        self.distance = 0
        self.clicked = False

    def draw(self):
        pygame.draw.circle(self.window.screen, self.color,
                           (self.x, self.y), self.r1, 2)
        pygame.draw.circle(self.window.screen, self.color, (self.x + self.distance * math.sin(
            math.radians(self.angle)), self.y - self.distance * math.cos(math.radians(self.angle))), self.r2)

    def read(self):
        if self.window.mouse.left_down:
            if self.window.mouse.is_in_circle(self.x, self.y, self.r1):
                self.clicked = True
        if self.window.mouse.left and self.clicked:
            self.distance = self.window.mouse.get_distance(self.x, self.y)
            if self.distance > self.r1:
                self.distance = self.r1
            self.angle = self.window.mouse.get_angle(self.x, self.y)
            self.angle = (self.angle + 360) % 360
        else:
            self.distance = 0
            self.angle = 0
            self.clicked = False

class Image:
    def __init__(self, path, window, w = None, h = None, x = None, y = None):
        self.image = pygame.image.load(path)
        if w is not None and h is not None:
            self.image = pygame.transform.scale(self.image, (w, h))
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.window: Window = window

    def draw(self, x = None, y = None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.window.screen.blit(self.image, (self.x, self.y))

    def scale(self, w, h):
        self.image = pygame.transform.scale(self.image, (w, h))
        self.w = w
        self.h = h

class Button:
    def __init__(self, x, y, w, h, color, window):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.window: Window = window
        self.clicked = False
        self.down = False

    def draw(self):
        pygame.draw.rect(self.window.screen, self.color, (self.x, self.y, self.w, self.h), border_radius=5)

    def read(self):
        if self.window.mouse.left_down:
            if self.window.mouse.is_in_rect(self.x, self.y, self.w, self.h):
                self.clicked = True
                self.down = True
                print('Click')
        else:
            self.clicked = False
        if not self.window.mouse.left:
            self.down = False