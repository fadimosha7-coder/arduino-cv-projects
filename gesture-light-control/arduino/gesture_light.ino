int ledPin9 = 9;
int ledPin10 = 10;
int ledPin11 = 11;
int ledPin12 = 12;
int ledPin13 = 13;

void setup () {
  pinMode(ledPin9,OUTPUT);
  pinMode(ledPin10,OUTPUT);
  pinMode(ledPin11,OUTPUT);
  pinMode(ledPin12,OUTPUT);
  pinMode(ledPin13,OUTPUT);
  Serial.begin(9600);
  Serial.println("LED BRIGHTNESS CONTROLLER");
}

void loop() {
  if (Serial.available() > 0) {
    int brightness = Serial.parseInt();
    brightness = constrain(brightness,0,255);
    analogWrite(ledPin9, brightness);
    analogWrite(ledPin10, brightness);
    analogWrite(ledPin11, brightness);
    analogWrite(ledPin12, brightness);
    analogWrite(ledPin13, brightness);

    Serial.print("LED BRIGHTNESS: ");
    Serial.println(brightness);

    while (Serial.available() > 0) {
      Serial.read();
    }
  }
}