from teachable_machine_lite import TeachableMachineLite
import cv2 as cv
import time
from time import strftime, sleep
from datetime import datetime
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

cap = cv.VideoCapture(0)

model_path = 'detect.tflite'
image_file_name = "frame.jpg"
labels_path = "labelmap.txt"

tm_model = TeachableMachineLite(model_path=model_path, labels_file_path=labels_path)

# Button configuration
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(255, 255, 255))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Prepare Fonts
Sans = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
Sans_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf", 35)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

items = ["headphone", "neutral", "laptop", "charger", "box"]
detected_items = []

def display_success(text):
    draw.rectangle((0, 0, width, height), outline=0, fill=(255, 255, 255))
    checkmark = Image.open(f'program_img/checkmark.png')
    image.paste(checkmark, (0, 0), checkmark)
    draw.text((10, 80), f'Found {text}', font=Sans, fill="#000000")
    disp.image(image, rotation) 
    speak_sentence(f'found {text}')
    
    time.sleep(1)

def speak_sentence(sentence):
    subprocess.check_output(f'./googletts_arg.sh "{sentence}"', shell=True, stderr=subprocess.PIPE, universal_newlines=True)
    

speak_sentence("Let's start packing, dont forget your laptop, headphone, charger, and the IDD box!")

while True:
    ret, frame = cap.read()
    # cv.imshow('Cam', frame)
    cv.imwrite(image_file_name, frame)
    
    results = tm_model.classify_frame(image_file_name)
    # print("results:",results)
    # print(results['label'])
    # print(results['id'])
    
    if (not results['id'] == 1) and (not items[results['id']] in detected_items): # neutral
        detected_items.append(items[results['id']])
        display_success(results['label'])
    
    # draw background
    draw.rectangle((0, 0, width, height), outline=0, fill=(255, 255, 255))
    background_image = Image.open(f'program_img/itembackgrounds.png')
    image.paste(background_image, (0, 0), background_image)
    
    # draw what's in the detected_items
    for item_name in detected_items:
        item_image = Image.open(f'program_img/{item_name}.png')
        image.paste(item_image, (0, 0), item_image)
    
    disp.image(image, rotation)
    k = cv.waitKey(1)
    if k% 255 == 27:
        # press ESC to close camera view.
        break
    
    if (len(detected_items) == 4):
        time.sleep(1)
        speak_sentence("Great Job! You've found everything")
        break