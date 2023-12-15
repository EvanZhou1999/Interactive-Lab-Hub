import pygame

CURRENT = 0
EXPECTED = 1

class BaseUI:
    def __init__(self, surface, x, y, width, height, focusable=True):
        # all animatable variables are a list [Current_value, Expected_value]
        self.x = [x, x]
        self.y = [y, y]
        self.width = [width, width]
        self.height = [height, height]
        
        self.surface = surface
        self.focusable = focusable
        self.in_focus = False
        
        self.step_portion = 0.2 # motion speed when animating, each update will increment by step_portion
        
        self.action = None
    
    def animation_step_update(self):
        animatable_objects = ['x', 'y', 'width', 'height']
        for name in animatable_objects:
            attr = getattr(self, name)
            direction = 1 if attr[EXPECTED] >= attr[CURRENT] else -1
            diff = abs(attr[EXPECTED] - attr[CURRENT])
            step = diff * self.step_portion
            attr[CURRENT] = attr[EXPECTED] if step <= 0.5 else attr[CURRENT] + (direction * round(step))
            setattr(self, name, attr)
    
    def draw(self):
        pass
    
    def focus(self):
        self.in_focus = True
    
    def defocus(self):
        self.in_focus = False
    
    def trigger(self, *args, **kwargs):
        if not self.action == None:
            self.action(*args, **kwargs)
    
    ########################################
    ###  GETTERS AND SETTERS ###
    ########################################
    def setRect(self, x=None, y=None, width=None, height=None):
        if not x == None:
            self.x[EXPECTED] = x
        if not y == None:
            self.y[EXPECTED] = y
        if not width == None:
            self.width[EXPECTED] = width
        if not height == None:
            self.height[EXPECTED] = height
    
    def get_rect(self):
        return pygame.rect(self.x[CURRENT], self.y[CURRENT], self.width[CURRENT], self.height[CURRENT])
