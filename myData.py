class MyData:
    __INN=""
    __PASSWORD=""
    __CLIENT_SECRET=""
    __INUSE=0

    def __init__ (self, INN,PASSWORD,SECRET,INUSE):
        self.__INN=INN
        self.__PASSWORD=PASSWORD
        self.__CLIENT_SECRET=SECRET
        self.__INUSE=INUSE


    def Use(self):
        self.__INUSE+=1;
        return self

    def GetINN(self)->str:
        return self.__INN

    def GetPASS(self)->str:
        return self.__PASSWORD

    def GetSEC(self)->str:
        return self.__CLIENT_SECRET

    def GetUSE(self)->int:
        return self.__INUSE

    def ZeoUse(self):
        self.__INUSE=0

    def CodeMe(self):
        return (self.__INN,self.__PASSWORD, self.__CLIENT_SECRET, self.__INUSE)


class MyDataMass:
    __Data=list()

    def append(self, value):
        self.__Data.append(value)

    def size(self)->int:
        return len(self.__Data)

    def GetI(self, i):
        return self.__Data[i]

    def CodeMe(self):
        ret=list()
        for one in self.__Data:
            ret.append(one.CodeMe())
        return ret

    def UnCodeData(self, data):
        self.__Data=list()
        for one in data:
            self.__Data.append(MyData(one[0],one[1], one[2], one[3]))

    def ZeroUse(self):
        for one in self.__Data:
            one.ZeoUse()