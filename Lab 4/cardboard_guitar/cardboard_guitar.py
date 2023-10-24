import time
import os
import sys
import board
import busio
import adafruit_mpr121
import pygame as pg
# import qwiic_led_stick
# import random

i2c = busio.I2C(board.SCL, board.SDA)
pad1 = adafruit_mpr121.MPR121(i2c) # 0x5a
pad2 = adafruit_mpr121.MPR121(i2c, address=0x5b)
pg.mixer.init()

# my_stick = qwiic_led_stick.QwiicLEDStick()

# if my_stick.begin() == False:
#     print("\nThe Qwiic LED Stick isn't connected to the sytsem. Please check your connection", \
#         file=sys.stderr)
# else:
#     print("\nLED Stick ready!")

# my_stick.set_all_LED_brightness(15)

sound_file_mappins = [
    ["HV_64", "HV_65", "HV_66", "HV_67"],  # E
    ["HV_59", "HV_60", "HV_61", "HV_62"],  # B
    ["HV_55", "HV_56", "HV_57", "HV_58"],  # G
    ["HV_50", "HV_51", "HV_52", "HV_53"],  # D
    ["HV_45", "HV_46", "HV_47", "HV_48"],  # A
    ["HV_40", "HV_41", "HV_42", "HV_43"]   # Low E
]

sensor_mapping = [
    [pad1[5], pad1[6], pad2[11], pad2[0]], # E
    [pad1[4], pad1[7], pad2[10], pad2[1]], # B
    [pad1[3], pad1[8], pad2[9], pad2[2]],  # G
    [pad1[2], pad1[9], pad2[8], pad2[3]],  # D
    [pad1[1], pad1[10], pad2[7], pad2[4]], # A
    [pad1[0], pad1[11], pad2[6], pad2[5]]  # Low E
]

prev_value_mapping = []
current_value_mapping = []


def sensor_update():
    global prev_value_mapping
    global current_value_mapping
    
    out = [-1, -1, -1, -1, -1, -1] # -1 means not triggered, [0] = E, [5] = Low E
    # get sensor_mapping  updates
    prev_value_mapping = current_value_mapping.copy()
    current_value_mapping = [[col.value for  col in columns] for columns in sensor_mapping]
    
    for i in range(len(out)): # [0] = E, [5] = Low E
        # first detect whether to activate it 
        # looking into [3] column
        if current_value_mapping[i][3] and not prev_value_mapping[i][3]:
            # Then look are the first occurance of the pressing
            out[i] = 0
            for j in range(2, -1, -1):
                if current_value_mapping[i][j]:
                    out[i] = j+1
                    break   
    
    return out

def debug_value_mapping():
    out = sensor_update()
    for i in current_value_mapping:
        print(i)
    for j in out:
        print(j)
    print()



# initialize sounds
sound_maps = [[ pg.mixer.Sound(f'./guitar_sound_samples/{sound_file_mappins[i][j]}.wav') for j in range(4)] for i in range(6)]

pg.mixer.set_num_channels(50)

while True:
    out = sensor_update()
    for string, fret in enumerate(out):
        if not fret == -1:
            sound_maps[string][fret].play()
            #my_stick.set_all_LED_color(random.randint(0, 220), random.randint(0, 220), random.randint(0, 220))

    #time.sleep(0.1)
    