#include <Arduino.h>
#include <Wire.h>
#include "Qwiic_LED_Stick.h"
#include <Adafruit_MPU6050.h>

// Import WiFi Libraries
#include <WiFi.h>
#include <HTTPClient.h>
#include <esp_wpa2.h>
#include <esp_wifi.h>
//#include <ESPAsyncWebServer.h>
// Import DNS Library
#include <ESPmDNS.h>
// Import wireless configurations
#include "wireless_config.h"

// Import MQTT
#include <PubSubClient.h>

#define VIBRATION_MOTOR_PIN 18
#define MOTOR_CHANNEL 1
#define STRENGTH_SOFT 80
#define STRENGTH_MILD 160
#define STRENGTH_HIGH 250
#define VIBRATION_SETTING_ADDR 1

// const char* mqtt_server = "public.cloud.shiftr.io";
// const char* mqtt_server = "broker.hivemq.com";
const char* mqtt_server = "10.56.6.114";


// PLAYER CONFIGS
#define PLAYER_ID 2
#define OPPONENT_ID 1


/*
 * =======================================================
 * Instantiate Global Objects/Devices
 * =======================================================
 */
LED LEDStick; //Create an object of the LED class
Adafruit_MPU6050 mpu;
WiFiClient espClient;
PubSubClient client(espClient);

/*
 * =======================================================
 * Global Variables
 * =======================================================
 */
sensors_event_t acc, gyro, temp;
sensors_event_t acc_prev, gyro_prev, temp_prev;
int wand_color[] = {255, 0, 255};
int player_health = 100;


/*
 * =======================================================
 * Callback Functions
 * =======================================================
 */

void display_health(){
  LEDStick.LEDOff();
  int index = int(player_health) / int(10) + 1;
  for (int i = 0; i < index; i++){
    LEDStick.setLEDColor(i, wand_color[0]/255*15, wand_color[1]/255*15, wand_color[2]/255*15);
    vTaskDelay(80 / portTICK_PERIOD_MS);
  }
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Parse topics
  //if (String(topic) == ("IDD/player" + String(PLAYER_ID) + "/activate")) {
  if (String(topic).equals(("IDD/player" + String(PLAYER_ID) + "/activate"))) {
    Serial.println(messageTemp);
    // Find the positions of commas
    int comma1 = messageTemp.indexOf(',');
    int comma2 = messageTemp.lastIndexOf(',');

    // Extract substrings between commas
    int red = messageTemp.substring(0, comma1).toInt();
    int green = messageTemp.substring(comma1 + 1, comma2).toInt();
    int blue = messageTemp.substring(comma2 + 1).toInt();

    wand_color[0] = red;
    wand_color[1] = green;
    wand_color[2] = blue;

    Serial.print("Updated Wand Color: ");
    Serial.println(String(wand_color[0]) + "  " + String(wand_color[1]) + "  " + String(wand_color[2]));
    player_health = 100;
    display_health();
  } else if (String(topic).equals(("IDD/player" + String(PLAYER_ID) + "/beam/start"))) {
    ledcWrite(MOTOR_CHANNEL, 250);
    // animate
    for (int i=0; i<11; i++){
      LEDStick.setLEDColor(i, wand_color[0]/255*200, wand_color[1]/255*200, wand_color[2]/255*200);
      vTaskDelay(20 / portTICK_PERIOD_MS);
    }

  } else if (String(topic).equals(("IDD/player" + String(PLAYER_ID) + "/beam/end"))) {
    ledcWrite(MOTOR_CHANNEL, 0);
    for (int i=0; i<11; i++){
      LEDStick.setLEDColor(i, 0, 0, 0);
      vTaskDelay(20 / portTICK_PERIOD_MS);
    }
    display_health();
  
  } else if (String(topic).equals(("IDD/player" + String(PLAYER_ID) + "/shield/start"))) {
    ledcWrite(MOTOR_CHANNEL, 250);
    // animate
    LEDStick.setLEDColor( 100, 200, 200);
  
  } else if (String(topic).equals(("IDD/player" + String(PLAYER_ID) + "/shield/end"))) {
    ledcWrite(MOTOR_CHANNEL, 0);
    display_health();
  
  } else if (String(topic).equals(("IDD/player" + String(PLAYER_ID) + "/pulse/start"))) {
    ledcWrite(MOTOR_CHANNEL, 250);
    // animate
    LEDStick.setLEDColor(1, wand_color[0]/255*200, wand_color[1]/255*200, wand_color[2]/255*200);
    for (int i=1; i<11; i++){
      LEDStick.setLEDColor(i-1, 0, 0, 0);
      LEDStick.setLEDColor(i, wand_color[0]/255*200, wand_color[1]/255*200, wand_color[2]/255*200);
      vTaskDelay(20 / portTICK_PERIOD_MS);
    }
    ledcWrite(MOTOR_CHANNEL, 0);
    display_health();
  
  } else if (String(topic).equals(("IDD/player" + String(PLAYER_ID) + "/specialattack/start"))) {
    ledcWrite(MOTOR_CHANNEL, 250);
    LEDStick.setLEDColor(wand_color[0]/255*200, wand_color[1]/255*200, wand_color[2]/255*200);
    vTaskDelay(100 / portTICK_PERIOD_MS);
    ledcWrite(MOTOR_CHANNEL, 0);
    display_health();
  
  } else if (String(topic).equals(("IDD/player" + String(PLAYER_ID) + "/hit"))) {
    for (int i=0; i<3; i++){
      ledcWrite(MOTOR_CHANNEL, 250);
      LEDStick.setLEDColor(0, 0, 0);
      vTaskDelay(100 / portTICK_PERIOD_MS);
      ledcWrite(MOTOR_CHANNEL, 0);
      LEDStick.setLEDColor(200, 0, 0);
      vTaskDelay(100 / portTICK_PERIOD_MS);
      mpu.getEvent(&acc, &gyro, &temp);
      if (gyro.gyro.z > 4){
          if (PLAYER_ID == 1){
            client.publish("IDD/player1/spellcast", "");
          } else if (PLAYER_ID == 2){
            client.publish("IDD/player2/spellcast", "");
          }
      }
    }
    int newhealth = messageTemp.toInt();
    player_health = newhealth;
    // display_health();
  }
}

/*
 * =======================================================
 * Functions
 * =======================================================
 */

bool connectWifi_WAP2_Personal() {
    /*
    //ESP32 As access point
      WiFi.mode(WIFI_AP); //Access Point mode
      WiFi.softAP(ssid, password);
    */
    WiFi.mode(WIFI_STA);
    //Serial.print("MAC address >> ");
    //Serial.println(WiFi.macAddress());
    WiFi.begin(ssid, password);
    // Make Sure Wifi is connected
    float timeout = 0.0;
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("Connecting to WiFi...");
        timeout += 0.5;
        if (timeout > 30){ // timeout is set to 30 seconds
            return false;
        }
    }
    Serial.println("Connected to the WiFi network");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    delay(500);

    return true;
}

bool connectWifi_WAP2_Enterprise() {
    // Set NULL WiFi mode for hostname change
    WiFi.mode(WIFI_MODE_NULL);
    // Set host name
    WiFi.disconnect(true);
    delay(1000);
    //WiFi.config(INADDR_NONE, INADDR_NONE, INADDR_NONE, INADDR_NONE);
    WiFi.setHostname(domainName); // have to do this everytime since new host name won't be remembered
    // Set ESP32 to sation mode
    WiFi.mode(WIFI_MODE_STA);
    // Change mac address if needed
    //esp_wifi_set_mac(WIFI_IF_STA, &newMACAddress[0]);
    // Configure enterprise network
    esp_wifi_sta_wpa2_ent_set_identity((uint8_t *)EAP_IDENTITY, strlen(EAP_IDENTITY));
    esp_wifi_sta_wpa2_ent_set_username((uint8_t *)EAP_IDENTITY, strlen(EAP_IDENTITY));
    esp_wifi_sta_wpa2_ent_set_password((uint8_t *)EAP_PASSWORD, strlen(EAP_PASSWORD));
    esp_wifi_sta_wpa2_ent_enable();
    // Start connection
    WiFi.begin(WAP2_SSID);
    // Make Sure Wifi is connected
    float timeout = 0.0;
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("Connecting to WiFi...");
        timeout += 0.5;
        if (timeout > 30){ // timeout is set to 30 seconds
            return false;
        }
    }
    Serial.println("Connected to the WiFi network");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    delay(500);
    Serial.print("Host Name >> ");
    Serial.println(WiFi.getHostname());

    return true;
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    // if (client.connect("ESP8266Client", "public", "public")) {
    if (client.connect(("ESP32Client" + PLAYER_ID))) {
      Serial.println("connected");
      // Subscribe
      if (PLAYER_ID == 1){
        client.subscribe("IDD/player1/activate");
        client.subscribe("IDD/player1/beam/start");
        client.subscribe("IDD/player1/beam/end");
        client.subscribe("IDD/player1/shield/start");
        client.subscribe("IDD/player1/shield/end");
        client.subscribe("IDD/player1/pulse/start");
        client.subscribe("IDD/player1/specialattack/start");
        client.subscribe("IDD/player1/hit");
      } else if (PLAYER_ID == 2){
        client.subscribe("IDD/player2/activate");
        client.subscribe("IDD/player2/beam/start");
        client.subscribe("IDD/player2/beam/end");
        client.subscribe("IDD/player2/shield/start");
        client.subscribe("IDD/player2/shield/end");
        client.subscribe("IDD/player2/pulse/start");
        client.subscribe("IDD/player2/specialattack/start");
        client.subscribe("IDD/player2/hit");
      }
      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}



/*
 * =======================================================
 * Setup Function
 * =======================================================
 */
void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  Wire.setClock(400000);
  Serial.begin(115200);

  // Setup Device Vibration Motor
  // Configure PWM functionalities: PWMChannel(0-15), Signal Frequency, Duty Cycle resolution
  ledcSetup(MOTOR_CHANNEL, 5000, 8); 
  // Attach the channel to the GPIO to e controlled
  ledcAttachPin(VIBRATION_MOTOR_PIN, MOTOR_CHANNEL); // Pin and channel

  // Start up communication with the LED Stick
  if (LEDStick.begin() == false){
    Serial.println("Qwiic LED Stick failed to begin. Please check wiring and try again!");
    while(1);
  }
  // Start up MPU6050
  if (!mpu.begin()) {
    Serial.println("Sensor init failed");
    while (1)
      yield();
  }
  Serial.println("Found a MPU-6050 sensor");
  mpu.getEvent(&acc, &gyro, &temp);

  Serial.println("Qwiic LED Stick ready!");
  //turn off all LEDs
  LEDStick.LEDOff();

  ledcWrite(MOTOR_CHANNEL, 250);
  vTaskDelay(500 / portTICK_PERIOD_MS);
  ledcWrite(MOTOR_CHANNEL, 0);

  // Connect to Wifi
  bool connectionSuccess;
  if (UseWAPEnterprise) {
      connectionSuccess = connectWifi_WAP2_Enterprise();
  }else{
      connectionSuccess = connectWifi_WAP2_Personal();
  }

  if (connectionSuccess){
    LEDStick.setLEDColor(0, 100, 0);
    // Connect to MQTT Broker
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
  } else {
    LEDStick.setLEDColor(100, 0, 0);
  }

  vTaskDelay(2000 / portTICK_PERIOD_MS);
  LEDStick.LEDOff();
}


/*
 * =======================================================
 * Loop Function
 * =======================================================
 */
void loop() {
  // check MQTT and loop once
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  // Publish Example: client.publish("esp32/humidity", humString);

  // Acquire sensor readings
  acc_prev = acc;
  gyro_prev = gyro;
  temp_prev = temp;
  mpu.getEvent(&acc, &gyro, &temp);
  // Serial.println(acc.acceleration.y);
  Serial.println(gyro.gyro.z);

  // detect spell casting motion
  if (gyro.gyro.z > 4){
      if (PLAYER_ID == 1){
        client.publish("IDD/player1/spellcast", "");
      } else if (PLAYER_ID == 2){
        client.publish("IDD/player2/spellcast", "");
      }
      // ledcWrite(MOTOR_CHANNEL, 250);
      // LEDStick.setLEDColor(wand_color[0]/255*200, wand_color[1]/255*200, wand_color[2]/255*200);
      while (gyro.gyro.z > 4){
        acc_prev = acc;
        gyro_prev = gyro;
        temp_prev = temp;
        mpu.getEvent(&acc, &gyro, &temp);
      }
  }

  // detect spell cancel motion
  if (gyro.gyro.z < -2){
      if (PLAYER_ID == 1){
        client.publish("IDD/player1/spellcancel", "");
      } else if (PLAYER_ID == 2){
        client.publish("IDD/player2/spellcancel", "");
      }
      // ledcWrite(MOTOR_CHANNEL, 0);
      // LEDStick.setLEDColor(wand_color[0]/255*15, wand_color[1]/255*15, wand_color[2]/255*15);
      while (gyro.gyro.z < -4){
        acc_prev = acc;
        gyro_prev = gyro;
        temp_prev = temp;
        mpu.getEvent(&acc, &gyro, &temp);
      }
  }

  vTaskDelay(10 / portTICK_PERIOD_MS);
}

