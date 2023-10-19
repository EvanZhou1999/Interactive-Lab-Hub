# Sound Source:
# https://freepats.zenvoid.org/index.html
# Keyword: Soundfont, 

import pygame as pg
import time

pg.mixer.init()
pg.init()

a1Note = pg.mixer.Sound("./sound_samples/HV_60.wav")
#a1Note.set_volume(0.1)
a2Note = pg.mixer.Sound("./sound_samples/HV_64.wav")
#a2Note.set_volume(0.1)
a3Note = pg.mixer.Sound("./sound_samples/HV_67.wav")
#a3Note.set_volume(0.1)


pg.mixer.set_num_channels(50)

key_sound_map = {
    pg.K_w: a1Note,
    pg.K_s: a2Note,
    pg.K_x: a3Note,
}

# for i in range(5):
#     a1Note.play()
#     time.sleep(0.3)
#     a2Note.play()
#     time.sleep(0.3)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key in key_sound_map:
                key_sound_map[event.key].play()
            elif event.key == pygame.K_q:  # Check for the 'Q' key
                running = False  # Exit the program when 'Q' is pressed


pg.quit()
