#!/bin/bash

cd /home/pi/MS/InsideController
git pull

sudo /home/pi/MS/avrdude/avrdude -C /home/pi/MS/avrdude/avrdude.conf -v -p atmega8 -c pi_1
sudo /home/pi/MS/avrdude/avrdude -C /home/pi/MS/avrdude/avrdude.conf -v -p atmega8 -c pi_1 -U lfuse:w:0xe4:m -U hfuse:w:0xca:m
sudo /home/pi/MS/avrdude/avrdude -C /home/pi/MS/avrdude/avrdude.conf -v -p atmega8 -c pi_1 -U flash:w:/home/pi/MS/InsideController/Arduino/Arduino.ino.standard.hex:i
