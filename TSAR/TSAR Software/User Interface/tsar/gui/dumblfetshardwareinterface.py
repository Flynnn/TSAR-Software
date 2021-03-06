from LFETSHardwareInterface import LFETSHardwareInterface
from time import time
from math import sin, cos, tan

class DumbLFETSHardwareInterface(LFETSHardwareInterface):
	
	#Should set valve to open if open true, and vice versa.
	def SetValveOpen58_1(self, open):
		pass
	#Should return boolean indicating if valve is open.
	def GetValveOpen58_1(self):
		pass
	
	#Should set valve to open if open true, and vice versa.
	def SetValveOpen42_1(self, open):
		pass
	#Should return boolean indicating if valve is open.
	def GetValveOpen42_1(self):
		pass
	
	#Should set valve to open if open true, and vice versa.
	def SetValveOpen9_3(self, open):
		pass
	#Should return boolean indicating if valve is open.
	def GetValveOpen9_3(self):
		pass
	
	
	#Should set valve to open if open true, and vice versa.
	def SetValveOpen9_2(self, open):
		pass
	#Should return boolean indicating if valve is open.
	def GetValveOpen9_2(self):
		pass
	
	
	#Should set valve to open if open true, and vice versa.
	def SetValveOpen49_1(self, open):
		pass
	#Should return boolean indicating if valve is open.
	def GetValveOpen49_1(self):
		pass
		
	#Should set valve to open if open true, and vice versa.
	def SetValveOpen49_2(self, open):
		pass
	#Should return boolean indicating if valve is open.
	def GetValveOpen49_2(self):
		pass	
		
	#Should set valve to open if open true, and vice versa.
	def SetValveOpen9_1(self, open):
		pass
	#Should return boolean indicating if valve is open.
	def GetValveOpen9_1(self):
		pass

		#Should return (Float): (Pressure)	
	def GetPressure4_1(self):
		return sin(time()) * 10 + 10
	
	#Should return (Float): (Pressure)	
	def GetPressure4_2(self):
		return cos(time()) * 10 + 10
	
	#Should return (Float): (Pressure)	
	def GetPressure4_3(self):
		return abs(tan(time()/2) * 10)
		
	#Should return (Float): (Pressure)	
	def GetPressure4_4(self):
		return abs(1/tan(time()/10)) + 15
	
	#Should return (Float): (Pressure)	
	def GetPressure4_5(self):
		return 10 ** sin(time()/10)
		
			#Should return (Float): (Temperature)
	def GetTemperature43_1(self):
		return sin(time() / 15) * 5 + 45

	#Should return (Float): (Temperature)
	def GetTemperature43_2(self):
		return (5 ** sin(time() / 15)) + 50
	
	#Should return (Float): (Temperature)
	def GetTemperature43_3(self):
		pass
	
	#Should return (Float): (Temperature)
	def GetTemperature43_X(self):
		pass

	def SetSparkIgniter(self, on):
		pass

	def SetServo68_1(self, value):
		pass

	#Should return current servo value
	def GetServo69_1(self):
		return sin(time() / 15) * 180 + 180

	### ADDED TO COMPILE
	def GetServo68_1(self):
		return cos(time() / 15) * 180 + 180

# obj = DumbLFETSHardwareInterface()
# obj.SetAllValvesOpen(True)