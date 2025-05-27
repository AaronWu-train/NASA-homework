from pwn import remote
import hashlib

HOST = '140.112.91.4'
PORT1 = 11451
PORT2 = 11452


def main():
    soyo = remote(HOST, PORT2)
    id = (b'name=soyo')
    zero_id = b'\x00' + id

    soyo.sendlineafter(b'> ', b'2')
    soyo.sendlineafter(b'sign:\n', zero_id)
    soyo.recvuntil(b'signature:')
    signature = soyo.recvline()
    print("signature:\n", signature.decode())
    soyo.sendlineafter(b'> ', b'3')
    soyo.close()

    anon = remote(HOST, PORT1)
    anon.sendlineafter(b'ID: ', id)
    anon.sendlineafter(b'Signature: ', signature)
    anon.interactive()
    anon.close()

if __name__ == "__main__":
    main()
