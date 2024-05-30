#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <string.h>
#include <stdlib.h>
const char* ssid = "Accio_2.4G";
const char* password =  "accio@123";
const char* mqtt_server = "mqtt.eclipseprojects.io";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() 
{
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.print("Connected to WiFi :");
  Serial.println(WiFi.SSID());
  client.setServer(mqtt_server, mqtt_port);
  while (!client.connected()) 
  {
    Serial.println("Connecting to MQTT...");
    if (client.connect("client-ptl-mqtt","sanjanaAccio","password"))
    {
      Serial.println("connected");
    }
    else
    {
      Serial.print("failed with state ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

void loop() 
{
  const int temp = rand() % 10;
  // generate temp values - send it to mqtt server - generate graphs
  char message[10];
  sprintf(message, "%d", temp);
  client.publish("temp", message);
  delay(5000);
  client.loop();
}
