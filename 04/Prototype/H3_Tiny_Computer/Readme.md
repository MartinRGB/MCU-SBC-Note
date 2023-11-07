
<img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/541298eb-1428-4145-9eb8-d0831305145f" width="50%" height="50%">

# Device used

- NanoPi Duo2
  
  <img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/ffc7aaa2-5fb8-406e-a335-180fce53fc26" width="50%" height="50%">

- HR91105A 5pins RJ45 Ethernet module

  <img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/a3305b80-9970-4af9-b05a-796c08c3cbce" width="50%" height="50%">

- USB Type A 4pins breakout board
  
  <img src="https://github.com/MartinRGB/MCU-SBC-Note/assets/7036706/4f13ca1a-c425-46d6-8ad8-bb55e8f7e8b6" width="50%" height="50%">

- ILI9341 2.8 inch
  - tut [here](https://github.com/MartinRGB/MCU-SBC-Note/tree/main/01-Screen/ili9341_drivers)
 
### Steps

- Connect USB board to Duo2
  - USB's D+   to Duo2's USB3-D+
  - USB's D-   to Duo2's USB3-D-
  - USB's VBUS to Duo2's 3V3
  - USB's GND  to Duo2's GND
  
- Connect Ethernet board to Duo2
  - Ethernet's R-  to Duo2's EPHY-RXN
  - Ethernet's R+  to Duo2's EPHY-RXP
  - Ethernet's T+  to Duo2's EPHY-TXP
  - Ethernet's T-  to Duo2's EPHY-TXN
  - Ethernet's GND to Duo2's GND

- Connenct ILI9341 to Duo2

