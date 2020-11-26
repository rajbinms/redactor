from math import gcd
import random
import time

# Generating Private/Public Key Pair
def KeyGen(p,q):
    n = p*q
    phi_n = (p-1)*(q-1)
    e,d = get_ed(phi_n)
    public_key = [e,n]
    private_key = [d,n]
    return public_key,private_key

#  Get values of e and d for private and public keys
def get_ed(phi_n):
    not_prime = True
    # Random prime value for e
    while not_prime:
        e = random.randrange(1,phi_n)
        if (gcd(phi_n,e) == 1) :
            not_prime = False
    d = pow(e,-1,phi_n)
    #  check to see if e and d are equal
    if e==d:
        return get_ed(phi_n)
    else:
        return e,d


# Encrypt and decrypt text
def enc(pk, text):
    # t = time.process_time_ns() # start time of enc process
    key, n = pk
    cipher = [] # list of appended plain text or cypher text
    for i in text:
        intval = int(i)
        cipher.append(pow(intval,key,n))
    
    # o = time.process_time_ns() # end time of enc process
    # print("Time elapsed: ", o-t)
    return cipher

# method to get either plain text or cypher text and convert to list of integers or characters
def crypt(pk,text,encryptor = True):
    key, n = pk
    crypt_text =[]
    num_text =''
    # Default True takes input plain text and converts to list of integers
    if encryptor:
        for char in text:

            num_text +=str(ord(char)) # convert character to integer from ascii table and concat as string
            text_char = ord(char)
            f_text =''

            #  check if value is greated than n value from key 
            if text_char > n:
                text_char = str(ord(char))
                #  split character into two 
                if len(text_char) > 2:
                    crypt_text.append(int(text_char[0:2]))
                    crypt_text.append(int(text_char[2:]))
                else:
                    crypt_text.append(int(text_char[0:1]))
                    crypt_text.append(int(text_char[1:]))
            else:
                crypt_text.append(text_char)

        return enc(pk,crypt_text)
    else: 
        # False attribute takes input list of integers and converts to plain text
        f_text=''
        # get list of decrypted integers
        crypt_text = enc(pk,text)
        # print(crypt_text)
        temp_text =''
        #  convert list to characters based on Ascii table and concat as string
        for c in crypt_text:
            temp_text += str(c)
            if int(temp_text) >= 32:
                f_text += chr(int(temp_text))
                temp_text =''
        return f_text
