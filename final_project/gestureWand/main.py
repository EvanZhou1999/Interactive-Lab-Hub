import pygame
import paho.mqtt.client as mqtt
import random
import time
import math
import threading
import uuid
import ssl
# from pygame import gfxdraw
# from PIL import Image, ImageDraw
from player import Player
from handtracking import HandTracking
from basic_shape import Fire, healthWidget
from icon import Icon
from text import Text

from pygame.locals import(
    K_ESCAPE,
    KEYDOWN,
    K_d,
    K_s,
    QUIT
)   

CURRENT = 0
EXPECTED = 1

#########################################################
# CONFIG
player_id = 2
opponent_id = 2 if player_id == 1 else 1
#########################################################


# Configure MQTT ================================================
#this is the callback that gets called once we connect to the broker. 
#we should add our subscribe functions here as well
def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(f"IDD/player{player_id}/#")
    client.subscribe(f"IDD/player{opponent_id}/hit")
    #client.subscribe('IDD/#')
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')

# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
    global alpha_overlay
    global shield_alpha
    print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
	# you can filter by topics
	# if msg.topic == 'IDD/some/other/topic': do thing
    if msg.topic == f'IDD/player{player_id}/spellcast' and player.player_available(): # if the player is alive and wand is activated
        # check which spell the player want to cast
        if player.player_pulse_focus():
            # check if the player:
            # - not engaging shield
            # - not engaging beam
            if not player.shield_engaging and not player.beam_engaging:
                # then check if the player has spell remaining
                if player.magic_circle.pulsewidget.progress[CURRENT] > 0:
                    # send MQTT to the wand
                    client.publish(f"IDD/player{player_id}/pulse/start", "")
                    client.publish(f"IDD/player{player_id}/godot/pulse/start", "")
                    # Update UI
                    player.pulseAttack()
                    # send MQTT to the opponent for damage assessment
                    #client.publish(f"IDD/player{opponent_id}/damage", f"{player.pulse_damage}")
        elif player.player_beam_focus():
            # check if the player already has shield engaged
            if not player.shield_engaging:
                if player.magic_circle.beamwidget.progress[EXPECTED] > 0:
                    # send MQTT to the wand
                    client.publish(f"IDD/player{player_id}/beam/start", "")
                    # Update UI
                    player.beamAttack()
                    # send MQTT to the opponent for damage assessment
                    # client.publish(f"IDD/player{opponent_id}/damage", f"{player.beam_damage}")
                    
        elif player.player_shield_focus():
            # check if the player already has beam engaged
            if not player.beam_engaging:
                if player.magic_circle.shieldwidget.progress[EXPECTED] > 0:
                    # send MQTT to the wand
                    client.publish(f"IDD/player{player_id}/shield/start", "")
                    # Update UI
                    player.shieldEngage()

        elif player.player_special_focus():
            # check if the player already have something engaged
            if not player.shield_engaging and not player.beam_engaging:
                # check if the player's special attack bar have filled
                if player.magic_circle.specialwidget.progress[EXPECTED] >= 100:
                    # send MQTT to the wand
                    client.publish(f"IDD/player{player_id}/specialattack/start", "")
                    # Update UI
                    player.specialAttack()
                    # send MQTT to the opponent for damage assessment
                    client.publish(f"IDD/player{opponent_id}/damage", f"{player.special_attack_damage}")
                    
    elif msg.topic == f'IDD/player{player_id}/spellcancel' and player.player_available():
        # check which weapon the player has engaged
        if player.shield_engaging:
            # send MQTT to the wand
            client.publish(f"IDD/player{player_id}/shield/end", "")
            # Update UI
            player.shieldDisengage()
        
        elif player.beam_engaging:
            # send MQTT to the wand
            client.publish(f"IDD/player{player_id}/beam/end", "")
            client.publish(f"IDD/player{player_id}/godot/beam/end", "")
            # Update UI
            player.beamAttackEnd()
    
    elif msg.topic == f'IDD/player{player_id}/damage' and player.player_available():
        # check if the user has shield engaged:
        # if not player.shield_engaging:
        if player.player_available():
            # user will take damage
            # change UI
            alpha_overlay = 240
            # change player status
            player.player_hit(int(msg.payload.decode('UTF-8')))
            # send MQTT to the wand
            client.publish(f"IDD/player{player_id}/hit", f"{player.health}")
        else:
            pass
            #shield_alpha = 240
            #client.publish(f"IDD/player{player_id}/successfulDefend", "")
            
    
    elif msg.topic == f'IDD/player{player_id}/successfulDefend' and player.player_available():
        shield_alpha = 240
    
    elif msg.topic == f'IDD/player{opponent_id}/hit':
        opponenthealth.setProgress(int(msg.payload.decode('UTF-8')))
    


def player_stat_update():
    # check if the player is engaging the shield
    if player.shield_engaging:
        # Update UI
        player.shieldEngage()
        if player.magic_circle.shieldwidget.progress[EXPECTED] <= 0:
            # send MQTT to the wand
            client.publish(f"IDD/player{player_id}/shield/end", "")
            # Update UI
            player.shieldDisengage()
    elif player.beam_engaging:
        # Update UI
        player.beamAttack()
        # send MQTT to the opponent for damage assessment
        # client.publish(f"IDD/player{opponent_id}/damage", f"{player.beam_damage}")
        client.publish(f"IDD/player{player_id}/godot/beam/start", "")
        if player.magic_circle.beamwidget.progress[EXPECTED] <= 0:
            # send MQTT to the wand
            client.publish(f"IDD/player{player_id}/beam/end", "")
            client.publish(f"IDD/player{player_id}/godot/beam/end", "")
            # Update UI
            player.beamAttackEnd()
            
            
        

# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
# client.tls_set(cert_reqs=ssl.CERT_NONE)
# this is the username and pw we have setup for the class
# client.username_pw_set('public', 'public')

# attach out callbacks to the client
client.on_connect = on_connect
client.on_message = on_message
#connect to the broker
# client.connect(
#     'public.cloud.shiftr.io',
#     port=1883)
client.connect(
    'broker.hivemq.com',
    port=1883)
# client.connect(
#     '10.56.6.114',
#     port=1883)
# client.loop_start() # we won't start the loop while player is not instantiated

# Configure Pygame ================================================
pygame.init()

# Setup the drawing window
screen = pygame.display.set_mode( [1280, 720] )
#screen = pygame.display.set_mode( (0, 0), pygame.FULLSCREEN )

# get the ecreen size
width, height = screen.get_size()


# initiate gameobjects
track = HandTracking()
player = Player(surface=screen, player_id=player_id)
fire_group = pygame.sprite.Group()

# we start loop MQTT after instantiating player
client.loop_start()

########################################
###  MAIN GAME LOOP ###
########################################
# Setup the clock for a decent framerate
clock = pygame.time.Clock()
# Run until the user asks to quit
running = True


## some initializations for the first screen UI
offset = 50
gesture_prompt_up = Icon(surface=screen, 
                         filepath='./img/demo_hand_up.png', 
                         color=(100, 100, 100), 
                         x=width/2-30, y=height/2-offset-53,
                         width=80, height=53)
gesture_prompt_down = Icon(surface=screen, 
                         filepath='./img/demo_hand_down.png', 
                         color=(100, 100, 100), 
                         x=width/2-40, y=height/2+offset,
                         width=80, height=53)

text_prompt = Text(surface=screen,
                   color=(255, 255, 255),
                   x=width/2 - 50, y=height/2 + 100,
                   text = "Cast Your Spells", 
                   text_size=20)

# First check if the start gesture id being detected
while running and not track.detectStartGesture():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            # Was it the Escale key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

    offset -= 1
    if offset < -5:
        offset = 50
    gesture_prompt_up.y[EXPECTED] = height/2-offset-53
    gesture_prompt_down.y[EXPECTED] = height/2+offset
    screen.fill( (0, 0, 0) )
    gesture_prompt_up.draw()
    gesture_prompt_down.draw()
    text_prompt.draw()
    
    # Flip the display / Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of60 frames per second
    clock.tick(60)


# Start Gesture detected, add flame effect
direction = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            # Was it the Escale key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

    direction = track.detectThumbAngle() # return 1 for vertical, 2 for horizontal, 3 for 45 degree, or None
    if not direction == None:
        if direction == 1: # vertical - pulse
            # player.setStrength('pulse')
            thread = threading.Thread(target=player.setStrength, args=('pulse',))
            thread.start()
        if direction == 2: # horizontal - shield
            # player.setStrength('shield')
            thread = threading.Thread(target=player.setStrength, args=('shield',))
            thread.start()
        if direction == 3: # diagonal - beam
            # player.setStrength('beam')
            thread = threading.Thread(target=player.setStrength, args=('beam',))
            thread.start()
        break


    screen.fill( (0, 0, 0) )
    
    # draw flame effect
    for i in range(2):
        x, y = 640, 360
        r = random.randint(4, 10)
        f = Fire(x, y, r)
        fire_group.add(f)
    
    fire_group.update(screen)
    for fire in fire_group:
        if fire.radius <= 0:
            fire.kill()
    
    # Flip the display / Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of60 frames per second
    clock.tick(60)

# space filler for magic ring loading thread
time.sleep(0.1)
finger1 = (640, 360)
finger2 = (640, 360)
r_portion = 0.01
while running and player.loading:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            # Was it the Escale key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
    
    
    coor = track.detectThumbCoordinates()
    if not coor == None:
        finger1 = coor[0]
        finger2 = coor[1]
        print(coor)
    
    
    screen.fill( (0, 0, 0) )
    # draw some tracked lines
    dist = math.sqrt((finger1[0] - finger2[0])**2 + (finger1[1] - finger2[1])**2)
    pygame.draw.circle(surface=screen, color=player.color, center=((finger1[0]+finger2[0])/2, (finger1[1]+finger2[1])/2), radius=dist * r_portion, width=5)
    r_portion += 0.008
    pygame.draw.circle(surface=screen, color=player.color, center=finger1, radius=20, width=0)
    pygame.draw.circle(surface=screen, color=player.color, center=finger2, radius=20, width=0)
    if direction == 1: # vertical
        pygame.draw.line(surface=screen, color=player.color, start_pos=finger1, end_pos=finger2, width=5)
    elif direction == 2: # horizontal
        pygame.draw.line(surface=screen, color=player.color, start_pos=finger1, end_pos=finger2, width=5)
    elif direction == 3: # diagonal
        pygame.draw.line(surface=screen, color=player.color, start_pos=finger1, end_pos=finger2, width=5)
    # draw flame effect
    for i in range(2):
        # x1, y1, = 640, 360
        r1 = random.randint(4, 10)
        r2 = random.randint(4, 10)
        f1 = Fire(round(finger1[0]), round(finger1[1]), r1)
        f2 = Fire(finger2[0], finger2[1], r2)
        fire_group.add(f1)
        fire_group.add(f2)
    
    fire_group.update(screen)
    for fire in fire_group:
        if fire.radius <= 0:
            fire.kill()
    
    # Flip the display / Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of 60 frames per second
    clock.tick(60)
    

# activate te wand
player.wand_activated = True
client.publish(f"IDD/player{player_id}/activate", f'{player.color[0]},{player.color[1]},{player.color[2]}')
# Additional HP bar
myhealth = healthWidget(surface=screen, x=25, y=20, title="YOU")
myhealth.x[CURRENT] = -70
opponenthealth = healthWidget(surface=screen, x=1170, y=20, title="ENEMY")
opponenthealth.x[CURRENT] = 1280
# spawn the magic circle
magic_circle_angle = 0
alpha_overlay = 0
shield_alpha = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            # Was it the Escale key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_d:
                alpha_overlay = 240
            if event.key == K_s:
                shield_alpha = 240
                
    detection = track.detectLeftHandAngle()
    if not detection == None:
        magic_circle_angle = detection
    
    player_stat_update()

    screen.fill( (0, 0, 0) )
    player.magic_circle.setAngle(magic_circle_angle)
    player.magic_circle.draw()
    fire_group.update(screen)
    for fire in fire_group:
        if fire.radius <= 0:
            fire.kill()
    
    transparent_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
    transparent_surface.fill((255, 0, 0, alpha_overlay))
    screen.blit(transparent_surface, (0, 0))
    shield_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
    shield_surface.fill((player.color[0], player.color[1], player.color[2], shield_alpha))
    screen.blit(shield_surface, (0, 0))
    # pygame.draw.rect(screen, color=(255, 0, 0, alpha_overlay), rect=pygame.Rect(0, 0, 1280, 720), width=0)
    if alpha_overlay > 0 and not player.is_dead:
        alpha_overlay -= 30
    if shield_alpha > 0:
        shield_alpha -= 30
    
    # update HP bars
    myhealth.setProgress(player.health)
    # the opponent health bar will be set via callback functions
    if player.magic_circle.ring_body.r_ring1[CURRENT] == player.magic_circle.ring_body.r_ring1[EXPECTED]:
        myhealth.draw()
        opponenthealth.draw()
        # send current focus
        client.publish(f"IDD/player{player_id}/currentfocus", ",".join([str(int(x)) for x in player.magic_circle.getFocused()]))
    
    # Flip the display / Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of60 frames per second
    clock.tick(60)



pygame.quit()
    
