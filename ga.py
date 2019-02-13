import numpy as np
import random

class GA(object):
	def __init__(self, length, genSize, crossoverPoints, topN, randomN, freshN, mutationRate, mutationRange, fitness):
		self.length = length
		self.generation = 0
		self.genSize = genSize
		self.batch = [np.random.rand(length) * 2 - 1 for i in xrange(genSize)]
		self.fitnessHistory = []
		self.crossoverPoints = crossoverPoints
		self.topN = topN
		self.randomN = randomN
		self.freshN = freshN
		self.mutationRate = mutationRate
		self.mutationRange = mutationRange
		self.fitness = fitness

	def next(self):
		fitness = sorted([(x, self.fitness(x)) for x in self.batch], key=lambda x: x[1], reverse=True)

		self.fitnessHistory.append((fitness[0][1], sum(x[1] for x in fitness) / len(fitness)))

		sources = [x[0] for x in fitness[:self.topN]] + [x[0] for x in random.sample(fitness[self.topN:], self.randomN)]
		sources += [np.random.rand(self.length) * 2 - 1 for i in xrange(self.freshN)]
		dsources = sources[:self.topN] * 10 + sources[self.topN:]
		each = (self.genSize - self.topN) / len(sources)

		self.batch = sources[:self.topN]
		for i, source in enumerate(sources):
			for j in xrange(each):
				self.batch.append(self.mutate(self.crossover(source, dsources[random.randrange(len(dsources))])))

		self.generation += 1

	def crossover(self, a, b):
		points = list(sorted(random.sample(range(self.length), self.crossoverPoints)))
		points.append(self.length)

		c = []
		lpoint = 0
		for point in points:
			c.append((a if random.randrange(2) == 0 else b)[lpoint:point])
			lpoint = point

		return np.concatenate(c)

	def mutate(self, string):
		for i in xrange(random.randrange(self.mutationRate)):
			p = random.randrange(self.length)
			string[p] = max(min(string[p] + random.uniform(-1, 1) * self.mutationRange, 1), -1)
		return string
