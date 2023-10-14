import numpy as np
from numpy.polynomial import polynomial as poly

class Polygen:
    def binarypoly(size):
        return np.random.randint(0, 2, size=size, dtype=np.int64)

    def uniformpoly(size, modulus):
        return np.random.randint(0, modulus, size=size, dtype=np.int64)

    def normalpoly(size):
        return np.int64(np.random.normal(0, 2, size=size))

    def mulwm(f, g, pmod): 
        '''should give polynomial f(x)/mod'''
        return poly.polydiv(poly.polymul(f, g), pmod)[1]

    def addwm(f, g, pmod): 
        '''should give polynomial f(x)/mod'''
        return poly.polydiv(poly.polyadd(f, g), pmod)[1]

class FHEencryption:
    def makekey(size, modulus, pmod):
        sk = Polygen.binarypoly(size)
        a = Polygen.uniformpoly(size, modulus)
        e1 = Polygen.normalpoly(size)
        b = poly.polyadd(poly.polymul(-a, sk, modulus, pmod), -e1, modulus, pmod) 
        return ((b, a), sk)

    def encrypt_data(pkey, size, q, t, pmod, data):
        mat = np.array([pt] + [0]*(size - 1), dtype = np.int64) % t
        delta = q // t
        matscale = (delta * mat) % q
        e1 = Polygen.normalpoly(size)
        e2 = Polygen.normalpoly(size)
        u = Polygen.binarypoly(size)
        ct0 = poly.polyadd(poly.polyadd(poly.polymul(pkey[0], u, q, pmod), e1, q, pmod), matscale, q, pmod)
        ct1 = poly.polyadd(poly.polymul(pk[1], u, q, pmod), e2, q, pmod)
        return (ct0, ct1)

    def decrypt_data(sk, size, q, t, pmod, ct):
        ptscale = poly.polyadd(poly.polynomial(ct[1], sk, q, pmod))
        decrypted = np.round(ptscale*t/q) % t
        return int(decrypted[0])
