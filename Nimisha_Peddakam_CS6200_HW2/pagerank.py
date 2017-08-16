import sys
from math import log
from math import pow
pages=[]
sinknodes=[]
l=""
d=0.85
pageranks=dict()
entropy=0
perplexitycount=0
perplexity=0
iterationcount=0
inlinkdict={}
outlinkdict={}

def dict_for_in_links(graph):
    global inlinkdict
    for g in graph:
        inlinks=[]
        inl=g.split(" ")[1:]
        for k in inl:
            inlinks.append(k.strip('\n'))
        for k in inlinks:
            if k=='':
                inlinks.remove(k)
        inlinkdict[g.split(" ")[0].strip("\n")]=list(set(inlinks))
    return inlinkdict

def inlinkstopage(p, graph):
    return inlinkdict[p]

def outlinkstopage(p, graph):
    return outlinkdict[p]

def main():
    global inlinks
    global perplexity
    global perplexitycount
    global entropy
    global iterationcount
    global inlinkdict
    f=open(sys.argv[1],"r")
    graph=f.readlines()
    inlinkdict=dict_for_in_links(graph)
    pages=inlinkdict.keys()     # all pages
    for lists in inlinkdict.values():   
        for k in lists:
            if outlinkdict.has_key(k):
                outlinkdict[k] = outlinkdict[k] + 1
            else:
               outlinkdict[k] = 1
    sinknodes=list(set(inlinkdict.keys())-set(outlinkdict.keys()))
    for p in pages:             # intial value of pagerank is 1/total number of pages
        pageranks[p] = 1/float(len(pages))
    entropy=0
    for p in pages:
        entropy+= -(pageranks[p]*log(pageranks[p],2))
    perplexity=pow(2, entropy)
    perplexitycount=0
    while perplexitycount<4:
        entropy=0
        latestpagerank={}
        iterationcount+=1
        sinkPR=0        
        for p in sinknodes:
            sinkPR+=pageranks[p]
        for p in pages:
            latestpagerank[p]=(1-d)/len(pages)
            latestpagerank[p]+=d*sinkPR/len(pages)
            for q in inlinkstopage(p, graph):
                latestpagerank[p]+=d*pageranks[q]/outlinkstopage(q, graph)
        for p in pages:
            pageranks[p]=latestpagerank[p]
        for p in pages:
            entropy+= -(pageranks[p]*log(pageranks[p],2))
        if perplexity-pow(2,entropy)<1:
            perplexity=pow(2,entropy)
            perplexitycount+=1
        else:
            perplexity=pow(2,entropy)
            perplexitycount=0
        print "Perplexity for iteration",iterationcount,perplexity
    print "Top 50 pages in the decreasing order of pagerank"
    sorted_pageranks = sorted(pageranks, key=lambda x: pageranks[x],reverse=True)
    for k in sorted_pageranks[:50]:
        print("{} : {}".format(k, pageranks[k]))
    noinlinkscnt=0
    for i in inlinkdict:
        if len(inlinkdict[i])==0:
            noinlinkscnt+=1
    print "No. of pages with no in-links", noinlinkscnt
    print "No. of pages with no out-links", len(sinknodes)
    print "Proportion of pages with no in-links", float(noinlinkscnt)/len(pages)
    print "Proportion of pages with no out-links", float(len(sinknodes))/len(pages)
    inlinkcount={}
    for g in inlinkdict:
        inlinkcount[g]=len(inlinkdict[g])
    sorted_inlinkcount = sorted(inlinkcount, key=lambda x: inlinkcount[x],reverse=True)
    for k in sorted_inlinkcount[:50]:
        print("{} : {}".format(k, inlinkcount[k]))
main()
