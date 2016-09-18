#!/bin/bash

cd /home/pi/MS/InsideController
git pull

# connection test
sudo /home/pi/MS/avrdude/avrdude -C /home/pi/MS/avrdude/avrdude.conf -v -p atmega8 -c pi_1

# flash fuses for the atmega8-16PU
sudo /home/pi/MS/avrdude/avrdude -C /home/pi/MS/avrdude/avrdude.conf -v -p atmega8 -c pi_1 -U lfuse:w:0xe4:m -U hfuse:w:0xca:m
sudo /home/pi/MS/avrdude/avrdude -C /home/pi/MS/avrdude/avrdude.conf -v -p atmega8 -c pi_2 -U lfuse:w:0xe4:m -U hfuse:w:0xca:m

#Flashes the inside Controller
sudo /home/pi/MS/avrdude/avrdude -C /home/pi/MS/avrdude/avrdude.conf -v -p atmega8 -c pi_1 -U flash:w:/home/pi/MS/InsideController/Arduino/Arduino.ino.standard.hex:i

#Flashes the outside Controller
sudo /home/pi/MS/avrdude/avrdude -C /home/pi/MS/avrdude/avrdude.conf -v -p atmega8 -c pi_2 -U flash:w:/home/pi/MS/OutsideController/Arduino/Arduino.ino.standard.hex:i
