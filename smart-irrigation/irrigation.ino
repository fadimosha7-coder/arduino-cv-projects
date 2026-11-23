int soil = 8;
int pump1 = 10;
int pump2 = 9;
int value = 0;

void setup() {

pinMode(soil, INPUT);
pinMode(pump1, OUTPUT);
pinMode(pump2, OUTPUT);
Serial.begin(9600);
}


void loop() {
  value = digitalRead(soil);
  Serial.print(value);    
  
   if (value == 0) {

    digitalWrite(pump1, LOW);
    digitalWrite(pump2, LOW);

  }
   else{
    digitalWrite(pump1, HIGH);
  digitalWrite(pump2, HIGH);
}
}