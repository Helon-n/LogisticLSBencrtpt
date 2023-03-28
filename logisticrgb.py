import cv2
import numpy as np
def chaosrgb(img,key):
  r,g,b,init,n = key.split('-')
  r = float(r)
  g = float(g)
  b = float(b)
  init = float(init)
  Xlenth = img.shape[1]          # 图片列数
  Ylenth = img.shape[0]          # 图片行数
  z1 = r #init
  z2 = g
  z3 = b
  q = init #param
  #init 
  for i in range(200):
    z1 = q * z1 * (1-z1)
    z2 = q * z2 * (1-z2)
    z3 = q * z3 * (1-z3)
  for i in range(Ylenth):      
    for j in range(Xlenth):
        z1 = q * z1 * (1-z1)
        z2 = q * z2 * (1-z2)
        z3 = q * z3 * (1-z3)
        img[i][j][1] = img[i][j][1] ^ np.array((int(z1*255),),dtype=np.uint8)
        img[i][j][2] = img[i][j][2] ^ np.array((int(z2*255),),dtype=np.uint8)
        img[i][j][0] = img[i][j][0] ^ np.array((int(z3*255),),dtype=np.uint8)
  return img
