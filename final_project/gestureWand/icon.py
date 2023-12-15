from baseui import BaseUI
import pygame

CURRENT = 0
EXPECTED = 1

class Icon(BaseUI):
    def __init__(self, surface, filepath, color, x, y, width, height, corner_radius=3, focusable=True):
        super().__init__(surface, x, y, width, height, focusable)
        self.corner_radius = [corner_radius, corner_radius]
        self.color = color
        self.filepath = filepath
        
        self.focus_intensity = 0.1
        self.saved_x_offset = 0
        self.saved_y_offset = 0
        
        # load the icon
        self.loaded_icon = pygame.image.load(self.filepath).convert_alpha()
        self.updateColor()


    def updateColor(self):
        w, h = self.loaded_icon.get_size()
        for x in range(w):
            for y in range(h):
                alpha = self.loaded_icon.get_at((x, y))[3] #[r, g, b, a]
                self.loaded_icon.set_at((x, y), pygame.Color(*self.color, alpha))


    def animation_step_update(self):
        super().animation_step_update()
    
    def draw(self):
        self.animation_step_update()
        icon_render = pygame.transform.scale(self.loaded_icon, (self.width[CURRENT], self.height[CURRENT]))
        icon_rect = icon_render.get_rect()
        icon_rect.center = (self.x[CURRENT] + self.width[CURRENT]//2), (self.y[CURRENT] + self.height[CURRENT]//2)
        self.surface.blit(icon_render, icon_rect)


    def focus(self):
        # default focus behavior: enlarge by self.focus_intensity
        if not self.in_focus:
            x_offset = round(self.width[CURRENT] * self.focus_intensity)
            y_offset = round(self.height[CURRENT] * self.focus_intensity)
            self.saved_x_offset = x_offset
            self.saved_y_offset = y_offset
            self.x[EXPECTED] -= x_offset
            self.y[EXPECTED] -= y_offset
            self.width[EXPECTED] += 2 * x_offset
            self.height[EXPECTED] += 2 * y_offset
        super().focus()
    
    
    def defocus(self):
        # default defocus behavior: shrink by self.focus_intensity
        if self.in_focus:
            x_offset = self.saved_x_offset
            y_offset = self.saved_y_offset
            self.x[EXPECTED] += x_offset
            self.y[EXPECTED] += y_offset
            self.width[EXPECTED] -= 2 * x_offset
            self.height[EXPECTED] -= 2 * y_offset
        super().defocus()
    
    def trigger(self, *args, **kwargs):
        super().trigger(*args, **kwargs)
    
    ########################################
    ###  GETTERS AND SETTERS ###
    ########################################
    
    def setColor(self, color):
        self.color = color
        self.updateColor()
    
    def setCornerRadius(self, value):
        self.corner_radius[EXPECTED] = value
    
    def setIconFilepath(self, filepath):
        self.filepath = filepath
        self.loaded_icon = pygame.image.load(self.filepath).convert_alpha()
        self.updateColor()