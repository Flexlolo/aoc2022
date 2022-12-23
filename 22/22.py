from lsm.aoc import get_input, get_input_filename
from lsm.aoc.space import get_directions
from lsm.aoc.vector import Vector
import re
from collections import defaultdict


grid = {}
bounds = [0, 0]
start = None

# read grid
grid_input, instructions = get_input().split('\n\n')

for y, line in enumerate(grid_input.splitlines()):
	for x, c in enumerate(line):
		if c == ' ':
			continue

		if start is None:
			start = Vector(x, y)

		grid[Vector(x, y)] = c

		if bounds[0] < x + 1:
			bounds[0] = x + 1

	if bounds[1] < y + 1:
		bounds[1] = y + 1

# parse instructions
instructions = re.findall(r'(\d+|[RL])', instructions)

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def part1():
	# generate warp points
	warps = {0: {}, 1: {}}

	for i, bound in enumerate(bounds):
		for pos in range(bound):
			w = []

			for fn, offset in ((min, -1), (max, +1)):
				r = (p[(i + 1) % 2] for p in grid if p[i] == pos)

				if i == 0:
					w.append(Vector(pos, fn(r) + offset))
				else:
					w.append(Vector(fn(r) + offset, pos))

			warps[i][w[0]] = w[1]
			warps[i][w[1]] = w[0]

	warp_index = [1, 0, 1, 0]
	facing = 0
	pos = start.copy()

	for instruction in instructions:
		if instruction in 'RL':
			if instruction == 'R':
				facing = (facing + 1) % 4
			else:
				facing = (facing - 1) % 4
		else:
			d = directions[facing]

			for step in range(int(instruction)):
				pos_new = pos + d

				if pos_new in warps[warp_index[facing]]:
					pos_new = warps[warp_index[facing]][pos_new] + d

				if pos_new in grid:
					if grid[pos_new] != '#':
						pos = pos_new
					else:
						break
	pos += (1, 1)
	return pos[1] * 1000 + pos[0] * 4 + facing

cube_adj_faces = {
	'f': ['r', 'bot', 'l', 't'],
	'bot': ['r', 'back', 'l', 'f'],
	'back': ['r', 't', 'l', 'bot'],
	't': ['r', 'f', 'l', 'back'],
	'l': ['f', 'bot', 'back', 't'],
	'r': ['back', 'bot', 'f', 't'],
}

def connections_to_faces(connections, face_size):
	faces = {}

	for key, values in connections.items():
		if not faces:
			face_name = 'f'
			face_rotation = 0
			faces[key] = ('f', face_rotation)
		else:
			face_name, face_rotation = faces[key]

		for value in values:
			d = tuple((value - key) // face_size)
			direction_index = directions.index(d)
			direction_index_rotated = (direction_index - face_rotation) % 4

			new_face_name = cube_adj_faces[face_name][direction_index_rotated]

			new_face_rotation = direction_index - 2 - cube_adj_faces[new_face_name].index(face_name)
			new_face_rotation = new_face_rotation % 4
			if new_face_rotation > 2:
				new_face_rotation -= 4

			faces[value] = (new_face_name, new_face_rotation)

	return faces

def pos_to_face(faces, face_size, pos):
	for s, (face, _) in faces.items():
		e = s + Vector(face_size - 1, face_size - 1)

		if pos.inside(s, e):
			return face

def part2():
	match get_input_filename():
		case 'test':
			face_size = 4

		case _:
			face_size = 50

	connections = defaultdict(list)
	seen = set()
	queue = [start.copy()]

	while queue:
		face = queue.pop(0)

		if face in seen:
			continue
		else:
			seen.add(face)

		for d in get_directions(ndim=2):
			face_next = face + Vector(d) * face_size
			if face_next in grid and face_next not in seen:
				queue.append(face_next)
				connections[face].append(face_next)

	connections = dict(connections)
	faces = connections_to_faces(connections, face_size)
	faces_map = {f[0]: (p, f[1]) for p, f in faces.items()}

	facing = 0
	pos = start.copy()

	for instruction in instructions:
		if instruction in 'RL':
			if instruction == 'R':
				facing = (facing + 1) % 4
			else:
				facing = (facing - 1) % 4
		else:
			for step in range(int(instruction)):
				d = directions[facing]
				pos_new = pos + d

				if pos_new not in grid:
					face = pos_to_face(faces, face_size, pos)
					face_start, face_rotation = faces_map[face]

					face_center = Vector(face_size - 1, face_size - 1) / 2
					pos_local = pos - face_start - face_center
					face_dir = facing - face_rotation % 4

					face_warp = cube_adj_faces[face][face_dir]
					face_warp_start, face_warp_rotation = faces_map[face_warp]

					rel_warp_rotation = facing - 2 - cube_adj_faces[face_warp].index(face)
					face_warp_rotation = (face_warp_rotation - rel_warp_rotation) % 4

					facing_new = (facing + face_warp_rotation) % 4

					for _ in range(face_warp_rotation):
						pos_local = Vector(-pos_local[1], pos_local[0])

					pos_new = face_center + pos_local + directions[facing_new]
					pos_new = face_warp_start + pos_new % face_size
					pos_new = Vector(int(p) for p in pos_new)

					if grid[pos_new] != '#':
						pos = pos_new
						facing = facing_new
					else:
						break
				else:
					if grid[pos_new] != '#':
						pos = pos_new
					else:
						break
	pos += (1, 1)
	return pos[1] * 1000 + pos[0] * 4 + facing

print('PART 1:', part1())
print('PART 2:', part2())