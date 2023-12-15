import pygame
import random
import math
from text import Text

CURRENT = 0
EXPECTED = 1

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super(Fire, self).__init__()
        self.x = x
        self.y = y
        self.radius = radius
        
        self.yvel = random.randint(1, 9)
        self.burn_rate = 0.1
        
        self.layers = 2
        self.glow = 2
        
        surf_size = 2 * self.radius * self.layers * self.layers * self.glow
        self.surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
        
    def update(self, win):
        xvel = random.randint(-int(self.radius), int(self.radius))
        self.x += xvel
        self.y -= self.yvel
        
        self.radius -= self.burn_rate
        if self.radius <= 0:
            self.radius = 0.01
        
        surf_size = 2 * self.radius * self.layers * self.layers * self.glow
        self.surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
        
        for i in range(self.layers, -1, -1):
            alpha = 255 - i * (255 // self.layers - 5)
            if alpha <= 0:
                alpha = 0.01
            radius = int(self.radius * self.glow * i * i)
             
            if self.radius >3.5:
                color = 255, 0, 0
            elif self.radius > 2.5:
                color = 255, 150, 0
            else:
                color = 50, 50, 50
            color = (*color, alpha)
        
            pygame.draw.circle(self.surf, color, (self.surf.get_width() // 2, self.surf.get_height() // 2), radius)
        win.blit(self.surf, self.surf.get_rect(center=(self.x, self.y)))

class healthWidget():
    def __init__(self, surface, x, y, height=640, width=70, title=""):
        self.surface = surface
        
        self.x = [x, x]
        self.y = [x, y]
        self.height = [height, height]
        self.width = [width, width] 
        
        self.title = title
        self.outline_color = (140, 140, 140)
        self.hp_color = (160, 47, 64)
        
        self.progress = [100, 100]
        
        self.title_x = x
        self.title_y = y
        self.title = Text(surface=surface,
                        color=(240, 240, 240),
                        x=self.title_x, y=self.title_y,
                        width=width, height=30,
                        text = title, 
                        text_size=30,
                        font='fonts/SFPro-Bold.ttf')
        
        self.percent_text_x = self.x[EXPECTED]
        self.percent_text_y = self.y[EXPECTED]+self.height[EXPECTED]-5
        self.percent_text = Text(surface=surface,
                                color=(240, 240, 240),
                                x=self.percent_text_x, y=self.percent_text_y,
                                width=width, height=30,
                                text = title, 
                                text_size=25,
                                font='fonts/SFPro-Bold.ttf')
        
        self.step_portion = 0.2
    
    
    def animation_step_update(self):
        animatable_objects = ['x', 'y', 'height', 'width', 'progress']
        for name in animatable_objects:
            attr = getattr(self, name)
            direction = 1 if attr[EXPECTED] >= attr[CURRENT] else -1
            diff = abs(attr[EXPECTED] - attr[CURRENT])
            step = diff * self.step_portion
            attr[CURRENT] = attr[EXPECTED] if step <= 0.5 else attr[CURRENT] + (direction * round(step))
            setattr(self, name, attr)
    
    def draw(self):
        self.animation_step_update()
        # draw title
        self.title.draw()
        # draw percent text
        self.percent_text.setText(f"{self.progress[CURRENT]}%")
        self.percent_text.draw()
        # draw the outline of HP bar (with ruonded corner)
        outline_width = self.width[CURRENT] - 20
        outline_height = self.height[CURRENT] - 60
        pygame.draw.rect(self.surface,
                        color=self.outline_color,
                        rect=pygame.Rect(self.x[CURRENT] + (self.width[CURRENT]//2) - (outline_width//2), self.y[CURRENT] + 50, outline_width, outline_height),
                        width=4,
                        border_radius=outline_width//2)

        # draw the actual HP bar (with ruonded corner)
        hp_width = outline_width - 24
        hp_height = round((outline_height - 20) / 100 * self.progress[CURRENT])
        pygame.draw.rect(self.surface,
                        color=self.hp_color,
                        rect=pygame.Rect(self.x[CURRENT] + (self.width[CURRENT]//2) - (hp_width//2), self.y[CURRENT] + 50 + outline_height - hp_height - 10, hp_width, hp_height),
                        width=0,
                        border_radius=hp_width//2)
    
    
    def setPosition(self, x=None, y=None):
        self.x[EXPECTED] = x
        self.y[EXPECTED] = y
        self.title_x = self.x[EXPECTED]
        self.title_y = self.y[EXPECTED]
        self.percent_text_x = self.x[EXPECTED]
        self.percent_text_y = self.y[EXPECTED]+self.height[EXPECTED]-5
        self.title.setRect(x, y, self.width, 30)
        self.percent_text.setRect(x, y, self.width, 30)

    def setProgress(self, value):
        self.progress[EXPECTED] = value
        
        
        