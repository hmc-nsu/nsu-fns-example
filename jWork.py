import json
import random


class Jwork:
    shtamp = ['INN', 'PASSWORD', 'CLIENT_SECRET', 'INUSE']

    def __init__(self):
        self.i = 0
        self.data=dict()
        self.enduse=1
        self.lastuse=None

    def saveDict(self):
        with open("fns_info.json", "w") as write_file:
            json.dump(self.data, write_file, indent=4)

    def doDict(self, inn,password,client_secret)->dict:
        self.i+=1
        return {
            self.i: {
                str(self.shtamp[0]): inn,
                self.shtamp[1]: password,
                self.shtamp[2]: client_secret,
                self.shtamp[3]: 0
            }
        }

    def addUse(self,r):
        return {r: {
                str(self.shtamp[0]): self.data.setdefault(r).setdefault(self.shtamp[0]),
                self.shtamp[1]: self.data.setdefault(r).setdefault(self.shtamp[1]),
                self.shtamp[2]: self.data.setdefault(r).setdefault(self.shtamp[2]),
                self.shtamp[3]: int(self.data.setdefault(r).setdefault(self.shtamp[3]))+1
            }
        }

    def zeroedOne(self,r):
        return {r: {
                str(self.shtamp[0]): self.data.setdefault(r).setdefault(self.shtamp[0]),
                self.shtamp[1]: self.data.setdefault(r).setdefault(self.shtamp[1]),
                self.shtamp[2]: self.data.setdefault(r).setdefault(self.shtamp[2]),
                self.shtamp[3]: 0
            }
        }

    def partDickt(self,r):
        return {
            str(self.shtamp[0]): self.data.setdefault(r).setdefault(self.shtamp[0]),
            self.shtamp[1]: self.data.setdefault(r).setdefault(self.shtamp[1]),
            self.shtamp[2]: self.data.setdefault(r).setdefault(self.shtamp[2]),
        }


    def saveNewData(self, inn,password,client_secret):
        self.loadDict();
        self.data.update(self.doDict(inn,password,client_secret))
        self.saveDict()

    def testData(self):
        self.saveNewData(111, 'qwerty', 'vegan')
        self.saveNewData(222, 'asdfgh', 'ne vegan')

    def loadDict(self):
        with open("fns_info.json", "r") as read_file:
            self.data = json.load(read_file)
        self.i=len(self.data)

    def getInf(self)->dict:
        self.lastuse=self.getCanUse()
        if(self.lastuse==None):
            return None
        return self.partDickt(self.lastuse)

    def tryToUse(self)->bool:
        r=self.lastuse
        if(int(self.data.setdefault(r).setdefault(self.shtamp[3])) >= self.enduse ):
            return False
        self.data.update(self.addUse(r))
        self.saveDict()
        return True

    def getCanUse(self)->str:
        self.loadDict()
        myhave=list()
        r=str( random.randrange(1, self.i+1, 1))
        myhave.append(r)
        donow=True
        while(int(self.data.setdefault(r).setdefault(self.shtamp[3])) >= self.enduse and donow):
            r = str( random.randrange(1, self.i+1, 1))
            myhave.append(r)
            myhave=list(set(myhave))
            if(len(myhave)==self.i):
                donow=False

        if(donow):
            return r
        return None

    def zeroedUse(self):
        self.loadDict()

        for j in range(self.i):
            self.data.update(self.zeroedOne(str(j+1)))
        self.saveDict()

    def doEmpty(self):
        self.data=dict()
        self.saveDict()