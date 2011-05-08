#!/usr/bin/python

import random

class Dist1D:
	mean = 0.0
	stddev = 0.0

	def __init__(self, mean, stddev):
		self.mean = mean
		self.stddev = stddev	

	def newPoint(self):
		newm = random.normalvariate(self.mean, self.stddev)
		news = self.stddev
		return newm, news
