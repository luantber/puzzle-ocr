import cv2
import numpy as np
from ocr.ocr import *
from astar import *

from collections import Counter 


capture = cv2.VideoCapture(2)

# define the list of boundaries
boundaries = [
	([17, 15, 100], [50, 56, 200]),
	([86, 31, 10], [225, 100, 60]),
	([25, 146, 190], [62, 174, 250]),
	([103, 86, 65], [145, 133, 128])
]


kernel = np.ones((3,3), np.uint8) 

def four_point_transform(image, pts,rect):

	(tl, tr, br, bl) = pts
 
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))

	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
 
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

	return warped

def paintCorners(image,corners):
	for i in corners:
		x = i[0]
		y = i[1]
		cv2.circle(image,(x,y),10,(0, 0, 255),2)    	

def sortCorners(corners):
	corners = [ i[0].tolist() for i in sorted(corners, key=cv2.contourArea, reverse=True)]
	corners = np.asarray(corners)	
	rect = np.zeros((4, 2), dtype = "float32")	
	s = corners.sum(axis = 1)
	
	rect[0] = corners[np.argmin(s)]
	rect[2] = corners[np.argmax(s)]		
	diff = np.diff(corners, axis = 1)	    
	rect[1] = corners[np.argmin(diff)]	    
	rect[3] = corners[np.argmax(diff)]
	return rect
	
def splitBoard(imageWraped):
	w=imageWraped.shape[0]
	h=imageWraped.shape[1]
	
	d_w = int(w/3)
	d_h = int(h/3)
	

	fig_1 = imageWraped[0:d_h,		0:d_w]
	fig_2 = imageWraped[0:d_h,		d_w:d_w*2]
	fig_3 = imageWraped[0:d_h,		d_w*2:w]
	fig_4 = imageWraped[d_h:d_h*2,	0:d_w]
	fig_5 = imageWraped[d_h:d_h*2,	d_w:d_w*2]
	fig_6 = imageWraped[d_h:d_h*2,	d_w*2:w]
	fig_7 = imageWraped[h-d_h:h,	0:d_w]
	fig_8 = imageWraped[h-d_h:h,	d_w:d_w*2]
	fig_9 = imageWraped[h-d_h:h,	d_w*2:w]
	
	return [fig_1,fig_2,fig_3,fig_4,fig_5,fig_6,fig_7,fig_8,fig_9]
	

def most_frequent(List): 
	occurence_count = Counter(List) 
	return occurence_count.most_common(1)[0][0]

def checkIsCorrect(array):
	array=array.sort()

	for i in range(0,9):
		print(i,array[i])
		if array[i]!=i:
			return False
	
	return True	

	
def compare(A,B):
	for i in range(len(A)):
		if A[i] != B[i]:
			print( A[i] ,B[i])
			return False
	return True
			

	


count_tolerance = 0
threshold_tolerance = 1

cells_buffer = [[],[],[],[],[],[],[],[],[]]

best_numbers = [0,0,0,0,0,0,0,0,0]
temp_best = [0,0,0,0,0,0,0,0,0]

while(True):
     
    ret, image = capture.read()
    lower,upper=boundaries[1]
    
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    
    #cv2.imshow("mask", mask)
    #cv2.imshow("bitwise_and", output)

    
    
    output = cv2.cvtColor(output, cv2.COLOR_HSV2BGR)
    #cv2.imshow("hsv",output )
    gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY)   
    bi = cv2.bilateralFilter(mask, 5, 75, 75)


    img_dilation = cv2.dilate(bi, kernel, iterations=15) 
    #cv2.imshow("dilatation",img_dilation )
    img_erosion = cv2.erode(img_dilation, kernel, iterations=15) 
    #cv2.imshow("erosion", img_erosion )
    
    wrapedImage = image
    
    

    try:
	    corners = cv2.goodFeaturesToTrack(img_erosion,50,0.3,10)
	    corners = np.float32(corners)

	    if len(corners) == 4:
	    	corners=sortCorners(corners)
	    	
	    	wrapedImage=four_point_transform(image,corners,corners)
	    	pieces = splitBoard(wrapedImage)	    		    	

	    	numbers=reconocer(pieces)
	    	"""
	    	if count_tolerance < threshold_tolerance :
	    		for it2 in range(0,9):

	    			cells_buffer[it2].append(numbers[it2])


	    		count_tolerance+=1

	    	else:
	    		for it3 in range(0,9):
	    			best_numbers[it3]=most_frequent(cells_buffer[it3])
	    		cells_buffer = [[],[],[],[],[],[],[],[],[]]
	    		count_tolerance = 0
	    	"""
	    	# print(numbers,"probably wrong")
	    	if len(numbers) == len(set(numbers)):
				
	    		if not compare(temp_best,numbers) :
	    			print("cambio : ")
	    			temp_best = numbers
	    			inputAstar = ''.join([str(elem) for elem in numbers]) 
	    			print(inputAstar)
	    			resultado = astar(inputAstar)
	    			print("res ",resultado)
	    			if resultado == []:
	    				print("No hay solución")
	    			else :
	    				print("resultado")
	    				print(resultado[0])

	    			
	    	
	    	
	    	paintCorners(image,corners)
	    	cv2.imshow("wraperd", wrapedImage)

	    	
	    cv2.imshow("images", image)
    except:
        cv2.imshow("images", image)
    
    

    if cv2.waitKey(1) == 27:
    	break

 
capture.release()
cv2.destroyAllWindows()
