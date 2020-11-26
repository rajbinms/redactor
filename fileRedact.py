import re
import crypt as cr
import sympy as sp

# Generate 2 random prime numbers
def randPrime():
    prime1 = sp.randprime(1000,10000)
    different_prime = True
    while different_prime:
        prime2 = sp.randprime(1000,10000)
        if prime1 != prime2:
            # smameprime = False
            return prime1,prime2

# Redaction of highlighted text form file
def redact(filename):
    file = open(filename,"r+")
    p1,p2 = randPrime() # Get two prime numbers
    pk,puk = cr.KeyGen(p1,p2) # Get private and public key
    text = []
    # Looping through lines in the file
    for l in file:
        encode = [] # store list of words to be redacted
        start_word_index =0
        word_start = True
        # Itterate through line 
        for i,c in enumerate(l):
            # Condition to store words between '#'
            if c =='#':
                if word_start: # store instance of #
                    start_word_index = i
                    word_start = False
                else: # second instance of #
                    word = l[start_word_index+1:i] #get word/s between #
                    encode.append(word) # add word to be redacted
                    start_word_index =0
                    word_start= True
        # Itterate through list of words that need to be redacted
        for e in encode:
            encr = cr.crypt(pk,e) # encrypt word
            encrstr = ' '.join([str(elem) for elem in encr]) # create a string of crypted numbers from list
            l = l.replace(e,encrstr) # replace word with encrypted string of numbers
        text.append(l) # add to output text line
    listToStr = ''.join([str(elem) for elem in text]) 
    file.close()
    # open file are replace text with now encrypted text
    file = open(filename,"w")
    file.writelines(listToStr)
    return puk



# Undo Redaction using key from file
def release(filename,key):
    file = open(filename,"r+")
    text = []
    # Looping through lines in the file
    for l in file:
        encode = [] # store list of crypt words to be deciphered
        start_word_index=0
        word_start = True
        # Itterate through line 
        for i,c in enumerate(l):
            # Condition to store words between '#'
            if c =='#': 
                if word_start: # store instance of #
                    start_word_index = i
                    word_start = False
                else: # second instance of #
                    word = l[start_word_index+1:i] #get crypt text/s between #
                    encode.append(word) # add word to be deciphered
                    start_word_index=0
                    word_start= True
        # Itterate through list of crypt words that need to be deciphered
        for e in encode:
            x = list(e.split(" ")) # Split word into list
            intlist = [int(i) for i in x] # convert to intefer list
            encr = cr.crypt(key,intlist,False) # decrypt list of crypted text
            l = l.replace(e,encr) # replace crypt word with decrypted word
        text.append(l)
    listToStr = ''.join([str(elem) for elem in text]) 
    file.close()
    # open new or existing file and replace text with now decrypted text
    newfile = "Unredacted_"+filename
    file = open(newfile,"w")
    file.writelines(listToStr)
    print("NewFIle: ",newfile)

# Structure key into 1 by 2 list
def set_key(key):
    key = key.split()
    keyint = []
    for i in key:
        keyint.append(int(i))
    return keyint