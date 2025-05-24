#!/usr/bin/env python3

import sys, io, signal, select
from Crypto.Util.number import bytes_to_long
from secret import soyo_private_key, soyo_public_key

# Shamelessly copied from CNS 2024 HW1
def input_bytes(prompt: str) -> bytes:
    """
    Just for handling network I/O
    You can ignore me
    """
    print(prompt, end="")
    buf = io.BytesIO()
    b = sys.stdin.buffer.read1(4096)
    assert buf.write(b) == len(b)

    def stdin_ready():
        rlist, _, _ = select.select([sys.stdin.fileno()], [], [], 1)
        return rlist

    while stdin_ready():
        b = sys.stdin.buffer.read1(4096)
        assert buf.write(b) == len(b)

    return buf.getvalue()

def print_menu():
    print("==============================================================")
    print("Hello, I'm Soyo.")
    print("What do you want to do now?")
    print("1. View my RSA public key")
    print("2. Give me a message to sign using my RSA private key")
    print("3. Say goodbye")
    print("==============================================================")

def show_pubkey(e, n):
    print(f"Here is my public key (e, n): ({e}, {n})")

def sign_msg(d, n):
    msg = input_bytes('Please provide the message you\'d like me to sign:\n').strip(b"\n ")
    if msg.startswith(b"name="):
        print('I will not sign an ID for anyone. You must NEVER impersonate me!')
        return
    signature = pow(bytes_to_long(msg), d, n)
    print(f"Here is the signature: {signature}")

def alarm(second):
    def handler(signum, frame):
        print('Session Timeout! You need to be faster :(')
        exit()
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(second)

def main():
    sys.stdout = io.TextIOWrapper(open(sys.stdout.fileno(), 'wb', 0), write_through=True)
    e, d, n = soyo_public_key[1], soyo_private_key[1], soyo_private_key[0]
    alarm(200)
    while True:
        print_menu()
        try:
            cmd = int(input('> ').strip("\n "))
        except ValueError:
            print('Invalid input! Please try again.')
            continue

        match cmd:
            case 1:
                show_pubkey(e, n)
            case 2:
                sign_msg(d, n)
            case 3:
                break
            case _:
                print('Invalid input! Please try again.')
    print('Are you gonna tell a lie and hurt me? Just kidding. Bye!')

if __name__ == "__main__":
    main()
