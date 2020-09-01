''' lemonator.py es un programa que toma una imagen de un limón y devuelve información relevante como el tamaño del diámetro
polar, ecuatorial y su media, su indice de color cítrico (CCI por sus siglas en inglés) y el porcentaje de defectos presentes
en la cáscara de la fruta.

Esta información se usa para evaluar si la fruta en cuestión es apta para el mercado de exportación o para el mercado nacional.
Cabe aclarar que la evaluación se hace de manera jerarquica, es decir, primero se evalúa el tamaño, después el CCI y, por ultimo
los defectos. Por lo tanto, si un limón no cumple con la especificación de tamaño NO SE REALIZARAN los demás calculos.

Para mayor información contactar a Angel Moisés Hernández Ponce a los correos amhrdz.1001@gmail.com o ahernandezp1800@alumno.ipn.mx
'''

### Estas librerias son las necesarias para ejecutar correctamente el programa
import numpy as np
import cv2 as cv
# from spaces import rgb2Hunter
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import imutils
import spaces
import math
import glob

### Las siguientes lineas son solamente scripts que hacen funciones específicas, no son el programa como tal
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def size_estimation(image):
	""" Regresa la estimación del diámetro polar y ecuatorial de un limón. La estimación se logra utilizando la
		relación pixel por metro en una imagen.
		imagen --> diametro polar, diamtero ecuatorial
		"""
	width = 200 ### Este valor se determina con base a la imagen y está dado en píxeles
	r = 38 # El valor real del objeto, expresado en milímetros

	# Pasar a escala de grises y suavizar la imagen
	gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
	gray = cv.GaussianBlur(gray, (7,7), 0)

	# Detección de bordes
	edged = cv.Canny(gray, 50, 100)
	edged = cv.dilate(edged, None, iterations = 1)
	edged = cv.erode(edged, None, iterations = 1)

	# Búsqueda de los contornos

	cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL,
		cv.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	(cnts, _) = contours.sort_contours(cnts)
	ppm = width / r

	for c in cnts:
    # Se establece un threshold para descartar contornos muy pequeños o ruido
	    if cv.contourArea(c) > 500:
	        
	        orig = image.copy()
	        box = cv.minAreaRect(c)
	        box = cv.boxPoints(box) if imutils.is_cv2() else cv.boxPoints(box)
	        box = np.array(box, dtype="int")

	        # Se dibujan los puntos en el contorno para que aparezcan de arriba a abajo
	        # y de izquierda a derecha después se dibuja la caja alredor del objeto
	        box = perspective.order_points(box)
	        # print(type(box))
	        cv.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

	        for (x, y) in box:
	            
	            (tl, tr, br, bl) = box
	            (tltrX, tltrY) = midpoint(tl, tr)
	            (blbrX, blbrY) = midpoint(bl, br)

	            (tlblX, tlblY) = midpoint(tl, bl)
	            (trbrX, trbrY) = midpoint(tr, br)

	                        
	            # Calculo de la distancia euclideana entre los puntos medios
	            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
	            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

	            dimA = dA / ppm
	            dimB = dB / ppm
	            mean = (dimA + dimB) / 2

	return(mean)

def rgb2Hunter(*args):
	"""Toma los pixles RGB de una imagen
	y devuelve los valores en XYZ """

	Xn = 95.0489
	Yn = 100
	Zn = 108.8840
	
	# Leemos la imagen
	# image = cv.imread(args)

	# Se cambian las dimensiones de la imagen
	# image.reshape(-1,3)

	# for i in image:
	for i in args:
		# if all(i) == False:
		if all(i) == False or i[0] > 100:
			Hl = 0
			Ha = 0
			Hb = 0		
		else:
			# Se normalizan los canales RGB 
			vr = (i[2]) / 255
			vg = (i[1]) / 255
			vb = (i[0]) / 255

			# Las siguientes comparaciones se hacen para obtener
			# los valores de Vr, Vg y Vb respectivamente

			if vr > 0.04045:
				vr = ((vr + 0.055) / 1.055)**2.4
			else:
				vr = vr / 12.92
			if vg > 0.04045:
				vg = ((vg + 0.055) / 1.055)**2.4
			else:
				vg = vg / 12.92
			if vb > 0.04045:
				vb = ((vb + 0.055) / 1.055)**2.4
			else:
				vb = vb / 12.92

			vr = vr * 100
			vg = vg * 100
			vb = vb * 100

			xyz = np.array([vr,vg,vb])
			# Matriz de constantes para hacer la conversión
			m = np.array([
				[0.4124, 0.3576, 0.1805],
				[0.2126, 0.7152, 0.0722],
				[0.0193, 0.1192, 0.9505]])

			res = np.matmul(m,xyz) # Multiplicación de matrices

			# Valores en el espacio de color XYZ
			X = res[0]
			Y = res[1]
			Z = res[2]

			### Coversión de XYZ a Hunter Lab con base al estandar Illuminant D65
			### Los valores están declarados al inicio

			varKa = 172.349
			varKb = 67.039

			Hl = 100 * (Y/Yn)**0.5
			Ha = varKa * (((X/Xn) - (Y/Yn)) / math.sqrt(Y/Yn))
			Hb = varKb * (((Y/Yn) - (Z/Zn)) / math.sqrt(Y/Yn))

	return(Hl,Ha,Hb)

def CCI(image):
	""" Regresa el valor medio del CCI (Citrus Color Index) de 
	la imagen de un limón 
	"""
	image = image.reshape(-1,3)
	image.tolist()

	sl = []

	for j in image:
		h = spaces.rgb2Hunter(j)

		if all(h) == False:
			pass
		else:
			cci = (1000*h[1]) / (h[0]*h[2]) # Cálculo del CCI. La formula es CCI = (1000*a)/(L*b)
			sl.append(cci) # Se guardan todos los valores obtenidos en una lista. De ella saldrá el valor promedio


	return(np.mean(sl))

def cont_defects(image):

	""" Regresa el porcentaje de defectos superficiales un limón. El parámetro que debe ingresar a la función
		es una imagen a escala de grises.
		imagen(blanco y negro) ---> porcentaje de defectos
		"""

	gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

	ret, thresh = cv.threshold(gray, 90, 190, cv.THRESH_BINARY)

	contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

	l1 = []
	l2 = []
	l3 = []
	el = []

	for c in contours:
		area = cv.contourArea(c)
		el.append(area)

		if area > 5000:
			x  = area
			cont = cv.drawContours(image, c, -1, (0,0,255), 1)
			l1.append(x)
		elif area > 100:
			xx = area
			l2.append(xx)
			cont = cv.drawContours(image, c, -1, (255,0,0), 1)
		else:
			xxx = area
			l3.append(xxx)
			cont = cv.drawContours(image, c, -1, (0,0,0), 1)

	v2 = sum(l2) + sum(l3)
	percentage = v2*100/max(el)

	return(percentage)

def color_defects(image):
	uT = -8.888 # Valor del umbral superior
	lT = -21.322 # Valor del umbral inferior

	image = image.reshape(-1,3)
	image.tolist()
	i_aux = image.tolist()

	sl = [] # Lista que servirá de apoyo

	### En este ciclo se calcula el CCI para cada tríada de píxeles de la imagen
	### Si todos los valores son cero no se ejecuta nada, si esta condición no se
	### cumplen entonces se ejecuta el código

	cont = 0

	for j in i_aux:
		h = rgb2Hunter(j)

		if all(h) == False:
			p = 0
		else:
			cci = (1000*h[1]) / (h[0]*h[2])
			sl.append(cci)
			if lT < cci < uT:
				cont += 1
	
	p = (cont*100)/len(sl)

	return(p)

### A partir de aquí comienza el programa pirncipal

for filename in glob.glob(r'*.png'):
	i = cv.imread(filename)

	size = size_estimation(i)

	if size >= 10:
		cci_val = CCI(i)

		if -21.322 < cci_val < -8.888:
			defectos = color_defects(i)

			if defectos < 50:
				state = "Pasa"
				print("Para la imagen: {} el resultado es {}". format(filename,state))
				print("Sus valores son --> Tamaño: % 5.2f, CCI: % 5.2f, Defectos: % 5.2f" % (size, cci_val, defectos))
			else:
				state = "No pasa"
				print("Para la imagen: {} el resultado es: {}".format(filename,state))
		else:
			state = "No pasa"
			print("Para la imagen: {} el resultado es: {}".format(filename,state))
	else:
		state = "No pasa"
		print("Para la imagen: {} el resultado es: {}".format(filename,state))

input("Presiona 'Enter' para terminar")
