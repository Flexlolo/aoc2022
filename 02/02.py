from lsm.aoc import get_input

ROCK = 0
PAPER = 1
SCISSORS = 2

LOSE = 0
DRAW = 3
WIN = 6

shapes = {
	'A': ROCK,
	'X': ROCK,
	'B': PAPER,
	'Y': PAPER,
	'C': SCISSORS,
	'Z': SCISSORS,
}

outcomes = {
	'X': LOSE,
	'Y': DRAW,
	'Z': WIN,
}

def solve(lines, part2: bool):
	score = 0

	for line in lines:
		parts = line.split(' ')

		if part2:
			elf, result = shapes[parts[0]], outcomes[parts[1]]
		else:
			elf, you = shapes[parts[0]], shapes[parts[1]]

		if part2:
			if result == DRAW:
				you = elf
			elif result == LOSE:
				you = (elf - 1) % 3
			else:
				you = (elf + 1) % 3
		else:
			if elf == you:
				result = DRAW
			elif you == (elf + 1) % 3:
				result = WIN
			else:
				result = LOSE

		score += result + you + 1

	print(f"part {'2' if part2 else '1'}:", score)


lines = get_input('input', day=2, year=2022).splitlines()

solve(lines, False)
solve(lines, True)
