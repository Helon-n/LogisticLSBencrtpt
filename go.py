from logisticrgb import chaosrgb
import lsb
import getopt
import sys
import cv2



def main():

  opts, args = getopt.getopt(sys.argv[1:],'-h-m:-f:-k:-o:-v-c:',['help','mode=','filename=','key=','output=','version','code='])
  print(opts)
  key = ''
  output_file = ''
  mode = ''
  code = ''
  for opt_name,opt_value in opts:
    if opt_name in ('-h','--help'):
        print("[*] Help info")

        print("[*] python3 go.py -m encrypt -f file_path -k key -o output")

        print("[*] python3 go.py -m decrypt -f file_path -c code -o output")

        print("[*] key example r-g-b-init- ")

        print("[*] r,g,b [0~1]") 
        
        exit()

    if opt_name in ('-v','--version'):
        
        print("[*] Version is 0.01 ")        
        exit()

    if opt_name in ('-m','--mode'):
        
        mode = opt_value

    if opt_name in ('-f','--filename'):
        
        fileName = opt_value

    if opt_name in ('-k','--key'):

        key = opt_value

    if opt_name in ('-c','--code'):

        code = opt_value

    if opt_name in ('-o','--output'):

        output_file = opt_value



  if mode == 'encrypt':
    f = open("code","w")
    img = cv2.imread(fileName)
    img = chaosrgb(img,key)
    img2 , keys = lsb.encode_lsb(img,key)
    cv2.imwrite(output_file,img2)
    f.write(keys)

  if mode == 'decrypt':
    f=open(code,'r')
    img = cv2.imread(fileName)
    code = f.read()
    img = lsb.recov_lsb(img,code)
    key = lsb.decode_lsb(img)
    print(key)
    
    img = chaosrgb(img,key)
    cv2.imwrite(output_file,img)

  return
if __name__== '__main__':
  main()
