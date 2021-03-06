from game import Game

game = Game()

while True:
	print
	print 'Score:', game.score
	pp = game.getPiecePieces()

	delta = game.findLowestDelta()
	if delta == 0:
		mdir = 0
	elif delta < 0:
		mdir = -1
	else:
		mdir = 1

	print 'Delta:', mdir
	print 'Flat landing:', game.calculateFlatLanding()
	for y, row in list(enumerate(game.board))[::-1]:
		print ''.join('#' if v else ('*' if (x, y) in pp else '.') for x, v in enumerate(row))
	print
	game.update(raw_input())

	if game.lost:
		print 'LOST THE GAME'
		break
