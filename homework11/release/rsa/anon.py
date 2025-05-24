#!/usr/bin/env python3

import sys, io, signal
from Crypto.Util.number import getStrongPrime, bytes_to_long, GCD
from secret import soyo_public_key # Anon should never know Soyo's private key!
from secret import FLAG1, FLAG2

def rsa_key_gen():
    e = 7
    while 48763:
        p, q = getStrongPrime(2048), getStrongPrime(2048)
        n = p * q
        phi = (p - 1) * (q - 1)
        if GCD(e, phi)==1 and p!=q:
            break
    return e, n

def login():
    print("Hello, I'm Anon (not Ann). Sorry... I only talk to Soyo now.")
    print("It seems that I don't know who you are, show me your ID in the format \"name=<your_name>\" and give me its signature signed by your RSA private key.")
    ID = input('ID: ').strip("\n ")
    signature = input('Signature: ').strip("\n ")

    if not ID.startswith("name="):
        print('Invalid ID!')
        exit()

    name = ID.split('=', maxsplit=1)[1]
    if name != 'soyo':
        print('Who are you? You are not Soyo >:(')
        exit()

    try:
        signature = int(signature)
    except ValueError:
        print("Signature should be an integer.")
        exit()

    # check the validity of the signature
    n, e = soyo_public_key
    if (pow(signature, e, n)-bytes_to_long(ID.encode()))%n != 0:
        print('Hey Soyorin! Welco... Wait a minute, you are NOT Soyo! The signature is invalid! Don\'t try to fool me >:(')
        exit()

    print("I'm sure you are Soyorin since your signature matches the ID :D")
    print(f"Here is the flag just for you, Soyorin: {FLAG1}")

def print_menu():
    print("========================================================================")
    print("What do you want to do now?")
    print("1. View my RSA public key")
    print("2. View my VERY SECRET diary encrypted using my RSA public key")
    print("3. Exit")
    print("========================================================================")

def show_pubkey(e, n):
    print(f"Here is my public key (e, n): ({e}, {n})")

def show_secret(e, n):
    c = pow(bytes_to_long(FLAG2.encode()), e, n)
    print(f"Alright, I'll give you my encrypted SECRET diary, but I'll never reveal the private key, so there's no way you can uncover the diary! haha >:D\nHere is the encrypted diary c: {c}")

def alarm(second):
    def handler(signum, frame):
        print('Session Timeout! You need to be faster :(')
        exit()
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(second)

def main():
    sys.stdout = io.TextIOWrapper(open(sys.stdout.fileno(), 'wb', 0), write_through=True)
    alarm(100)
    login()
    alarm(0)

    print('Hold on, let me generate my RSA key.')
    e, n = rsa_key_gen()

    alarm(200)
    while True:
        print_menu()
        try:
            cmd = int(input('> ').strip("\n "))
        except:
            print('Invalid input! Please try again.')
            continue

        match cmd:
            case 1:
                show_pubkey(e, n)
            case 2:
                show_secret(e, n)
            case 3:
                break
            case _:
                print('Invalid input! Please try again.')

    print('Bye!')

if __name__ == "__main__":
    main()
