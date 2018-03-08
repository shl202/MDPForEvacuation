from Map import Map

class LEDConfiguration:
	def __init__(self, map):
		self.map_ = map
		self.ledStates_ = []
		self.actions_ = [0, 1, 2, 3]
		self.actions_id_ = { 'W':0, 'N':1, 'E':2, 'S':3 }

		
	def policyToLEDStates(self, policy):
		ledID = 0
		for r, row in enumerate(self.map_.getCells()):
			for c, cell in enumerate(row):
				s = [r, c]
				if cell == "W" or cell == "E":
					continue

				for a in self.actions_:
					if not self.has_next_state(s, a):
						continue
					
					ns = self.next_state(s, a)
					if self.map_.isWall(ns):
						continue
					
					ledState = 0
					if policy[r][c] == a:
						ledState = 1
					else:
						ledState = 0
					self.ledStates_.append( ledState)
					ledID += 1
					
		return(self.ledStates_)
						
						
					
					
					
	def has_next_state(self, s, a):
		width = self.map_.getWidth()
		height = self.map_.getHeight()
		y, x = s
		if a == 0 and ( x == 0 ):
			return False
		elif a == 1 and ( y == 0 ):
			return False
		elif a == 2 and ( x == (width - 1) ):
			return False
		elif a == 3 and ( y == (height - 1)):
			return False
		else:
			return True
			
	def next_state(self, s, a):
		y, x = s
		if a == 0:
			return (y, x-1)
		elif a == 1:
			return (y-1, x)
		elif a == 2:
			return (y, x+1)
		else:
			return (y+1, x)