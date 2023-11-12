
reference:

Schematic:https://github.com/milkv-duo/duo-hardware/blob/main/duo/duo-schematic-v1.2.pdf

Guide:https://community.milkv.io/t/milk-v-duo-spi-st7789/131


### hardware connection

<img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/5bef7e95-fde8-41dd-9d8a-cf0099ba132c" width="75%" height="75%"/>

```
Duo       |       st7789
GND       |         GND
3.3v(out) |         VCC
GPIO23    |         SCL
GPIO22    |         SDA
GPIOA23   |         RES
GPIOA24   |         DC
GPIO18    |         CS
```

### Code

- `duo-buildroot-sdk/u-boot-2021.10/board/cvitek/cv180x/board.c`
- `duo-buildroot-sdk/build/boards/cv180x/cv1800b_milkv_duo_sd/dts_riscv/cv1800b_milkv_duo_sd.dts`
- `duo-buildroot-sdk/linux_5.10/drivers/staging/fbtft/fbtft-core.c`
- `duo-buildroot-sdk/linux_5.10/drivers/staging/fbtft/fb_st7789v.c`
- `duo-buildroot-sdk/build/boards/default/dts/cv180x/cv180x_base.dtsi`
- `duo-buildroot-sdk/build/boards/cv180x/cv1800b_milkv_duo_sd/linux/cvitek_cv1800b_milkv_duo_sd_defconfig`
- `duo-buildroot-sdk/u-boot-2021.10/include/configs/cv180x-asic.h`

Replace them then compile the image.burn the system into SD card

### Target Packages

reference:https://community.milkv.io/t/milkv-duo-python-pip3-nano-vim-tmux/611/1

modify `build/boards/cv180x/cv1800b_milkv_duo_sd/memmap.py`

```
ION_SIZE = 0 * SIZE_1M
```

run `./build_milkv.sh`

