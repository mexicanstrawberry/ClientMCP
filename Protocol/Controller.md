uint8_t 1  CMD
uint8_t 1  SubCMD
uint8_t 1  Size
uint8_t n  Data

CMD
00 Network 
   00 PING Send Back the transmitted data with an offset of 1 (SPI) n data
   
10 Firmware
   00 GET Firmware Version     1 Byte Major  ,   1 Byte Minor,    1 Byte BuildVersion
   10 GET Uptime               1 Byte Year,      1 Byte Month,    1 Byte Day,          1 Byte Hour,   1 Byte Minute,  1 Byte Second
   20 SET Reboot               1 Byte ASCII "M", 1 Byte ASCII "S"

20 Sensor
   00 GET Temperature Outside  1 Byte Integer, 1 Byte Decimal
   01 GET Temperature Inside   1 Byte Integer, 1 Byte Decimal
   02 GET Temperature Water    1 Byte Integer, 1 Byte Decimal
   03 GET Temperature Light1   1 Byte Integer, 1 Byte Decimal
   04 GET Temperature Light2   1 Byte Integer, 1 Byte Decimal
   05 GET Temperature Light3   1 Byte Integer, 1 Byte Decimal
   10 GET Humidity Outside     1 Byte Integer, 1 Byte Decimal
   11 GET Humidity Inside      1 Byte Integer, 1 Byte Decimal
   20 GET CO2                  1 Byte PPM
   30 GET Ph                   1 Byte Integer, 1 Byte Decimal
   40 GET Redox                2 Byte Integer 
   
30 Motor
   00 GET LightMovementSpeed
   01 SET LightMovementSpeed
   02 GET LightMovementPosition
   03 SET LightMovementPosition
   04 GET LightMovementCounter
   10 GET LightFan1Speed
   11 SET LightFan1Speed
   12 GET Light1DesiredTemperature
   13 SET Light1DesiredTemperature
   20 GET LightFan2Speed
   21 SET LightFan2Speed
   22 GET Light2DesiredTemperature
   23 SET Light2DesiredTemperature
   30 GET LightFan3Speed
   31 SET LightFan3Speed
   32 GET Light3DesiredTemperature
   33 SET Light3DesiredTemperature
   40 GET Hatch 
   41 SET Hatch
   50 GET OutsideFan
   51 SET OutsideFan
   60 GET InsideFan
   61 SET InsideFan

40 Light
   00 GET IntensityIR
   01 SET IntensityIR
   10 GET IntensityFS
   11 SET IntensityFS
   20 GET IntensityUV
   21 SET IntensityUV
   
50 Heater
   00 GET HeaterAir
   01 SET HeaterAir
   10 GET HeaterWater
   11 SET HeaterWater
   
