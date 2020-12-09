from Crypto.Cipher import AES
import os
BLOCKSIZE = 16
flag='flag{********************************}'


def pad(data):
        pad_len = BLOCKSIZE - (len(data) % BLOCKSIZE) if  len(data) % BLOCKSIZE != 0 else 0
        return data + chr(pad_len) * pad_len

def unpad(data):
        num = ord(data[-1])
        return data[:-num]


def enc(data,key):
	cipher = AES.new(key,AES.MODE_ECB)
	encrypt = cipher.encrypt(pad(data))
	return encrypt


def dec(data,key):
	try:
		cipher = AES.new(key,AES.MODE_ECB)
		encrypt = cipher.decrypt(data)
		return unpad(encrypt)
	except:
		exit()


def task():
        try:
                key = os.urandom(16)
                while True:
                        plaintext = raw_input("Amazing function: ").decode('hex')
                        yusa = plaintext+flag
                        print enc(yusa,key).encode('hex')
        except Exception as e:
                print str(e)
                exit()
if __name__ == "__main__":
        task()
