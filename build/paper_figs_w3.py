"""Week 3 논문 기반 그림 -> build/assets/week3/paper_*.png (독립 실행: python build/paper_figs_w3.py).

원문 그림은 쓰지 않고 matplotlib 도식으로 새로 그린다. 수치는 build/research/papers/week3.md 에
출처와 함께 적힌 값만 쓴다. (기존 그림은 week3_figs.py — 이 스크립트는 그것들을 건드리지 않는다.)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deckkit  # noqa: E402
deckkit.use_theme("clean")
from deckkit import mpl_setup, PALETTE_HEX as P  # noqa: E402

import numpy as np  # noqa: E402

plt = mpl_setup()
from matplotlib import font_manager  # noqa: E402
font_manager.fontManager.addfont("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf")
plt.rcParams["font.family"] = ["NanumGothic", "DejaVu Sans"]
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402

OUT = os.path.join(HERE, "assets", "week3")
os.makedirs(OUT, exist_ok=True)
TEAL, TEAL2, MINT, DARK, GRAY, ACC, LINE = (P[k] for k in ("TEAL", "TEAL2", "MINT", "DARK", "GRAY", "ACCENT", "LINE"))
MINT2, BG, MID, OFF, ACC_MID, ACC_BG = (P.get(k) for k in ("MINT2", "BG", "MID", "OFF", "ACC_MID", "ACC_BG"))


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)


def rbox(ax, x, y, w, h, text="", fc=MINT, ec=None, fs=15, color=DARK, bold=False, lw=1.2, r=0.08):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec or fc, lw=lw))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
                fontweight="bold" if bold else "normal")


def arr(ax, x1, y1, x2, y2, color=TEAL2, lw=2.0, ms=16, style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, shrinkA=0, shrinkB=0))


def note(fig, text, y=-0.02, fs=13):
    fig.text(0.5, y, text, ha="center", va="top", fontsize=fs, color=GRAY)


def layer_stack(ax, x, yc, side, n_planes, fc, ec="white", dx=0.09, maxshow=4):
    """특징 맵 묶음을 겹친 정사각형으로 (n_planes개 중 최대 maxshow장)."""
    k = min(n_planes, maxshow)
    for i in range(k):
        ax.add_patch(Rectangle((x + i * dx, yc - side / 2 + i * dx), side, side, fc=fc, ec=ec, lw=1.4))
    return x + (k - 1) * dx + side


# 1. Neocognitron (§5 구조, Fig.2 개념) ---------------------------------------
def fig_neocognitron():
    fig, ax = plt.subplots(figsize=(14, 4.8))
    ax.axis("off")
    layers = [("U0", "입력", 16, 1, OFF, "16×16"),
              ("US1", "S", 16, 24, TEAL2, "16×16×24"),
              ("UC1", "C", 10, 24, MINT2, "10×10×24"),
              ("US2", "S", 8, 24, TEAL2, "8×8×24"),
              ("UC2", "C", 6, 24, MINT2, "6×6×24"),
              ("US3", "S", 2, 24, TEAL2, "2×2×24"),
              ("UC3", "C", 1, 24, MINT2, "24")]
    x = 0.0
    sc = 0.17
    for name, kind, n, planes, fc, sub in layers:
        side = max(0.32, n * sc)
        r = layer_stack(ax, x, 1.9, side, planes, fc)
        cx = (x + r) / 2
        ax.text(cx, 3.75, name, ha="center", fontsize=17, fontweight="bold", color=DARK)
        ax.text(cx, 0.15, sub, ha="center", va="top", fontsize=14, color=GRAY)
        nxt = r + 0.75
        if name != "UC3":
            arr(ax, r + 0.1, 1.9, nxt - 0.1, 1.9, color=TEAL2 if kind != "S" else GRAY, lw=2)
        x = nxt
    ax.set_xlim(-0.3, x)
    ax.set_ylim(-1.8, 4.2)
    # 범례
    rbox(ax, 0.0, -0.95, 0.4, 0.4, fc=TEAL2)
    ax.text(0.55, -0.75, "S-층: 5×5 국소 특징 · 같은 plane은 같은 가중치 (학습)", fontsize=15, va="center", color=DARK)
    rbox(ax, 0.0, -1.65, 0.4, 0.4, fc=MINT2)
    ax.text(0.55, -1.45, "C-층: 이웃 S-cell 반응 모으기 (고정 연결) — pooling의 조상", fontsize=15, va="center", color=DARK)
    ax.text(x / 2, 4.15, "", ha="center")
    note(fig, "원문 §5 실험 망(각 층 24 cell-plane) · Fig.2 기반 재구성 — 학습은 비지도 자기조직화 (역전파 없음)", y=0.02)
    save(fig, "paper_neocognitron.png")


# 2. LeCun 1989 구조 (§3.3, p.548 구조도) -------------------------------------
def fig_lecun89():
    fig, ax = plt.subplots(figsize=(14, 5.4))
    ax.axis("off")
    ax.set_xlim(0, 14)
    ax.set_ylim(-1.2, 5.6)
    cols = [("입력", "16×16 = 256", "", "", OFF, 2.0),
            ("H1", "12맵 × 8×8 = 768", "5×5 · stride 2", "연결 19,968\n파라미터 1,068", TEAL2, 1.55),
            ("H2", "12맵 × 4×4 = 192", "5×5 · stride 2\n(H1 맵 8개씩)", "연결 38,592\n파라미터 2,592", TEAL2, 1.1),
            ("H3", "30", "완전 연결", "5,790", TEAL, 0.9),
            ("출력", "10", "완전 연결", "310", ACC, 0.6)]
    xs = [0.9, 4.0, 7.0, 9.8, 12.4]
    for (name, size, op, cnt, fc, h), x in zip(cols, xs):
        rbox(ax, x - 0.75, 2.6 - h, 1.5, 2 * h, fc=fc, r=0.1)
        ax.text(x, 4.9, name, ha="center", fontsize=18, fontweight="bold", color=DARK)
        ax.text(x, 0.25, size, ha="center", va="top", fontsize=14, color=DARK)
        if cnt:
            ax.text(x, -0.35, cnt, ha="center", va="top", fontsize=13.5, color=GRAY, linespacing=1.3)
    for (a, b), (_, _, op, _, _, _) in zip(zip(xs[:-1], xs[1:]), cols[1:]):
        arr(ax, a + 0.85, 2.6, b - 0.85, 2.6, color=TEAL2)
        ax.text((a + b) / 2, 2.85, op, ha="center", va="bottom", fontsize=13, color=TEAL, linespacing=1.2)
    note(fig, "원문 §3.3 · p.548 구조도 기반 재구성 — pooling 층 없음, 합계 64,660 연결 / 9,760 파라미터", y=0.02)
    save(fig, "paper_lecun89_arch.png")


# 3. LeNet-5 구조 (1998 Fig.2) ------------------------------------------------
def fig_lenet5():
    fig, ax = plt.subplots(figsize=(15, 5.2))
    ax.axis("off")
    st = [("입력", "32×32", 32, 1, OFF, "", ""),
          ("C1", "6@28×28", 28, 6, TEAL2, "합성곱 5×5", "156"),
          ("S2", "6@14×14", 14, 6, MINT2, "서브샘플링 2×2\n(평균형·학습 계수)", "12"),
          ("C3", "16@10×10", 10, 16, TEAL2, "합성곱 5×5\n(일부 맵만 연결)", "1,516"),
          ("S4", "16@5×5", 5, 16, MINT2, "서브샘플링\n2×2", "32"),
          ("C5", "120", 1, 1, TEAL, "합성곱\n5×5→1×1", "48,120"),
          ("F6", "84", 1, 1, TEAL, "완전 연결", "10,164"),
          ("출력", "10", 1, 1, ACC, "유클리드 RBF", "고정")]
    x = 0.0
    sc = 0.085
    centers = []
    for name, shape, n, planes, fc, op, par in st:
        if n == 1:
            hgt = {"C5": 2.2, "F6": 1.7, "출력": 0.8}[name]
            ax.add_patch(Rectangle((x, 1.6 - hgt / 2), 0.32, hgt, fc=fc, ec="white"))
            r = x + 0.32
        else:
            r = layer_stack(ax, x, 1.6, n * sc, planes, fc, dx=0.07)
        cx = (x + r) / 2
        centers.append((x, r))
        ax.text(cx, 3.45, name, ha="center", fontsize=18, fontweight="bold", color=DARK)
        ax.text(cx, -0.35, shape, ha="center", va="top", fontsize=14, color=DARK)
        if par:
            ax.text(cx, -0.95, par, ha="center", va="top", fontsize=13.5, color=GRAY)
        x = r + 1.6
    for i in range(len(st) - 1):
        a, b = centers[i][1], centers[i + 1][0]
        arr(ax, a + 0.08, 1.6, b - 0.08, 1.6, color=TEAL2, lw=1.8, ms=13)
        op = st[i + 1][5]
        ax.text((a + b) / 2, 4.15 if i % 2 else 2.5 + 0.0, "", fontsize=1)
    # 연산 이름은 층 이름 아래 작은 글씨로
    for (l, r), s in zip(centers, st):
        if s[5]:
            ax.text((l + r) / 2, 3.35, s[5], ha="center", va="top", fontsize=12.5, color=TEAL, linespacing=1.15)
    ax.text(-0.2, -0.95, "파라미터", ha="right", va="top", fontsize=13.5, color=GRAY)
    ax.set_xlim(-1.5, x - 1.0)
    ax.set_ylim(-1.6, 4.0)
    note(fig, "원문 Fig.2 · §II.B 기반 재구성 — 학습 파라미터 합 60,000, 연결 340,908", y=0.02)
    save(fig, "paper_lenet5_arch.png")


# 4. MNIST 분류기 비교 (1998 Fig.9) -------------------------------------------
def fig_mnist():
    rows = [("선형 분류기", 12.0, "o"), ("k-NN (유클리드)", 5.0, "o"), ("완전 연결 300 은닉", 4.7, "o"),
            ("1000 RBF", 3.6, "o"), ("LeNet-1", 1.7, "c"), ("SVM 다항식 4차", 1.1, "s"),
            ("Tangent Distance", 1.1, "o"), ("LeNet-4", 1.1, "c"), ("RS-SVM", 1.0, "s"),
            ("LeNet-5", 0.95, "h"), ("LeNet-5 [증강]", 0.8, "c"), ("V-SVM 9차 [증강]", 0.8, "s"),
            ("Boosted LeNet-4 [증강]", 0.7, "c")]
    col = {"o": OFF, "c": TEAL2, "s": MID, "h": ACC}
    fig, ax = plt.subplots(figsize=(11, 6.6))
    y = np.arange(len(rows))[::-1]
    ax.barh(y, [r[1] for r in rows], color=[col[r[2]] for r in rows], height=0.7)
    for yy, (n, v, k) in zip(y, rows):
        ax.text(v + 0.15, yy, (f"{v:.2f}" if v == 0.95 else f"{v:.1f}") + "%", va="center", fontsize=14, color=DARK,
                fontweight="bold" if k == "h" else "normal")
    ax.set_yticks(y, [r[0] for r in rows], fontsize=14)
    ax.set_xlabel("MNIST 테스트 오류 (%)", fontsize=15)
    ax.tick_params(axis="x", labelsize=13)
    ax.set_xlim(0, 13.5)
    ax.text(13.3, y[3], "파랑 = 합성곱 망\n하늘 = SVM 계열\n[증강] = 왜곡 데이터 추가", ha="right", va="center",
            fontsize=13.5, color=GRAY, linespacing=1.4)
    note(fig, "원문 Fig.9에서 일부 발췌·재구성 (오차 약 ±0.1%p)", y=0.0)
    fig.tight_layout()
    save(fig, "paper_mnist_fig9.png")


# 5. Soft margin 개념도 (Cortes & Vapnik §3) -----------------------------------
def fig_softmargin():
    fig, ax = plt.subplots(figsize=(6.6, 5.4))
    w = np.array([0.5, 0.5])
    b = 0.0
    pos = np.array([[1, 1], [2.0, 1.4], [1.6, 2.4], [2.6, 2.4], [1.0, 2.2]])
    neg = np.array([[-1, -1], [-2.0, -1.3], [-1.4, -2.4], [-2.5, -2.2], [-2.2, -0.4]])
    out_p = np.array([[-0.6, -0.4]])   # 경계를 넘은 + 점
    in_n = np.array([[-0.3, -0.2]])     # 마진 안의 − 점 (분류는 맞음)
    xs = np.linspace(-3.4, 3.4, 10)
    for c, ls, lab in ((0, "-", ""), (1, "--", ""), (-1, "--", "")):
        ax.plot(xs, (c - b) / w[1] - w[0] / w[1] * xs, color=TEAL if c == 0 else GRAY, ls=ls, lw=2.6 if c == 0 else 1.8)
    ax.fill_between(xs, -1 / w[1] - xs, 1 / w[1] - xs, color=MINT, alpha=0.6, lw=0)
    ax.scatter(*pos.T, s=150, color=TEAL, zorder=3)
    ax.scatter(*neg.T, s=150, color=ACC, marker="s", zorder=3)
    ax.scatter(*out_p.T, s=150, color=TEAL, zorder=3, edgecolor=DARK, lw=2)
    ax.scatter(*in_n.T, s=150, color=ACC, marker="s", zorder=3, edgecolor=DARK, lw=2)
    for p, yv in ((out_p[0], 1), (in_n[0], -1)):
        xi = max(0, 1 - yv * (w @ p + b))
        lab = f"ξ = {xi:.2f}" + ("  (반대편: 오분류)" if xi > 1 else "  (마진 안)")
        ax.annotate(lab, xy=p, xytext=((-3.3, -2.0) if yv == 1 else (-3.3, 2.0)),
                    fontsize=15, color=DARK, arrowprops=dict(arrowstyle="->", color=DARK),
                    bbox=dict(fc="white", ec="none", pad=1.5))
    ax.text(0.2, -2.9, "w·x + b = 0", fontsize=15, color=TEAL, fontweight="bold")
    ax.set_xlim(-3.4, 3.4)
    ax.set_ylim(-3.2, 3.4)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines[["left", "bottom"]].set_visible(False)
    note(fig, "개념도 (원문 Fig.2·§3 기반) · 점선 = w·x+b = ±1\n검은 테두리 = 제약을 어긴 점, ξ = max(0, 1 − y(w·x+b))", y=0.05, fs=13)
    save(fig, "paper_svm_softmargin.png")


# 6. USPS Table 2 (다항식 차수) ------------------------------------------------
def fig_usps():
    deg = np.arange(1, 8)
    err = [12.0, 4.7, 4.4, 4.3, 4.3, 4.2, 4.3]
    sv = [200, 127, 148, 165, 175, 185, 190]
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    ax.bar(deg, err, color=[OFF] + [TEAL2] * 6, width=0.6)
    for d, e in zip(deg, err):
        ax.text(d, e - 0.3, f"{e}", ha="center", va="top", fontsize=14, color=DARK if d == 1 else "white",
                fontweight="bold")
    ax.axhline(5.1, color=ACC, lw=2, ls="--", xmax=0.86)
    ax.text(7.5, 5.1, "LeNet1\n5.1%", ha="left", va="center", fontsize=14, color=ACC, fontweight="bold")
    ax.axhline(2.5, color=GRAY, lw=1.5, ls=":", xmax=0.86)
    ax.text(7.5, 2.5, "사람\n2.5%", ha="left", va="center", fontsize=14, color=GRAY)
    ax.set_xlim(0.4, 8.4)
    ax.set_xticks(deg, [f"{d}차\nSV {s}" for d, s in zip(deg, sv)], fontsize=13)
    ax.set_ylabel("USPS 테스트 오류 (%)", fontsize=15)
    ax.tick_params(axis="y", labelsize=13)
    ax.set_ylim(0, 13.5)
    ax.set_title("다항식 커널 차수 — 특징 공간 256 → 약 $10^{16}$차원", fontsize=15, color=TEAL)
    note(fig, "원문 Table 1–2 기반 (SV = support vector 수)", y=0.0)
    fig.tight_layout()
    save(fig, "paper_usps_table2.png")


# 7. DBN 구조 (Hinton 2006 Fig.1) ---------------------------------------------
def fig_dbn():
    fig, ax = plt.subplots(figsize=(8.6, 6.4))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.6, 8.4)
    lay = [(0.6, "784 픽셀 (28×28)", OFF), (2.6, "500 유닛", MINT2), (4.6, "500 유닛", MINT2), (6.6, "2000 유닛", TEAL2)]
    for y, t, fc in lay:
        rbox(ax, 2.0, y, 6.0, 0.95, t, fc=fc, fs=17, bold=True, color="white" if fc == TEAL2 else DARK)
    rbox(ax, 0.1, 4.6, 1.6, 0.95, "10 라벨", fc=ACC, fs=15, bold=True, color="white")
    # 방향성 생성 연결(아래로)
    for y0, y1 in ((2.6, 1.55), (4.6, 3.55)):
        arr(ax, 4.0, y0, 4.0, y1, color=GRAY, lw=2.2)
        arr(ax, 6.0, y1, 6.0, y0, color=TEAL2, lw=2.2)
    ax.text(3.8, 2.07, "생성", ha="right", va="center", fontsize=13.5, color=GRAY)
    ax.text(6.2, 2.07, "인식", ha="left", va="center", fontsize=13.5, color=TEAL2)
    # 무방향
    ax.plot([5.0, 5.0], [5.55, 6.6], color=ACC, lw=3.5)
    ax.plot([0.9, 0.9, 2.6], [5.55, 6.1, 6.6], color=ACC, lw=2.5)
    ax.text(5.2, 6.07, "무방향 연합 기억 (RBM)", fontsize=14, color=ACC, va="center", fontweight="bold")
    ax.text(5.0, 8.1, "RBM을 아래부터 한 층씩 학습 → up-down으로 미세 조정", ha="center", fontsize=15, color=DARK)
    ax.text(5.0, -0.45, "원문 Fig.1 · §6.1 기반 재구성 — 가중치 약 170만 개", ha="center", fontsize=13, color=GRAY)
    save(fig, "paper_dbn_arch.png")


# 8. Glorot & Bengio Table 1 -------------------------------------------------
def fig_glorot():
    data = {"MNIST": [2.21, 1.76, 1.64], "CIFAR-10": [57.28, 55.9, 52.92], "Shapeset-3×2": [82.61, 27.15, 15.60]}
    labs = ["Sigmoid", "Tanh", "Tanh + normalized init"]
    cols = [OFF, MID, TEAL]
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.8))
    for ax, (k, v) in zip(axs, data.items()):
        bars = ax.bar(range(3), v, color=cols, width=0.65)
        for i, e in enumerate(v):
            ax.text(i, e + max(v) * 0.02, f"{e:g}", ha="center", fontsize=14, color=DARK,
                    fontweight="bold" if i == 2 else "normal")
        ax.set_title(k, fontsize=16, color=TEAL)
        ax.set_xticks([])
        ax.set_ylim(0, max(v) * 1.18)
        ax.tick_params(axis="y", labelsize=12)
    axs[0].set_ylabel("테스트 오류 (%)", fontsize=15)
    fig.legend(bars, labs, loc="lower center", ncol=3, fontsize=14, frameon=False, bbox_to_anchor=(0.5, -0.07))
    fig.tight_layout(w_pad=2.5)
    note(fig, "원문 Table 1 (은닉 5층, 층당 1,000 유닛) 기반 — 사전학습 없음", y=-0.1)
    save(fig, "paper_glorot_table1.png")


# 9. AlexNet Table 2 (ILSVRC-2012 top-5) --------------------------------------
def fig_alexnet():
    rows = [("2위 팀\nSIFT + FV", 26.2, OFF, "테스트"),
            ("CNN 1개", 18.2, MID, "검증"),
            ("CNN 5개 평균", 16.4, TEAL2, "테스트"),
            ("CNN 7개 평균\n(2개는 외부 데이터\n사전학습)", 15.3, ACC, "테스트")]
    fig, ax = plt.subplots(figsize=(10, 5.6))
    x = np.arange(len(rows))
    ax.bar(x, [r[1] for r in rows], color=[r[2] for r in rows], width=0.6)
    for i, (n, v, c, sp) in enumerate(rows):
        ax.text(i, v + 0.5, f"{v}%", ha="center", fontsize=17, fontweight="bold", color=DARK)
        ax.text(i, v / 2, sp, ha="center", va="center", fontsize=13.5, color=DARK if c in (OFF, MID) else "white")
    ax.set_xticks(x, [r[0] for r in rows], fontsize=13.5)
    ax.set_ylabel("ILSVRC-2012 top-5 오류 (%)", fontsize=15)
    ax.tick_params(axis="y", labelsize=13)
    ax.set_ylim(0, 30)
    note(fig, "원문 Table 2 기반. 외부 데이터 = ImageNet Fall 2011 (약 1,500만 장, 22K 클래스). 외부 데이터 없는 공식 결과 16.4%", y=0.0, fs=12.5)
    fig.tight_layout()
    save(fig, "paper_alexnet_table2.png")


# 10. ResNet 원 블록 (Fig.2) ---------------------------------------------------
def fig_resnet_block():
    fig, ax = plt.subplots(figsize=(6.2, 6.6))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.6, 10.4)
    ax.text(4.2, 9.8, "x", ha="center", fontsize=20, fontweight="bold", color=DARK)

    def blk(y, t, fc=MINT2):
        rbox(ax, 2.2, y, 4.0, 1.0, t, fc=fc, fs=16, bold=True)
    blk(7.6, "weight layer")
    blk(5.9, "ReLU", fc=MINT)
    blk(4.2, "weight layer")
    for y0, y1 in ((9.55, 8.62), (7.6, 6.92), (5.9, 5.22), (4.2, 3.05)):
        arr(ax, 4.2, y0, 4.2, y1)
    ax.add_patch(plt.Circle((4.2, 2.65), .4, fc="white", ec=ACC, lw=2.5))
    ax.text(4.2, 2.65, "+", ha="center", va="center", fontsize=22, color=ACC, fontweight="bold")
    ax.plot([4.2, 7.6, 7.6], [9.2, 9.2, 2.65], color=ACC, lw=2.6)
    arr(ax, 7.6, 2.65, 4.65, 2.65, color=ACC, lw=2.6)
    ax.text(7.8, 6.0, "항등\n지름길\n(x 그대로)", ha="left", va="center", fontsize=14, color=ACC, fontweight="bold")
    ax.text(2.0, 6.4, "F(x)", ha="right", fontsize=18, color=TEAL, fontweight="bold")
    arr(ax, 4.2, 2.25, 4.2, 1.72)
    rbox(ax, 2.7, 0.75, 3.0, 0.95, "ReLU", fc=ACC_BG, ec=ACC, fs=16, bold=True, color=ACC)
    ax.text(4.2, -0.3, "y = ReLU( F(x) + x )", ha="center", fontsize=17, fontweight="bold", color=DARK)
    ax.text(6.0, 1.2, "← 덧셈 뒤 ReLU", fontsize=13.5, color=ACC, va="center")
    save(fig, "paper_resnet_block.png")


# 11. ResNet Table 2 (plain vs ResNet) ----------------------------------------
def fig_resnet_table2():
    fig, ax = plt.subplots(figsize=(8.4, 5.6))
    vals = {"plain": [27.94, 28.54], "ResNet": [27.88, 25.03]}
    x = np.array([0, 1])
    w = 0.36
    for k, (name, v) in enumerate(vals.items()):
        bars = ax.bar(x + (k - 0.5) * w, v, w, color=[OFF, GRAY] if name == "plain" else [MID, TEAL], label=name)
        for xx, e in zip(x + (k - 0.5) * w, v):
            ax.text(xx, e + 0.08, f"{e:.2f}", ha="center", fontsize=15, color=DARK, fontweight="bold")
    ax.set_xticks(x, ["18층", "34층"], fontsize=16)
    ax.set_ylim(24, 29.4)
    ax.set_ylabel("ImageNet 검증 top-1 오류 (%)", fontsize=15)
    ax.tick_params(axis="y", labelsize=13)
    ax.text(-0.18, 24.25, "plain", ha="center", fontsize=14, color=DARK)
    ax.text(0.18, 24.25, "ResNet", ha="center", fontsize=14, color=DARK)
    ax.text(0.82, 24.25, "plain", ha="center", fontsize=14, color="white")
    ax.text(1.18, 24.25, "ResNet", ha="center", fontsize=14, color="white")
    ax.text(0.82, 29.0, "18→34층: 더 나빠짐", ha="center", fontsize=14, color=ACC, fontweight="bold")
    ax.text(1.18, 25.55, "18→34층:\n좋아짐", ha="center", fontsize=14, color=TEAL, fontweight="bold")
    note(fig, "원문 Table 2 (10-crop) 기반 — 세로축은 24%부터", y=0.0)
    fig.tight_layout()
    save(fig, "paper_resnet_table2.png")


# 12. BN Fig.3 — 72.2% 정확도까지 step ------------------------------------------
def fig_bn_steps():
    rows = [("Inception (BN 없음)", 31.0, OFF), ("BN-Baseline", 13.3, MID), ("BN-x5 (학습률 5배)", 2.1, ACC),
            ("BN-x30 (학습률 30배)", 2.7, TEAL)]
    fig, ax = plt.subplots(figsize=(10, 4.6))
    y = np.arange(len(rows))[::-1]
    ax.barh(y, [r[1] for r in rows], color=[r[2] for r in rows], height=0.6)
    for yy, (n, v, c) in zip(y, rows):
        ax.text(v + 0.4, yy, f"{v}M step", va="center", fontsize=15, color=DARK,
                fontweight="bold" if c == ACC else "normal")
    ax.set_yticks(y, [r[0] for r in rows], fontsize=15)
    ax.set_xlabel("검증 정확도 72.2%에 도달하기까지의 학습 step (백만)", fontsize=14.5)
    ax.tick_params(axis="x", labelsize=13)
    ax.set_xlim(0, 37)
    ax.text(36.5, y[2], "31.0 / 2.1 ≈ 14배 적음", ha="right", va="center", fontsize=15, color=ACC, fontweight="bold")
    note(fig, "원문 Fig.3(표) 기반 — BN-x30은 최종 74.8%까지 도달", y=0.0)
    fig.tight_layout()
    save(fig, "paper_bn_steps.png")


# 13. CNN BatchNorm 축 vs LayerNorm 축 ------------------------------------------
def fig_bn_cnn_axes():
    fig, axs = plt.subplots(1, 2, figsize=(14, 5.2), gridspec_kw={"width_ratios": [1.35, 1]})
    ax = axs[0]
    ax.axis("off")
    ax.set_xlim(-0.3, 13.6)
    ax.set_ylim(-1.8, 6.2)
    Bn, Cn, n = 3, 3, 4
    cell = 0.3
    gw = n * cell
    for b in range(Bn):
        x0 = b * 4.7
        for c in range(Cn):
            ox, oy = x0 + c * (gw + 0.2), 1.6
            on = c == 1
            for i in range(n):
                for j in range(n):
                    ax.add_patch(Rectangle((ox + j * cell, oy + i * cell), cell, cell,
                                           fc=ACC if on else MINT2, ec="white", lw=1.2))
            ax.text(ox + gw / 2, oy + gw + 0.15, f"c{c + 1}", ha="center", va="bottom", fontsize=13,
                    color=ACC if on else GRAY, fontweight="bold" if on else "normal")
        ax.text(x0 + 1.9, 1.3, f"샘플 {b + 1}", ha="center", va="top", fontsize=15, color=DARK)
    ax.text(5.6, 5.5, "BatchNorm (합성곱 층): 채널 c 하나 = B × H × W 전체", ha="center", fontsize=17,
            color=TEAL, fontweight="bold")
    ax.text(5.6, -0.4, "주황 = 채널 2의 모든 샘플·모든 위치 → 평균·분산 하나, γ·β도 채널당 한 쌍",
            ha="center", va="top", fontsize=14, color=DARK)
    ax.text(5.6, -1.05, "예: B = 32, 14×14 맵 → 채널당 32 × 196 = 6,272개 값", ha="center", va="top", fontsize=14,
            color=GRAY)
    ax = axs[1]
    ax.axis("off")
    N, D = 5, 8
    ax.set_xlim(-1.4, D + 0.4)
    ax.set_ylim(-2.2, N + 1.6)
    for i in range(N):
        for j in range(D):
            on = i == 2
            ax.add_patch(Rectangle((j, N - 1 - i), 1, 1, fc=ACC if on else MINT2, ec="white", lw=2))
    ax.text(D / 2, N + 0.15, "특징 축 d →", ha="center", fontsize=15, color=GRAY)
    ax.text(-0.25, N / 2, "토큰(샘플) →", ha="right", va="center", fontsize=15, color=GRAY, rotation=90)
    ax.text(D / 2, N + 0.85, "LayerNorm: 토큰 하나의 d개 값", ha="center", fontsize=17, color=TEAL, fontweight="bold")
    ax.text(D / 2, -0.4, "배치의 다른 샘플과 무관 → 학습·추론 계산 동일", ha="center", va="top", fontsize=14, color=DARK)
    ax.text(D / 2, -1.05, "Ioffe & Szegedy §3.2 / Ba et al. §3 기반", ha="center", va="top", fontsize=13, color=GRAY)
    fig.tight_layout(w_pad=2)
    save(fig, "paper_bn_cnn_axes.png")


# 14. toy: 잔차 지름길과 기울기 (2016 후속 해석의 직관) ---------------------------
def toy_grad_norms(depth=40, n=64, residual=False, seed=0):
    rng = np.random.default_rng(seed)
    h = rng.normal(size=n)
    Ws, pre = [], []
    for _ in range(depth):
        W = rng.normal(scale=np.sqrt(1.0 / n), size=(n, n))
        z = W @ h
        f = np.maximum(z, 0)
        h = h + 0.1 * f if residual else f
        Ws.append(W)
        pre.append(z)
    g = np.ones(n) / np.sqrt(n)
    norms = [np.linalg.norm(g)]
    for W, z in zip(Ws[::-1], pre[::-1]):
        gf = W.T @ (g * (z > 0))
        g = g + 0.1 * gf if residual else gf
        norms.append(np.linalg.norm(g))
    return np.array(norms[::-1])


def fig_toy_grad():
    fig, ax = plt.subplots(figsize=(9, 5.2))
    d = 40
    p = toy_grad_norms(d, residual=False)
    r = toy_grad_norms(d, residual=True)
    L = np.arange(d + 1)
    ax.semilogy(L, p / p[-1], color=GRAY, lw=3, label="plain: h ← ReLU(Wh)")
    ax.semilogy(L, r / r[-1], color=ACC, lw=3, label="순수 항등 지름길: h ← h + F(h)")
    ax.set_xlabel("층 번호 (0 = 입력 쪽)", fontsize=15)
    ax.set_ylabel("‖∂L/∂h‖ (출력 층 = 1)", fontsize=15)
    ax.tick_params(labelsize=13)
    ax.legend(frameon=False, fontsize=14, loc="lower right")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: ("1e" + str(int(round(np.log10(v))))) if v > 0 else ""))
    note(fig, "toy 실험 (40층, 무작위 가중치, BN 없음) — 논문 결과 아님", y=0.0)
    fig.tight_layout()
    save(fig, "paper_toy_grad.png")


if __name__ == "__main__":
    for f in (fig_neocognitron, fig_lecun89, fig_lenet5, fig_mnist, fig_softmargin, fig_usps, fig_dbn, fig_glorot,
              fig_alexnet, fig_resnet_block, fig_resnet_table2, fig_bn_steps, fig_bn_cnn_axes, fig_toy_grad):
        f()
        print("ok", f.__name__)
