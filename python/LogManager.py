
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

    def Err(self, msg, error_code):
        self.__Write('[ERR] [{0}] - {1} - {2}'.format(error_code, self.__GetDate(), msg), LogLevel.Error)

    def __Write(self, msg, level):
        with open(self.__param.OutputFilePath, 'a') as f: 
            f.write('{0}\r\n'.format(msg))

    def __GetDate(self):
        return '{0} {1}'.format(date.today().strftime('%d/%m/%Y'), time.strftime('%H:%M:%S'))

