#!/usr/bin/python
import sys, math, random, copy
import Model1D, Data1D, ObjFn1D
import pylab

def run_model(model, data, move, scale):
	if (move == 1):
		model.update_terms(scale)
	terms = model.terms
	y_sim = model.solve(data.dataX)
	objfn = ObjFn1D.ObjFn1D(data.dataY, y_sim)
	obj = objfn.ssr()
	
	return obj, terms, y_sim
	

def main(argv):
	factor = 1.0001

        dataX = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        dataY = [0.0, 0.1, 0.4, 0.6, 0.8, 0.7, 0.4, 0.2, 0.15, 0.1]
        #for x in dataX:
		#dataY.append(math.sin(x))
		#dataY.append(x)
		#dataY.append(-1.0*((x-5)**2)+20)

        data = Data1D.Data1D(dataX,dataY)
	data.show()

	all_models = []
	all_sims = []

	M = int(argv[1])
	N = int(argv[2])

	for mi in range(M):
		print "Model " + str(mi)
		model = Model1D.Model1D(0.0,0.05,mi)
		objs = []
		y_sims = []
		terms = []
		scale = 1.0
		move = 1.0
		accepted = 0
		acc = 0.0
		obj1, terms1, y_sim1 = run_model(model, data, 0, scale)
		for run in range(N):
			run = run + 1
			a = random.uniform(0, 1)
			obj2, terms2, y_sim2 = run_model(model, data, move, scale)
			like1 = math.exp(-(obj1/100))+1
			like2 = math.exp(-(obj2/100))+1
			b = like2/like1
	
			pick2 = 0
			if (b > 1):
				pick2 = 1
			else:
				if (b > a):
					pick2 = 1
				else:
					pick2 = 0
		
			if pick2 == 1:
				move = 1
				accepted = accepted + 1
				objs.append(copy.deepcopy(obj2))
				y_sims.append(copy.deepcopy(y_sim2))
				terms.append(copy.deepcopy(terms2))
				obj1 = obj2
				terms1 = terms2
				y_sim1 = y_sim2
			else:
				move = 0

			acc = (accepted*1.0)/(run*1.0)
			if acc < 0.50:
				scale = scale / factor
			else:
				scale = scale * factor

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
	ss = ss[5]

        for i, s in enumerate(all_models):
                if s < ss:
                        #pass
                        pylab.plot(data.dataX, all_sims[i])


	print "Best model: ", i_best, " with obj_fn ", m


	#pylab.legend( () )
	pylab.savefig('output.png')

main(sys.argv)
