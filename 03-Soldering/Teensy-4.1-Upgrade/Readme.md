Reference:

https://protosupplies.com/product/teensy-4-1-fully-loaded/
https://www.pjrc.com/store/psram.html

### Device used

  <img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/121d95c0-0a1c-4c41-8781-4cb309207a17" width="50%" height="50%">

- Soldering iron
- Soldering flux
- Thermal tape
- Teensy 4.1
  
  <img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/29c07168-2092-46e2-9258-6e9608f21e98" width="50%" height="50%">

- PSRAM Chips(Choose one of them)

  <img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/442506ff-4bf8-4cf0-9aea-acea4dca6bdb" width="50%" height="50%">
  
  - Lyontek LY68L6400S(Not work for me)
  - ESP PSRAM64H
  - AP 6404L-3SQR

### Steps


- uses thermal tape to act as a temporary solder mask on Teensy board.

  <img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/51df1366-cfd5-4ede-a785-ee700affa9f5" width="50%" height="50%">
  
- added some solder flux gel on top of the pads.
  
  <img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/a1afdb37-d79a-47c0-9f89-61bc3bd2891f" width="50%" height="50%">

- Soldering

  <img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/1332c469-77d5-4d3c-971b-d53129596ad0" width="50%" height="50%">

### Test:

- use PaulStoffregen's arduino test sketch —— [teensy41_psram_memtest](https://github.com/PaulStoffregen/teensy41_psram_memtest)

- https://arduino.stackexchange.com/questions/81253/teensy4-1-with-2x-8mb-psram-chips-external-psram-size-0-but-extmem-char-works

- https://protosupplies.com/learn/prototyping-system-for-teensy-4-1-working-with-teensy-4-1-memory/

```c
//===============================================================================
//  Find Optional Memory Chips on Teensy 4.1
//===============================================================================
#include "LittleFS.h"
extern "C" uint8_t external_psram_size;

//===============================================================================
//  Initialization
//===============================================================================
void setup() {
  Serial.begin(115200);       //Initialize USB serial port to computer

  // Check for PSRAM chip(s) installed
  uint8_t size = external_psram_size;
  Serial.printf("PSRAM Memory Size = %d Mbyte\n", size);
  if (size == 0) {
    Serial.println ("No PSRAM Installed");
  }

// Check for either NOR or NAND Flash chip installed
  LittleFS_QSPIFlash myfs_NOR;    // NOR FLASH
  LittleFS_QPINAND myfs_NAND;      // NAND FLASH 1Gb

  // Check for NOR Flash chip installed
  if (myfs_NOR.begin()) {
    Serial.printf("NOR Flash Memory Size = %d Mbyte / ", myfs_NOR.totalSize() / 1048576);
    Serial.printf("%d Mbit\n", myfs_NOR.totalSize() / 131072);
  }
  // Check for NAND Flash chip installed
  else if (myfs_NAND.begin()) {
    Serial.printf("NAND Flash Memory Size =  %d bytes / ", myfs_NAND.totalSize());
    Serial.printf("%d Mbyte / ", myfs_NAND.totalSize() / 1048576);
    Serial.printf("%d Gbit\n", myfs_NAND.totalSize() * 8 / 1000000000);
  }
  else {
    Serial.printf("No Flash Installed\n");
  }
}
void loop() {
  // put your main code here, to run repeatedly:

}
```
