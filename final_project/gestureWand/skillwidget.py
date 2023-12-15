import pygame
from PIL import Image, ImageDraw
import math

CURRENT = 0
EXPECTED = 1

class SkillWidget():
    # once x_center and y_center are determined, 
    # the location of the widget is dependent entirely on the y and theta component 
    # (r should stay constant as well, so really just "theta")
    def __init__(self, surface, theta, color, icon_filepath, text_filepath, x=640, y=360, r=245,
                 r_inner=40, r_outer=62, s_icon=50, s_text=70, progress=80):
        self.surface = surface
        
        self.x_center = x # the x componenet of the center that the widget is revolving
        self.y_center = y # the y componenet of the center that the widget is revolving
        self.r = r # how far away is the widget from its (x, y) center
        self.icon_filepath = icon_filepath
        self.text_filepath = text_filepath
        self.color = color
        # all animatable variables are a list [Current_value, Expected_value]
        self.theta = [0, theta] # the angular direction of the widget
        self.r_inner = [0.1, r_inner] # radius of the inner circle
        self.r_outer = [0.1, r_outer] # radius of the outer circle
        self.r_iconpadding = [0.1, r_inner - 10]
        self.r_progress = [0.1, self.r_iconpadding[EXPECTED]-5] # radius of the circular progress bar
        self.size_icon = [0.1, s_icon] # side length of the square text icon
        self.size_texticon = [0.1, s_text] # side length of the square text icon
        self.progress = [progress, progress] # circular progress bar value
        
        self.loaded_icon = pygame.image.load(self.icon_filepath).convert_alpha()
        self.loaded_texticon = pygame.image.load(self.text_filepath).convert_alpha()
        self.updateColor()
        
        self.in_focus = False
        self.focus_intensity = 10 # unit: pixels
        self.step_portion = 0.4
    
    def updateColor(self):
        w, h = self.loaded_icon.get_size()
        for x in range(w):
            for y in range(h):
                alpha = self.loaded_icon.get_at((x, y))[3] #[r, g, b, a]
                self.loaded_icon.set_at((x, y), pygame.Color(*self.color, alpha))
        w, h = self.loaded_texticon.get_size()
        for x in range(w):
            for y in range(h):
                alpha = self.loaded_texticon.get_at((x, y))[3] #[r, g, b, a]
                self.loaded_texticon.set_at((x, y), pygame.Color(*self.color, alpha))
                
    def drawPieslice(self, surface, x, y, r, start, end, color):
        # first generate Pi slice using PIL
        pil_image = Image.new("RGBA", (int(r*2), int(r*2)))
        pil_draw = ImageDraw.Draw(pil_image)
        pil_draw.pieslice((0, 0, r*2-1, r*2-1), start, end, fill=color)
        # convert to pygame surface
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        image = pygame.image.fromstring(data, size, mode)
        image_rect = image.get_rect()
        image_rect.center = (x, y)
        # draw
        surface.blit(image, image_rect)
    
    def animation_step_update(self):
        if self.theta[CURRENT] > 330 or self.theta[CURRENT] < 30:
            self.focus()
        else:
            self.defocus()
        animatable_objects = ['r_inner', 'r_outer', 'r_iconpadding', 'r_progress', 'size_icon', 'size_texticon', 'progress']
        for name in animatable_objects:
            attr = getattr(self, name)
            direction = 1 if attr[EXPECTED] >= attr[CURRENT] else -1
            diff = abs(attr[EXPECTED] - attr[CURRENT])
            step = diff * self.step_portion
            attr[CURRENT] = attr[EXPECTED] if step <= 0.5 else attr[CURRENT] + (direction * round(step))
            setattr(self, name, attr)
        
        # special stepping for circular variables
        # 'theta'
        clockwisedist = 0
        counterclockwisedist = 0
        if self.theta[CURRENT] <= self.theta[EXPECTED]:
            clockwisedist = self.theta[EXPECTED] - self.theta[CURRENT]
            counterclockwisedist = self.theta[CURRENT] + (360 - self.theta[EXPECTED])
        else: # self.theta[CURRENT] > self.theta[EXPECTED]:
            clockwisedist = self.theta[EXPECTED] + (360 - self.theta[CURRENT])
            counterclockwisedist = self.theta[CURRENT] - self.theta[EXPECTED]
        
        # calculate theta step and update
        if clockwisedist <= counterclockwisedist:
            step = clockwisedist * self.step_portion
            self.theta[CURRENT] = self.theta[EXPECTED] if step <= 0.5 else (self.theta[CURRENT] + round(step)) % 360
        else: 
            step = counterclockwisedist * self.step_portion
            self.theta[CURRENT] = self.theta[EXPECTED] if step <= 0.5 else (self.theta[CURRENT] - round(step)) % 360
            
    
    def draw(self):
        self.animation_step_update()
        x_widget = self.x_center + round(self.r * math.cos(math.radians(self.theta[CURRENT] - 90))) # the x component of the actual widget center
        y_widget = self.y_center + round(self.r * math.sin(math.radians(self.theta[CURRENT] - 90))) # the y component of the actual widget center
        
        # draw the outer circle
        pygame.draw.circle(surface=self.surface, color=self.color, center=(x_widget, y_widget), radius=self.r_outer[CURRENT], width=2)
        # draw the texticon
        texticon_render = pygame.transform.scale(self.loaded_texticon, (self.size_texticon[CURRENT], self.size_texticon[CURRENT]))
        texticon_rect = texticon_render.get_rect()
        texticon_rect.center = (x_widget, y_widget)
        self.surface.blit(texticon_render, texticon_rect)
        # draw inner circle (first draw the solid center, then draw the outline)
        pygame.draw.circle(surface=self.surface, color=(0, 0, 0), center=(x_widget, y_widget), radius=self.r_inner[CURRENT], width=0)
        pygame.draw.circle(surface=self.surface, color=self.color, center=(x_widget, y_widget), radius=self.r_inner[CURRENT], width=5)
        # draw pie slice (for progress bar)
        self.drawPieslice(self.surface, x_widget, y_widget, self.r_progress[CURRENT], -90, round(self.progress[CURRENT]*360/100-90), self.color)
        # draw the icon padding
        pygame.draw.circle(surface=self.surface, color=(0, 0, 0), center=(x_widget, y_widget), radius=self.r_iconpadding[CURRENT], width=0)
        # draw the icon
        icon_render = pygame.transform.scale(self.loaded_icon, (self.size_icon[CURRENT], self.size_icon[CURRENT]))
        icon_rect = icon_render.get_rect()
        icon_rect.center = (x_widget, y_widget)
        self.surface.blit(icon_render, icon_rect)
        
        
    
    def focus(self):
        if self.in_focus:
            return
        self.in_focus = True
        # adjust widget
        self.r_inner[EXPECTED] += 27
        self.r_outer[EXPECTED] += 40
        self.r_iconpadding[EXPECTED] += 15
        self.r_progress[EXPECTED] += 30
        self.size_icon[EXPECTED] += 30
        self.size_texticon[EXPECTED] += 120
        
    
    def defocus(self):
        if not self.in_focus:
            return
        self.in_focus = False
        # adjust widget
        self.r_inner[EXPECTED] -= 27
        self.r_outer[EXPECTED] -= 40
        self.r_iconpadding[EXPECTED] -= 15
        self.r_progress[EXPECTED] -= 30
        self.size_icon[EXPECTED] -= 30
        self.size_texticon[EXPECTED] -= 120
    
    ########################################
    ###  GETTERS AND SETTERS ###
    ########################################
    
    def setColor(self, color):
        self.color = color
        self.updateColor()
    
    def setAngularPosition(self, angle):
        self.theta[EXPECTED] = angle
    
    def decreaseProrgess(self, stepsize):
        self.progress[EXPECTED] -= stepsize
        if self.progress[EXPECTED] < 0:
            self.progress[EXPECTED] = 0 
    
    def increaseProrgess(self, stepsize):
        self.progress[EXPECTED] += stepsize
        if self.progress[EXPECTED] > 100:
            self.progress[EXPECTED] = 100 
    
    def setProrgess(self, value):
        self.progress[EXPECTED] = value
        