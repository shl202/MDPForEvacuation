from MDP import MDP
from MapLoader import MapLoader
from LEDConfiguration import LEDConfiguration


maploader = MapLoader()
map = maploader.loadFromFile("EBU3F3_SIMPLE.txt")
reward = 1.0
penalty  = -1.0
gamma = 0.9925 # learning rate of mdp

map.show()
while True:
	var = input("Please enter command: ")


	if var.lower() == "exit":
		print("Thank you for using this product. Stay safe!")
		break
		
	elif var.lower() == "reset":
		map.reset()
		print("Map has been reseted")
		map.show()
		continue
	
	else:
		try:
			c, y, x = var.split()
		except ValueError:
			print("Invalid Command.")
			continue
			
		if c.lower() == "gunner" or c.lower() == "gunshot":
			print("Gunshot detected at position " + str(y) + " " + str(x) )
			if not map.isEmpty((int(y), int(x))):
				print("Invalid gunner position")
				continue
				
			map.addGunner([int(y), int(x)], 0.9)
			#map.addGunner([3, 4], 0.9)
			#map.printMap()

			
		elif c.lower() == "reward":
			if not float(x) > 0:
				print("Invalid Reward. Reward must be a Positive value.")
			reward = float(x)
			print("Reward has been changed to " + str(x))
			
		elif c.lower() == "penalty":
			if not float(x) <0:
				print("Invalid Penalty. Penalty must be a negative value.")
			penalty = float(x)
			print("Penalty has been changed to " + str(x))
			
		elif c.lower() == "learningrate" or "gamma":
			if not (float(x) > 0 and float(x) <= 1):
				print("Invalid Learning Rate. Learning Rate must be between 0 and 1")
			gamma = float(x)
			print("Learning Rate has been changed to " + str(x))
			
		else:
			print("Invalid Command.")
			continue
		
		mdp = MDP(map, reward, penalty, gamma)
		policies, values = mdp.value_iteration()
		mdp.show(values)
		mdp.show(policies, policy=True)
		
		ledc = LEDConfiguration(map)
		ledstates = ledc.policyToLEDStates(policies)
		print(ledstates)
		
		statesString = ""
		for state in ledstates:
			statesString += str(state)

		LEDStatesFile = open("ledstates.txt", "w")
		LEDStatesFile.write(statesString)
		LEDStatesFile.close()
		
	
