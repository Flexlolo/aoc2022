from lsm.aoc import get_input

def solve(lines, part2: bool):
	score = 0

	for line in lines:
		elf, you = line.split(' ')
		
		elf = 'ABC'.index(elf)
		result = you = 'XYZ'.index(you)

		if part2:
			outcomes = ((elf - 1) % 3, elf, (elf + 1) % 3)
			you = outcomes[result]
		else:
			outcomes = (you == (elf - 1) % 3, elf == you, you == (elf + 1) % 3)
			result = outcomes.index(True)

		score += (result * 3) + you + 1

	return score

lines = get_input('input', day=2, year=2022).splitlines()

print('PART 1:', solve(lines, False))
print('PART 2:', solve(lines, True))
