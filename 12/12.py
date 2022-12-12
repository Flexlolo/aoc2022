from lsm.aoc import get_input


class Node:

	def __init__(self, position: tuple[int, int], value: int):
		self.position = position
		self.value = value
		self.edges = []

	def __str__(self):
		return f'NODE <{self.position}> {chr(self.value)}'

	__repr__ = __str__

nodes = {}
path = {}

for y, line in enumerate(get_input().splitlines()):
	for x, char in enumerate(line):
		position = (x, y)

		if char == 'S':
			path['S'] = position
			char = 'a'
		elif char == 'E':
			path['E'] = position
			char = 'z'

		node = Node(position, ord(char))
		nodes[position] = node

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))

for position, node in nodes.items():
	for direction in DIRECTIONS:
		neighbour = tuple(position[i] + direction[i] for i in range(2))

		if neighbour in nodes:
			nnode = nodes[neighbour]
			elevation = nnode.value - node.value

			if elevation > 1:
				continue

			node.edges.append(nnode)

path['S'] = nodes[path['S']]
path['E'] = nodes[path['E']]

nodes = list(nodes.values())

def bfs(nodes, start, end):
	seen = set()
	queue = [(start, 0)]

	while queue:
		(node, distance) = queue.pop(0)

		if node in seen:
			continue
		else:
			seen.add(node)

		if node == end:
			return distance

		for adj in node.edges:
			queue.append((adj, distance + 1))

distances = {}

for start in nodes:
	if start.value == 97:
		distance = bfs(nodes, start, path['E'])

		if distance:
			distances[start] = distance


print('PART 1:', distances[path['S']])
print('PART 2:', min(distances.values()))
