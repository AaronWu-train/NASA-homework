from Crypto.Util.number import long_to_bytes

with open("rsa_key_n.txt", "r") as file:
    n = int(file.read())
with open("rsa_key_d.txt", "r") as file:
    d = int(file.read())
with open("message.txt", "r") as file:
    message = int(file.read())
e = 65537

# Perform RSA decryption: plaintext = (ciphertext^d) mod n
plaintext_int = pow(message, d, n)

# Convert decrypted integer to readable text
plaintext = long_to_bytes(plaintext_int).decode(errors="ignore")

print(plaintext)
