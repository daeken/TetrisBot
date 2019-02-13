import random

BOARD_WIDTH  = 10
BOARD_HEIGHT = 23

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
		self.cleared = 0
		self.board = [[False] * BOARD_WIDTH for i in xrange(BOARD_HEIGHT)]
		self.lost = False

		self.currentPiece = None
		self.piecePosition = None
		self.pieceRotation = 0
		self.nextPiece = random.randrange(7)

		self.bakePiece()

	def update(self, command=''):
		def translate(x):
			ox, oy = self.piecePosition
			self.piecePosition = ox + x, oy
			if self.findCollision():
				self.piecePosition = ox, oy

		if command.startswith('l'):
			command = command[1:]
			translate(-1)
		elif command.startswith('r'):
			command = command[1:]
			translate(1)
		if command.startswith('a'):
			command = command[1:]
			self.rotate(True)
		elif command.startswith('s'):
			command = command[1:]
			self.rotate(False)

		ox, oy = self.piecePosition
		self.piecePosition = ox, oy - 1
		if self.findCollision():
			self.piecePosition = ox, oy
			self.bakePiece()
		elif command == 'd':
			self.update('d')

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
				self.score += 10
				self.cleared += 1

		self.currentPiece = self.nextPiece
		self.nextPiece = random.randrange(7)
		self.pieceRotation = 0

		if self.currentPiece <= 1:
			self.piecePosition = (3, 19)
		else:
			self.piecePosition = (1, 19)

		if self.findCollision():
			self.lost = True
			#self.score -= 10000

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

	def calculateFlatLanding(self):
		pc = {}
		pp = self.getPiecePieces()
		left = min(*[px for px, _ in pp])
		for piece in pp:
			piece = piece[0], piece[1]
			if piece[0] not in pc:
				pc[piece[0]] = piece[1]
			else:
				pc[piece[0]] = min(piece[1], pc[piece[0]])
		if len(pc) == 1:
			return 1
		hab = max(*pc.values()) - min(*pc.values())
		bottom = min(*pc.values())
		columns = [[j for j, row in enumerate(self.board) if row[i]][::-1] + [-1] if i in pc.keys() else [-1] for i in xrange(10)]
		
		tc = max(*map(max, columns))
		if tc == -1:
			return 1
		tpos = [i for i, v in enumerate(columns) if v[0] == tc][0]

		bdelta = pc[tpos] - columns[tpos][0]
		
		flat = 0
		for i, ph in pc.items():
			column = columns[i]
			if ph - bdelta == column[0]:
				flat += 1

		return flat / float(len(pc))

	def findLowestDelta(self):
		pp = self.getPiecePieces()
		left = min(*[px for px, _ in pp])
		ox, oy = self.piecePosition
		all = []
		for i in xrange(-10, 10):
			self.piecePosition = ox + i, oy
			if self.findCollision():
				continue
			flatness = self.calculateFlatLanding()
			cy = oy
			while cy >= 0:
				cy -= 1
				self.piecePosition = ox + i, cy
				if self.findCollision():
					break
			all.append((i, cy, flatness))
		self.piecePosition = ox, oy
		all = sorted(all, key=lambda x: x[2], reverse=True)
		all = [x[:2] for x in all if x[2] == all[0][2]]
		all = sorted(all, key=lambda x: x[1])
		all = sorted((x[0] for x in all if x[1] == all[0][1]), key=abs)
		return all[0]
