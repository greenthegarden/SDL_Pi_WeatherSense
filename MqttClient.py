import config

from paho.mqtt import publish
from paho.mqtt.client import Client

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# instantiate an paho mqtt client and connect to the mqtt server
client = Client("WeatherSenseMonitor")
client.on_connect = on_connect
client.connect(config.MQTThost, config.MQTTport)
client.loop_start()
