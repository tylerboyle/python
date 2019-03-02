import paho.mqtt.client as mqtt
import json
import time
import math
import psutil

# MQTT Broker Information
username = "BrokerUserName"
password = "BrokerPassword"

# Connect to the broker
client = mqtt.Client()
client.username_pw_set(username, password=password)
client.connect("YourBrokerURL", port=1883, keepalive=60)
client.loop_start()

sensor_data = {'unixtime':0, 'cpu_utilization':0, 'mem_percent_used':0} # First build the 'json' variable

sensor_data['unixtime'] = round(time.time(), 0)
sensor_data['cpu_utilization'] = psutil.cpu_percent()
sensor_data['mem_percent_used'] = psutil.virtual_memory().percent
client.publish('YourBrokerTopic', json.dumps(sensor_data), qos=0)
#print(json.dumps(sensor_data))

client.loop_stop()
client.disconnect()
