import sys
from time import sleep
import loadparam
import RPi.GPIO as GPIO
from LogManager import LogManager



# Linear Actuator Manager
class LAManager():

    def __init__(self):        
        self.__param = loadparam.Param()
        self.__logger = LogManager()
        self.__error_code = "2x"

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.__param.Open["GPIO"], GPIO.OUT)
        GPIO.setup(self.__param.Close["GPIO"], GPIO.OUT)

        GPIO.output(self.__param.Open["GPIO"],GPIO.LOW) 
        GPIO.output(self.__param.Close["GPIO"],GPIO.LOW) 


    def Open(self):
        self.__Move(self.__param.Open)


    def Close(self):        
        self.__Move(self.__param.Close)


    def SavePosition(self, pos):
        try :
            with open(self.__param.PositionFile,'r+') as f:
                f.seek(0)
                f.write(str(pos))
        except Exception as e:
            self.__logger.Err("something bad just happened while trying to save position in position.txt", self.__error_code + '1')
            self.__logger.Err(e, self.__error_code + '1')


    def __Move(self, param):
        try:            
            gpio = param["GPIO"]
            duration = param["duration"]
            pos = param["position"]

            GPIO.output(gpio,GPIO.HIGH)            
            sleep(int(duration) / 1000)            
            GPIO.output(gpio,GPIO.LOW)        
            
            self.SavePosition(pos)
            self.__logger.Log("switching gpio {0} for {1} ms".format(gpio, duration))
        except Exception as e:
            print(e)
            self.__logger.Err("error while moving linear actuator gpio={0} duration={1} ms - see error below for more info".format(gpio, duration),  self.__error_code + '2')
            self.__logger.Err(e,  self.__error_code + '2')
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
        print("wrong parameter : argument should be 'open' or 'close'")