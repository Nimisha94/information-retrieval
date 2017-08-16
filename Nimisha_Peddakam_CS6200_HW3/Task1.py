#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import sys
from string import maketrans
import re
import os
from bs4 import BeautifulSoup
from py2casefold import casefold
reload(sys)
sys.setdefaultencoding("UTF-8")
text=""
input = open('URL_list.txt','r')
if not os.path.exists(os.getcwd()+'\Corpus'):
    os.makedirs(os.getcwd()+'\Corpus')
os.chdir(os.getcwd() + '\Corpus')
#t='hello\nhow are you?[9]take care[10]'
#t=re.sub(r'\[[0-9]*\]', "", t, flags=0)
#print t
#print input.read()

def name_change(name):
    n=''
    for char in name:
        if char.isalpha() or char.isdigit():
            n+=char
    return n

for i in input:
    text=""
    response = urllib2.urlopen(i)
    webContent = response.read()
    soup = BeautifulSoup(webContent, 'html.parser')
    title=soup.title.string
    title=re.sub(r'- Wikipedia',"",title,flags=0)
    title=name_change(title)
    print title
    for link in soup.find_all('p'):
        #print(link.get_text())
        text+=link.get_text()
        text = re.sub(r'\[[0-9]*\]', " ", text, flags=0)
        text= re.sub(r'([a-zA-Z])([\.\[\]{}()*+?^$|%"\';’!<>,:/])',r'\1 ',text, flags=0 )
        text = re.sub(r'([a-zA-Z])([\.\[\]{}()*+?^$|%"\';!<>,:])([\.\[\]{}()*+?^$|%"\';!<>,:])', r'\1 ', text, flags=0)
        text=re.sub(r'([0-9])([\.\[\]{}()*+?^$|"\';!<>])([a-zA-Z\s])',r'\1\3',text,flags=0)
        text=re.sub(r'([\.\[\]{}()*+?^$|"\';!<>])([\s])',r'\2',text)
        text=re.sub(r'([\.\[\]{}()*+?^$|"\';!<>])([a-zA-Z])',r'\2',text)
        #for 2012, => 2012
        text=re.sub(r'([0-9])([\.\[\]{}()*+?^,$|"\';!<>])([\s])', r'\1\3',text)
        #for (1973 = 1973
        text=re.sub(r'([\s])([\.\[\]{}()*+?^,$|"\';!<>])([0-9])', r'\1\3',text)
        #for a),b = a b
        text=re.sub(r'([\.\[\]{}()*+?^$|%"\';’!<>,:/\s-])([\.\[\]{}()*+?^$|%"\';’!<>,:/-])',' ',text)
        text=casefold(text)
    target = open(title+'.txt', 'w')
    target.write(text)
    target.close()
