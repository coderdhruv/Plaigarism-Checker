import timeit
import pandas as pd
import numpy as np
import random
import math

start = timeit.default_timer()
#files for storing the results
f1 = open("ir_jacc_sim.txt", 'w+')
f2 = open("ir_sig_sim.txt", 'w+')
f3 = open("ir_sig_sim_band.txt", 'w+')
f4 = open("ir_cosine_sim.txt", 'w+')
f5 = open("ir_row_band_sim_scores.txt", 'w+')
f6 = open("ir_jacc_and_cosine_sim_using_string_hash.txt", 'w+')
f7 = open("ir_running_time.txt", 'w+')
f8 = open("ir_writing_hash_buckets.txt", 'w+')
#function to calculate jaccard score given two documents from the column vectors in
#signature matrix
def cal_jaccard_score(sigmat,d1,d2):
    intersec = 0
    uni = 0
    for i in range(0,len(sigmat)):
        if sigmat[i][d1] == sigmat[i][d2]:
            intersec += 1
    uni = len(sigmat)
    return intersec/uni


#function to calculate cosine score given two documents from the column vectors in
#signature matrix
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


dictionary = list()  # a list  to store hashed buckets
#This function is used to create hashbuckets for every band in the 
#signature matrix
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
    


#function to calculate candidate pairs using jaccard score
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



#function to calculate candidate pairs using cosine score
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


#initializing variables
df = pd.read_csv('news_summary.csv', sep=',', encoding='latin-1')
d = {}
shingle = {}
len_doc = 0



# making shingles of length 9
for x in range(0, 5):
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
    


# making the list obtained as value from 9-shingle key unique
for key,value in shingle.items():
    list1 = set(value)
    shingle[key] = list(list1)

#print(shingle)


#building the input matrix
finalArray = np.zeros(shape=(len(shingle), len_doc))
e = 0
for key, value in shingle.items():
    #print(value)
    for i in value:
        finalArray[e][i] = 1
    e = e + 1

#print(finalArray)


#building the signature matrix using hash functions

#initializing signature matrix and filling with infinity values
sig_mat = np.zeros(shape = (100,len_doc))
for i in range(0,100):
    for j in range(0,len_doc):
        sig_mat[i][j] = 999999



#building list that will be used for multiplication with x in hash function ax + b i.e. a
mul_list = set(random.sample(range(0, 1000), 100))
while(len(mul_list)<100):
    mul_list.append(random.sample(range(0, 1000), 1)[0])
mul_list = list(mul_list)



#building list that will be used for addition in h(x) in hash function ax + b i.e. b
add_list = set(random.sample(range(0, 1000), 100))
while(len(add_list)<100):
    add_list.append(random.sample(range(0, 1000), 1)[0])
add_list = list(add_list)



#building 100 hash functions
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
print(sig_mat)


#finding jaccard similarity between each pair of columns in original input matrix(finalArray) and signature matrix
print("printing similarity between rows")
candidate_pairs = []
for i in range(0,len_doc):
    for j in range(i+1,len_doc):
        ori_int = 0
        ori_uni = 0
        sig_int = 0
        sig_uni = 0
        
        #for cosine similarity-
        mult = 0;
        mod_doc1 = 0;
        mod_doc2 = 0;

        for k in range(0,len(shingle)):
            if finalArray[k][i] == 1 and finalArray[k][j] == 1:
                ori_int = ori_int + 1
            if finalArray[k][i] == 1 or finalArray[k][j] == 1:
                ori_uni = ori_uni + 1


        for k in range(0,100):
            if sig_mat[k][i] == sig_mat[k][j]:
                sig_int = sig_int + 1
            mult = mult + sig_mat[k][i] * sig_mat[k][j]
            mod_doc1 = mod_doc1 + sig_mat[k][i]*sig_mat[k][i]
            mod_doc2 = mod_doc2 + sig_mat[k][j]*sig_mat[k][j]
        cosine_sim = mult/(math.sqrt(mod_doc1) * math.sqrt(mod_doc2))
        sig_uni = 100
        jacc_sim_ori = ori_int/ori_uni
        sig_sim_sig = sig_int/sig_uni
        if sig_sim_sig > 0.2:
            list1 = []
            list1.append(i)
            list1.append(j)
            candidate_pairs.append(list1)
        f1.write("Jaccard Similarity between doc %d & %d : %f\n" %(i, j, jacc_sim_ori))
        f2.write("Signature Similarity between doc %d & %d : %f\n" %(i, j, sig_sim_sig))
        f4.write("Cosine Similarity between doc %d & %d : %f\n" %(i, j, cosine_sim))

#printing candidate pairs
print("printing candidate pairs")
print(candidate_pairs)

print("\n\nprinting band candidate pairs")
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
            f5.write("%d and %d row similarity for band %d: %f" %(i, j, k, score))
            f5.write("\n")
            if score > 0.2:
                set2 = []
                set2.append(i)
                set2.append(j)
                print(set2,score)
                band_can_pairs.append(set2)
                if set2 not in s1:
                    s1.append(set2)
    cnt = cnt + num_rows
    all_can_pairs[k] = band_can_pairs
s1.sort()
print(s1)
print(all_can_pairs)

for key, value in all_can_pairs.items():
    f3.write("Candidate pairs for band %d are: " %(key+1))
    f3.write(str(value))
    f3.write("\n")    
f3.write("\n\n\n All combined candidate pairs: ")
f3.write(str(s1))

#combining all functions to obtain the final candidate pairs
hash_signature2(sig_mat,20,5)
print("printing using jaccard")
calculated_jacc_score = cal_jacc_score_candidate_pairs(0.2)
calculated_cosine_score = cal_cosine_score_candidate_pairs(0.2)
print(calculated_jacc_score)
f6.write(str(calculated_jacc_score))
print("printing using cosine")
print(calculated_cosine_score)
stop = timeit.default_timer()
q1 = 0
for i in dictionary:
    f8.write(str(i))
    f8.write("\n")
print("Running time:",stop - start)
f7.write(str(stop-start))
f6.write("\n\n\n\n")
f6.write(str(calculated_cosine_score))
f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
f7.close()
f8.close()

