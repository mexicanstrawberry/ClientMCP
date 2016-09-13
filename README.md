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
  4. wget latest version from http://download.savannah.gnu.org/releases/avrdude/   (avrdude-6.3.tar.gz has a bug but 6.1 works fine) 
  5. tar xvfz avrdude-6.1.tar.gz
  6. cd avrdude-6.1
  7. ./configure --enable-linuxgpio
  8. make
  9. cp avrdude avrdude.conf /home/pi/
  10. vim avrdude.conf and add this:
      ```
      programmer
        id    = "pi_1";
        desc  = "Use the Linux sysfs interface to bitbang GPIO lines";
        type  = "linuxgpio";
        reset = 22;
        sck   = 11;
        mosi  = 10;
        miso  =  9;
      ;

      programmer
        id    = "pi_2";
        desc  = "Use the Linux sysfs interface to bitbang GPIO lines";
        type  = "linuxgpio";
        reset = 27;
        sck   = 11;
        mosi  = 10;
        miso  =  9;
      
      programmer
        id    = "pi_3";
        desc  = "Use the Linux sysfs interface to bitbang GPIO lines";
        type  = "linuxgpio";
        reset = 17;
        sck   = 11;
        mosi  = 10;
        miso  =  9;
       ```
  11. Test connection 
      ```
    
      sudo ./avrdude -C ./avrdude.conf -v -p atmega8 -c pi_1
    
      ```
4. Install python
    ```
    
    sudo apt-get update
    sudo apt-get install python-pip git python-virtualenv python-rpi.gpio
    
    ```
5. Setup the environment
   ```
   
   git clone https://github.com/mexicanstrawberry/ClientMCP.git
   cd /home/pi/MS/ClientMCP/Python
   virtualenv .
   pip install -r Pip-Packages.txt
   
   ```
9. Install couchDB



