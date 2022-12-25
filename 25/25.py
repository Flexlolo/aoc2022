from lsm.aoc import get_input
from collections import defaultdict


mapping = {
	'2': 2,
	'1': 1,
	'0': 0,
	'-': -1,
	'=': -2,
}

reverse_mapping = {v: k for k, v in mapping.items()}

def snafu_to_int(value: str) -> int:
	total = 0

	for i, c in enumerate(reversed(value)):
		total += mapping[c] * 5 ** i

	return total

def find_biggest_power(value: int):
	biggest = 0

	while True:
		biggest += 1

		if value < 5 ** biggest:
			return biggest - 1

def int_to_snafu(value: int) -> str:
	magnitudes = defaultdict(int)

	while value > 0:
		power = find_biggest_power(value)
		whole = value // 5 ** power
		rem = value % 5 ** power

		magnitudes[power] += whole
		value = rem

	while True:
		done = True

		for i in range(max(magnitudes.keys()) + 1):
			if magnitudes[i] > 5:
				magnitudes[i + 1] += magnitudes[i] // 5
				magnitudes[i] = magnitudes[i] % 5
				done = False
			elif magnitudes[i] > 2:
				magnitudes[i + 1] += 1
				magnitudes[i] -= 5
				done = False

		if done:
			break

	string = ''

	for i in range(max(magnitudes.keys()) + 1):
		string = reverse_mapping[magnitudes[i]] + string

	return string

total = 0

for line in get_input().splitlines():
	total += snafu_to_int(line)

print('PART 1:', int_to_snafu(total))