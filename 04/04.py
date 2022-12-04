from lsm.aoc import get_input

def get_range(r: str) -> set[int]:
	s, e = (int(p) for p in r.split('-'))
	return set(i for i in range(s, e + 1))

counter = [0, 0]

for line in get_input().splitlines():
	r = [get_range(p) for p in line.split(',')]
	overlap = r[0].intersection(r[1])

	if overlap:
		counter[1] += 1

		if overlap == r[0] or overlap == r[1]:
			counter[0] += 1

print('PART 1:', counter[0], '\nPART 2:', counter[1])