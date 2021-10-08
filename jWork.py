import json
import random


class Jwork:
    #Ключевые слова для словаря
    shtamp = ['INN', 'PASSWORD', 'CLIENT_SECRET', 'INUSE']

    def __init__(self):
        self.i = 0
        self.data=dict()
        self.enduse=1
        self.lastuse=None

    #Сохранить текущий словарь
    def saveDict(self):
        with open("fns_info.json", "w") as write_file:
            json.dump(self.data, write_file, indent=4)

    #Создать словарь с иннн, поролем и секрктным полем
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

    #Добавть одно использование к набору данных под номерои r
    def addUse(self,r):
        return {r: {
                str(self.shtamp[0]): self.data.setdefault(r).setdefault(self.shtamp[0]),
                self.shtamp[1]: self.data.setdefault(r).setdefault(self.shtamp[1]),
                self.shtamp[2]: self.data.setdefault(r).setdefault(self.shtamp[2]),
                self.shtamp[3]: int(self.data.setdefault(r).setdefault(self.shtamp[3]))+1
            }
        }

    #Обнулить количество использований набора r
    def zeroedOne(self,r):
        return {r: {
                str(self.shtamp[0]): self.data.setdefault(r).setdefault(self.shtamp[0]),
                self.shtamp[1]: self.data.setdefault(r).setdefault(self.shtamp[1]),
                self.shtamp[2]: self.data.setdefault(r).setdefault(self.shtamp[2]),
                self.shtamp[3]: 0
            }
        }

    #Вернуть словарь под номером r, причём только инн, пароль и секретное поле
    def partDickt(self,r):
        return {
            str(self.shtamp[0]): self.data.setdefault(r).setdefault(self.shtamp[0]),
            self.shtamp[1]: self.data.setdefault(r).setdefault(self.shtamp[1]),
            self.shtamp[2]: self.data.setdefault(r).setdefault(self.shtamp[2]),
        }

    #Добавить в json новые данные
    def saveNewData(self, inn,password,client_secret):
        self.loadDict();
        self.data.update(self.doDict(inn,password,client_secret))
        self.saveDict()

    #Некоторые тестовые значения(потом изменить)
    def testData(self):
        self.saveNewData(111, 'qwerty', 'vegan')
        self.saveNewData(222, 'asdfgh', 'ne vegan')

    #Загрузить словарь из json
    def loadDict(self):
        with open("fns_info.json", "r") as read_file:
            self.data = json.load(read_file)
        self.i=len(self.data)

    #Получить словарь с данными для установления соединения. Если такого нет, то вернуть None
    def getInf(self)->dict:
        self.lastuse=self.getCanUse()
        if(self.lastuse==None):
            return None
        return self.partDickt(self.lastuse)

    #Проверка, можно ли ещё использовать последний выбранный набор
    def tryToUse(self)->bool:
        r=self.lastuse
        if(int(self.data.setdefault(r).setdefault(self.shtamp[3])) >= self.enduse ):
            return False
        self.data.update(self.addUse(r))
        self.saveDict()
        return True

    #Получение номера набора, который можно использовать. Если такого нет, то вернуть None
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

    #Обнулить количество использований
    def zeroedUse(self):
        self.loadDict()

        for j in range(self.i):
            self.data.update(self.zeroedOne(str(j+1)))
        self.saveDict()

    #Обнулить количество использований всех данных
    def doEmpty(self):
        self.data=dict()
        self.saveDict()