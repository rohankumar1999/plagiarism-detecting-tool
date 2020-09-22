#=========================================================================================================================
#             PLAGIARISM CHECKING TOOL USING LSH TO REDUCE DIMENSIONALITY OF DATA
#=========================================================================================================================
from __future__ import division
import os
import re
import random
import time
import binascii
from bisect import bisect_right
from heapq import heappop, heappush

a=os.listdir("C:\\Users\\karth\\Desktop\\ir2")    #path to the document corpus is given here
k_gram=3                      #shingle length can be adjusted here
#=========================================================================================================================
#                           SHINGLING
#=========================================================================================================================
def shingles(string):
  return set(string[head:head+k_gram] for head in range(0,len(string)-k_gram))
shingles_list=list()
all_shingles_set=set();
for file in a:
  f=open(os.path.join("C:\\Users\\karth\\Desktop\\ir2",file),'r')
  content=f.read()
  shingles_list.append(shingles(content))
# print(shingles_list)
for i in range(len(shingles_list)):
  for j in shingles_list[i]:
    all_shingles_set.add(j)
# print(all_shingles_set)
all_shingles_list=list(all_shingles_set)
#=========================================================================================================================
#                           DOCUMENT MATRIX
#=========================================================================================================================

matrix=[[0 for i in range(len(a))]for j in range(len(all_shingles_list))]
for i in range(len(all_shingles_list)):
  for j in range(len(a)):
    if all_shingles_list[i] in shingles_list[j]:
      matrix[i][j]=1
#=========================================================================================================================
#                           MIN-HASHING
#=========================================================================================================================
hashes_count=20
t0=time.time()
maxShingleID=2**32-1
nextprime= 4294967311
def pickRandomCoeffs(k):          #function to create 'k' random numbers,thereby creating random hash-functions
  # Create a list of 'k' random values.
  randList = []
  
  while k > 0:
    # Get a random shingle ID.
    randIndex = random.randint(0, maxShingleID) 
  
    # Ensure that each random number is unique.
    while randIndex in randList:
      randIndex = random.randint(0, maxShingleID) 
    
    # Add the random number to the list.
    randList.append(randIndex)
    k = k - 1
    
  return randList
coeffA = pickRandomCoeffs(hashes_count)
coeffB = pickRandomCoeffs(hashes_count)
k_index=pickRandomCoeffs(len(all_shingles_list))

signature=[[0 for i in range(len(a))]for j in range(hashes_count)]
for i in range(hashes_count):           #computing minimum value for each hash function
  for j in range(len(a)):
    minval=2**32-1
    for k in range(len(all_shingles_list)):
      if matrix[k][j]==1:
        if minval>(((coeffA[i])*k+(coeffB[i]))%nextprime):
          minval=(((coeffA[i])*k+(coeffB[i]))%nextprime)
    signature[i][j]=minval
print('\n','signature matrix: ','\n')
for i in range(len(signature)):
  print(signature[i])
bands=10
rows=2

#=========================================================================================================================
#                     LOCALITY SENSITIVE  HASHING
#=========================================================================================================================
hash_table_list=list()
for i in range(bands):          #hashing documents into respective buckets
  hash_table=dict()
  for j in range(len(a)):
    tup=list()
    for k in range(rows):
      tup.append(signature[i*rows+k][j])
    if hash(tuple(tup)) in hash_table:
      hash_table[hash(tuple(tup))].append(j)
    else:
      hash_table[hash(tuple(tup))]=[j]
  hash_table_list.append(hash_table)
print('\n','buckets are: ','\n')
for i in range(len(hash_table_list)):
  print(hash_table_list[i])

doc_id=0          #you can also take input for the document you wish to compute the candidate pairs for
similar_docs=set()
for i in range(len(hash_table_list)):
  for list in hash_table_list[i].values():
    if doc_id in list:
      for j in list :
        if j!=doc_id:
          similar_docs.add(j)
print('\n','similar documents are: ',similar_docs)