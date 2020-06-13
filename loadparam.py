import json
import sys




class Param(object):

	path = '/opt/linear-actuator/param.json'
	
	def __init__(self):
		with open(self.path, 'r') as f:
			self.__dict__ = json.load(f)





