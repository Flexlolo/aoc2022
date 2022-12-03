CC = gcc
CFLAGS = -O2 -I${HOME}/.lsm/lib/include
LDFLAGS := -l:liblsm.so 
SOURCE_DIR := .
BUILD_DIR := build

SOURCES := $(wildcard $(SOURCE_DIR)/*.c)
OBJECTS := $(SOURCES:%=$(BUILD_DIR)/%.o)
TARGET = $(SOURCES:.c=)


all: $(TARGET) clean

$(TARGET): $(OBJECTS)
	$(CC) $(LDFLAGS) -o $(TARGET) $^

$(BUILD_DIR)/%.c.o: %.c
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	@rm -rf $(BUILD_DIR)