from lsm.aoc import get_input
from copy import copy
import re

class Monkey:

	def __init__(self, index: int, op: tuple[str, int], test: tuple[int, int, int]):
		self.index = index
		self.items = []
		self.op = op
		self.test = test
		self.score = 0
		self.div_total = 1

	def inspect(self, part2: bool):
		self.score += len(self.items)

		div, div_true, div_false = self.test
		op_func, op_value = self.op

		while self.items:
			item = self.items.pop(0)

			if item > self.div_total:
				item = item % self.div_total

			if op_func == '**':
				item = item * item
			elif op_func == '*':
				item = item * op_value
			else:
				item = item + op_value

			if not part2:
				item = item // 3

			if item % div == 0:
				yield item, div_true
			else:
				yield item, div_false

monkeys = []
monkey_items = []
div_total = 1

for i, monkey_text in enumerate(get_input().split('\n\n')):
	lines = monkey_text.splitlines()

	items = [int(i) for i in lines[1].split(':')[-1].split(', ')]
	if (m := re.search(r'new = old ([\*\+]) (\d+)', lines[2])):
		op = (m.group(1), int(m.group(2)))
	elif m := re.search(r'new = old \* old', lines[2]):
		op = ('**', 0)

	div = int(re.search(r'\d+', lines[3]).group(0))
	div_true = int(re.search(r'\d+', lines[4]).group(0))
	div_false = int(re.search(r'\d+', lines[5]).group(0))
	div_total *= div

	monkeys.append(Monkey(i, op, (div, div_true, div_false)))
	monkey_items.append(items)

for monkey in monkeys:
	monkey.div_total = div_total

ROUNDS = [20, 10_000]

for part, rounds_total in enumerate(ROUNDS):
	for monkey in monkeys:
		monkey.items = copy(monkey_items[monkey.index])
		monkey.score = 0

	for r in range(rounds_total):
		state = []

		for i, monkey in enumerate(monkeys):
			state.append(len(monkey.items))

			for item, new_monkey in monkey.inspect(part):
				monkeys[new_monkey].items.append(item)

	score = sorted([monkey.score for monkey in monkeys])[-2:]
	score = score[0] * score[1]
	print(f'PART {part + 1}: {score}')
