import numpy as np
import PIL
import matplotlib.pyplot as plt
import time
import threading
import requests
import random

def invertible(mat):
    try:
        inv = np.linalg.inv(mat)
    except:
        return 0
    return 1

def threadfunction(pixarray, key):
    for i in range(len(pixarray)):
        for j in range(len(pixarray[i])):
            pixarray[i][j] = np.matmul(pixarray[i][j], key)

'''
Uses openweather API to gather weather information
The random function gives a pseudo random value to index the city that the weather is taken from
The randomness in the variables comes from the weather of the place itself
'''
apikey = '7f356d5a6b31cd357f0976956b2e9297'
base = 'http://api.openweathermap.org/data/2.5/weather?'
f = open('City_Names.csv', 'r')
cities = f.readlines()
cities = [i[0:-1:1] for i in cities]
pkey = random.randint(0, len(cities)-1) #Public Key
citykey = cities[pkey]
url = base + 'appid=' + apikey + '&q=' + citykey
response = requests.get(url)
vals = response.json()
matkey = [[int(vals['coord']['lon']), int(vals['coord']['lat']) , int(vals['weather'][0]['id'])],
          [int(vals['main']['temp']), int(vals['main']['temp_max']), int(vals['main']['temp_min'])],
          [int(vals['wind']['deg']), int(vals['sys']['id']), vals['cod']]]
matkey = np.array(matkey)
while not invertible(matkey):
    pkey = random.randint(0, len(cities)-1) #Public Key
    citykey = cities[pkey]
    url = base + 'appid=' + apikey + '&q=' + citykey
    response = requests.get(url)
    vals = response.json()
    matkey = [[int(vals['coord']['lon']), int(vals['coord']['lat']) , int(vals['weather'][0]['id'])],
            [int(vals['main']['temp']), int(vals['main']['temp_max']), int(vals['main']['temp_min'])],
            [int(vals['wind']['deg']), int(vals['sys']['id']), vals['cod']]]
invkey = np.linalg.inv(matkey) #Private Key
print("The public key (city index) is:", pkey, end='\n')
print("The city of choice is:", vals['name'])
print("The matrix key is:\n", matkey, end='\n')
print("The secret key (matrix inverse) is:\n", invkey, end='\n')
addr = r"C:\Users\Samhruth\Pictures\Saved Pictures\ForEncry.jpeg" #Insert Image Here
img = PIL.Image.open(addr)
pixels = np.asarray(img)
sample = np.asarray(img, dtype = np.uint32)
print("Sample pixel before encryption:", sample[0][0])
t1 = threading.Thread(target = threadfunction, args = (pixels, matkey))
t2 = threading.Thread(target = threadfunction, args = (sample, matkey))
t3 = threading.Thread(target = threadfunction, args = (sample, invkey))
start = time.time()
t1.start()
t2.start()
t1.join()
t2.join()
end = time.time()
print("Encryption Time:", end - start)
res = PIL.Image.fromarray(pixels)
res.save(r"C:\Users\Samhruth\Pictures\Saved Pictures\Encrypted.jpeg")
start = time.time()
t3.start()
t3.join()
end = time.time()
sample = np.asarray(sample, dtype = np.uint8)
print("Decryption Time:", end - start)
print("Sample pixel post encryption:", sample[0][0])
res = PIL.Image.fromarray(sample)
res.save(r"C:\Users\Samhruth\Pictures\Saved Pictures\Decrypted.jpeg")