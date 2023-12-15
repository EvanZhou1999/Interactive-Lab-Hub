import paho.mqtt.client as mqtt
import time
import math
from magiccircle import MagicCircle

CURRENT = 0
EXPECTED = 1

class Player():
    def __init__(self, surface, player_id, strength='none'):
        self.surface = surface
        self.strength = strength  # 'pulse', 'beam', 'shield'
        self.color = (255, 255, 255) # white for non-specialized player (default)
        
        # skill settings
        self.pulse_deduction = 5 # how many of the "progress bar" will you loose everytime you use pulse mgic
        self.pulse_damage = 10
        self.beam_deduction = 4 # how many of the "progress bar" will you loose everime you use beam magic
        self.beam_damage = 3
        self.shield_deduction = 0.1 # how many "progress bar" will you loose everime you engage the shield 
        self.special_attack_damage = 40
        self.special_attack_increment = 2
        
        # other variables
        self.id = player_id
        self.health = 100
        self.is_dead = False
        self.wand_activated = False
        
        self.shield_engaging = False
        self.beam_engaging = False
        
        # special variable
        self.loading = False # this flag will set to true if there is a function running on a separate thread
        
        
        # configure player
        if strength == 'pulse':
            self.color = (255, 255, 0) # yellow
            self.pulse_deduction /= 2
        elif strength == 'beam':
            self.color = (0, 255, 255) # cyan
            self.beam_deduction /= 2
        elif strength == 'shield':
            self.color = (0, 255, 0) # green
            self.shield_deduction /= 2
        
        
        # set magic circle
        self.magic_circle = MagicCircle(surface=self.surface, color=self.color)
    
    
    def player_available(self):
        return (not self.is_dead) and self.wand_activated
    
    def player_beam_focus(self):
        return self.magic_circle.getFocused()[0]
    
    def player_pulse_focus(self):
        return self.magic_circle.getFocused()[1]
    
    def player_shield_focus(self):
        return self.magic_circle.getFocused()[2]
    
    def player_special_focus(self):
        return self.magic_circle.getFocused()[3]
    
    def player_health_focus(self):
        return self.magic_circle.getFocused()[4]
    
    def setStrength(self, strength):
        self.loading = True
        if strength == 'pulse':
            self.color = (255, 255, 0) # yellow
            self.pulse_deduction /= 2
        elif strength == 'beam':
            self.color = (0, 255, 255) # cyan
            self.beam_deduction /= 2
        elif strength == 'shield':
            self.color = (0, 255, 0) # green
            self.shield_deduction /= 2
        self.magic_circle.setColor(self.color)
        self.loading = False
        
    
    def player_hit(self, damage):
        self.magic_circle.healthwidget.decreaseProrgess(damage)
        self.health = self.magic_circle.healthwidget.progress[EXPECTED]
        self.magic_circle.specialwidget.increaseProrgess(self.special_attack_increment * damage)
        if self.magic_circle.healthwidget.progress[EXPECTED] <= 0:
            self.dead()

    
    def dead(self):
        self.is_dead = True
        self.wand_activated = False
    
    def pulseAttack(self):
        self.magic_circle.pulsewidget.decreaseProrgess(self.pulse_deduction)
    
    def specialAttack(self):
        self.magic_circle.specialwidget.setProrgess(0)
    
    def beamAttack(self):
        self.magic_circle.beamwidget.decreaseProrgess(self.beam_deduction)
        self.beam_engaging = True
    
    def beamAttackEnd(self):
        self.beam_engaging = False
    
    def shieldEngage(self):
        self.magic_circle.shieldwidget.decreaseProrgess(self.shield_deduction)
        self.shield_engaging = True
    
    def shieldDisengage(self):
        self.shield_engaging = False
    
    
        
        
        
        
        