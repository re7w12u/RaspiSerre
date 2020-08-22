<<<<<<< HEAD

from enum import Enum
from loadparam import Param
from datetime import date
import time



class LogLevel(Enum):
    Info = 1
    Warn = 2
    Error = 3

class LogManager:  

    def __init__(self): 
        self.__param = Param()

    def Log(self, msg):
        self.__Write('[OK] {0} - {1}'.format(self.__GetDate(), msg), LogLevel.Info)

    def Warn(self, msg):
        self.__Write('[WARN] {0} - {1}'.format(self.__GetDate(), msg), LogLevel.Warn)

    def Err(self, msg):
        self.__Write('[ERR] {0} - {1}'.format(self.__GetDate(), msg), LogLevel.Error)

    def __Write(self, msg, level):
        with open(self.__param.ErrorFilePath, 'a') as f: 
            f.write(msg)

    def __GetDate(self):
        return '{0} {1}'.format(date.today().strftime('%d/%m/%Y'), time.strftime('%H:%M:%S'))

=======

from enum import Enum
from loadparam import Param
from datetime import date
import time



class LogLevel(Enum):
    Info = 1
    Warn = 2
    Error = 3

class LogManager:  

    def __init__(self): 
        self.__param = Param()

    def Log(self, msg):
        self.__Write('[OK] {0} - {1}'.format(self.__GetDate(), msg), LogLevel.Info)

    def Warn(self, msg):
        self.__Write('[WARN] {0} - {1}'.format(self.__GetDate(), msg), LogLevel.Warn)

    def Err(self, msg):
        self.__Write('[ERR] {0} - {1}'.format(self.__GetDate(), msg), LogLevel.Error)

    def __Write(self, msg, level):
        with open(self.__param.ErrorFilePath, 'a') as f: 
            f.write(msg)

    def __GetDate(self):
        return '{0} {1}'.format(date.today().strftime('%d/%m/%Y'), time.strftime('%H:%M:%S'))

>>>>>>> b5bad87a72bc654c73c7fe1ab9cc9ada9751aab0
