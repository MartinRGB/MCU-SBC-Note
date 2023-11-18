#include <Arduino.h>
#include <Wire.h>
#include "PAJ7620U2.h"



uint8_t I2C_readByte(uint8_t  addr)
{
  Wire.beginTransmission(PAJ7620U2_I2C_ADDRESS);
  Wire.write(addr);
  Wire.endTransmission();
  Wire.requestFrom(PAJ7620U2_I2C_ADDRESS, 1);
  if (Wire.available()) {
   return Wire.read();
  }
  return 0;
}
uint16_t I2C_readU16(uint8_t addr)
{
 uint16_t x; uint16_t t;

  Wire.beginTransmission(PAJ7620U2_I2C_ADDRESS);
  Wire.write(addr); 
  Wire.endTransmission();
  Wire.requestFrom(PAJ7620U2_I2C_ADDRESS, 2);
  t = Wire.read();
  x = Wire.read();
  x <<= 8;
  x |= t;
  return x;
}
void I2C_writeByte(uint8_t addr, uint8_t data)
{
  Wire.beginTransmission(PAJ7620U2_I2C_ADDRESS);
  Wire.write(addr);
  Wire.write(data & 0xFF);
  Wire.endTransmission();
}
uint8_t PAJ7620U2_init()
{
  uint8_t i,State;
  State =I2C_readByte(0x00);                       //Read State
  if (State != 0x20) return 0;                      //Wake up failed
  I2C_writeByte(PAJ_BANK_SELECT, 0);                    //Select Bank 0
  for (i=0;i< Init_Array;i++)
  {
    I2C_writeByte(Init_Register_Array[i][0], Init_Register_Array[i][1]);//Power up initialize
  }
  return 1;
}
