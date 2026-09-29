/* mergeSort.c - 병합 정렬 (top-down, 보조 배열 n개 사용). 안정 정렬. */
#include <stdlib.h>
#include "sort.h"

static void mergeRange(Record *a, Record *buf, size_t lo, size_t hi, int depth, SortStats *st) {
    sortDepth(st, depth);
    if (hi - lo < 2) return;
    size_t mid = lo + (hi - lo) / 2;
    mergeRange(a, buf, lo, mid, depth + 1, st);
    mergeRange(a, buf, mid, hi, depth + 1, st);

    size_t i = lo, j = mid, k = lo;
    while (i < mid && j < hi) {
        /* 오른쪽이 "더 작을 때만" 오른쪽을 먼저 꺼낸다 -> 같으면 왼쪽 우선 = 안정 */
        if (sortLess(&a[j], &a[i], st)) sortAssign(&buf[k++], &a[j++], st);
        else                            sortAssign(&buf[k++], &a[i++], st);
    }
    while (i < mid) sortAssign(&buf[k++], &a[i++], st);
    while (j < hi)  sortAssign(&buf[k++], &a[j++], st);
    for (k = lo; k < hi; k++) sortAssign(&a[k], &buf[k], st);
}

void mergeSort(Record *a, size_t n, SortStats *st) {
    if (n < 2) return;
    Record *buf = malloc(n * sizeof(Record));
    if (!buf) abort();
    if (st) st->extraBytes = n * sizeof(Record);
    mergeRange(a, buf, 0, n, 1, st);
    free(buf);
}
