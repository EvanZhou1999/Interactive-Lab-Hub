# Little Interactions Everywhere

**NAMES OF COLLABORATORS HERE**

Siddharth Kothari - sk2793
Neelraj Patil - njp75
Yifan Zhou - yz2889
Tahmid Kazi - tk596
Omar Mohamed - om84

## Prep

1. Pull the new changes from the class interactive-lab-hub. (You should be familiar with this already!)
2. Install [MQTT Explorer](http://mqtt-explorer.com/) on your laptop. If you are using Mac, MQTT Explorer only works when installed from the [App Store](https://apps.apple.com/app/apple-store/id1455214828).
3. Readings before class:
   * [MQTT](#MQTT)
   * [The Presence Table](https://dl.acm.org/doi/10.1145/1935701.1935800) and [video](https://vimeo.com/15932020)


## Overview

The point of this lab is to introduce you to distributed interaction. We have included some Natural Language Processing (NLP) and Generation (NLG) but those are not really the emphasis. Feel free to dig into the examples and play around the code which you can integrate into your projects if wanted. However, we want to emphasize that the grading will focus on your ability to develop interesting uses for messaging across distributed devices. Here are the four sections of the lab activity:

A) [MQTT](#part-a)

B) [Send and Receive on your Pi](#part-b)

C) [Streaming a Sensor](#part-c)

D) [The One True ColorNet](#part-d)

E) [Make It Your Own](#part-)

## Part 1.

### Part A
### MQTT

MQTT is a lightweight messaging portal invented in 1999 for low bandwidth networks. It was later adopted as a defacto standard for a variety of [Internet of Things (IoT)](https://en.wikipedia.org/wiki/Internet_of_things) devices. 

#### The Bits

* **Broker** - The central server node that receives all messages and sends them out to the interested clients. Our broker is hosted on the far lab server (Thanks David!) at `farlab.infosci.cornell.edu/8883`. Imagine that the Broker is the messaging center!
* **Client** - A device that subscribes or publishes information to/on the network.
* **Topic** - The location data gets published to. These are *hierarchical with subtopics*. For example, If you were making a network of IoT smart bulbs this might look like `home/livingroom/sidelamp/light_status` and `home/livingroom/sidelamp/voltage`. With this setup, the info/updates of the sidelamp's `light_status` and `voltage` will be store in the subtopics. Because we use this broker for a variety of projects you have access to read, write and create subtopics of `IDD`. This means `IDD/ilan/is/a/goof` is a valid topic you can send data messages to.
*  **Subscribe** - This is a way of telling the client to pay attention to messages the broker sends out on the topic. You can subscribe to a specific topic or subtopics. You can also unsubscribe. Following the previouse example of home IoT smart bulbs, subscribing to `home/livingroom/sidelamp/#` would give you message updates to both the light_status and the voltage.
* **Publish** - This is a way of sending messages to a topic. Again, with the previouse example, you can set up your IoT smart bulbs to publish info/updates to the topic or subtopic. Also, note that you can publish to topics you do not subscribe to. 


**Important note:** With the broker we set up for the class, you are limited to subtopics of `IDD`. That is, to publish or subcribe, the topics will start with `IDD/`. Also, setting up a broker is not much work, but for the purposes of this class, you should all use the broker we have set up for you!


#### Useful Tooling

Debugging and visualizing what's happening on your MQTT broker can be helpful. We like [MQTT Explorer](http://mqtt-explorer.com/). You can connect by putting in the settings from the image below.


![input settings](imgs/mqtt_explorer.png?raw=true)


Once connected, you should be able to see all the messages under the IDD topic. , go to the **Publish** tab and try publish something! From the interface you can send and plot messages as well. Remember, you are limited to subtopics of `IDD`. That is, to publish or subcribe, the topics will start with `IDD/`.


<img width="1026" alt="Screen Shot 2022-10-30 at 10 40 32 AM" src="https://user-images.githubusercontent.com/24699361/198885090-356f4af0-4706-4fb1-870f-41c15e030aba.png">



### Part B
### Send and Receive on your Pi

[sender.py](./sender.py) and and [reader.py](./reader.py) show you the basics of using the mqtt in python. Let's spend a few minutes running these and seeing how messages are transferred and shown up. Before working on your Pi, keep the connection of `farlab.infosci.cornell.edu/8883` with MQTT Explorer running on your laptop.

**Running Examples on Pi**

* Install the packages from `requirements.txt` under a virtual environment:

  ```
  pi@raspberrypi:~/Interactive-Lab-Hub $ source circuitpython/bin/activate
  (circuitpython) pi@raspberrypi:~/Interactive-Lab-Hub $ cd Lab\ 6
  (circuitpython) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 6 $ pip install -r requirements.txt
  ...
  ```
* Run `sender.py`, fill in a topic name (should start with `IDD/`), then start sending messages. You should be able to see them on MQTT Explorer.

  ```
  (circuitpython) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 6 $ python sender.py
  >> topic: IDD/AlexandraTesting
  now writing to topic IDD/AlexandraTesting
  type new-topic to swich topics
  >> message: testtesttest
  ...
  ```
* Run `reader.py`, and you should see any messages being published to `IDD/` subtopics. Type a message inside MQTT explorer and see if you can receive it with `reader.py`.

  ```
  (circuitpython) pi@raspberrypi:~ Interactive-Lab-Hub/Lab 6 $ python reader.py
  ...
  ```

<img width="890" alt="Screen Shot 2022-10-30 at 10 47 52 AM" src="https://user-images.githubusercontent.com/24699361/198885135-a1d38d17-a78f-4bb2-91c7-17d014c3a0bd.png">

**\*\*\*Consider how you might use this messaging system on interactive devices, and draw/write down 5 ideas here.\*\*\***

**Smart Home Control System**: Utilize MQTT to create a centralized control system for smart home devices like lights, thermostats, and security cameras. Users can send commands from a smartphone or computer to control these devices remotely. For example, turning off lights or adjusting the thermostat while away from home.

**Health Monitoring System**: Implement a health monitoring system for elderly or patients with special needs. Sensors can collect data like heart rate, temperature, or movement, and send this information via MQTT to caregivers or medical professionals. This system can trigger alerts in case of abnormal readings, ensuring timely medical attention.

**Industrial Automation**: In a manufacturing setting, MQTT can facilitate communication between different machines and sensors. This system can monitor machine performance, environmental conditions, or production progress, sending data to a central server. It can help in predictive maintenance, process optimization, and ensuring safety standards.

**Retail Customer Engagement**: Use MQTT in retail environments to enhance customer experience. Interactive displays can provide product information, promotions, or personalized recommendations based on customer input or behavior. MQTT can also be used for inventory tracking, updating display items based on stock levels.

**Educational Tools and Interactive Learning**: In an educational setting, MQTT can be used to create interactive learning experiences. For example, a science museum exhibit might include sensors and interactive displays where visitors' actions (like pressing a button or walking through a sensor-equipped doorway) trigger informative displays or change the exhibit in real-time.

### Part C
### Streaming a Sensor

We have included an updated example from [lab 4](https://github.com/FAR-Lab/Interactive-Lab-Hub/tree/Fall2021/Lab%204) that streams the [capacitor sensor](https://learn.adafruit.com/adafruit-mpr121-gator) inputs over MQTT. 

Plug in the capacitive sensor board with the Qwiic connector. Use the alligator clips to connect a Twizzler (or any other things you used back in Lab 4) and run the example script:

<p float="left">
<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="150" />
<img src="https://cdn-shop.adafruit.com/970x728/4210-02.jpg" height="150">
<img src="https://cdn-learn.adafruit.com/guides/cropped_images/000/003/226/medium640/MPR121_top_angle.jpg?1609282424" height="150"/>
<img src="https://media.discordapp.net/attachments/679721816318803975/823299613812719666/PXL_20210321_205742253.jpg" height="150">
</p>

 ```
 (circuitpython) pi@raspberrypi:~ Interactive-Lab-Hub/Lab 6 $ python distributed_twizzlers_sender.py
 ...
 ```

**\*\*\*Include a picture of your setup here: what did you see on MQTT Explorer?\*\*\***

![IMG_9180](https://github.com/omar-mokht/Interactive-Lab-Hub/assets/111816253/3cc06f6a-8576-47bf-aa19-362a947b00e9)

![IMG_9183](https://github.com/omar-mokht/Interactive-Lab-Hub/assets/111816253/b5e695c4-6f2b-4f60-8e65-2e1a080660f0)

**\*\*\*Pick another part in your kit and try to implement the data streaming with it.\*\*\***

![battery_data](https://github.com/omar-mokht/Interactive-Lab-Hub/assets/111816253/3b903ab5-6947-4e93-af0c-a7284a53ad3f)

**Link**: https://youtu.be/6dvJKqHLT6k

### Part D
### The One True ColorNet

It is with great fortitude and resilience that we shall worship at the altar of the *OneColor*. Through unity of the collective RGB, we too can find unity in our heart, minds and souls. With the help of machines, we can overthrow the bourgeoisie, get on the same wavelength (this was also a color pun) and establish [Fully Automated Luxury Communism](https://en.wikipedia.org/wiki/Fully_Automated_Luxury_Communism).

The first step on the path to *collective* enlightenment, plug the [APDS-9960 Proximity, Light, RGB, and Gesture Sensor](https://www.adafruit.com/product/3595) into the [MiniPiTFT Display](https://www.adafruit.com/product/4393). You are almost there!

<p float="left">
  <img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="150" />
  <img src="https://cdn-shop.adafruit.com/970x728/4210-02.jpg" height="150">
  <img src="https://cdn-shop.adafruit.com/970x728/3595-03.jpg" height="150">
</p>


The second step to achieving our great enlightenment is to run `color.py`. We have talked about this sensor back in Lab 2 and Lab 4, this script is similar to what you have done before! Remember to activate the `circuitpython` virtual environment you have been using during this semester before running the script:

 ```
 (circuitpython) pi@raspberrypi:~ Interactive-Lab-Hub/Lab 6 $ systemctl stop mini-screen.service
 (circuitpython) pi@raspberrypi:~ Interactive-Lab-Hub/Lab 6 $ python color.py
 ...
 ```

By running the script, wou will find the two squares on the display. Half is showing an approximation of the output from the color sensor. The other half is up to the collective. Press the top button to share your color with the class. Your color is now our color, our color is now your color. We are one.

(A message from the previous TA, Ilan: I was not super careful with handling the loop so you may need to press more than once if the timing isn't quite right. Also, I haven't load-tested it so things might just immediately break when everyone pushes the button at once.)

**\*\*\*Can you set up the script that can read the color anyone else publish and display it on your screen?\*\*\***




### Part E
### Make it your own

Find at least one class (more are okay) partner, and design a distributed application together based on the exercise we asked you to do in this lab.

**\*\*\*1. Explain your design\*\*\*** For example, if you made a remote controlled banana piano, explain why anyone would want such a thing.

**MQTT HOT POTATO GAME!**

This is a MQTT based Hot Potato + Trivia game, consisting of one host (game coordinator) and multiple clients (players). To start with, the host will randomly “throw” an explosive potato (yes it will explode within a randomly generated countdown) to a player, and display a list of trivia questions. Players will then compete the answer these questions by pressing buttons on their client device (raspberry pi), and the person that answers the wrong questions or is the slowest to respond will get the potato in the next round. 

When the timer ends (player doesn’t know when), whoever holds the potato will be eliminated. 

This is a fun game that supports any number of people, it is competitive and fun at the same time. And with the help of distributed MQTT network, anyone can join the game instantly with minimal setup. 


**\*\*\*2. Diagram the architecture of the system.\*\*\*** Be clear to document where input, output and computation occur, and label all parts and connections. For example, where is the banana, who is the banana player, where does the sound get played, and who is listening to the banana music?

![Slide1](https://github.com/omar-mokht/Interactive-Lab-Hub/assets/111816253/ee2a8cd4-8225-494a-81bc-1acfbc04e51d)

![Slide2](https://github.com/omar-mokht/Interactive-Lab-Hub/assets/111816253/c6bfcff2-dd16-4eba-bdc9-019269c9a174)

![Slide3](https://github.com/omar-mokht/Interactive-Lab-Hub/assets/111816253/874b91bd-04e8-4da4-946a-b86189d42325)

![Slide4](https://github.com/omar-mokht/Interactive-Lab-Hub/assets/111816253/8af51bea-1610-4ffb-b327-83ddd020850b)

**\*\*\*3. Build a working prototype of the system.\*\*\*** Do think about the user interface: if someone encountered these bananas somewhere in the wild, would they know how to interact with them? Should they know what to expect?

To bring the exhilarating game of Hot Potato into the digital realm, we've designed a dynamic prototype that merges technology with fun. This system centers around an MQTT host, running on a separate computer linked to a TV, creating an immersive visual experience. In our unique twist on the classic game, players engage in a fast-paced question-and-answer challenge. This setup becomes the heart of the game, showcasing both the intriguing questions and the players' responses in real-time on the screen. The excitement builds as the one who answers the slowest in each round finds themselves with the 'hot potato'

At the core of player interaction are the personalized Raspberry Pi units, each equipped with intuitive buttons and displays. These devices are not just functional but also visually captivating. We've crafted detailed vector images for various screens, making the gameplay both clear and engaging. One of these screens cleverly illustrates the button layout, guiding players on how to interact seamlessly with the game. The highlight of the interface is the 'boom' screen – a vibrant display that dramatically indicates who is currently caught with the digital 'hot potato'.

This user interface has been thoughtfully designed to be intuitive and engaging. Even if someone stumbled upon this device 'in the wild', they would find it inviting and easy to understand. It's designed to be self-explanatory, ensuring that players, regardless of their tech savvy, can dive right into the fun without confusion. The anticipation of the 'boom' and the thrill of the game are sure to create an unforgettable experience.


**\*\*\*4. Document the working prototype in use.\*\*\*** It may be helpful to record a Zoom session where you should the input in one location clearly causing response in another location.

**Link**: https://youtu.be/x9wKcUHqADo

<!--**\*\*\*5. BONUS (Wendy didn't approve this so you should probably ignore it)\*\*\*** get the whole class to run your code and make your distributed system BIGGER.-->
