#!/usr/bin/python
import random, math
import Dist1D

class Term:
	Dist = 0
	x = 0.0
	s = 0.0
	def __init__(self, Dist):
		self.Dist = Dist
		self.x, self.s = self.Dist.newPoint()

	def update(self, scale):
		self.s = self.s * scale
		self.Dist = Dist1D.Dist1D(self.x, self.s)
		self.x, self.s =  self.Dist.newPoint()

	def calc_coef(self, xin):
		y = 0.0
		try:
			y = self.x * xin
		except:
			y = 0.0
		return y

	def calc_exp(self, xin):
		y = 0.0
		try:
			y = self.x ** xin
		except: 
			y = 0.0
		return y

	def __str__(self):
		return str(self.x)

class Model1D:
	terms = []

	def __init__(self, mean = 0.0, stddev = 1.0, N = 10):
		N = int(N)
		self.terms = []
		self.create_terms(mean, stddev, N)

	def create_terms(self, mean, stddev, N):
		terms = self.terms
		for i in range(N):
			Dist = Dist1D.Dist1D(mean,stddev)
			T = Term(Dist)				
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
			b = 1.0
			e = 1.0
			if (num_terms % 2) == 0:
				for i in range(0,num_terms,2):
					try:
						y = y + terms[i].x * (x ** terms[i+1].x)
					except:
						y = 0.0
			else:
				y = y + terms[0].x * x
				for i in range(1,num_terms,2):
					try:
						y = y + terms[i].x * (x ** terms[i+1].x)
					except:
						y = 0.0	
			y_data.append(y)
		return y_data
	
	def show(self):
		terms = self.terms
		for i in range(len(terms)):
			T = terms[i]
			print "T" + str(i) + " :" + str(T)
