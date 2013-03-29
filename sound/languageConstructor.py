import json
import re

class Language:
	
	def __init__(self, filePath):
		self.filePath = filePath
	
	def testing(self):
		with open(self.filePath) as data:
			getCounter = 0
			postCounter = 0
			JSONCounter = 0
			counter = 0
			for line in data:
				check = self.isCall(line) #returns none if not a call
				if check:
					print check.data
					
			
	def isCall(self, line):
		if re.search(r"\[method\=[A-Z]+\]", line):
			print "Match!"
			data = Call()
			data.castString(line)
			return data
		return None
		
class Call:
	def __init__(self):
		self.data = {}
		
	def castString(self, string):
		params = string.split("][")
		for param in params:
			if "method=" in param:
				self.data["method"] = re.sub(r'^(.*?)(method\=)([A-Z]+)$', r'\3', param)
			elif "status=" in param:
				self.data["status"] = int(re.sub(r'^(status\=)([0-9]+)$', r'\2', param))
			elif "resp_msecs=" in param:
				self.data["responseTime"] = int(re.sub(r'^(resp_msecs\=)([0-9]+)$', r'\2', param))
			elif "resp_bytes=" in param:
				self.data["responseBytes"] = int(re.sub(r'^(resp_bytes\=)([0-9]+)$', r'\2', param))
			elif "req_bytes=" in param:
				self.data["requiredBytes"] = int(re.sub(r'^(req_bytes\=)([0-9]+)(.*?)$',r'\2',param))
		

test = Language("../../filepicker.io.log")
test.testing()
