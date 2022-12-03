#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "file.h"
#include "list.h"
#include "str.h"

int main(int argc, char const *argv[])
{
	if (argc == 1)
	{
		printf("Usage: solution FILE\n");
		return 1;
	}

	char *buffer = readfile(argv[1]);
	struct List *blocks = buffer_split(buffer, "\n\n");

	int value;
	int max[3] = {0, 0, 0};

	for (int block_index = 0; block_index < blocks->size; block_index++)
	{
		char *block = list_get(blocks, block_index);
		struct List *lines = buffer_split(block, "\n");

		value = 0;

		for (int line_index = 0; line_index < lines->size; line_index++)
		{
			char *line = list_get(lines, line_index);
			value += atoi(line);
		}

		for (int i = 0; i < 3; i++)
		{
			if (max[i] < value)
			{
				for (int j = 3 - i - 1; j > 0; j--)
				{
					max[j] = max[j - 1];
				}

				max[i] = value;
				break;
			}
		}
	}

	printf("PART 1: %d\nPART 2: %d\n", max[0], max[0] + max[1] + max[2]);

	return 0;
}