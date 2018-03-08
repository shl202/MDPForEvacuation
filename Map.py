class Map:
	def __init__(self, height, width, cells):
		self.height_ = height
		self.width_ = width
		self.cells_ = cells
		self.probNorth_ = dict()
		self.probSouth_ = dict()
		self.probWest_ = dict()
		self.probEast_ = dict()
		
	
	def __str__(self):
		str = ""
		for row in self.cells_:
			str = str + "".join(row) + "\n"	
		return str

	def add(self, object, position):
		if not self.isEmpty(position):
			return False
		y, x = position[0], position[1] 
		self.cells_[y][x] = object

	def getCells(self):
		return self.cells_
	
	def getCell(self, position):
		y, x = position
		if(self.inbound(position)):
			return self.cells_[y][x]
		else:
			return 'X'
	
	def getHeight(self):
		return self.height_
		
	def getWidth(self):
		return self.width_
	
	def getSize(self):
		return [self.height_, self.width_]
		
	def isEmpty(self, position):
		if not self.inbound(position):
			return False
		y, x = position[0], position[1]	
		if self.cells_[y][x] == " ":
			return True
		else:
			return False
			
	def isWall(self, position):
		if not self.inbound(position):
			return True # Assume everything outside the map are walls for mdp
		y, x = position[0], position[1]
		if self.cells_[y][x] == "W" or self.cells_[y][x] == "w":
			return True
		else:
			return False		
		
	def inbound(self, position):
		y, x = position[0], position[1]
		if y < 0 or y >= self.height_:
			return False
		if x < 0 or x >= self.width_:
			return False
		return True
	
	def to1D(self, y, x):
		return y * self.getWidth() + x
	
	def printMap(self):
		print(self)
		
	def addGunner(self, position, dangerRate):
		if not self.isEmpty(position):
			return False
		y, x = position[0], position[1] 
		self.cells_[y][x] = "G"
		self.updateStatesProb(position, dangerRate)
	
	def updateStatesProb(self, positionGunner, dangerRate):
		yG, xG = positionGunner
		
		boundup = yG - 1
		bounddown = yG + 1
		boundleft = xG - 1
		boundright = xG + 1
		
		while True:
			if self.isWall([boundup, xG]):
				break
			boundup -= 1
		
		while True:
			if self.isWall([bounddown, xG]):
				break
			bounddown += 1
		
		while True:
			if self.isWall([yG, boundleft]):
				break
			boundleft -= 1
			
		while True:
			if self.isWall([yG, boundright]):
				break
			boundright += 1
		
		for r, row in enumerate(self.cells_):
			for c, cell in enumerate(row):

				if not self.isEmpty([r, c]):
					continue
					
				if r > boundup and r < bounddown and c > boundleft and c < boundright:
					self.updateStateProb(positionGunner, [r, c], dangerRate)
		
		#print(self.probNorth_)
		
		
	def updateStateProb(self, positionGunner, positionCur, dangerRate):
		yG, xG = positionGunner
		yC, xC = positionCur
		sG = self.to1D(yG, xG)
		sC = self.to1D(yC, xC)
		sCN = self.to1D(yC-1, xC)
		sCS = self.to1D(yC+1, xC)
		sCW = self.to1D(yC, xC-1)
		sCE = self.to1D(yC, xC+1)
		if abs(yC - yG) >= abs(xC - xG):  
			if (yC - yG) > 0:
				self.probNorth_[(sC, sCN)] = 1
				
				self.probWest_[(sC, sCN)] = dangerRate
				self.probWest_[(sC, sCW)] = 1 - dangerRate
				
				self.probSouth_[(sC, sCN)] = dangerRate
				self.probSouth_[(sC, sCS)] = 1 - dangerRate
				
				self.probEast_[(sC, sCN)] = dangerRate
				self.probEast_[(sC, sCE)] = 1 - dangerRate
			else:
				self.probSouth_[(sC, sCS)] = 1
				
				self.probWest_[(sC, sCS)] = dangerRate
				self.probWest_[(sC, sCW)] = 1 - dangerRate
				
				self.probNorth_[(sC, sCS)] = dangerRate
				self.probNorth_[(sC, sCN)] = 1 - dangerRate
				
				self.probEast_[(sC, sCS)] = dangerRate
				self.probEast_[(sC, sCE)] = 1 - dangerRate
			
		
		else: 
			if (xC - xG) > 0:
				self.probWest_[(sC, sCW)] = 1
				
				self.probNorth_[(sC, sCW)] = dangerRate
				self.probNorth_[(sC, sCN)] = 1 - dangerRate
				
				self.probSouth_[(sC, sCW)] = dangerRate
				self.probSouth_[(sC, sCS)] = 1 - dangerRate
				
				self.probEast_[(sC, sCW)] = dangerRate
				self.probEast_[(sC, sCE)] = 1 - dangerRate
				
			else:
				self.probEast_[(sC, sCE)] = 1
				
				self.probNorth_[(sC, sCE)] = dangerRate
				self.probNorth_[(sC, sCN)] = 1 - dangerRate
				
				self.probSouth_[(sC, sCE)] = dangerRate
				self.probSouth_[(sC, sCS)] = 1 - dangerRate
				
				self.probWest_[(sC, sCE)] = dangerRate
				self.probWest_[(sC, sCW)] = 1 - dangerRate
			
				
	def reset(self):
		for r, row in enumerate(self.cells_):
			for c, cell in enumerate(row):
				if cell == "G":
					self.cells_[r][c] = " "
					
		self.probNorth_ = dict()
		self.probSouth_ = dict()
		self.probWest_ = dict()
		self.probEast_ = dict()
		
	def show(self):
		print(self)
		
		
		
		