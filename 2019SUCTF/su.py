a='J2261C63-3I2I-EGE4-IBCC-IE41A5I5F4HB'
flag = "flag{"
for i in a:
    if i>='0' and i<='9':
        flag += chr(ord(i)+48)
    elif i>='A' and i<='J':
        flag += chr(ord(i)-17)
    else:
        flag +=i
print (flag,end='')
print("}")