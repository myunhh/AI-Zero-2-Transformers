"""Week 3 그림 생성 — build/assets/week3/*.png"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deckkit import PALETTE_HEX as P, mpl_setup  # noqa: E402

plt = mpl_setup()
plt.rcParams["font.family"] = ["NanumGothic", "DejaVu Sans"]
from matplotlib import font_manager as _fm  # noqa: E402
_fm.fontManager.addfont("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf")
from matplotlib.ticker import FuncFormatter  # noqa: E402


def logfmt(ax, axis="y"):
    f = FuncFormatter(lambda v, _: f"10^{int(round(np.log10(v)))}" if v > 0 else "")
    f = FuncFormatter(lambda v, _: ("1e" + str(int(round(np.log10(v))))) if v > 0 else "")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(f)
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "week3")
os.makedirs(OUT, exist_ok=True)
TEAL, TEAL2, MINT, DARK, GRAY, ACC, LINE = (P[k] for k in ("TEAL", "TEAL2", "MINT", "DARK", "GRAY", "ACCENT", "LINE"))
MINT2 = "#CFE8EE"
ACC_BG = "#FDF1E8"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)


def grid(ax, arr, x0, y0, cell=1.0, hl=None, hl_color=ACC, fs=13, fill=None, title=None, fmt="{:g}",
         title_fs=14):
    """arr를 (x0,y0)=왼쪽 위 기준 격자로 그림."""
    arr = np.asarray(arr)
    h, w = arr.shape
    vmax = max(1e-9, np.abs(arr).max())
    for i in range(h):
        for j in range(w):
            v = arr[i, j]
            if fill is None:
                t = abs(v) / vmax
                fc = MINT if t < 0.05 else (MINT2 if t < 0.6 else "#9FD0DB")
            else:
                fc = fill
            ax.add_patch(Rectangle((x0 + j * cell, y0 - (i + 1) * cell), cell, cell, fc=fc, ec="white", lw=1.5))
            ax.text(x0 + (j + .5) * cell, y0 - (i + .5) * cell, fmt.format(v), ha="center", va="center",
                    fontsize=fs, color=DARK)
    if hl is not None:
        (r0, c0, hh, ww) = hl
        ax.add_patch(Rectangle((x0 + c0 * cell, y0 - (r0 + hh) * cell), ww * cell, hh * cell, fc="none",
                               ec=hl_color, lw=3.2))
    if title:
        ax.text(x0 + w * cell / 2, y0 + 0.35 * cell, title, ha="center", va="bottom", fontsize=title_fs,
                color=TEAL, fontweight="bold")


def canvas(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


# ---------------------------------------------------------------- 1. 이미지 = 텐서
def fig_image_tensor():
    fig, ax = canvas(9, 5.2, (-0.3, 17.2), (-9.3, 1.2))
    img = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 210, 250, 250, 250, 240, 0, 0],
        [0, 0, 0, 0, 30, 230, 0, 0],
        [0, 0, 0, 0, 190, 120, 0, 0],
        [0, 0, 0, 60, 230, 0, 0, 0],
        [0, 0, 0, 200, 90, 0, 0, 0],
        [0, 0, 20, 240, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]])
    for i in range(8):
        for j in range(8):
            v = int(img[i, j])
            g = v / 255  # 0 = 검정, 255 = 흰색
            ax.add_patch(Rectangle((j, -i - 1), 1, 1, fc=(g, g, g), ec=LINE, lw=.6))
            ax.text(j + .5, -i - .5, str(v), ha="center", va="center", fontsize=9,
                    color="white" if v < 128 else DARK)
    ax.text(4, 0.3, "흑백 8×8 이미지 = (1, 8, 8)", ha="center", fontsize=14, color=TEAL, fontweight="bold")
    ax.text(4, -8.8, "각 칸은 0~255 밝기 값 (0 = 검정, 255 = 흰색)", ha="center", fontsize=11.5, color=GRAY)
    # RGB 스택
    cols = ["#E57373", "#81C784", "#64B5F6"]
    names = ["R", "G", "B"]
    for k in range(3):
        x, y = 11.2 + k * 0.9, -6.6 + k * 0.9
        ax.add_patch(Rectangle((x, y), 4.2, 4.2, fc=cols[k], ec="white", lw=2, alpha=.85))
        ax.text(x + 0.25, y + 0.25, names[k], fontsize=14, color="white", fontweight="bold")
    ax.text(13.9, 0.3, "컬러 이미지 = (C, H, W)", ha="center", fontsize=14, color=TEAL, fontweight="bold")
    ax.text(13.9, -7.6, "C=3 채널 × H × W", ha="center", fontsize=12, color=DARK)
    ax.text(13.9, -8.5, "배치로 묶으면 (B, C, H, W)", ha="center", fontsize=12, color=ACC, fontweight="bold")
    save(fig, "image_tensor.png")


# ---------------------------------------------------------------- 2. 합성곱 슬라이딩
def fig_conv_sliding():
    x = np.array([[10, 10, 10, 0, 0, 0]] * 6)
    k = np.array([[1, 0, -1]] * 3)
    y = np.array([[np.sum(x[i:i + 3, j:j + 3] * k) for j in range(4)] for i in range(4)])
    fig, ax = canvas(11, 5.2, (-0.4, 17.6), (-8.6, 1.3))
    grid(ax, x, 0, 0, hl=(1, 1, 3, 3), title="입력 x (6×6)")
    ax.text(6.55, -3, "∗", fontsize=30, ha="center", va="center", color=DARK)
    grid(ax, k, 7.3, -1.5, hl=None, fill=ACC_BG, title="필터 W (3×3)")
    ax.text(11.05, -3, "=", fontsize=30, ha="center", va="center", color=DARK)
    grid(ax, y, 11.9, -1.0, hl=(1, 1, 1, 1), title="출력 y (4×4)")
    ax.text(8.8, -6.9, "주황 창 위치의 계산: (10·1 + 10·0 + 0·(−1)) × 3행 = 30",
            ha="center", fontsize=13.5, color=ACC, fontweight="bold")
    ax.text(8.8, -8.0, "같은 9개 가중치를 모든 위치에서 재사용 → 세로 경계가 있는 곳에서만 큰 값",
            ha="center", fontsize=12.5, color=DARK)
    save(fig, "conv_sliding.png")
    fig_inductive_bias()
    fig_bridge_sketch()


def _cells(ax, x0, y0, n, cell=1.0, fc=MINT2):
    """n×n 빈 격자 (왼쪽 위 = (x0, y0))."""
    for i in range(n):
        for j in range(n):
            ax.add_patch(Rectangle((x0 + j * cell, y0 - (i + 1) * cell), cell, cell, fc=fc, ec="white", lw=1.5))


def _window(ax, x0, y0, r, c, k=3, cell=1.0, col=ACC, lw=3):
    ax.add_patch(Rectangle((x0 + c * cell, y0 - (r + k) * cell), k * cell, k * cell, fc="none", ec=col, lw=lw))


# ---------------------------------------------------------------- 2b. 세 가지 구조적 가정 (슬라이드 9)
def fig_inductive_bias():
    fig, axs = plt.subplots(1, 3, figsize=(13.5, 4.2))
    for ax in axs:
        ax.set_xlim(-0.3, 10.3); ax.set_ylim(-8.7, 1.0); ax.set_aspect("equal"); ax.axis("off")
    # ① 지역성: 3×3 창 → 출력 한 칸
    ax = axs[0]
    _cells(ax, 0, 0, 6)
    _window(ax, 0, 0, 1, 1)
    ax.add_patch(Rectangle((8.3, -3.0), 1, 1, fc=ACC_BG, ec=ACC, lw=2.5))
    for (xx, yy) in ((1, -1), (4, -1), (1, -4), (4, -4)):
        ax.plot([xx, 8.3], [yy, -2.5], color=ACC, lw=1.2, alpha=.7)
    ax.text(8.8, -3.4, "출력\n한 칸", ha="center", va="top", fontsize=13, color=ACC, fontweight="bold")
    ax.text(5.0, 0.35, "① 가까운 3×3 영역만 연결", ha="center", va="bottom", fontsize=15, color=TEAL, fontweight="bold")
    ax.text(5.0, -8.5, "출력 한 칸은 입력 9개만 본다", ha="center", va="bottom", fontsize=13, color=DARK)
    # ② 같은 필터를 모든 위치에
    ax = axs[1]
    _cells(ax, 0, 0, 6)
    _window(ax, 0, 0, 0, 0)
    _window(ax, 0, 0, 3, 3)
    ax.text(1.5, -1.5, "W", ha="center", va="center", fontsize=15, color=ACC, fontweight="bold")
    ax.text(4.5, -4.5, "같은 W", ha="center", va="center", fontsize=15, color=ACC, fontweight="bold")
    ax.add_patch(FancyArrowPatch((2.5, -3.2), (3.3, -4.0), arrowstyle="-|>", mutation_scale=18, color=GRAY, lw=1.6,
                                 linestyle="--"))
    ax.text(5.0, 0.35, "② 같은 필터를 모든 위치에", ha="center", va="bottom", fontsize=15, color=TEAL, fontweight="bold")
    ax.text(8.3, -3.0, "귀는 어디\n있어도 귀", ha="center", va="center", fontsize=13, color=DARK)
    ax.text(5.0, -8.5, "9개 가중치를 위치마다 재사용", ha="center", va="bottom", fontsize=13, color=DARK)
    # ③ 계층: 층을 쌓으면 넓게
    ax = axs[2]
    for k, (x0, n, lab) in enumerate(((0, 6, "선"), (4.0, 4, "모양"), (7.2, 2, "물체"))):
        y0 = -3 + n / 2
        _cells(ax, x0, y0, n, fc=[MINT2, "#9FD0DB", TEAL2][k])
        ax.text(x0 + n / 2, -6.3, lab, ha="center", va="top", fontsize=13, color=DARK, fontweight="bold")
        if k < 2:
            ax.add_patch(FancyArrowPatch((x0 + n + 0.15, -3), (x0 + n + 0.85, -3), arrowstyle="-|>",
                                         mutation_scale=18, color=TEAL2, lw=2))
    ax.text(5.0, 0.35, "③ 층을 쌓아 넓게 본다", ha="center", va="bottom", fontsize=15, color=TEAL, fontweight="bold")
    ax.text(5.0, -8.5, "위층의 한 칸은 아래층의 넓은 영역을 요약", ha="center", va="bottom", fontsize=13, color=DARK)
    fig.tight_layout(w_pad=1.5)
    save(fig, "inductive_bias.png")


# ---------------------------------------------------------------- 2c. 다리 놓기: 고정된 창 vs 입력에 따른 비중 (슬라이드 36)
def fig_bridge_sketch():
    fig, axs = plt.subplots(1, 2, figsize=(13.5, 3.0))
    for ax in axs:
        ax.set_xlim(-0.3, 15.3); ax.set_ylim(-3.6, 1.6); ax.set_aspect("equal"); ax.axis("off")
    n = 9
    for ax, mode in zip(axs, ("cnn", "attn")):
        for j in range(n):
            on = (3 <= j <= 5) if mode == "cnn" else True
            ax.add_patch(Rectangle((j * 1.2, -3.2), 1.0, 1.0, fc=ACC_BG if on else MINT2, ec=ACC if on else "white",
                                   lw=2 if on else 1.5))
            ax.text(j * 1.2 + 0.5, -2.7, f"x{j + 1}", ha="center", va="center", fontsize=11, color=DARK)
        ox, oy = 4 * 1.2 + 0.5, 0.6
        ax.add_patch(Rectangle((ox - 0.5, oy - 0.5), 1.0, 1.0, fc=TEAL, ec="none"))
        ax.text(ox, oy, "y", ha="center", va="center", fontsize=13, color="white", fontweight="bold")
        rng = np.random.default_rng(3)
        wts = rng.uniform(0.2, 1.0, n); wts[[1, 4, 7]] = (2.6, 1.6, 3.2)
        for j in range(n):
            if mode == "cnn":
                if 3 <= j <= 5:
                    ax.plot([j * 1.2 + 0.5, ox], [-2.2, oy - 0.5], color=ACC, lw=2.2)
            else:
                ax.plot([j * 1.2 + 0.5, ox], [-2.2, oy - 0.5], color=ACC, lw=wts[j], alpha=min(1, 0.35 + wts[j] / 3))
        ax.text(12.4, -0.5, "고정된 3×3 창\n같은 가중치" if mode == "cnn" else "입력마다 달라지는\n위치와 비중",
                ha="left", va="center", fontsize=13, color=ACC if mode == "attn" else DARK, fontweight="bold")
    axs[0].set_title("CNN: 참조 위치와 비중이 미리 정해진다", fontsize=15, color=TEAL)
    axs[1].set_title("Attention (5주차): 참조 위치와 비중을 계산한다", fontsize=15, color=ACC)
    fig.tight_layout(w_pad=2)
    save(fig, "bridge_sketch.png")


# ---------------------------------------------------------------- 3. 파라미터 수 비교
def fig_params():
    fc = 3072 * 65536
    local = 32 * 32 * 64 * 27
    conv = 27 * 64
    labels = ["Fully connected\n(모든 입력 → 모든 출력)", "국소 연결만\n(가중치 공유 없음)", "합성곱\n(국소 연결 + 공유)"]
    vals = [fc, local, conv]
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    cols = [GRAY, TEAL2, ACC]
    bars = ax.barh(labels[::-1], vals[::-1], color=cols[::-1], height=.55)
    ax.set_xscale("log")
    logfmt(ax, "x")
    ax.set_xlim(1e2, 5e10)
    for b, v in zip(bars, vals[::-1]):
        ax.text(v * 1.6, b.get_y() + b.get_height() / 2, f"{v:,}", va="center", fontsize=14, color=DARK,
                fontweight="bold")
    ax.set_xlabel("가중치 수 (log 눈금, bias 제외)", fontsize=12)
    ax.tick_params(axis="y", labelsize=12.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("입력 32×32×3 → 출력 32×32×64 (3×3 창, 같은 크기 유지)", fontsize=13, color=TEAL, pad=12)
    save(fig, "params_fc_conv.png")


# ---------------------------------------------------------------- 4. Pooling
def fig_pool():
    x = np.array([[1, 3, 2, 0], [4, 6, 1, 1], [0, 2, 9, 5], [3, 1, 4, 7]])
    fig, ax = canvas(8.4, 4.6, (-0.4, 10.4), (-5.5, 1.1))
    quad = [MINT2, ACC_BG, "#E3F1D9", "#EDE3F6"]
    for i in range(4):
        for j in range(4):
            q = (i // 2) * 2 + j // 2
            ax.add_patch(Rectangle((j, -i - 1), 1, 1, fc=quad[q], ec="white", lw=2))
            ax.text(j + .5, -i - .5, str(x[i, j]), ha="center", va="center", fontsize=15,
                    color=DARK, fontweight="bold" if x[i, j] == x[(i // 2) * 2:(i // 2) * 2 + 2, (j // 2) * 2:(j // 2) * 2 + 2].max() else None)
    ax.text(2, 0.35, "입력 (4×4)", ha="center", fontsize=14, color=TEAL, fontweight="bold")
    ax.add_patch(FancyArrowPatch((4.4, -2), (6.2, -2), arrowstyle="-|>", mutation_scale=22, color=TEAL2, lw=2.5))
    ax.text(5.3, -1.4, "2×2 max\nstride 2", ha="center", fontsize=11.5, color=GRAY)
    y = x.reshape(2, 2, 2, 2).max(axis=(1, 3))
    for i in range(2):
        for j in range(2):
            ax.add_patch(Rectangle((6.8 + j * 1.3, -1 - i * 1.3 - .3), 1.3, 1.3, fc=quad[i * 2 + j], ec="white", lw=2))
            ax.text(6.8 + j * 1.3 + .65, -1 - i * 1.3 + .35, str(y[i, j]), ha="center", va="center", fontsize=17,
                    fontweight="bold", color=ACC)
    ax.text(8.1, 0.35, "출력 (2×2)", ha="center", fontsize=14, color=TEAL, fontweight="bold")
    ax.text(5, -4.9, "학습 파라미터 0개 · 공간 크기 1/2 · 작은 이동에 덜 민감", ha="center", fontsize=12.5, color=DARK)
    save(fig, "pooling.png")


# ---------------------------------------------------------------- 5. 수용 영역
def fig_receptive():
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.axis("off")
    n = 11
    ys = [0, 1.3, 2.6, 3.9]
    names = ["입력", "층 1 (3×3)", "층 2 (3×3)", "층 3 (3×3)"]
    c = 5
    rf = {3: [c], 2: [c - 1, c, c + 1], 1: list(range(c - 2, c + 3)), 0: list(range(c - 3, c + 4))}
    for L, yy in enumerate(ys):
        for i in range(n):
            on = i in rf[L]
            col = (ACC if L == 3 else TEAL) if on else "#DDE7EB"
            ax.add_patch(plt.Circle((i, yy), .28, color=col, zorder=3))
        ax.text(-1.0, yy, names[L], ha="right", va="center", fontsize=12, color=DARK)
    for L in (3, 2, 1):
        for i in rf[L]:
            for d in (-1, 0, 1):
                ax.plot([i, i + d], [ys[L], ys[L - 1]], color=TEAL2, lw=1.4, zorder=1, alpha=.8)
    ax.text(n + 0.2, ys[0], "입력 7칸을 봄 (수용 영역 7)", va="center", fontsize=12.5, color=ACC, fontweight="bold")
    ax.text(n + 0.2, ys[1], "층1의 5칸에 의존", va="center", fontsize=11, color=GRAY)
    ax.text(n + 0.2, ys[2], "층2의 3칸에 의존", va="center", fontsize=11, color=GRAY)
    ax.text(n + 0.2, ys[3], "층3 뉴런 하나", va="center", fontsize=11, color=ACC)
    ax.set_xlim(-4.2, n + 4.2)
    ax.set_ylim(-.6, 4.5)
    ax.set_aspect("equal")
    save(fig, "receptive_field.png")


# ---------------------------------------------------------------- 6. LeNet-5 shape 흐름
def pipeline(stages, name, figsize, scale, title=None, fs=11.5, stagger=0.0):
    """stagger > 0이면 아래쪽 shape 라벨을 홀수 번째마다 그만큼 더 내려 이웃끼리 겹치지 않게 한다."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")
    x = 0
    maxh = max(s[1] for s in stages) * scale
    for i, (lab, size, depth, col, sub) in enumerate(stages):
        h = size * scale
        w = 0.25 + depth
        yb = (maxh - h) / 2
        ax.add_patch(FancyBboxPatch((x, yb), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc=col, ec="white", lw=1.5))
        ax.text(x + w / 2, maxh + 0.45, lab, ha="center", va="bottom", fontsize=fs, color=DARK, fontweight="bold")
        sy = -0.35 - (stagger if i % 2 else 0)
        ax.text(x + w / 2, sy, sub, ha="center", va="top", fontsize=fs - 1.5, color=GRAY)
        if i < len(stages) - 1:
            ax.add_patch(FancyArrowPatch((x + w + 0.08, maxh / 2), (x + w + 0.62, maxh / 2), arrowstyle="-|>",
                                         mutation_scale=14, color=TEAL2, lw=1.8))
        x += w + 0.7
    ax.set_xlim(-0.3, x)
    ax.set_ylim(-1.3 - stagger, maxh + 1.1)
    if title:
        ax.set_title(title, fontsize=13, color=TEAL, pad=4)
    save(fig, name)


def fig_lenet():
    st = [("입력", 32, .25, "#B0BEC5", "1@32×32"),
          ("C1 conv5", 28, .6, TEAL2, "6@28×28"),
          ("S2 pool", 14, .6, MINT2, "6@14×14"),
          ("C3 conv5", 10, 1.1, TEAL2, "16@10×10"),
          ("S4 pool", 5, 1.1, MINT2, "16@5×5"),
          ("C5", 1, .2, TEAL, "120"),
          ("F6", 1, .2, TEAL, "84"),
          ("출력", 1, .2, ACC, "10")]
    # 크기를 보기 좋게: 1인 것은 세로 막대
    st2 = []
    for lab, s, d, c, sub in st:
        st2.append((lab, s if s > 1 else {"120": 20, "84": 15, "10": 6}[sub], d, c, sub))
    pipeline(st2, "lenet_pipeline.png", (11.5, 3.8), 0.12, fs=14, stagger=0.6)


# ---------------------------------------------------------------- 7. 이동 등변성 실험
def conv2d(x, k):
    H, W = x.shape
    K = k.shape[0]
    return np.array([[np.sum(x[i:i + K, j:j + K] * k) for j in range(W - K + 1)] for i in range(H - K + 1)])


def fig_equivariance():
    pat = np.array([[1, 0, 0], [1, 0, 0], [1, 1, 1]])  # L 모양
    x1 = np.zeros((5, 5)); x1[0:3, 0:3] = pat
    x2 = np.zeros((5, 5)); x2[1:4, 2:5] = pat
    k = pat.astype(float)
    y1, y2 = conv2d(x1, k), conv2d(x2, k)
    fig, ax = canvas(9.6, 7.0, (-0.4, 17.4), (-12.4, 1.3))
    for r, (x, y, lab) in enumerate(((x1, y1, "원래 입력 (5×5)"), (x2, y2, "아래 1칸·오른쪽 2칸 이동"))):
        oy = -r * 6.3
        grid(ax, x, 0, oy, cell=1.0, fs=13, fmt="{:.0f}", title=lab, title_fs=14)
        ax.add_patch(FancyArrowPatch((5.4, oy - 2.5), (7.3, oy - 2.5), arrowstyle="-|>", mutation_scale=22,
                                     color=TEAL2, lw=2.4))
        ax.text(6.35, oy - 2.95, "3×3 필터", ha="center", va="top", fontsize=12, color=GRAY)
        am = np.unravel_index(np.argmax(y), y.shape)
        grid(ax, y, 7.8, oy - 1.0, cell=1.0, fs=13, fmt="{:.0f}", hl=(am[0], am[1], 1, 1),
             title="출력 (3×3)" if r == 0 else None, title_fs=14)
        ax.add_patch(FancyArrowPatch((11.2, oy - 2.5), (12.7, oy - 2.5), arrowstyle="-|>", mutation_scale=22,
                                     color=TEAL2, lw=2.4))
        ax.text(12.25, oy - 2.95, "전체 max", ha="center", va="top", fontsize=12, color=GRAY)
        ax.add_patch(Rectangle((13.1, oy - 3.1), 1.3, 1.2, fc=ACC_BG, ec=ACC, lw=2))
        ax.text(13.75, oy - 2.5, f"{y.max():.0f}", ha="center", va="center", fontsize=17, color=ACC, fontweight="bold")
        ax.text(14.8, oy - 2.5, f"최댓값 위치\n{tuple(int(v) for v in am)}", ha="left", va="center", fontsize=12.5,
                color=DARK)
    ax.text(8.5, -12.1, "출력 지도는 입력과 같은 만큼 이동(등변성) · 전체 max는 이동과 무관(이 경우의 불변성)",
            ha="center", va="bottom", fontsize=12.5, color=DARK)
    save(fig, "equivariance.png")


# ---------------------------------------------------------------- 8. SVM margin
def fig_svm():
    pos = np.array([[3, 3], [4, 2], [4.2, 3.6], [5, 2.6], [3.4, 4.3], [5.4, 4], [4.6, 5], [6, 3.1]])
    neg = np.array([[2, 2], [1, 3], [0.6, 1.4], [1.6, 0.8], [0.5, 2.6], [2.2, 0.6], [1.2, 2.0], [0.3, 0.5]])
    fig, ax = plt.subplots(figsize=(7.4, 5.4))
    xs = np.linspace(-0.5, 7, 10)
    ax.fill_between(xs, 4 - xs, 6 - xs, color=MINT2, alpha=.8, lw=0)
    ax.plot(xs, 5 - xs, color=TEAL, lw=3, label="최대 마진 경계")
    ax.plot(xs, 6 - xs, color=TEAL, lw=1.2, ls="--")
    ax.plot(xs, 4 - xs, color=TEAL, lw=1.2, ls="--")
    yy = np.linspace(-0.2, 5.6, 10)
    ax.plot(2.7 - 0.3 * yy, yy, color=GRAY, lw=2, ls=":", label="분리는 되지만 마진이 작은 경계")
    ax.scatter(pos[:, 0], pos[:, 1], s=90, color=ACC, zorder=3, label="클래스 +1")
    ax.scatter(neg[:, 0], neg[:, 1], s=90, color=TEAL2, marker="s", zorder=3, label="클래스 −1")
    for p in ([3, 3], [4, 2], [2, 2], [1, 3]):
        ax.scatter(*p, s=320, facecolors="none", edgecolors=DARK, lw=1.8, zorder=4)
    ax.annotate("서포트 벡터", xy=(1, 3), xytext=(-0.3, 4.6), fontsize=12, color=DARK,
                arrowprops=dict(arrowstyle="->", color=DARK))
    ax.annotate("", xy=(2.5, 2.5), xytext=(3.0, 3.0), arrowprops=dict(arrowstyle="<->", color=ACC, lw=2))
    ax.text(3.05, 2.35, "마진", fontsize=13, color=ACC, fontweight="bold")
    ax.set_xlim(-0.5, 6.8)
    ax.set_ylim(-0.2, 5.6)
    ax.set_aspect("equal")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=10.5, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlabel("x1", fontsize=11); ax.set_ylabel("x2", fontsize=11)
    save(fig, "svm_margin.png")


# ---------------------------------------------------------------- 9. 커널: 차원 올리기
def fig_kernel():
    a = np.array([-3, -2.5, -2.1, 2.2, 2.6, 3.1])
    b = np.array([-1.2, -0.7, -0.2, 0.3, 0.8, 1.3])
    fig, axs = plt.subplots(2, 1, figsize=(8, 5.6), gridspec_kw=dict(height_ratios=[1, 2.6]))
    ax = axs[0]
    ax.axhline(0, color=LINE, lw=2)
    ax.scatter(a, np.zeros_like(a), s=120, color=ACC, zorder=3, label="클래스 +1")
    ax.scatter(b, np.zeros_like(b), s=120, color=TEAL2, marker="s", zorder=3, label="클래스 −1")
    ax.set_xlim(-3.6, 3.6)
    ax.set_ylim(-0.7, 1.3); ax.set_yticks([])
    ax.set_xlabel("x", fontsize=12, labelpad=1)
    ax.set_title("1차원: 점 하나로는 두 부류를 나눌 수 없다", fontsize=13.5, color=TEAL)
    ax.legend(loc="upper center", ncol=2, frameon=False, fontsize=11.5, bbox_to_anchor=(0.5, 1.02))
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax = axs[1]
    ax.scatter(a, a ** 2, s=120, color=ACC, zorder=3)
    ax.scatter(b, b ** 2, s=120, color=TEAL2, marker="s", zorder=3)
    xx = np.linspace(-3.5, 3.5, 100)
    ax.plot(xx, xx ** 2, color=LINE, lw=1)
    ax.axhline(3.2, color=TEAL, lw=2.5)
    ax.text(0, 3.75, "$x^2$ = 3.2 : 직선 경계", fontsize=12.5, color=TEAL, va="bottom", ha="center")
    ax.set_xlim(-3.6, 3.6)
    ax.set_xlabel("x", fontsize=12); ax.set_ylabel("$x^2$", fontsize=13)
    ax.set_title("φ(x) = (x, $x^2$)로 올리면 선형 분리 가능", fontsize=13.5, color=TEAL)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(h_pad=1.5)
    save(fig, "kernel_lift.png")


# ---------------------------------------------------------------- 10. AlexNet 흐름
def fig_alexnet():
    st = [("입력", 227, .3, "#B0BEC5", "227×227×3"),
          ("conv1\n11×11 s4", 55, .9, TEAL2, "55×55×96"),
          ("pool", 27, .9, MINT2, "27×27×96"),
          ("conv2\n5×5", 27, 1.5, TEAL2, "27×27×256"),
          ("pool", 13, 1.5, MINT2, "13×13×256"),
          ("conv3·4\n3×3", 13, 2.0, TEAL2, "13×13×384"),
          ("conv5\n3×3", 13, 1.5, TEAL2, "13×13×256"),
          ("pool", 6, 1.5, MINT2, "6×6×256"),
          ("FC6·7", 90, .25, TEAL, "4096"),
          ("FC8", 40, .25, ACC, "1000")]
    st = [(l, {227: 110}.get(s, s), d, c, sub) for l, s, d, c, sub in st]
    pipeline(st, "alexnet_pipeline.png", (12.5, 3.9), 0.03, fs=15, stagger=0.75)


# ---------------------------------------------------------------- 11. ReLU vs sigmoid gradient
def fig_relu_grad():
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.0))
    z = np.linspace(-5, 5, 400)
    s = 1 / (1 + np.exp(-z))
    ax = axs[0]
    ax.plot(z, s * (1 - s), color=ACC, lw=3)
    ax.plot(z, (z > 0).astype(float), color=TEAL, lw=3)
    # 범례 대신 곡선 옆에 직접 이름을 쓴다 (겹침 방지)
    ax.text(-4.8, 0.56, "sigmoid′ (최대 0.25)", fontsize=13, color=ACC, fontweight="bold", va="bottom")
    ax.text(2.6, 1.07, "ReLU′ = 1  (z > 0)", fontsize=13, color=TEAL, fontweight="bold", va="bottom", ha="center")
    ax.text(-3.0, 0.30, "ReLU′ = 0  (z < 0)", fontsize=12, color=TEAL, va="bottom", ha="center")
    ax.set_ylim(-0.08, 1.35)
    ax.set_xlabel("z", fontsize=13)
    ax.set_title("활성화 함수 하나의 미분", fontsize=14.5, color=TEAL)
    ax.spines[["top", "right"]].set_visible(False)
    ax = axs[1]
    L = np.arange(1, 21)
    ax.semilogy(L, 0.25 ** L, "o-", color=ACC, lw=2.5, ms=5)
    ax.semilogy(L, np.ones_like(L, dtype=float), "s-", color=TEAL, lw=2.5, ms=5)
    ax.text(13.5, 0.12, "1^L — ReLU (활성 경로): 줄지 않는다", fontsize=13, color=TEAL, fontweight="bold", ha="center",
            va="top")
    ax.text(1.0, 3e-12, "0.25^L — sigmoid 최선의 경우", fontsize=13, color=ACC, fontweight="bold", va="bottom")
    ax.annotate("10층: 9.5×10⁻⁷", xy=(10, 0.25 ** 10), xytext=(13.0, 1e-5), fontsize=13, color=ACC,
                arrowprops=dict(arrowstyle="->", color=ACC))
    ax.set_xlabel("층 수 L", fontsize=13)
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.set_title("L층을 거치며 곱해진 미분 (가중치 효과 제외)", fontsize=14.5, color=TEAL)
    ax.set_ylim(1e-13, 30)
    logfmt(ax)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(w_pad=3)
    save(fig, "relu_grad.png")


# ---------------------------------------------------------------- 12. ILSVRC
def fig_ilsvrc():
    yrs = ["2010\nNEC-UIUC", "2011\nXRCE", "2012\nAlexNet", "2013\nClarifai", "2014\nGoogLeNet", "2015\nResNet"]
    err = [28.2, 25.8, 15.3, 11.7, 6.67, 3.57]
    depth = ["얕은 특징+분류기", "얕은 특징+분류기", "8층", "CNN", "22층", "152층"]
    cols = [GRAY, GRAY, ACC, TEAL2, TEAL2, TEAL]
    fig, ax = plt.subplots(figsize=(7.6, 4.9))
    bars = ax.bar(yrs, err, color=cols, width=.62)
    for b, e, d in zip(bars, err, depth):
        ax.text(b.get_x() + b.get_width() / 2, e + 0.7, f"{e}%", ha="center", fontsize=13, fontweight="bold", color=DARK)
        ax.text(b.get_x() + b.get_width() / 2, e / 2, d, ha="center", va="center", fontsize=9.5, color="white",
                rotation=90 if len(d) > 4 else 0, fontweight="bold")
    ax.annotate("2014년 2위 VGG: 7.3% (16–19층)", xy=(4.3, 7.3), xytext=(2.75, 20.5), fontsize=10.5, color=TEAL2,
                arrowprops=dict(arrowstyle="->", color=TEAL2))
    ax.set_ylabel("top-5 분류 오류율 (%)", fontsize=12)
    ax.set_ylim(0, 33)
    ax.tick_params(axis="x", labelsize=10.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("ILSVRC 분류 우승 팀의 top-5 오류", fontsize=13, color=TEAL)
    save(fig, "ilsvrc.png")


# ---------------------------------------------------------------- 13. degradation 개념도
def fig_degradation():
    it = np.linspace(0, 1, 200)
    def curve(final, speed):
        return final + (0.6 - final) * np.exp(-speed * it * 6)
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.1), sharey=True)
    for ax, (a, b, ttl) in zip(axs, (((0.10, 1.0), (0.16, 0.8), "Plain 망 (shortcut 없음)"),
                                       ((0.11, 1.0), (0.06, 0.9), "Residual 망"))):
        ax.plot(it, curve(*a), color=TEAL2, lw=3, label="20층")
        ax.plot(it, curve(*b), color=ACC, lw=3, label="56층")
        ax.set_title(ttl, fontsize=18, color=TEAL)
        ax.set_xlabel("학습 진행 →", fontsize=16)
        ax.set_xticks([])
        ax.set_ylim(0, 0.66)
        ax.legend(frameon=False, fontsize=16, loc="upper right")
        ax.spines[["top", "right"]].set_visible(False)
    axs[0].set_ylabel("학습(training) 오류", fontsize=16)
    axs[0].set_yticks([])
    # 설명 글은 곡선 위쪽 빈 공간(오른쪽 중단)에 둔다
    axs[0].text(0.98, 0.30, "깊은 쪽(56층)이 학습 오류도 높다\n→ 과적합이 아니라 최적화 문제", fontsize=16, color=ACC,
                va="bottom", ha="right")
    axs[1].text(0.98, 0.30, "깊이의 이점이 다시 나타난다", fontsize=16, color=TEAL, va="bottom", ha="right")
    fig.text(0.5, -0.02, "개념도: He et al. (2015) Fig.1·6의 정성적 경향을 단순화해 그린 것 (실제 수치 아님)",
             ha="center", fontsize=14, color=GRAY)
    fig.tight_layout(w_pad=2)
    save(fig, "degradation.png")


# ---------------------------------------------------------------- 14. residual block + gradient toy
def toy_grad_norms(depth=40, n=64, residual=False, seed=0):
    rng = np.random.default_rng(seed)
    h = rng.normal(size=n)
    Ws, pre, hs = [], [], [h]
    for _ in range(depth):
        W = rng.normal(scale=np.sqrt(1.0 / n), size=(n, n))  # ReLU에 작은(Xavier식) 초기화
        z = W @ h
        f = np.maximum(z, 0)
        h = h + 0.1 * f if residual else f
        Ws.append(W); pre.append(z); hs.append(h)
    g = np.ones(n) / np.sqrt(n)
    norms = [np.linalg.norm(g)]
    for W, z in zip(Ws[::-1], pre[::-1]):
        gf = (W.T @ (g * (z > 0)))
        g = g + 0.1 * gf if residual else gf
        norms.append(np.linalg.norm(g))
    return np.array(norms[::-1])


def fig_residual():
    fig = plt.figure(figsize=(12.5, 4.2))
    ax = fig.add_axes([0.0, 0.0, 0.40, 1.0])
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    def blk(y, text, col=MINT2, tc=DARK):
        ax.add_patch(FancyBboxPatch((2.2, y), 4.0, 1.1, boxstyle="round,pad=0.05,rounding_size=0.2", fc=col, ec="none"))
        ax.text(4.2, y + .55, text, ha="center", va="center", fontsize=13, color=tc, fontweight="bold")
    ax.text(4.2, 9.35, "x", ha="center", fontsize=16, fontweight="bold", color=DARK)
    blk(7.3, "weight layer")
    blk(5.4, "ReLU", col=MINT)
    blk(3.5, "weight layer")
    for y0, y1 in ((9.1, 8.45), (7.3, 6.55), (5.4, 4.65), (3.5, 2.35)):
        ax.add_patch(FancyArrowPatch((4.2, y0), (4.2, y1), arrowstyle="-|>", mutation_scale=16, color=TEAL2, lw=2))
    ax.add_patch(plt.Circle((4.2, 1.95), .4, fc="white", ec=ACC, lw=2.5))
    ax.text(4.2, 1.95, "+", ha="center", va="center", fontsize=20, color=ACC, fontweight="bold")
    ax.plot([4.2, 7.2, 7.2], [8.85, 8.85, 1.95], color=ACC, lw=2.5)
    ax.add_patch(FancyArrowPatch((7.2, 1.95), (4.65, 1.95), arrowstyle="-|>", mutation_scale=16, color=ACC, lw=2.5))
    ax.text(7.45, 5.4, "identity\nshortcut\n(x 그대로)", ha="left", va="center", fontsize=12, color=ACC,
            fontweight="bold")
    ax.text(1.9, 5.9, "F(x)", ha="right", fontsize=15, color=TEAL, fontweight="bold")
    ax.add_patch(FancyArrowPatch((4.2, 1.55), (4.2, 0.75), arrowstyle="-|>", mutation_scale=16, color=TEAL2, lw=2))
    ax.text(4.2, 0.2, "y = x + F(x)", ha="center", fontsize=15, color=DARK, fontweight="bold")
    ax2 = fig.add_axes([0.52, 0.16, 0.46, 0.72])
    d = 40
    p = toy_grad_norms(d, residual=False)
    r = toy_grad_norms(d, residual=True)
    L = np.arange(d + 1)
    ax2.semilogy(L, p / p[-1], color=GRAY, lw=2.8, label="plain: h ← ReLU(Wh)")
    ax2.semilogy(L, r / r[-1], color=ACC, lw=2.8, label="residual: h ← h + F(h)")
    ax2.set_xlabel("층 번호 (0 = 입력 쪽)", fontsize=13.5)
    ax2.set_ylabel("‖∂L/∂h‖ (출력 층 = 1)", fontsize=14)
    ax2.set_title("40층 toy 망에서 입력 쪽으로 전달되는 gradient", fontsize=14, color=TEAL)
    ax2.legend(frameon=False, fontsize=13, loc="lower right")
    logfmt(ax2)
    ax2.spines[["top", "right"]].set_visible(False)
    save(fig, "residual.png")


# ---------------------------------------------------------------- 15. BN vs LN
def fig_norm_axes():
    # regen_figs는 이 그림에 배율 1.0을 쓰므로 글자 크기를 여기서 직접 키운다
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.0))
    B, D = 4, 8
    for ax, mode in zip(axs, ("BN", "LN")):
        ax.set_xlim(-1.3, D + .3); ax.set_ylim(-1.4, B + 1.3); ax.set_aspect("equal"); ax.axis("off")
        for i in range(B):
            for j in range(D):
                on = (j == 2) if mode == "BN" else (i == 1)
                ax.add_patch(Rectangle((j, B - 1 - i), 1, 1, fc=ACC if on else MINT2, ec="white", lw=2))
        ax.text(D / 2, B + 0.25, "특징 축 d →", ha="center", fontsize=17, color=GRAY)
        ax.text(-0.25, B / 2, "샘플 축 B →", ha="right", va="center", fontsize=17, color=GRAY, rotation=90)
        if mode == "BN":
            ax.set_title("BatchNorm: 같은 특징을 batch 전체에서", fontsize=20, color=TEAL)
            ax.text(D / 2, -0.85, "특징마다 B개 값의 평균·분산 → batch에 의존", ha="center", fontsize=17, color=DARK)
        else:
            ax.set_title("LayerNorm: 한 샘플(토큰)의 모든 특징에서", fontsize=20, color=TEAL)
            ax.text(D / 2, -0.85, "샘플마다 d개 값의 평균·분산 → batch와 무관", ha="center", fontsize=17, color=DARK)
    fig.tight_layout(w_pad=3)
    save(fig, "bn_vs_ln.png")


if __name__ == "__main__":
    for f in (fig_image_tensor, fig_conv_sliding, fig_params, fig_pool, fig_receptive, fig_lenet,  # conv_sliding이 inductive_bias·bridge_sketch도 만든다
              fig_equivariance, fig_svm, fig_kernel, fig_alexnet, fig_relu_grad, fig_ilsvrc,
              fig_degradation, fig_residual, fig_norm_axes):
        f()
    print(sorted(os.listdir(OUT)))
