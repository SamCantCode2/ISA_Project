import numpy as np
import PIL
import random
import matplotlib.pyplot as plt
import time
import threading

def invertible(mat):
    #Checks if matrix is invertible
    try:
        inv = np.linalg.inv(mat)
    except:
        return 0
    return 1

def threadfunction(pixarray, key):
    '''Used to encrypt pixels by isolating into a thread
    Args:
        pixarray: Array of pixels
        key: Matrix Key used for encryption'''
    for i in range(len(pixarray)):
        for j in range(len(pixarray[i])):
            pixarray[i][j] = np.matmul(pixarray[i][j], key)

addr = r"" #Insert Image Here
matkey = [[random.randint(0, 1000) for i in range(3)] for i in range(3)]
while(not invertible(matkey)):
    matkey = [[random.randint(0, 1000) for i in range(3)] for i in range(3)]
matkey = np.matrix(np.array(matkey))
invkey = np.linalg.inv(matkey)
#Matrix is checked for invertibility

print("The matrix key is:\n", matkey, end='\n')
print("The matrix inverse is:\n", invkey, end='\n')

img = PIL.Image.open(addr)
pixels = np.asarray(img)
sample = np.asarray(img, dtype = np.uint32)
print(sample[0][0])
#Turns image into pixel array

'''
Threads are created to make sure the encryption can happen simultaneously
Each thread is used for one purpose
t1 allows for the demonstration of the image and the transfer of the image as noise but works only in 8 bits
t2 does the actual 32 bit encryption to allow for the matrices to exist without hash values and a change in the vector
t3 decrypts the 32 bit pixel array
'''
t1 = threading.Thread(target = threadfunction, args = (pixels, matkey))
t2 = threading.Thread(target = threadfunction, args = (sample, matkey))
t3 = threading.Thread(target = threadfunction, args = (sample, invkey))
start = time.time() #Measuring time
t1.start() #Start of encryptions
t2.start()
t1.join()
t2.join()
end = time.time()
print("Encryption Time:", end - start)

'''Here res allows the image to be demonstrated under the 8 bit constraint'''
res = PIL.Image.fromarray(pixels)
res.save(r"C:\Users\Samhruth\Pictures\Saved Pictures\Encrypted.jpeg")
start = time.time()
t3.start() #Start of decryption
t3.join()
end = time.time()
sample = np.asarray(sample, dtype = np.uint8)
print("Decryption Time:", end - start)

print(sample[0][0])
res = PIL.Image.fromarray(sample)
res.save(r"C:\Users\Samhruth\Pictures\Saved Pictures\Decrypted.jpeg") #Saving the resultant image
