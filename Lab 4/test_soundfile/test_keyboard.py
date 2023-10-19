# python3 -m pip install sparkfun-qwiic-keypad
import time
import sys
import board
import busio
import adafruit_mpr121
import qwiic_keypad


i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)
myKeypad = qwiic_keypad.QwiicKeypad()

if myKeypad.is_connected() == False:
    print("The Qwiic Keypad device isn't connected to the system. Please check your connection", \
        file=sys.stderr)
    exit()

myKeypad.begin()

def getkeypad():
    button = 0 
    button = myKeypad.get_button()
 
    if button == -1:
        print("No keypad detected")
        time.sleep(1)
    if button != 0:
        charButton = chr(button)
        print(charButton)
    else:
        print('keypad empty')
    
while True:
    myKeypad.update_fifo() 
    if mpr121[1].value:
        print("Pin 1 touched!   ", end="")
        getkeypad()
    if mpr121[2].value:
        print("Pin 2 touched!   ", end="")
        getkeypad()
    if mpr121[3].value:
        print("Pin 3 touched!   ", end="")
        getkeypad()
    if mpr121[4].value:
        print("Pin 4 touched!   ", end="")
        getkeypad()
    
    time.sleep(0.1)