# ClientMCP

Communicates via SPI with the hardware controllers 
Sends MQTT data into the cloud
Local CouchDB for the original Webinterface
Local API Wrapper for the original Webinterface
avrdude for flashing the hardware controllers

## Install

1. Install Raspian light from https://www.raspberrypi.org/downloads/raspbian/. Easiest way with https://www.etcher.io/
  1. sudo apt-get update
  2. sudo apt-get upgrade
2. Activate SPI with `sudo raspi-config`
3. Install avrdude with linuxGPIO support (https://learn.adafruit.com/program-an-avr-or-arduino-using-raspberry-pi-gpio-pins/installation)
  1. sudo apt-get update
  2. sudo apt-get install -y build-essential bison flex automake libelf-dev libusb-1.0-0-dev libusb-dev libftdi-dev libftdi1
  3. mkdir avrdudeinstall && cd avrdudeinstall
  4. wget latest version from http://download.savannah.gnu.org/releases/avrdude/   (avrdude-6.3.tar.gz) 
  5. tar xvfz avrdude-6.3.tar.gz
  6. cd avrdude-6.3
  7. ./configure --enable-linuxgpio


9. Install couchDB



