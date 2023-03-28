
import cv2

def encode_lsb(img, message):
    n=0
    binary_message = ''.join(format(ord(i), '08b') for i in message)
    # print(len(binary_message))
    if len(binary_message) > img.shape[0] * img.shape[1] * 3:
        raise ValueError("Message too large to encode in image")
    binary_message += '0' * (img.shape[0] * img.shape[1] * 3 - len(binary_message))
    binary_message_index = 0
    binary_lsb =''
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                binary_pixel = format(img[i][j][k], '08b')
                # print(binary_pixel[7])
                binary_lsb = binary_lsb + binary_pixel[7]
                new_binary_pixel = binary_pixel[:-1] + binary_message[binary_message_index]
                binary_message_index += 1
                img[i][j][k] = int(new_binary_pixel, 2)
                n = n+1
                if binary_message_index >= len(binary_message):
                    # print(n)
                    return img, binary_lsb
    
    return img

def decode_lsb(img):

    binary_message = ''
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                binary_pixel = format(img[i][j][k], '08b')
                binary_message += binary_pixel[-1]
    message = ''
    for i in range(0, len(binary_message), 8):
        message += chr(int(binary_message[i:i+8], 2))
    return message
def recov_lsb(img,message):
    
    msg_index = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                binary_pixel = format(img[i][j][k], '08b')
                new_binary_pixel = binary_pixel[:-1] + message[msg_index]
                msg_index=msg_index+1
                img[i][j][k] = int(new_binary_pixel, 2)
    return img
