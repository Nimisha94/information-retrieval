import sys,glob,os,json

neg_files=[]
pos_files=[]
train_neg={}
train_pos={}
combined_train_data={}
l=[]

train_neg_filepath=sys.argv[1]+"/train/neg"
train_pos_filepath=sys.argv[1]+"/train/pos"

os.chdir(train_neg_filepath)
neg_files=glob.glob("*.txt")

os.chdir(train_pos_filepath)
pos_files=glob.glob("*.txt")

path=sys.argv[1]+"\\train\\neg\\"
for file in neg_files:
    f=open(path+file,'r')
    listofwords=[]
    listofwords=[word for line in f for word in line.split()]
    for word in listofwords:
        if word not in train_neg:
            train_neg[word]=1
        else:
            train_neg[word]+=1
    f.close()

path=sys.argv[1]+"\\train\\pos\\"
for file in pos_files:
    f=open(path+file,'r')
    listofwords = []
    listofwords = [word for line in f for word in line.split()]
    for word in listofwords:
        if word not in train_pos:
            train_pos[word] = 1
        else:
            train_pos[word] += 1
    f.close()

for w in train_neg:
    if w not in combined_train_data:
        combined_train_data[w]=train_neg[w]
    else:
        combined_train_data[w]+=train_neg[w]

for w in train_pos:
    if w not in combined_train_data:
        combined_train_data[w]=train_pos[w]
    else:
        combined_train_data[w]+=train_pos[w]

for w in combined_train_data:
    if combined_train_data[w]<5:
        if w in train_neg:
            train_neg.pop(w)
        if w in train_pos:
            train_pos.pop(w)

l.append(train_neg)
l.append(train_pos)
l.append(combined_train_data)

with open(sys.argv[1]+'\\'+sys.argv[2], 'w') as fp:
    json.dump(l, fp)
