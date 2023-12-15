#include <Arduino.h>
// ===========================================================
// This is the header file for storing wireless configurations
// ===========================================================


// WiFi - Configuration
//===================================================
const char* ssid = "";
const char* password = "";
//===================================================

// WiFi - WAP2 Enterprise Configuration
// set this to true if you want to connect to eduroam
// set this to false if you want to connect to other Wi-Fi
bool UseWAPEnterprise = true;
//===================================================
const char* WAP2_SSID = "eduroam";
const char* EAP_IDENTITY = "xxxxx@cornell.edu";
const char* EAP_PASSWORD = "";
//===================================================


// new Mac Address (not used)
// !!Becareful with reuse this code and cause duplicated Mac Address!!
uint8_t newMACAddress[] = {0x32, 0xAE, 0xA4, 0x07, 0x0D, 0x66};

// Server Configuration
// Once domain/Host name is changed, wait sometime for it to propagate (1-2h)
const char* domainName = "magicWand01";
