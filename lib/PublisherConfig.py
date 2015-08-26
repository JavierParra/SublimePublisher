import re
import json

class Config:
	confFile = "";
	data = {};

	def __init__(self, path):
		self.confFile = path;
		self.data = self.validateConfig(self.parseConfig(path))

	def parseConfig(self, path):
		handle = open(path)
		placeholder=""
		for line in handle:
			if (re.search('^(?!(\s*//)|\s*$)', line)):
				placeholder += line

		try:
			data = json.loads(placeholder)
		except ValueError:
			 print("Error parsing configuration file. Perhaps you have a trailing coma?");
			 return 0
		
		return data;

	def validateConfig(self, data):
		required = ['host', 'type', 'user', 'remote_path']
		errors = []

		for req in required:
			if not req in data:
				errors.append(req)

		if len(errors) > 0:
			print( "Error: missing required attributes:");
			print (errors)