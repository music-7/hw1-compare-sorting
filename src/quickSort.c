/* quickSort.c - 퀵 정렬 (Hoare 분할 + median-of-three 피벗). 불안정 정렬.
 * 작은 쪽을 재귀, 큰 쪽을 반복문으로 처리해 재귀 깊이를 O(log n)으로 제한한다. */
#include "sort.h"

static void medianToFront(Record *a, size_t lo, size_t hi, SortStats *st) {
    size_t mid = lo + (hi - lo) / 2;          /* hi는 마지막 원소의 인덱스 */
    if (sortLess(&a[mid], &a[lo], st)) sortSwap(&a[mid], &a[lo], st);
    if (sortLess(&a[hi],  &a[lo], st)) sortSwap(&a[hi],  &a[lo], st);
    if (sortLess(&a[hi],  &a[mid], st)) sortSwap(&a[hi], &a[mid], st);
    sortSwap(&a[lo], &a[mid], st);            /* 중앙값을 맨 앞(피벗 자리)으로 */
}

static void quickRange(Record *a, long lo, long hi, int depth, SortStats *st) {
    while (lo < hi) {
        sortDepth(st, depth);
        medianToFront(a, (size_t)lo, (size_t)hi, st);
        Record pivot = a[lo];
        long i = lo - 1, j = hi + 1;
        for (;;) {
            do { i++; } while (sortLess(&a[i], &pivot, st));
            do { j--; } while (sortLess(&pivot, &a[j], st));
            if (i >= j) break;
            sortSwap(&a[i], &a[j], st);
        }
        /* [lo..j] 와 [j+1..hi] 로 나뉜다. 작은 쪽만 재귀. */
        if (j - lo < hi - j - 1) { quickRange(a, lo, j, depth + 1, st); lo = j + 1; }
        else                     { quickRange(a, j + 1, hi, depth + 1, st); hi = j; }
    }
}

void quickSort(Record *a, size_t n, SortStats *st) {
    if (n < 2) return;
    quickRange(a, 0, (long)n - 1, 1, st);
}
