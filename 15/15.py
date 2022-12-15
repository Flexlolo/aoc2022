from lsm.aoc import get_input, get_input_filename
from lsm.aoc.vector import Vector
import re

lines = []

for line in get_input().splitlines():
	m = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line)

	s = Vector(int(m.group(1)), int(m.group(2)))
	b = Vector(int(m.group(3)), int(m.group(4)))
	v = b - s

	lines.append((s, b, v))

# https://www.geeksforgeeks.org/merging-intervals/
def merge_intervals(intervals) -> int:
	intervals.sort()
	stack = []
	stack.append(intervals[0])
	
	for i in intervals[1:]:
		if stack[-1][0] <= i[0] <= stack[-1][-1]:
			stack[-1][-1] = max(stack[-1][-1], i[-1])
		else:
			stack.append(i)

	return stack 

def check_row(row: int, part2: bool) -> int:
	coverage = []

	if row % 10_000 == 0:
		print('checking row', row)

	for (s, b, v) in lines:
		if (s[1] <= row and s[1] + v.mlength >= row) or (s[1] > row and s[1] - v.mlength <= row):
			ds = v.mlength - abs(s[1] - row)
			coverage.append([s[0] - ds, s[0] + ds])

	intervals = merge_intervals(coverage)

	if part2:
		if len(intervals) > 1:
			for i in range(len(intervals) - 1):
				gap = intervals[i + 1][0] - intervals[i][1]

				if gap > 1:
					return intervals[i][1] + 1

		return None

	else:
		total = 0

		for r in intervals:
			total += r[1] - r[0]

		return total

row_middle = {'test': 10, 'input': 2_000_000}
row_middle = row_middle[get_input_filename()]

print('PART 1:', check_row(row_middle, False))

for row in range(row_middle, row_middle * 2):
	x = check_row(row, True)

	if x is not None:
		print('PART 2:', x * 4000000 + row)
		break
