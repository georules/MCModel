#!/usr/bin/python
import random, math
import Dist1D

class Term:
	DistA = 0
	DistB = 0
	DistC = 0
	a = 0.0
	b = 0.0
	c = 0.0
	s = 0.0
	def __init__(self, mean, stddev):
		self.s = stddev
		self.DistA = Dist1D.Dist1D(mean, stddev)
		self.DistB = Dist1D.Dist1D(mean, stddev)
		self.DistC = Dist1D.Dist1D(mean, stddev)
		self.a = self.DistA.startPoint()
		self.b = self.DistB.startPoint()
		self.c = self.DistC.startPoint()

	def update(self, scale):
		self.s = self.s * scale
		self.a = self.DistA.newPoint(self.a, self.s)
		self.b = self.DistB.newPoint(self.b, self.s)
		self.c = self.DistC.newPoint(self.c, self.s)

	def calc_wave(self, x):
		y = 0.0
		try:
			y = self.a * math.sin( self.b * x + self.c )
		except:
			y = 0.0
		return y

	def __str__(self):
		return str(self.a) + " *sin( " + str(self.b) + " *x+ " + str(self.c) + " )" 

class Model1D:
	terms = []

	def __init__(self, mean = 0.0, stddev = 1.0, N = 10):
		N = int(N)
		self.terms = []
		self.create_terms(mean, stddev, N)

	def create_terms(self, mean, stddev, N):
		terms = self.terms
		for i in range(N):
			T = Term(mean, stddev)	
			terms.append(T)

	def update_terms(self, s):
		terms = self.terms
		for t in terms:
			t.update(s)
	
	def solve(self, x_data):
		terms = self.terms
		num_terms = len(terms)
		y_data = []
		for x in x_data:
			y = 0.0
			for t in terms:
				y = y + t.calc_wave(x)
			y_data.append(y)
		return y_data
	
	def show(self):
		terms = self.terms
		for i in range(len(terms)):
			T = terms[i]
			print "T" + str(i) + " :" + str(T)
