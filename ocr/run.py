from ocr import *


img1 = cv2.imread("ocr/imgs/1.png")
# img2 = cv2.imread("imgs/2.png")
# img3 = cv2.imread("imgs/3.png")
# img4 = cv2.imread("imgs/4.png")
# img5 = cv2.imread("imgs/5.png")
# img6 = cv2.imread("imgs/6.png")
# img7 = cv2.imread("imgs/7.png")
# img8 = cv2.imread("imgs/8.png")
# img0 = cv2.imread("imgs/0.png")

print(reconocer([img1]))
