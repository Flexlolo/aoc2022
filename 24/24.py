from lsm.aoc import get_input
from lsm.aoc.vector import Vector


directions = ((1, 0), (-1, 0), (0, -1), (0, 1))
direction_names = '><^v'

initial_state = set()

for y, line in enumerate(get_input().splitlines()):
	for x, c in enumerate(line):
		if c in ('#', '.'):
			continue

		v = Vector(x, y)
		direction = direction_names.index(c)
		initial_state.add((v, direction))

bounds = [Vector(1, 1), Vector(x - 1, y - 1)]

simulation_cache = {0: initial_state}

def simulate_minutes(minutes: int):
	if minutes in simulation_cache:
		return simulation_cache[minutes]

	state = simulate_minutes(minutes - 1)
	state_new = set()

	for pos, direction in state:
		pos_new = pos + directions[direction]

		if not pos_new.inside(*bounds):
			match direction:
				# right
				case 0:
					pos_new[0] = bounds[0][0]

				# left
				case 1:
					pos_new[0] = bounds[1][0]

				# up
				case 2:
					pos_new[1] = bounds[1][1]

				# down
				case 3:
					pos_new[1] = bounds[0][1]

		state_new.add((pos_new, direction))

	simulation_cache[minutes] = state_new
	return state_new

def solve(start, end, minutes_offset):
	minutes = minutes_offset
	queue = [start]

	while True:
		minutes += 1
		# print('SOLVING', minutes)

		state = simulate_minutes(minutes)
		occupied = set((s[0] for s in state))

		queue_new = set()

		while queue:
			pos = queue.pop(0)

			for direction in directions:
				pos_new = pos + direction

				if pos_new == end:
					return minutes - minutes_offset

				if not pos_new.inside(*bounds):
					continue

				if pos_new in occupied:
					continue

				queue_new.add(pos_new)

			if pos not in occupied:
				queue_new.add(pos)

		queue = list(queue_new)

# start, end
dests = (bounds[0] - (0, 1), bounds[1] + (0, 1))
total = 0

for i in range(3):
	minutes = solve(dests[i % 2], dests[(i + 1) % 2], total)
	total += minutes

	if i == 0:
		print('PART 1:', total)

	if i == 2:
		print('PART 2:', total)