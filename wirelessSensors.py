#
# wireless sensor routines


import config

import json
import random

import sys
from subprocess import PIPE, Popen, STDOUT
from threading import Thread
import datetime
import MySQLdb as mdb
import traceback
import state
import os
import util

import updateWeb

import aqi

from paho.mqtt import publish
from paho.mqtt.client import Client

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

# instantiate an paho mqtt client and connect to the mqtt server
client = Client("WeatherSenseMonitor")
client.on_connect = on_connect
client.connect("emqx.services.localdomain", 1883)
client.loop_start()

from ha_mqtt.ha_device import HaDevice
from ha_mqtt.mqtt_device_base import MqttDeviceBase, MqttDeviceSettings
from ha_mqtt.mqtt_sensor import MqttSensor
from ha_mqtt.mqtt_thermometer import MqttThermometer
from ha_mqtt.util import HaDeviceClass

# create device info dictionary
# weatherstation_ft020t = HaDevice("FT020T", "FT020T-weatherstation", send_only=True)
# # thermo_f016th_1 = HaDevice("F016TH Channel 1", "FT016TH-thermometer-01")
# thermo_f016th_2 = HaDevice("F016TH Channel 2", "FT016TH-thermometer-02")

dev_F016TH_ch1 = HaDevice("F016TH Thermo-Hygrometer Channel 1", "F016TH_ch1")
dev_F016TH_ch1.add_config_option("manufacturer", "SwitchDoc Labs")
dev_F016TH_ch1.add_config_option("model", "SwitchDoc Labs F016TH Thermo-Hygrometer")
dev_F016TH_ch1_batteryState = MqttDeviceSettings("F016TH Channel 1 Battery State", "F016TH_ch1_batteryState", client, dev_F016TH_ch1)
sensor_F016TH_ch1_batteryState = MqttSensor(dev_F016TH_ch1_batteryState, "", HaDeviceClass.BATTERY, send_only=True)
dev_F016TH_ch1_humidity = MqttDeviceSettings("F016TH Channel 1 Humidity", "F016TH_ch1_humidity", client, dev_F016TH_ch1)
sensor_F016TH_ch1_humidity = MqttSensor(dev_F016TH_ch1_humidity, "%", HaDeviceClass.HUMIDITY, send_only=True)
dev_F016TH_ch1_temperature = MqttDeviceSettings("F016TH Channel 1 Temperature", "F016TH_ch1_temperature", client, dev_F016TH_ch1)
sensor_F016TH_ch1_temperature = MqttSensor(dev_F016TH_ch1_temperature, "°C", HaDeviceClass.TEMPERATURE, send_only=True)

dev_F016TH_ch2 = HaDevice("F016TH Thermo-Hygrometer Channel 2", "F016TH_ch2")
dev_F016TH_ch2.add_config_option("manufacturer", "SwitchDoc Labs")
dev_F016TH_ch2.add_config_option("model", "SwitchDoc Labs F016TH Thermo-Hygrometer")
dev_F016TH_ch2_batteryState = MqttDeviceSettings("F016TH Channel 2 Battery State", "F016TH_ch2_batteryState", client, dev_F016TH_ch2)
sensor_F016TH_ch2_batteryState = MqttSensor(dev_F016TH_ch2_batteryState, "", HaDeviceClass.BATTERY, send_only=True)
dev_F016TH_ch2_humidity = MqttDeviceSettings("F016TH Channel 2 Humidity", "F016TH_ch2_humidity", client, dev_F016TH_ch2)
sensor_F016TH_ch2_humidity = MqttSensor(dev_F016TH_ch2_humidity, "%", HaDeviceClass.HUMIDITY, send_only=True)
dev_F016TH_ch2_temperature = MqttDeviceSettings("F016TH Channel 2 Temperature", "F016TH_ch2_temperature", client, dev_F016TH_ch2)
sensor_F016TH_ch2_temperature = MqttSensor(dev_F016TH_ch2_temperature, "°C", HaDeviceClass.TEMPERATURE, send_only=True)

dev_FT020T = HaDevice("FT020T", "FT020T")
dev_FT020T.add_config_option("manufacturer", "SwitchDoc Labs")
dev_FT020T.add_config_option("model", "SwitchDoc Labs FT020T AIO")
dev_FT020T_batteryState = MqttDeviceSettings("FT020T Battery State", "FT020T_batteryState", client, dev_FT020T)
sensor_FT020T_batteryState = MqttSensor(dev_FT020T_batteryState, "", HaDeviceClass.BATTERY, send_only=True)
dev_FT020T_cumulativeRain = MqttDeviceSettings("FT020T Cumulative Rain", "FT020T_cumulativeRain", client, dev_FT020T)
sensor_FT020T_cumulativeRain = MqttSensor(dev_FT020T_cumulativeRain, "mm", HaDeviceClass.PRECIPITATION, send_only=True)
dev_FT020T_humidity = MqttDeviceSettings("FT020T Humidity", "FT020T_humidity", client, dev_FT020T)
sensor_FT020T_humidity = MqttSensor(dev_FT020T_humidity, "%", HaDeviceClass.HUMIDITY, send_only=True)
dev_FT020T_light = MqttDeviceSettings("FT020T Light", "FT020T_light", client, dev_FT020T)
sensor_FT020T_light = MqttSensor(dev_FT020T_light, "klux", HaDeviceClass.ILLUMINANCE , send_only=True)
dev_FT020T_temperature = MqttDeviceSettings("FT020T Temperature", "FT020T_temperature", client, dev_FT020T)
sensor_FT020T_temperature = MqttSensor(dev_FT020T_temperature, "°C", HaDeviceClass.TEMPERATURE, send_only=True)
dev_FT020T_uv = MqttDeviceSettings("FT020T UV", "FT020T_uv", client, dev_FT020T)
sensor_FT020T_uv = MqttSensor(dev_FT020T_uv, "", HaDeviceClass.NONE, send_only=True)
dev_FT020T_windDirection = MqttDeviceSettings("FT020T Wind Direction", "FT020T_windDirection", client, dev_FT020T)
sensor_FT020T_windDirection = MqttSensor(dev_FT020T_windDirection, "°", HaDeviceClass.NONE, send_only=True)
dev_FT020T_windSpeedAvg = MqttDeviceSettings("FT020T Windspeed (Avg)", "FT020T_windSpeedAvg", client, dev_FT020T)
sensor_FT020T_windSpeedAvg = MqttSensor(dev_FT020T_windSpeedAvg, "m/s", HaDeviceClass.WIND_SPEED, send_only=True)
dev_FT020T_windSpeedGust = MqttDeviceSettings("FT020T Windspeed (Gust)", "FT020T_windSpeedGust", client, dev_FT020T)
sensor_FT020T_windSpeedGust = MqttSensor(dev_FT020T_windSpeedGust, "m/s", HaDeviceClass.WIND_SPEED, send_only=True)

dev_WeatherSenseAQI = HaDevice("WeatherSense Air Quality Sensor", "WeatherSenseAQI")
dev_WeatherSenseAQI.add_config_option("manufacturer", "SwitchDoc Labs")
dev_WeatherSenseAQI.add_config_option("model", "SwitchDoc Labs AQI")
dev_WeatherSenseAQI.add_config_option("sw_version", "3")
dev_WeatherSenseAQI_1_0_micron_particles_standard = MqttDeviceSettings("WeatherSenseAQI 1.0 micron particles (Standard)", "WeatherSenseAQI_1_0_micron_particles_standard", client, dev_WeatherSenseAQI)
sensor_WeatherSenseAQI_1_0_micron_particles_standard = MqttSensor(dev_WeatherSenseAQI_1_0_micron_particles_standard, "µg/m³", HaDeviceClass.PM1, send_only=True)
dev_WeatherSenseAQI_2_5_micron_particles_standard = MqttDeviceSettings("WeatherSenseAQI 2.5 micron particles (Standard)", "WeatherSenseAQI_2_5_micron_particles_standard", client, dev_WeatherSenseAQI)
sensor_WeatherSenseAQI_2_5_micron_particles_standard = MqttSensor(dev_WeatherSenseAQI_2_5_micron_particles_standard, "µg/m³", HaDeviceClass.PM25, send_only=True)
dev_WeatherSenseAQI_10_micron_particles_standard = MqttDeviceSettings("WeatherSenseAQI 10 micron particles (Standard)", "WeatherSenseAQI_10_micron_particles_standard", client, dev_WeatherSenseAQI)
sensor_WeatherSenseAQI_10_micron_particles_standard = MqttSensor(dev_WeatherSenseAQI_10_micron_particles_standard, "µg/m³", HaDeviceClass.PM10, send_only=True)
dev_WeatherSenseAQI_1_0_micron_particles_atmospheric = MqttDeviceSettings("WeatherSenseAQI 1.0 micron particles (Atmospheric)", "WeatherSenseAQI_1_0_micron_particles_atmospheric", client, dev_WeatherSenseAQI)
sensor_WeatherSenseAQI_1_0_micron_particles_atmospheric = MqttSensor(dev_WeatherSenseAQI_1_0_micron_particles_atmospheric, "µg/m³", HaDeviceClass.PM1, send_only=True)
dev_WeatherSenseAQI_2_5_micron_particles_atmospheric = MqttDeviceSettings("WeatherSenseAQI 2.5 micron particles (Atmospheric)", "WeatherSenseAQI_2_5_micron_particles_atmospheric", client, dev_WeatherSenseAQI)
sensor_WeatherSenseAQI_2_5_micron_particles_atmospheric = MqttSensor(dev_WeatherSenseAQI_2_5_micron_particles_atmospheric, "µg/m³", HaDeviceClass.PM25, send_only=True)
dev_WeatherSenseAQI_10_micron_particles_atmospheric = MqttDeviceSettings("WeatherSenseAQI 10 micron particles (Atmospheric)", "WeatherSenseAQI_10_micron_particles_atmospheric", client, dev_WeatherSenseAQI)
sensor_WeatherSenseAQI_10_micron_particles_atmospheric = MqttSensor(dev_WeatherSenseAQI_10_micron_particles_atmospheric, "µg/m³", HaDeviceClass.PM10, send_only=True)
dev_WeatherSenseAQI_AQI = MqttDeviceSettings("WeatherSenseAQI Air Quality Index", "WeatherSenseAQI_AQI", client, dev_WeatherSenseAQI)
sensor_WeatherSenseAQI_AQI = MqttSensor(dev_WeatherSenseAQI_AQI, "", HaDeviceClass.NONE, send_only=True)
dev_WeatherSenseAQI_batteryCurrent = MqttDeviceSettings("WeatherSenseAQI Battery Current", "WeatherSenseAQI_batteryCurrent", client, dev_WeatherSenseAQI)
sensor_WeatherSenseAQI_batteryCurrent = MqttSensor(dev_WeatherSenseAQI_batteryCurrent, "mA", HaDeviceClass.CURRENT , send_only=True)
dev_WeatherSenseAQI_batteryVoltage = MqttDeviceSettings("WeatherSenseAQI Battery Voltage", "WeatherSenseAQI_batteryVoltage", client, dev_WeatherSenseAQI)
sensor_WeatherSenseAQI_batteryVoltage = MqttSensor(dev_WeatherSenseAQI_batteryVoltage, "V", HaDeviceClass.VOLTAGE, send_only=True)
dev_WeatherSenseAQI_loadCurrent = MqttDeviceSettings("WeatherSenseAQI Load Current", "WeatherSenseAQI_loadCurrent", client, dev_WeatherSenseAQI)
sensor_WeatherSenseAQI_loadCurrent = MqttSensor(dev_WeatherSenseAQI_loadCurrent, "mA", HaDeviceClass.CURRENT , send_only=True)
dev_WeatherSenseAQI_loadVoltage = MqttDeviceSettings("WeatherSenseAQI Load Voltage", "WeatherSenseAQI_loadVoltage", client, dev_WeatherSenseAQI)
sensor_WeatherSenseAQI_loadVoltage = MqttSensor(dev_WeatherSenseAQI_loadVoltage, "V", HaDeviceClass.VOLTAGE, send_only=True)
dev_WeatherSenseAQI_solarCurrent = MqttDeviceSettings("WeatherSenseAQI Solar Current", "WeatherSenseAQI_solarCurrent", client, dev_WeatherSenseAQI)
sensor_WeatherSenseAQI_solarCurrent = MqttSensor(dev_WeatherSenseAQI_solarCurrent, "mA", HaDeviceClass.CURRENT , send_only=True)
dev_WeatherSenseAQI_solarVoltage = MqttDeviceSettings("WeatherSenseAQI Solar Voltage", "WeatherSenseAQI_solarVoltage", client, dev_WeatherSenseAQI)
sensor_WeatherSenseAQI_solarVoltage = MqttSensor(dev_WeatherSenseAQI_solarVoltage, "V", HaDeviceClass.VOLTAGE, send_only=True)

dev_SolarMAX = HaDevice("SolarMAX", "SolarMAX")
dev_SolarMAX.add_config_option("manufacturer", "SwitchDoc Labs")
dev_SolarMAX.add_config_option("model", "SwitchDoc Labs SolarMAX")
dev_SolarMAX.add_config_option("sw_version", "15")
dev_SolarMAX_batteryCurrent = MqttDeviceSettings("SolarMAX Battery Current", "SolarMAX_batteryCurrent", client, dev_SolarMAX)
sensor_SolarMAX_batteryCurrent = MqttSensor(dev_SolarMAX_batteryCurrent, "mA", HaDeviceClass.CURRENT , send_only=True)
dev_SolarMAX_batteryVoltage = MqttDeviceSettings("SolarMAX Battery Voltage", "SolarMAX_batteryVoltage", client, dev_SolarMAX)
sensor_SolarMAX_batteryVoltage = MqttSensor(dev_SolarMAX_batteryVoltage, "V", HaDeviceClass.VOLTAGE, send_only=True)
dev_SolarMAX_loadCurrent = MqttDeviceSettings("SolarMAX Load Current", "SolarMAX_loadCurrent", client, dev_SolarMAX)
sensor_SolarMAX_loadCurrent = MqttSensor(dev_SolarMAX_loadCurrent, "mA", HaDeviceClass.CURRENT , send_only=True)
dev_SolarMAX_loadVoltage = MqttDeviceSettings("SolarMAX Load Voltage", "SolarMAX_loadVoltage", client, dev_SolarMAX)
sensor_SolarMAX_loadVoltage = MqttSensor(dev_SolarMAX_loadVoltage, "V", HaDeviceClass.VOLTAGE, send_only=True)
dev_SolarMAX_solarCurrent = MqttDeviceSettings("SolarMAX Solar Current", "SolarMAX_solarCurrent", client, dev_SolarMAX)
sensor_SolarMAX_solarCurrent = MqttSensor(dev_SolarMAX_solarCurrent, "mA", HaDeviceClass.CURRENT , send_only=True)
dev_SolarMAX_solarVoltage = MqttDeviceSettings("SolarMAX Solar Voltage", "SolarMAX_solarVoltage", client, dev_SolarMAX)
sensor_SolarMAX_solarVoltage = MqttSensor(dev_SolarMAX_solarVoltage, "V", HaDeviceClass.VOLTAGE, send_only=True)
dev_SolarMAX_internalHumidity = MqttDeviceSettings("SolarMAX Internal Humidity", "SolarMAX_internalHumidity", client, dev_SolarMAX)
sensor_SolarMAX_internalHumidity = MqttSensor(dev_SolarMAX_internalHumidity, "%", HaDeviceClass.HUMIDITY , send_only=True)
dev_SolarMAX_internalTemperature = MqttDeviceSettings("SolarMAX Internal Temperature", "SolarMAX_internalTemperature", client, dev_SolarMAX)
sensor_SolarMAX_internalTemperature = MqttSensor(dev_SolarMAX_internalTemperature, "°C", HaDeviceClass.TEMPERATURE, send_only=True)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

# cmd = [ '/usr/local/bin/rtl_433', '-q', '-F', 'json', '-R', '147']
cmd = ['/usr/local/bin/rtl_433', '-q', '-F', 'json', '-R', '146', '-R', '147', '-R', '148', '-R', '150', '-R', '151', '-R', '152', '-R', '153']


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#   A few helper functions...

def nowStr():
    return (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)


#   We're using a queue to capture output as it occurs
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x
ON_POSIX = 'posix' in sys.builtin_module_names


def enqueue_output(src, out, queue):
    for line in iter(out.readline, b''):
        queue.put((src, line))
    out.close()


def randomadd(value, spread):
    return round(value + random.uniform(-spread, spread), 2)


# MQTT Publish Line
def mqtt_publish_single(message, topic):
    topic = '{0}/{1}'.format("weathersense", topic)
    # return
    try:
        publish.single(
            topic=topic,
            payload=message,
            hostname=config.MQTThost,
            port=config.MQTTport,
            client_id="WeatherSenseMonitor",
            qos=config.MQTTqos
        )
    except:
        traceback.print_exc()
        print('Mosquitto not available')


# process functions
import gpiozero

def processFT020T(sLine, lastFT020TTimeStamp, ReadingCount):
    
    if (config.SWDEBUG):
        sys.stdout.write("processing FT020T Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')
        sys.stdout.write('ReadingCount=: ' + str(ReadingCount) + '\n')

    var = json.loads(sLine)

    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, "FT020T")


    if (lastFT020TTimeStamp == var["time"]):
        # duplicate
        if (config.SWDEBUG):
            sys.stdout.write("duplicate found\n")
        return ""
    
    lastFT0202TTimeStamp = var["time"]

    # now check for adding record

    if ((ReadingCount % config.RecordEveryXReadings) != 0):
        # skip write to database 
        if (config.SWDEBUG):
            sys.stdout.write("skipping write to database \n")
        return ""

    # outside temperature and Humidity

    mainID = var["id"]
    lastMainReading = nowStr()

    wTemp = var["temperature"]

    ucHumi = var["humidity"]

    wTemp = (wTemp - 400) / 10.0
    # deal with error condtions
    if (wTemp > 140.0):
        # error condition from sensor
        if (config.SWDEBUG):
            sys.stdout.write("error--->>> Temperature reading from FT020T\n")
            sys.stdout.write('This is the raw temperature: ' + str(wTemp) + '\n')
        # put in previous temperature 
        wtemp = state.currentOutsideTemperature
        # print("wTemp=%s %s", (str(wTemp),nowStr() ));
    if (ucHumi > 100.0):
        # bad humidity
        # put in previous humidity
        ucHumi = state.currentOutsideHumidity

    # convert temperature reading to Celsius
    OutdoorTemperature = round(((wTemp - 32.0) / (9.0 / 5.0)), 2)
    #OutdoorTemperature = round(wTemp, 2)
    OutdoorHumidity = ucHumi

    WindSpeed = round(var["avewindspeed"] / 10.0, 1)
    WindGust = round(var["gustwindspeed"] / 10.0, 1)
    WindDirection = var["winddirection"]

    TotalRain = round(var["cumulativerain"] / 10.0, 1)
    Rain60Minutes = 0.0

    wLight = var["light"]
    #if (wLight >= 0x1fffa):
    #    wLight = wLight | 0x7fff0000

    wUVI = var["uv"]
    if (wUVI >= 0xfa):
        wUVI = wUVI | 0x7f00

    SunlightVisible = wLight
    SunlightUVIndex = round(wUVI / 10.0, 1)

    if (var['batterylow'] == 0):
        BatteryOK = "OK"
        BatteryLevel = 100
    else:
        BatteryOK = "LOW"
        BatteryLevel = 0

    # SkyWeather2 Compatiblity
    AQI = 0
    Hour24_AQI = 0
    IndoorTemperature = 0
    IndoorHumidity = 0
    BarometricPressure = 0.0
    BarometricPressureSeaLevel = 0.0
    BarometricTemperature = 0.0

    if (config.enable_HA_discovery == True):
        sensor_FT020T_batteryState.publish_state(BatteryLevel)
        sensor_FT020T_cumulativeRain.publish_state(TotalRain)
        sensor_FT020T_humidity.publish_state(OutdoorHumidity)
        sensor_FT020T_light.publish_state(SunlightVisible)
        sensor_FT020T_temperature.publish_state(OutdoorTemperature)
        sensor_FT020T_uv.publish_state(SunlightUVIndex)
        sensor_FT020T_windDirection.publish_state(WindDirection)
        sensor_FT020T_windSpeedAvg.publish_state(WindSpeed)
        sensor_FT020T_windSpeedGust.publish_state(WindGust)

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:
            cpu = gpiozero.CPUTemperature()
            CPUTemperature = cpu.temperature

            con = mdb.connect(
                config.MySQL_Host,
                config.MySQL_User,
                config.MySQL_Password,
                config.MySQL_Schema
            )

            cur = con.cursor()

            fields = "OutdoorTemperature, OutdoorHumidity, IndoorTemperature, IndoorHumidity, TotalRain, SunlightVisible, SunlightUVIndex, WindSpeed, WindGust, WindDirection,BarometricPressure, BarometricPressureSeaLevel, BarometricTemperature, AQI, AQI24Average, BatteryOK, CPUTemperature"
            values = "%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%6.2f,%6.2f,%6.2f, \'%s\',%6.2f" % (
            OutdoorTemperature, OutdoorHumidity, IndoorTemperature, IndoorHumidity, TotalRain, SunlightVisible,
            SunlightUVIndex, WindSpeed, WindGust, WindDirection, BarometricPressure, BarometricPressureSeaLevel,
            BarometricTemperature, float(AQI), Hour24_AQI, BatteryOK, CPUTemperature)
            query = "INSERT INTO WeatherData (%s) VALUES(%s )" % (fields, values)
            # print("query=", query)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con
            
    return lastFT0202TTimeStamp


# processes Inside Temperature and Humidity
def processF016TH(sLine, ReadingCountArray):

    if (config.SWDEBUG):
        sys.stdout.write('Processing F016TH data' + '\n')
        sys.stdout.write('This is the raw data: ' + sLine + '\n')
        if config.SWDEBUG:
            print(ReadingCountArray)

    var = json.loads(sLine)
    
    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, '/'.join(["F016TH", str(var["channel"])]))

    IndoorTemperature = round(((var["temperature_F"] - 32.0) / (9.0 / 5.0)), 2)
    #IndoorTemperature = var["temperature_F"]
    
    if (var['battery'] == "OK"):
        batteryState = "OK"
        batteryLevel = 100
    else:
        batteryState = "LOW"
        batteryLevel = 0

    if (config.enable_HA_discovery == True):    
        channel = var["channel"]
        sys.stdout.write('Channel ' + str(channel) + '\n')
        if (channel == 1):
            sensor_F016TH_ch1_batteryState.publish_state(batteryLevel)
            sensor_F016TH_ch1_humidity.publish_state(var["humidity"])
            sensor_F016TH_ch1_temperature.publish_state(IndoorTemperature)
        if (channel == 2):
            sensor_F016TH_ch2_batteryState.publish_state(batteryLevel)
            sensor_F016TH_ch2_humidity.publish_state(var["humidity"])
            sensor_F016TH_ch2_temperature.publish_state(IndoorTemperature)

    lastIndoorReading = nowStr()

    # check for reading count per device
    # indoor T/H sensors support channels 1-8
    # the sensor channel needs to be lowered by one
    chan_array_pos = var['channel'] - 1

    #if ((ReadingCountArray[var["channel"]] % config.IndoorRecordEveryXReadings) != 0):
    if (ReadingCountArray[chan_array_pos] % config.IndoorRecordEveryXReadings) != 0:
        if config.SWDEBUG:
            print("skipping write to database for channel=", var["channel"])
        # increment ReadingCountArray
        # ReadingCountArray[var["channel"]] = ReadingCountArray[var["channel"]] + 1
        ReadingCountArray[chan_array_pos] += 1
        return ""
    # increment ReadingCountArray
    # ReadingCountArray[var["channel"]] = ReadingCountArray[var["channel"]] + 1
    ReadingCountArray[chan_array_pos] += 1

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:

            con = mdb.connect(
                config.MySQL_Host,
                config.MySQL_User,
                config.MySQL_Password,
                config.MySQL_Schema
            )

            cur = con.cursor()

            fields = "DeviceID, ChannelID, Temperature, Humidity, BatteryOK, TimeRead"

            values = "%d, %d, %6.2f, %6.2f, \"%s\", \"%s\"" % (
            var["device"], var["channel"], IndoorTemperature, var["humidity"], var["battery"], var["time"])
            query = "INSERT INTO IndoorTHSensors (%s) VALUES(%s )" % (fields, values)
            # print("query=", query)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con
    return




# processes Generic Packets 
def processWeatherSenseGeneric(sLine):
    if (config.SWDEBUG):
        sys.stdout.write("processing Generic Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, "WSGeneric")

    return

# processes Radiation Detector Packets 
def processWeatherSenseRadiation(sLine):
    # WeatherSense Protocol 19
    state = json.loads(sLine)
    myProtocol = state['weathersenseprotocol']
    if (config.SWDEBUG):
        sys.stdout.write("processing Radiation Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, "WSRadiation")

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:

            con = mdb.connect(
                config.MySQL_Host,
                config.MySQL_User,
                config.MySQL_Password,
                config.MySQL_Schema
            )
            
            # calculate Radiation 24 Hour
            timeDelta = datetime.timedelta(days=1)
            now = datetime.datetime.now()
            before = now - timeDelta
            before = before.strftime('%Y-%m-%d %H:%M:%S')
            query = "SELECT uSVh, TimeStamp FROM RAD433MHZ WHERE (TimeStamp > '%s') ORDER BY TimeStamp " % (before)

            cur = con.cursor()
            cur.execute(query)
            myRADRecords = cur.fetchall()
            myRADTotal = 0.0
            if (len(myRADRecords) > 0):
                for i in range(0, len(myRADRecords)):
                    myRADTotal = myRADTotal + myRADRecords[i][0]

                RAD24Hour = (myRADTotal + float(state['uSVh'])) / (len(myRADRecords) + 1)
            else:
                RAD24Hour = 0.0

            batteryPower =  float(state["batterycurrent"])* float(state["batteryvoltage"])
            loadPower  =  float(state["loadcurrent"])* float(state["loadvoltage"])
            solarPower =  float(state["solarpanelcurrent"])* float(state["solarpanelvoltage"])
            batteryCharge = util.returnPercentLeftInBattery(state["batteryvoltage"], 4.2)

            fields = "uSVh24Hour, deviceid, protocolversion, softwareversion, weathersenseprotocol, CPM, nSVh, uSVh, batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, solarpresent, radiationpresent, keepalivemessage, lowbattery, batterycharge, messageID, batterypower, loadpower, solarpower "
            values = "%6.2f, %d, %d, %d, %d, %d,%d,  %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %d, %d, %d,%d,%d,%6.2f, %d,%6.2f, %6.2f, %6.3f" % ( RAD24Hour, state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],
            state['CPM'], state['nSVh'], state['uSVh'], 
            state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"],
            state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"],state["solarpresent"],state["radBoardPresent"],state["keepalivemessage"],state["lowbattery"],     batteryCharge, state["messageid"],
            batteryPower, loadPower, solarPower )
            query = "INSERT INTO RAD433MHZ (%s) VALUES(%s )" % (fields, values)
            # print("query=", query)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con
            
            CPM = state['CPM']
            uSVh = state['uSVh']
            # update web maps
            updateWeb.update_SafeCast(CPM, uSVh)
            updateWeb.update_RadMon(CPM)
            updateWeb.update_GMCMap(CPM, uSVh)

            



    return

# processes AfterShock Packets 
def processWeatherSenseAfterShock(sLine):

    # weathersense protocol 18
    state = json.loads(sLine)
    myProtocol = state['weathersenseprotocol']
    if (config.SWDEBUG):
        sys.stdout.write("processing AfterShock Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, "WSAfterShock")

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:
            myTEST = ""
            myTESTDescription = ""

            con = mdb.connect(
                config.MySQL_Host,
                config.MySQL_User,
                config.MySQL_Password,
                config.MySQL_Schema
            )

            cur = con.cursor()
            batteryPower =  float(state["batterycurrent"])* float(state["batteryvoltage"])
            loadPower  =  float(state["loadcurrent"])* float(state["loadvoltage"])
            solarPower =  float(state["solarpanelcurrent"])* float(state["solarpanelvoltage"])
            batteryCharge = util.returnPercentLeftInBattery(state["batteryvoltage"], 4.2)

            fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol, eqcount, finaleq_si, finaleq_pga, instanteq_si, instanteq_pga, batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, solarpresent, aftershockpresent, keepalivemessage, lowbattery, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
            values = "%d, %d, %d, %d, %d,%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f, %d, %d, %d, %d,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (
            state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],
            state['eqcount'], state['finaleq_si'], state['finaleq_pga'], state['instanteq_si'],
            state['instanteq_pga'], 
            state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"],
            state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"],state["solarpresent"],state["aftershockpresent"],state["keepalivemessage"],state["lowbattery"],     batteryCharge, state["messageid"],
            batteryPower, loadPower, solarPower, myTEST, myTESTDescription)
            query = "INSERT INTO AS433MHZ (%s) VALUES(%s )" % (fields, values)
            # print("query=", query)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con

    return



def processWeatherSenseTB(sLine):
    # weathersense protocol 16
    state = json.loads(sLine)
    myProtocol = state['weathersenseprotocol']
    if (config.SWDEBUG):
        sys.stdout.write("processing Lightning TB Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, "WSLightning")

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:
            myTEST = ""
            myTESTDescription = ""

            con = mdb.connect(
                config.MySQL_Host,
                config.MySQL_User,
                config.MySQL_Password,
                config.MySQL_Schema
            )

            cur = con.cursor()
            batteryPower =  float(state["batterycurrent"])* float(state["batteryvoltage"])
            loadPower  =  float(state["loadcurrent"])* float(state["loadvoltage"])
            solarPower =  float(state["solarpanelcurrent"])* float(state["solarpanelvoltage"])
            batteryCharge = util.returnPercentLeftInBattery(state["batteryvoltage"], 4.2)

            fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol,irqsource, previousinterruptresult, lightninglastdistance, sparebyte, lightningcount, interruptcount,  batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
            values = "%d, %d, %d, %d, %d, %d, %d, %d,%d, %d,%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (
            state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],
            state['irqsource'], state['previousinterruptresult'], state['lightninglastdistance'], state['sparebyte'],
            state['lightningcount'], state['interruptcount'],
            state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"],
            state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"], batteryCharge, state["messageid"],
            batteryPower, loadPower, solarPower, myTEST, myTESTDescription)
            query = "INSERT INTO TB433MHZ (%s) VALUES(%s )" % (fields, values)
            # print("query=", query)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con

    return


def processWeatherSenseAQI(sLine):
    # weathersense protocol 15
    state = json.loads(sLine)
    myProtocol = state['weathersenseprotocol']
    if (config.SWDEBUG):
        sys.stdout.write("processing AQI Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, "WSAQI")
        
    if (config.enable_HA_discovery == True):
        sensor_WeatherSenseAQI_1_0_micron_particles_standard.publish_state(state['PM1.0S'])
        sensor_WeatherSenseAQI_2_5_micron_particles_standard.publish_state(state['PM2.5S'])
        sensor_WeatherSenseAQI_10_micron_particles_standard.publish_state(state['PM10S'])
        sensor_WeatherSenseAQI_1_0_micron_particles_atmospheric.publish_state(state['PM1.0A'])
        sensor_WeatherSenseAQI_2_5_micron_particles_atmospheric.publish_state(state['PM2.5A'])
        sensor_WeatherSenseAQI_10_micron_particles_atmospheric.publish_state(state['PM10A'])
        sensor_WeatherSenseAQI_AQI.publish_state(state['AQI'])
        sensor_WeatherSenseAQI_batteryCurrent.publish_state(state['batterycurrent'])
        sensor_WeatherSenseAQI_batteryVoltage.publish_state(state['batteryvoltage'])
        sensor_WeatherSenseAQI_loadCurrent.publish_state(state['loadcurrent'])
        sensor_WeatherSenseAQI_loadVoltage.publish_state(state['loadvoltage'])
        sensor_WeatherSenseAQI_solarCurrent.publish_state(state['solarpanelcurrent'])
        sensor_WeatherSenseAQI_solarVoltage.publish_state(state['solarpanelvoltage'])

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:
            myTEST = ""
            myTESTDescription = ""

            con = mdb.connect(
                config.MySQL_Host,
                config.MySQL_User,
                config.MySQL_Password,
                config.MySQL_Schema
            )

            cur = con.cursor()
            batteryPower =  float(state["batterycurrent"])* float(state["batteryvoltage"])
            loadPower  =  float(state["loadcurrent"])* float(state["loadvoltage"])
            solarPower =  float(state["solarpanelcurrent"])* float(state["solarpanelvoltage"])
            batteryCharge = util.returnPercentLeftInBattery(state["batteryvoltage"], 4.2)
            
            # calculate AQI 24 Hour
            timeDelta = datetime.timedelta(days=1)
            now = datetime.datetime.now()
            before = now - timeDelta
            before = before.strftime('%Y-%m-%d %H:%M:%S')
            query = "SELECT AQI, TimeStamp FROM AQI433MHZ WHERE (TimeStamp > '%s') ORDER BY TimeStamp " % (before)

            cur.execute(query)
            myAQIRecords = cur.fetchall()
            myAQITotal = 0.0
            if (len(myAQIRecords) > 0):
                for i in range(0, len(myAQIRecords)):
                    myAQITotal = myAQITotal + myAQIRecords[i][0]

                AQI24Hour = (myAQITotal + float(state['AQI'])) / (len(myAQIRecords) + 1)
            else:
                AQI24Hour = 0.0
            # HOTFIX for AQI problem from the wireless AQI sensor
            # recalculate AQI from RAW values and write in database

            myaqi = aqi.to_aqi([
                (aqi.POLLUTANT_PM25, state['PM2.5A']),
                (aqi.POLLUTANT_PM10, state['PM10A'])
                ])
            if (myaqi > 500):
                myaqi = 500
            print("myaqi=", myaqi)
            state['AQI'] = myaqi

            fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol, PM1_0S, PM2_5S, PM10S, PM1_0A, PM2_5A, PM10A, AQI, AQI24Hour, batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
            values = "%d, %d, %d, %d, %d, %d, %d, %d, %d,%d, %d, %6.2f,%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (
            state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],
            state['PM1.0S'], state['PM2.5S'], state['PM10S'], state['PM1.0A'], state['PM2.5A'], state['PM10S'],
            state['AQI'], AQI24Hour,
            state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"],
            state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"], batteryCharge, state["messageid"],
            batteryPower, loadPower, solarPower, myTEST, myTESTDescription)
            query = "INSERT INTO AQI433MHZ (%s) VALUES(%s )" % (fields, values)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con

    return


def processSolarMAX(sLine):
    
    state = json.loads(sLine)

    if (config.SWDEBUG):
        sys.stdout.write("Processing SolarMAX Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    # only accept SolarMAX Protocols (8,10,11)
    myProtocol = state['weathersenseprotocol']
    if ((myProtocol == 8) or (myProtocol == 10) or (myProtocol == 11)):

        if (config.enable_MQTT == True):
            mqtt_publish_single(sLine, "SolarMAX")
            
        if (config.enable_HA_discovery == True):
            sensor_SolarMAX_batteryCurrent.publish_state(state["batterycurrent"])
            sensor_SolarMAX_batteryVoltage.publish_state(state["batteryvoltage"])
            sensor_SolarMAX_loadCurrent.publish_state(state["loadcurrent"])
            sensor_SolarMAX_loadVoltage.publish_state(state["loadvoltage"])
            sensor_SolarMAX_solarCurrent.publish_state(state["solarpanelcurrent"])
            sensor_SolarMAX_solarVoltage.publish_state(state["solarpanelvoltage"])
            sensor_SolarMAX_internalHumidity.publish_state(state["internalhumidity"])
            sensor_SolarMAX_internalTemperature.publish_state(state["internaltemperature"])

        if (config.enable_MySQL_Logging == True):
            # open mysql database
            # write log
            # commit
            # close
            try:
                myTEST = ""
                myTESTDescription = ""

                con = mdb.connect(
                    config.MySQL_Host,
                    config.MySQL_User,
                    config.MySQL_Password,
                    config.MySQL_Schema
                )

                cur = con.cursor()
                batteryPower =  float(state["batterycurrent"])* float(state["batteryvoltage"])
                loadPower  =  float(state["loadcurrent"])* float(state["loadvoltage"])
                solarPower =  float(state["solarpanelcurrent"])* float(state["solarpanelvoltage"])
                batteryCharge = util.returnPercentLeftInBattery(state["batteryvoltage"], 13.2)

                fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol, batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, internaltemperature,internalhumidity, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
                values = "%d, %d, %d, %d, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (
                state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],
                state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"],
                state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"], state["internaltemperature"],
                state["internalhumidity"], batteryCharge, state["messageid"], batteryPower, loadPower, solarPower,
                myTEST, myTESTDescription)
                query = "INSERT INTO SolarMax433MHZ (%s) VALUES(%s )" % (fields, values)
                cur.execute(query)
                con.commit()
            except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0], e.args[1]))
                con.rollback()
                # sys.exit(1)

            finally:
                cur.close()
                con.close()

                del cur
                del con

    return


# main read 433HMz Sensor Loop
def readSensors():
    print("")
    print("######")
    print("Read Wireless Sensors")
    print("######")
    #   Create our sub-process...
    #   Note that we need to either ignore output from STDERR or merge it with STDOUT due to a limitation/bug somewhere under the covers of "subprocess"
    #   > this took awhile to figure out a reliable approach for handling it...

    p = Popen(cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, close_fds=ON_POSIX)
    q = Queue()

    t = Thread(target=enqueue_output, args=('stdout', p.stdout, q))

    t.daemon = True  # thread dies with the program
    t.start()

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    pulse = 0
    print("starting 433MHz scanning")
    print("######")
    # last timestamp for FT020T to remove duplicates
    lastFT020TTimeStamp = ""
    FT020Count = 0
    IndoorReadingCountArray = [0, 0, 0, 0, 0, 0, 0, 0]
    # temp value
    #config.SWDEBUG = False

    while True:
        #   Other processing can occur here as needed...
        # sys.stdout.write('Made it to processing step. \n')
        
        try:
            src, line = q.get(timeout=1)
            # print(line.decode())
        except Empty:
            pulse += 1
        else:  # got line
            pulse -= 1
            sLine = line.decode()
            #   See if the data is something we need to act on...

            # if (sLine.find('F007TH') != -1) or (sLine.find('FT0300') != -1) or (sLine.find('F016TH') != -1) or (
            #         sLine.find('FT020T') != -1):

            if ((sLine.find('F007TH') != -1) or (sLine.find('F016TH') != -1)):
                processF016TH(sLine, IndoorReadingCountArray)
                
            if ((sLine.find('FT0300') != -1) or (sLine.find('FT020T') != -1)):
                lastFT020TTimeStamp = processFT020T(sLine, lastFT020TTimeStamp, FT020Count)
                FT020Count = FT020Count + 1

            if (sLine.find('SolarMAX') != -1):
                processSolarMAX(sLine)

            if (sLine.find('AQI') != -1):
                processWeatherSenseAQI(sLine)

            if (sLine.find('TB') != -1):
                processWeatherSenseTB(sLine)

            if (sLine.find('Generic') != -1):
                processWeatherSenseGeneric(sLine)

            if (sLine.find('AfterShock') != -1):
                processWeatherSenseAfterShock(sLine)

            if (sLine.find('Radiation') != -1):
                processWeatherSenseRadiation(sLine)

        sys.stdout.flush()




