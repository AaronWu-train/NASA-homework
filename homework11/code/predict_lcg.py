# predict_lcg.py
# used for problem 6.(a)

from pwn import remote

HOST = '140.112.91.4'
PORT = 1234

a = 10594026576823571650290222498858025152304387909825664795528079453461649287609526487105795664413997588814110924788498929126401917810915685684968717044468079
c = 7056014247531909712023296693630658223554290422190096692431189012363338779621916807655719448009311644475444286742221385004709604304643043647397873918849913
m = 0xa34d80e56c2cd0d35209cb13e5665fc58176fac6b1fee26af23388deebee59da1a884cbba6111ea819f7a2059f0accd8b1e7e23dbe4d90896b2cd482c0b934d97e3bbdbfd26b968e9bfeb2f8df037cab44557d2cf6eb57385a191c3db536c62f781e598405bdd818ae98dfd7df48c4da55d9d5b49d75aa46c91a27a186b9bf77

def next_state(x0):
    x1 = (a * x0 + c) % m
    return x1

r = remote(HOST, PORT)

# Get X_0 State
r.sendlineafter(b'choice: ', b'1')
r.sendlineafter(b'number: ', b'48763')
r.recvuntil(b'the number I picked is ')
d = r.recvuntil(b',')
x0 = int(d.strip().replace(b',', b''))

for i in range (100):
    print("process:", i)
    r.sendlineafter(b'choice: ', b'1')
    x0 = next_state(x0)
    r.sendlineafter(b'number: ', str(x0).encode('utf-8'))
    r.recvuntil(b'fan.')
    d = r.recvuntil(b',')
    print("number:", x0)

r.sendlineafter(b'choice: ', b'2')
print(r.recvuntil(b'choice: ').decode('utf-8'))
r.sendline(b'7')
r.close()

