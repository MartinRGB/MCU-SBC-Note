#define ROTATOR_PIN A0
#define BUTTON_PIN 10

#define WL_PIN  3
#define CL_PIN  5

float rotatorValue;  //variable to store sensor value
byte buttonState;
float mapBrightnessValue;
float mapWarmValue = 1;
float mapColdValue = 1;
void setup() {
  Serial.begin(9600);
  pinMode(ROTATOR_PIN, INPUT);
  pinMode(BUTTON_PIN, INPUT);
  pinMode(WL_PIN,OUTPUT);
  pinMode(CL_PIN,OUTPUT);
}

void loop() {
  buttonState = digitalRead(BUTTON_PIN);
  rotatorValue = analogRead(ROTATOR_PIN);
  Serial.println(rotatorValue);
  
  if (buttonState == HIGH) {
      Serial.println("Button is pressed");
      mapBrightnessValue = map(rotatorValue,0,1023,0,42);
      analogWrite(WL_PIN, mapBrightnessValue * 1.5);
      analogWrite(CL_PIN, (42 - mapBrightnessValue)* 1.5);
  }
  else {
      Serial.println("Button is not pressed");
      mapBrightnessValue = map(rotatorValue,0,1023,0,42);
      analogWrite(WL_PIN, mapBrightnessValue);
      analogWrite(CL_PIN, mapBrightnessValue);
  }
  
}
