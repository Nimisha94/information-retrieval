from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import requests
import Queue
import sys
import httplib
import urllib2
import html2text
import time

reload(sys)
sys.setdefaultencoding("UTF-8")
sys.setrecursionlimit(9000)
q=Queue.Queue()
visited=[]
pagelink=""
depth=dict()
depth[sys.argv[2]]=1
basepage=[]
keywords = []

class MyHTMLParser(HTMLParser):

   def handle_starttag(self, tag, attrs):
        try:
            global pagelink
            for t in attrs:
                if t[0]=='href':
                   if type(t[1]) is str:
                        if t[1].startswith('/wiki') or t[1].startswith('https://en.wikipedia.org'):
                            s=t[1]
                            if t[1].startswith('/wiki'):
                                s = 'https://en.wikipedia.org' + s
                            if s not in q.queue and s not in visited and s != 'https://en.wikipedia.org':
                                if not s.__contains__("#") and s.count(":") == 1:
                                    if s not in basepage:
                                        basepage.append(s)
                                        q.put(s)
                                        if s != pagelink:
                                            depth[s] = depth[pagelink] + 1
                                elif s.__contains__("#") and s.count(":") == 1:
                                    st = s.split("#")
                                    if st[0] not in basepage:
                                        basepage.append(st[0])
                                        q.put(s)
                                        if s != pagelink:
                                            depth[s] = depth[pagelink] + 1
                                elif not s.count(":") > 1:
                                    q.put(s)
                                    if s != pagelink:
                                        depth[s] = depth[pagelink] + 1
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

class MyClass:
    def mymethod(self,link):
        try:
            global pagelink
            parser = MyHTMLParser()
            while visited.__len__()<90 and depth[link]<=5:
                time.sleep(1)
                page = requests.get(link)
                pagelink=link
                soup = BeautifulSoup(page.content, 'html.parser')
                for tag in soup.find_all('html'):
                    if tag.get('lang')=='en':
                        if link.__contains__(keywords[0]) or link.__contains__(keywords[1]):
                            parser.feed(page.content)
                            if link not in visited:
                                visited.append(link)
                                print "Link crawled:", link
                        if visited.__len__()==90:
                             break
                        else:
                             self.mymethod(q.get())
        except Exception as inst:
            print "Link:",link
            print(type(inst))
            print(inst.args)
            print(inst)
            x, y = inst.args
            print('x =', x)
            print('y =', y)
            print "Link error:", link

def main():
    keywords.append(sys.argv[1])
    keywords.append(sys.argv[1].title())
    myobject = MyClass()
    myobject.mymethod(sys.argv[2])
    print "Size of Queue:",q.qsize()

    f = open('Task2A.txt', 'w')

    for v in visited:
        f.write("%s\n" % v)

    f.close()
    counter=0
    for v in visited:
        page = urllib2.urlopen(v)
        html_content = page.read()
        rendered_content = html2text.html2text(html_content)
        filename='BFS_file_text'+str(counter)+'.txt'
        counter+=1
        html_file = open(filename, 'w')
        html_file.write(rendered_content)
        html_file.close()

main()