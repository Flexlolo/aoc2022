from lsm.aoc import get_input, get_input_filename
from bisect import insort
from copy import copy
import re


blueprints = []

for line in get_input().splitlines():
	cost = re.findall(r'\d+', line)

	blueprint = {
		'ore': int(cost[1]),
		'clay': int(cost[2]),
		'obsidian': (int(cost[3]), int(cost[4])),
		'geode': (int(cost[5]), int(cost[6])),
	}

	blueprints.append(blueprint)

res_index = {k: i for i, k in enumerate(blueprint.keys())}

def robot_build(blueprint, resources: list[int], resource: str):
	if resource == 'ore':
		if resources[res_index['ore']] >= blueprint[resource]:
			new_resources = copy(resources)
			new_resources[res_index['ore']] -= blueprint[resource]
			return True, new_resources
	elif resource == 'clay':
		if resources[res_index['ore']] >= blueprint[resource]:
			new_resources = copy(resources)
			new_resources[res_index['ore']] -= blueprint[resource]
			return True, new_resources
	elif resource == 'obsidian':
		have_iron = resources[res_index['ore']] >= blueprint[resource][0]
		have_clay = resources[res_index['clay']] >= blueprint[resource][1]

		if have_iron and have_clay:
			new_resources = copy(resources)
			new_resources[res_index['ore']] -= blueprint[resource][0]
			new_resources[res_index['clay']] -= blueprint[resource][1]
			return True, new_resources

	elif resource == 'geode':
		have_iron = resources[res_index['ore']] >= blueprint[resource][0]
		have_obsidian = resources[res_index['obsidian']] >= blueprint[resource][1]

		if have_iron and have_obsidian:
			new_resources = copy(resources)
			new_resources[res_index['ore']] -= blueprint[resource][0]
			new_resources[res_index['obsidian']] -= blueprint[resource][1]
			return True, new_resources

	return False, None

def state_rating(blueprint, state, time_left):
	return sum((state['resources'][i] + state['robots'][i] * time_left) * 100**i for i in range(4))

def blueprint_quality(blueprint, time_limit: int, queue_limit: int = 5000):

	def resources_mine(state):
		for i, amount in enumerate(state['robots']):
			state['resources'][i] += amount

	state = {
		'resources': [0 for _ in res_index],
		'robots': [0 for _ in res_index],
	}

	state['robots'][res_index['ore']] = 1
	state['rating'] = 0

	queue = [state]
	time_passed = 0

	while time_passed < time_limit:
		time_passed += 1

		queue_next = []
		time_left = time_limit - time_passed

		while queue:
			state = queue.pop(0)
			for robot in reversed(blueprint.keys()):
				success, new_resources = robot_build(blueprint, state['resources'], robot)

				if success:
					branch = {
						'resources': new_resources,
						'robots': copy(state['robots']),
					}

					resources_mine(branch)

					branch['robots'][res_index[robot]] += 1
					branch['rating'] = state_rating(blueprint, branch, time_left)
					insort(queue_next, branch, key=lambda x: x['rating'])
			
			resources_mine(state)
			state['rating'] = state_rating(blueprint, state, time_left)
			insort(queue_next, state, key=lambda x: x['rating'])


		queue = queue_next[-queue_limit:]

	best_score = 0

	for state in queue:
		geodes = state['resources'][-1]

		if geodes > best_score:
			best_score = geodes

	return best_score


score = 0

for n, blueprint in enumerate(blueprints):
	if (n + 1) % 5 == 0:
		print(f'blueprint {n + 1}/{len(blueprints)}')

	score += (n + 1) * blueprint_quality(blueprint, time_limit=24, queue_limit=1000)

print('PART 1:', score)

score = 1

for n, blueprint in enumerate(blueprints):
	if n > 2:
		continue

	print('doing part 2...')
	score *= blueprint_quality(blueprint, time_limit=32, queue_limit=5000)

print('PART 2:', score)