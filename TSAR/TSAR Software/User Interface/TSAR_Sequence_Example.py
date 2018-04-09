#################
# UNTESTED CODE #
#################
#Written by Georges Oates Larsen

from TSAR import LFETSHardwareInterface
import time

class DumbLFETSHardwareInterface	(LFETSHardwareInterface):
	#Put your implementation details here --
	#IE, make motors turn when valves get told to open/close, store and report pressure values from hardware
	#This implementation is stupid, and does nothing.
	pass


#Pre-programmed(?) ambient pressures (in bars):
acceptable_pressure_difference = 0.1
acceptable_temperature_difference = 2
ambient_pressures = {
	"4.1":1.01325,
	"4.2":1.01325,
	"4.3":1.01325,
	"4.4":1.01325,
	"4.5":1.01325,
}


def TestSequence():
	global acceptable_pressure_difference
	global acceptable_temperature_difference
	global ambient_pressures
	lhi = DumbLFETSHardwareInterface()

	#Close all valves:
	lhi.SetAllValvesOpen(False)
	#Wait a bit to let pressures begin to show trends.
	time.sleep(0.1)

	#Record initial pressures:
	initial_pressures = {
	}
	
	#Record initial temperatures:
	initial_temperatures = {
		"43.1":lhi.GetTemperature("43.1"),
		"43.2":lhi.GetTemperature("43.3"),
		"43.X":lhi.GetTemperature("43.X"),
	}
	
	#Ensure 4.1 above ambient, 4.2-4.5 at ambient.
	#Should probably be done with a for loop, but as this is an example, I find this better as it is less cryptic:
	if (not (lhi.GetPressure("4.1") > ambient_pressures["4.1"] and
		CheckAmbient(lhi,"4.2") and
		CheckAmbient(lhi,"4.3") and
		CheckAmbient(lhi,"4.4") and
		CheckAmbient(lhi,"4.5")):
		return Panic()
	
	#For safety, AwaitStable and the above ambient pressure checks should really be concurrent,
	#But for the sake of this demonstration being simple, I will not do so.
	AwaitStable(lhi, "4.1", 0.01)
	
	#Open 58.1
	lhi.SetValveOpen("58.1", True)
	
	#Wait for fluctuation on 4.2
	while CheckAmbient(lhi,"4.2"):
		time.sleep(0.1)
	
	#Panic if 4.3 not ambient.
	if (not CheckAmbient(lhi,"4.3")):
		return Panic()
	
	#Personnel confirm the fuel tank is full.
	lhi.PersonnelConfirmFuelTankFull(True)
	
	#Open 42.1
	lhi.SetValveOpen("42.1", True)
	
	#Wait for fluctuation on 4.3
	while CheckAmbient(lhi,"4.3"):
		time.sleep(0.1)
		
	#Wait for 43.1, 43.3, 43.X colder
	while not (lhi.GetTemperature("43.1") < initial_temperatures["43.1"] - acceptable_temperature_difference and
			   lhi.GetTemperature("43.3") < initial_temperatures["43.3"] - acceptable_temperature_difference and
			   lhi.GetTemperature("43.X") < initial_temperatures["43.X"] - acceptable_temperature_difference):
		time.sleep(0.1)
	
	#Personnel confirm the LOX tank is full.
	lhi.PersonnelConfirmLOXTankFull(True)
	
	#Personnel confirm the evacuation.
	lhi.PersonnelConfirmEvacuation(True)
	
	#Close 42.1, 58.1
	lhi.SetValveOpen("42.1", False)
	lhi.SetValveOpen("58.1", False)
	
	#Ignition sequence
	while True:	
		#Record ignition initial pressures:
		initial_pressures["4.4"] = lhi.GetPressure("4.4")
		initial_pressures["4.3"] = lhi.GetPressure("4.3")
		initial_pressures["4.2"] = lhi.GetPressure("4.2")
		
		#Open 9.3, 9.2
		lhi.SetValveOpen("9.3", True)
		lhi.SetValveOpen("9.2", True)
		
		#Await pressure increase on 4.2. 4.3:
		while (not (lhi.GetPressure("4.2") > initial_pressures["4.2"] + acceptable_pressure_difference) and
		       not (lhi.GetPressure("4.3") > initial_pressures["4.3"] + acceptable_pressure_difference)):
			time.sleep(0.1)
		
		#Should this be XOR or OR? I had a little trouble reading the flow diagram here. Defaulted to OR, makes more sense to me.
		if (lhi.GetPressure("4.2") > 51.7107 or lhi.GetPressure("4.3") > 37.9212):
			return Panic()
	
		
		#Once again, the flow-chart calls for concurrency, and I do not deliver, for simplicity, for now.
		
		#Regulate LOX Pressure.
		if (lhi.GetPressure("4.3") > 31.0264):
			lhi.SetValveOpen("42.1", True)
			while lhi.GetPressure("4.3") > 31.0264:
				time.sleep(0.1)
			lhi.SetValveOpen("42.1", False)
		
		#Regulate Fuel Pressure.
		if (lhi.GetPressure("4.2") > 48.2633):
			lhi.SetValveOpen("58.1", True)
			while lhi.GetPressure("4.2") > 48.2633:
				time.sleep(0.1)
			lhi.SetValveOpen("58.1", False)
		
		#Activate Spark Igniter
		lhi.SetSparkIgniter(True)
		
		#Open 49.1, 49.2
		lhi.SetValveOpen("49.1", True)
		lhi.SetValveOpen("49.2", True)
		
		ignitionOccured = False
		ignitionTime = 2
		
		#Give ignition 2 seconds to occur.
		while not ignitionOccurred:
			if (PressureChangeIndicatesIgnition(lhi.GetPressure("4.4"), initial_pressures["4.4"])):
				ignitionOccurred = True
			if (ignitionTime <= 0):
				break
			ignitionTime = ignitionTime = 0.1 #Not the correct way to do this, but it'll work for example purposes.
			time.sleep(0.1)
		
		
		ShouldReattempt = True
		if (ignitionOccurred):
			break
		else:
			lhi.SetValveOpen("49.1", False)
			lhi.SetValveOpen("49.2", False)
			if (not ShouldReattempt):
				lhi.SetValveOpen("42.1", True)
				lhi.SetValveOpen("58.1", True)
				return Panic()
	
	#Post-Ignition Sequence:
	###Command Servos 68.1 and 69.1 in some unspecified way###
	
	#Delay 0.5 to 1 second (I chose 1 second)
	time.sleep(1)
	
	#Close 49.1, 49.2
	lhi.SetValveOpen("49.1", False)
	lhi.SetValveOpen("49.2", False)

	#Delay 0.5 seconds.
	time.sleep(0.5)
	
	#Terminate Spark Igniter
	lhi.SetSparkIgniter(False)
	
	#Delay for set time interval for fuel to burn
	time.sleep(20)
	
	###Command Servos 68.1 and 69.1 in some unspecified way###
	
	#Close 49.1, 49.2 (again) (why do we do this a second time...?), 9.2, 9.3
	lhi.SetValveOpen("49.1", False)
	lhi.SetValveOpen("49.2", False)
	lhi.SetValveOpen("9.2", False)
	lhi.SetValveOpen("9.3", False)
	
	#Open 9.1
	lhi.SetValveOpen("9.1", True)
	
	#Delay ~10 seconds for N2 purge
	time.sleep(10)
	
	#Close 9.1
	lhi.SetValveOpen("9.1", False)
	
	#Open 42.1, 58.1
	lhi.SetValveOpen("42.1", True)
	lhi.SetValveOpen("58.1", True)
	
	#Some time passes...
	time.sleep(10)
	
	#All pressure readings should now be ambient:
	if (CheckAmbient(lhi,"4.1") and
		CheckAmbient(lhi,"4.2") and
		CheckAmbient(lhi,"4.3") and
		CheckAmbient(lhi,"4.4") and
		CheckAmbient(lhi,"4.5")):
		return Panic()
	

def Panic()
	print("Oh no...")

def CheckAmbient(lhi, transducer):
	global acceptable_pressure_difference
	global ambient_pressures
	return abs(lhi.GetPressure(transducer) - ambient_pressures[transducer]) < acceptable_pressure_difference

def AwaitStable(lhi, transducer, max_delta):
	lastValue = lhi.GetPressure(transducer)
	while True:
		time.sleep(1)
		currentValue = lhi.GetPressure(transducer)
		if (abs(currentValue - lastValue) < max_delta):
			return
		lastValue = currentValue

def PressureChangeIndicatesIgnition(a, b):
	return True
