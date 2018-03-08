import string
import re
from Map import Map

class MapLoader:
	def __init__(self):
		self.width_ = 0
		self.height_ = 0
		
	def loadFromFile(self, filename):
		file = open(filename, "r")
		header = ""
		while(True):
			header = file.readline()
			if header in ["\n", "\r\n"]:
				continue 
			elif header[0] == "c":
				continue 
			else:
				break

		dimensions = header.split(" ")
		self.height_ = int(dimensions[0])
		self.width_ = int(dimensions[1])
		lineNum = 0
		cells = []
		
		while lineNum < self.height_:
			line = file.readline()
			cells.append(list(line.rstrip()))
			lineNum += 1
		
		return Map(self.height_, self.width_, cells)
