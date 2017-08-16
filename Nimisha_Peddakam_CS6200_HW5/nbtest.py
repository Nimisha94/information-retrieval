import json, sys, math, operator, os, glob

total_neg_terms=0
total_pos_terms=0
total_terms=0
pos_to_neg_weight={}
neg_to_pos_weight={}
test_pos_val={}
test_neg_val={}

model_file=sys.argv[1]
path=sys.argv[2]
predictions_file=sys.argv[3]

with open(sys.argv[1]) as data_file:
    data = json.load(data_file)

neg_terms,pos_terms,all_terms=data[0],data[1],data[2]

for t in pos_terms:
    if pos_terms[t]<=0:
        print t

for t in neg_terms:
    if neg_terms[t]<=0:
        print t

for term in neg_terms:
    total_neg_terms+=neg_terms[term]

for term in pos_terms:
    total_pos_terms+=pos_terms[term]

for term in all_terms:
    total_terms+=all_terms[term]

for term in all_terms:
    if term in pos_terms:
        pos_term_frequency=pos_terms[term]
    else:
        pos_term_frequency=1.0
    if term in neg_terms:
        neg_term_frequency=neg_terms[term]
    else:
        neg_term_frequency=1.0
    pos_ratio=pos_term_frequency/float(total_pos_terms)
    neg_ratio = neg_term_frequency / float(total_neg_terms)
    pos_to_neg_weight[term]=math.log(pos_ratio/neg_ratio)
    neg_to_pos_weight[term]=math.log(neg_ratio/pos_ratio)
sorted_pos_to_neg_weight = sorted(pos_to_neg_weight.items(), key=operator.itemgetter(1), reverse=True)
sorted_neg_to_pos_weight = sorted(neg_to_pos_weight.items(), key=operator.itemgetter(1), reverse=True)
f_sort_postoneg=open('Postive_To_Negative_Weight.txt','w')
f_sort_postoneg.write("Term"+"\t"+"PositiveToNegativeRatio"+"\n")
for i in range(0,20):
    f_sort_postoneg.write(str(sorted_pos_to_neg_weight[i][0])+"\t"+str(sorted_pos_to_neg_weight[i][1])+"\n")
f_sort_postoneg.close()

f_sort_negtopos=open('Negative_To_Positive_Weight.txt','w')
f_sort_negtopos.write("Term"+"\t"+"NegativeToPositiveRatio"+"\n")
for i in range(0,20):
    f_sort_negtopos.write(str(sorted_neg_to_pos_weight[i][0])+"\t"+str(sorted_neg_to_pos_weight[i][1])+"\n")
f_sort_negtopos.close()

prior_positive_terms_prob=math.log(total_pos_terms/float(total_terms))
prior_negative_terms_prob=math.log(total_neg_terms/float(total_terms))

path=sys.argv[2]
os.chdir(path)
test_files=glob.glob("*.txt")
for file in test_files:
    pos_freq=0
    pos_ratio=0
    neg_freq=0
    neg_ratio=0
    f=open(path+"\\"+file,'r')
    listofwords=[]
    listofwords=[word for line in f for word in line.split()]
    for word in listofwords:
        if word in pos_terms:
            pos_freq=pos_terms[word]
        if word in neg_terms:
            neg_freq=neg_terms[word]
        if pos_freq==0:
            pos_freq=1
        if neg_freq==0:
            neg_freq=1
        pos_ratio=pos_ratio+math.log(pos_freq/float(total_pos_terms))
        neg_ratio=neg_ratio+math.log(neg_freq/float(total_neg_terms))
    pos=pos_ratio+prior_positive_terms_prob
    neg=neg_ratio+prior_negative_terms_prob
    test_pos_val[file]=pos
    test_neg_val[file]=neg
    f.close()

pos_rev=0
neg_rev=0

for t in test_neg_val:
    if test_neg_val[t]>test_pos_val[t]:
        neg_rev+=1
    elif test_pos_val[t]>test_neg_val[t]:
        pos_rev+=1


f=open(predictions_file,'w')
f.write("Accuracy-- "+"Negative: "+str(((neg_rev)/float(len(test_pos_val)))*100)+" Positive: "+str((pos_rev/float(len(test_pos_val)))*100)+"\n")
for t in test_pos_val:
    f.write("Filename-- "+t+" Score for positive review: "+str(test_pos_val[t])+" Score for negative review: "+
            str(test_neg_val[t])+"\n")
f.close()

print "Generated Predictions file and List of top 20 terms"