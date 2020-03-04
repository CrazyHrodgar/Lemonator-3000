const int sensorPin = 9;
//const int sensorPin = 0;
const int output = 13;
int value = 0;

void setup() {
  Serial.begin(9600);   //iniciar puerto serie
  pinMode(sensorPin , INPUT);  //definir pin como entrada
  pinMode(output, OUTPUT);
}

void loop() {
//  value = 0;
  
  value = digitalRead(sensorPin );  //lectura digital de pin
//  Serial.println(value);

  if (value == 1) {
    digitalWrite(output, LOW);
    Serial.println("1");
  } else {
    digitalWrite(output, HIGH);
    Serial.println("0");
  }
  delay(50); // Tiempo en milisegundos (ms)
}
