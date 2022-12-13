from lsm.aoc import get_input
from functools import cmp_to_key, reduce
from copy import deepcopy

def compare(p1, p2):
	packets = [p1, p2]
	types = [type(packet) for packet in packets]

	if types[0] != types[1]:
		packets = [packet if isinstance(packet, list) else [packet] for packet in packets]

	if isinstance(packets[0], list):
		for pair in zip(*packets):
			r = compare(*pair)

			if r:
				return r

		if len(packets[0]) < len(packets[1]):
			return -1

		elif len(packets[0]) == len(packets[1]):
			return 0

	else:
		if packets[0] < packets[1]:
			return -1

		elif packets[0] == packets[1]:
			return 0

	return 1

total = 0

dividers = [
	[[2]],
	[[6]],
]

all_packets = deepcopy(dividers)

for i, group in enumerate(get_input().split('\n\n')):
	packets = [eval(line) for line in group.splitlines()]

	for packet in packets:
		all_packets.append(packet)

	r = compare(*packets)

	if r == -1:
		total += i + 1

print('PART 1:', total)

all_packets = sorted(all_packets, key=cmp_to_key(compare))
print('PART 2:', reduce(lambda x,y: x * y, (all_packets.index(d) + 1 for d in dividers)))
