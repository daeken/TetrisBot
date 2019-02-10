import random

BOARD_WIDTH  = 10
BOARD_HEIGHT = 30

pieceShapes = (
	[
		[0, 0, 0, 0], 
		[1, 1, 1, 1], 
		[0, 0, 0, 0], 
		[0, 0, 0, 0]
	], 
	[
		[0, 1, 1, 0], 
		[0, 1, 1, 0], 
		[0, 0, 0, 0], 
		[0, 0, 0, 0]
	], 
	[
		[1, 0, 0], 
		[1, 1, 1], 
		[0, 0, 0]
	], 
	[
		[0, 0, 1], 
		[1, 1, 1], 
		[0, 0, 0]
	], 
	[
		[0, 1, 1], 
		[1, 1, 0], 
		[0, 0, 0]
	], 
	[
		[0, 1, 0], 
		[1, 1, 1], 
		[0, 0, 0]
	], 
	[
		[1, 1, 0], 
		[0, 1, 1], 
		[0, 0, 0]
	]
)

KICK = {
	0x01: [(-1, 0), (-1, 1), (0,-2), (-1,-2)], 
	0x10: [( 1, 0), ( 1,-1), (0, 2), ( 1, 2)], 
	0x12: [( 1, 0), ( 1,-1), (0, 2), ( 1, 2)], 
	0x21: [(-1, 0), (-1, 1), (0,-2), (-1,-2)], 
	0x23: [( 1, 0), ( 1, 1), (0,-2), ( 1,-2)], 
	0x32: [(-1, 0), (-1,-1), (0, 2), (-1, 2)], 
	0x30: [(-1, 0), (-1,-1), (0, 2), (-1, 2)], 
	0x03: [( 1, 0), ( 1, 1), (0,-2), ( 1,-2)]
}

IKICK = {
	0x01: [(-2, 0), ( 1, 0), (-2,-1), ( 1, 2)], 
	0x10: [( 2, 0), (-1, 0), ( 2, 1), (-1,-2)], 
	0x12: [(-1, 0), ( 2, 0), (-1, 2), ( 2,-1)], 
	0x21: [( 1, 0), (-2, 0), ( 1,-2), (-2, 1)], 
	0x23: [( 2, 0), (-1, 0), ( 2, 1), (-1,-2)], 
	0x32: [(-2, 0), ( 1, 0), (-2,-1), ( 1, 2)], 
	0x30: [( 1, 0), (-2, 0), ( 1,-2), (-2, 1)], 
	0x03: [(-1, 0), ( 2, 0), (-1, 2), ( 2,-1)]
}

pieces = []
for shape in pieceShapes:
	shape = [[x == 1 for x in row] for row in shape[::-1]]
	all = []
	for i in xrange(4):
		all.append(shape)
		shape = zip(*shape[::-1])
	pieces.append(all)

class Game(object):
	def __init__(self):
		self.score = 0
		self.board = [[False] * BOARD_WIDTH for i in xrange(BOARD_HEIGHT)]
		self.lost = False

		self.currentPiece = None
		self.piecePosition = None
		self.pieceRotation = 0
		self.nextPiece = random.randrange(7)

		self.bakePiece()

	def update(self, command=None):
		def translate(x):
			ox, oy = self.piecePosition
			self.piecePosition = ox + x, oy
			if self.findCollision():
				self.piecePosition = ox, oy

		if command == 'l':
			translate(-1)
		elif command == 'r':
			translate(1)
		elif command == 'a':
			self.rotate(True)
		elif command == 's':
			self.rotate(False)

		ox, oy = self.piecePosition
		self.piecePosition = ox, oy - 1
		if self.findCollision():
			self.piecePosition = ox, oy
			self.bakePiece()

	def bakePiece(self):
		if self.currentPiece is not None:
			for x, y in self.getPiecePieces():
				if x >= 0 and x < BOARD_WIDTH and y >= 0 and y < BOARD_HEIGHT:
					self.board[y][x] = True
			self.score += 1
			for y in xrange(21, -1, -1):
				if False in self.board[y]:
					continue
				self.board = self.board[:y] + self.board[y + 1:] + [[False] * BOARD_WIDTH]
				self.score += 100

		self.currentPiece = self.nextPiece
		self.nextPiece = random.randrange(7)
		self.pieceRotation = 0

		if self.currentPiece <= 1:
			self.piecePosition = (3, 21)
		else:
			self.piecePosition = (1, 21)

		if self.findCollision():
			self.lost = True

	def rotate(self, cw):
		orot = self.pieceRotation
		self.pieceRotation = (self.pieceRotation + 4 + (1 if cw else -1)) % 4
		if not self.findCollision():
			return

		ox, oy = self.piecePosition
		kt = (IKICK if self.currentPiece == 0 else KICK)[(orot << 4) | self.pieceRotation]
		for kx, ky in kt:
			self.piecePosition = ox + kx, oy + ky
			if not self.findCollision():
				return
		self.piecePosition = ox, oy
		self.pieceRotation = orot

	def getPiecePieces(self):
		cpiece = pieces[self.currentPiece][self.pieceRotation]
		pp = []
		for y, row in enumerate(cpiece):
			for x, v in enumerate(row):
				if v:
					pp.append((self.piecePosition[0] + x, self.piecePosition[1] + y))
		return pp

	def findCollision(self):
		for x, y in self.getPiecePieces():
			if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT or self.board[y][x]:
				return True
		return False
