"""report/results.csv 로 그래프(PNG)를 그린다. 필요: matplotlib, numpy"""
import csv, math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

for f in font_manager.findSystemFonts():
    if "NotoSansCJK-Regular" in f or "NanumGothic" in f:
        font_manager.fontManager.addfont(f)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=f).get_name()
        break
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "report")
rows = list(csv.DictReader(open(os.path.join(OUT, "results.csv"))))
ALGS = ["mergeSort", "quickSort", "heapSort"]
COL = {"mergeSort": "#4c78a8", "quickSort": "#e45756", "heapSort": "#54a24b"}
SHAPES = ["random", "sorted", "reversed", "duplicates"]

def get(exp, shape, n, alg, key):
    for r in rows:
        if r["experiment"] == exp and r["shape"] == shape and int(r["n"]) == n and r["algorithm"] == alg:
            return float(r[key])

def grouped(metric, title, ylabel, fname, log=False):
    fig, ax = plt.subplots(figsize=(7, 3.6))
    w = 0.26
    for i, a in enumerate(ALGS):
        vals = [get("shape", s, 100000, a, metric) for s in SHAPES]
        ax.bar(np.arange(4) + (i - 1) * w, vals, w, label=a, color=COL[a])
    ax.set_xticks(range(4)); ax.set_xticklabels(SHAPES)
    ax.set_title(title); ax.set_ylabel(ylabel)
    if log: ax.set_yscale("log")
    if not log: ax.set_ylim(0, ax.get_ylim()[1] * 1.18)
    ax.legend(ncol=3, loc="upper center"); ax.grid(axis="y", alpha=.3)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, fname), dpi=170); plt.close(fig)

grouped("ms", "입력 모양별 걸린 시간 (n = 100,000)", "시간 (ms)", "shapes-time.png")
grouped("compares", "입력 모양별 비교 횟수 (n = 100,000)", "비교 횟수", "shapes-compares.png")
grouped("moves", "입력 모양별 이동 횟수 (n = 100,000)", "이동 횟수", "shapes-moves.png")

ns = sorted({int(r["n"]) for r in rows if r["experiment"] == "growth"})
def series(alg, key): return [get("growth", "random", n, alg, key) for n in ns]

fig, ax = plt.subplots(figsize=(7, 3.8))
for a in ALGS:
    ax.plot(ns, series(a, "ms"), "o-", ms=4, label=a, color=COL[a])
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("n"); ax.set_ylabel("시간 (ms)"); ax.set_title("n이 커질 때 걸린 시간 (random, 로그-로그)")
ax.grid(alpha=.3, which="both"); ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(OUT, "growth-time.png"), dpi=170); plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 3.6))
for a in ALGS:
    y = [c / (n * math.log2(n)) for c, n in zip(series(a, "compares"), ns)]
    ax.plot(ns, y, "o-", ms=4, label=a, color=COL[a])
ax.set_xscale("log"); ax.set_xlabel("n"); ax.set_ylabel("비교 횟수 / (n log2 n)")
ax.set_title("비교 횟수를 n log2 n 으로 나눈 값 (random)")
ax.grid(alpha=.3); ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(OUT, "growth-compares-norm.png"), dpi=170); plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 3.4))
for a in ALGS:
    ax.plot(ns, [v / 1024 for v in series(a, "extraBytes")], "o-", ms=4, label=a, color=COL[a])
ax.set_xscale("log"); ax.set_xlabel("n"); ax.set_ylabel("추가 메모리 (KiB)")
ax.set_title("추가 메모리 사용량"); ax.grid(alpha=.3); ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(OUT, "memory.png"), dpi=170); plt.close(fig)

# 로그-로그 기울기(복잡도 지수) 출력
for a in ALGS:
    for key in ("ms", "compares"):
        y = series(a, key)
        k = len(ns) // 2
        slope = np.polyfit(np.log(ns[k:]), np.log(y[k:]), 1)[0]
        print(f"{a:10s} {key:9s} slope(n>={ns[k]}) = {slope:.3f}")
