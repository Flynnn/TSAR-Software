#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, math

from LFETSHardwareInterface import LFETSHardwareInterface
from dumblfetshardwareinterface import DumbLFETSHardwareInterface

π = math.pi

try:
	#TODO: Fix these horrible import statements
	from PyQt5.QtWidgets import *
	from PyQt5 import QtGui
	from PyQt5.QtGui import *
	from PyQt5.QtCore import *
	from PyQt5.QtCore import Qt
except ImportError:
	print("PyQt 5 not installed.")
	sys.exit(1)

class SCADA(QWidget):
	def __init__(self, widgets=[]):
		super().__init__()
		
		# self.setGeometry(300, 100, 1200, 800)
		self.setFixedSize(1200, 800)

		# Set background color
		self.setAutoFillBackground(True)
		self.palette = self.palette()
		self.palette.setColor(self.backgroundRole(), Qt.black)
		self.setPalette(self.palette)

		self.widgets = widgets
		
		# Set regular updates
		self.timer = QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(100)	# 10 Hz

		self.show()

	def paintEvent(self, event):
		super().paintEvent(event)

		qp = QPainter()
		qp.begin(self)

		pipes = []
		widgets = []

		# Divide all widgets into pipes and everything else
		for widget in self.widgets:
			if isinstance(widget, Pipe):
				pipes.append(widget)
			else:
				widgets.append(widget)

		# Paint pipes first
		for pipe in pipes:
			pipe.paint(qp)

		# Paint widgets on top of pipes
		for widget in widgets:
			widget.paint(qp)

		qp.end()

class PassiveWidget:
	def __init__(self, hardware_interface=None, name="", rect=None, img_file="", text_color=Qt.white):
		self.hardware = hardware_interface
		self.name = name
		self.rect = rect if rect else QRect()
		self.image = QPixmap(img_file) if img_file else None
		self.color = text_color

	def paint(self, qp):
		qp.drawPixmap(self.rect, self.image)

		# Create rect directly to right of image
		info_rect = QRect(self.rect)
		info_rect.setX(self.rect.right() + 1) # Add one to avoid one pixel overlap

		# Resize rect to fit text
		info_rect = qp.boundingRect(info_rect, Qt.AlignLeft, self.get_text())
		info_rect.setWidth(info_rect.width() + 10)
		info_rect.setHeight(info_rect.height() + 10)

		# Paint background
		brush = QBrush(QColor("green")) # TODO: change color from green to something less obnoxious
		qp.fillRect(info_rect, brush)

		# Create another inset rect for text
		text_rect = QRect(info_rect)
		# text_rect.setWidth(text_rect.width()-10)
		text_rect.setX(text_rect.x() + 5)
		text_rect.setY(text_rect.y() + 5)
		# text_rect.setHeight(text_rect.height()-10)

		# Draw text
		qp.setPen(self.color)
		# size_rect = qp.boundingRect(text_rect, Qt.AlignLeft, self.get_text())
		# self.info_rect = size_rect
		qp.drawText(text_rect, Qt.AlignLeft, self.get_text())
		

	def get_text(self):
		return "Name: {}".format(self.name)

class PressureTranducer4_1(PassiveWidget):
	def get_data(self):
		return self.hardware.GetPressure4_1()

	def get_text(self):
		return "Name: {}\nPressure: {:.3f} kPa".format(self.name, self.hardware.GetPressure4_1())

class PressureTranducer4_2(PassiveWidget):
	def get_data(self):
		return self.hardware.GetPressure4_2()

	def get_text(self):
		return "Name: {}\nPressure: {:.3f} kPa".format(self.name, self.hardware.GetPressure4_2())

class PressureTranducer4_3(PassiveWidget):
	def get_data(self):
		return self.hardware.GetPressure4_3()

	def get_text(self):
		return "Name: {}\nPressure: {:.3f} kPa".format(self.name, self.hardware.GetPressure4_3())

class PressureTranducer4_4(PassiveWidget):
	def get_data(self):
		return self.hardware.GetPressure4_4()

	def get_text(self):
		return "Name: {}\nPressure: {:.3f} kPa".format(self.name, self.hardware.GetPressure4_4())

class PressureTranducer4_5(PassiveWidget):
	def get_data(self):
		return self.hardware.GetPressure4_5()

	def get_text(self):
		return "Name: {}\nPressure: {:.3f} kPa".format(self.name, self.hardware.GetPressure4_5())

class Valve9_1(PassiveWidget):
	def get_data(self):
		return self.hardware.GetValveOpen9_1()

	def get_text(self):
		return "Name: {}\nValve: {}".format(self.name, "Open" if self.hardware.GetValveOpen9_1() else "Closed")

class Valve9_2(PassiveWidget):
	def get_data(self):
		return self.hardware.GetValveOpen9_2()

	def get_text(self):
		return "Name: {}\nValve: {}".format(self.name, "Open" if self.hardware.GetValveOpen9_2() else "Closed")

class Valve9_3(PassiveWidget):
	def get_data(self):
		return self.hardware.GetValveOpen9_3()

	def get_text(self):
		return "Name: {}\nValve: {}".format(self.name, "Open" if self.hardware.GetValveOpen9_3() else "Closed")

class Valve42_1(PassiveWidget):
	def get_data(self):
		return self.hardware.GetValveOpen42_1()

	def get_text(self):
		return "Name: {}\nValve: {}".format(self.name, "Open" if self.hardware.GetValveOpen42_1() else "Closed")

class Valve49_1(PassiveWidget):
	def get_data(self):
		return self.hardware.GetValveOpen49_1()

	def get_text(self):
		return "Name: {}\nValve: {}".format(self.name, "Open" if self.hardware.GetValveOpen49_1() else "Closed")

class Valve49_2(PassiveWidget):
	def get_data(self):
		return self.hardware.GetValveOpen49_2()

	def get_text(self):
		return "Name: {}\nValve: {}".format(self.name, "Open" if self.hardware.GetValveOpen49_2() else "Closed")

class Valve58_1(PassiveWidget):
	def get_data(self):
		return self.hardware.GetValveOpen58_1()

	def get_text(self):
		return "Name: {}\nValve: {}".format(self.name, "Open" if self.hardware.GetValveOpen58_1() else "Closed")

class Servo68_1(PassiveWidget):
	def get_data(self):
		return self.hardware.GetServo68_1()

	def get_text(self):
		# TODO: Servos have three states: Open, Partial, and Closed. Add text to represent states
		return "Name: {}\nValve: {}".format(self.name, self.hardware.GetServo68_1())

class Servo69_1(PassiveWidget):
	def get_data(self):
		return self.hardware.GetServo69_1()

	def get_text(self):
		# TODO: Servos have three states: Open, Partial, and Closed. Add text to represent states
		return "Name: {}\nValve: {}".format(self.name, self.hardware.GetServo69_1())

class TemperatureSensor43_1(PassiveWidget):
	# Enums for temperature display
	CELSIUS = "C"
	FAHRENHEIT = "F"
	KELVIN = "K"

	def __init__(self, *args, format="C", **kwargs):
		self.format = format
		super().__init__(*args, **kwargs)

	def get_data(self):
		return self.hardware.GetTemperature43_1()

	def get_kelvin(self):
		return self.hardware.GetTemperature43_1()

	def get_celsius(self):
		return self.get_kelvin() + 273.15

	def get_fahrenheit(self):
		return self.get_celsius() * 1.8 + 32.0

	def get_text(self):
		func = None
		if self.format == TemperatureSensor43_1.CELSIUS:
			func = self.get_celsius			
		elif self.format == TemperatureSensor43_1.FAHRENHEIT:
			func = self.get_fahrenheit
		elif self.format == TemperatureSensor43_1.KELVIN:
			func = self.get_kelvin
		else:
			func = lambda: float("NaN")
		return "Name: {}\nTemperature: {:.2f} °{}".format(self.name, func(), self.format)

class TemperatureSensor43_2(PassiveWidget):
	# Enums for temperature display
	CELSIUS = "C"
	FAHRENHEIT = "F"
	KELVIN = "K"

	def __init__(self, *args, format="C", **kwargs):
		self.format = format
		super().__init__(*args, **kwargs)

	def get_data(self):
		return self.hardware.GetTemperature43_2()

	def get_kelvin(self):
		return self.hardware.GetTemperature43_2()

	def get_celsius(self):
		return self.hardware.GetTemperature43_2() + 273.15

	def get_fahrenheit(self):
		return self.get_celsius() * 1.8 + 32.0

	def get_text(self):
		func = None
		if self.format == TemperatureSensor43_1.CELSIUS:
			func = self.get_celsius			
		elif self.format == TemperatureSensor43_1.FAHRENHEIT:
			func = self.get_fahrenheit
		elif self.format == TemperatureSensor43_1.KELVIN:
			func = self.get_kelvin
		else:
			func = lambda: float("NaN")
		return "Name: {}\nTemperature: {:.2f} °{}".format(self.name, func(), self.format)

class Rocket_Nozzle(PassiveWidget):
	def __init__(self, *args, **kwargs):
		PassiveWidget.__init__(self, *args, **kwargs)
		self.temperature = TemperatureSensor43_2()
		self.pressure = PressureTranducer4_5()

	def get_text(self):
		pass


class Pipe:
	def __init__(self, start, end, startAnchor=(.5, .5), endAnchor=(.5, .5), joints=0, color=Qt.white, direction=0):
		if isinstance(start, QPoint):
			self.start = start
		else:
			self.start = start.rect.topLeft()
			self.start.setX(self.start.x() + start.rect.width() * startAnchor[0])
			self.start.setY(self.start.y() + start.rect.height() * startAnchor[1])

		if isinstance(end, QPoint):
			self.end = end
		else:
			self.end = end.rect.topLeft()
			self.end.setX(self.end.x() + end.rect.width() * endAnchor[0])
			self.end.setY(self.end.y() + end.rect.height() * endAnchor[1])

		self.joints = joints
		self.direction = direction
		self.color = color

	def paint(self, qp):
		qp.setPen(QPen(self.color, 5, 1, 0x10, 0x40))
		if self.joints <= 1:
			qp.drawLine(self.start, self.end)
		elif self.joints == 2:
			midpoints = (QPoint(self.start.x(), self.end.y()), QPoint(self.end.x(), self.start.y()))
			midpoint = midpoints[self.direction % 2]
			
			qp.drawLine(self.start, midpoint)
			qp.drawLine(midpoint, self.end)
		elif self.joints == 3:
			midpoint = QPoint((self.start.x() + self.end.x()) / 2,(self.start.y() + self.end.y()) / 2)

			if abs(self.start.x() - self.end.x()) > abs(self.start.y() - self.end.y()):
				# Horizontal connection
				qp.drawLine(self.start, QPoint(midpoint.x(), self.start.y()))
				qp.drawLine(QPoint(midpoint.x(), self.start.y()), QPoint(midpoint.x(), self.end.y()))
				qp.drawLine(QPoint(midpoint.x(), self.end.y()), self.end)
			else:
				# Vertical connection
				qp.drawLine(self.start, QPoint(self.start.x(), midpoint.y()))
				qp.drawLine(QPoint(self.start.x(), midpoint.y()), QPoint(self.end.x(), midpoint.y()))
				qp.drawLine(QPoint(self.end.x(), midpoint.y()), self.end)

		elif isinstance(self.joints, list):
			qp.drawLine(self.start, self.joints[0])

			current = self.joints[0]
			for point in self.joints[1:]:
				qp.drawLine(current, point)
				current = point

			qp.drawLine(self.joints[-1], self.end)


if __name__ == "__main__":
	app = QApplication(sys.argv)

	dumdum = DumbLFETSHardwareInterface()
	
	# Widgets
	widgets = {
			"50.1":	PassiveWidget(None, "Nitrogen Tank 50.1", QRect(550, 150, 120, 98), "images/tank.jpg"),
			"28.1":	PassiveWidget(None, "Fuel Tank 28.1", QRect(900, 450, 120, 98), "images/tank.jpg"),
			"4.1":	PressureTranducer4_1(dumdum, "Pressure Tranducer 4.1", QRect(600, 25, 50, 75), "images/transducer.png"),
			"4.2":	PressureTranducer4_2(dumdum, "Pressure Tranducer 4.2", QRect(900, 250, 50, 75), "images/transducer.png"),
			"4.3":	PressureTranducer4_3(dumdum, "Pressure Tranducer 4.3", QRect(150, 225, 50, 75), "images/transducer.png"),
			"4.4":	PressureTranducer4_4(dumdum, "Pressure Tranducer 4.4", QRect(450, 500, 50, 75), "images/transducer.png"),
			"4.5":	PressureTranducer4_5(dumdum, "Pressure Tranducer 4.5", QRect(600, 720, 50, 75), "images/transducer.png"),
			"11.1": PassiveWidget(None, "Pressure Regulator 11.1", QRect(900, 50, 50, 50), "images/regulator.jpg"),
			"7.1":	PassiveWidget(None, "Pressure Regulator 7.1", QRect(300, 50, 50, 50), "images/regulator.jpg"),
			"9.1":	Valve9_1(dumdum, "Valve 9.1", QRect(250, 110, 50, 75), "images/valve.jpg"),
			"9.2":	Valve9_2(dumdum, "Valve 9.2", QRect(900, 150, 50, 75), "images/valve.jpg"),
			"9.3":	Valve9_3(dumdum, "Valve 9.3", QRect(100, 50, 50, 75), "images/valve.jpg"),
			"42.1":	Valve42_1(dumdum, "Valve 42.1", QRect(0, 150, 50, 75), "images/valve.jpg"),
			"49.1":	Valve49_1(dumdum, "Valve 49.1", QRect(250, 400, 50, 75), "images/valve.jpg"),
			"49.2":	Valve49_2(dumdum, "Valve 49.2", QRect(600, 400, 50, 75), "images/valve.jpg"),
			"58.1":	Valve58_1(dumdum, "Valve 58.1", QRect(1000, 350, 50, 75), "images/valve.jpg"),
			"68.1":	Servo68_1(dumdum, "Servo 68.1", QRect(900, 600, 50, 75), "images/valve.jpg"),
			"69.1":	Servo69_1(dumdum, "Servo 69.1", QRect(50, 600, 50, 75), "images/valve.jpg"),
			"21.1":	PassiveWidget(None, "Liquid Oxygen Tank 21.1", QRect(25, 300, 120, 98), "images/tank.jpg"),
			"43.1":	TemperatureSensor43_1(dumdum, "Temperature Sensor 43.1", QRect(200, 340, 37.5, 75), "images/temp.png"),
			"43.2":	TemperatureSensor43_2(dumdum, "Temperature Sensor 43.2", QRect(600, 635, 37.5, 75), "images/temp.png"),
			"nozz":	PassiveWidget(None, "Rocket Booster Nozzle", QRect(400, 600, 150, 200), "images/nozzle.gif"),
	}

	# Intersections
	int0 = QPoint(925, 375)

	# Pipes
	pipes = [
		Pipe(widgets["50.1"], widgets["4.1"], joints=2, direction=1),
		Pipe(widgets["4.1"], widgets["7.1"], startAnchor=(.5, .85), joints=2, direction=1),
		Pipe(widgets["4.1"], widgets["11.1"], startAnchor=(.5, .75), joints=2, direction=1),
		Pipe(widgets["11.1"], widgets["9.2"]),
		Pipe(widgets["9.2"], widgets["4.2"]),
		Pipe(widgets["58.1"], int0, joints=2),
		Pipe(widgets["4.2"], int0),
		Pipe(widgets["28.1"], int0, joints=2, direction=1),
		Pipe(widgets["9.3"], widgets["7.1"], joints=2),
		Pipe(widgets["9.1"], QPoint(275, 75), joints=2, direction=1),
		Pipe(widgets["9.3"], widgets["21.1"], endAnchor=(.84, .5)),
		Pipe(widgets["42.1"], QPoint(125, 210), (.5, .8)),
		Pipe(widgets["4.3"], QPoint(130, 262)),
		Pipe(widgets["43.1"], widgets["21.1"], (.30, .38), (.5, .7)),
		Pipe(widgets["21.1"], widgets["69.1"], endAnchor=(.7, .5)),
		Pipe(widgets["49.1"], QPoint(90, 437)),
		Pipe(widgets["69.1"], widgets["nozz"], (.5, .85), (.5, .31)),
		Pipe(widgets["4.4"], widgets["nozz"]),
		Pipe(widgets["49.1"], widgets["4.4"], joints=2, direction=0),
		Pipe(widgets["nozz"], widgets["4.5"], joints=2, direction=0),
		Pipe(widgets["nozz"], widgets["43.2"], joints=2, direction=0),
		Pipe(widgets["28.1"], widgets["68.1"], joints=2, direction=1),
		Pipe(widgets["68.1"], widgets["nozz"], endAnchor=(.5, .56), joints=2, direction=0),
		Pipe(widgets["28.1"], widgets["49.2"], endAnchor=(.5, .75), joints=2),
		Pipe(widgets["49.2"], widgets["4.4"], startAnchor=(.5, .75), joints=2, direction=1),
	]

	# RAINBOW PIPES???
	import random
	colors = [Qt.red, QColor("orange"), Qt.yellow, Qt.green, Qt.cyan, QColor("indigo"), QColor("violet")]#, Qt.white]
	for pipe in pipes:
		pipe.color = random.choice(colors)

	# Add pipes to widgets list
	for pipe in pipes:
		widgets.update({pipe: pipe})

	# Create interface
	main = SCADA(widgets.values())
	main.setWindowTitle('LFETS TSAR SCADA')

	# Run app
	sys.exit(app.exec_())