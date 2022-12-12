from lsm.aoc import get_input


DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))

start = (-1, -1)
end = (-1, -1)
nodes = {}

for y, line in enumerate(get_input().splitlines()):
	for x, char in enumerate(line):
		position = (x, y)

		if char == 'S':
			start = position
			char = 'a'
		elif char == 'E':
			end = position
			char = 'z'

		nodes[position] = ord(char)

def solve(part2: bool):
	seen = set()
	
	if part2:
		queue = [(end, 0)]
	else:
		queue = [(start, 0)]

	while queue:
		position, distance = queue.pop(0)

		if position in seen:
			continue

		seen.add(position)

		if part2:
			if nodes[position] == ord('a'):
				return distance
		else:
			if position == end:
				return distance

		for direction in DIRECTIONS:
			neighbour = tuple(position[i] + direction[i] for i in range(2))

			if neighbour in nodes and neighbour not in seen:
				if part2:
					if nodes[position] - nodes[neighbour] < 2:
						queue.append((neighbour, distance + 1))

				else:
					if nodes[neighbour] - nodes[position] < 2:
						queue.append((neighbour, distance + 1))

print('PART 1:', solve(False))
print('PART 2:', solve(True))