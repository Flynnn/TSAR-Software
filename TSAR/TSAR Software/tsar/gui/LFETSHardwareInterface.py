#################
# UNTESTED CODE #
#################
#Written by Georges Oates Larsen

#(Mostly) Abstract class defining what constitutes a completed LETS hardware interface.
#Some basic functions, such as personnel-type hardare, and general accessors are pre-defined.
#We will implement this twice times:
#Firstly, to define a simulated LFETs for testing.
#Secondly, to define actual hardware interfaces on RPI.

#This file essentially contains low-level hardware commands. We'll implement a separate interface for high-level commands,
#Which we'll use in the network protocol and the GUI. More on that later.


from abc import ABC, abstractmethod
class LFETSHardwareInterface(ABC):

	def __init__(self):
		self.fuelTankFul = False
		self.loxTankFul = False
		self.personnelEvacuated = False

	##############
	### Valves ###
	##############
	
	def SetAllValvesOpen(self, open):
		self.SetValveOpen("58.1", open)
		self.SetValveOpen("42.1", open)
		self.SetValveOpen("9.3", open)
		self.SetValveOpen("9.2", open)
		self.SetValveOpen("49.1", open)
		self.SetValveOpen("49.2", open)
	
	def SetValveOpen(self, valve, open):
		if (valve == "58.1"):
			return self.SetValveOpen58_1(open)
		elif (valve == "42.1"):
			return self.SetValveOpen42_1(open)
		elif (valve == "9.3"):
			return self.SetValveOpen9_3(open)
		elif (valve == "9.2"):
			return self.SetValveOpen9_2(open)
		elif (valve == "49.1"):
			return self.SetValveOpen49_1(open)
		elif (valve == "49.2"):
			return self.SetValveOpen49_2(open)
		elif (valve == "9.1"):
			return self.SetValveOpen9_1(open)
		else:
			raise LookupError("Bad Valve Identifier: " + str(valve))
	
	def GetValveOpen(self, valve):
		if (valve == "58.1"):
			return self.GetValveOpen58_1()
		elif (valve == "42.1"):
			return self.GetValveOpen42_1()
		elif (valve == "9.3"):
			return self.GetValveOpen9_3()
		elif (valve == "9.2"):
			return self.GetValveOpen9_2()
		elif (valve == "49.1"):
			return self.GetValveOpen49_1()
		elif (valve == "49.2"):
			return self.GetValveOpen49_2()
		elif (valve == "9.1"):
			return self.GetValveOpen9_1()
		else:
			raise LookupError("Bad Valve Identifier: " + str(valve))
	
	#Should set valve to open if open true, and vice versa.
	@abstractmethod
	def SetValveOpen58_1(self, open):
		pass
	#Should return boolean indicating if valve is open.
	@abstractmethod
	def GetValveOpen58_1(self):
		pass
	
	#Should set valve to open if open true, and vice versa.
	@abstractmethod
	def SetValveOpen42_1(self, open):
		pass
	#Should return boolean indicating if valve is open.
	@abstractmethod
	def GetValveOpen42_1(self):
		pass
	
	#Should set valve to open if open true, and vice versa.
	@abstractmethod
	def SetValveOpen9_3(self, open):
		pass
	#Should return boolean indicating if valve is open.
	@abstractmethod
	def GetValveOpen9_3(self):
		pass
	
	
	#Should set valve to open if open true, and vice versa.
	@abstractmethod
	def SetValveOpen9_2(self, open):
		pass
	#Should return boolean indicating if valve is open.
	@abstractmethod
	def GetValveOpen9_2(self):
		pass
	
	
	#Should set valve to open if open true, and vice versa.
	@abstractmethod
	def SetValveOpen49_1(self, open):
		pass
	#Should return boolean indicating if valve is open.
	@abstractmethod
	def GetValveOpen49_1(self):
		pass
		
	#Should set valve to open if open true, and vice versa.
	@abstractmethod
	def SetValveOpen49_2(self, open):
		pass
	#Should return boolean indicating if valve is open.
	@abstractmethod
	def GetValveOpen49_2(self):
		pass	
		
	#Should set valve to open if open true, and vice versa.
	@abstractmethod
	def SetValveOpen9_1(self, open):
		pass
	#Should return boolean indicating if valve is open.
	@abstractmethod
	def GetValveOpen9_1(self):
		pass
		
	#TODO: Need full list of valves.
	
	################
	### Pressure ###
	################
	
	def GetPressure(self, transducer):
		if (transducer == "4.1"):
			return self.GetPressure4_1()
		elif (transducer == "4.2"):
			return self.GetPressure4_2()
		elif (transducer == "4.3"):
			return self.GetPressure4_3()
		elif (transducer == "4.4"):
			return self.GetPressure4_4()
		elif (transducer == "4.5"):
			return self.GetPressure4_5()
		else:
			raise LookupError("Bad Pressure Transducer Identifier: " + str(transducer))
	
	#Should return (Float): (Pressure)	
	@abstractmethod
	def GetPressure4_1(self):
		pass
	
	#Should return (Float): (Pressure)	
	@abstractmethod
	def GetPressure4_2(self):
		pass
	
	#Should return (Float): (Pressure)	
	@abstractmethod
	def GetPressure4_3(self):
		pass
		
	#Should return (Float): (Pressure)	
	@abstractmethod
	def GetPressure4_4(self):
		pass
	
	#Should return (Float): (Pressure)	
	@abstractmethod
	def GetPressure4_5(self):
		pass
		
	#TODO: Need full list of pressure transducers.
	#TODO: Should nominal be calibrated for each pressure valve on command? Or use pre-programmed values?
	
	###################
	### Temperature ###
	###################
	
	def GetTemperature(self, thermometer):
		if (thermometer == "43.1"):
			return self.GetTemperature43_1()
		elif (thermometer == "43.2"):
			return self.GetTemperature43_2()
		elif (thermometer == "43.3"):
			return self.GetTemperature43_3()
		elif (thermometer == "43.X"):
			return self.GetTemperature43_X()
		else:
			raise LookupError("Bad Thermometer Identifier: " + str(thermometer))
	
	#Should return (Float): (Temperature)
	@abstractmethod
	def GetTemperature43_1(self):
		pass
	
	#Should return (Float): (Temperature)
	@abstractmethod
	def GetTemperature43_2(self):
		pass

	#Should return (Float): (Temperature)
	@abstractmethod
	def GetTemperature43_3(self):
		pass
	
	#Should return (Float): (Temperature)
	@abstractmethod
	def GetTemperature43_X(self):
		pass
		
	#TODO: Need full list of thermometers.
	
	
	###############
	### MISC ###
	###############
	
	#Should turn on or turn off the spark igniter according to whether "on" True or False.
	@abstractmethod
	def SetSparkIgniter(self, on):
		pass
		
	##############
	### SERVOS ###
	##############
	
	def SetServo(self, servo, value):
		if (valve == "68.1"):
			return self.SetServo68_1(value)
		elif (valve == "69.1"):
			return self.SetServo69_1(value)
		else:
			raise LookupError("Bad Servo Identifier: " + str(valve))
	
	def GetServo(self, servo):
		if (servo == "68.1"):
			return self.GetServo68_1()
		elif (servo == "69.1"):
			return self.GetServo69_1()
		else:
			raise LookupError("Bad Servo Identifier: " + str(valve))
	
	#Should set servo to value
	@abstractmethod
	def SetServo68_1(self, value):
		pass
	#Should return current servo value
	@abstractmethod
	def GetServo69_1(self):
		pass

	#TODO: Need full list of servos.
	
	#################
	### Personnel ###
	#################
	
	def PersonnelConfirmFuelTankFull(self, confirm):
		self.fuelTankFull = confirm
	
	def GetFuelTankFull(self):
		return self.fuelTankFull
		
	def PersonnelConfirmLOXTankFull(self, confirm):
		self.loxTankFull = confirm
	
	def GetLOXTankFull(self):
		return self.loxTankFull
	
	def PersonnelConfirmEvacuation(self, confirm):
		self.personnelEvacuated = confirm
	
	def GetPersonnelEvacuated(self):
		return self.personnelEvacuated
	
	