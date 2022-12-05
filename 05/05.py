from lsm.aoc import get_input
import re
from copy import deepcopy

task = get_input()
config, instructions = task.split('\n\n')
config = config.splitlines()[:-1]

qwto = []

for instruction in instructions.splitlines():
	m = re.match(r'move (\d+) from (\d+) to (\d+)', instruction)
	q, w, to = int(m.group(1)), int(m.group(2)), int(m.group(3))
	qwto.append((q, w, to))


def read_line(line: str) -> list[str]:
	items = []
	i = 0

	while i < len(line):
		item = line[i + 1]

		if item != ' ':
			items.append(item)
		else:
			items.append(None)

		i += 4

	return items

stacks = [*zip(*[read_line(line) for line in config])]
stacks = [[i for i in stack if i is not None] for stack in stacks]

def solve(stacks: list[str], part2: bool) -> str:
	stacks = deepcopy(stacks)

	for (q, w, to) in qwto:
		if part2:
			for i in range(q-1, -1, -1):
				stacks[to - 1].insert(0, stacks[w - 1].pop(i))

		else:
			for i in range(q):
				stacks[to - 1].insert(0, stacks[w - 1].pop(0))

	return ''.join([stack[0] for stack in stacks])


print('PART 1:', solve(stacks, False))
print('PART 2:', solve(stacks, True))
