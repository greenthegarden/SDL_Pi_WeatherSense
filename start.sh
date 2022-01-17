#!/usr/bin/env bash

script="WeatherSenseMonitor.py"

var=$(date +"%FORMAT_STRING")
now=$(date +"%Y-%m-%d")

echo $(pwd)

tree

if [ -d weather-sense-monitor ] ; then
  cd weather-sense-monitor
fi

if [ -f ${script} ] ; then
  printf "\n\nStarting %s at %s\n" ${script} ${now}
  printf "Logging to %s\n\n" "${script/.py/_${now}.log}"
  sudo /usr/bin/python3 ${script} >> "${script/.py/_${now}.log}" 2>&1
else
  printf "Required script %s not found!!\n"
  exit 1
fi
