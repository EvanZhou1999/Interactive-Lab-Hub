import paho.mqtt.client as mqtt
import random
import time
import uuid
import ssl
from time import strftime, sleep
from datetime import datetime
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import socket
from datetime import datetime

# Get the hostname
hostname = socket.gethostname()
# Get the IP address
ip_address = socket.gethostbyname(hostname)
player_id = ip_address.replace(".", "")

potato_phrases = [
    "Caught you!",
    "Whoops, hot potato!",
    "Aha, it's yours now!",
    "Gotcha!",
    "You're it!",
    "Tag, you're the spud holder!",
    "Pass it quick!",
    "Potato alert!",
    "You're the chosen one!",
    "Hot potato incoming!",
    "Ready, set, pass!",
    "It's in your court now!",
    "Time to pass the heat!",
    "You've got the sizzling spud!",
    "Potato power to you!",
    "On fire with the potato!",
    "Quick, pass the heat!",
    "Hot potato, hot hands!",
    "The hot potato's with you!"
]

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

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

server = "farlab.infosci.cornell.edu"
gamestart = False

def speak_sentence(sentence):
    subprocess.check_output(f'./googletts_arg.sh "{sentence}"', shell=True, stderr=subprocess.PIPE, universal_newlines=True)

def on_connect(client, userdata, flags, rc):
    print(">> MQTT CLIENT CONNECTED")
    print(f">> connected with result code {rc}")
    client.subscribe('IDD/#')

def on_message(cleint, userdata, msg):
    global gamestart
    # print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
    if msg.topic == "IDD/nextpotato":
        pass
    if msg.topic == "IDD/potatogamestart":
        updatedisplay("no_potato")
        gamestart = True
    if msg.topic == "IDD/nextpotato":
        potatoid = msg.payload.decode('UTF-8')
        # print("YOUR POTATO?")
        if potatoid == player_id:
            # print("YOUR POTATO!")
            updatedisplay("potato")
            speak_sentence(random.choice(potato_phrases))
        else:
            updatedisplay["no_potato"]
    if msg.topic == "IDD/potatoboom":
        potatoid = msg.payload.decode('UTF-8')
        if potatoid == player_id:
            updatedisplay("boom")
            time.sleep(0.5)
            speak_sentence("BOOM!!! Game over!")

def updatedisplay(filename):
    background_image = Image.open(f'img_assets/{filename}.png')
    image.paste(background_image, (0, 0))
    disp.image(image, rotation)
    
    
# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set(cert_reqs=ssl.CERT_NONE)
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')
client.on_connect = on_connect
client.on_message = on_message
#connect to the broker
client.connect(server,port=8883)
client.loop_start()

time.sleep(1)
print(player_id)

updatedisplay("player_ready_waiting")
player_ready = False
while not player_ready:
    if (not buttonA.value) or (not buttonB.value):
        client.publish("IDD/playerready", player_id)
        speak_sentence("Player Ready")
        player_ready = True

updatedisplay("player_ready")

while not gamestart:
    pass

while gamestart:
    if not buttonA.value:
        client.publish("IDD/playeranswer", f'{player_id},2,{datetime.now().timestamp()}')
        while not buttonA.value:
            pass
    if not buttonB.value:
        client.publish("IDD/playeranswer", f'{player_id},1,{datetime.now().timestamp()}')
        while not buttonB.value:
            pass


