#!/usr/bin/python
# -*- coding: utf-8 -*-
import glob, os
import csv
import operator
listoffilesincorpus=[]
invertedindex=dict()
termfrequency=dict()
sorted_termfrequency=list()
documentfrequency=dict()
if not os.path.exists(os.getcwd()+'\Corpus'):
    os.makedirs(os.getcwd()+'\Corpus')
os.chdir(os.getcwd()+'\Corpus')
for file in glob.glob("*.txt"):
    listoffilesincorpus.append(file)
for file in listoffilesincorpus:
    listofbigrams=[]
    docid=file.split(".")[0]
    print docid
    f = open(docid+'.txt','r')
    listofwords=[word for line in f for word in line.split()]
    print len(listofwords)
    i=0
    while i<len(listofwords)-1:
        bigram=""
        bigram=listofwords[i]+" "+listofwords[i+1]
        i+=1
        listofbigrams.append(bigram)
    print len(listofbigrams)
    listofbigrams_without_duplicates = list(set(listofbigrams))
    print len(listofbigrams_without_duplicates)
    for word in listofbigrams_without_duplicates:
        if word not in invertedindex:
            invertedindex[word]=[]
            invertedindex[word].append([docid,listofbigrams.count(word)])
        else:
            invertedindex[word].append([docid,listofbigrams.count(word)])
    f.close()
print len(invertedindex)
f=open('inverted_index_bigrams.csv','wb')
w = csv.writer(f)
w.writerows(invertedindex.items())
f.close()
#term frequency table
for index in invertedindex:
    tf=0
    for doc in invertedindex[index]:
        tf+=doc[1]
    termfrequency[index]=tf
print len(termfrequency)
sorted_tf = sorted(termfrequency.items(), key=operator.itemgetter(1))
for i in reversed(sorted_tf):
    sorted_termfrequency.append(i)
f=open('term_frequency_bigram.csv','wb')
csv_out=csv.writer(f)
csv_out.writerow(['term','frequency'])
for row in sorted_termfrequency:
    csv_out.writerow(row)
f.close()
#document frequency table
for i in invertedindex:
    lst=[]
    doclst=[]
    for l in invertedindex[i]:
        doclst.append(l[0])
    lst.append(doclst)
    lst.append(len(doclst))
    documentfrequency[i]=lst
allkeys=documentfrequency.keys()
allkeys.sort()
sort_df=[]
for key in allkeys:
    k=(key,documentfrequency[key])
    sort_df.append(k)
f=open('document_frequency_bigram.csv','wb')
csv_out=csv.writer(f)
csv_out.writerow(['term','documents and df'])
for row in sort_df:
    csv_out.writerow(row)
f.close()