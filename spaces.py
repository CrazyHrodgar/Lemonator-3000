import numpy as np
import math
# import cv2 as cv

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
		if all(i) == False:
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