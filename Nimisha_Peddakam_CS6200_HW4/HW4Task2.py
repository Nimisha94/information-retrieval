#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
import operator
import math
import re
reload(sys)
sys.setdefaultencoding("UTF-8")

queries=dict()
queries1=dict()
listofbigrams=[]
document_length=dict()
avg_len_doc=0
s=0
b=0.75
k1=1.2
k2=100
score=0
R=0
term_query=dict()
term_scores= dict()
query_score=0
documentfrequency=dict()
sorted_bm25docs=[]
query_count=0

with open('inverted_index.csv', mode='r') as infile:
    reader = csv.reader(infile)
    unigrams_dict = dict((rows[0],rows[1]) for rows in reader)
with open('Documents_Length.csv', mode='r') as infile:
    reader = csv.reader(infile)
    document_length = dict((rows[0],rows[1]) for rows in reader)
with open('Input_Queries.csv', mode='r') as infile:
    reader = csv.reader(infile)
    queries = dict((rows[1],rows[0]) for rows in reader)

print queries

for d in document_length:
    s+=int(document_length[d])
    n = ''
    for char in d:
        if char.isalpha() or char.isdigit():
            n += char
    document_length[n] = document_length.pop(d)
avg_len_doc=s/len(document_length)

#print sys.argv[0], sys.argv[1], sys.argv[2]
"""while query_count<int(sys.argv[1]):
    queries[sys.argv[query_count+2]]=query_count
    query_count+=1"""



#print document_length['BadenWrttemberg']

N=len(document_length)

for q in queries:
    query=q
    bm25 = dict()
    termdocdict = dict()
    bm25_scores = []
    #query="light bulb bulbs alternative alternatives"
    terms_in_query=query.split(" ")
    for term in terms_in_query:
        termdocdict[term]=[]
        if term not in term_query:
            term_query[term]=1
        else:
            term_query[term]+=1
    #getting the dictionary from csv file
    for term in terms_in_query:
        list_of_unigrams = unigrams_dict[term]
        list_of_unigrams=list_of_unigrams[2:len(list_of_unigrams)-2]
        unigrams_arr=list_of_unigrams.split("], [")
        for doc_count in unigrams_arr:
            l=[]
            a=doc_count.split(",")
            l.append(a[0].replace("'",""))
            l.append(a[1])
            termdocdict[term].append(l)

    for termdoc in termdocdict:
        for doc in termdocdict[termdoc]:
            new_name=""
            l=[]
            n=doc[0].encode('string-escape')
            if n.find(r"\\x")!=-1:
                new_name=n[0:n.find(r"\x")-1]+n[(n.find(r"\x")+4):len(n)]
                print new_name
                K = ((1 - b) + (b * int(document_length[new_name]) / avg_len_doc)) * k1
            elif n.find(r"\x")!=-1:
                new_name=n[0:n.find(r"\x")-1]+n[(n.find(r"\x")+4):len(n)]
                print new_name
                K = ((1 - b) + (b * int(document_length[new_name]) / avg_len_doc)) * k1
            else:
                K = ((1 - b) + (b * int(document_length[doc[0]]) / avg_len_doc)) * k1
            n=(len(termdocdict[termdoc]))
            f=doc[1]
            score1=(0+0.5)/(0-0+0.5)
            score2=(n-0+0.5)/(N-n-0+0+0.5)
            score3=(float(k1+1)*float(f))/(float(K)+float(f))
            score4=(float(k2+1)*float(term_query[termdoc]))/(float(k2)+float(term_query[termdoc]))
            final_score=(math.log(score1/score2))*score3*score4
            l.append(doc[0])
            l.append(final_score)
            if doc[0] not in bm25:
                bm25[doc[0]]=0
                bm25[doc[0]]+=final_score
            else:
                bm25[doc[0]]+=final_score
    #print bm25
    sorted_bm25 = sorted(bm25.items(), key=operator.itemgetter(1))
    for i in reversed(sorted_bm25):
        sorted_bm25docs.append(i)
    rank=1
    for t in sorted_bm25:
        t=t+(queries[q],"Q0",rank,"BM_25")
        t_new=(t[2],t[3],t[0],t[4],t[1],t[5])
        bm25_scores.append(t_new)
        rank+=1
    #print bm25_scores
    f=open('BM25_Documents-'+query+'.csv','wb')
    csv_out=csv.writer(f)
    csv_out.writerow(['query_id', 'Q0', 'doc_id', 'rank', 'BM25_Score','system_name'])
    row_count=0
    for row in bm25_scores:
        if row_count<100:
            csv_out.writerow(row)
            row_count+=1
        else:
            break
    f.close()