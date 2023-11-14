import paho.mqtt.client as mqtt
import csv
import random
import time
import uuid
import ssl
import threading
from colorama import Fore, Back, Style, init
from datetime import datetime

# Initialize colorama on Windows
init()

server = "farlab.infosci.cornell.edu"
numplayers = 0
player_ids = []
player_answers = []
potatoholder = "0"

def load_questions_from_csv(file_name):
    questions = []
    with open(file_name, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            questions.append({
                "question": row['questiontext'],
                "choice1": row['choice1'],
                "choice2": row['choice2'],
                "correct_choice": int(row['correct_id'])  # Convert to int if necessary
            })
    return questions

def timer_function(duration):
    time.sleep(duration)
    global game_in_progress
    game_in_progress = False

def on_connect(client, userdata, flags, rc):
    print(">> MQTT CLIENT CONNECTED")
    print(f">> connected with result code {rc}")
    client.subscribe('IDD/#')

def on_message(cleint, userdata, msg):
    # print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
    if msg.topic == "IDD/playerready":
        id = msg.payload.decode('UTF-8')
        player_ids.append(id)
        print(f'player {id} has joined')
    if msg.topic == "IDD/playeranswer":
        data = msg.payload.decode('UTF-8').split(",")
        for ans in player_answers:
            if data[0] == ans[0]:
                return
        print(data)
        player_answers.append(data)

print("\n\n")
print(Fore.CYAN + "========================================")
print(Fore.YELLOW + "MQTT HOT POTATO GAME !!!")
print(Fore.CYAN + "========================================")
print(Style.RESET_ALL)
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
print(f'>> TO: {server}')
print("\n")

numplayers = int(input(">> Enter the number of players: "))
while numplayers <= 0:
    print(Fore.RED + ">> [ERROR] Number of players must be greater than zero")
    print(Style.RESET_ALL)
    numplayers = int(input(">> Enter the number of players: "))
print(Fore.GREEN + f'\n [Confirmed: {numplayers} players]')
print(Style.RESET_ALL)


print(Fore.CYAN + "========================================")
print(Fore.YELLOW + "WAITING FOR PLAYERS TO JOIN")
print(Fore.CYAN + "========================================")
print(Style.RESET_ALL)
print("Joined players: ")
while not len(player_ids) == numplayers:
    print(Fore.GREEN + f'>>> {len(player_ids)}', end='\r')
print(Style.RESET_ALL)
client.publish("IDD/potatogamestart", "none")


print(Fore.CYAN + "========================================")
print(Fore.YELLOW + "GAME START!")
print(Fore.CYAN + "========================================")
print(Style.RESET_ALL)
print(">> Randomly assign potato in .....")
time.sleep(1)
print(">> 3......")
time.sleep(1)
print(">> 2....")
time.sleep(1)
print(">> 1..")
time.sleep(1)
print(Fore.GREEN + ">> !!POTATO DISTRIBUTED!!")
print(Style.RESET_ALL)

# randomly assign potato
potatoholder = random.choice(player_ids)
client.publish("IDD/nextpotato", potatoholder)


time.sleep(1)
# load questions
questions = load_questions_from_csv('questions.csv')
game_in_progress = True

# set timer
timevalue = random.randint(35, 90)
print(f'time remaining: {timevalue} seconds')
timer = threading.Thread(target=timer_function, args=(timevalue,))
timer.start()

print(Fore.CYAN + "========================================")
print(Fore.YELLOW + "TIME BEGIN! GET RID OF YOUR POTATO")
print(Fore.CYAN + "========================================")
print(Style.RESET_ALL)

while game_in_progress:
    question = random.choice(questions)
    print("========================================\n")
    print(Fore.YELLOW + question["question"])
    print(Fore.RED + f'A: {question["choice1"]}       ' + Fore.CYAN + f'B: {question["choice2"]}')
    print(Style.RESET_ALL + " ")
    print("========================================")
    while not len(player_answers) == numplayers:
        if not game_in_progress:
            break
    if not game_in_progress:
        break
    # now start pick the next player to throw the potato
    players_correct = []
    players_wrong = []
    for player in player_answers:
        if player[1] == question["correct_choice"]:
            players_correct.append(player)
        else:
            players_wrong.append(player)
            
    players_wrong = sorted(players_wrong, key=lambda x: x[2], reverse=True)
    if players_wrong:
        potatoholder = players_wrong[-1][0]  # Selecting the slowest wrong answer player
    else:
        # If no wrong answers, select the slowest among all players
        player_answers = sorted(player_answers, key=lambda x: x[2], reverse=True)
        potatoholder = player_answers[0][0]
    
    client.publish("IDD/nextpotato", potatoholder)
    player_answers = []
    print(Fore.GREEN + f'Correct Answer: {question["choice1"] if question["correct_choice"] == 1 else question["choice2"]}')
    for i in range(50):
        time.sleep(0.01)
        if not game_in_progress:
            break
    print(Fore.CYAN + f'======================================================== {potatoholder} has the potato !')
    print(Style.RESET_ALL)

client.publish("IDD/potatoboom", potatoholder)
print(Fore.CYAN + "========================================")
print(Fore.YELLOW + "TIME IS UP!!!")
print(Fore.RED + f"Player: {potatoholder} is OUT")
print(Fore.CYAN + "========================================")
print(Style.RESET_ALL)


time.sleep(1)
        
            
    



    






