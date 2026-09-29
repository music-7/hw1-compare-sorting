/* sort.h - 공통 인터페이스: 세 정렬(병합/퀵/힙)을 같은 잣대로 비교하기 위한 헤더 */
#ifndef SORT_H
#define SORT_H
#include <stddef.h>

/* key로 정렬하고, tag에는 입력에서의 원래 순서를 새겨 안정성을 실측한다. */
typedef struct Record {
    int key;
    int tag;
} Record;

/* 정렬이 스스로 세는 값. 시간과 달리 입력이 같으면 언제나 같은 값이 나온다. */
typedef struct SortStats {
    unsigned long long compares;  /* key 비교 횟수 */
    unsigned long long moves;     /* Record 대입(이동) 횟수 */
    size_t extraBytes;            /* 입력 배열 밖에서 잡은 최대 메모리(바이트) */
    int maxDepth;                 /* 도달한 최대 재귀 깊이 */
} SortStats;

typedef struct SortAlgorithm {
    const char *name;
    const char *timeAvg;
    const char *timeWorst;
    const char *space;
    int stable;                   /* 안정 정렬이라고 "주장"하는 값 (실측과 대조한다) */
    void (*sort)(Record *a, size_t n, SortStats *st);
} SortAlgorithm;

extern const SortAlgorithm SORT_ALGORITHMS[];
extern const size_t SORT_ALGORITHM_COUNT;

void mergeSort(Record *a, size_t n, SortStats *st);
void quickSort(Record *a, size_t n, SortStats *st);
void heapSort(Record *a, size_t n, SortStats *st);

/* 비교/이동을 세는 작은 도구들. 모든 정렬이 이것만 쓴다. */
static inline int sortLess(const Record *x, const Record *y, SortStats *st) {
    if (st) st->compares++;
    return x->key < y->key;
}
static inline void sortAssign(Record *dst, const Record *src, SortStats *st) {
    if (st) st->moves++;
    *dst = *src;
}
static inline void sortSwap(Record *x, Record *y, SortStats *st) {
    Record t;
    sortAssign(&t, x, st);
    sortAssign(x, y, st);
    sortAssign(y, &t, st);
}
static inline void sortDepth(SortStats *st, int d) {
    if (st && d > st->maxDepth) st->maxDepth = d;
}
#endif
