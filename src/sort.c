#include "sort.h"

const SortAlgorithm SORT_ALGORITHMS[] = {
    {"mergeSort", "O(n log n)", "O(n log n)", "O(n)",     1, mergeSort},
    {"quickSort", "O(n log n)", "O(n^2)",     "O(log n)", 0, quickSort},
    {"heapSort",  "O(n log n)", "O(n log n)", "O(1)",     0, heapSort},
};
const size_t SORT_ALGORITHM_COUNT = sizeof(SORT_ALGORITHMS) / sizeof(SORT_ALGORITHMS[0]);
