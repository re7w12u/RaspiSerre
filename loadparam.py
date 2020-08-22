import json
import sys




class Param(object):

	path = '/opt/linear-actuator/param.json'
	
	def __init__(self):
		with open(self.path, 'r') as f:
			self.__dict__ = json.load(f)



<<<<<<< HEAD
	def Save(self, p):
		pass



=======
>>>>>>> b5bad87a72bc654c73c7fe1ab9cc9ada9751aab0


