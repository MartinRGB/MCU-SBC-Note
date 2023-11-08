Reference:

https://wiki.luckfox.com/zh/Luckfox-Pico/Luckfox-Pico-GPIO

https://wiki.luckfox.com/zh/Luckfox-Pico/Luckfox-Pico-LCD

### Device used

LuckFox Pico Max

<img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/7476b7bc-aab7-4a0c-adfe-ba669c3abd61" width="50%" height="50%">

ST7789 LCD/Waveshare Pico LCD 2

<img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/cb19b0bc-9d05-49a7-83eb-46e2f6f67f0e" width="50%" height="50%">

### hardware connection


<img src="https://user-images.githubusercontent.com/7036706/280813192-51f94bca-47d4-44ca-8ab7-0c5f96a07909.png" width="100%" height="100%"/>

Compare Pico LCD 2's GPIO Layout & LuckFox Pico's,The GPIOs used are:

```
BL  - 72 - GPIO2-PB0
RST - 51 - GPIO1-PC3
DIN - 50 - GPIO1-PC2
CLK - 49 - GPIO1-PC1
CS  - 48 - GPIO1-PC0
DC  - 73 - GPIO2-PB1
```

<img src="https://user-images.githubusercontent.com/7036706/281272858-ee6a76f8-7652-43e0-b63e-58586f8503f0.png" width="100%" height="100%"/>

for Pico LCD 2inch's key:

| define in code| Printed Name in LCD Board | Pin number|
| -------- | ------- |------- |
| GET_KEY1|KEY0| 57|
| GET_KEY2|KEY1|69|
| GET_KEY_UP|KEY2|55|
| GET_KEY_PRESS|KEY3|54|

### Compile the IMAGE

modify `<SDK Directory>/sysdrv/source/kernel/arch/arm/boot/dts/rv1106g-luckfox-pico-pro-max.dts`

compile the IMAGE:

```
cd ~/Luckfox-Pico/luckfox-pico
./build.sh clean
./build.sh 
```

Burn the system via SocToolKit

### Compile the LCD Code

Modify Makefile with gcc path

gcc path:`<SDK directory\>/tools/linux/toolchain/arm-rockchip830-linux-uclibcgnueabihf/bin/arm-rockchip830-linux-uclibcgnueabihf-gcc`

```
CC=home/luckfox/Luckfox-Pico/luckfox-pico/tools/linux/toolchain/arm-rockchip830-linux-uclibcgnueabihf/bin/arm-rockchip830-linux-uclibcgnueabihf-gcc
```

