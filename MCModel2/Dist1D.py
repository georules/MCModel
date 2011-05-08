#!/usr/bin/python

import random

class Dist1D:
	mean = 0.0
	stddev = 0.0

	def __init__(self, mean, stddev):
		self.mean = mean
		self.stddev = stddev	

	def startPoint(self):
		newm = random.normalvariate(self.mean, self.stddev)
		return newm

	def newPoint(self, m, s):
		self.stddev = s
		self.mean = m
		newm = random.normalvariate(self.mean, self.stddev)
		return newm
