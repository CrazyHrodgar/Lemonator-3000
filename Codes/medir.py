### Importar librerias

from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import imutils
import cv2

### Función de ayuda para calcular el punto medio

def midpoint (ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# Se establece el width del objeto de referencia
# para obtener el valor del pixels per metric
# la formula es ppm = pixeles / radio del objeto

width = 200
r = 38

# Lectura de la imagen y su procesamiento
# img = cv2.imread('shapes.jpg')
img = cv2.imread(r'C:\Users\caoti\Desktop\Lemon Images\Groundtruth\manually segmented/si0.png')
# img = cv2.imread(r'C:\Users\caoti\Desktop\Lemon Images\Processed\miniset/im8.png')
# img = cv2.imread(r'C:\Users\caoti\Desktop\Lemon Images\Processed/im878.png')
# img = cv2.imread(r'C:\Users\caoti\Desktop\Lemon Images/190520-1.jpg')
# La siguiente instrucción reescala la imagen, usar si la imagen es muy grande
# img = cv2.resize(img, (0,0), fx = 0.5, fy = 0.5)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# Detección de bordes
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# Búsqueda de los contornos
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                       cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

(cnts, _) = contours.sort_contours(cnts)
ppm = width / r

# Loop para todos los contornos encontrados

for c in cnts:
    # Se establece un threshold para descartar contornos muy pequeños o ruido
    if cv2.contourArea(c) > 500:
        
        orig = img.copy()
        box = cv2.minAreaRect(c)
        print(type(box))
        box = cv2.boxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        # Se dibujan los puntos en el contorno para que aparezcan de arriba a abajo
        # y de izquierda a derecha después se dibuja la caja alredor del objeto
        box = perspective.order_points(box)
        # print(type(box))
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

        for (x, y) in box:
            #cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

            # print(x,y)

            (tl, tr, br, bl) = box
            (tltrX, tltrY) = midpoint(tl, tr)
            (blbrX, blbrY) = midpoint(bl, br)

            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)

            # Se dibujan los puntos medios en la imagen
            #cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
            #cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
            #cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
            #cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

            # 
            # Se dibujan lineas entre los puntos medios
            # cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 255, 255), 2)
            # cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (0, 0, 255), 2)
            
            # Calculo de la distancia euclideana entre los puntos medios
            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

            dimA = dA / ppm
            dimB = dB / ppm
            mean = (dimA + dimB) / 2

            print(dimA, dimB)

            # Se dibuja el tamaño de los objetos en la imagen
            cv2.putText(orig, "{:.1f}mm".format(dimA),
                (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                 0.65, (255, 255, 255), 2)
            cv2.putText(orig, "{:.1f}mm".format(dimB),
                (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                 0.65, (255, 255, 255), 2)
            cv2.putText(orig, "m_size = {:.1f}mm".format(mean),
                (int(tltrX - 50), int(tltrY - 50)), cv2.FONT_HERSHEY_SIMPLEX,
                 0.65, (255, 255, 0), 2)

            # Se muestra el resultado
            cv2.imshow("Imagen", orig)
            cv2.waitKey(0)
