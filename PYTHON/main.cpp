#include <Arduino.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <WebSocketsClient.h>
#include <SocketIOClient.h>
#include <Hash.h>
#include <SimpleDHT.h>

#define SSID "Alesya Sinitsa"
#define PASSWORD "12345678"
#define ADDR "172.20.10.3"
#define PORT 5001

#define pinDHT11 2
#define pinLOCK 0
#define pinCOFFEE 16
#define pinLIGHT1 14
#define pinLIGHT2 4
#define pinLIGHT3 5
#define pinLIGHT 12

SocketIOclient webSocket;

SimpleDHT11 dht11(pinDHT11);

byte temperature = 0;
byte humidity = 0;

byte light;
byte light1;
byte light2;
byte light3;
byte lock;
byte coffee;

void getData(uint8_t *json, size_t length)
{
  DynamicJsonDocument data(1024);
  deserializeJson(data, json, length);
  String type = data[0];
  JsonObject content = data[1];
  Serial.print("\nПришло сообщение: ");
  Serial.println(type);
  if (type == "light")
  {
    light = content["status"];
    Serial.print("Свет изменён на: ");
    Serial.println(light);
  }
  if (type == "light1")
  {
    light1 = content["status"];
    Serial.print("Свет изменён на: ");
    Serial.println(light1);
  }
  if (type == "light2")
  {
    light2 = content["status"];
    Serial.print("Свет изменён на: ");
    Serial.println(light2);
  }
  if (type == "light3")
  {
    light3 = content["status"];
    Serial.print("Свет изменён на: ");
    Serial.println(light3);
  }
  if (type == "lock")
  {
    lock = content["status"];
    Serial.print("Дверь изменена на: ");
    Serial.println(lock);
  }
  if (type == "coffee")
  {
    coffee = content["status"];
    Serial.print("Кофе: ");
    Serial.println(coffee);
  }
}

void sendAuth()
{
  webSocket.sendEVENT("[\"auth\", {\"name\": \"esp\"}]");
  Serial.println("\nsendAuth");
}

void sendAllData(byte temperature, byte humidity, byte light, byte light1, byte light2, byte light3, byte lock, byte coffee)
{
  DynamicJsonDocument doc(1024);
  JsonArray array = doc.to<JsonArray>();

  array.add("data_sensors");

  JsonObject data = array.createNestedObject();
  data["air_temp"] = temperature;
  data["humidity"] = humidity;
  data["light"] = light;
  data["light1"] = light1;
  data["light2"] = light2;
  data["light3"] = light3;
  data["lock"] = lock;
  data["coffee"] = coffee;
  String output;
  serializeJson(doc, output);

  webSocket.sendEVENT(output);
  Serial.print("\nОтправлены данные: ");
  Serial.println(output);
}

void socketIOEvent(socketIOmessageType_t type, uint8_t *payload, size_t length)
{
  switch (type)
  {
  case sIOtype_DISCONNECT:
    Serial.println("[IOc] Disconnected!\n");
    break;
  case sIOtype_CONNECT:
    Serial.println("[IOc] Connected");
    webSocket.send(sIOtype_CONNECT, "/");
    sendAuth();
    break;
  case sIOtype_EVENT:
    Serial.print("[IOc] get event: %s\n ");
    getData(payload, length);
    break;
  case sIOtype_ACK:
    Serial.println("[IOc] get ack: %u\n");
    hexdump(payload, length);
    break;
  case sIOtype_ERROR:
    Serial.println("[IOc] get error: %u\n");
    hexdump(payload, length);
    break;
  case sIOtype_BINARY_EVENT:
    Serial.println("[IOc] get binary: %u\n");
    hexdump(payload, length);
    break;
  case sIOtype_BINARY_ACK:
    Serial.println("[IOc] get binary ack: %u\n");
    hexdump(payload, length);
    break;
  }
}

void connectToWifi()
{
  WiFi.begin(SSID, PASSWORD);
  Serial.print("\n\nConnecting to wi-fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("connected");
}

void initWebsockets()
{
  webSocket.setReconnectInterval(5000);
  webSocket.onEvent(socketIOEvent);
  webSocket.begin(ADDR, PORT, "/socket.io/?EIO=4");
}

void setup()
{
  Serial.begin(9600);
  pinMode(pinLIGHT, OUTPUT);
  pinMode(pinLIGHT1, OUTPUT);
  pinMode(pinLIGHT2, OUTPUT);
  pinMode(pinLIGHT3, OUTPUT);
  pinMode(pinLOCK, OUTPUT);
  pinMode(pinCOFFEE, OUTPUT);
  connectToWifi();
  initWebsockets();
}

void readSensor()
{
  byte temperatureNew;
  byte humidityNew;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperatureNew, &humidityNew, NULL)) != SimpleDHTErrSuccess)
  {
    Serial.print("Read DHT11 failed, err=");
    Serial.print(SimpleDHTErrCode(err));
    Serial.print(",");
    Serial.println(SimpleDHTErrDuration(err));
    return;
  }
  if (temperature != temperatureNew || humidityNew != humidity)
  {
    temperature = temperatureNew;
    humidity = humidityNew;
    sendAllData(temperature, humidity, light, light1, light2, light3, lock, coffee);
    Serial.print("Sample OK: ");
    Serial.print((int)temperature);
    Serial.print(" *C, ");
    Serial.print((int)humidity);
    Serial.println(" H");
  }
}

unsigned long timer;
byte flagLight;
byte flagLight1;
byte flagLight2;
byte flagLight3;
byte flagLock;
byte flagCoffee;
void loop()
{
  webSocket.loop();
  if (millis() - timer > 1000)
  {
    readSensor();
    timer = millis();
    if (flagLight != light)
    {
      flagLight = light;
      digitalWrite(pinLIGHT, flagLight);
    }
    if (flagLight1 != light1)
    {
      flagLight1 = light1;
      digitalWrite(pinLIGHT1, flagLight1);
    }
    if (flagLight2 != light2)
    {
      flagLight2 = light2;
      digitalWrite(pinLIGHT2, flagLight2);
    }
    if (flagLight3 != light3)
    { 
      flagLight3 = light3;
      digitalWrite(pinLIGHT3, flagLight3);
    }
    if (flagLock != lock)
    {
      flagLock = lock;
      digitalWrite(pinLOCK, flagLock);
    }
    if (flagCoffee != coffee)
    {
      flagCoffee = coffee;
      digitalWrite(pinCOFFEE, flagCoffee);
    }
  }
}