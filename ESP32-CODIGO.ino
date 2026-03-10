#include <ESP32Servo.h>

Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;

String dataString = "";

int thumbAngle = 90;
int indexAngle = 90;
int middleAngle = 90;
int ringAngle = 90;
int pinkyAngle = 90;

// Pines del ESP32
int pinThumb = 13;
int pinIndex = 12;
int pinMiddle = 14;
int pinRing = 27;
int pinPinky = 26;

void setup() {

  Serial.begin(115200);

  servoThumb.attach(pinThumb);
  servoIndex.attach(pinIndex);
  servoMiddle.attach(pinMiddle);
  servoRing.attach(pinRing);
  servoPinky.attach(pinPinky);

  servoThumb.write(90);
  servoIndex.write(90);
  servoMiddle.write(90);
  servoRing.write(90);
  servoPinky.write(90);

}

void loop() {

  if (Serial.available()) {

    dataString = Serial.readStringUntil('\n');

    int values[5];
    int index = 0;

    char *token = strtok((char*)dataString.c_str(), ",");

    while (token != NULL && index < 5) {
      values[index] = atoi(token);
      token = strtok(NULL, ",");
      index++;
    }

    if (index == 5) {

      thumbAngle = constrain(values[0], 0, 180);
      indexAngle = constrain(values[1], 0, 180);
      middleAngle = constrain(values[2], 0, 180);
      ringAngle = constrain(values[3], 0, 180);
      pinkyAngle = constrain(values[4], 0, 180);

      servoThumb.write(thumbAngle);
      servoIndex.write(indexAngle);
      servoMiddle.write(middleAngle);
      servoRing.write(ringAngle);
      servoPinky.write(pinkyAngle);

    }
  }

}

