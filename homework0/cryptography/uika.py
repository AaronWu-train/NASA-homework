#!/usr/bin/env python3

import sys, io, signal
from Crypto.Util.number import bytes_to_long
from secret import MISSION

def get_public_key():
    print("Hi, I'm Misumi Uika, and I have a SECRET mission for you.")
    print("To prevent any eavesdropping on this message about the SECRET mission, I'll ensure its confidentiality using RSA encryption.")

    e = 65537
    l = 2048
    print(f"First and foremost, please generate an RSA key pair consisting of a public key (n, e) and a private key (n, d) such that e={e}, n has {2*l} bits, and e*d=1 (mod (p-1)*(q-1)), where n is the product of two {l}-bit prime numbers p and q. Once generated, provide me with your public key (n, e).")
    print("Note: d is the private exponent, e is the public exponent, and n is the modulus.")

    try:
        n = int(input('n: ').strip("\n "))
        e2 = int(input('e: ').strip("\n "))
    except ValueError:
        print("\nInvalid input")
        exit()

    if e!=e2:
        print(f"\nInvalid public exponent e (which should be {e})")
        exit()

    if n.bit_length() != 2*l:
        print(f"\nInvalid modulus n")
        exit()

    return n, e

def send_mission(n, e):
    msg = bytes_to_long(MISSION.encode())
    if msg >= n:
        print("\nThe modulus n is not large enough!")
        exit()
    c = pow(msg, e, n)
    print("Great! Now I'll tell you the SECRET mission, which is encrypted using the RSA public key you just gave me. You may then uncover it using your private key.")
    print(f"Here is the encrypted message: {c}")

def alarm(second):
    def handler(signum, frame):
        print('\nSession Timeout! You need to be faster :(')
        exit()
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(second)

def main():
    sys.stdout = io.TextIOWrapper(open(sys.stdout.fileno(), 'wb', 0), write_through=True)
    alarm(200)

    n, e = get_public_key()
    send_mission(n, e)

if __name__ == "__main__":
    main()
