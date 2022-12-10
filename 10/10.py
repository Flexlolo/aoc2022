from lsm.aoc import get_input
from collections import defaultdict


class CPU:

	def __init__(self):
		self.registers = {'X': 1}
		self.clock = 0

	def set_interrupt(self, callback):
		self.callback = callback

	def cycle(self, steps: int):
		for step in range(steps):
			self.clock += 1
			self.callback(self)

	def instruction(self, string: str):
		match string.split():
			case ['noop']:
				self.cycle(1)

			case ['addx', value]:
				self.cycle(2)
				self.registers['X'] += int(value)

class CRT:

	def __init__(self):
		self.buffer = []

	def cpu_interrupt_callback(self, cpu):
		sprite = [cpu.registers['X'] + i for i in (-1, 0, +1)]

		if (cpu.clock - 1) % 40 in sprite:
			self.buffer.append('#')
		else:
			self.buffer.append(' ')

instructions = get_input().splitlines()

crt = CRT()
cpu = CPU()

total = 0

def interrupt_callback(cpu):
	global total

	if cpu.clock in (20, 60, 100, 140, 180, 220):
		signal = cpu.clock * cpu.registers['X']
		total = total + signal

	crt.cpu_interrupt_callback(cpu)

cpu.set_interrupt(interrupt_callback)

for instruction in instructions:
	cpu.instruction(instruction)

print('PART 1:', total)
print('PART 2:')
print('\n'.join([''.join(chunk) for chunk in zip(*(iter(crt.buffer),) * 40)]))