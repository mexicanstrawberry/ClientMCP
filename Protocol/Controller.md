uint8_t 1  CMD
uint8_t 1  SubCMD
uint8_t 1  Size
uint8_t n  Data
uint8_t 4  CRC over CMD, SubCMD, Size, Data

CMD
00 Network 
   00 PING Send Back the transmitted data with an offset of 1 (SPI) n data
   
10 Firmware
   00 GET Type                      1 Byte Type 00 -> Inside Controller 10 -> Outside Controller
   10 GET Firmware Version          1 Byte Major  ,   1 Byte Minor,    1 Byte BuildVersion
   20 GET Uptime                    4 Byte Milliseconds
   30 SET Reboot                    1 Byte ASCII "M", 1 Byte ASCII "S"

20 Sensor
   00 GET Temperature Outside       1 Byte Integer, 1 Byte Decimal
   01 GET Temperature Inside        1 Byte Integer, 1 Byte Decimal
   02 GET Temperature Water         1 Byte Integer, 1 Byte Decimal
   03 GET Temperature Light1        1 Byte Integer, 1 Byte Decimal
   04 GET Temperature Light2        1 Byte Integer, 1 Byte Decimal
   05 GET Temperature Light3        1 Byte Integer, 1 Byte Decimal
   10 GET Humidity Outside          1 Byte Integer, 1 Byte Decimal
   11 GET Humidity Inside           1 Byte Integer, 1 Byte Decimal
   20 GET CO2                       2 Byte PPM
   30 GET Ph                        1 Byte Integer, 1 Byte Decimal
   40 GET Redox                     2 Byte Integer 
   
30 Motor
   00 GET LightMovementSpeed        1 Byte Herz 
   01 SET LightMovementSpeed        1 Byte Herz
   02 GET LightMovementPosition     2 Byte Steps from left
   03 SET LightMovementPosition     2 Byte Steps from left
   04 GET LightMovementCounter      2 Byte Counter
   10 GET LightFan1Speed            1 Byte Percentage
   11 SET LightFan1Speed            1 Byte Percentage
   12 GET Light1DesiredTemperature  1 Byte Integer
   13 SET Light1DesiredTemperature  1 Byte Integer
   20 GET LightFan2Speed            1 Byte Percentage
   21 SET LightFan2Speed            1 Byte Percentage
   22 GET Light2DesiredTemperature  1 Byte Integer
   23 SET Light2DesiredTemperature  1 Byte Integer
   30 GET LightFan3Speed            1 Byte Percentage
   31 SET LightFan3Speed            1 Byte Percentage
   32 GET Light3DesiredTemperature  1 Byte Integer
   33 SET Light3DesiredTemperature  1 Byte Integer
   40 GET Hatch                     1 Byte Percentage Open
   41 SET Hatch                     1 Byte Percentage Open
   50 GET OutsideFan                1 Byte Percentage
   51 SET OutsideFan                1 Byte Percentage
   60 GET InsideFan                 1 Byte Percentage
   61 SET InsideFan                 1 Byte Percentage

40 Light
   00 GET IntensityIR               1 Byte Percentage
   01 SET IntensityIR               1 Byte Percentage
   10 GET IntensityFS               1 Byte Percentage
   11 SET IntensityFS               1 Byte Percentage
   20 GET IntensityUV               1 Byte Percentage
   21 SET IntensityUV               1 Byte Percentage
   
50 Heater
   00 GET HeaterAir                 1 Byte Percentage
   01 SET HeaterAir                 1 Byte Percentage
   10 GET HeaterWater               1 Byte Percentage
   11 SET HeaterWater               1 Byte Percentage
   