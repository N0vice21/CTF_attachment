from Crypto.Cipher import AES
import os
flag='flag{********************************}'
BLOCKSIZE = 16



def pad(data):
        pad_len = BLOCKSIZE - (len(data) % BLOCKSIZE) if  len(data) % BLOCKSIZE != 0 else 0
        return data + "=" * pad_len

def unpad(data):
        return data.replace("=","")


def enc(data,key,iv):
	cipher = AES.new(key,AES.MODE_CBC,iv)
	encrypt = cipher.encrypt(pad(data))
	return encrypt


def dec(data,key,iv):
	try:
		cipher = AES.new(key,AES.MODE_CBC,iv)
		encrypt = cipher.decrypt(data)
		return unpad(encrypt)
	except:
		exit()


def task():
        try:
                key = os.urandom(16)
                iv = os.urandom(16)
                pre = "yusa"*4
                for _ in range(3):
                        choice = raw_input(menu)
                        if choice == '1':
                                name = raw_input("What's your name?")
                                if name == 'admin':
                                        exit()
                                token = enc(pre+name,key,iv)
                                print "Here is your token(in hex): "+iv.encode('hex')+token.encode('hex')
                                continue
                        elif choice == '2':
                                token = raw_input("Your token(in hex): ").decode('hex')
                                iv = token[:16]
                                name = dec(token[16:],key,iv)
                                print iv.encode('hex')+name.encode('hex')
                                if name[:16] == "yusa"*4:
                                        print "Hello, "+name[16:]
                                        if name[16:] == 'admin':
                                                print flag
                                                exit()
                        else:
                                continue
        except:
                exit()
menu='''
1. register
2. login
3. exit
'''
if __name__ == "__main__":
        task()
