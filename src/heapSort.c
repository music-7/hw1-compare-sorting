/* heapSort.c - 힙 정렬 (최대 힙, 제자리). 수업에서 다루지 않은 정렬. 불안정. */
#include "sort.h"

static void siftDown(Record *a, size_t start, size_t end, SortStats *st) {
    size_t root = start;                       /* end는 힙 크기 */
    while (2 * root + 1 < end) {
        size_t child = 2 * root + 1;
        if (child + 1 < end && sortLess(&a[child], &a[child + 1], st)) child++;
        if (sortLess(&a[root], &a[child], st)) { sortSwap(&a[root], &a[child], st); root = child; }
        else return;
    }
}

void heapSort(Record *a, size_t n, SortStats *st) {
    if (n < 2) return;
    sortDepth(st, 1);
    for (size_t s = n / 2; s-- > 0; ) siftDown(a, s, n, st);   /* 1단계: 힙 만들기 O(n) */
    for (size_t end = n - 1; end > 0; end--) {                  /* 2단계: 최댓값을 뒤로 */
        sortSwap(&a[0], &a[end], st);
        siftDown(a, 0, end, st);
    }
}
