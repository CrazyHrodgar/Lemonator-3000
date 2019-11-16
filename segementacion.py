import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

cap = cv.VideoCapture(0)


while True:

    ret, frame = cap.read()
    cv.imshow('Imagen', frame)

    # frame = cv.resize(frame, (0,0), fx = 0.5, fy = 0.5)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # Convertir a escala de grises
    th, threshed = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV|cv.THRESH_OTSU)
    # th, threshed = cv.threshold(gray, 127, 255, cv.THRESH_BINARY|cv.THRESH_OTSU)
    cv.imshow('Threshed', threshed)
    # cv.imshow('Threshed2',threshed2)

    cnts = cv.findContours(threshed, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2]
    cnts = sorted(cnts, key=cv.contourArea)

    for cnt in cnts:
        if cv.contourArea(cnt) > 10000:
            break

    mask = np.zeros(frame.shape[:2], np.uint8)
    cv.drawContours(mask, [cnt],-1, 255, -1)
    dst = cv.bitwise_and(frame, frame, mask=mask)
    cv.imshow('Resultado', dst)


    if cv.waitKey(1) & 0xFF == ord('q'): # Presionar 'q' para detener la toma de imagenes
        break

cap.release() # Se liberan las camara(s)
cv.destroyAllWindows() # Se destruyen todas la ventanas de opencv
