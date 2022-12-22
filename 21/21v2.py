from lsm.aoc import get_input
from lsm.aoc.vector import Vector
import re


monkeys = {}

for line in get_input().splitlines():
	if (m := re.match(r'(\S+): (\d+)', line)):
		# represent as (0 * x + value)
		monkeys[m.group(1)] = Vector(0, int(m.group(2)))

	if (m := re.match(r'(\S+): (\S+) ([\+\-\*\/]) (\S+)', line)):
		monkeys[m.group(1)] = (m.group(3), m.group(2), m.group(4))

def compute(name):
	if isinstance(monkeys[name], Vector):
		if name == 'humn':
			# humn is just x
			return Vector(1, 0)
		else:
			return monkeys[name]
	else:
		op = monkeys[name][0]
		ms = [compute(n) for n in monkeys[name][1:]]

		if op == '+':
			return ms[0] + ms[1]

		elif op == '-':
			return ms[0] - ms[1]

		elif op == '*':
			for i in range(2):
				if ms[i][0] != 0:
					return ms[i] * ms[(i + 1) % 2][1]

			return Vector(0, ms[0][1] * ms[1][1])

		elif op == '/':
			if ms[0][0] != 0:
				return ms[0] / ms[1][1]
			else:
				return Vector(0, ms[0][1] / ms[1][1])

root_op = monkeys['root'][0]
root = [compute(m) for m in monkeys['root'][1:]]
humn_index = [m[0] != 0 for m in root].index(True)

# convert humn to int
assert root_op == '+'
part1 = root[humn_index][0] * monkeys['humn'][1] + root[humn_index][1]
part1 += root[1][1]
print('PART 1:', int(part1))

# solve x
part2 = (root[1][1] - root[humn_index][1]) / root[humn_index][0]
print('PART 2:', int(part2))