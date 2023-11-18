
#include <Wire.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "PAJ7620U2.h"

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 26 // Popular NeoPixel ring size
#define RGB_PIN        6 // On Trinket or Gemma, suggest changing this to 1
#define SPEED_READ_PIN 2
#define SPEED_WRITE_PIN A1
#define SLIDER_PIN A6
#define SLIDER_LED_PIN A7
#define LEDUPDATE 1000

int WSUpdate = 500;
long WSTimeStamp=0;              // Type needs to match millis() function

#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

Adafruit_NeoPixel pixels(NUMPIXELS, RGB_PIN, NEO_GRB + NEO_KHZ800);

long TimeStamp=0;              // Type needs to match millis() function
int  NumberOfPulses;  // Used in interrupt function so make volatile
int LastReading;

int sliderValue,sliderMapFanSpeedValue,sliderMapRGBSpeedValue;  //variable to store sensor value
float mapGreyScaleValue;
double RPMValue;

unsigned short  Gesture_Data;
String  myString;
int RV = 0;
int GV = 150;
int BV = 0;

void setup()
{
  Serial.begin(115200);
  // Set up interrupt pin with pull-up so that it reliably detects FALLING
  pinMode(SPEED_READ_PIN,INPUT_PULLUP);
  pinMode(SPEED_WRITE_PIN,OUTPUT);
  pinMode(SLIDER_PIN,OUTPUT);
  pinMode(SLIDER_LED_PIN,INPUT);
  // Set an interrupt to trigger with a falling edge on pin 2/3
  attachInterrupt(digitalPinToInterrupt(D2),PulseCount,FALLING); // 0/1 means pin 2/3
  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
    clock_prescale_set(clock_div_1);
  #endif
  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)

  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  // Clear the buffer
  display.clearDisplay();

  // Show the display buffer on the screen. You MUST call display() after
  // drawing commands to make them visible on screen!
  display.display();
  delay(2000);

  uint8_t i;

  Serial.print("\nGesture Sensor Test Program ...\n");
  delayMicroseconds(800);
  Wire.begin();
  delayMicroseconds(10);
  while(!PAJ7620U2_init())
  { Serial.print("\nGesture Sensor Error\n");
    delay(500);
  }
  Serial.print("\nGesture Sensor OK\n");
  I2C_writeByte(PAJ_BANK_SELECT, 0);//Select Bank 0
  for (i = 0; i < Gesture_Array_SIZE; i++)
  {
    I2C_writeByte(Init_Gesture_Array[i][0], Init_Gesture_Array[i][1]);//Gesture register initializes
  }

}

// Interrupt function for speed measurement
void PulseCount()
{
  NumberOfPulses++; // Just increment count
  return;
}

void loop()
{
  if(millis()-TimeStamp>LEDUPDATE)
    { 
      detachInterrupt(digitalPinToInterrupt(SPEED_READ_PIN));
      if(NumberOfPulses<3)NumberOfPulses=0; // Fan still outputs 1 or 2 pulses each second even when stopped!

      //Serial.println((double)(NumberOfPulses+LastReading)/2*30000.00/(double)LEDUPDATE);

      RPMValue = (double)(NumberOfPulses+LastReading)/2*30000.00/(double)LEDUPDATE;
      Serial.println((String)"RPM Value:" + RPMValue);
      LastReading=NumberOfPulses;
      NumberOfPulses=0;

      // Re-attach the interrupt
      attachInterrupt(digitalPinToInterrupt(SPEED_READ_PIN),PulseCount,FALLING); // 0/1 means pin 2/3

      Gesture_Data = I2C_readU16(PAJ_INT_FLAG1);
      
      if (Gesture_Data)
      {
        switch (Gesture_Data)
        {
          case PAJ_UP:                   Serial.print("Up\r\n");     myString="Up";  RV=0;GV=0;BV=255;     break;
          case PAJ_DOWN:                 Serial.print("Down\r\n");   myString="Down"; RV=255;GV=0;BV=0;      break;
          case PAJ_LEFT:                 Serial.print("Left\r\n");   myString="Left"; RV=random(0,255);GV=random(0,255);BV=random(0,255);      break;
          case PAJ_RIGHT:                Serial.print("Right\r\n");  myString="Right"; RV=0;GV=150;BV=0;      break;
          case PAJ_FORWARD:              Serial.print("Forward\r\n");myString="Forward";       break;
          case PAJ_BACKWARD:             Serial.print("Backward\r\n");myString="Backward";      break;
          case PAJ_CLOCKWISE:            Serial.print("Clockwise\r\n");myString="Clockwise";     break;
          case PAJ_COUNT_CLOCKWISE:      Serial.print("AntiClockwise\r\n");myString="AntiClockwise"; break;
          case PAJ_WAVE:                 Serial.print("Wave\r\n");  myString="Wave";        break;
          default: break;
        }
        Gesture_Data=0;
      }

      display.clearDisplay();
      display.setTextSize(1);             // Normal 1:1 pixel scale
      display.setTextColor(WHITE);        // Draw white text
      display.setCursor(28,8);             // Start at top-left corner
      display.println("RPM: " + String(RPMValue));

      display.setCursor(28,20);             // Start at top-left corner
      display.println("R: " + String(RV));
      display.setCursor(28,36);             // Start at top-left corner
      display.println("G: " + String(GV));
      display.setCursor(28,52);             // Start at top-left corner
      display.println("B: " + String(BV));
      display.display();
     
      // Save a new timestamp
      TimeStamp=millis();
  }

  sliderValue = analogRead(SLIDER_PIN);
  sliderMapFanSpeedValue = map(sliderValue,0,1023,0,255);
  sliderMapRGBSpeedValue = map(sliderValue,0,1023,250,16);
  mapGreyScaleValue = map(sliderValue,0,1023,0.1,1.0);
  //Serial.println(sliderValue);
  analogWrite(SLIDER_LED_PIN,sliderMapFanSpeedValue);
  analogWrite(SPEED_WRITE_PIN,sliderMapFanSpeedValue);
  // Deal with overflow
  if(millis()<TimeStamp)TimeStamp=millis();


  if(millis()-WSTimeStamp>WSUpdate)
  { 
     
      pixels.clear(); // Set all pixel colors to 'off'
      for(int a=0; a<NUMPIXELS; a++) { // For each pixel...

        // pixels.Color() takes RGB values, from 0,0,0 up to 255,255,255
        // Here we're using a moderately bright green color:
        pixels.setPixelColor(a, pixels.Color(RV, GV, BV));

        pixels.show();   // Send the updated pixel colors to the hardware.

        delay(33); // Pause before next pass through loop
      }

      WSTimeStamp=millis();
  }

// Deal with overflow
  if(millis()<WSTimeStamp)WSTimeStamp=millis();

  // Comment this to deal busy port
  //The first NeoPixel in a strand is #0, second is 1, all the way up
  //to the count of pixels minus one.
  



} // END OF loop()