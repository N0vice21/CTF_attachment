from flag import FLAG
from Crypto.Util.number import *
import gmpy2
import random

while True:
    p = int(gmpy2.next_prime(random.randint(10**399, 10**400-1)))
    q = int(str(p)[200:]+str(p)[:200])
    if gmpy2.is_prime(q):
        break

m = bytes_to_long(FLAG)
n = p*q
e = 65537
c = pow(m,e,n)

with open("enc","wb") as f:
    f.write(str(c))
    f.write("\n")
    f.write(str(n))