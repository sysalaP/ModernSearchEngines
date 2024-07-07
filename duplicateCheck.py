import hashlib
from nltk.corpus import stopwords

#Create a hash for text thats similar for similar texts
def computeHash(words):
     hash_length = 16
     fingerprint = [0] * hash_length
     for word in words:
          #Hash the word and convert it to binary
          hash = bin(int(hashlib.md5(word.encode('utf-8')).hexdigest(), 16)).replace('0b', '').zfill(128)
          #Read bits and convert to list of integer
          bits = [int(d) for d in hash]

          #Turn 0s to -1     
          l = [-1 if x==0 else x for x in bits]

          #Per column addition
          for i in range(hash_length):
               fingerprint[i] += l[i]
            
     #Map back to binary
     fingerprint = [1 if x>0 else 0 for x in fingerprint]
     return fingerprint

#Check a single document Footprint/hash (docHash) against an existing collection of previsouly seen documents hashes (docsHashes) for near duplicates
def check_simhash(docHash, docsHashes):
     threshold = 7
     hash = docHash
     for h in docsHashes:
          diff = 0
          for i in range(len(h)):
               diff += abs(hash[i] - h[i])
          #print(diff)     
          if(diff < threshold):
               return True
     return False