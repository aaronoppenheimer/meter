from __future__ import division
import cv2
import numpy as np
import math

def main():
	image = cv2.imread('circles.jpg')
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# ret,bw_image = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)
	ret,bw_image = cv2.threshold(gray_image,75,255,cv2.THRESH_BINARY)
	# bw_image = cv2.adaptiveThreshold(gray_image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)

	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
	circles_dilated = cv2.dilate(bw_image, kernel, iterations = 10)

	im2, contours, hierarchy = cv2.findContours(circles_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	real_contours = [c for c in contours if cv2.contourArea(c) > 10000 and cv2.contourArea(c) < 100000]

	ext_points = []

	for c in real_contours:
		extLeft = tuple(c[c[:, :, 0].argmin()][0])
		extRight = tuple(c[c[:, :, 0].argmax()][0])
		extTop = tuple(c[c[:, :, 1].argmin()][0])
		extBot = tuple(c[c[:, :, 1].argmax()][0])
		ext_points.append([extLeft,extRight,extTop,extBot])

	ext_points.sort(key = lambda x: int(x[0][0]))


	centers = [
		(321,320),
		(873,329),
		(1419,344),
		(1950,366),
		(2469,372)
	]

	# now, for each contour and center, figure out which extreme point is furthest from the center
	angles = []
	for n in range(0,len(centers)):
		ep = ext_points[n]
		c = centers[n]

		d = [np.linalg.norm(np.asarray(a)-np.asarray(c)) for a in ep]
		i = d.index(max(d))

		arad = math.atan2(c[1]-ep[i][1], c[0]-ep[i][0])
		adeg = math.degrees(arad)
		angles.append(adeg - 90)

	angles = [a if a > 0 else a+360 for a in angles]

	dials = [
		0,
		10,
		0,
		10,
		0
	]

	vals=[]
	for i in range(0,len(angles)):
		val = (angles[i] / 360) * 10
		val = val if dials[i] == 0 else 10-val
		vals.append(str(int(val)))

	print "".join(vals)


if __name__ == "__main__":
	main()