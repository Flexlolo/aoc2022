from lsm.aoc import get_input

signal = get_input()

def solve(signal: str, length: int) -> int:
	for i in range(len(signal)):
		marker = signal[i:i+length]

		if len(set(marker)) == length:
			return i + length 

print('PART 1:', solve(signal, 4))
print('PART 2:', solve(signal, 14))
