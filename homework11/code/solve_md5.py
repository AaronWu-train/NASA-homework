from pwn import remote
import hashlib

HOST = '140.112.91.4'
PORT = 1234

def create_md5_table():
    table = {}
    for i in range(0, 2**24-1):
        hash = hashlib.md5(str(i).encode()).hexdigest()[:8].encode()
        table[hash] = str(i).encode()
    return table

def main():
    md5_table = create_md5_table()

    # Connect to the remote service
    r = remote(HOST, PORT)
    r.sendlineafter(b'choice: ', b'4')

    for i in range(10):
        r.recvuntil(b'== "') 
        hash = r.recv(8)
        r.recv(4)
        r.sendline(md5_table[hash])

    r.interactive()
    r.close()

if __name__ == "__main__":
    main()
