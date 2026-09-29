#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "bench.h"

static void row(const char *exp, const char *shape, size_t n, const SortAlgorithm *alg,
                const BenchResult *r, int csv) {
    if (csv)
        printf("%s,%s,%zu,%s,%.4f,%llu,%llu,%zu,%d,%d,%d\n", exp, shape, n, alg->name, r->ms,
               r->stats.compares, r->stats.moves, r->stats.extraBytes, r->stats.maxDepth,
               r->sorted, r->stableObserved);
    else
        printf("%-10s %-10s %8zu %-10s %10.3f %13llu %13llu %10zu %5d %s %s\n", exp, shape, n,
               alg->name, r->ms, r->stats.compares, r->stats.moves, r->stats.extraBytes,
               r->stats.maxDepth, r->sorted ? "OK " : "BAD", r->stableObserved ? "stable" : "unstable");
}

int main(int argc, char **argv) {
    int csv = argc > 1 && strcmp(argv[1], "--csv") == 0;
    if (csv) puts("experiment,shape,n,algorithm,ms,compares,moves,extraBytes,maxDepth,sorted,stable");
    else printf("%-10s %-10s %8s %-10s %10s %13s %13s %10s %5s\n", "exp", "shape", "n", "algorithm",
                "ms", "compares", "moves", "extraB", "depth");

    /* 실험 A: 입력 모양별 (n = 100,000) */
    size_t nA = 100000;
    Record *in = malloc(nA * sizeof(Record));
    for (int s = 0; s < SHAPE_COUNT; s++) {
        makeInput(in, nA, (Shape)s, 12345);
        for (size_t k = 0; k < SORT_ALGORITHM_COUNT; k++) {
            BenchResult r = benchRun(&SORT_ALGORITHMS[k], in, nA, 20);
            row("shape", SHAPE_NAMES[s], nA, &SORT_ALGORITHMS[k], &r, csv);
        }
    }
    free(in);

    /* 실험 B: n을 키우며 (random) */
    size_t sizes[] = {1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 512000, 1024000};
    for (size_t i = 0; i < sizeof sizes / sizeof sizes[0]; i++) {
        size_t n = sizes[i];
        in = malloc(n * sizeof(Record));
        makeInput(in, n, SHAPE_RANDOM, 777);
        int reps = n <= 16000 ? 200 : n <= 128000 ? 20 : 5;
        for (size_t k = 0; k < SORT_ALGORITHM_COUNT; k++) {
            BenchResult r = benchRun(&SORT_ALGORITHMS[k], in, n, reps);
            row("growth", "random", n, &SORT_ALGORITHMS[k], &r, csv);
        }
        free(in);
    }
    return 0;
}
