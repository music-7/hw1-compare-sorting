"""report/REPORT.pdf 를 만든다. (reportlab, report/results.csv 와 그래프 PNG 사용)"""
import csv, math, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak, Preformatted, KeepTogether)

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "report")
REPO_URL = "https://github.com/<본인-GitHub-ID>/hw1-compare-sorting"   # <- 제출 전에 실제 URL로 교체
STUDENT = "이름: ○○○   학번: ○○○○○○○○"                                   # <- 교체

pdfmetrics.registerFont(TTFont("K", "/tmp/fonts/K-Regular.ttf"))   # tools/mkfont.py 로 만든 부분집합 폰트
pdfmetrics.registerFont(TTFont("KB", "/tmp/fonts/K-Bold.ttf"))
pdfmetrics.registerFontFamily("K", normal="K", bold="KB", italic="K", boldItalic="KB")

body = ParagraphStyle("body", fontName="K", fontSize=9.6, leading=15, wordWrap="CJK", spaceAfter=4)
small = ParagraphStyle("small", parent=body, fontSize=8.4, leading=12.5, textColor=colors.HexColor("#444444"))
h1 = ParagraphStyle("h1", parent=body, keepWithNext=1, fontName="KB", fontSize=14, leading=19, spaceBefore=10, spaceAfter=6,
                    textColor=colors.HexColor("#1f3b63"))
h2 = ParagraphStyle("h2", parent=body, keepWithNext=1, fontName="KB", fontSize=11, leading=16, spaceBefore=6, spaceAfter=3)
title = ParagraphStyle("title", parent=body, fontName="KB", fontSize=20, leading=27, spaceAfter=4)
code = ParagraphStyle("code", fontName="K", fontSize=7.6, leading=10.6, backColor=colors.HexColor("#f4f5f7"),
                      borderPadding=5, leftIndent=4, spaceBefore=3, spaceAfter=8)
cell = ParagraphStyle("cell", parent=body, fontSize=8.4, leading=11.5, spaceAfter=0)
cellb = ParagraphStyle("cellb", parent=cell, fontName="KB")

P = lambda t, s=body: Paragraph(t, s)
rows = list(csv.DictReader(open(os.path.join(R, "results.csv"))))
def g(exp, shape, n, alg, key):
    for r in rows:
        if r["experiment"] == exp and r["shape"] == shape and int(r["n"]) == n and r["algorithm"] == alg:
            return float(r[key])
ALGS = ["mergeSort", "quickSort", "heapSort"]
fmt = lambda v: f"{int(v):,}"

def table(data, widths, header=True, align_right_from=None, bold_first_col=False):
    data = [[Paragraph(str(c), cellb if (header and i == 0) or (bold_first_col and j == 0) else cell)
             for j, c in enumerate(r)] for i, r in enumerate(data)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8bec8")),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if header: st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6ecf5")))
    t.setStyle(TableStyle(st)); return t

def img(name, w=150):
    from PIL import Image as PI
    iw, ih = PI.open(os.path.join(R, name)).size
    return Image(os.path.join(R, name), width=w * mm, height=w * mm * ih / iw)

S = []
nA0 = 100000
# ---------------- 표지/개요 ----------------
S += [P("과제 1. 정렬 비교 보고서", title),
      P("병합 정렬 · 퀵 정렬 · 힙 정렬(수업에서 배우지 않은 정렬)", h2),
      P(STUDENT, body),
      P(f"GitHub 저장소: <font color='#1a56b0'>{REPO_URL}</font>", body),
      Spacer(1, 4),
      P("1. 무엇을 비교했나", h1),
      P("세 정렬을 <b>하나의 공통 인터페이스</b>(<font name='K'>SortAlgorithm</font> 구조체 + 함수 포인터)로 묶고, "
        "같은 입력·같은 측정 도구로 <b>시간, 비교 횟수, 이동 횟수, 추가 메모리, 재귀 깊이, 안정성</b>을 쟀다. "
        "시간은 기계와 부하에 따라 흔들리지만 비교·이동 횟수는 입력이 같으면 항상 같으므로, 두 종류를 함께 보고 결론은 가능하면 횟수로 뒷받침했다."),
      table([["구분", "정렬", "선택 이유"],
             ["배운 정렬 ①", "병합 정렬 (Merge)", "안정 정렬이고 최악에도 O(n log n). 대신 O(n) 추가 메모리가 든다."],
             ["배운 정렬 ②", "퀵 정렬 (Quick)", "실전에서 가장 빠르다고 알려진 정렬. 불안정하고 최악은 O(n²)이다."],
             ["배우지 않은 정렬", "힙 정렬 (Heap)", "O(n log n) 최악 보장 + 제자리(O(1)). 병합·퀵이 각각 가진 장점을 반씩 가져 "
              "셋이 서로 다른 절충점에 놓인다."]],
            [30, 38, 112]),
      Spacer(1, 4),
      P("세 정렬은 모두 평균 O(n log n)이라 &quot;누가 더 빠른가&quot;만 보면 재미가 없다. 그래서 <b>같은 O(n log n)인데 실제로는 왜 차이가 나는가</b>"
        "(상수항, 메모리 접근 패턴, 안정성, 메모리 비용)를 이번 보고서의 질문으로 삼았다."),
      P(f"환경: Ubuntu 24.04 컨테이너, Intel Xeon 1 vCPU, gcc 13.3 <font name='K'>-std=c17 -Wall -Wextra -O2</font>. "
        "원소는 <font name='K'>Record{int key; int tag;}</font> (8바이트). key로 정렬하고 tag에 입력 순서를 새겨 안정성을 실측한다.", small)]

# ---------------- AI 학습 ----------------
S += [P("2. 배우지 않은 정렬: 힙 정렬 (AI를 통한 학습)", h1),
      P("AI(Claude, Anthropic)에게 아래 순서로 물어 학습했고(전체 요약은 부록 A), AI의 설명을 그대로 믿지 않고 "
        "<b>손으로 추적 → 코드로 구현 → 테스트·실험으로 확인</b>하는 순서로 검증했다."),
      P("2.1 힙 정렬의 핵심 아이디어", h2),
      P("① <b>최대 힙</b>은 &quot;모든 노드가 자식보다 크거나 같다&quot;는 완전 이진 트리다. 루트가 항상 최댓값이다. "
        "② 완전 이진 트리는 <b>배열 하나로 표현</b>할 수 있다. 0부터 셀 때 인덱스 i의 자식은 2i+1, 2i+2다(포인터 불필요). "
        "③ 정렬은 두 단계다. <b>(1) 힙 만들기</b>: 마지막 부모부터 루트까지 거꾸로 <font name='K'>siftDown</font>. "
        "<b>(2) 반복 추출</b>: 루트(최댓값)를 배열 맨 뒤와 바꾸고, 힙 크기를 1 줄이고, 루트에 siftDown. 최댓값이 뒤쪽부터 채워진다."),
      P("AI에게 &quot;왜 힙 만들기는 O(n log n)이 아니라 O(n)인가?&quot;를 물었다. 답: siftDown 비용은 그 노드의 <i>높이</i>에 비례하는데, "
        "노드의 절반은 높이 0(잎), 1/4은 높이 1 … 이라 총합이 Σ n/2<super>h+1</super>·h = O(n)이다. "
        "추출 단계가 n번 × O(log n)이므로 전체는 O(n log n)이고, 이때 최악과 평균이 같다(입력에 안 민감)."),
      P("2.2 손으로 추적: [4, 10, 3, 5, 1]", h2),
      Preformatted(
        "힙 만들기   [4,10,3,5,1] -> siftDown(1): 10 >= 자식(5,1) 이라 그대로\n"
        "                       -> siftDown(0): 4 < 10 이므로 교환 [10,4,3,5,1], 4 < 5 이므로 교환 [10,5,3,4,1]   (힙 완성)\n"
        "추출 1회    맨 뒤(1)와 루트(10) 교환 -> [1,5,3,4 | 10]   siftDown -> [5,4,3,1 | 10]\n"
        "추출 2회    5와 1 교환 -> [1,4,3 | 5,10]              siftDown -> [4,1,3 | 5,10]\n"
        "추출 3회    4와 3 교환 -> [3,1 | 4,5,10]              siftDown 은 이동 없음\n"
        "추출 4회    3과 1 교환 -> [1 | 3,4,5,10]   ->   결과 [1,3,4,5,10]", code),
      P("실제 구현(<font name='K'>heapSort</font>)에 같은 입력을 넣었을 때 <font name='K'>1 3 4 5 10</font>이 나와 손 추적과 일치했다.", small),
      P("2.3 힙 정렬은 왜 불안정한가 (직접 확인)", h2),
      P("AI는 &quot;루트와 맨 뒤를 교환하는 순간 같은 key의 상대 순서가 멀리 뛰어넘어 깨진다&quot;고 설명했다. 반례를 직접 만들어 돌려 보았다: "
        "입력 (key=2,tag=0), (key=2,tag=1), (key=1,tag=2) → 결과 (1,2), <b>(2,1), (2,0)</b>. 같은 key 2의 순서가 뒤집혔다. "
        "이 사실은 <font name='K'>tests/test_sort.c</font>의 안정성 검사(주장과 실측이 일치하는지)에도 들어 있다."),
      P("2.4 AI 설명 중 실험으로 확인한 것 / 보정한 것", h2),
      table([["AI가 설명한 내용", "확인 방법", "결과"],
             ["힙 정렬은 입력 모양(정렬됨·역순)에 둔감하다", "실험 A (n=100,000)",
              f"비교 횟수가 random/sorted/reversed에서 {g('shape','random',nA0,'heapSort','compares')/1e6:.2f}M / "
              f"{g('shape','sorted',nA0,'heapSort','compares')/1e6:.2f}M / {g('shape','reversed',nA0,'heapSort','compares')/1e6:.2f}M로 거의 같다 → 일치. "
              f"(시간은 random이 더 느린데 {g('shape','random',nA0,'heapSort','ms'):.1f} 대 {g('shape','sorted',nA0,'heapSort','ms'):.1f}ms, 원인은 확인하지 못했다.)"],
             ["O(1) 추가 메모리", "extraBytes 측정", "모든 n에서 0 바이트 (병합 정렬은 8n 바이트)."],
             ["캐시에 불리해 같은 O(n log n)이어도 느리다", "n을 키우며 시간·비교 횟수 비교",
              "n=1,024,000에서 병합보다 비교는 약 2배 많음. 시간 기울기가 횟수 기울기보다 큼 (4.3절)."],
             ["평균 비교 횟수 ≈ 2 n log2 n", "비교/(n log2 n) 계산", "1.70 → 1.85로 2에 가까워짐. 대체로 일치."]],
            [52, 40, 88])]

# ---------------- 세 정렬 ----------------
S += [P("3. 세 정렬 개요와 구현", h1),
      table([["", "병합 정렬", "퀵 정렬", "힙 정렬"],
             ["핵심 아이디어", "반으로 나눠 각각 정렬, 정렬된 두 구간을 병합", "피벗 기준으로 분할, 양쪽을 재귀", "최대 힙 구성 후 최댓값을 뒤로 하나씩"],
             ["평균 / 최악", "O(n log n) / O(n log n)", "O(n log n) / <b>O(n²)</b>", "O(n log n) / O(n log n)"],
             ["추가 메모리", "<b>O(n)</b>", "O(log n) 스택", "<b>O(1)</b>"],
             ["안정성", "<b>안정</b>", "불안정", "불안정"],
             ["구현 요점", "같으면 왼쪽 먼저 꺼냄(안정성의 열쇠)", "Hoare 분할 + median-of-three, 작은 쪽만 재귀", "siftDown 한 함수로 두 단계 모두 처리"]],
            [26, 50, 52, 52], bold_first_col=True),
      Spacer(1, 3),
      P("<b>공통 인터페이스.</b> 세 정렬이 <font name='K'>sortLess</font>(비교), <font name='K'>sortAssign</font>(이동)만 사용하도록 하여 "
        "비교·이동 횟수를 정렬 코드 안에서 같은 기준으로 센다(교환 1회 = 이동 3회). 시간은 정렬 <i>밖</i>(bench.c)에서 재서 "
        "구현마다 측정 방식이 달라지지 않게 했다. 정렬을 하나 더 추가하려면 <font name='K'>SORT_ALGORITHMS</font> 표에 한 줄만 넣으면 테스트와 벤치마크에 자동으로 들어온다."),
      Preformatted(
        "typedef struct SortAlgorithm {\n"
        "    const char *name, *timeAvg, *timeWorst, *space;\n"
        "    int stable;                                   /* claimed stability, checked against measurement */\n"
        "    void (*sort)(Record *a, size_t n, SortStats *st);\n"
        "} SortAlgorithm;", code),
      P("<b>퀵 정렬 주의점.</b> 피벗을 첫 원소로 고르면 정렬된 입력에서 O(n²)이 되므로 median-of-three(처음·가운데·끝의 중앙값)를 쓴다. "
        "또 작은 쪽만 재귀하고 큰 쪽은 반복문으로 돌려 재귀 깊이를 O(log n)으로 묶었다. Hoare 분할은 같은 값에서 멈추기 때문에 "
        "중복이 많아도 분할이 균형을 유지한다(4.2절 duplicates 결과)."),
      P("<b>검증.</b> <font name='K'>make test</font>: 크기 0~300 × 입력 4종 × 정렬 3종, qsort와 key 열 대조, 안정성 주장 대 실측, 통계 기록 확인 → "
        "<b>3,623개 검사 모두 통과</b>. <font name='K'>make asan</font>: AddressSanitizer·UBSan으로 같은 테스트를 돌려 경고 없음.")]

# ---------------- 실험 ----------------
nA = 100000
S += [P("4. 실험 결과", h1),
      P("4.1 실험 설계", h2),
      P("입력은 고정 시드의 xorshift 난수로 만들어 언제나 같다. <b>실험 A</b>: n=100,000에서 입력 모양 4가지(random, sorted, reversed, duplicates=key 16종) × 20회 평균. "
        "<b>실험 B</b>: random 입력에서 n=1,000~1,024,000(11단계). 입력 복사 시간은 뺐다. 시간(ms)은 이 기계 한 대에서 잰 값이므로 <b>같은 표 안에서만</b> 비교한다."),
      P("4.2 입력 모양별 (n = 100,000)", h2)]
data = [["입력", "알고리즘", "시간(ms)", "비교", "이동", "깊이", "안정(실측)"]]
for s in ["random", "sorted", "reversed", "duplicates"]:
    for a in ALGS:
        st = "안정" if g("shape", s, nA, a, "stable") == 1 else "불안정"
        data.append([s if a == "mergeSort" else "", a, f"{g('shape',s,nA,a,'ms'):.2f}", fmt(g('shape',s,nA,a,'compares')),
                     fmt(g('shape',s,nA,a,'moves')), int(g('shape',s,nA,a,'maxDepth')), st])
S += [table(data, [22, 26, 22, 30, 30, 14, 22]),
      P("※ &quot;안정(실측)&quot;은 <b>중복 key가 있는 입력에서만 의미</b>가 있다. sorted·reversed는 key가 모두 달라 어떤 정렬이든 &quot;안정&quot;으로 나온다. "
        "안정성 판정은 random·duplicates 행을 봐야 하고, 거기서 퀵·힙은 불안정, 병합만 안정으로 나왔다.", small),
      KeepTogether([img("shapes-time.png", 118)]),
      P(f"<b>관찰.</b> ① random에서 퀵이 가장 빠르다({g('shape','random',nA,'quickSort','ms'):.2f}ms, 병합 {g('shape','random',nA,'mergeSort','ms'):.2f}, 힙 {g('shape','random',nA,'heapSort','ms'):.2f}). "
        f"② 그런데 <b>비교 횟수는 퀵({fmt(g('shape','random',nA,'quickSort','compares'))})이 병합({fmt(g('shape','random',nA,'mergeSort','compares'))})보다 {(g('shape','random',nA,'quickSort','compares')/g('shape','random',nA,'mergeSort','compares')-1)*100:.0f}% 많다.</b> "
        f"퀵이 이기는 이유는 이동이 절반({fmt(g('shape','random',nA,'quickSort','moves'))} 대 {fmt(g('shape','random',nA,'mergeSort','moves'))})이고 "
        "보조 배열 복사가 없기 때문이다. 즉 &quot;비교 횟수가 적은 쪽이 빠르다&quot;는 단순한 등식은 성립하지 않는다. "
        f"③ 병합은 입력에 거의 둔감하다: 이동은 모든 입력에서 {fmt(g('shape','random',nA,'mergeSort','moves'))}로 동일하고(보조 배열을 늘 복사), "
        f"비교만 sorted·reversed에서 약 절반({fmt(g('shape','sorted',nA,'mergeSort','compares'))})으로 준다. "
        f"④ 퀵은 median-of-three 덕분에 sorted·reversed에서도 O(n²)로 무너지지 않았다(reversed 비교 {fmt(g('shape','reversed',nA,'quickSort','compares'))}회, "
        f"n<super>2</super>/2 = 5×10<super>9</super> 와 비교). 다만 reversed는 random보다 비교가 {(g('shape','reversed',nA,'quickSort','compares')/g('shape','random',nA,'quickSort','compares')-1)*100:.0f}% 늘어 피벗 선택이 완벽하지 않음을 보여 준다. "
        f"⑤ 힙은 어떤 입력에서도 비슷한 시간대이며 이동 횟수가 가장 많다(random {fmt(g('shape','random',nA,'heapSort','moves'))}).")]
S += [img("shapes-compares.png", 112), img("shapes-moves.png", 112)]

# ---------------- 성장 ----------------
S += [P("4.3 n을 키우며 (random)", h2)]
data = [["n", "병합 ms", "퀵 ms", "힙 ms", "병합 비교", "퀵 비교", "힙 비교"]]
for n in [1000, 8000, 64000, 256000, 1024000]:
    data.append([fmt(n)] + [f"{g('growth','random',n,a,'ms'):.2f}" for a in ALGS] + [fmt(g('growth','random',n,a,'compares')) for a in ALGS])
n1 = 1024000
lb = math.lgamma(n1 + 1) / math.log(2)
S += [table(data, [24, 22, 22, 22, 30, 30, 30]),
      Spacer(1, 3), img("growth-time.png", 118),
      P(f"<b>관찰.</b> 로그-로그 그래프에서 세 선은 거의 나란하고 기울기는 병합 1.09, 퀵 1.07, 힙 1.15(n≥32,000 구간의 직선 맞춤)다. "
        "n log n의 이 구간 이론 기울기는 1+1/ln n ≈ 1.08이므로 <b>세 정렬 모두 O(n log n)으로 자란다</b>. "
        f"n=1,024,000에서 퀵은 병합보다 {g('growth','random',n1,'mergeSort','ms')/g('growth','random',n1,'quickSort','ms'):.2f}배, "
        f"힙보다 {g('growth','random',n1,'heapSort','ms')/g('growth','random',n1,'quickSort','ms'):.2f}배 빠르다. "
        "<b>힙의 시간 기울기(1.15)가 비교 횟수 기울기(1.09)보다 큰 점</b>이 눈에 띈다. 배열이 캐시에 다 들어가는 작은 n에서는 "
        "병합과 거의 같은 속도(n=8,000: 0.52 대 0.54ms)이던 힙이, 배열이 커지자 뒤처진다. 힙은 부모·자식이 2배씩 멀리 떨어져 있어 "
        "<b>메모리 접근이 순차적이지 않기 때문</b>이라는 것이 AI의 설명이었다(이 실험은 캐시 미스를 직접 세지는 않았으므로 정황 증거일 뿐이다)."),
      img("growth-compares-norm.png", 112),
      P(f"비교 횟수를 n log2 n으로 나누면 병합은 0.87→0.94, 퀵은 1.61→1.41, 힙은 1.70→1.85다. "
        f"병합의 n=1,024,000 비교 {fmt(g('growth','random',n1,'mergeSort','compares'))}회는 비교 정렬의 이론적 하한 log2(n!) ≈ {lb:,.0f}회보다 "
        f"불과 {(g('growth','random',n1,'mergeSort','compares')/lb-1)*100:.1f}% 많다. 즉 <b>병합은 비교 횟수 면에서 거의 최적</b>이고, "
        "그 대가로 이동(보조 배열 복사)과 메모리를 쓴다."),
      P("4.4 메모리와 재귀 깊이", h2)]
S += [table([["알고리즘", f"추가 메모리 (n={n1:,})", "재귀 깊이", "비고"],
             ["mergeSort", f"{fmt(g('growth','random',n1,'mergeSort','extraBytes'))} B (≈{g('growth','random',n1,'mergeSort','extraBytes')/1e6:.1f} MB)", int(g('growth','random',n1,'mergeSort','maxDepth')), "입력 배열과 같은 크기 O(n)"],
             ["quickSort", "0 B", int(g('growth','random',n1,'quickSort','maxDepth')), "스택만 사용. 작은 쪽 재귀로 깊이 ≤ log2 n"],
             ["heapSort", "0 B", int(g('growth','random',n1,'heapSort','maxDepth')), "반복문만 사용, 제자리"]],
            [28, 50, 22, 80]),
      P("병합의 8.2MB는 원소가 8바이트라서이며, 원소가 크면 그만큼 커진다. 퀵은 깊이가 log2(1,024,000)≈20보다 작은 14에 그쳤다(작은 쪽만 재귀한 효과).", small)]

# ---------------- 결론 ----------------
S += [P("5. 종합 비교와 결론", h1),
      table([["기준", "병합", "퀵", "힙", "근거"],
             ["평균 속도 (random)", "○", "<b>◎</b>", "△", f"n=1.02M: {g('growth','random',n1,'mergeSort','ms'):.0f} / {g('growth','random',n1,'quickSort','ms'):.0f} / {g('growth','random',n1,'heapSort','ms'):.0f} ms"],
             ["비교 횟수", "<b>◎</b>", "○", "△", "n log2 n 대비 0.94 / 1.41 / 1.85"],
             ["최악 보장", "◎", "△ (O(n²))", "◎", "이론. 퀵은 median-of-three로 실험 입력에선 회피"],
             ["추가 메모리", "△ O(n)", "○ O(log n)", "<b>◎ O(1)</b>", "실측 8.2MB / 0 / 0"],
             ["안정성", "<b>◎</b>", "×", "×", "duplicates 입력 실측 + 반례"]],
            [32, 22, 26, 26, 74]),
      Spacer(1, 4),
      P("<b>결론.</b> 세 정렬은 이론상 모두 O(n log n)이지만 실제로는 서로 다른 것을 얻고 다른 것을 지불한다. "
        "<b>병합</b>은 안정성과 최소 비교 횟수를 얻는 대신 O(n) 메모리와 많은 이동을 지불한다(같은 key의 순서를 지켜야 하거나 연결 리스트·외부 정렬이면 선택). "
        "<b>퀵</b>은 평균 속도가 가장 좋지만 최악의 O(n²)를 피하려는 피벗 전략이 필요하고 불안정하다(범용 배열 정렬의 기본값). "
        "<b>힙</b>은 O(1) 메모리와 최악 O(n log n)을 모두 보장하지만 상수가 크고 캐시에 불리해 평균은 가장 느리다(메모리가 빡빡하거나 최악 보장이 필수일 때). "
        "이번에 얻은 가장 큰 배움은 <b>비교 횟수만으로는 속도를 예측할 수 없다</b>는 점이었다. 비교가 더 많은(약 57%) 퀵이 병합보다 빨랐다."),
      P("<b>한계.</b> ① 시간은 1 vCPU 컨테이너 한 대에서 잰 값이다. ② 캐시 미스는 직접 재지 않았다(힙이 느린 이유는 정황 설명). "
        "③ 퀵의 최악(피벗을 첫 원소로 고르는 단순 버전의 O(n²))은 구현·측정하지 않고 이론으로만 언급했다. "
        "④ 병합은 top-down 단순 구현이며, 작은 구간을 삽입 정렬로 대체하는 등의 최적화는 넣지 않았다. ⑤ 난수 입력은 시드 하나로 만든 것이다.", small),
      P("부록 A. AI 학습 대화 요약 (힙 정렬)", h1),
      table([["질문", "AI 답변 요약", "내가 한 확인"],
             ["힙 정렬을 초보자에게 설명해 줘", "최대 힙 = 부모≥자식인 완전 이진 트리, 배열로 표현(자식 2i+1, 2i+2). 힙 만들기 → 최댓값을 뒤로 보내며 반복.", "손 추적(2.2절)으로 확인"],
             ["왜 힙 만들기는 O(n)인가", "siftDown 비용이 노드 높이에 비례하고 높이가 큰 노드는 드물다. Σ n/2^(h+1)·h = O(n).", "이론값과 실험의 비교 횟수 추세 비교"],
             ["왜 불안정한가, 반례를 보여 줘", "루트↔맨뒤 교환이 같은 key를 뛰어넘는다. (2a,2b,1c) → (1c,2b,2a).", "같은 입력을 코드에 넣어 재현"],
             ["병합·퀵과 비교하면?", "최악 보장+제자리라는 장점, 캐시 비우호적이라 실전 평균은 느림. introsort는 퀵이 나빠지면 힙으로 전환.", "실험 B로 시간·비교 횟수 대조"],
             ["구현 시 실수하기 쉬운 곳", "siftDown 경계(end 미포함), 힙 크기 1씩 줄이기, 자식이 하나뿐인 경우.", "n=0..300 전수 테스트, ASan"]],
            [40, 88, 52]),
      P("부록 B. 코드와 재현 방법", h1),
      P(f"저장소: <font color='#1a56b0'>{REPO_URL}</font> (zip도 함께 제출)"),
      Preformatted("make test    # 3,623 checks\nmake asan    # AddressSanitizer + UBSan\nmake run     # 비교 표 출력\nmake charts  # results.csv 와 그래프(PNG) 재생성 (python3 + matplotlib 필요)", code),
      P("파일: src/sort.h(공통 인터페이스) · mergeSort.c · quickSort.c · heapSort.c · sort.c(구현 표) · bench.c(측정) · main.c · tests/test_sort.c · tools/plot.py · tools/build_report.py", small)]

def footer(c, d):
    c.saveState(); c.setFont("K", 8); c.setFillColor(colors.grey)
    c.drawCentredString(A4[0] / 2, 10 * mm, f"- {d.page} -"); c.restoreState()

doc = SimpleDocTemplate(os.path.join(R, "REPORT.pdf"), pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm,
                        topMargin=14 * mm, bottomMargin=16 * mm, title="과제1 정렬 비교 보고서")
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print("built")
