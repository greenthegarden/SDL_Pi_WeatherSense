#  Copyright (c) 2022 - Andreas Philipp
#  This code is published under the MIT license

# (c) Andreas Philipp - 2021
#  andreas.philipp@anphi.de

# simple demo script for a MQTT controlled switch
# The device registers itself in homeassistant via the homeassistant
# MQTT discovery protocol and shows up as switch
# when the device is switched on or off the accordingly callbacks are called
# on() and off() in this example


import time

from paho.mqtt.client import Client

from ha_mqtt.ha_device import HaDevice
from ha_mqtt.mqtt_device_base import MqttDeviceSettings
from ha_mqtt.mqtt_switch import MqttSwitch

# instantiate an paho mqtt client and connect to the mqtt server
client = Client("testscript")
client.connect("localhost", 1883)
client.loop_start()


# create device info dictionary
dev = HaDevice("Testdevice", "test123456-veryunique")
dev.add_config_option(settings: MqttDeviceSettings, unit: str="°C", send_only=True)
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    # close the device for cleanup. Gets marked as offline/unavailable in homeassistant
    client.loop_stop()
    client.disconnect()
