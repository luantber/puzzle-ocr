import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
from keras.models import load_model
model = load_model("mnist.h5")

def read_imgs(array_imgs):
    imgs = []
    for img in array_imgs:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convertir RGB to GRAY
        

        img_bin,th = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) #convertir imagen a binario
        

        # cv2.imshow("dilatado",th)

        #kernel = np.zeros((2,2), np.uint8)  ###
        #th = cv2.dilate(th, kernel, iterations=3) ### 
        

        img = cv2.addWeighted(th,0.9,gray,0.1,0) # fusionar img gray y bin para no perder calidad
        img = cv2.resize(img,(28,28),interpolation=cv2.INTER_AREA) #resize img a 28
        
        # img = cv2.resize( img[3:27 , 5:27] , (28,28) , interpolation=cv2.INTER_AREA )

        # img = cv2.dilate(img, kernel, iterations=1) 

        img = cv2.bitwise_not(img) #invertir colores #NEGATIVO
        

        # cv2.imshow('img',img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        imgs.append(img.reshape(28,28,1))
    return imgs



def reconocer(array_imgs):
    array_imgs = read_imgs(array_imgs)

    cv2.imshow( "m" , array_imgs[6] )
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    imgs = np.array(array_imgs)
    imgs = imgs.astype('float32')
    imgs /= 255

    


    resultado = model.predict_classes(imgs)

    


    return resultado # retorna array ejemplo [0 1 2 3 4 5 6 7 8]



