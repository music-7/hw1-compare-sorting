#ifndef BENCH_H
#define BENCH_H
#include "sort.h"
typedef enum { SHAPE_RANDOM, SHAPE_SORTED, SHAPE_REVERSED, SHAPE_DUPLICATES, SHAPE_COUNT } Shape;
extern const char *SHAPE_NAMES[];
typedef struct BenchResult {
    double ms;            /* reps회 평균 시간 (입력 복사 시간 제외) */
    SortStats stats;
    int sorted;           /* key가 오름차순인가 */
    int stableObserved;   /* 같은 key끼리 tag가 오름차순인가 (실측) */
} BenchResult;
void makeInput(Record *a, size_t n, Shape shape, unsigned seed);
BenchResult benchRun(const SortAlgorithm *alg, const Record *input, size_t n, int reps);
int isSorted(const Record *a, size_t n);
int isStable(const Record *a, size_t n);
#endif
