#include <Arduino.h>

// Import WiFi Libraries
#include <WiFi.h>
#include <HTTPClient.h>
#include <esp_wpa2.h>
#include <esp_wifi.h>
#include <ESPmDNS.h>
#include "wireless_config.h"
#include <iostream>
#include <string>
// Import MQTT
#include <PubSubClient.h>
using namespace std;


#define VIBRATION_MOTOR_PIN 18
#define MOTOR_CHANNEL 1
#define STRENGTH_SOFT 80
#define STRENGTH_MILD 160
#define STRENGTH_HIGH 250
#define VIBRATION_SETTING_ADDR 1

#define PLAYER_ID 1
#define OPPONENT_ID 2


const char* mqtt_server = "10.56.6.114";
WiFiClient espClient;
PubSubClient client(espClient);
int player_health = 100;

int rr = 0;
int gg = 255;
int bb = 0;


#include <Adafruit_NeoMatrix.h>
#include <Adafruit_GFX.h>
#include <Adafruit_NeoPixel.h>

#define PIN 10
#define MATRIX_WIDTH 32
#define MATRIX_HEIGHT 8

// Modify the matrix layout here for zigzag pattern
Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(MATRIX_WIDTH, MATRIX_HEIGHT, PIN,
  NEO_MATRIX_TOP + NEO_MATRIX_LEFT + NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB + NEO_KHZ800);

void updateHealthBar(int health) {
  int ledCount = (health * MATRIX_WIDTH) / 100; // Calculate the number of LEDs to represent health

  matrix.fillScreen(0); // Clear the matrix

  for (int y = 0; y < MATRIX_HEIGHT; y++) {
    for (int x = 0; x < MATRIX_WIDTH; x++) {
      if (x < ledCount) {
        // Change color based on health value
        if (health > 66) {
          matrix.drawPixel(x, y, matrix.Color(0, 255, 0)); // Green for high health
        } else if (health > 33) {
          matrix.drawPixel(x, y, matrix.Color(255, 255, 0)); // Yellow for medium health
        } else {
          matrix.drawPixel(x, y, matrix.Color(255, 0, 0)); // Red for low health
        }
      }
    }
  }

  matrix.show(); // Update the display
}

void displayAdvancedTimeStoneEffect(int frame) {
  matrix.fillScreen(0); // Clear the matrix

  for (int x = 0; x < MATRIX_WIDTH; x++) {
    for (int y = 0; y < MATRIX_HEIGHT; y++) {
      // Calculate distance from the middle of the matrix
      int dist = abs(MATRIX_HEIGHT / 2 - y);

      // Create a vertically moving swirling pattern based on y-coordinate and frame
      int swirl = (frame - dist * 2) % MATRIX_HEIGHT;

      // Set color and intensity based on swirl position
      if (swirl < 8) {
        int intensity = 255 - (swirl * 32);
        uint32_t color = matrix.Color(intensity / 3, intensity, intensity / 4); // Mystical green with hints of other colors
        matrix.drawPixel(x, y, color);
      }
    }
  }
}

void displayTimeStoneEffect(int frame) {
  matrix.fillScreen(0); // Clear the matrix

  for (int x = 0; x < MATRIX_WIDTH; x++) {
    for (int y = 0; y < MATRIX_HEIGHT; y++) {
      // Calculate distance from the center of the effect
      int dist = abs(MATRIX_WIDTH- x) + abs(MATRIX_HEIGHT / 2 - y);

      // Create a swirling pattern based on frame and distance
      int swirl = (frame - dist * 2) % 20;

      // Set color and intensity based on swirl position
      if (swirl < 8) {
        int intensity = 255 - (swirl * 32);
        uint32_t color = matrix.Color(intensity / 3, intensity, intensity / 4); // Mystical green with hints of other colors
        matrix.drawPixel(x, y, color);
      }
    }
  }
}

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

int findIndexOfOnes(String data) {
  int startIndex = 0;
  while (startIndex < data.length()) {
    int index = data.indexOf("1", startIndex);

    // Check if '1' is found
    if (index == -1) {
      break; // Exit if no more '1' is found
    }

    // Check if '1' is a standalone number or part of another number
    if ((index == 0 || data.charAt(index - 1) == ',') &&
        (index == data.length() - 1 || data.charAt(index + 1) == ',')) {
      return index; // Return the index of '1'
      // Serial.println(index); // Print the index of '1'
    }

    // Move to the next part of the string
    startIndex = index + 1;
  }
}


void fillPixels(uint16_t (*coordinates)[2], int size, uint16_t color) {
  for(int i = 0; i < size; i++) {
    int x = coordinates[i][0];
    int y = coordinates[i][1];
    matrix.drawPixel(x, y, color);
  }
}

/// Funtion to display the shield spell on the led Matrix
void displayShield(uint16_t color){
  matrix.fillScreen(0);
  uint16_t coordinates[][2] = {{16, 0}, {15, 0}, {14, 0}, {13, 0}, {17, 0}, {18, 0}, {19, 0}, {13, 1}, {13, 2}, {13, 3}, {13, 4}, {14, 5}, {15, 6}, {16, 7}, {19, 1}, {19, 2}, {19, 3}, {19, 4}, {18, 5}, {17, 6}} ;
  fillPixels(coordinates, 20, color); // Passing the color white
  matrix.show();
}

/// Function to display the pulse magic spell on the led Matrix
void displayPulseMagic(uint16_t color){
  matrix.fillScreen(0);
  uint16_t coordinates[][2] = {{16, 0}, {16, 1}, {16, 2},{21, 6},{16, 7},{14, 2},{14, 3},{14, 5},{15, 1}, {15, 2}, {15, 3}, {15, 6}, {13, 3}, {13, 4}, {12, 4}, {12, 5}, {17, 1}, {17, 2}, {17, 3}, {17, 6}, {18, 2}, {18, 3}, {18, 5}, {19, 3}, {19, 4}, {20, 4}, {20, 5}, {21, 5}, {11, 5}, {11,6}} ;
  fillPixels(coordinates, 30, color); // Passing the color white
  matrix.show();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    // if (client.connect("ESP8266Client", "public", "public")) {
    if (client.connect(("FeatherClient" + PLAYER_ID))) {
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
        client.subscribe("IDD/player1/currentfocus");
      } else if (PLAYER_ID == 2){
        client.subscribe("IDD/player2/activate");
        client.subscribe("IDD/player2/beam/start");
        client.subscribe("IDD/player2/beam/end");
        client.subscribe("IDD/player2/shield/start");
        client.subscribe("IDD/player2/shield/end");
        client.subscribe("IDD/player2/pulse/start");
        client.subscribe("IDD/player2/specialattack/start");
        client.subscribe("IDD/player2/hit");
        client.subscribe("IDD/player2/currentfocus");
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

/// Function to show red twice on the led Matrix when hit by opponent
void hit(int r, int g, int b) {
  matrix.fillScreen(matrix.Color(r,g,b));
  matrix.show();
  delay(150);
  matrix.fillScreen(0);
  matrix.show();
  delay(150);
  matrix.fillScreen(matrix.Color(r,g,b));
  matrix.show();
  delay(150);
  matrix.fillScreen(0);
  matrix.show();
}

static int frame = 0;
static int frameBeam = 0;


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

    rr = red;
    gg = green; 
    bb = blue;
    // wand_color[0] = red;
    // wand_color[1] = green;
    // wand_color[2] = blue;

    // matrix print text with small font


    Serial.print("Updated Wand Color: ");
    Serial.println(String(red) + "  " + String(green) + "  " + String(blue));
    matrix.fillScreen(0);
    matrix.setCursor(14, 1); 
    matrix.setTextColor(matrix.Color(red, green, blue));
    // matrix.fillScreen(matrix.Color(red,green,blue));
    // matrix.setTextColor(matrix.Color(0, 0, 0));
    matrix.print(F("1"));
    matrix.show();
  } else if (String(topic).equals(("IDD/player" + String(PLAYER_ID) + "/hit"))) {
    Serial.println(messageTemp);
    // Find the positions of commas
    int comma1 = messageTemp.indexOf(',');
    int comma2 = messageTemp.lastIndexOf(',');
    player_health = messageTemp.toInt();
    hit(255, 0, 0);
    matrix.show();
  } else if (String(topic).equals(("IDD/player" + String(PLAYER_ID) + "/currentfocus"))) {
    Serial.println(messageTemp);
    // In MQTT message IDD/player1/currentfocus (0,0,0,0,0) Indices represent which spell is currently selected
    if (messageTemp[4] == '1') {
      displayShield(matrix.Color(rr, gg, bb));
    } else if (messageTemp[2] == '1') {
      displayPulseMagic(matrix.Color(rr, gg, bb));
    } else if (messageTemp[6] == '1') {
      displayTimeStoneEffect(frame);
      matrix.show();
      delay(30); // Adjust for desired speed of the effect
      frame++;
    } else if (messageTemp[0] == '1') {
      displayAdvancedTimeStoneEffect(frameBeam);
      matrix.show();
      delay(50); // Adjust for desired speed of the effect

      frameBeam++;
      // displayBeamMagic(matrix.Color(rr, gg, bb));
    } else if (messageTemp[8] == '1') {
      updateHealthBar(player_health);
      // matrix.fillScreen(matrix.Color(rr, gg, bb));
      // matrix.show();
    }
  }
}

void shiftGridUp() {
  // Buffer to store the first row
  uint32_t buffer[MATRIX_WIDTH];

  // Read and store the first row
  for (int x = 0; x < MATRIX_WIDTH; x++) {
    buffer[x] = matrix.getPixelColor(x + MATRIX_WIDTH * (MATRIX_HEIGHT - 1));
  }

  // Shift all pixels up by one row
  for (int y = MATRIX_HEIGHT - 1; y > 0; y--) {
    for (int x = 0; x < MATRIX_WIDTH; x++) {
      uint32_t color = matrix.getPixelColor(x + MATRIX_WIDTH * (y - 1));
      matrix.drawPixel(x, y, color);
    }
  }

  // Draw the first row on the bottom
  for (int x = 0; x < MATRIX_WIDTH; x++) {
    matrix.drawPixel(x, 0, buffer[x]);
  }
}

void initializeMatrix() {
  // Example: Fill the matrix with a color or pattern
  matrix.fillScreen(matrix.Color(0, 255, 0)); // Green color
  matrix.show();
}

void setup() {
  matrix.begin();
  matrix.setBrightness(255);
  Serial.begin(115200);
  initializeMatrix();
  bool connectionSuccess;
  if (UseWAPEnterprise) {
    connectionSuccess = connectWifi_WAP2_Enterprise();
  }else{
    connectionSuccess = connectWifi_WAP2_Personal();
  }
  if (connectionSuccess){
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
    matrix.fillScreen(0);
    matrix.setCursor(0, 1);
    matrix.print(F("Eduroam"));
    matrix.setTextColor(matrix.Color(0, 0, 0));
    matrix.show();
    delay(1000);
  }
}




const uint16_t colors[] = {matrix.Color(255, 0, 0), matrix.Color(0, 255, 0), matrix.Color(0, 0, 255) };

int x    = matrix.width();
int pass = 0;


void loop() {


  if (!client.connected()) {
    matrix.fillScreen(0);
    matrix.setCursor(0, 1);
    matrix.print(F("hold Up"));
    matrix.setTextColor(matrix.Color(0, 0, 0));
    matrix.show();
    delay(2000);
    reconnect();
  }
  client.loop();
}
