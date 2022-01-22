
# # uses 
# from HaMqttDevice import *


# # Set up devices
# f016th_1_device = Device.from_config("devices/F016TH_1.yaml")
# f016th_1_device = Device.from_config("devices/F016TH_2.yaml")
# ft020t_device = Device.from_config("devices/FT020T.yaml")

# f016th_1_temperature_sensor = Sensor(
#     mqtt_client,
#     "Indoor Temperature 1",
#     parent_device=f016th_1_device,
#     unit_of_measurement="°C",
#     topic_parent_level="inside",
# )

# f016th_1_humidity_sensor = Sensor(
#     mqtt_client,
#     "Indoor Humidity 1",
#     parent_device=f016th_1_device,
#     unit_of_measurement="%",
#     topic_parent_level="inside",
# )

# f016th_2_temperature_sensor = Sensor(
#     mqtt_client,
#     "Indoor Temperature 2",
#     parent_device=f016th_2_device,
#     unit_of_measurement="°C",
#     topic_parent_level="inside",
# )

# f016th_2_humidity_sensor = Sensor(
#     mqtt_client,
#     "Indoor Humidity 2",
#     parent_device=f016th_2_device,
#     unit_of_measurement="%",
#     topic_parent_level="inside",
# )

# outside_temperature_sensor = Sensor(
#     mqtt_client,
#     "Outside Temperature",
#     parent_device=ft020t_device,
#     unit_of_measurement="°C",
#     topic_parent_level="outside",
# )

# Discoery topics
# https://www.home-assistant.io/docs/mqtt/discovery/

# Topic format <discovery_prefix>/<component>/[<node_id>/]<object_id>/config

