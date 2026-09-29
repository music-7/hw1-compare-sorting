# 정렬 비교 (과제 1) - 병합 · 퀵 · 힙

- 배운 정렬 2개: **병합 정렬**, **퀵 정렬**
- 배우지 않은 정렬 1개: **힙 정렬** (AI로 학습, 보고서 2절·부록 A)
- 보고서: [`report/REPORT.pdf`](report/REPORT.pdf)

## 실행
```
make test     # 유닛 테스트 (3,623 checks)
make asan     # AddressSanitizer + UBSan
make run      # 비교 표 출력
make charts   # report/results.csv + 그래프(PNG) 재생성 (python3, matplotlib 필요)
```
환경: gcc (`-std=c17 -Wall -Wextra -O2`). 시간은 기계마다 다르지만 비교/이동 횟수는 항상 같다.

## 구조
| 파일 | 역할 |
| --- | --- |
| `src/sort.h` | 공통 인터페이스 (`SortAlgorithm`, `SortStats`, 비교/이동 카운터) |
| `src/mergeSort.c` `quickSort.c` `heapSort.c` | 정렬 구현 |
| `src/sort.c` | 구현 표 `SORT_ALGORITHMS` (정렬을 추가하려면 한 줄) |
| `src/bench.c` `main.c` | 시간·횟수·메모리·안정성 측정 |
| `tests/test_sort.c` | 크기 0~300 전수, qsort 대조, 안정성 주장 대 실측 |
| `tools/plot.py` | CSV -> 그래프 |
| `tools/build_report.py` `mkfont.py` | 보고서 PDF 생성 (선택 사항) |
