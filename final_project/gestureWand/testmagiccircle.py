import pygame
import paho.mqtt.client as mqtt
import time
import math
# from pygame import gfxdraw
# from PIL import Image, ImageDraw
from magiccircle import MagicCircle
from handtracking import HandTracking
from basic_shape import healthWidget

CURRENT = 0
EXPECTED = 1

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
angle = 0
track = HandTracking()
magic_circle = MagicCircle(surface=screen, color=(255, 255, 0))
myhealth = healthWidget(surface=screen, x=25, y=20, title="YOU")
myhealth.x[CURRENT] = -70
opponenthealth = healthWidget(surface=screen, x=1170, y=20, title="ENEMY")
opponenthealth.x[CURRENT] = 1280


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
                angle = (angle + 10) % 360
            if event.key == K_e:
                angle = (angle - 10) % 360
            if event.key == K_1:
                myhealth.setProgress(57)
            if event.key == K_2:
                myhealth.setProgress(100)
            if event.key == K_3:
                myhealth.setProgress(3)
            
    detection = track.detectLeftHandAngle()
    if not detection == None:
        angle = detection

    screen.fill( (0, 0, 0) )
    magic_circle.setAngle(angle)
    magic_circle.draw()
    myhealth.draw()
    opponenthealth.draw()
    
    
    
    # Flip the display / Update the display
    pygame.display.flip()
    
    # Ensure program maintains a rate of60 frames per second
    clock.tick(60)

pygame.quit()
    
