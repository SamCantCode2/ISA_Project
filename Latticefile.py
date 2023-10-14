import numpy as np
from numpy.polynomial import polynomial as poly

class Polygen:
    def binarypoly(size):
        """Generates a polynomial with coeffecients in [0, 1]
        Args:
            size: number of coeffcients, size-1 being the degree of the
                polynomial.
        Returns:
            array of coefficients with the coeff[i] being 
            the coeff of x ^ i.
        """
        return np.random.randint(0, 2, size, dtype=np.int64)


    def uniformpoly(size, modulus):
        """Generates a polynomial with coeffecients being integers in Z_modulus
        Args:
            size: number of coeffcients, size-1 being the degree of the
                polynomial.
        Returns:
            array of coefficients with the coeff[i] being 
            the coeff of x ^ i.
        """
        return np.random.randint(0, modulus, size, dtype=np.int64)


    def normalpoly(size):
        """Generates a polynomial with coeffecients in a normal distribution
        of mean 0 and a standard deviation of 2, then discretize it.
        Args:
            size: number of coeffcients, size-1 being the degree of the
                polynomial.
        Returns:
            array of coefficients with the coeff[i] being 
            the coeff of x ^ i.
        """
        return np.int64(np.random.normal(0, 2, size=size))


    # Functions for polynomial evaluation in Z_q[X]/(X^N + 1)

    def polymul(x, y, modulus, pmod):
        """Multiply two polynoms
        Args:
            x, y: two polynoms to be multiplied.
            modulus: coefficient modulus.
            poly_mod: polynomial modulus.
        Returns:
            A polynomial in Z_modulus[X]/(poly_mod).
        """
        return np.int64(np.round(poly.polydiv(poly.polymul(x, y) % modulus, pmod)[1] % modulus))


    def polyadd(x, y, modulus, pmod):
        """Add two polynoms
        Args:
            x, y: two polynoms to be added.
            modulus: coefficient modulus.
            poly_mod: polynomial modulus.
        Returns:
            A polynomial in Z_modulus[X]/(poly_mod).
        """
        return np.int64(np.round(poly.polydiv(poly.polyadd(x, y) % modulus, pmod)[1] % modulus))

class FHEEncryption:
    def makekey(size, modulus, pmod):
        """Generate a public and secret keys
        Args:
            size: size of the polynoms for the public and secret keys.
            modulus: coefficient modulus.
            poly_mod: polynomial modulus.
        Returns:
            Public and secret key.
        """
        s = Polygen.binarypoly(size)
        a = Polygen.uniformpoly(size, modulus)
        e = Polygen.normalpoly(size)
        b = Polygen.polyadd(Polygen.polymul(-a, s, modulus, pmod), -e, modulus, pmod)
        return (b, a), s


    def encrypt(pk, size, q, t, pmod, pt):
        """Encrypt an integer.
        Args:
            pk: public-key.
            size: size of polynomials.
            q: ciphertext modulus.
            t: plaintext modulus.
            poly_mod: polynomial modulus.
            pt: integer to be encrypted.
        Returns:
            Tuple representing a ciphertext.      
        """
        # encode the integer into a plaintext polynomial
        m = np.array([pt] + ([0] * (size - 1))) % t
        delta = q // t
        scaled_m = delta * m
        e1 = Polygen.normalpoly(size)
        e2 = Polygen.normalpoly(size)
        u = Polygen.binarypoly(size)
        ct0 = Polygen.polyadd(Polygen.polyadd(Polygen.polymul(pk[0], u, q, pmod), e1, q, pmod), scaled_m, q, pmod)
        ct1 = Polygen.polyadd(Polygen.polymul(pk[1], u, q, pmod), e2, q, pmod)
        return (ct0, ct1)


    def decrypt(sk, size, q, t, poly_mod, ct):
        """Decrypt a ciphertext
        Args:
            sk: secret-key.
            size: size of polynomials.
            q: ciphertext modulus.
            t: plaintext modulus.
            poly_mod: polynomial modulus.
            ct: ciphertext.
        Returns:
            Integer representing the plaintext.
        """
        scaled_pt = Polygen.polyadd(Polygen.polymul(ct[1], sk, q, poly_mod), ct[0], q, poly_mod)
        delta = q // t
        decrypted_poly = np.round(scaled_pt / delta) % t
        return int(decrypted_poly[0])


class CryptOps:
    def add_plain(ct, pt, q, t, poly_mod):
        """Add a ciphertext and a plaintext.
        Args:
            ct: ciphertext.
            pt: integer to add.
            q: ciphertext modulus.
            t: plaintext modulus.
            poly_mod: polynomial modulus.
        Returns:
            Tuple representing a ciphertext.
        """
        size = len(poly_mod) - 1
        # encode the integer into a plaintext polynomial
        m = np.array([pt] + [0] * (size - 1), dtype=np.int64) % t
        delta = q // t
        scaled_m = delta * m
        new_ct0 = Polygen.polyadd(ct[0], scaled_m, q, poly_mod)
        return (new_ct0, ct[1])


    def add_cipher(ct1, ct2, q, poly_mod):
        """Add a ciphertext and a ciphertext.
        Args:
            ct1, ct2: ciphertexts.
            q: ciphertext modulus.
            poly_mod: polynomial modulus.
        Returns:
            Tuple representing a ciphertext.
        """
        new_ct0 = Polygen.polyadd(ct1[0], ct2[0], q, poly_mod)
        new_ct1 = Polygen.polyadd(ct1[1], ct2[1], q, poly_mod)
        return (new_ct0, new_ct1)


    def mul_plain(ct, pt, q, t, poly_mod):
        """Multiply a ciphertext and a plaintext.
        Args:
            ct: ciphertext.
            pt: integer to multiply.
            q: ciphertext modulus.
            t: plaintext modulus.
            poly_mod: polynomial modulus.
        Returns:
            Tuple representing a ciphertext.
        """
        size = len(poly_mod) - 1
        # encode the integer into a plaintext polynomial
        m = np.array([pt] + [0] * (size - 1), dtype=np.int64) % t
        new_c0 = Polygen.polymul(ct[0], m, q, poly_mod)
        new_c1 = Polygen.polymul(ct[1], m, q, poly_mod)
        return (new_c0, new_c1)