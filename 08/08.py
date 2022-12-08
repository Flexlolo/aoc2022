from lsm.aoc import get_input
from lsm.aoc.space import get_directions, point_step
from itertools import product

directions = get_directions(2)
space = {}

for y, line in enumerate(get_input().splitlines()):
	for x, c in enumerate(line):
		space[(x, y)] = int(c)

SIZE = x + 1

def is_visible(point) -> bool:
	def is_visible_dir(direction):
		for p in point_step(point, direction, space):
			if space[p] >= space[point]:
				return False

		return True

	return True in (is_visible_dir(direction) for direction in directions)

def scenic_score(point) -> int:
	score = 1

	for direction in directions:
		i = 0

		for i, p in enumerate(point_step(point, direction, space)):
			if space[p] >= space[point]:
				break

		score *= i + 1

	return score

visible = 0
best_score = 0

for point in product(range(SIZE), range(SIZE)):
	if is_visible(point):
		visible += 1

	score = scenic_score(point)

	if score > best_score:
		best_score = score

print('PART 1:', visible)
print('PART 2:', best_score)