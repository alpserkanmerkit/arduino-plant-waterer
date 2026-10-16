/*
  plant-watering ("Super Fulffy") — Alp Serkan Merkit, MIT License

  Example sketch written 2026 for the owner's Tinkercad circuit "Super Fulffy";
  the original Tinkercad code was not preserved.

  Pins (read from the Tinkercad design, see docs/wiring.png):
    soil moisture sensor SIG -> A0, servo signal -> D9, both powered from the Uno 5 V / GND.
  Behaviour: when the soil is dry the servo turns to ANGLE_OPEN for WATER_MS (to let water flow),
  turns back, then waits SOAK_MS so the water can reach the sensor before the next reading.
  The water mechanism itself (a tipping bottle, a tube clamp ...) is not part of the Tinkercad design.

  Calibrate DRY_BELOW: open the Serial Monitor (9600 baud), note the value with the prongs in dry soil
  and in wet soil, and set DRY_BELOW between the two. With this kind of resistive probe a higher value
  means wetter soil (capacitive probes read the other way round).
*/
#include <Servo.h>

const int SOIL_PIN  = A0;
const int SERVO_PIN = 9;

const int DRY_BELOW    = 300;      // tune: below this the soil counts as dry
const int ANGLE_CLOSED = 0;
const int ANGLE_OPEN   = 90;
const unsigned long WATER_MS = 2000;
const unsigned long SOAK_MS  = 10000;

Servo valve;

void setup() {
  valve.attach(SERVO_PIN);
  valve.write(ANGLE_CLOSED);
  Serial.begin(9600);
}

void loop() {
  int moisture = analogRead(SOIL_PIN);   // 0..1023
  Serial.print("moisture=");
  Serial.println(moisture);

  if (moisture < DRY_BELOW) {
    Serial.println("dry -> watering");
    valve.write(ANGLE_OPEN);
    delay(WATER_MS);
    valve.write(ANGLE_CLOSED);
    delay(SOAK_MS);
  }
  delay(1000);
}
