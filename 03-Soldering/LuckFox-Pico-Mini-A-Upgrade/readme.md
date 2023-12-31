### Device used

- thermal tape
- hot air gun
- solder paste
- LuckFox Pico Mini A(RV1103 without NAND Flash)

  <img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/099ed986-348a-49e8-baf3-ceecbdcd2344" width="50%" height="50%">

- NAND Flash Chips - Winbond 25n02kvzeir(256MB)

  <img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/3a8078ad-dc42-4f59-9769-da52821eeced" width="50%" height="50%">
  
### Steps


- uses thermal tape to act as a temporary solder mask on LuckFox board.

  <img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/bcc30907-c041-4456-9d2b-a40732796501" width="50%" height="50%">
  
- added some solder paste on top of the NAND Flash pads,then soldering with hot air gun
   
  <img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/50627595-e93a-43fd-a503-5569e4e71ae7" width="50%" height="50%">

### Compile the IMAGE

modify `<SDK Directory>/project/cfg/BoardConfig_IPC/BoardConfig-SPI_NAND-NONE-RV1103_Luckfox_Pico_Mini_B-IPC.mk`

compile the IMAGE:

```
cd ~/Luckfox-Pico/luckfox-pico
./build.sh clean
./build.sh lunch
# select LuckFox Pico Mini B
./build.sh 
```

Burn the system via SocToolKit

### Test:

<img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/e5eedce3-9fb1-4631-9268-176d41706494" width="50%" height="50%">
 
- run `dmesg | grep'MiB'`

- run `df -h`






