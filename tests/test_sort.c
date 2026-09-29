#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../src/bench.h"

static int checks = 0, failures = 0;
#define CHECK(cond, ...) do { checks++; if (!(cond)) { failures++; printf("FAIL: "); printf(__VA_ARGS__); printf("\n"); } } while (0)

static int cmpKey(const void *a, const void *b) {
    return ((const Record *)a)->key - ((const Record *)b)->key;
}

int main(void) {
    for (size_t k = 0; k < SORT_ALGORITHM_COUNT; k++) {
        const SortAlgorithm *alg = &SORT_ALGORITHMS[k];

        /* 1) 크기 0..300 x 모든 입력 모양: 정렬되는가 */
        for (size_t n = 0; n <= 300; n++) {
            for (int s = 0; s < SHAPE_COUNT; s++) {
                Record *a = malloc((n + 1) * sizeof(Record));
                makeInput(a, n, (Shape)s, 99 + (unsigned)n);
                alg->sort(a, n, NULL);
                CHECK(isSorted(a, n), "%s n=%zu shape=%s not sorted", alg->name, n, SHAPE_NAMES[s]);
                free(a);
            }
        }
        /* 2) qsort 결과와 key 열이 같은가 (난수 5000개) */
        {
            size_t n = 5000;
            Record *a = malloc(n * sizeof(Record)), *b = malloc(n * sizeof(Record));
            makeInput(a, n, SHAPE_RANDOM, 4242);
            memcpy(b, a, n * sizeof(Record));
            alg->sort(a, n, NULL);
            qsort(b, n, sizeof(Record), cmpKey);
            int same = 1;
            for (size_t i = 0; i < n; i++) if (a[i].key != b[i].key) same = 0;
            CHECK(same, "%s differs from qsort", alg->name);
            free(a); free(b);
        }
        /* 3) 안정성: 안정이라고 주장하면 실측도 안정이어야 한다.
              (불안정이라고 주장하는 정렬은 실제로 깨지는 입력이 있어야 의미가 있다) */
        {
            size_t n = 20000;
            Record *a = malloc(n * sizeof(Record));
            makeInput(a, n, SHAPE_DUPLICATES, 5);
            alg->sort(a, n, NULL);
            int stable = isStable(a, n);
            if (alg->stable) CHECK(stable, "%s claims stable but is not", alg->name);
            else             CHECK(!stable, "%s claims unstable but looked stable on this input", alg->name);
            free(a);
        }
        /* 4) 측정 도구: 통계가 기록되는가 */
        {
            Record a[8]; makeInput(a, 8, SHAPE_REVERSED, 1);
            SortStats st; memset(&st, 0, sizeof st);
            alg->sort(a, 8, &st);
            CHECK(st.compares > 0 && st.moves > 0, "%s stats not recorded", alg->name);
        }
    }
    /* 5) 안정성 판정기가 위반을 잡는가 */
    { Record bad[2] = {{1, 5}, {1, 2}}; CHECK(!isStable(bad, 2), "isStable missed a violation"); }
    { Record ok[2]  = {{1, 2}, {1, 5}}; CHECK(isStable(ok, 2), "isStable false alarm"); }

    printf("%d checks, %d failures\n", checks, failures);
    return failures ? 1 : 0;
}
