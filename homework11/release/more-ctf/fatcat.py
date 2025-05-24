#!/usr/bin/env python3
# Reference: 2021 & 2023 NTU CSIE NASA HW5

from binascii import hexlify
import random
import hashlib
from timeit import timeit
import secrets
from utils import alarm
from secret import lcg_param, FLAG1, FLAG2, FLAG3, FLAG4, club_shared_key

class SuperRandomNumberGenerator:
    def __init__(self):
        self.state = int.from_bytes(secrets.token_bytes(64), 'little')
        self.a = lcg_param['a']
        self.c = lcg_param['c']
        self.m = 0xa34d80e56c2cd0d35209cb13e5665fc58176fac6b1fee26af23388deebee59da1a884cbba6111ea819f7a2059f0accd8b1e7e23dbe4d90896b2cd482c0b934d97e3bbdbfd26b968e9bfeb2f8df037cab44557d2cf6eb57385a191c3db536c62f781e598405bdd818ae98dfd7df48c4da55d9d5b49d75aa46c91a27a186b9bf77

        for _ in range(69):
            self.get_random()

    def get_random(self):
        self.state = (self.state * self.a + self.c) % self.m
        return self.state

def menu(trust):
    print()
    print("------------------------------------------------------")
    print("| What's up? I'm Fatcat. Only my 麻吉 get to have my |")
    print("| flag! BTW, do you want to play a game wiwh me?     |")
    print(f"| [Current trust level: {trust}]                           |")
    print("| [Choices]:                                         |")
    print("| 1. Play a game                                     |")
    print("| 2. Ask for the flag                                |")
    print("| 3. Ask him about the exam result                   |")
    print("| 4. Help his 麻吉 do some work                      |")
    print("| 5. Ask him to verify your club membership          |")
    print("| 6. Ask him to prove his club membership            |")
    print("| 7. Leave                                           |")
    print("------------------------------------------------------")
    print()

def game(rng, trust):
    print("Great! Let's play a simple number-guessing game.")
    print("I am going to randomly pick a number without revealing it to you, and then you guess it.")
    print("You win iff the number you guessed is equal to my number modulo 500.")
    print("You'd better be a White Album 2 enjoyer, 'cause only they would know what number I’d choose!")

    number = rng.get_random()
    try:
        your_number = int(input("Guess a number: ").strip())
    except ValueError:
        print("Are you serious?")
        return trust-1

    if (number-your_number)%500 == 0:
        print("Congratulations!! I guess you must be a White Album 2 fan.")
        return trust+1
    else:
        print(f"Nice try, but the number I picked is {number}, which is not the same as yours modulo 500.")
        return trust

def OTPEncrypt(msg: bytes) -> bytes:
    key_len = 10
    key = secrets.token_bytes(key_len)
    enc = bytes(msg[i] ^ key[i % key_len] for i in range(len(msg)))
    return enc

def send_exam_result():
    print("My score on the exam?")
    print("Oh, uh... yeah. I got 35. That's what I got. Definitely 35.")
    print("What? You want to check my answer sheet because you think I'm lying?")
    print("Fine. Here you go. This is my answer sheet... ENCRYPTED by a one-time pad!!!")

    encrypted_flag = hexlify(OTPEncrypt(FLAG2.encode())).decode()
    print(encrypted_flag)

    print("You'll never get to check my actual score, fools!")


def proof_of_work():
    r = random.randint(0, 2**24 - 1)
    h = hashlib.md5(str(r).encode()).hexdigest()[0:8]
    i = input(f'Give me `i` such that md5(i)[0:8] == "{h}" : ').strip()
    if hashlib.md5(str(i).encode()).hexdigest()[0:8] != h:
        print('Wrong')
        exit()

def do_many_PoW():
    n = 10
    rate = n / timeit(proof_of_work, number=n)
    rate_str = str(rate)
    print(f'Wow! You can solve {rate_str} PoWs per second!')
    if rate > 150:
        print(f'Thanks for helping out with the work! Please accept this flag as thanks: {FLAG3}')

def verifier():
    nonce = str(random.randint(0, 2**32-1))
    print(f'nonce: {nonce}')

    response = input('Please give me "your_name||SHA256(nonce||shared_key)": ').strip()
    try:
        v = response.split('||')
        name = v[0]
        mac = v[1]
    except IndexError:
        print("\nInvalid\n")
        exit()

    if name == 'fatcat':
        print("You can't be me! You IMPOSTOR!")
        exit()

    if hashlib.sha256(f'{nonce}||{club_shared_key}'.encode()).hexdigest() != mac:
        print('You are not a member!')
        exit()

def prover():
    try:
        nonce = int(input('Please give me a nonce: ').strip())
    except ValueError:
        print("\nInvalid\n")
        exit()

    name = 'fatcat'
    mac = hashlib.sha256(f'{nonce}||{club_shared_key}'.encode()).hexdigest()
    response = f'{name}||{mac}'
    print(f'Proof: {response}')

def main():
    alarm(200)
    trust = 0
    rng = SuperRandomNumberGenerator()
    while True:
        menu(trust)
        try:
            choice = int(input("Your choice: ").strip())
        except ValueError:
            print("\nInvalid Input\n")
            continue

        match choice:
            case 1:
                trust = game(rng, trust)

            case 2:
                if trust < 100:
                    print("Who are you??? I won't give you my flag unless you're my 麻吉!")
                    continue
                print(f"You must be a 麻吉 of mine! Here is the flag for you: {FLAG1}")

            case 3:
                send_exam_result()

            case 4:
                do_many_PoW()

            case 5:
                print("Let me verify if you're a member first.")
                verifier()
                print(f'Wow, you play MapleStory too! Here is your flag: {FLAG4}')

            case 6:
                print("You don't believe I'm a member? Fine, I'll prove it.")
                prover()

            case 7:
                break
    print("Bye!")


if __name__ == '__main__':
    main()
