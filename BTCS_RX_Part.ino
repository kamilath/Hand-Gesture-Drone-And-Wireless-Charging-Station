#include <LiquidCrystal.h>

LiquidCrystal lcd(8, 9, 10, 11, 12, 13);

#define splash splash1
#define python Serial

#define m1 7
#define m2 6
#define m3 2
#define m4 4
#define en1 5
#define en2 3

float t = 0.0;
float vlb_chv;
float bt_t = 0.0;

String IncomingData = "";
int speed1 = 255;
int speed2 = 255;

void (*resetFunc)(void) = 0;


void setup() {
  LcDSet();
  Serial.begin(115200);
  python.begin(115200);
  pinMode(m1, OUTPUT);
  pinMode(m2, OUTPUT);
  pinMode(m3, OUTPUT);
  pinMode(m4, OUTPUT);
  pinMode(en1, OUTPUT);
  pinMode(en2, OUTPUT);
  analogWrite(en1, speed1);
  analogWrite(en2, speed2);
  digitalWrite(m1, LOW);
  digitalWrite(m2, LOW);
  digitalWrite(m3, LOW);
  digitalWrite(m4, LOW);

  lcd.clear();
  python.println("Ready");
}

void LcDSet() {
  lcd.begin(16, 2);

  splash(0, "Gesture Drone");
  splash(1, "");

  delay(2000);
  lcd.clear();
}

void loop() {
  while (python.available()) {
    IncomingData = python.readString();
    delayMicroseconds(5);
  }

  if (IncomingData.length() > 0) {
    splash(1, IncomingData);
    if (IncomingData == "Land") {
      splash(1, "Land");
      for (int pos = 255; pos >= 0; pos -= 1) {
        analogWrite(en1, pos);
        analogWrite(en2, pos);
        delay(20);
      }

      python.println("Landed");
      splash(1, "Landed");
    }

    else if (IncomingData == "Up") {
      splash(1, "Up");
      speed1 = 255;
      speed2 = 255;

      digitalWrite(m1, HIGH);
      digitalWrite(m2, LOW);
      digitalWrite(m3, HIGH);
      digitalWrite(m4, LOW);
      analogWrite(en1, speed1);
      analogWrite(en2, speed2);
    } else if (IncomingData == "Down") {
      splash(1, "Down");
      speed1 = 100;
      speed2 = 100;

      digitalWrite(m1, HIGH);
      digitalWrite(m2, LOW);
      digitalWrite(m3, HIGH);
      digitalWrite(m4, LOW);

      analogWrite(en1, speed1);
      analogWrite(en2, speed2);

    } else if (IncomingData == "Left") {
      splash(1, "Left");
      speed1 = 255;
      speed2 = 80;

      digitalWrite(m1, HIGH);
      digitalWrite(m2, LOW);
      digitalWrite(m3, HIGH);
      digitalWrite(m4, LOW);
      analogWrite(en1, speed1);
      analogWrite(en2, speed2);
    } else if (IncomingData == "Right") {
      splash(1, "Right");
      speed1 = 80;
      speed2 = 255;

      digitalWrite(m1, HIGH);
      digitalWrite(m2, LOW);
      digitalWrite(m3, HIGH);
      digitalWrite(m4, LOW);
      analogWrite(en1, speed1);
      analogWrite(en2, speed2);
    }

    IncomingData = "";
  }

  float vlc = getVolt2(A1);
  float vlb = getVolt(A0);

  float vlc_fn = vlc;

  if (vlc > 7.5 && vlb_chv < 13.50) {
    splash(1, "Charging");
    vlb_chv = vlb + bt_t;
    vlc_fn = vlc + bt_t;
  } else if (vlc > 7.5 && vlb_chv > 13.50) {
    splash(1, "Battery Full");
    vlb_chv = vlc_fn;
  } else {
    // splash(1, "DisCharging");
    vlc_fn = vlc + 0;
    vlb_chv = vlb + bt_t;
  }

  if (vlc > 7.5 && vlb > 13.51) {
    bt_t += 0;
  } else if (vlc > 7.5 && vlb > 12) {
    bt_t += 0.007;
  } else if (vlc > 7.5 && vlb > 11) {
    bt_t += 0.003;
  } else if (vlc > 7.5 && vlb > 10) {
    bt_t += 0.006;
  }

  lcd.setCursor(0, 0);
  lcd.print("B:     ");
  lcd.setCursor(2, 0);
  lcd.print(vlb_chv);
  lcd.setCursor(9, 0);
  lcd.print("C:     ");
  lcd.setCursor(11, 0);
  lcd.print(vlc_fn);
  lcd.setCursor(9, 1);

  delay(200);
}

float getVolt(int pin) {
  int value = 0;
  float vout = 0.0;
  float vin = 0.0;
  float R1 = 10052.0;
  float R2 = 960.0;
  value = analogRead(pin);
  vout = (value * 5.0) / 1023.0;
  vin = vout / (R2 / (R1 + R2));
  if (vin < 0.09) {
    vin = 0.0;
  }
  return vin;
}

float getVolt2(int pin) {
  int value = 0;
  float vout = 0.0;
  float vin = 0.0;
  float R1 = 10052.0;
  float R2 = 960.0;
  value = analogRead(pin);
  vout = (value * 5.0) / 1023.0;
  vin = vout / (R2 / (R1 + R2));
  if (vin < 0.09) {
    vin = 0.0;
  }
  return vin;
}

void splash1(int row, String txt) {
  int curs = (17 - txt.length()) / 2;
  lcd.setCursor(0, row);
  lcd.print("----------------");

  lcd.setCursor(curs, row);
  lcd.print(txt);
  delay(100);
}
