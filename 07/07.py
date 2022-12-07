from lsm.aoc import get_input
import re
import json

fs = {}
path = []

for line in get_input().splitlines():
	if line.startswith('$'):
		_, cmd = line.split(' ', 1)

		if cmd == 'ls':
			continue
		else:
			cmd, args = cmd.split(' ', 1)

			cursor = fs

			if args == '..':
				path.pop(-1)
			else:
				if args == '/':
					path = []
				else:
					path.append(args)

			for f in path:
				cursor = cursor[f]
	else:
		kw, filename = line.split(' ', 1)

		if kw == 'dir':
			cursor[filename] = {}
		else:
			cursor[filename] = int(kw)

def get_size(cursor: dict, path: list = []) -> list[tuple[tuple[str], int]]:
	r = []
	total = 0

	for k, v in cursor.items():
		if isinstance(v, dict):
			rs = get_size(v, path + [k])
			
			for spath, size in rs:
				if len(spath) == len(path) + 1:
					total += size

			r += rs
		else:
			total += v

	r.append((tuple(path), total))

	return r

fs_size = get_size(fs)
total = sum([size for _, size in fs_size if size <= 100_000])
print('PART 1:', total)

fs_size = sorted(fs_size, key=lambda x: x[1])
root = fs_size[-1][1]

TOTAL = 70_000_000
NEEDED = 30_000_000
LEFT = (TOTAL - root)
TO_DEL = NEEDED - LEFT

for _, size in fs_size:
	if size >= TO_DEL:
		print('PART 2:', size)
		break