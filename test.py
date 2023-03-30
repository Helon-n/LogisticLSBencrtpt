import getopt
import sys
import checkValue
import cv2



def main():
    opts, args = getopt.getopt(sys.argv[1:],'-h-m:-x:-y:-n:',['help','mode=','file1=','file2=,number='])
    num = 0
    file1 ='test1.png'
    file2 = ''
    print(opts)
    for opt_name,opt_value in opts:
        if opt_name in ('-h','--help'):
            print("[*] -m UACI check UACI  ")
            exit()
        if opt_name in  ('-m','--mode'):
            mode = opt_value
        if opt_name in  ('-x','--file1'):
            print(file1)
            file1 = opt_value
        if opt_name in  ('-y','--file2'):
            file2 = opt_value
        
        if opt_name in  ('-n','--number'):
            num = opt_value
     

    if mode == 'UACI':
        
        img1 = cv2.imread(file1)
            
        img2 = cv2.imread(file2)
        
        print("RGB UACI : "+str(checkValue.UACI(img1,img2)))
            
    if mode == 'NPCR':
        
        img1 = cv2.imread(file1)
            
        img2 = cv2.imread(file2)
        
        print("NPCR:"+str(checkValue.NPCR(img1,img2)))
        
    if mode == 'hist':
        
        img1 = cv2.imread(file1)
        
        checkValue.hist(img1)
    
    if mode == 'correlation':
        # print(file1)
        img1 = cv2.imread(file1)
        # img2 = cv2.imread(file2)
        # print(type(num))
        checkValue.correlation(img1,int(num))
    if mode == 'entroy':
        img1 =cv2.imread(file1)
        print('entroy : '+str(checkValue.entropy(img1)))

    if mode == 'EQ':
        img1 = cv2.imread(file1)
            
        img2 = cv2.imread(file2)
        print('EQ: '+str(checkValue.EQ(img1,img2)))
    if mode == 'PSNR':
        img1 = cv2.imread(file1)
        img2 = cv2.imread(file2)

        print("PSNR : " +str(checkValue.PSNR(img1,img2)))


    return

if __name__== '__main__':
      main()
