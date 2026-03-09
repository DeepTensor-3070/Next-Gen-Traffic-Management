int red = 8;
int yellow = 9;
int green = 10;

int cars = 0;

void setup() {

  Serial.begin(9600);

  pinMode(red, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(green, OUTPUT);

  digitalWrite(red, HIGH);
}

void loop() {

  if (Serial.available()) {

    cars = Serial.parseInt();

    int greenTime;

    if (cars <= 2)
      greenTime = 5000;

    else if (cars <= 4)
      greenTime = 10000;

    else
      greenTime = 15000;


    digitalWrite(red, LOW);
    digitalWrite(green, HIGH);
    delay(greenTime);

    digitalWrite(green, LOW);
    digitalWrite(yellow, HIGH);
    delay(2000);

    digitalWrite(yellow, LOW);
    digitalWrite(red, HIGH);
    delay(5000);
  }
}
