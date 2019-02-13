from ga import GA
from game import Game
from model import model
import numpy as np

def evaluate(chromosome):
	v = [chromosome]
	def eat(length):
		t = v[0][:length]
		v[0] = v[0][length:]
		return t
	model.layers[0].set_weights([
		np.reshape(eat(2 * 3), (2, 3)), 
		eat(3)
	])

	def sub():
		game = Game()
		for i in xrange(2000):
			if game.lost:
				break

			pp = game.getPiecePieces()
			delta = game.findLowestDelta()

			if delta == 0:
				mdir = 0
			elif delta < 0:
				mdir = -1
			else:
				mdir = 1

			inputs = [
				mdir, 
				game.calculateFlatLanding()
			]

			output = model.predict(np.asarray([np.asarray(inputs)]))[0]
			
			cmd = ''
			if abs(output[0]) < 0.5:
				pass
			elif output[0] <= -0.5:
				cmd += 'l'
			elif output[0] >= 0.5:
				cmd += 'r'

			if abs(output[1]) < 0.5:
				pass
			elif output[1] <= -0.5:
				cmd += 'a'
			elif output[1] >= 0.5:
				cmd += 's'

			if output[2] >= 0.9:
				cmd += 'd'

			game.update(cmd)

		if game.cleared:
			print 'Cleared', game.cleared, 'rows'
		return game.score

	return sub()

ga = GA(
	3 * 2 + 3, 
	36, 
	5, 
	4, 2, 2, 
	3, .1, 
	evaluate
)

while True:
	print 'Generation', ga.generation
	ga.next()
	best, avg = ga.fitnessHistory[-1]
	print 'Best score %i, average %i' % (best, avg)
