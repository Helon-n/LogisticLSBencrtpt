import cv2
import matplotlib.pyplot as plt
def hist(img):

  B,G,R=cv2.split(img)
  
  R=R.flatten(order='C')
  G=G.flatten(order='C')
  B=B.flatten(order='C')



  plt.rcParams['font.sans-serif'] = ['SimHei']  
  plt.subplot(232)

  plt.hist(img.flatten(order='C'),bins=range(257),color='gray')
  # plt.title('原图')

  plt.subplot(234)

  plt.hist(R,bins=range(257),color='red')
  # plt.title('通道R')



  plt.subplot(235)
  plt.hist(G,bins=range(257),color='green')
  # plt.title('通道G')
  # plt.show()
  # plt.axis('off')

  plt.subplot(236)
  plt.hist(B,bins=range(257),color='blue')
  # plt.title('通道B')
  # plt.axis('off')

  plt.tight_layout()
  plt.show()