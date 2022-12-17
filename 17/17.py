from lsm.aoc import get_input
from lsm.aoc.vector import Vector

shapes = []

with open('shapes.txt') as f:
	for shape in f.read().split('\n\n'):
		shape_points = []

		lines = shape.splitlines()
		for y in range(len(lines)):
			for x, c in enumerate(lines[len(lines) - y - 1]):
				if c == '#':
					shape_points.append(Vector(float(x), float(y)))

		shape_bounds = [(min(p[i] for p in shape_points), max(p[i] for p in shape_points)) for i in range(2)]
		shape_center = Vector(b[0] + b[1] / 2 for b in shape_bounds)
		points_rel = tuple(p - shape_center for p in shape_points)
		bounds_rel = tuple((min(p[i] for p in points_rel), max(p[i] for p in points_rel)) for i in range(2))

		shape = {
			'center': shape_center, 
			'points': points_rel,
			'bounds': bounds_rel
		}
		shapes.append(shape)

jets = []

for c in get_input():
	if c == '>':
		jets.append((1, 0))
	else:
		jets.append((-1, 0))

def check_collision(grid, grid_bounds, shape, position):
	for point in shape['points']:
		p = position + point 

		if p in grid:
			return True

		if p[0] <= grid_bounds[0] or p[0] >= grid_bounds[1]:
			return True

		if p[1] <= 0:
			return True

	return False

def guess_seq_len(seq, min_len = 10):
	guess = 1
	max_len = int(len(seq) / 2)
	for x in range(min_len, max_len):
		if seq[0:x] == seq[x:2*x] :
			return x

	return guess

def solve(steps: int) -> int:
	jet_index = -1
	grid = set()
	grid_y_max = 0
	grid_bounds = [0, 8]
	grid_gaps = (3, 4)
	vector_down = Vector(0, -1)
	max_incr = []

	for step in range(steps):
		shape_index = step % len(shapes)
		shape = shapes[shape_index]

		position = Vector([shape['center'][i] * 2 + shape['bounds'][i][0] + grid_gaps[i] for i in range(2)])
		position += (0, grid_y_max)

		while True:
			jet_index = (jet_index + 1) % len(jets)
			jet = jets[jet_index]

			position_new = position + jet

			if not check_collision(grid, grid_bounds, shape, position_new):
				position = position_new

			position_new = position + vector_down

			if check_collision(grid, grid_bounds, shape, position_new):
				for point in shape['points']:
					p = position + point
					grid.add(p)

				shape_highest = position[1] + shape['bounds'][1][1]

				if shape_highest > grid_y_max:
					max_incr.append(int(shape_highest - grid_y_max))
					grid_y_max = shape_highest
				else:
					max_incr.append(0)

				break
			else:
				position = position_new
	
		if step > len(jets) * 2:
			half = int(len(max_incr) / 2)

			for offset in range(half, half * 2):
				pattern_length = guess_seq_len(max_incr[offset:])

				if pattern_length > 1:
					print(f'{pattern_length=} {offset=}')
					pattern = max_incr[offset:offset + pattern_length]
					pattern_length = guess_seq_len(max_incr[offset:])
					pattern_sum = sum(pattern)

					total = sum(max_incr[:offset])
					repetitions = (steps - offset) // pattern_length
					total += repetitions * pattern_sum

					total_steps = offset + repetitions * pattern_length

					i = 0

					while total_steps < steps:
						total += pattern[i]
						total_steps += 1
						i += 1

					return total

	return int(grid_y_max)

print('PART 1:', solve(2022))
print('PART 2:', solve(1_000_000_000_000))