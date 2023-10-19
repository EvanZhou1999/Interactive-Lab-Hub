import time
import sys
import board
import busio
import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)
pad1 = adafruit_mpr121.MPR121(i2c) # 0x5a
pad2 = adafruit_mpr121.MPR121(i2c, address=0x5b)


while True:
    if pad1[1].value:
        print("Pin 1 touched! ")
    if pad1[2].value:
        print("Pin 2 touched! ")
    if pad1[3].value:
        print("Pin 3 touched! ")
    if pad1[4].value:
        print("Pin 4 touched! ")
    if pad2[1].value:
        print("Pin 1 touched! ")
    if pad2[2].value:
        print("Pin 2 touched! ")
    if pad2[3].value:
        print("Pin 3 touched! ")
    if pad2[4].value:
        print("Pin 4 touched! ")
    
    time.sleep(0.1)