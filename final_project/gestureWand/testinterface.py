import pygame
import paho.mqtt.client as mqtt
import time
import math
# from pygame import gfxdraw
# from PIL import Image, ImageDraw
from skillwidget import SkillWidget
from statuswidget import StatusWidget
from magicringbody import MagicRingBody

from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_c,
    K_e,
    K_a,
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_RETURN,
    KEYDOWN,
    QUIT
)   

pygame.init()

# Setup the drawing window
screen = pygame.display.set_mode( [1280, 720] )
#screen = pygame.display.set_mode( (0, 0), pygame.FULLSCREEN )

# get the ecreen size
width, height = screen.get_size()


########################################
###  LOAD UI ELEMENTS ###
########################################
testvar = 0
pulsewidget = SkillWidget(surface=screen, 
                            theta = 0,
                            color = (255, 255, 0),
                            icon_filepath='./img/pulse_magic.png',
                            text_filepath='./img/pulse_text.png')

healthwidget = StatusWidget(surface=screen, 
                            theta = 288,
                            color = (255, 255, 0),
                            text_filepath='./img/health_text.png')

ring_body = MagicRingBody(surface=screen, color=(255, 255, 0))


########################################
###  MAIN GAME LOOP ###
########################################
# Setup the clock for a decent framerate
clock = pygame.time.Clock()
# Run until the user asks to quit
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            # Was it the Escale key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_c:
                pulsewidget.decreaseProrgess(10)
            if event.key == K_e:
                pulsewidget.setProrgess(100)
            if event.key == K_1:
                pulsewidget.setAngularPosition(90)
                healthwidget.setAngularPosition(0)
            if event.key == K_2:
                pulsewidget.setAngularPosition(0)
                healthwidget.setAngularPosition(288)
            if event.key == K_3:
                ring_body.setAngularPosition(0)
            if event.key == K_4:
                ring_body.setAngularPosition(90)

                
    screen.fill( (50, 50, 50) )
    #pulsewidget.draw()
    #healthwidget.draw()
    ring_body.draw()
    
    
    
    # Flip the display / Update the display
    pygame.display.flip()
    
    # Ensure program maintains a rate of60 frames per second
    clock.tick(60)

pygame.quit()
    
