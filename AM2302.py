import Adafruit_DHT
import time
import os
import loadparam
import GHManager as GHM
import requests


DHT_SENSOR = Adafruit_DHT.AM2302
DHT_PIN = 4
param = loadparam.Param()

# pull latest measure from csv file
def GetLatestMeasure():
	with open(param.TemperatureDataFile) as f:
		return f.readlines()[-1]

# called by AM2302.service on a regular basis (see AM2302.timer)
def CheckSensor():
	try:
		hum, temp = MakeNewMeasure()			
		SaveNewMeasure(temp, hum)
		CheckTemperature(temp)	
	except Exception as e:
		with open(param.ErrorFilePath,'a+') as f:
			f.write(e)

# check temperature to keep green house not too warm, not too cold
def CheckTemperature(temp):
	isClosed = GHM.GetDoorPosition() == GHM.Position.CLOSED
	# it's getting warmer and it's still closed => open the greenhouse
	if(temp > param.TemperatureTreshold and isClosed):
		requests.get('http://localhost:8081/move/{0}/{1}'.format(param.Open["GPIO"], param.Open["duration"]))
	# it's getting colder and it's still opened => close the greenhouse
	elif(temp < param.TemperatureTreshold and not isClosed):
		requests.get('http://localhost:8081/move/{0}/{1}'.format(param.Close["GPIO"], param.Close["duration"]))

# get new measure from sensor
def MakeNewMeasure():
	hum, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
	if hum is None and temp is None:
		raise Exception('{0},{1},{2}\r\n'.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M'), "Failed to retrieve data from humidity sensor")) 
	return hum, temp

# save data to csv file
def SaveNewMeasure(hum, temp):
	if hum is not None and temp is not None:
		#print("Temp={0:0.1f}°C Humidity={1:0.1f}%".format(temp,hum))
		with open(param.TemperatureDataFile,'a+') as f:
			f.write('{0},{1},{2:0.1f},{3:0.1f}\r\n'.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M:%S'), temp, hum))
	else:
		with open(param.ErrorFilePath,'a+') as f:
			f.write('{0},{1},{2}\r\n'.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M'), "Failed to retrieve data from humidity sensor"))


