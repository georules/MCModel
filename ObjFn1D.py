#!/usr/bin/python

class ObjFn1D:
	y_d = []
	y_s = []
	def __init__(self, y_d, y_s):
		self.y_d = y_d
		self.y_s = y_s

	def sumresid(self):
		y_d = self.y_d
		y_s = self.y_s
		n = len(y_d)
		s = 0.0
		for i in range(n):
			r = y_d[i] - y_s[i]
			s = s + r
		return s

	def ssr(self):
		y_d = self.y_d
		y_s = self.y_s
		n = len(y_d)
		s = 0.0
		for i in range(n):
			r = y_d[i] - y_s[i]
			r = r*r
			s = s + r
		return s
