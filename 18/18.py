from lsm.aoc import get_input
from lsm.aoc.space import get_directions
from lsm.aoc.vector import Vector

cubes = set()

for line in get_input().splitlines():
	position = Vector(int(p) for p in line.split(','))
	cubes.add(position)

total = 0

for direction in get_directions(ndim=3):
	for cube in cubes:
		if cube + direction not in cubes:
			total += 1

print('PART 1:', total)

is_pocket_cache = {}

def is_pocket(point, max_len):
	global is_pocket_cache

	if point in is_pocket_cache:
		return is_pocket_cache[point]

	queue = [(point, 0)]
	seen = set()

	while queue:
		p, length = queue.pop(0)

		if length > max_len:
			for p in seen:
				is_pocket_cache[p] = False

			return False

		if p in seen:
			continue

		seen.add(p)

		for direction in get_directions(ndim=3):
			pd = p + direction

			if pd not in cubes and pd not in seen:
				queue.append((p + direction, length + 1))

	for p in seen:
		is_pocket_cache[p] = True

	return True

total = 0

for cube in cubes:
	for direction in get_directions(ndim=3):
		direction = Vector(direction)
		if cube + direction not in cubes:
			if not is_pocket(cube + direction, 32):
				total += 1

print('PART 2:', total)