import random


'''
Euclid's algorithm for determining the greatest common divisor
Use iteration to make it faster for larger integers
'''
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a




#Euclid's extended algorithm for finding the multiplicative inverse of two numbers
def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi




#returns True if a number is prime else False
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in xrange(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True




def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    #n = pq
    n = p * q

    #Phi is the totient of n
    phi = (p-1) * (q-1)

    #Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    #Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    #Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    
    #Return public and private keypair
    #Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))




def encrypt(pk, plaintext):
    #Unpack the key into it's components
    key, n = pk
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = (plaintext ** key) % n
    #Return the array of bytes
    return cipher




def decrypt(pk, ciphertext):
    #Unpack the key into its components
    key, n = pk
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = (ciphertext ** key) % n
    #Return the array of bytes as a string
    return plain
    


def tumb_protocol():
    print "***************************************************************"
    print "             Tumble Bit Transaction Protocol"
    print "***************************************************************"
    print "\n\nAssumptions::: "
    print "Alice = Customer"
    print "Bob = Merchant / seller"
    print "P.H = Payment Hub (a trustless 3rd party mediator)"
    print
    print "\n\n--------------- Generating (z,c) at P.H ------------------------"
    temp=random.randrange(1000, 1500)
    while(is_prime(temp) != True):
        temp = random.randrange(1, 50)
    p = temp #taking any random no
    q = 197 #taking any random no
    
    #Generating your public/private keypairs
    public, private = generate_keypair(p, q)
    print "P.H (RSA public key) = ", public ," P.H(RSA private key) = ", private

    epsilon = random.randrange(1, 50)
    sigma = random.randrange(1, 50)
    print "Sigma = ",sigma,"epsilon = ",epsilon
    z = decrypt(public, epsilon)
    c = sigma + epsilon




    print "\n\n\n"
    print "-------------- [P.H ---> Bob Communication]-------------------"
    print "P.H sending (z,c) = (",z,", ",c,") to Bob"


    print "Puzzle promise protocol exchange"
    for x in xrange(1,5):
        bf = random.randrange(1000, 5000)
        print "Blinding factor bf = ", bf," Hash = ",hash(bf)
    for x in xrange(1,5):
        temp = random.randrange(1000, 5000)
        print "Fake factors = ", temp




    print "\n\n\n"
    print "-------------- [Bob ---> Alice Communication]-------------------"
    print "Blinding the z before sending"
    bf = random.randrange(1, 10)
    print "Blinding factor bf = ", bf,"& send zStar = z*(bf^p.k)"

    e,n = public
    zStar = (z*decrypt(public, bf))%n
    print "Bob sending zStar Z* to Alice= ",zStar
    print "verify zStar=",decrypt(public, bf*epsilon)




    print "\n\n\n"
    print "--------------[Alice ---> P.H Communication]-------------------"
    print "Alice request solution of zStar (z*) to P.H for 1 coin"
    

    epsilonStar=encrypt(private, zStar)
    print "epsilonStar = ",epsilonStar
    x = random.randrange(1, 500)
    y = hash(x)
    q = epsilonStar + x



    print "Payment solver protocol exchange"
    for x in xrange(1,5):
        bff = random.randrange(1000, 5000)
        print "Blinding factors bf = ", bf
    for x in xrange(1,5):
        temp = random.randrange(1000, 5000)
        print "Fake factors = ", temp

    print "P.H sends (y,q) = (",y,q,") to Alice"



    print "\n\n\n"
    print "--------------[Alice ---> Bob Communication]-------------------"
    print "Alice sending epsilonStar to Bob"
    print "Bob calculating epsilon from epsilonStar"
    
    epsilonBob=epsilonStar / bf
    print "calculated epsilon at Bob = ",epsilonBob
    print "finding sigma from epsilon at Bob"
    
    sigmaBob = c - epsilonBob
    print "sigma at Bob = ",sigmaBob
    print "Bob sending sigma to get 1 coin"




#calling function for protocol
tumb_protocol()