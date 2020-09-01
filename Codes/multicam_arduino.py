### El código que va en el arduino es el sensor_ir.ino

import cv2 as cv
import serial, time # La libreria serial sirve para establecer la comunicacion entre arduino y python
					# Si no está instalada un pip install pyserial bastará ;)
import numpy as np
import matplotlib.pyplot as plt

cap = cv.VideoCapture(1)
cap2 = cv.VideoCapture(2)

encoding = 'utf-8'

arduino = serial.Serial('COM4',9600) ### Para el Arduino Mega 2560, esto solo aplica en mi computadora.
# arduino = serial.Serial('COM7',9600) ### Para el Arduino UNO, esto solo aplica en mi computadora x2
time.sleep(2) # Pequeño tiempo de espera para que se inicialize bien la comunicacion serial



# while (cap.isOpened()):
while True:
	ret, frame = cap.read()
	cv.imshow('Feed 1', frame)

	ret2, frame2 = cap2.read()
	cv.imshow('Feed 2', frame2)
	
	rawString = arduino.readline()
	print(rawString)
	ns = str(rawString, encoding)
	
	# if ns == "0\r\n":
	if ns == "1\r\n":
		# print('activo')
		ret4, img2 = cap2.read()
		cv.imshow('Snap 2', img2)
		# cv.imwrite('cam_down.tiff',img2)
		
		ret3, img1 = cap.read()
		cv.imshow('Snap 1', img1)
		# cv.imwrite('cam_up.tiff',img1)

	if cv.waitKey(1) & 0xFF == ord('q'): # Presionar 'q' para detener la toma de imagenes
		break

cap.release() # Se liberan las camara(s)
cv.destroyAllWindows() # Se destruyen todas la ventanas de opencv
arduino.close() # Se cierra la comunicacion serial con el arduino
