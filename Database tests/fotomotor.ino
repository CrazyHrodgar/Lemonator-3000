// Se carga la libreria Stepper para poder controlar motores a pasos
#include <Stepper.h>

const int stepsPerRevolution = 200; // Número total de revoluciones del motor NEMA 17
int boton = 2; // Puerto digital donde se coloca el push button
int led = 13; // Puerto del led integrado en la placa
int estado = 0, cont = 0; // Variables necesarias para el programa
const int step = 50; // Valor fijo para  el ciclo for

// Se define el motor a pasos así como los pines donde se conectaran las bobinas
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);


void setup()
{
  // Se establece una velocidad de 30 rpm. Se puede cambiar la velocidad si se requiere
  myStepper.setSpeed(30);
  pinMode(boton, INPUT); // Declaramos el puerto del push button como entrada
  // Inicializamos el puerto serial
  Serial.begin(9600);
}

void loop()
{
  // Se lee el puerto digital del push button
  estado = digitalRead(boton);
  // Envía 0 al puerto serial, esto sirve para que en Python se observe en "tiempo real" la camara, de lo contrario solo se veran las imágenes
  // cuando se presione el push button
  Serial.println("0");
  delay(50);

  // Si se presiona el push button entra este ciclo
  if (estado == HIGH) {
    cont = 0;
    for (int i = 0; i < 5; i++) {
      cont = cont + step;
      myStepper.step(50); // Se mueve 50 pasos el motor
      digitalWrite(led, HIGH); // Led indicando el funcionamiento
      delay(2000); // Espera dos segundos para que la cámara enfoque el limón
      Serial.println(1); // Manda 1 al puerto serial con lo cual el programa de Python toma una fotografía
      delay(500); // Espera 500 milisegundos
    }
  }
}
