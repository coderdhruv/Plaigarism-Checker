import os
import numpy as np
import random
import math
import pandas as pd


def intersection(lst1, lst2):
    return set(lst1).intersection(lst2)

def union(lst1, lst2):
    final_list = lst1 + lst2
    return final_list


#file1 = open(r"C:\Users\medet\Desktop\Year3Sem1\Information retrieval\ir1.txt", "r")
#yourpath = r"C:\Users\medet\Desktop\ir_files"
#
#
## for filename in os.listdir(os.getcwd()):
#d = {}
#shingle = {}
#len_doc = 0
#for files in os.listdir(yourpath):
#    #print(files)
#    with open(yourpath+'\\'+files, "r") as fileobj:
#        sh = []
#        for x in fileobj:
#            for i in range(0, len(x)-9):
#                sh.append(x[i:i+9:1])
#                if not x[i:i+9:1] in shingle:
#                    shingle[x[i:i+9:1]] = [len_doc]
#                    #global_shingle.append(x[i:i+9:1])
#                else:
#                    shingle[x[i:i+9:1]].append(len_doc)
#        # print(sh)
#        d[len_doc] = sh
#        len_doc = len_doc + 1
#        # print(len_doc)
    

df = pd.read_csv('news_summary.csv', sep=',', encoding='latin-1')
d = {}
shingle = {}
len_doc = 0

for x in range(0, 20):
    string = df['ctext'][x]
    sh = []
    for i in range(0, len(string)-9):
        sh.append(string[i:i+9:1])
        if not string[i:i+9:1] in shingle:
            shingle[string[i:i+9:1]] = [len_doc]
            #global_shingle.append(x[i:i+9:1])
        else:
            shingle[string[i:i+9:1]].append(len_doc)
    d[len_doc] = sh
    len_doc += 1
#print(d[5])
print(len_doc)

for key,value in shingle.items():
    list1 = set(value)
    shingle[key] = list(list1)


# making the list obtained as value from 9-shingle key unique
for key, value in shingle.items():
    list1 = set(value)
    shingle[key] = list(list1)

# printing modified shingle dictionary
# print("printing modified shingle dictionary")
# for key, value in shingle.items():
    # print(key)
    # print(value)


# doing random tests for correctness(to be deleted later)
# print(d[1])
# print(shingle["nment wil"])
# print(len(shingle))
# print(finalArray)
shin_hash = {}
h = 0
for i in shingle:
    shin_hash[h] = i
    h = h + 1


# building the input matrix
finalArray = np.zeros(shape=(len(shingle), len_doc))
e = 0
for key, value in shingle.items():
    # print(value)
    for i in value:
        finalArray[e][i] = 1
    e = e + 1

# print(finalArray[450:560])

# building the signature matrix using hash functions

# print("printing mul and add lists")
# initializing signature matrix and filling with infinity values
sig_mat = np.zeros(shape = (100, len_doc))
for i in range(0,100):
    for j in range(0,len_doc):
        sig_mat[i][j] = 9999999

print(type(sig_mat))
# building list that will be used for multiplication with x in hash function ax + b i.e. a
mul_list = set(random.sample(range(0, 1000), 100))
while(len(mul_list)<100):
    mul_list.append(random.sample(range(0, 1000), 1)[0])
mul_list = list(mul_list)
print(mul_list)

# building list that will be used for addition in h(x) in hash function ax + b i.e. b
add_list = set(random.sample(range(0, 1000), 100))
while(len(add_list)<100):
    add_list.append(random.sample(range(0, 1000), 1)[0])
add_list = list(add_list)
print(add_list)

# building 100 hash functions
print("printing signature matrix")
r2 = 0
for i in range(0, len(mul_list)):
    for k in range(0,len(shingle)):
        h = (int)(mul_list[i]*(k+1) + add_list[i])%(len(shingle))
        for l in range(0,len_doc):
            if finalArray[k][l] == 1:
                if sig_mat[r2][l] > h:
                    sig_mat[r2][l] = h
    r2 = r2 + 1
# print(sig_mat)

def cal_jaccard_score(sigmat,d1,d2):
    intersec = 0
    uni = 0
    for i in range(0,len(sigmat)):
        if sigmat[i][d1] == sigmat[i][d2]:
            intersec += 1
    uni = len(sigmat)
    return intersec/uni

def cal_cosine_score(sig_mat,d1,d2):
    mult = 0;
    mod_doc1 = 0;
    mod_doc2 = 0;
    for k in range(0, len(sig_mat)):
        mult = mult + sig_mat[k][d1] * sig_mat[k][d2]
        mod_doc1 = mod_doc1 + sig_mat[k][d1] * sig_mat[k][d1]
        mod_doc2 = mod_doc2 + sig_mat[k][d2] * sig_mat[k][d2]
    cosine_sim = mult / (math.sqrt(mod_doc1) * math.sqrt(mod_doc2))
    return cosine_sim




"""def hash_signature(sig_mat, b, r):
    dictionary = list()  # a list  to store hashed buckets
    buckets = {}    # a dictionary to store hashes of one band of size r rows
    print("entering hashSig", b, r)
    startIndex = 0
    bands_done = 0
    for k in range(0, b): # iterating through each bands
        for i in range(0, len(sig_mat.T)):  # iterating through each column given by transpose of sig_mat
            toCompress = ''     # string to be compressed
            for j in range(startIndex, r + startIndex):
                print(j)
                toCompress += (str(int(sig_mat[j][i])))
            print("toCompress is ", toCompress)
            print(toCompress)
            bytesObject = bytes(toCompress.encode('latin-1'))
            c = Compressor()
            c.use_zlib()
            c.compress(toCompress, zlib_level=3)
            print(toCompress)
        startIndex += r
        # bands_done += 1

# hash_signature(sig_mat, 15, 5)
"""
dictionary = list()  # a list  to store hashed buckets
def hash_signature2(sig_mat, b, r):
    print("entering hashSig", b, r)
    startIndex = 0
    for k in range(0, b): # iterating through each bands
        buckets = {}  # a dictionary to store hashes of one band of size r rows
        for i in range(0, len_doc):  # iterating through each column given by transpose of sig_mat
            toCompress = ''     # string to be compressed
            for j in range(startIndex, r + startIndex):
                #print(j)
                toCompress += (str(int(sig_mat[j][i])))
            if toCompress not in buckets:
                buckets[str(toCompress)] = [i]
            else:
                buckets[str(toCompress)].append(i)
        startIndex += r
        # bands_done += 1
        dictionary.append(buckets)
    print("printing list of hashtables")
    e = 0;
    for i in dictionary:
        print("bucket",e)
        for key, hash in i.items():
            print(key,hash)
        e += 1

# hash_signature(sig_mat, 15, 5)5

def cal_jacc_score_candidate_pairs(threshold):
    final_can_pairs = {}
    for i in dictionary:
        for key,hash in i.items():
            if len(hash) > 1:
                #print("yes",hash)
                for j in range(0,len(hash)):
                    for k in range(j+1,len(hash)):
                        if cal_jaccard_score(sig_mat,hash[j],hash[k]) > threshold:
                            if (hash[j],hash[k]) not in final_can_pairs :
                                final_can_pairs[(hash[j],hash[k])] = cal_jaccard_score(sig_mat,hash[j],hash[k])
                                #print(cal_jaccard_score(sig_mat,hash[j],hash[k]))
    return final_can_pairs

def cal_cosine_score_candidate_pairs(threshold):
    final_can_pairs = {}
    for i in dictionary:
        for key,hash in i.items():
            if len(hash) > 1:
                #print("yes",hash)
                for j in range(0,len(hash)):
                    for k in range(j+1,len(hash)):
                        if cal_cosine_score(sig_mat,hash[j],hash[k]) > threshold:
                            if (hash[j],hash[k]) not in final_can_pairs :
                                final_can_pairs[(hash[j],hash[k])] = cal_cosine_score(sig_mat,hash[j],hash[k])
                                #print(cal_cosine_score(sig_mat,hash[j],hash[k]))
    return final_can_pairs

# finding jaccard similarity between each pair of columns in original input matrix(finalArray)
print("printing similarity between rows")
candidate_pairs = []
for i in range(0,len_doc):
    for j in range(i+1,len_doc):
        ori_int = 0
        ori_uni = 0
        sig_int = 0
        sig_uni = 0

        for k in range(0,len(shingle)):
            if finalArray[k][i] == 1 and finalArray[k][j] == 1:
                ori_int = ori_int + 1
            if finalArray[k][i] == 1 or finalArray[k][j] == 1:
                ori_uni = ori_uni + 1


        for k in range(0,100):
            if sig_mat[k][i] == sig_mat[k][j]:
                sig_int = sig_int + 1
        sig_uni = 100
        jacc_sim_ori = ori_int/ori_uni
        sig_sim_sig = sig_int/sig_uni
        if sig_sim_sig > 0.5:
            list1 = []
            list1.append(i+1)
            list1.append(j+1)
            candidate_pairs.append(list1)
        print(jacc_sim_ori)
        print(sig_sim_sig)
        print()
# printing candidate pairs
print("printint candidate pairs")
print(candidate_pairs)

print("\n\n\n\nprinting band candidate pairs")
num_rows = 20
all_can_pairs = {}
s1 = []
cnt = 0
for k in range(0,int(100/num_rows)):
    band_can_pairs = []
    for i in range(0,len_doc):
        for j in range(i + 1, len_doc):
            sig_band_int = 0
            for l in range(cnt, cnt + num_rows):
                if sig_mat[l][i] == sig_mat[l][j]:
                    sig_band_int = sig_band_int + 1
            score = sig_band_int/num_rows
            if score > 0.6:
                set2 = []
                set2.append(i+1)
                set2.append(j+1)
                print(set2,score)
                band_can_pairs.append(set2)
                if set2 not in s1:
                    s1.append(set2)
    cnt = cnt + num_rows
    all_can_pairs[k] = band_can_pairs
print("print ha ha ha")
print(s1)
print(all_can_pairs)

hash_signature2(sig_mat,20,5)
print("printing using jaccard")
print(cal_jacc_score_candidate_pairs(0.2))
print("printing using cosine")
print(cal_cosine_score_candidate_pairs(0.2))




