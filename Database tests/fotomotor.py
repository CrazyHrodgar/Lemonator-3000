import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

import serial, time

cap = cv.VideoCapture(0)

encoding = 'utf-8'

arduino = serial.Serial('COM8',9600) ### Para el Arduino Mega 2560, esto solo aplica en mi computadora.
# arduino = serial.Serial('COM7',9600) ### Para el Arduino UNO, esto solo aplica en mi computadora x2
time.sleep(2) # Pequeño tiempo de espera para que se inicialize bien la comunicacion serial

image_list = []
new_path = r'C:\Users\caoti\Desktop\Lemon Images\Database/'

while True:

	ret, frame = cap.read()
	cv.imshow('Camera', frame)

	rawString = arduino.readline()
	print(rawString)
	ns = str(rawString, encoding)

	if ns == '1\r\n':
		ret3, img1 = cap.read()
		cv.imshow('Snap 1', img1)
		image_list.append(img1)

	if cv.waitKey(1) & 0xFF == ord('q'): # Presionar 'q' para detener la toma de imagenes
		break

cap.release() # Se liberan las camara(s)
cv.destroyAllWindows() # Se destruyen todas la ventanas de opencv
arduino.close() # Se cierra la comunicacion serial con el arduino

### Con esta función se guardan las imágenes obtenidas
def gen_name(num):
	for i in range(num):
		filename = new_path + 'img' + str(i) + '.png'
		print(filename)
		cv.imwrite(filename, image_list[i])

gen_name(len(image_list))
