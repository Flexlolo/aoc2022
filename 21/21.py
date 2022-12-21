from lsm.aoc import get_input
from copy import deepcopy
import re

class HUMN:

	def __init__(self):
		# value expressed as nX + y
		self.value = [1, 0]

	def calc(self, x):
		return self.value[0] * x + self.value[1]

	def solve(self, answer):
		return (answer - self.value[1]) / self.value[0]

	def __add__(self, y):
		self.value[1] += y
		return self

	def __sub__(self, y):
		self.value[1] -= y
		return self

	def __mul__(self, y):
		self.value = [v * y for v in self.value]
		return self

	def __floordiv__(self, y):
		self.value = [v / y for v in self.value]
		return self

	def __str__(self):
		return f'{self.value[0]} * X + {self.value[1]}'

	__repr__ = __str__

ops = {
	'+': lambda x,y: x + y,
	'-': lambda x,y: x - y,
	'*': lambda x,y: x * y,
	'/': lambda x,y: x // y
}

monkeys = {}

for line in get_input().splitlines():
	if (m := re.match(r'(\S+): (\d+)', line)):
		monkeys[m.group(1)] = int(m.group(2))

	if (m := re.match(r'(\S+): (\S+) ([\+\-\*\/]) (\S+)', line)):
		monkeys[m.group(1)] = (m.group(2), m.group(4), m.group(3))

def solve(monkeys, name, part2):
	if isinstance(monkeys[name], int):
		if name == 'humn':
			return HUMN()
		else:
			return monkeys[name]
	else:
		m1, m2 = monkeys[name][0], monkeys[name][1]
		op_code = monkeys[name][2]
		op = ops[op_code]
		m1, m2 = solve(monkeys, m1, part2=part2), solve(monkeys, m2, part2=part2)

		if name == 'root':
			if part2:
				print('SOLVE:', m1, '=', m2)

				if isinstance(m1, HUMN):
					return m1.solve(m2)
				else:
					return m2.solve(m1)
			else:
				if isinstance(m1, HUMN):
					m1 = m1.calc(monkeys['humn'])
				else:
					m2 = m2.calc(monkeys['humn'])

		if isinstance(m2, HUMN):
			if op_code == '+':
				monkeys[name] = m2 + m1
			elif op_code == '-':
				monkeys[name] = (m2 * -1) + m1
			elif op_code == '/':
				print("UH OH")
				return
			elif op_code == '*':
				monkeys[name] = m2 * m1
		else:
			monkeys[name] = op(m1, m2)

		return monkeys[name]

print('PART 1:', solve(deepcopy(monkeys), 'root', False))
print('PART 2:', solve(deepcopy(monkeys), 'root', True))