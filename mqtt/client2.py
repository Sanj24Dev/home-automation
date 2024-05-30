import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

mqttBroker ="mqtt.eclipseprojects.io" 

client = mqtt.Client("Voltage")
client.connect(mqttBroker) 

while True:
    randNumber = uniform(10.0, 11.0)
    client.publish("PGV", randNumber)
    print("Just published " + str(randNumber) + " to topic PGV")
    time.sleep(1)