<<<<<<< HEAD
import sys
import time
import loadparam
import RPi.GPIO as GPIO
from LogManager import LogManager


# Linear Actuator Manager
class LAManager():

    def __init__(self):        
        self.__param = loadparam.Param()
        self.__logger = LogManager()

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.__param.Open["GPIO"], GPIO.OUT)
        GPIO.setup(self.__param.Close["GPIO"], GPIO.OUT)


    def Open(self):
        self.__Move(self.__param.Open)


    def Close(self):        
        self.__Move(self.__param.Close)


    def SavePosition(self, pos):
        try :
            with open(self.__param.PositionFile,'r+') as f:
                f.seek(0)
                f.write(pos)
        except :
            self.__logger.Err("something bad just happened while trying to save position in position.txt")


    def __Move(self, param):
        try:            
            gpio = param["GPIO"]
            duration = param["duration"]
            pos = param["position"]

            print("gpio {0} for {1} ms".format(gpio, duration))
            print("value={0}".format(GPIO.input(gpio)))
            GPIO.output(gpio,GPIO.HIGH)
            print("set to HIGH - sleeping...")
            time.sleep(duration / 1000)
            print("waking up...")
            GPIO.output(gpio,GPIO.LOW)        
            print("set to LOW - done.")

            self.SavePosition(pos)
            self.__logger.Log("switching gpio {0} for {1} ms".format(gpio, duration))
        except:
            self.__logger.Err("error while moving linear actuator gpio={0} duration={1} ms".format(gpio, duration))
        finally:
            GPIO.cleanup()


if __name__ == "__main__":    
    args = sys.argv
    lam = LAManager()
    method = args[1]
    if method == "open":
        lam.Open()
    elif method == "close":
        lam.Close()
    else:        
=======
import sys
import time
import loadparam
import RPi.GPIO as GPIO
from LogManager import LogManager


# Linear Actuator Manager
class LAManager():

    def __init__(self):        
        self.__param = loadparam.Param()
        self.__logger = LogManager()

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.__param.Open["GPIO"], GPIO.OUT)
        GPIO.setup(self.__param.Close["GPIO"], GPIO.OUT)


    def Open(self):
        self.__Move(self.__param.Open)


    def Close(self):        
        self.__Move(self.__param.Close)


    def SavePosition(self, pos):
        try :
            with open(self.__param.PositionFile,'r+') as f:
                f.seek(0)
                f.write(pos)
        except :
            self.__logger.Err("something bad just happened while trying to save position in position.txt")


    def __Move(self, param):
        try:            
            gpio = param["GPIO"]
            duration = param["duration"]
            pos = param["position"]

            print("gpio {0} for {1} ms".format(gpio, duration))
            print("value={0}".format(GPIO.input(gpio)))
            GPIO.output(gpio,GPIO.HIGH)
            print("set to HIGH - sleeping...")
            time.sleep(duration / 1000)
            print("waking up...")
            GPIO.output(gpio,GPIO.LOW)        
            print("set to LOW - done.")

            self.SavePosition(pos)
            self.__logger.Log("switching gpio {0} for {1} ms".format(gpio, duration))
        except:
            self.__logger.Err("error while moving linear actuator gpio={0} duration={1} ms".format(gpio, duration))
        finally:
            GPIO.cleanup()


if __name__ == "__main__":    
    args = sys.argv
    lam = LAManager()
    method = args[1]
    if method == "open":
        lam.Open()
    elif method == "close":
        lam.Close()
    else:        
>>>>>>> b5bad87a72bc654c73c7fe1ab9cc9ada9751aab0
        print("wrong parameter : argument should be 'open' or 'close'")