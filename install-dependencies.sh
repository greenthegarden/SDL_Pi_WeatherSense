#!/usr/bin/env bash

CWD="$(pwd)"

# Install Nomad dependencies
sudo pip3 install SafecastPy

install_rtl433 () {
# install rtl_433 library
sudo apt-get install -y libtool libusb-1.0-0-dev librtlsdr-dev rtl-sdr build-essential autoconf cmake pkg-config

cd /tmp
git clone https://github.com/switchdoclabs/rtl_433
cd rtl_433/
mkdir build
cd build
cmake ..
make clean
make
sudo make install

cd $CWD
}

#install_rtl433

install_mqsql () {
# install mysql and create database
sudo apt-get install -y python3-dev python3-pip mariadb-server
sudo python3 -m pip install mysqlclient

sudo mysql -u root -p < WeatherSenseWireless.sql
}

# install python dependencies
sudo apt-get install -y libopenjp2-7
sudo python3 -m pip install -r requirements.txt
