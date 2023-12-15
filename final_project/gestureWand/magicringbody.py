import pygame
import math

CURRENT = 0
EXPECTED = 1

class MagicRingBody():
    def __init__(self, surface, color, x=640, y=360):
        self.surface = surface
        
        # general variables
        self.x_center = x # the x componenet of the center of the magic ring
        self.y_center = y # the y componenet of the center of the magic ring
        self.color = color
        
        # self spinning elements ===========
        # outer text ring
        self.loaded_outer_text_ring = pygame.image.load('./img/spell_ring_outer.png').convert_alpha()
        self.outer_text_ring_angle = 0
        self.outer_text_ring_size = [0.1, 575]
        self.outer_text_ring_speed = 0.32
        # square 1
        self.loaded_square1 = pygame.image.load('./img/ring_square.png').convert_alpha()
        self.square1_angle = 0
        self.square1_size = [0.1, 213]
        self.square1_speed = 0.7
        # square 2
        self.loaded_square2 = pygame.image.load('./img/ring_square.png').convert_alpha()
        self.square2_angle = 60
        self.square2_size = [0.1, 220]
        self.square2_speed = 0.82
        # square 3
        self.loaded_square3 = pygame.image.load('./img/ring_square.png').convert_alpha()
        self.square3_angle = 120
        self.square3_size = [0.2, 213]
        self.square3_speed = -0.32
        
        
        # static elements ============
        # ring 1 (outer most)
        self.r_ring1 = [0.1, 255]
        # ring 2
        self.r_ring2 = [0.1, 227]
        # ring 3
        self.r_ring3 = [0.1, 175]
        # ring 4 (inner most)
        self.r_ring4 = [0.1, 163]
        
        
        
        # dynamic elements ===========
        # inner text ring
        self.loaded_inner_text_ring = pygame.image.load('./img/spell_ring_inner.png').convert_alpha()
        self.inner_text_ring_angle = [0, 0]
        self.inner_text_ring_size = [0.1, 558]
        # star
        self.loaded_star = pygame.image.load('./img/ring_star.png').convert_alpha()
        self.star_angle = [0, 0]
        self.star_size = [0.1, 273]

        
        self.step_portion = 0.15
        
        self.updateColor()
        
    def updateColor(self):
        pngobjects = ['loaded_outer_text_ring', 'loaded_square1', 'loaded_square2', 'loaded_square3', 'loaded_inner_text_ring', 'loaded_star']
        for name in pngobjects:
            loaded_icon = getattr(self, name)
            w, h = loaded_icon.get_size()
            for x in range(w):
                for y in range(h):
                    alpha = loaded_icon.get_at((x, y))[3] #[r, g, b, a]
                    loaded_icon.set_at((x, y), pygame.Color(*self.color, alpha))
            setattr(self, name, loaded_icon)
    
    def animation_step_update(self):
        # process linear objects
        animatable_objects = ['outer_text_ring_size', 
                              'square1_size', 'square2_size', 'square3_size', 
                              'r_ring1', 'r_ring2', 'r_ring3', 'r_ring4', 
                              'inner_text_ring_size', 'star_size']
        for name in animatable_objects:
            attr = getattr(self, name)
            direction = 1 if attr[EXPECTED] >= attr[CURRENT] else -1
            diff = abs(attr[EXPECTED] - attr[CURRENT])
            step = diff * self.step_portion
            attr[CURRENT] = attr[EXPECTED] if step <= 0.5 else attr[CURRENT] + (direction * round(step))
            setattr(self, name, attr)
        
        # process angular objects
        animatable_objects = ['inner_text_ring_angle', 'star_angle']
        for name in animatable_objects:
            attr = getattr(self, name)
            clockwisedist = 0
            counterclockwisedist = 0
            if attr[CURRENT] <= attr[EXPECTED]:
                clockwisedist = attr[EXPECTED] - attr[CURRENT]
                counterclockwisedist = attr[CURRENT] + (360 - attr[EXPECTED])
            else: 
                clockwisedist = attr[EXPECTED] + (360 - attr[CURRENT])
                counterclockwisedist = attr[CURRENT] - attr[EXPECTED]
            # calculate theta step and update
            if clockwisedist <= counterclockwisedist:
                step = clockwisedist * self.step_portion
                attr[CURRENT] = attr[EXPECTED] if step <= 0.5 else (attr[CURRENT] + round(step)) % 360
            else: 
                step = counterclockwisedist * self.step_portion
                attr[CURRENT] = attr[EXPECTED] if step <= 0.5 else (attr[CURRENT] - round(step)) % 360
            setattr(self, name, attr)
        
        # self spinning elements stepping
        self.outer_text_ring_angle = (self.outer_text_ring_angle + self.outer_text_ring_speed) % 360
        self.square1_angle = (self.square1_angle + self.square1_speed) % 360
        self.square2_angle = (self.square2_angle + self.square2_speed) % 360
        self.square3_angle = (self.square3_angle + self.square3_speed) % 360

    def draw(self):
        self.animation_step_update()
        # draw outer text ring
        outer_text_ring_render = pygame.transform.scale(self.loaded_outer_text_ring, (self.outer_text_ring_size[CURRENT], self.outer_text_ring_size[CURRENT]))
        outer_text_ring_render = pygame.transform.rotate(outer_text_ring_render, self.outer_text_ring_angle)
        outer_text_ring_rect = outer_text_ring_render.get_rect()
        outer_text_ring_rect.center = (self.x_center, self.y_center)
        self.surface.blit(outer_text_ring_render, outer_text_ring_rect)
        # draw ring 1
        pygame.draw.circle(surface=self.surface, color=self.color, center=(self.x_center, self.y_center), radius=self.r_ring1[CURRENT], width=5)
        # draw ring 2
        pygame.draw.circle(surface=self.surface, color=self.color, center=(self.x_center, self.y_center), radius=self.r_ring2[CURRENT], width=5)
        # draw inner text ring
        inner_text_ring_render = pygame.transform.scale(self.loaded_inner_text_ring, (self.inner_text_ring_size[CURRENT], self.inner_text_ring_size[CURRENT]))
        inner_text_ring_render = pygame.transform.rotate(inner_text_ring_render, self.inner_text_ring_angle[CURRENT])
        inner_text_ring_rect = inner_text_ring_render.get_rect()
        inner_text_ring_rect.center = (self.x_center, self.y_center)
        self.surface.blit(inner_text_ring_render, inner_text_ring_rect)
        # draw ring 3
        pygame.draw.circle(surface=self.surface, color=self.color, center=(self.x_center, self.y_center), radius=self.r_ring3[CURRENT], width=2)
        # draw ring 4
        pygame.draw.circle(surface=self.surface, color=self.color, center=(self.x_center, self.y_center), radius=self.r_ring4[CURRENT], width=5)
        # draw square 1
        square1_render = pygame.transform.scale(self.loaded_square1, (self.square1_size[CURRENT], self.square1_size[CURRENT]))
        square1_render = pygame.transform.rotate(square1_render, self.square1_angle)
        square1_rect = square1_render.get_rect()
        square1_rect.center = (self.x_center, self.y_center)
        self.surface.blit(square1_render, square1_rect)
        # draw square 2
        square2_render = pygame.transform.scale(self.loaded_square2, (self.square2_size[CURRENT], self.square2_size[CURRENT]))
        square2_render = pygame.transform.rotate(square2_render, self.square2_angle)
        square2_rect = square2_render.get_rect()
        square2_rect.center = (self.x_center, self.y_center)
        self.surface.blit(square2_render, square2_rect)
        # draw square 3
        square3_render = pygame.transform.scale(self.loaded_square3, (self.square3_size[CURRENT], self.square3_size[CURRENT]))
        square3_render = pygame.transform.rotate(square3_render, self.square3_angle)
        square3_rect = square3_render.get_rect()
        square3_rect.center = (self.x_center, self.y_center)
        self.surface.blit(square3_render, square3_rect)
        # draw star
        star_render = pygame.transform.scale(self.loaded_star, (self.star_size[CURRENT], self.star_size[CURRENT]))
        star_render = pygame.transform.rotate(star_render, self.star_angle[CURRENT])
        star_rect = star_render.get_rect()
        star_rect.center = (self.x_center, self.y_center)
        self.surface.blit(star_render, star_rect)
        

    ########################################
    ###  GETTERS AND SETTERS ###
    ########################################
    
    def setColor(self, color):
        self.color = color
        self.updateColor()
    
    def setAngularPosition(self, angle):
        self.inner_text_ring_angle[EXPECTED] = -angle
        self.star_angle[EXPECTED] = angle
    
    
