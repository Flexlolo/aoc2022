from lsm.aoc import get_input
from itertools import product


grid = {}

for x, line in enumerate(get_input().splitlines()):
	for y, c in enumerate(line):
		grid[(x, y)] = int(c)

X = max([c[0] for c in grid]) + 1
Y = max([c[1] for c in grid]) + 1
assert X == Y

DIM = X

def is_visible(point: tuple[int, int]) -> bool:
	x, y = point

	DIRECTIONS = {
		(-1, 0): (range(x), None),
		(1, 0): (range(x + 1, DIM), None),
		(0, -1): (None, range(y)),
		(0, 1): (None, range(y + 1, DIM)),
	}

	for rx, ry in DIRECTIONS.values():
		rx = rx if rx else [x] * DIM
		ry = ry if ry else [y] * DIM
		m = max(grid[p] for p in zip(rx, ry))

		if m < grid[point]:
			return True

	return False

def scenic_score(point: tuple[int, int]) -> int:
	x, y = point

	DIRECTIONS = {
		(-1, 0): (range(x-1, -1, -1), None),
		(1, 0): (range(x + 1, DIM), None),
		(0, -1): (None, range(y-1, -1, -1)),
		(0, 1): (None, range(y + 1, DIM)),
	}

	score = 1

	for rx, ry in DIRECTIONS.values():
		rx = rx if rx else [x] * DIM
		ry = ry if ry else [y] * DIM

		for i, p in enumerate(zip(rx, ry)):
			if grid[p] >= grid[point]:
				break

		score *= i + 1

	return score

invisible = 0
best_score = 0

for point in product(range(DIM), range(DIM)):
	if True in [p == 0 or p == DIM - 1 for p in point]:
		continue

	if not is_visible(point):
		invisible += 1

	score = scenic_score(point)

	if score > best_score:
		best_score = score

print('PART 1:', DIM ** 2 - invisible)
print('PART 2:', best_score)