import pygame
import math
from skillwidget import SkillWidget
from statuswidget import StatusWidget
from magicringbody import MagicRingBody

CURRENT = 0
EXPECTED = 1

class MagicCircle():
    def __init__(self, surface, color):
        self.surface = surface
        self.color = color
        self.angle = 0
        
        # five skill/status objects
        self.pulsewidget = SkillWidget(surface=self.surface, 
                            theta = 0,
                            color = color,
                            icon_filepath='./img/pulse_magic.png',
                            text_filepath='./img/pulse_text_b.png')
        self.beamwidget = SkillWidget(surface=self.surface, 
                            theta = 0,
                            color = color,
                            icon_filepath='./img/beam_magic.png',
                            text_filepath='./img/beam_text_b.png')
        self.shieldwidget = SkillWidget(surface=self.surface, 
                            theta = 0,
                            color = color,
                            icon_filepath='./img/shield_magic.png',
                            text_filepath='./img/shield_text_b.png')
        self.healthwidget = StatusWidget(surface=self.surface, 
                            theta = 0,
                            color = color,
                            text_filepath='./img/health_text_b.png')
        self.specialwidget = StatusWidget(surface=self.surface, 
                            theta = 0,
                            color = color,
                            text_filepath='./img/special_attack_text_b.png')
        self.ring_body = MagicRingBody(surface=self.surface, color=color)
        
        self.pulsewidget.setProrgess(100)
        self.beamwidget.setProrgess(100)
        self.shieldwidget.setProrgess(100)
        self.healthwidget.setProrgess(100)
        self.specialwidget.setProrgess(0)
    
    
    def draw(self):
        self.ring_body.draw()
        self.pulsewidget.draw()
        self.beamwidget.draw()
        self.shieldwidget.draw()
        self.healthwidget.draw()
        self.specialwidget.draw()
    
    ########################################
    ###  GETTERS AND SETTERS ###
    ########################################
    
    def setColor(self, color):
        self.color = color
        self.pulsewidget.setColor(color)
        self.beamwidget.setColor(color)
        self.shieldwidget.setColor(color)
        self.healthwidget.setColor(color)
        self.specialwidget.setColor(color)
        self.ring_body.setColor(color)
    
    def setAngle(self, angle):
        self.angle = angle
        self.pulsewidget.setAngularPosition(self.angle)
        self.beamwidget.setAngularPosition((self.angle - 72) % 360)
        self.shieldwidget.setAngularPosition((self.angle + 72) % 360)
        self.healthwidget.setAngularPosition((self.angle - 144) % 360)
        self.specialwidget.setAngularPosition((self.angle + 155) % 360)
        self.ring_body.setAngularPosition(self.angle)
        
    def getFocused(self):
        focused_list = [] # order: beam, pulse, shield, special, health
        focused_list.append(self.beamwidget.in_focus)
        focused_list.append(self.pulsewidget.in_focus)
        focused_list.append(self.shieldwidget.in_focus)
        focused_list.append(self.specialwidget.in_focus)
        focused_list.append(self.healthwidget.in_focus)
        
        return focused_list
    