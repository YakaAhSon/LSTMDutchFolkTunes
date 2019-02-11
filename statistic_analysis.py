import re
class Tune:
    def __init__(self):
        self.L = "missing"
        self.K = "missing"
        self.M = "missing"
        self.Q = "missing"

def getTune(s):
    v = s.split("\n")
    tune = Tune()

    x = re.findall(r"K: [A-Z]b?",s)
    if len(x)>0:
        tune.K = x[0][3:]

    x = re.findall(r"L: \d/\d",s)
    if len(x)>0:
        tune.L = x[0][3:]
    
    x = re.findall(r"M: \d/\d",s)
    if len(x)>0:
        tune.M = x[0][3:]
    
    x = re.findall(r"Q: \d/\d=\d{2,3}",s)
    if len(x)>0:
        tune.Q = x[0][7:]

    return tune

def read_data(filename):
    f = open(filename,"r")
    s = f.read().split("\n\n")
    s = filter(lambda x: len(x)>10,s)

    result = []
    for i in s:
        result.append(getTune(i))

    return result

training = []
for i in range(1,2):
    training += read_data("./DutchFolkTunes/allnlb%d000.abc"%i)

sample = read_data("./samples/config5--20190120-011314-s42-1.00-20190121-210855.txt")

print len(training)
print len(sample)

import collections

trainingL = [i.L for i in training]
counterTL = collections.Counter(trainingL)

trainingM = [i.M for i in training]
counterTM = collections.Counter(trainingM)

trainingK = [i.K for i in training]
counterTK = collections.Counter(trainingK)

trainingQ = [i.Q for i in training]
counterTQ = collections.Counter(trainingQ)

sampleL = [i.L for i in sample]
counterSL = collections.Counter(sampleL)

sampleM = [i.M for i in sample]
counterSM = collections.Counter(sampleM)

sampleK = [i.K for i in sample]
counterSK = collections.Counter(sampleK)

sampleQ = [i.Q for i in sample]
counterSQ = collections.Counter(sampleQ)

def createCSVFile(name,ctraining,csample):
    s = ",training, sample\n"
    c = {}
    for i in ctraining:
        c[i] = [ctraining[i],0]
    for i in csample:
        if i in c:
            c[i][1] = csample[i]
        else:
            c[i] = [0,csample[i]]
    for i in c:
        s+="'%s,%.2f,%.2f\n"%(i,c[i][0]*100.0/len(training),c[i][1]*100.0/len(sample))
    
    f = open("./ana/%s.csv"%name,"w")
    f.write(s)
    f.close()

createCSVFile("L",counterTL,counterSL)
createCSVFile("M",counterTM,counterSM)
createCSVFile("Q",counterTQ,counterSQ)
createCSVFile("K",counterTK,counterSK)