### Device used

CM4-IO-BASE-B (GPIO layout is as same as rpi 4b)

<img src="https://raw.githubusercontent.com/MartinRGB/RaspberryPi-CM4-eGPU-Guide/main/art/Hardware/CM4-IO-BASE-A.png" width="50%" height="50%">

RPI CM4

<img src="https://raw.githubusercontent.com/MartinRGB/RaspberryPi-CM4-eGPU-Guide/main/art/Hardware/CM4.png" width="50%" height="50%">

WaveShare 1.69inch LCD Module

<img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/b0ea00eb-8fac-4c06-80a2-724c825839d3" width="50%" height="50%">

### hardware connection

<img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/51c89206-22d7-4a8d-84b6-b465409f6a66" width="50%" height="50%">

### for Raspberry Pi OS:

- download waveshare LCD_Module_code via [this](https://www.waveshare.com/wiki/1.69inch_LCD_Module#Run_Python_Demo) link
  - create `1inch69_LCD_temp.py` in `{YOUR DIR}/LCD_Module_code/RaspberryPi/python`

- make sure `dtparam=spi=on` is uncommented

- add `sudo python3 {YOUR DIR}/LCD_Module_code/RaspberryPi/python/1inch69_LCD_temp.py &` before `exit 0` in `/etc/rc.local`

<img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/b61eb05f-a422-4a89-aa86-575f6ca5eccf" width="50%" height="50%">
