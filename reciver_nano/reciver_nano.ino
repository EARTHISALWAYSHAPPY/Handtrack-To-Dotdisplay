#include <LedControl.h>
LedControl lc = LedControl(11, 13, 10, 1);
byte goodjob[8] = {
  B00000000,
  B01100110,
  B01100110,
  B00000000,
  B10000001,
  B01000010,
  B00111100,
  B00000000
};
byte fighting[8] = {
  B01010000,
  B01010000,
  B01010000,
  B01111100,
  B01100110,
  B01011010,
  B01100110,
  B00100100
};
byte love[8] = {
  B00000000,
  B01100110,
  B11111111,
  B11111111,
  B11111111,
  B01111110,
  B00111100,
  B00011000
};
byte star[8] = {
  B00011000,
  B00100100,
  B11100111,
  B10000001,
  B01000010,
  B10000001,
  B10011001,
  B11100111
};
void setup() {
  Serial.begin(115200);
  DDRD |= B01110000;
  lc.shutdown(0, false);
  lc.setIntensity(0, 5);
  lc.clearDisplay(0);
}

unsigned long lastTime = 0;
const unsigned long Delay = 1000;

void loop() {
  check_process();
}

void check_process() {
  static char preCommand = '\0';  // empty char
  if (Serial.available() > 0) {
    char realcommand = Serial.read();
    if (realcommand != preCommand) {
      preCommand = realcommand;
      process(realcommand);
      lastTime = millis();
    }
  } else {
    if (millis() - lastTime > Delay) {
      turnOff();
      lc.clearDisplay(0);
      preCommand = '\0';
    }
  }
}

void process(char command) {
  switch (command) {
    case 'A':
      PORTD |= 0x40;
      show_goodjob();
      break;
    case 'B':
      PORTD |= 0x20;
      show_fighting();
      break;
    case 'C':
      PORTD |= 0x60;
      show_love();
      break;
    case 'D':
      PORTD |= 0x10;
      show_star();
      break;
    default:
      break;
  }
}
void turnOff() {
  PORTD &= B11101111;
  PORTD &= B11011111;
  PORTD &= B10111111;
}
void show_goodjob() {
  for (int i = 0; i < 8; i++) lc.setRow(0, i, goodjob[i]);
}
void show_fighting() {
  for (int i = 0; i < 8; i++) lc.setRow(0, i, fighting[i]);
}
void show_love() {
  for (int i = 0; i < 8; i++) lc.setRow(0, i, love[i]);
}
void show_star() {
  for (int i = 0; i < 8; i++) lc.setRow(0, i, star[i]);
}
