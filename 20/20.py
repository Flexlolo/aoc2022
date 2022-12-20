from lsm.aoc import get_input
from copy import copy

def mix(numbers, times: int):
	result = copy(numbers)

	for _ in range(times):
		for i in range(len(numbers)):
			n = numbers[i]
			offset = n[1]

			if offset == 0:
				continue

			pos = result.index(n)
			pos_new = (pos + offset) % (len(result) - 1)

			del result[pos]
			result.insert(pos_new, n)

	return result

def answer(numbers):
	result = [r[1] for r in numbers]
	total = 0 

	for pos in (1000, 2000, 3000):
		index = (result.index(0) + pos) % len(result)
		total += result[index]

	return total

part1 = [(i, int(n)) for i, n in enumerate(get_input().splitlines())]
constant = 811589153
part2 = [(i, int(n) * constant) for i, n in enumerate(get_input().splitlines())]

print('PART 1:', answer(mix(part1, 1)))
print('PART 2:', answer(mix(part2, 10)))