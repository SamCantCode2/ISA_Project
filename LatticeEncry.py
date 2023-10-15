import numpy as np
import PIL
import matplotlib.pyplot as plt
import time
import threading
import requests
import random
import Latticefile as lf


addr = r"" #Insert Image Here
apikey = '' #insert key here
base = 'http://api.openweathermap.org/data/2.5/weather?'
f = open('City_Names.csv', 'r')
cities = f.readlines()
cities = [i[0:-1:1] for i in cities]
pkey = random.randint(0, len(cities)-1) #Punlic Key
citykey = cities[pkey]
url = base + 'appid=' + apikey + '&q=' + citykey
response = requests.get(url)
vals = response.json()
n = int(2**np.abs(np.round((vals['main']['temp'] - 273.15)%10) + 4))
q = int(2**np.abs(np.round(vals['wind']['speed'] % 10) + 12))
t = int(2**np.abs(np.round((vals['main']['pressure'] % 10)) + 5))
print("Params", n, q, t)
pmod = [1] + [0] * (n-1) + [1]
pk, sk = lf.FHEEncryption.makekey(n, q, pmod)
img = PIL.Image.open(addr)
pixels = np.asarray(img)
sample = np.asarray(img, dtype = np.uint64)
ct = []
pt = []
print("Original Data:")
for i in range(10):
    print(sample[0][i])
    ct.append([lf.FHEEncryption.encrypt(pk, n, q, t, pmod, sample[0][i][0]), lf.FHEEncryption.encrypt(pk, n, q, t, pmod, sample[0][i][1]), lf.FHEEncryption.encrypt(pk, n, q, t, pmod, sample[0][i][2])])
    pt.append([lf.FHEEncryption.decrypt(sk, n, q, t, pmod, ct[i][0]), lf.FHEEncryption.decrypt(sk, n, q, t, pmod, ct[i][1]), lf.FHEEncryption.decrypt(sk, n, q, t, pmod, ct[i][2])])
print("Encrypted Data:", end = '\n\n')
for i in range(len(ct)):
    print("Pixel", i+1)
    print("Component 1:\n", ct[i][0], "Component 2:\n", ct[i][1], "Component 3:\n", ct[i][2], end = '\n\n')
print("Decrypted Data:")
for i in pt:
    print(i)
