import numpy as np
import random

class GA(object):
	def __init__(self, length, genSize, crossoverPoints, topN, randomN, mutationRate, mutationRange):
		self.length = length
		self.generation = 0
		self.genSize = genSize
		self.batch = [np.random.rand(length) for i in xrange(genSize)]
		self.fitnessHistory = []
		self.crossoverPoints = crossoverPoints
		self.topN = topN
		self.randomN = randomN
		self.mutationRate = mutationRate
		self.mutationRange = mutationRange

	def next(self):
		fitness = sorted([(x, self.fitness(x)) for x in self.batch], key=lambda x: x[1], reverse=True)

		self.fitnessHistory.append((fitness[0][1], sum(x[1] for x in fitness) / len(fitness)))

		sources = [x[0] for x in fitness[:self.topN]] + [x[0] for x in random.sample(fitness[self.topN:], self.randomN)]
		each = self.genSize / len(sources)

		self.batch = []
		for i, source in enumerate(sources):
			for j in xrange(each):
				while True:
					other = random.randrange(len(sources))
					if other != i:
						break
				self.batch.append(self.mutate(self.crossover(source, sources[other])))

		self.generation += 1

	def fitness(self, string):
		return 0

	def crossover(self, a, b):
		points = list(sorted(random.sample(range(self.length), self.crossoverPoints)))
		switch = False
		points.append(self.length)

		c = []
		lpoint = 0
		for point in points:
			c.append((a if switch else b)[lpoint:point])
			switch = not switch
			lpoint = point

		return np.concatenate(c)

	def mutate(self, string):
		for i in xrange(random.randrange(self.mutationRate)):
			p = random.randrange(self.length)
			string[p] = min(max(string[p] + random.uniform(-1, 1) * self.mutationRange, 0), 1)
		return string
