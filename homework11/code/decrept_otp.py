from binascii import hexlify, unhexlify
import re

FLAG_PATTERN = re.compile(r"NASA_HW11\{[0-9A-Za-z_':/@]+\}")
ENCRYPTED = b"665e0de370f8f1ec9e4f484502cb78eec4e58b470a7902eb74b0f6e18d494b4343d572e5c2e5c3121c1725ea70ed8aceb8796b682bd120bbcbb0ce5a755c50ff4ee7c5b5ce7548043cb226d5dcb3cd1f1d6857b34ee680eecf751e023cf67dbe81eece1952001e"

def OTPDecrypt(msg: bytes, key: bytes, shift: int) -> bytes:
    key_len = 10
    dec = bytes(msg[i] ^ key[(i + shift)% key_len] for i in range(len(msg)))
    return dec 

def decrypt_key(enc: bytes, pos: int) -> bytes:
    flg = b"NASA_HW11{"
    key = bytes(enc[(i + pos)%len(enc)] ^ flg[i] for i in range(10))
    return key

def main():
    enc: bytes = unhexlify(ENCRYPTED)

    for i in range(0, len(enc) - 10):
        try:
            key = decrypt_key(enc, i)
            msg = OTPDecrypt(enc, key, 10 - (i%10)).decode()
            if (bool(FLAG_PATTERN.search(msg))):
                print(msg)

        except Exception as e:
            print("error in shift:", i)
            print(e)

if __name__ == '__main__':
    main()



