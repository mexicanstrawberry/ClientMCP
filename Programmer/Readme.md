
# test
```
sudo ./avrdude -C ./avrdude.conf -v -p atmega8 -c pi_1
sudo ./avrdude -C ./avrdude.conf -v -p atmega8 -c pi_1 -U lfuse:w:0xe4:m -U hfuse:w:0xca:m
sudo ./avrdude -C ./avrdude.conf -v -p atmega8 -c pi_1 -U flash:w:Blink.cpp.hex:i
```
