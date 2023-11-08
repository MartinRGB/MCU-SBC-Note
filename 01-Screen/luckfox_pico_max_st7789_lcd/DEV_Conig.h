/*****************************************************************************

* | File      	:   DEV_Config.h

* | Author      :   Luckfox team

* | Function    :   Hardware underlying interface

* | Info        :

*----------------

* |	This version:   V2.0

* | Date        :   2019-07-08

* | Info        :   Basic version

*

******************************************************************************/

#ifndef _DEV_CONFIG_H_

#define _DEV_CONFIG_H_



#include "Debug.h"



#define USE_DEV_LIB 1



#ifdef USE_DEV_LIB

    #include "sysfs_gpio.h"

    #include "dev_hardware_SPI.h"

	#include <stdio.h>

	#include <unistd.h>

	#include <stdlib.h>

	#include <pthread.h>

	// #define USE_DEV_LIB_PWM

#endif

#include <unistd.h>



#include <errno.h>

#include <stdio.h>

#include <string.h>

#include <stdint.h>



/**

 * data

**/

#define UBYTE   uint8_t

#define UWORD   uint16_t

#define UDOUBLE uint32_t



// #define LCD_DC   (34)

// #define LCD_CS   (48)

// #define LCD_RST  (51)

// #define LCD_BL   (4)



#define LCD_DC   (73)

#define LCD_CS   (48)

#define LCD_RST  (51)

#define LCD_BL   (72)



//LCD

#define LCD_CS_0		DEV_Digital_Write(LCD_CS,0)

#define LCD_CS_1		DEV_Digital_Write(LCD_CS,1)



#define LCD_RST_0		DEV_Digital_Write(LCD_RST,0)

#define LCD_RST_1		DEV_Digital_Write(LCD_RST,1)



#define LCD_DC_0		DEV_Digital_Write(LCD_DC,0)

#define LCD_DC_1		DEV_Digital_Write(LCD_DC,1)



#define LCD_BL_0		DEV_Digital_Write(LCD_BL,0)

#define LCD_BL_1		DEV_Digital_Write(LCD_BL,1)



/*PICO*/

// #define KEY_UP_PIN      55

// #define KEY_DOWN_PIN    134

// #define KEY_LEFT_PIN    137

// #define KEY_RIGHT_PIN   131

// #define KEY_PRESS_PIN   54 

// #define KEY1_PIN        57

// #define KEY2_PIN        136

// #define KEY3_PIN        16

// #define KEYA_PIN        57

// #define KEYB_PIN        136

// #define KEYX_PIN        130

// #define KEYY_PIN        132



/*PLUS*/

#define KEY_UP_PIN      55

#define KEY_DOWN_PIN    101

#define KEY_LEFT_PIN    102

#define KEY_RIGHT_PIN   98

#define KEY_PRESS_PIN   54 

#define KEY1_PIN        57

#define KEY2_PIN        69 //103

#define KEY3_PIN        16

#define KEYA_PIN        57

#define KEYB_PIN        103

#define KEYX_PIN        100

#define KEYY_PIN        99



#define GET_KEY_UP       		DEV_Digital_Read(KEY_UP_PIN) //

#define GET_KEY_DOWN     		DEV_Digital_Read(KEY_DOWN_PIN)

#define GET_KEY_LEFT     		DEV_Digital_Read(KEY_LEFT_PIN)

#define GET_KEY_RIGHT    		DEV_Digital_Read(KEY_RIGHT_PIN)

#define GET_KEY_PRESS    		DEV_Digital_Read(KEY_PRESS_PIN) //

#define GET_KEY1         		DEV_Digital_Read(KEY1_PIN) //

#define GET_KEY2         		DEV_Digital_Read(KEY2_PIN) //

#define GET_KEY3         		DEV_Digital_Read(KEY3_PIN)

#define GET_KEYA         		DEV_Digital_Read(KEYA_PIN)

#define GET_KEYB         		DEV_Digital_Read(KEYB_PIN)

#define GET_KEYX         		DEV_Digital_Read(KEYX_PIN)

#define GET_KEYY         		DEV_Digital_Read(KEYY_PIN) 



#define LCD_SetBacklight(Value) DEV_SetBacklight(Value)



/*------------------------------------------------------------------------------------------------------*/

UBYTE DEV_ModuleInit(void);

void DEV_ModuleExit(void);



void DEV_GPIO_Mode(UWORD Pin, UWORD Mode);

void DEV_Digital_Write(UWORD Pin, UBYTE Value);

UBYTE DEV_Digital_Read(UWORD Pin);

void DEV_Delay_ms(UDOUBLE xms);



void DEV_SPI_WriteByte(UBYTE Value);

void DEV_SPI_Write_nByte(uint8_t *pData, uint32_t Len);

void DEV_SetBacklight(UWORD Value);

#endif
