#include<Stepper.h>

#define s1 2
#define s2 3
#define s3 4
#define s4 5

const int num_steps = 50;
int count = 0;
int ss1 = 0;
int led = 13;

Stepper myStepper(num_steps, 8, 9, 10, 11);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
//  Serial.println("Fotos");
  pinMode(s1, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  ss1 = digitalRead(s1);
  myStepper.setSpeed(60);
  Serial.println("2");
  delay(50);
  
  if (ss1 == HIGH){
    count = count + num_steps;
    myStepper.step(num_steps);
    Serial.println(count);digitalWrite(led,HIGH);
    delay(1000);
    Serial.println("1");
    delay(1000);
    
    if (count == 200){
      count = 0;
      Serial.println("Restableciendo");
      myStepper.step(1);
      delay(1000);
    }
  }
  
}
