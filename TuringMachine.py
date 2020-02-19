import re

#read txt files
testcase1 = open('testcase1.txt', 'r')
testcase1 = testcase1.read()

testcase2 = open('testcase2.txt', 'r')
testcase2 = testcase2.read()

testcase3 = open('testcase3.txt', 'r')
testcase3 = testcase3.read()

testcase4 = open('testcase4.txt', 'r')
testcase4 = testcase4.read()

testcase5 = open('testcase5.txt', 'r')
testcase5 = testcase5.read()

testcase6 = open('testcase6.txt', 'r')
testcase6 = testcase6.read()

TMmaxLoop = 20
class semiTape:
    def __init__(self, inputString=''):
        self.header=0
        self.stringArray = list(inputString)  #stringArray is a list whose elements are str type
     
    def copy(self, semiTape2):
        self.header = semiTape2.header
        self.stringArray = semiTape2.stringArray.copy()
    
    def read(self):  #return current symbol
        return self.stringArray[self.header]
    
    def printAll(self): #used for debugging
        for i in range(len(self.stringArray)):
            print (self.stringArray[i], end="")
    
    def write(self, checkChar, writeChar, direction):
        if self.stringArray[self.header] == checkChar:
            self.stringArray[self.header] = writeChar
            if direction=='R':
                #boundary case
                if self.header==len(self.stringArray)-1:
                    self.stringArray.append('_') 
                    self.header = self.header+1
                else:
                    self.header = self.header+1
            elif direction=='L':
                if self.header != 0:
                    self.header = self.header-1
            return True
        
        else:
            print('no such transition, error')
            return False


class TMpath:
    def __init__(self, inputString=''):
        self.semiTape = semiTape(inputString)
        self.currentNode = 'q0'
        self.flag = 'none' # accept, reject(reach qr or no transition), none 
        
    def copy(self, TMpath2):
        self.semiTape.copy(TMpath2.semiTape)
        self.currentNode = TMpath2.currentNode
        
    def write(self, nextNode, checkChar, writeChar, direction):
        self.currentNode = nextNode
        self.semiTape.write(checkChar, writeChar, direction)
        if self.currentNode == 'qa':
            self.flag = 'accept'
        elif self.currentNode == 'qr':
            self.flag = 'reject'
        
    def readSym(self):  #return current symbol of semiTape
        return self.semiTape.read()
    
    def readNode(self):
        return self.currentNode


class TMnode:
    def __init__(self, name):
        self.name = name
        self.transTable = []  #transition table
        
    def writeTransTable(self, oldSym, newSym, newNode, direction): #4-element tuple: old tapeSymbol, new tapeSymbol, new node, direction
        self.transTable.append( (oldSym, newSym, newNode, direction) )
        
class TuringMachine:
    def __init__(self, txtString, maxLoop):
        self.nodedict = {}
        self.transCount = 0
        self.nodeCount = 0
        self.pathTable = []
        self.maxLoop = maxLoop
        self.resultString = 'M is still running'
        
        txtString = txtString.rstrip()
        txtString = re.split('#', txtString)
        txtString = [x for x in txtString if x]
        
        #get inputString
        self.inputString = txtString[-1]
        
        #get TM structure
        self.Structure = txtString[:-1]
        self.transCount = len(self.Structure)
        
        #initialize TM structure
        for transStr in self.Structure:
            transStr = re.split(',|->', transStr)
            if transStr[0] not in self.nodedict:
                self.nodedict[transStr[0]] = TMnode(transStr[0])
                self.nodedict[transStr[0]].writeTransTable(transStr[1], transStr[3], transStr[2], transStr[4])
                self.nodeCount = self.nodeCount + 1

            else:
                self.nodedict[transStr[0]].writeTransTable(transStr[1], transStr[3], transStr[2], transStr[4])

            if transStr[2] not in self.nodedict:
                self.nodedict[transStr[2]] = TMnode(transStr[2])
                self.nodeCount = self.nodeCount + 1
                
    def runTM(self):
        initPath = TMpath(self.inputString)
        self.pathTable.append(initPath)
        notAccept = True
        while(self.maxLoop>=0 and notAccept):
            self.maxLoop = self.maxLoop-1
            loopPathTable = self.pathTable.copy()
            for index, path in enumerate(loopPathTable):
                if path.flag == 'accept':
                    notAccept = False
                    self.resultString = 'M stops and accepts w' 
                    break
                    
                if path.flag != 'reject':
                    nextTrans = [x for x in self.nodedict[path.readNode()].transTable if x[0] == path.readSym()] 
                    if len(nextTrans) == 0:
                        self.pathTable[index].flag = 'reject'
                    elif len(nextTrans) == 1:
                        nextTransItem = nextTrans[0]
                        self.pathTable[index].write(nextTransItem[2], nextTransItem[0], nextTransItem[1], nextTransItem[3])
                        
                        #update flag
                        if nextTransItem[2] == 'qa':
                            self.pathTable[index].flag = 'accept'
                        elif nextTransItem[2] == 'qr':
                            self.pathTable[index].flag = 'reject'
                    
                    elif len(nextTrans)>=2:
                        subPathList = [TMpath() for x in range(len(nextTrans)-1)]
                        for x in range(len(subPathList)):
                            subPathList[x].copy(path) 
                        subPathList.insert(0, self.pathTable[index])
                        
                        for ind, nextTransItem in enumerate(nextTrans):
                            subPathList[ind].write(nextTransItem[2], nextTransItem[0], nextTransItem[1], nextTransItem[3])
                            #update flag
                            if nextTransItem[2] == 'qa':
                                subPathList[ind].flag = 'accept'
                            elif nextTransItem[2] == 'qr':
                                subPathList[ind].flag = 'reject'
                            
                            if ind>0:
                                self.pathTable.append(subPathList[ind])  
                          
                        
        if notAccept:
            self.resultString = 'M stops and rejects on w'
            for x in self.pathTable:
                if x.flag != 'reject':
                    self.resultString = 'M is still running'
                    break
        
        #line1
        print('The encoding string of Turing Machine:')
        stdForm = []
        stdForm.append('')
        stdForm = stdForm + self.Structure
        stdForm.append('')
        print('#'.join(str(ele) for ele in stdForm) )
        print()
               
        #line2
        print('input string:')
        print(''.join(str(ele) for ele in ['e' if i=='_' else i for i in self.inputString ] ) )
        print()
        
        #line3
        print('Total number of transitions:')
        print(self.transCount)
        print()
        
        #line4
        print('Total number of states')
        print(self.nodeCount)
        print()
        
        #line5
        print('Result:')
        print (self.resultString)
        print()
                
    
print('TM1')
TM1 = TuringMachine (testcase1, TMmaxLoop)
TM1.runTM()

print('TM2')
TM2 = TuringMachine (testcase2, TMmaxLoop)
TM2.runTM()

print('TM3')
TM3 = TuringMachine (testcase3, TMmaxLoop)
TM3.runTM()

print('TM4')
TM4 = TuringMachine (testcase4, TMmaxLoop)
TM4.runTM()

print('TM5')
TM5 = TuringMachine (testcase5, TMmaxLoop)
TM5.runTM()

print('TM6')
TM6 = TuringMachine (testcase6, TMmaxLoop)
TM6.runTM()

