#!/usr/bin/python
import sys, math, random, copy
import Model1D, Data1D, ObjFn1D
import pylab

def average(x):
	s = 0.0
	for r in x:
		s = s + r
	if len(x) == 0:
		return 0.0
	else:
		return s / len(x)
def sdev(x):
	if len(x) == 0:
		return 0.0
	N = len(x)
	t1 = 1.0 / (N-1.0)
	a = average(x)
	s = 0.0
	for i in x:
		r = (i - a)
		rr = r*r
		s = s + rr
	t2 = t1 * s
	t3 = math.sqrt(t2)
	return t3	

def run_model(model, data, move, scale):
	if (move == 1):
		model.update_terms(scale)
	terms = model.terms
	y_sim = model.solve(data.dataX)
	objfn = ObjFn1D.ObjFn1D(data.dataY, y_sim)
	obj = objfn.ssr()
	obj = objfn.diff2()	
	return obj, terms, y_sim
	

def main(argv):

	dataX = []
	for i in range(14):
		dataX.append(i)
	dataY = [10.07,9.86,10.24,10.39,10.55,10.78,10.82,11.01,11.19,11.19,11.17,11.52,11.27,11.30]
	#dataY = []
        #for x in dataX:
	#	r = random.normalvariate(0.0,0.25)
	#	y = math.sin(x) + r
	#	dataY.append(y)
	#	dataY.append(x)
	#	dataY.append(-1.0*((x-5)**2)+20)

	startm = 0 #average(dataY)
	starts = sdev(dataY)
	print "starting ", startm, starts

        data = Data1D.Data1D(dataX,dataY)
	data.show()

	all_models = []
	all_sims = []

	M = int(argv[1])
	N = int(argv[2])
	target_acc = 0.3

	factor = (1.0/N)

	for mix in range(M):
		mi = mix
		print "Model " + str(mi)
		model = Model1D.Model1D(startm,starts,mi)
		objs = []
		y_sims = []
		terms = []
		scale = 1.0
		accepted = 0
		rejected_count = 0
		acc = 0.0

		obj1, terms1, y_sim1 = run_model(model, data, 0, scale)
		move = 1
		for run in range(N):
			run = run + 1
			a = random.uniform(0, 1)
			obj2, terms2, y_sim2 = run_model(model, data, move, scale)
		#	like1 = math.exp(-0.5*(obj1))
	 	#	like2 = math.exp(-0.5*(obj2))
			like1 = 1/obj1
			like2 = 1/obj2
		#	print obj1, obj2, like1, like2
			b = like2/like1
		#	print acc, b, obj1, obj2, scale	
			pick2 = 0
			if (b > a):
				pick2 = 1
			else:
				pick2 = 0
		
			if pick2 == 1:
				move = 1
				accepted = accepted + 1
				select_obj = obj2
				select_y = copy.deepcopy(y_sim2)
				select_terms = copy.deepcopy(terms2)

				obj1 = select_obj
				terms1 = select_y
				y_sim1 = select_terms
			else:
				move = 0
				rejected_count = rejected_count + 1
				if rejected_count > 1000:
					model = Model1D.Model1D(startm,starts,mi)
				select_obj = obj1
				select_y = copy.deepcopy(y_sim1)
				select_terms = copy.deepcopy(terms1)
	
			objs.append(select_obj)
			y_sims.append(select_y)
			terms.append(select_terms)


			acc = (accepted*1.0)/(run*1.0)
			scale = scale + factor * (acc - target_acc)

		m = min(objs)
		i = objs.index(m)
		print m, i, acc, scale
		print y_sims[i]
		s = ""
		for t in terms[i]:
			s = s + str(t) + ", "
		print s
		#pylab.plot(data.dataX, y_sims[i])

		all_models.append(m)
		all_sims.append(y_sims[i])

	pylab.plot(data.dataX, data.dataY, 'ok')

	m = min(all_models)
	i_best = all_models.index(m)
	y = all_sims[i_best]
		
	pylab.plot(data.dataX, y, 'ob')

	ss = sorted(all_models)
	ss = ss[4]

        for i, s in enumerate(all_models):
                if s < ss:
                        #pass
                        pylab.plot(data.dataX, all_sims[i])


	print "Best model: ", i_best, " with obj_fn ", m


	#pylab.legend( () )
	pylab.savefig('output.png')

main(sys.argv)
