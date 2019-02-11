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
		np.reshape(eat(15 * 32), (15, 32)), 
		eat(32)
	])
	model.layers[1].set_weights([
		np.reshape(eat(32 * 16), (32, 16)), 
		eat(16)
	])
	model.layers[2].set_weights([
		np.reshape(eat(16 * 4), (16, 4)), 
		eat(4)
	])

	game = Game()

	for i in xrange(10000):
		if game.lost:
			break

		columns = [[j for j, row in enumerate(game.board) if row[i]][::-1] for i in xrange(10)]
		inputs = [elem[0] / 22. if len(elem) else 0 for elem in columns]
		inputs.append(game.piecePosition[0] / 9.)
		inputs.append(game.piecePosition[1] / 22.)
		inputs.append(game.pieceRotation / 3.)
		inputs.append(game.currentPiece / 6.)
		inputs.append(game.nextPiece / 6.)

		output = model.predict(np.asarray([np.asarray(inputs)]))[0]
		
		top = sorted(enumerate(output), key=lambda x: x[1], reverse=True)

		if top[0][1] < 0.5 or top[0][1] - top[1][1] < 0.1:
			game.update()
		elif top[0][0] == 0:
			game.update('l')
		elif top[0][0] == 1:
			game.update('r')
		elif top[0][0] == 2:
			game.update('a')
		elif top[0][0] == 3:
			game.update('s')

	return game.score

ga = GA(
	32 * 15 + 16 * 32 + 4 * 16 + 32 + 16 + 4, 
	132, 
	50, 
	4, 2, 2, 
	50, 0.1, 
	evaluate
)

while True:
	print 'Generation', ga.generation
	ga.next()
	best, avg = ga.fitnessHistory[-1]
	print 'Best score %i, average %i' % (best, avg)
