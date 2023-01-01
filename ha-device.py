from HaMqttDevice import *

mqtt_client = mqtt.Client("user")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.username_pw_set("user", "pass")
mqtt_client.connect("mqtt.mqtt.ru", 1883, 60)
mqtt_client.loop_forever()

example_device = Device.from_config("example_device.yaml")

inside_temperature_sensor = Sensor(
    mqtt_client,
    "Temperature 1",
    parent_device=example_device,
    unit_of_measurement="°C",
    topic_parent_level="inside",
)

outside_temperature_sensor = Sensor(
    mqtt_client,
    "Temperature 2",
    parent_device=example_device,
    unit_of_measurement="°C",
    topic_parent_level="outside",
)

inside_temperature_sensor.send(22)
outside_temperature_sensor.send(5)
