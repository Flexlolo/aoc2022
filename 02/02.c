#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "file.h"
#include "list.h"
#include "str.h"

const char MOVES[] = "ABCXYZ";

int mod(int a, int b)
{
	int result = a % b;
	return result < 0 ? result + b : result;
}

int main(int argc, char const *argv[])
{
	if (argc == 1)
	{
		printf("Usage: solution FILE\n");
		return 1;
	}

	char *buffer = readfile(argv[1]);
	struct List *lines = buffer_split(buffer, "\n");

	int score[2] = {0, 0};

	for (int line_index = 0; line_index < lines->size; line_index++)
	{
		char *line = list_get(lines, line_index);
		int p[2];

		for (int i = 0; i < 2; i++)
		{
			int index = 2 * i;

			for (int j = 0; j < 6; j++)
			{
				if (line[index] == MOVES[j])
				{
					p[i] = j % 3;
					break;
				}
			}
		}

		score[0] +=	mod((p[1] - p[0] + 1), 3) * 3 + (p[1] + 1);
		score[1] +=	p[1] * 3 + mod((p[0] - (1 - p[1])), 3) + 1;
	}

	printf("PART 1: %d\nPART 2: %d\n", score[0], score[1]);

	return 0;
}