import Adafruit_DHT
import time
import os
import loadparam
import GHManager as GHM
import requests
import LAManager


DHT_SENSOR = Adafruit_DHT.AM2302
DHT_PIN = 4


# pull latest measure from csv file
def GetLatestMeasure():
	param = loadparam.Param()
	with open(param.TemperatureDataFile) as f:
		return f.readlines()[-1]

# called by AM2302.service on a regular basis (see AM2302.timer)
def CheckSensor():
	try:
		hum, temp = MakeNewMeasure()
		SaveNewMeasure(temp, hum)
		CheckGreenHouseTemperature(temp)
	except Exception as e:
		with open(param.ErrorFilePath,'a+') as f:
			f.write('{0} - {1} - {2}\r\n'.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M:%S') ,str(e)))

# check temperature to keep green house not too warm, not too cold
def CheckGreenHouseTemperature(temp):
	param = loadparam.Param()
	isClosed = GHM.GetDoorPosition() == GHM.Position.CLOSED
	# it's getting warmer and it's still closed => open the greenhouse
	print("isClosed={0}".format(isClosed))
	print("temp={0} (type={1})".format(temp,type(temp)))
	print("treshold={0}".format(param.TemperatureTreshold))
	if(temp > float(param.TemperatureTreshold) and isClosed):		
	#requests.get('http://localhost:8081/move/{0}/{1}'.format(param.Open["GPIO"], param.Open["duration"]))
		print("open")
		lam = LAManager.LAManager()
		lam.Open()
		
	# it's getting colder and it's still opened => close the greenhouse
	elif(temp < float(param.TemperatureTreshold) and not isClosed):
		#requests.get('http://localhost:8081/move/{0}/{1}'.format(param.Close["GPIO"], param.Close["duration"]))
		print("close")
		lam = LAManager.LAManager()
		lam.Close()

# get new measure from sensor
def MakeNewMeasure():
	hum, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
	if hum is None and temp is None:
		raise Exception('{0},{1},{2}\r\n'.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M'), "Failed to retrieve data from humidity sensor"))
	return hum, temp

# save data to csv file
def SaveNewMeasure(hum, temp):
	param = loadparam.Param()
	#print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temp,hum))
	with open(param.TemperatureDataFile,'a+') as f:
		f.write('{0},{1},{2:0.1f},{3:0.1f}\r\n'.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M:%S'), temp, hum))


