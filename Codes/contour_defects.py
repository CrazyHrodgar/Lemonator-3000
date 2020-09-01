import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os

# os.chdir(r'C:\Users\caoti\Desktop\Lemon Images\Processed\miniset')
os.chdir(r'C:\Users\caoti\Desktop\Lemon Images\Processed')

# img = cv.imread('im226.png')
img = cv.imread(r'C:\Users\caoti\Desktop\Lemon Images\Groundtruth\manually segmented/si9.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	# cielab = cv.cvtColor(img, cv.COLOR_BGR2Lab)
	# ret, thresh = cv.threshold(gray, 90, 190, cv.THRESH_BINARY)
ret, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)


contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

el = []
a1 = []

for c in contours:
	area = cv.contourArea(c)
	el.append(area)
	# cont = cv.drawContours(img, c, -1, (0,0,0), 1)

	# if area < 25000:
	# 	el.append(area)
	# 	cont = cv.drawContours(img, c, -1, (255, 0, 0), 1)

	# 	if area < 100:
	# 		cont = cv.drawContours(img, c, -1, (0,0,255), 1)
	# 		a1.append(area)
	# 	elif area < 5000:
	# 		cont = cv.drawContours(img, c, -1, (255,255,0), 1)
	# 		print(area)
	# 	else:
	# 		cont = cv.drawContours(img, c, -1, (0,0,255), 1)

	if area > 5000:
			# print('Area total:', area)
		cont = cv.drawContours(img, c, -1, (0,0,255), 1)
	elif area > 100:
		cont = cv.drawContours(img, c, -1, (255,0,0), 1)
			# print('Area = ', area)
	else:
			# print('Area = ', area)
		cont = cv.drawContours(img, c, -1, (0,255,255), 1)

print(len(el))
print(len(a1))
print(max(el))
cv.imshow('Contornos', img)
	# cv.imwrite('defectos_none.png',cont)

cv.imshow('thresh', thresh)

cv.waitKey(0)
cv.destroyAllWindows()

