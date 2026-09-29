CC      = gcc
CFLAGS  = -std=c17 -Wall -Wextra -O2 -Isrc
SRC     = src/sort.c src/mergeSort.c src/quickSort.c src/heapSort.c src/bench.c

all: src/main.out

src/main.out: $(SRC) src/main.c
	$(CC) $(CFLAGS) -o $@ $^

tests/test.out: $(SRC) tests/test_sort.c
	$(CC) $(CFLAGS) -o $@ $^

run: src/main.out
	./src/main.out

test: tests/test.out
	./tests/test.out

asan:
	$(CC) -std=c17 -Wall -Wextra -g -O1 -fsanitize=address,undefined -Isrc -o tests/asan.out $(SRC) tests/test_sort.c && ./tests/asan.out

csv: src/main.out
	./src/main.out --csv > report/results.csv

charts: csv
	python3 tools/plot.py

clean:
	rm -f src/main.out tests/test.out tests/asan.out
