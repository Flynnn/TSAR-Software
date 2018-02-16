#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, math

from LFETSHardwareInterface import LFETSHardwareInterface
from dumblfetshardwareinterface import DumbLFETSHardwareInterface

π = math.pi

try:
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
		
		self.setMouseTracking(True)

		self.setGeometry(300, 100, 1200, 800)
		self.setWindowTitle('LFETS SCADA')

		self.widgets = widgets
		
		self.timer = QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(100)

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

class Valve9_2(PassiveWidget):
	def get_data(self):
		return self.hardware.GetValveOpen9_2()

	def get_text(self):
		return "Name: {}\nValve: {}".format(self.name, "Open" if self.hardware.GetValveOpen9_2() else "Closed")

class Valve58_1(PassiveWidget):
	def get_data(self):
		return self.hardware.GetValveOpen58_1()

	def get_text(self):
		return "Name: {}\nValve: {}".format(self.name, "Open" if self.hardware.GetValveOpen58_1() else "Closed")

class Pipe:
	def __init__(self, start, end, joints=0, color=Qt.white):
		if isinstance(start, QPoint):
			self.start = start
		else:
			self.start = start.rect.center()

		if isinstance(end, QPoint):
			self.end = end
		else:
			self.end = end.rect.center()

		self.joints = joints
		self.color = color

	def paint(self, qp):
		qp.setPen(QPen(self.color, 5, 1, 0x10, 0x40))

		# start = self.start_widget.rect.center()
		# end = self.end_widget.rect.center()
		# angle = math.atan2(start.x()-end.x(), start.y()-end.y()) + (π/2)

		# if abs(angle) < .7854:
		# 	# Right side
		# 	start.setX(self.start_widget.rect.right())
		# 	end.setX(self.end_widget.rect.left())
		# elif abs(angle) > 2.3562:
		# 	# Left side
		# 	start.setX(self.start_widget.rect.left())
		# 	end.setX(self.end_widget.rect.right())
		# elif angle > 0:
		# 	# Top
		# 	start.setY(self.start_widget.rect.top())
		# 	end.setY(self.end_widget.rect.bottom())
		# else:
		# 	# Bottom
		# 	start.setY(self.start_widget.rect.bottom())
		# 	end.setY(self.end_widget.rect.top())

		# qp.drawLine(start.x(), start.y(), end.x(), end.y())

		qp.drawLine(self.start, self.end)


if __name__ == "__main__":
	app = QApplication(sys.argv)

	dumdum = DumbLFETSHardwareInterface()
	
	widgets = {
			"50.1":	PassiveWidget(None, "Nitrogen Tank 50.1", QRect(500, 150, 120, 98), "images/tank.jpg"),
			"28.1":	PassiveWidget(None, "Fuel Tank 28.1", QRect(900, 450, 120, 98), "images/tank.jpg"),
			"4.1":	PressureTranducer4_1(dumdum, "Pressure Tranducer 4.1", QRect(600, 50, 50, 75), "images/transducer.png"),
			"4.2":	PressureTranducer4_2(dumdum, "Pressure Tranducer 4.2", QRect(900, 250, 50, 75), "images/transducer.png"),
			"11.1": PassiveWidget(None, "Pressure Regulator 11.1", QRect(900, 50, 50, 50), "images/regulator.jpg"),
			"7.1":	PassiveWidget(None, "Pressure Regulator 7.1", QRect(300, 50, 50, 50), "images/regulator.jpg"),
			"9.2":	Valve9_2(dumdum, "Valve 9.2", QRect(900, 150, 50, 75), "images/valve.jpg"),
			"58.1":	Valve58_1(dumdum, "Valve 58.1", QRect(1000, 350, 50, 75), "images/valve.jpg"),
	}

	int0 = QPoint(925, 375)

	pipes = [
		Pipe(widgets["50.1"], widgets["4.1"]),
		Pipe(widgets["4.1"], widgets["7.1"]),
		Pipe(widgets["4.1"], widgets["11.1"]),
		Pipe(widgets["11.1"], widgets["9.2"]),
		Pipe(widgets["9.2"], widgets["4.2"]),
		Pipe(widgets["58.1"], int0),
		Pipe(widgets["4.2"], int0),
		Pipe(widgets["28.1"], int0),
	]

	for pipe in pipes:
		widgets.update({pipe: pipe})

	main = SCADA(widgets.values())
	main.setAutoFillBackground(True)
	p = main.palette()
	p.setColor(main.backgroundRole(), Qt.black)
	main.setPalette(p)
	sys.exit(app.exec_())