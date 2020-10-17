import hashlib
from pwn import *


def loop(fuck):
    for a in guess_all:
        for b in guess_all:
            for c in guess_all:
                guess = a + b + c
                result = hashlib.sha256(guess).hexdigest()
                if fuck == result:
                    print hexdump(guess)
                    return guess



r = remote("106.53.114.216", 9999, level="debug")
r.recvuntil("=========Pow========\n")
hash_value = r.recvuntil("\"\n", drop=True).split("== \"")[1]
length = int(r.recvuntil("\n", drop=True).split("== ")[1])
r.recvuntil(">")
guess_all = list(chr(x) for x in range(0x0, 0x100))
guess = loop(hash_value)
r.sendline(guess)
r.interactive()
