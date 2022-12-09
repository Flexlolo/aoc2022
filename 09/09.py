from lsm.aoc import get_input
from copy import copy

DIRECTIONS = {
	'R': [1, 0],
	'L': [-1, 0],
	'D': [0, 1],
	'U': [0, -1],
}

def is_touching(vector):
	for axis in vector:
		if abs(axis) > 1:
			return False

	return True

def clamp(vector):
	return [v//abs(v) if v else v for v in vector ]

def simulation_step(knots, vector):
	knots[0] = [knots[0][i] + vector[i] for i in range(2)]

	for knot_index in range(1, len(knots)):
		vector = [knots[knot_index-1][i] - knots[knot_index][i] for i in range(2)]

		if not is_touching(vector):
			knots[knot_index] = [knots[knot_index][i] + clamp(vector)[i] for i in range(2)]

def generate_knots(size):
	return [[0] * 2 for i in range(size)]

parts = [generate_knots(2), generate_knots(10)]
visited = [set(), set()]

for line in get_input().splitlines():
	d, count = line.split(' ')
	vector = DIRECTIONS[d]

	for i in range(int(count)):
		for i, knots in enumerate(parts):
			simulation_step(knots, vector)
			visited[i].add(str(parts[i][-1]))

print('PART 1:', len(visited[0]))
print('PART 2:', len(visited[1]))