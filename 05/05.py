from lsm.aoc import get_input
import re
from copy import deepcopy

task = get_input()
config, instructions = task.split('\n\n')
config = config.splitlines()[:-1]

stacks = [[line[i] for i in range(1, len(line), 4)] for line in config]
stacks = [*zip(*stacks)]
stacks = [[i for i in stack if i != ' '] for stack in stacks]

state = [deepcopy(stacks) for part in range(2)]

for instruction in instructions.splitlines():
	m = re.match(r'move (\d+) from (\d+) to (\d+)', instruction)
	q, w, to = int(m.group(1)), int(m.group(2)), int(m.group(3))

	for part in range(2):
		if part:
			for i in range(q-1, -1, -1):
				state[part][to - 1].insert(0, state[part][w - 1].pop(i))
		else:
			for i in range(q):
				state[part][to - 1].insert(0, state[part][w - 1].pop(0))

state = [''.join([s[0] for s in st]) for st in state]

print('PART 1:', state[0])
print('PART 2:', state[1])