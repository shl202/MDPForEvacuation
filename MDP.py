#!/usr/bin/env python
import sys
from sys import argv
import numpy as np
import string
from numpy import *
from Map import Map

class MDP:
	def __init__(self, map, rewardValue=1.0, penaltyValue=-1.0, gamma=0.9925):
		self.map_ = map
		self.numStates_ = map.getHeight() * map.getWidth()
		self.numActions_ = 4
		
		self.rewardValue_ = rewardValue
		self.penaltyValue_ = penaltyValue
		self.gamma_ = gamma
		
		self.numIt_ = self.numStates_
		self.stop_threshold_ = 0.00001

		self.rewards_ = []
		for row in map.getCells():
			for cell in row:
				if cell == "E":
					self.rewards_.append(self.rewardValue_)
				elif cell == "G":
					self.rewards_.append(self.penaltyValue_)
				else:
					self.rewards_.append(0.0)
		
					
		#self.rewardsLines = rewardsFile.readlines()
		#self.rewards = [ int(n.strip('\n')) for n in rewardsLines ]

		self.actions_ = ['<', '^', '>', 'v']
		self.actions_id_ = { 'W':0, 'N':1, 'E':2, 'S':3 }
		self.V_OFFSET_ = map.getWidth()
		self.H_OFFSET_ = 1

	'''
	# loading input files
	def sparse_to_dict(m):
		d = dict()
		for v in m:
			d[(v[0]-1,v[1]-1)] = v[2]
			
		return d
		
	def file_to_list( file ):
		lines = file.readlines()
		lists = [ n.strip('\n').split('  ') for n in lines ]
		return [ [int(p[0]), int(p[1]), float(p[2])] for p in lists ]


	cpt = [ 
		sparse_to_dict(file_to_list( p1File )), 
		sparse_to_dict(file_to_list( p2File )), 
		sparse_to_dict(file_to_list( p3File )), 
		sparse_to_dict(file_to_list( p4File ))]
	'''
		
	
	# helpers for mdp computation and visualization		
	def show(self, map, policy=False):
		#format np output to 2 decimal places
		np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
		height = self.map_.getHeight()
		width = self.map_.getWidth()
		toDisplay = []
		print('\n')
		if policy == True:
			#print(map)
			toDisplay = []
			for r, row in enumerate(map):
				toDisplay.append([])
				for c, cell in enumerate(row):
					if self.map_.isEmpty([r,c]):
						toDisplay[r].append(self.actions_[cell])
					else:
						toDisplay[r].append(self.map_.getCell([r,c]))
				#toDisplay.append(rowDisplay)
			print(np.array(toDisplay)) 
		else:
			#if type(map[0][0]) is float64: 
			#	print(np.array([[int(1000*m)/1000 for m in row] for row in map]))
			#else:
			print(np.array(map))
		print('\n')
		
	def to2D(self, s):
		y = int(s/self.map_.getWidth())
		x = s % self.map_.getWidth()
		return [y, x]
	
	def to1D(self, x, y):
		return y * self.map_.getWidth() + x
	
	def diff(self, l1, l2):
		return sum([abs(d) for d in (np.array(l1) - np.array(l2))])
	
	def has_next_state(self, s, a):
		width = self.map_.getWidth()
		height = self.map_.getHeight()
		
		if a == 0 and ( (s % width) == 0):
			return False
		elif a == 1 and ( int(s / width) == 0):
			return False
		elif a == 2 and ((s % width) == (width - 1) ):
			return False
		elif a == 3 and (int(s / width) == (height - 1)):
			return False
		else:
			return True
		
		
	def next_state(self, s, a):
		if a == 0:
			return s - self.H_OFFSET_
		elif a == 1:
			return s - self.V_OFFSET_
		elif a == 2:
			return s + self.H_OFFSET_
		else:
			return s + self.V_OFFSET_
	
		
	def probability(self, s, sp, a):
		prob = 0;
		
		if a == 0:
			prob = self.map_.probWest_.get((s, sp), -1)
		elif a == 1:
			prob = self.map_.probNorth_.get((s, sp), -1)
		elif a == 2:
			prob = self.map_.probEast_.get((s, sp), -1)
		else:
			prob = self.map_.probSouth_.get((s, sp), -1)
		
		
		#return cpt[a].get((s, sp), 0)
		#assuming no drift as of now
		#return 0.25
		if prob == -1:
			if (self.next_state(s, a) == sp):
				return 1.0
			else: 
				return 0
		return prob

			
	def action_value(self, s, a, v):
		value = 0
		if not self.map_.isEmpty(self.to2D(s)):
			return value

		for possible_action in range(self.numActions_):
			if self.has_next_state(s, possible_action):
				sp = self.next_state(s, possible_action)
				if self.map_.isWall(self.to2D(sp)):
					value += self.probability(s, sp, a) * v[s]
				else:
					value += self.probability(s, sp, a) * v[sp]
					
		return value
		
	def max_policy(self, s, v):	
		return max( [ self.action_value(s, a, v) for a in range(self.numActions_)] ) 

	def argmax_policy(self, s, v):
		return argmax( [ self.action_value(s,a,v) for a in range(self.numActions_)] )
			
	def value_iteration(self):
		#print(self.rewards_)
		v0 = 0
		v = np.array([v0]* self.numStates_)
		#print(v)
		vp = v
		for it in range(self.numIt_):
			v = np.array(self.rewards_) + self.gamma_ * np.array([ self.max_policy(s, v) for s in range(self.numStates_) ])
			if it % 1 == 0:
				#print( "iteration %i" % it)
				if self.diff(v, vp) < self.stop_threshold_:
					break
				vp = v
				
		plc = np.array([ self.argmax_policy(s, v) for s in range(self.numStates_) ])
		
		height = self.map_.getHeight()
		width = self.map_.getWidth()
		plc = np.reshape(np.array(plc), (height, width))
		v = np.reshape(np.array(v), (height, width))
		return (plc, v)
		
	def policy_iteration():
		v0 = 0
		v = np.array([v0]* self.numStates_)
		vp = v
		plc0 = self.actions_id_[a]
		plc = np.array([plc0]* self.numStates_)
		plcp = plc
		count = 1
		while True:
			# policy evaluation until converge
			for it in range(self.numIt_):
				v = np.array(self.rewards_) + self.gamma_ * np.array([ self.action_value(s, plc[s], v) for s in range(self.numStates_) ])
				#show(v)
				if it % 1 == 0:
					#print( "iteration %i" % it)
					if self.diff(v, vp) < self.stop_threshold_:
						break
					vp = v
			# update policy
			plc = np.array([ self.argmax_policy(s, v) for s in range(self.numStates_) ])
			if self.diff(plc, plcp) == 0:
				break
			else:
				plcp = plc
				count += 1
				
		
		#print("Pi = %s: %i iterations" % (a, count))
		height = self.map_.getHeight()
		width = self.map_.getWidth()
		plc = np.reshape(np.array(plc), (height, width))
		v = np.reshape(np.array(v), (height, width))

		return (plc, v)
