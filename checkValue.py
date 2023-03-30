import cv2
import skimage
from skimage.metrics import structural_similarity as ssim
import math
import numpy as np
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
  # plt.show()

  plt.subplot(234)
  plt.hist(R,bins=range(257),color='red')
  # plt.title('通道R')


  # plt.show()

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
# img  = cv2.imread("3.png")
# hist(img)
# img= cv2.imread("23.png")
# hist(img)

def NPCR(img1,img2):
      #opencv颜色通道顺序为BGR

  w,h,_=img1.shape

  #图像通道拆分
  B1,G1,R1=cv2.split(img1)
  B2,G2,R2=cv2.split(img2)
  #返回数组的排序后的唯一元素和每个元素重复的次数
  ar,num=np.unique((R1!=R2),return_counts=True)
  R_npcr=(num[0] if ar[0]==True else num[1])/(w*h)
  ar,num=np.unique((G1!=G2),return_counts=True)
  G_npcr=(num[0] if ar[0]==True else num[1])/(w*h)
  ar,num=np.unique((B1!=B2),return_counts=True)
  B_npcr=(num[0] if ar[0]==True else num[1])/(w*h)

  return R_npcr,G_npcr,B_npcr
def UACI(img1,img2):
  w,h,_=img1.shape
  #图像通道拆分
  B1,G1,R1=cv2.split(img1)
  B2,G2,R2=cv2.split(img2)
  #元素为uint8类型取值范围：0到255
  # print(R1.dtype)

  #强制转换元素类型，为了运算
  R1=R1.astype(np.int16)
  R2=R2.astype(np.int16)
  G1=G1.astype(np.int16)
  G2=G2.astype(np.int16)
  B1=B1.astype(np.int16)
  B2=B2.astype(np.int16)

  sumR=np.sum(abs(R1-R2))
  sumG=np.sum(abs(G1-G2))
  sumB=np.sum(abs(B1-B2))
  R_uaci=sumR/255/(w*h)
  G_uaci=sumG/255/(w*h)
  B_uaci=sumB/255/(w*h)

  return R_uaci,G_uaci,B_uaci


'''
计算图像的信息熵
'''
def entropy(img):
  # img=cv2.imread(img)
  w,h,_=img.shape
  B,G,R=cv2.split(img)
  gray,num1=np.unique(R,return_counts=True)
  gray,num2=np.unique(G,return_counts=True)
  gray,num3=np.unique(B,return_counts=True)
  R_entropy=0
  G_entropy=0
  B_entropy=0
  # print(len(gray))
  for i in range(len(gray)):
    p1=num1[i]/(w*h)
    p2=num2[i]/(w*h)
    p3=num3[i]/(w*h)
    R_entropy-=p1*(math.log(p1,2))
    G_entropy-=p2*(math.log(p2,2))
    B_entropy-=p3*(math.log(p3,2))
  return R_entropy,G_entropy,B_entropy

def RGB_correlation(channel,N):
      #计算channel通道
  h,w=channel.shape
  #随机产生pixels个[0,w-1)范围内的整数序列
  row=np.random.randint(0,h-1,N)
  col=np.random.randint(0,w-1,N)
  #绘制相邻像素相关性图,统计x,y坐标
  x=[]
  h_y=[]
  v_y=[]
  d_y=[]
  for i in range(N):
    #选择当前一个像素
    x.append(channel[row[i]][col[i]])
    #水平相邻像素是它的右侧也就是同行下一列的像素
    h_y.append(channel[row[i]][col[i]+1])
    #垂直相邻像素是它的下方也就是同列下一行的像素
    v_y.append(channel[row[i]+1][col[i]])
    #对角线相邻像素是它的右下即下一行下一列的那个像素
    d_y.append(channel[row[i]+1][col[i]+1])
  #三个方向的合到一起
  x=x*3
  y=h_y+v_y+d_y

  #结果展示
  # plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文乱码
  # plt.scatter(x,y)
  # plt.show()

  #计算E(x)，计算三个方向相关性时，x没有重新选择也可以更改
  ex=0
  for i in range(N):
    ex+=channel[row[i]][col[i]]
  ex=ex/N
  #计算D(x)
  dx=0
  for i in range(N):
    dx+=(channel[row[i]][col[i]]-ex)**2
  dx/=N

  #水平相邻像素h_y
  #计算E(y)
  h_ey=0
  for i in range(N):
    h_ey+=channel[row[i]][col[i]+1]
  h_ey/=N
  #计算D(y)
  h_dy=0
  for i in range(N):
    h_dy+=(channel[row[i]][col[i]+1]-h_ey)**2
  h_dy/=N
  #计算协方差
  h_cov=0
  for i in range(N):
    h_cov+=(channel[row[i]][col[i]]-ex)*(channel[row[i]][col[i]+1]-h_ey)
  h_cov/=N
  h_Rxy=h_cov/(np.sqrt(dx)*np.sqrt(h_dy))

  #垂直相邻像素v_y
  #计算E(y)
  v_ey=0
  for i in range(N):
    v_ey+=channel[row[i]+1][col[i]]
  v_ey/=N
  #计算D(y)
  v_dy=0
  for i in range(N):
    v_dy+=(channel[row[i]+1][col[i]]-v_ey)**2
  v_dy/=N
  #计算协方差
  v_cov=0
  for i in range(N):
    v_cov+=(channel[row[i]][col[i]]-ex)*(channel[row[i]+1][col[i]]-v_ey)
  v_cov/=N
  v_Rxy=v_cov/(np.sqrt(dx)*np.sqrt(v_dy))

  #计算E(y)
  d_ey=0
  for i in range(N):
    d_ey+=channel[row[i]+1][col[i]+1]
  d_ey/=N
  #计算D(y)
  d_dy=0
  for i in range(N):
    d_dy+=(channel[row[i]+1][col[i]+1]-d_ey)**2
  d_dy/=N
  #计算协方差
  d_cov=0
  for i in range(N):
    d_cov+=(channel[row[i]][col[i]]-ex)*(channel[row[i]+1][col[i]+1]-d_ey)
  d_cov/=N
  d_Rxy=d_cov/(np.sqrt(dx)*np.sqrt(d_dy))

  return h_Rxy,v_Rxy,d_Rxy,x,y
def correlation(img,N=3000):
      
  h,w,_=img.shape
  B,G,R=cv2.split(img)
  R_Rxy=RGB_correlation(R,N)
  G_Rxy=RGB_correlation(G,N)
  B_Rxy=RGB_correlation(B,N)

  #结果展示
  plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文乱码
  plt.subplot(221)
  plt.imshow(img[:,:,(2,1,0)])
  plt.title('原图像')
  #子图2
  plt.subplot(222)
  plt.scatter(R_Rxy[3],R_Rxy[4],s=1,c='red')
  plt.title('通道R')

  #子图3
  plt.subplot(223)
  plt.scatter(G_Rxy[3],G_Rxy[4],s=1,c='green')
  plt.title('通道G')
  #子图4
  plt.subplot(224)
  plt.scatter(B_Rxy[3],B_Rxy[4],s=1,c='blue')
  plt.title('通道B')
  plt.show()

  return R_Rxy[0:3],G_Rxy[0:3],B_Rxy[0:3]

'''

'''
# hist(p1)
def EQ(img1,img2):
  w,h,_=img1.shape
  B1,G1,R1=cv2.split(img1)
  B2,G2,R2=cv2.split(img2)
  R1_H={}
  R2_H={}
  G1_H={}
  G2_H={}
  B1_H={}
  B2_H={}
  R_EQ=0
  G_EQ=0
  B_EQ=0
  for i in range(256):
    R1_H[i]=0
    R2_H[i]=0
    G1_H[i]=0
    G2_H[i]=0
    B1_H[i]=0
    B2_H[i]=0

  for i in range(w):
    for j in range(h):
      R1_H[R1[i][j]]+=1;
      R2_H[R2[i][j]]+=1;
      G1_H[G1[i][j]]+=1;
      G2_H[G2[i][j]]+=1;
      B1_H[B1[i][j]]+=1;
      B2_H[B2[i][j]]+=1;

  for i in range(256):
    #公式里是平方，待考虑
    R_EQ+=abs(R1_H[i]-R2_H[i])
    G_EQ+=abs(G1_H[i]-G2_H[i])
    B_EQ+=abs(B1_H[i]-B2_H[i])
  # print(R_EQ)
  R_EQ/=256
  G_EQ/=256
  B_EQ/=256
  return R_EQ,G_EQ,B_EQ

def PSNR(img1,img2):
  w,h,_=img1.shape
  B1,G1,R1=cv2.split(img1)
  B2,G2,R2=cv2.split(img2)

  #强制转换元素类型，为了运算
  R1=R1.astype(np.int32)
  R2=R2.astype(np.int32)
  G1=G1.astype(np.int32)
  G2=G2.astype(np.int32)
  B1=B1.astype(np.int32)
  B2=B2.astype(np.int32)

  #计算均方误差,初始化64位无符号整型，防止累加中溢出
  R_mse=np.uint64(0)
  G_mse=np.uint64(0)
  B_mse=np.uint64(0)
  for i in range(w):
    for j in range(h):
      R_mse+=(R1[i][j]-R2[i][j])**2
      G_mse+=(G1[i][j]-G2[i][j])**2
      B_mse+=(B1[i][j]-B2[i][j])**2
  R_mse/=(w*h)
  G_mse/=(w*h)
  B_mse/=(w*h)
  R_psnr=10*math.log((255**2)/R_mse,10)
  G_psnr=10*math.log((255**2)/G_mse,10)
  B_psnr=10*math.log((255**2)/B_mse,10)

  return R_psnr,G_psnr,B_psnr