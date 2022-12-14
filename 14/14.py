from lsm.aoc import get_input
from copy import copy, deepcopy

grid = {}

# we use borders to check if sand goes to infinity in part 1
borders = {'min': [500, 0], 'max': [500, 0]}

for line in get_input().splitlines():
	# build list of points from line
	points = []

	for point in line.split(' -> '):
		point = tuple(int(p) for p in point.split(','))
		points.append(point)

		# update min/max borders
		for corner, corner_point in borders.items():
			for k in range(2):
				if corner == 'min':
					if point[k] < corner_point[k]:
						corner_point[k] = point[k]
				else:
					if point[k] > corner_point[k]:
						corner_point[k] = point[k]

	# draw lines on a grid from pairs of points
	for i in range(len(points) - 1):
		step = [points[i + 1][k] - points[i][k] for k in range(2)]
		steps = sum(abs(s) for s in step)
		step = [s // abs(s) if s else 0 for s in step]

		for j in range(steps + 1):
			p = tuple(points[i][k] + step[k] * j for k in range(2))
			grid[p] = '#'

def simulate(grid, borders, source, part2) -> bool:
	# part 2 exit
	if source in grid:
		return False

	# part 1 infinity check
	def inside_borders(point):
		for k in range(2):
			if not (point[k] >= borders['min'][k] and point[k] <= borders['max'][k]):
				return False

		return True

	# down, down + left, down + right
	directions = ((0, 1), (-1, 1), (1, 1))

	# start pos from source
	pos = copy(source)

	# part 2 infinity floor line
	floor = borders['max'][1] + 2

	while part2 or inside_borders(pos):
		moved = False

		for direction in directions:
			pos_new = tuple(pos[k] + direction[k] for k in range(2))

			# if something is in the way
			if pos_new in grid:
				continue

			# if reached infinity floor in part 2
			if part2:
				if pos_new[1] >= floor:
					continue

			pos = pos_new
			moved = True
			break

		if not moved:
			grid[pos] = 'o'
			return True

	return False


grids = [grid, deepcopy(grid)]

for part in range(1, 3):
	total = 0

	while simulate(grids[part - 1], borders, (500, 0), part == 2):
		total += 1

	print(f'PART {part}: {total}')