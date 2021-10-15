import json
import random

from myData import MyDataMass, MyData


class Jwork:

    def __init__(self):
        self.data = MyDataMass()
        self.enduse = 2
        self.lastuse = None

    # Сохранить текущий словарь
    def saveDict(self):
        with open("fns_info.json", "w") as write_file:
            json.dump(self.data.CodeMe(), write_file, indent=4)

    # Вернуть словарь под номером r, причём только инн, пароль и секретное поле
    def partDickt(self, r):
        return self.data.GetI(r)

    # Добавить в json новые данные
    def saveNewData(self, inn, password, client_secret):
        self.loadDict()
        self.data.append(MyData(inn, password, client_secret, 0))
        self.saveDict()

    # Некоторые тестовые значения(потом изменить)
    def testData(self):
        self.saveNewData(111, 'qwerty', 'vegan')
        self.saveNewData(222, 'asdfgh', 'ne vegan')

    # Загрузить словарь из json
    def loadDict(self):
        with open("fns_info.json", "r") as read_file:
             self.data.UnCodeData(json.load(read_file))

    # Получить словарь с данными для установления соединения. Если такого нет, то вернуть None
    def getInf(self) -> MyData:
        if (self.lastuse == None):
            self.lastuse = self.getCanUse()
        elif (self.tryToUse() != True):
            self.lastuse = self.getCanUse()
            return self.getInf()

        if (self.lastuse == None):
            return None
        self.data.GetI(self.lastuse).Use()
        self.saveDict()
        return self.data.GetI(self.lastuse)

    # Проверка, можно ли ещё использовать последний выбранный набор
    def tryToUse(self) -> bool:
        r = self.lastuse
        if (self.data.GetI(r).GetUSE() >= self.enduse):
            return False
        return True

    # Получение номера набора, который можно использовать. Если такого нет, то вернуть None
    def getCanUse(self) -> int:
        self.loadDict()
        myhave = list()
        r = (random.randrange(0, self.data.size(), 1))
        donow = True
        while (self.data.GetI(r).GetUSE() >= self.enduse and donow):
            myhave.append(r)
            myhave = list(set(myhave))
            if (len(myhave) == self.data.size()):
                donow = False
            r = (random.randrange(0, self.data.size(), 1))

        if (donow):
            return r
        return None

    # Обнулить количество использований
    def zeroedUse(self):
        self.loadDict()
        self.data.ZeroUse()
        self.saveDict()

    # Обнулить количество использований всех данных
    def doEmpty(self):
        self.data = MyDataMass()
        self.saveDict()