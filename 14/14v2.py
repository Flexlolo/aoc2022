from lsm.aoc import get_input
from lsm.aoc.vector import Vector

# down, down + left, down + right
sand_directions = ((0, 1), (-1, 1), (1, 1))

grid = {}
sand_source = Vector(500, 0)

# we use borders to check if sand goes to infinity in part 1
borders = {'min': sand_source.copy(), 'max': sand_source.copy()}

for line in get_input().splitlines():
	# build list of points from line
	points = []

	for point in line.split(' -> '):
		point = Vector(int(p) for p in point.split(','))
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
		step = points[i + 1] - points[i]
		steps = step.mlength
		step = step.clamp()

		for j in range(steps + 1):
			p = points[i] + step * j
			grid[p] = '#'

def simulate(grid, borders, sand, last_path, part2) -> bool:
	# part 2 exit
	if sand_source in sand:
		return False

	# part 1 infinity check
	def inside_borders(point):
		for k in range(2):
			if not (point[k] >= borders['min'][k] and point[k] <= borders['max'][k]):
				return False

		return True

	if last_path:
		last_path.pop(-1)

	if last_path:
		pos = last_path[-1]
	else:
		# start pos from source
		pos = sand_source.copy()

	# part 2 infinity floor line
	floor = borders['max'][1] + 2

	while part2 or inside_borders(pos):
		moved = False

		for direction in sand_directions:
			pos_new = pos + direction

			# if something is in the way
			if pos_new in grid or pos_new in sand:
				continue

			# if reached infinity floor in part 2
			if part2 and pos_new[1] >= floor:
				continue

			pos = pos_new
			last_path.append(pos)
			moved = True
			break

		if not moved:
			sand[pos] = 'o'
			return True

	return False

for part in range(1, 3):
	sand = {}
	last_path = []

	while simulate(grid, borders, sand, last_path, part == 2):
		continue

	print(f'PART {part}: {len(sand)}')