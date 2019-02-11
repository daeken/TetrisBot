from ga import GA
from game import Game
from model import model
import numpy as np

def evaluate(chromosome):
	model.layers[0].set_weights([
		np.reshape(chromosome[:64 * 205], (205, 64)), 
		chromosome[64 * 205 + 32 * 64 + 4 * 32:64 * 205 + 32 * 64 + 4 * 32 + 64] * 10 - 5
	])
	model.layers[1].set_weights([
		np.reshape(chromosome[64 * 205:64 * 205 + 32 * 64], (64, 32)), 
		chromosome[64 * 205 + 32 * 64 + 4 * 32 + 64:64 * 205 + 32 * 64 + 4 * 32 + 64 + 32] * 10 - 5
	])
	model.layers[2].set_weights([
		np.reshape(chromosome[64 * 205 + 32 * 64:64 * 205 + 32 * 64 + 4 * 32], (32, 4)), 
		chromosome[64 * 205 + 32 * 64 + 4 * 32 + 64 + 32:64 * 205 + 32 * 64 + 4 * 32 + 64 + 32 + 4] * 10 - 5
	])

	game = Game()

	for i in xrange(1000):
		if game.lost:
			break

		inputs = list(reduce(lambda a, x: a + x, ([1 if x else 0 for x in row] for row in game.board[:20])))
		inputs.append(game.piecePosition[0] / 9.)
		inputs.append(game.piecePosition[1] / 22.)
		inputs.append(game.pieceRotation / 3.)
		inputs.append(game.currentPiece / 6.)
		inputs.append(game.nextPiece / 6.)

		output = model.predict(np.asarray([np.asarray(inputs)]))[0]

		top = sorted(enumerate(output), key=lambda x: x[1], reverse=True)

		if top[0][0] == 0:
			game.update('l')
		elif top[0][0] == 1:
			game.update('r')
		elif top[0][0] == 2:
			game.update('a')
		elif top[0][0] == 3:
			game.update('s')

	return game.score

ga = GA(
	64 * 205 + 32 * 64 + 4 * 32 + 64 + 32 + 4, 
	256, 
	999, 
	4, 2, 2, 
	1000, 0.1, 
	evaluate
)

while True:
	print 'Generation', ga.generation
	ga.next()
	best, avg = ga.fitnessHistory[-1]
	print 'Best score %i, average %i' % (best, avg)
