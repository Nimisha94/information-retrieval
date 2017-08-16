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
url='https://en.wikipedia.org/wiki/Sustainable_energy'
q=Queue.Queue()
visited=[]
pagelink=""
depth=dict()
depth[url]=1
basepage=[]

class CrawlerHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        try:
            global pagelink
            for t in attrs:
                if t[0]=='href':    #parsing the html content
                   if type(t[1]) is str:
                        if t[1].startswith('/wiki') or t[1].startswith('https://en.wikipedia.org'):
                            s=t[1]
                            if t[1].startswith('/wiki'):
                                s='https://en.wikipedia.org' + s
                            if s not in q.queue and s not in visited and s!='https://en.wikipedia.org':
                                if not s.__contains__("#") and s.count(":")==1:     #checking for admin links and same page links
                                    basepage.append(s)                              #used to maintain base URL to distinguish URLS with #
                                    q.put(s)
                                    if s != pagelink:
                                        depth[s] = depth[pagelink] + 1              #maintaining the depth for each webpage
                                elif s.__contains__("#") and s.count(":")==1:
                                    st=s.split("#")
                                    if st[0] not in basepage:
                                        basepage.append(st[0])
                                        q.put(s)
                                        if s != pagelink:
                                            depth[s] = depth[pagelink] + 1
                                elif not s.count(":")>1:
                                    q.put(s)
                                    if s != pagelink:
                                        depth[s] = depth[pagelink] + 1
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

class StarterClass:
    def crawl_method(self,link):
        try:
            global pagelink
            parser = CrawlerHTMLParser()
            while visited.__len__()<1000 and depth[link]<=5:        #checking the limit of 1000 URLS and depth upto 5 levels
                time.sleep(1)                                       #abiding by the politeness policy
                page = requests.get(link)
                pagelink=link
                soup = BeautifulSoup(page.content, 'html.parser')
                for tag in soup.find_all('html'):
                    if tag.get('lang')=='en':                       #checking the language for english
                        parser.feed(page.content)
                        if link not in visited:
                            visited.append(link)
                            print "Link crawled:", link
                        if visited.__len__()==1000:
                             break
                        else:
                            self.crawl_method(q.get())              #recursively calling the crawl method
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
    myobject = StarterClass()
    myobject.crawl_method(url)
    f = open('Task1.txt', 'w')
    for v in visited:
        f.write("%s\n" % v)                     #writing the links to the text file
    f.close()
    counter=0
    #generating 1000 text files-crawled URLs
    for v in visited:
        page = urllib2.urlopen(v)
        html_content = page.read()
        rendered_content = html2text.html2text(html_content)
        filename='file_text'+str(counter)+'.txt'
        counter+=1
        html_file = open(filename, 'w')
        html_file.write(rendered_content)
        html_file.close()

main()