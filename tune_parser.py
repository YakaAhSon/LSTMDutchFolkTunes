import re

import DutchFolkTunes

def removeSpace(s):
    g = re.search(r"^\s+",s)
    if g:
        s = s[g.end():]
    g = re.search(r"\s+$",s)
    if g:
        s = s[:g.start()]
    return s


def height2pitch(height):
    pitches=[
        "C","^C","D","^D","E","F","_G","G","_A","A","_B","B",
        "c","^c","d","^d","e","f","_g","g","_a","a","_b","b",]
    
    if height<0:
        f = 0
        while height<0:
            f+=1
            height+=12
        return pitches[height]+","*f
    elif height>23:
        f = 0
        while height>23:
            f+=1
            height-=12
        return pitches[height]+"'"*f
    else:
        return pitches[height]

def pitch2height(pitch):
    pitches = {
            "C":0,
            "D":2,
            "E":4,
            "F":5,
            "G":7,
            "A":9,
            "B":11,
            "c":12,
            "d":14,
            "e":16,
            "f":17,
            "g":19,
            "a":21,
            "b":23
    }
    g = re.search(r"[A-G,a-g]",pitch)
    if not g:
        print pitch
    result = pitches[g.group()]
    result+=pitch.count("^")
    result-=pitch.count("_")
    result+=12*pitch.count("'")
    result-=12*pitch.count(",")
    return result

class Note:
    duration_from_last=[1,1] #1/1
    def __init__(self, s):
        g = re.search(r'[\-,\^]*[A-Z,a-z][\,,\']*',s)
        self.pitch = g.group()
        if self.pitch not in {"z","Z","x","X"}:
            self.pitch = height2pitch(pitch2height(self.pitch))
        self.duration = s[g.end():]
        self.duration = "1" if self.duration=="" else self.duration




class Bar:
    def __init__(self,tempbar):
        self.bar = tempbar

class Tune:

    def addToken(self,token):
        if re.match( r'[_,^]*[a-z,A-Z]\'*\,*\/?[2-8]?\/*[\<,\>]?',token):
            note = Note(token)
            self.tempbar.append(note)
            self.tokens.append(note)
        elif token == "|":
            if self.tempbar:
                self.bars.append(Bar(self.tempbar))
            self.tempbar=[]
            self.tokens.append("|")
        elif re.match(r'[\!](.*?)[\!]',token) or re.match(r'[\[](.*?)[\]]',token):
                return
        else:
            self.tokens.append(token)

    def parseBodyLine(self,line):
        token_set = [
            r'[\!](.*?)[\!]',
            r'[\[](.*?)[\]]',
            r'[_,^]*[a-z,A-Z]\'?\,?\/*[2-8]?\/*[\<,\>]?',
            r'\|',
            r'\]',
        ]
        token = ""
        start = 10000000
        end = 0
        for r in token_set:
            t = re.search(r,line)
            if t and t.start()<start:
                token = t.group()
                start = t.start()
                end = t.end()
        if len(token)>0:
            self.addToken(token)
            self.parseBodyLine(line[end:])

    

    def parseLine(self,line):
        line = removeSpace(line)
        if ("%%" in line) or ("X: " in line) or ("T:" in line):
            return
        if line[:2]=="L:":
            self.L = removeSpace(line[2:])
        elif line[:2]=="Q:":
            self.Q = removeSpace(line[2:])
        elif line[:2]=="M:":
            self.M = removeSpace(line[2:])
        elif line[:2]=="K:":
            self.K = removeSpace(line[2:])
        else:
            self.parseBodyLine(line)
    # input the string of the tune
    def __init__(self, s):
        v = s.split("\n")

        self.L = "missing"
        self.K = "missing"
        self.Q = "missing"
        self.M = "missing"
        self.tokens = []

        self.tempbar=[]
        self.bars = []
        for line in v:
            self.parseLine(line)

    def getMetaDataList(self):
        return ["L: "+self.L+"\n","Q: "+self.Q+"\n", "M: "+self.M+"\n", "K: "+ self.K+"\n"]

    def getTrainingTokens(self):
        t = self.getMetaDataList()
        for token in self.tokens:
            if isinstance(token, Note):
                t.append("<P>"+token.pitch)
                t.append("<D>"+token.duration)
            elif isinstance(token, str):
                if token=="|":
                    t.append("|\n")
                else:
                    t.append(token)
            else:
                print "ERROR!"
                raise 0
        return t
    
    def getTrainingTokens_Inc(self):
        pass

def loadTrainingSet():
    return [Tune(i) for i in DutchFolkTunes.tune_strings]
