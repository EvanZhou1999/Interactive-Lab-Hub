from baseui import BaseUI
import pygame

CURRENT = 0
EXPECTED = 1

class Text(BaseUI):
    def __init__(self, surface, color, x, y, width=None, height=None, text='', font='fonts/SFPro-Regular.ttf', corner_radius=0, text_size=13, text_align='center', focusable=True):
        # first estimate the rendered text rectangle in case we have None for width/height
        font_loaded = pygame.font.Font(font, text_size)
        text_render = font_loaded.render(text, True, color)
        temp_rect = text_render.get_rect() # pygame.Rect(x, y, w, h)
        # then initialize class variables
        super().__init__(surface, x, y, temp_rect[2] if width == None else width, temp_rect[3] if height == None else height, focusable)
        # all animatable variables are a list [Current_value, Expected_value]
        self.color = color
        self.corner_radius = [corner_radius, corner_radius]
        self.text = text
        self.text_size = [text_size, text_size]
        self.font = font
        
        self.text_align = text_align   # 'center', 'Left', 'right'
        
    
    def animation_step_update(self):
        super().animation_step_update()
        animatable_objects = ['corner_radius', 'text_size']
        for name in animatable_objects:
            attr = getattr(self, name)
            direction = 1 if attr[EXPECTED] >= attr[CURRENT] else -1
            diff = abs(attr[EXPECTED] - attr[CURRENT])
            step = diff * self.step_portion
            attr[CURRENT] = attr[EXPECTED] if step <= 0.5 else attr[CURRENT] + (direction * round(step))
            setattr(self, name, attr)


    def draw(self):
        self.animation_step_update()
        # loading Text
        font_loaded = pygame.font.Font(self.font, self.text_size[CURRENT])
        text_render = font_loaded.render(self.text, True, self.color)
        text_render_rect = text_render.get_rect()
        if self.text_align == 'center':
            text_render_rect.center = (self.x[CURRENT] + self.width[CURRENT]//2), (self.y[CURRENT] + self.height[CURRENT]//2)
        elif self.text_align == 'left':
            text_render_rect.centery = (self.y[CURRENT] + self.height[CURRENT]//2)
            text_render_rect.left = self.x[CURRENT]
        elif self.text_align == 'right':
            text_render_rect.centery = (self.y[CURRENT] + self.height[CURRENT]//2)
            text_render_rect.right = self.x[CURRENT] + self.width[CURRENT]
        
        self.surface.blit(text_render, text_render_rect)
    
    def focus(self):
        pass
        super().focus()
    
    def defocus(self):
        pass
        super().defocus()
    
    def trigger(self, *args, **kwargs):
        super().trigger(*args, **kwargs)

    ########################################
    ###  GETTERS AND SETTERS ###
    ########################################

    def setCornerRadius(self, value):
        self.corner_radius[EXPECTED] = value
    
    def setAlign(self, value):
        assert value == 'center' or value == 'left' or value == 'right'
        self.text_align = value
    
    def setText(self, str):
        self.text = str
    
    def setColor(self, color):
        self.color = color
    
    def setTextSize(self, value):
        self.text_size[EXPECTED] = value
    
    def setFont(self, value):
        self.font = value
