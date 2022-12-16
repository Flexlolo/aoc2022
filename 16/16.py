from lsm.aoc import get_input
import re
from copy import copy, deepcopy

valves = {}

for line in get_input().splitlines():
	# Valve HH has flow rate=22; tunnel leads to valve GG
	names = re.findall(r'[A-Z]{2}', line)
	rate = re.findall(r'rate=(\d+)', line)[0]

	valves[names[0]] = {'rate': int(rate), 'edges': tuple(names[1:])}

valves_bits = {list(valves.keys())[i]: 1<<i for i in range(len(valves.keys()))}
nodes = tuple(valve for valve in valves if valves[valve]['rate'] > 0)

shortest_path = {}

for key in valves:
	queue = [(key, 0)]
	seen = {}

	while queue:
		valve, time_spent = queue.pop(0)

		if valve in seen:
			continue

		seen[valve] = time_spent

		for edge in valves[valve]['edges']:
			if edge not in seen:
				queue.append((edge, time_spent + 1))

	shortest_path[key] = seen


def solve_naive(time_limit: int, workers_count: int = 1, options_max: int = 3) -> int | dict:
	branch = {
		'location': ['AA' for _ in range(workers_count)], 
		'path': 0, 
		'time_spent': [0 for _ in range(workers_count)], 
		'pressure_total': 0
		}

	queue = [branch]
	paths = []

	nodes = tuple(valve for valve in valves if valves[valve]['rate'] > 0)

	while queue:
		step = queue.pop(0)
		
		location 		= step['location']
		path 			= step['path']
		time_spent 		= step['time_spent']
		pressure_total 	= step['pressure_total']

		queue_changed = False

		for worker in range(workers_count):
			options = {}

			for valve in nodes:
				if path & valves_bits[valve]: 
					continue

				rate = valves[valve]['rate']
				time_to_travel = shortest_path[location[worker]][valve]
				time_to_open = time_to_travel + 1
				time_flowing = time_limit - time_spent[worker] - time_to_open

				if time_flowing > 0:
					pressure = rate * time_flowing
					options[valve] = (time_to_open, pressure)

			# print(options)
			for i, (valve, (time_to_open, pressure)) in enumerate(sorted(options.items(), key=lambda x:x[1][1], reverse=True)):
				if i >= options_max:
					break

				# print(f'CONSIDERING {i + 1}: {pressure}')
				branch = deepcopy(step)
				branch['location'][worker] = valve
				branch['path'] = branch['path'] | valves_bits[valve]
				branch['time_spent'][worker] += time_to_open
				branch['pressure_total'] += pressure

				queue.append(branch)
				queue_changed = True

		if not queue_changed:
			paths.append(step)

	# print(paths)
	paths = sorted(paths, key=lambda x: x['pressure_total'])
	return paths[-1]['pressure_total']
	return paths


# tuple[*workers, path] : best_pressure
cache = {}
function_calls = 0
cache_hits = 0

def solve(time_limit: int, workers_count: int = 1, options_max: int = 3, step = None) -> int | dict:
	global cache, function_calls, cache_hits

	if step is None:
		step = {
			# location, time_spent
			'workers': tuple(('AA', 0) for _ in range(workers_count)),
			'path': 0, 
			'pressure_total': 0
			}
	

	workers = step['workers']
	# print(type(workers))
	# print(workers)

	location 		= tuple(workers[i][0] for i in range(workers_count))
	time_spent 		= tuple(workers[i][1] for i in range(workers_count))
	path 			= step['path']
	pressure_total 	= step['pressure_total']

	# cache_entry = tuple([*workers, path])
	# cache_entry = (*location, *time_spent, path)
	function_calls += 1

	cache_entries = ((workers, path), (workers[::-1], path))

	for cache_entry in cache_entries:
		if cache_entry in cache:
			cache_hits += 1

			if cache_hits % 10_000 == 0:
				print(f'CACHE HIT %: {cache_hits / function_calls * 100.0:.2f} | {function_calls=}')

			return cache[cache_entry]

	result = 0
	queue_changed = False

	for worker in range(workers_count):
		options = {}

		for valve in nodes:
			if path & valves_bits[valve]: 
				continue

			rate = valves[valve]['rate']
			time_to_travel = shortest_path[location[worker]][valve]
			time_to_open = time_to_travel + 1
			time_flowing = time_limit - time_spent[worker] - time_to_open

			if time_flowing > 0:
				pressure = rate * time_flowing
				options[valve] = (time_to_open, pressure)

		# print(options)
		for i, (valve, (time_to_open, pressure)) in enumerate(sorted(options.items(), key=lambda x:x[1][1], reverse=True)):
			if i >= options_max - time_spent[worker] // 2:
				break
# 
			# print(f'CONSIDERING {i + 1}: {pressure}')
			branch = copy(step)
			workers_new = [list(w) for w in branch['workers']]
			workers_new[worker] = (valve, time_spent[worker] + time_to_open)
			# print(workers_new)

			branch['workers'] = tuple(tuple(w) for w in workers_new)
			branch['path'] = branch['path'] | valves_bits[valve]
			branch['pressure_total'] += pressure

			r = solve(time_limit=time_limit, workers_count=workers_count, options_max=options_max, step=branch)

			if r > result:
				result = r


	if result:
		for cache_entry in cache_entries:
			cache[cache_entry] = result

		return result
	else:
		return pressure_total

print('Solving part 1...')
print('PART 1:', solve_naive(30, workers_count=1, options_max=10))

print('Solving part 2...')
print('PART 2:', solve(26, workers_count=2, options_max=10))
print(function_calls)