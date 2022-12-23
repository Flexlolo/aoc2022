from lsm.aoc import get_input
from lsm.aoc.vector import Vector
from collections import defaultdict


grid = set()

for y, line in enumerate(get_input().splitlines()):
	for x, c in enumerate(line):
		if c == '#':
			grid.add(Vector(x, y))

# N, S, W, E
directions = ((0, -1), (0, 1), (-1, 0), (1, 0))
diagonals = ((-1, -1), (1, -1), (-1, 1), (1, 1))
adjacent = (*directions, *diagonals)


direction_checks = [
	[(-1, -1), (0, -1), (1, -1)],
	[(-1, 1), (0, 1), (1, 1)],
	[(-1, -1), (-1, 0), (-1, 1)],
	[(1, -1), (1, 0), (1, 1)],
]

def count_neighbours(grid, pos):
	count = 0

	for d in adjacent:
		if pos + d in grid:
			count += 1

	return count

def check_direction(grid, pos, direction):
	for check in direction_checks[direction]:
		if pos + check in grid:
			return False

	return True

def get_bounds(grid):
	bounds = [set((p[i] for p in grid)) for i in range(2)]
	bounds = [(min(b), max(b)) for b in bounds]
	return bounds

def draw_grid(grid):
	bounds = get_bounds(grid)

	for y in range(bounds[1][0], bounds[1][1] + 1):
		line = []

		for x in range(bounds[0][0], bounds[0][1] + 1):
			point = Vector(x, y)

			if point in grid:
				line.append('#')
			else:
				line.append('.')

		print(''.join(line))

def simulate(grid, offset):
	candidates = defaultdict(list)
	grid_new = set()

	for pos in grid:
		moved = False

		if count_neighbours(grid, pos) > 0:
			for i in range(4):
				direction = (i + offset) % 4

				if check_direction(grid, pos, direction):
					pos_new = pos + directions[direction]
					candidates[pos_new].append(pos)
					moved = True
					break

		if not moved:
			grid_new.add(pos)

	for pos, elfs in candidates.items():
		if len(elfs) == 1:
			grid_new.add(pos)
		else:
			for old_pos in elfs:
				grid_new.add(old_pos)

	return grid_new

def get_score(grid):
	bounds = get_bounds(grid)
	score = 0

	for x in range(bounds[0][0], bounds[0][1] + 1):
		for y in range(bounds[1][0], bounds[1][1] + 1):
			point = Vector(x, y)

			if point not in grid:
				score += 1

	return score

rounds = 0
while True:
	if rounds % 10 == 0:
		print(f'STEP {rounds}')

	grid_new = simulate(grid, rounds)
	rounds += 1

	if grid_new == grid:
		print(f'STOPPED MOVING AFTER {rounds} ROUNDS')
		break

	grid = grid_new

	if rounds == 10:
		print('PART 1:', get_score(grid))