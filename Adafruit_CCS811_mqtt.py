from time import sleep
from Adafruit_CCS811 import Adafruit_CCS811
import paho.mqtt.client as mqtt
import json
import time
import math

# MQTT Broker Information
username = "BrokerUserName"
password = "BrokerPassword"

# Connect to broker
client = mqtt.Client()
client.username_pw_set(username, password=password)
client.connect("BrokerURL", port=1883, keepalive=60) 
client.loop_start()

ccs =  Adafruit_CCS811()
co2 = 0
tvoc = 0
sensor_data = {'unixtime':0 ,'eco2':0, 'tvoc':0, 'temp':0} #Build the json object

while not ccs.available():
        pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0

if ccs.available():
	temp = ccs.calculateTemperature()
	temp = (temp * 9.0/5.0) + 32
	if not ccs.readData():
	      co2 = ccs.geteCO2()
	      tvoc = ccs.getTVOC()
	      sensor_data['unixtime'] = round(time.time(), 0)
	      sensor_data['eco2'] = co2
	      sensor_data['tvoc'] = tvoc
	      sensor_data['temp'] = temp
	      #print(json.dumps(sensor_data))
	      client.publish('mqttTopicName', json.dumps(sensor_data), qos=1)
	else:
              print "ERROR!"
              while(1):
                pass


client.loop_stop()
client.disconnect()
