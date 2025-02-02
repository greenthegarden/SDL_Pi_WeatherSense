#!/usr/bin/env bash

script="WeatherSenseMonitor.py"

var=$(date +"%FORMAT_STRING")
now=$(date +"%Y-%m-%d")

echo $(pwd)

if [ ! -d SDL_Pi_WeatherSense ] ; then
  cd local
  echo $(pwd)
fi

if [ -d SDL_Pi_WeatherSense ] ; then
  cd SDL_Pi_WeatherSense
  echo $(pwd)
fi

if [ -f ${script} ] ; then
  # printf "\n\nInitialising database\n"
  # sudo mysql -u root -p < WeatherSenseWireless.sql
  # sleep 5m
  printf "\n\nStarting %s on %s\n" ${script} ${now}
  printf "Logging to %s\n\n" "${script/.py/_${now}.log}"
  /usr/bin/python3 ${script} #>> "${script/.py/_${now}.log}" 2>&1
else
  printf "Required script %s not found!!\n"
  exit 1
fi
