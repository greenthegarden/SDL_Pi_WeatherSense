# (c) Andreas Philipp - 2021
#  andreas.philipp@anphi.de


import time
from random import uniform

from paho.mqtt.client import Client

from ha_mqtt.ha_device import HaDevice
from ha_mqtt.mqtt_device_base import MqttDeviceBase, MqttDeviceSettings
from ha_mqtt.mqtt_sensor import MqttSensor
from ha_mqtt.mqtt_thermometer import MqttThermometer
from ha_mqtt.util import HaDeviceClass

# instantiate an paho mqtt client and connect to the mqtt server
client = Client("testscript")
client.connect("localhost", 1883)
client.loop_start()


dev = HaDevice("FT16", "Indoor Sensor 1")
dev_hum = MqttDeviceSettings("FT16_1_hum", "hum1", client)
dev_temp = MqttDeviceSettings("FT16_1_temp", "temp1", client)
sens_hum = MqttSensor(dev_hum, "%", HaDeviceClass.HUMIDITY)
sens_temp = MqttSensor(dev_temp, "°C", HaDeviceClass.TEMPERATURE)
# instantiate an MQTTThermometer object
# th = MqttThermometer(dev_set, "°C")

try:
    while True:
        # publish a random "temperature" every 5 seconds
        temp = f"{uniform(-10, 10):2.2f}"
        print(
            f"publishing temperature: {temp} {sens_temp.unit_of_measurement}")
        sens_temp.publish_state(temp)
        sens_hum.publish_state(34)
        time.sleep(5)

except KeyboardInterrupt:
    pass
finally:
    # close the device for cleanup. Gets marked as offline/unavailable in homeassistant
    sens_hum.close()
    sens_temp.close()
    client.loop_stop()
    client.disconnect()
