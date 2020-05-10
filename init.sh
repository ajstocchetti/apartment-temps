#!/bin/bash

sudo apt-get update
sudo apt-get upgrade -y
sudo pip3 install --upgrade setuptools

# enable I2C and SPI
# https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
# https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-spi

sudo apt-get install libgpiod2 -Y
pip3 install RPI.GPIO
pip3 install adafruit-blinka # for to tranlating circuit-pyton to regular python (eg rasp pi)
pip3 install adafruit-circuitpython-dht


# influx db
# start on boot
sudo systemctl unmask influxdb
sudo systemctl enable influxdb

pip3 install --upgrade influxdb