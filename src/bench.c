#define _POSIX_C_SOURCE 200809L
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "bench.h"

const char *SHAPE_NAMES[] = {"random", "sorted", "reversed", "duplicates"};

/* 재현 가능한 자체 난수 (표준 rand()는 구현마다 다르다) */
static unsigned xorshift(unsigned *s) {
    unsigned x = *s; x ^= x << 13; x ^= x >> 17; x ^= x << 5; return *s = x;
}

void makeInput(Record *a, size_t n, Shape shape, unsigned seed) {
    unsigned s = seed ? seed : 2463534242u;
    for (size_t i = 0; i < n; i++) {
        switch (shape) {
        case SHAPE_RANDOM:     a[i].key = (int)(xorshift(&s) % 1000000u); break;
        case SHAPE_SORTED:     a[i].key = (int)i; break;
        case SHAPE_REVERSED:   a[i].key = (int)(n - i); break;
        case SHAPE_DUPLICATES: a[i].key = (int)(xorshift(&s) % 16u); break;
        default: a[i].key = 0;
        }
        a[i].tag = (int)i;
    }
}

int isSorted(const Record *a, size_t n) {
    for (size_t i = 1; i < n; i++) if (a[i - 1].key > a[i].key) return 0;
    return 1;
}
int isStable(const Record *a, size_t n) {
    for (size_t i = 1; i < n; i++)
        if (a[i - 1].key == a[i].key && a[i - 1].tag > a[i].tag) return 0;
    return 1;
}

static double nowMs(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e3 + t.tv_nsec / 1e6;
}

BenchResult benchRun(const SortAlgorithm *alg, const Record *input, size_t n, int reps) {
    BenchResult r; memset(&r, 0, sizeof r);
    Record *work = malloc(n * sizeof(Record));
    if (!work) abort();
    double total = 0;
    for (int k = 0; k < reps; k++) {
        memcpy(work, input, n * sizeof(Record));   /* 복사는 시간에서 뺀다 */
        SortStats st; memset(&st, 0, sizeof st);
        double t0 = nowMs();
        alg->sort(work, n, &st);
        total += nowMs() - t0;
        r.stats = st;                              /* 횟수는 매번 같다 */
    }
    r.ms = total / reps;
    r.sorted = isSorted(work, n);
    r.stableObserved = isStable(work, n);
    free(work);
    return r;
}
