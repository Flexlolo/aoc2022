from lsm.aoc import get_input

score = [0, 0]

for line in get_input().splitlines():
	p1, p2 = map(lambda x: 'ABCXYZ'.index(x) % 3, line.split(' '))
	ds = [
		(p2 - p1 + 1) % 3 * 3 + (p2 + 1), 
		p2 * 3 + (p1 - (1 - p2)) % 3 + 1
	]

	score = list(map(lambda x, y: x + y, score, ds))

print('PART 1:', score[0])
print('PART 2:', score[1])