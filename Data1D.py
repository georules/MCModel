#!/usr/bin/python

class Data1D:
	dataX = []
	dataY = []

	def __init__(self, dataX = [], dataY = []):
		self.dataX = dataX
		self.dataY = dataY

	def show(self):
		print self.dataX
		print self.dataY
