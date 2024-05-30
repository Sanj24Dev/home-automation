import paho.mqtt.client as mqtt
import time
import struct	
import csv	
import datetime

# finding checksum to cross check the data
def checkSum(n, len):
    checksum = 0
    for i in range(1,len):
        checksum ^= n[i]
    return checksum

# creating and opening csv files to log data
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
pgvFile = timestamp + ' pgv.csv'
encFile = timestamp + ' encoder.csv'
pgv = open(pgvFile, 'w', newline = '')
enc = open(encFile, 'w', newline = '')
pgvWriter = csv.writer(pgv)
encWriter = csv.writer(enc)

# writing the header in csv files
data = [["timestamp", "lpos", "rpos"]]
encWriter.writerows(data)
data = [["timestamp", "id", "x", "y", "z", "th"]]
pgvWriter.writerows(data)

# subscribing to PGV and ENC topics
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to topics upon connection
    client.subscribe("PGV")
    client.subscribe("ENC")

# function to handle PGV Feedback
def handle_PGVFeedback(n):
        id = struct.unpack('<H', n[3:5])[0]
        if id == 0xFFFF and n[2] == 2:
            print("Invalid")
            return 
        x = struct.unpack('<H', n[5:7])[0]
        y = struct.unpack('<H', n[7:9])[0]
        z = struct.unpack('<H', n[9:11])[0]
        th = struct.unpack('<H', n[11:13])[0]
        print("id: ",id, "  x: ",x, "  y: ", y, "  z: ", z, "  th: ", th)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = [[timestamp,id,x,y,z,th]]
        pgvWriter.writerows(data)

# function to handle Encoder Feedback
def handle_encoderFeedback(n):
    lpos = struct.unpack('<f', n[2:6])[0]
    rpos = struct.unpack('<f', n[6:10])[0]
    print("lpos: ", lpos, "   rpos: ", rpos)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [[timestamp, lpos, rpos]]
    encWriter.writerows(data)

# function to handle different messages of different topics
def on_message(client, userdata, msg):
    if msg.topic == "PGV":
        handle_PGVFeedback(msg.payload)
    elif msg.topic == "ENC":
        handle_encoderFeedback(msg.payload)


# main code
mqttBroker ="mqtt.eclipseprojects.io"
client = mqtt.Client("Logger")
client.connect(mqttBroker) 

client.loop_start()
client.subscribe("PGV")
client.subscribe("ENC")
client.on_message=on_message 
try:
    # mention the time in seconds to collect the data
    # will run for an hour
    time.sleep(3600)
except KeyboardInterrupt:
    pgv.close()
    enc.close()
client.loop_stop()