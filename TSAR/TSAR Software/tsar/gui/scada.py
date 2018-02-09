#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, math

from LFETSHardwareInterface import LFETSHardwareInterface
# from dumblfetshardwareinterface import DumbLFETSHardwareInterface

π = math.pi

try:
	from PyQt5.QtWidgets import *
	from PyQt5 import QtGui
	from PyQt5.QtGui import *
	from PyQt5.QtCore import *
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

		self.show()

	def paintEvent(self, event):
		super().paintEvent(event)

		qp = QPainter()
		qp.begin(self)

		# print(dir(event))
		# print(event.rect())

		for widget in sorted(self.widgets, key=lambda x: x.depth, reverse=True):
			widget.paint(qp)

		qp.end()

	# def mousePressEvent(self, event):
		# print("Pressed")
		# print(event)
		# print("\n".join([i for i in dir(QWidget) if "Event" in i]))

	def mouseMoveEvent(self, event):
		pos = event.pos()
		update = False
		depth = 0

		for widget in (widget for widget in self.widgets if isinstance(widget, TSARWidget)):
			if widget.rect.contains(pos):
				highlighted = True
				depth = -1
			else:
				highlighted = False
				depth = 1

			if widget.highlighted != highlighted:
				widget.highlighted = highlighted
				widget.depth = depth
				update = True

		if update:
			self.update()

	def add_widget(self, widget):
		self.widgets.append(widget)

class TSARWidget:
	def __init__(self, rect, img_file):
		# super().__init__()
		self.hardware = None
		self.rect = rect
		self.image = QPixmap(img_file) if img_file else None
		self.highlighted = False
		self.depth = 1

	def paint(self, qp):
		qp.drawPixmap(self.rect, self.image)

		if self.highlighted:

			brush = QBrush(QColor("green"))
			qp.fillRect(self.rect.right(), self.rect.top(), 300, 300, brush)

class Pipe:
	def __init__(self, start, end, joints=0):
		self.start_widget = start
		self.end_widget = end
		self.joints = joints
		self.depth = 99

	def paint(self, qp):
		qp.setPen(QPen(QColor(0, 0, 0), 5, 1, 0x10, 0x40))

		start = self.start_widget.rect.center()
		end = self.end_widget.rect.center()
		angle = math.atan2(start.x()-end.x(), start.y()-end.y()) + (π/2)

		if abs(angle) < .7854:
			# Right side
			start.setX(self.start_widget.rect.right())
			end.setX(self.end_widget.rect.left())
		elif abs(angle) > 2.3562:
			# Left side
			start.setX(self.start_widget.rect.left())
			end.setX(self.end_widget.rect.right())
		elif angle > 0:
			# Top
			start.setY(self.start_widget.rect.top())
			end.setY(self.end_widget.rect.bottom())
		else:
			# Bottom
			start.setY(self.start_widget.rect.bottom())
			end.setY(self.end_widget.rect.top())

		qp.drawLine(start.x(), start.y(), end.x(), end.y())


if __name__ == "__main__":
	app = QApplication(sys.argv)

	# dumdum = DumbLFETSHardwareInterface()
	
	widgets = [
			TSARWidget(QRect(100, 100, 240, 196), "tank.jpg"),
			TSARWidget( QRect(800, 450, 240, 196), "tank.jpg"),
			TSARWidget(QRect(200, 440, 240, 196), "tank.jpg"),
			TSARWidget(QRect(600, 200, 240, 196), "tank.jpg"),
			]

	widgets += [Pipe(widgets[0], widgets[2]),
				Pipe(widgets[0], widgets[3]),
				Pipe(widgets[2], widgets[1]),
				Pipe(widgets[3], widgets[1])]

	main = SCADA(widgets)
	sys.exit(app.exec_())