
import hashlib
from Crypto import Random
import random
from Crypto.PublicKey import RSA
import base64
##for tumbler##################
def generate_keys():
	# RSA modulus length must be a multiple of 256 and >= 1024
	modulus_length = 256*4 # use larger value in production
	key = RSA.generate(modulus_length, Random.new().read)
	publickey = key.publickey()
	# publickey = key.publickey().exportKey()
	# privatekey = key.exportKey()
	return key, publickey
# def gcdExtended(int a, int b, int *x, int *y):
#     if (a == 0): 
#     	*x = 0, *y = 1; 
# 		return b; 
    
  
#     int x1, y1; // To store results of recursive call 
#     int gcd = gcdExtended(b%a, a, &x1, &y1); 
  
#     // Update x and y using results of recursive 
#     // call 
#     *x = y1 - (b/a) * x1; 
#     *y = x1; 
  
#     return gcd; 
# } 

# def modInverse(a, m) : 
#     a = a % m; 
#     for x in range(1, m) : 
#         if ((a * x) % m == 1) : 
#             return x 
#     return 1

def modInverse(a, m) : 
    m0 = m 
    y = 0
    x = 1
  
    if (m == 1) : 
        return 0
  
    while (a > 1) : 
  
        # q is quotient 
        q = a // m 
  
        t = m 
  
        # m is remainder now, process 
        # same as Euclid's algo 
        m = a % m 
        a = t 
        t = y 
  
        # Update x and y 
        y = x - q * y 
        x = t 
  
  
    # Make x positive 
    if (x < 0) : 
        x = x + m0 
  
    return x 
  


def modDivide(a, b, m):
    a = a % m
    inv = modInverse(b, m)
    if (inv == -1) :
       print("Division not defined")
    else:
       print("Result of division is ",)
       ans = ((inv%m * a%m) % m)
       return ans


sk,pk=generate_keys()
print(sk.d)
print("************************************")
print(sk.n)
print("************************************")
print(sk.e)
print("************************************")

y=1051##puzzle y for alice


##m=1 and n=1
r=random.randint(1,5000)
print ("r_v="),
#print(r)
r_v=(y*(r**sk.e))%sk.n
print(r_v)
f=r
while(f==r):
	f=random.randint(1,5000)

pk=sk.publickey()
#x=pk.encrypt(str(f),32)
f_v=(int(f)**sk.e)%sk.n
print("f_v="+str(f_v))

value=[]##fake +real values , beta values
value.append(r_v)
value.append(f_v)

print("************************************")
#print(int(x)==f_v)
##Alice ends

##4-tumbler ...................

s_list=[]
print("s list is")
for i in range(2):#m=1,n=1
	#x=(f_v**sk.d)%sk.n
	x=pow(value[i],sk.d,sk.n)
	print(type(x))
	s_list.append(x)
	print(s_list[i])
	print("************************************************************************")

k_list=[]
print("K list is")
for i in range(2):
	k_list.append(random.randint(1,1000))
	print(k_list[i])

print("************************************************************************")
hashed_k=[]
hashed_knew=[]
#print("\nhashed_k\n")
for i in range(2):
	# print(hashlib.shake_256(str(k_list[i]).encode("utf-8")).hexdigest(length=8))
	# hashed_k.append( hashlib.shake_256(str(k_list[i]).encode("utf-8")).hexdigest(length=8))
	# print(type(hashed_k[i]))

	# print(hashlib.shake_256((k_list[i])).digest(length=8))


	#hash(k_list[i])
	hashed_knew.append(hash(k_list[i]))
#print("************************************************************************")		
print("hashed k values are :\n")
for i in range(len(k_list)):
	print(hashed_knew[i])
print("************************************************************************")		
print("c list is:")
c_list=[]
for i in range(len(k_list)):
	print(hashed_knew[i]^s_list[i])
	c_list.append(hashed_knew[i]^s_list[i])



# 6 check fake values 
if(f_v==pow(f,sk.e,sk.n)):
	print("checked fake value, all are correct")

# send k values for fake  i.e. index=2
#sent k_list[1]

# 7 step 
#for all fake values
if(hashed_knew[1]==k_list[1]):
	print("hashed k verified")
	s_new=hashed_knew[1]^c_list[1]
	if(s_new==f%sk.n):
		print(s_new)
		print(f%sk.n)
		print("s_new verified")

# 9 step check real values
#y and real values are sent to tumbler
if(value[0]==((y*(r**sk.e))%sk.n)):
	print("real vlaues are verified")

# step 10 
#real k are sent in Transaction

#step 11
# alice will obtained those k from transaction

s_j = hashed_knew[0]^c_list[0]
if(pow(s_j,sk.e,sk.n)==value[0]):
	print(pow(s_j,sk.e,sk.n))
	print(value[0])
	print("s_j verified")



# def modDivide(a, b, m) 
# { 
#     a = a % m; 
#     inv = modInverse(b, m); 
#     if (inv == -1) 
#        cout << "Division not defined"; 
#     else
#        cout << "Result of division is " << (inv * a) % m; 
# }


x = modDivide(s_j, value[0], sk.n)

comp = pow(y,sk.d,sk.n)

print("*****")
