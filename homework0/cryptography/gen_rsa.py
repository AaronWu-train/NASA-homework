from Crypto.Util.number import getPrime, inverse, long_to_bytes 

# Generate two 2048-bit prime numbers p and q
p = getPrime(2048)
q = getPrime(2048)
n = p * q

# Compute Euler's totient function φ(n) = (p-1) * (q-1)
phi_n = (p - 1) * (q - 1)

# Compute d = e^(-1) (mod φ(n))
e = 65537
d = inverse(e, phi_n)

with open("new_rsa_key_n.txt", "w") as file:
    file.write(str(n))
with open("new_rsa_key_d.txt", "w") as file:
    file.write(str(d))

# Should be 4096 bits, if not, re-run the code
print(f"n bit length: {n.bit_length()}") 