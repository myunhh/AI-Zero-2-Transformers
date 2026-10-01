"""Week 1 그림 생성 (build/assets/week1/*.png). week1.py 에서 호출."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from deckkit import PALETTE_HEX, mpl_setup  # noqa: E402

import numpy as np  # noqa: E402

OUT = os.path.join(HERE, "assets", "week1")
T, T2, A, G, D, M, L = (PALETTE_HEX[k] for k in ("TEAL", "TEAL2", "ACCENT", "GRAY", "DARK", "MINT", "LINE"))
MINT2 = "#CFE8EE"
ACC_BG = "#FDF1E8"

plt = mpl_setup()
plt.rcParams["font.family"] = ["NanumGothic", "DejaVu Sans"]  # 한글 + 기호(−, ŷ, ᵀ, ₕ) fallback
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402


def _save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    fig.savefig(p, facecolor="white")
    plt.close(fig)
    return p


def _grid(ax, x, y, rows, cols, c=0.3, fc=MINT2, ec=T, lw=1.0, vals=None, fs=10, alpha=1.0):
    """(x,y)=좌상단. rows 아래로, cols 오른쪽으로."""
    for r in range(rows):
        for k in range(cols):
            ax.add_patch(Rectangle((x + k * c, y - (r + 1) * c), c, c, fc=fc, ec=ec, lw=lw, alpha=alpha))
            if vals is not None:
                ax.text(x + (k + .5) * c, y - (r + .5) * c, str(vals[r][k]), ha="center", va="center",
                        fontsize=fs, color=D)


def _clean(ax):
    ax.set_aspect("equal")
    ax.axis("off")


# ------------------------------------------------------------------ 1. 스칼라→텐서
def tensor_ranks():
    fig, ax = plt.subplots(figsize=(9, 6))
    _clean(ax)
    c = 0.42
    # scalar
    ax.add_patch(Rectangle((0.6, 5.3), c * 2.4, c * 2.0, fc=ACC_BG, ec=A, lw=2))
    ax.text(0.6 + c * 1.2, 5.3 + c * 1.0, "0.42", ha="center", va="center", fontsize=14, color=D, weight="bold")
    ax.text(0.2, 7.0, "scalar  shape ()", fontsize=16, color=T, weight="bold")
    ax.text(0.2, 4.75, "수 하나 · 예: 손실 0.42", fontsize=13, color=G)
    # vector
    vx = 5.0
    ax.text(vx, 7.0, "vector  shape (8,)", fontsize=16, color=T, weight="bold")
    _grid(ax, vx, 6.25, 1, 8, c=c)
    ax.text(vx, 5.35, "한 축 · 토큰 하나의 특징 8개", fontsize=13, color=G)
    # matrix
    ax.text(0.2, 4.0, "matrix  shape (5, 8)", fontsize=16, color=T, weight="bold")
    _grid(ax, 0.3, 3.55, 5, 8, c=c)
    ax.text(0.2, 0.95 - 0.2, "두 축 · 토큰 5개 × 특징 8개", fontsize=13, color=G)
    # tensor 3D: two stacked matrices
    tx = 5.35
    ax.text(tx - 0.3, 4.0, "tensor  shape (2, 5, 8)", fontsize=16, color=T, weight="bold")
    _grid(ax, tx + 0.35, 3.55 - 0.05, 5, 8, c=c * 0.92, fc=M, ec=T2)
    _grid(ax, tx, 3.2, 5, 8, c=c * 0.92, fc=MINT2, ec=T)
    ax.text(tx - 0.3, 0.75, "세 축 이상 · 문장 2개 × 토큰 5 × 특징 8", fontsize=13, color=G)
    ax.annotate("", xy=(tx + 0.35, 3.62), xytext=(tx, 3.27),
                arrowprops=dict(arrowstyle="->", color=A, lw=2))
    ax.text(tx - 0.55, 3.55, "B", fontsize=15, color=A, weight="bold")
    ax.set_xlim(0, 9.4)
    ax.set_ylim(0.4, 7.5)
    return _save(fig, "tensor_ranks.png")


# ------------------------------------------------------------------ 2. 배치 축
def batch_axis():
    fig, ax = plt.subplots(figsize=(9, 7))
    _clean(ax)
    c = 0.62
    s1 = ["나는", "학교에", "간", "다", "."]
    s2 = ["비가", "온다", ".", "PAD", "PAD"]
    x0, y0 = 2.6, 5.4
    off = 0.7
    # back sentence (b=1)
    for r in range(5):
        pad = s2[r] == "PAD"
        for k in range(8):
            ax.add_patch(Rectangle((x0 + off + k * c, y0 + off - (r + 1) * c), c, c,
                                   fc="#EEEEEE" if pad else M, ec=G if pad else T2, lw=1))
    # front sentence (b=0)
    for r in range(5):
        for k in range(8):
            ax.add_patch(Rectangle((x0 + k * c, y0 - (r + 1) * c), c, c, fc=MINT2, ec=T, lw=1))
        ax.text(x0 - 0.12, y0 - (r + .5) * c, s1[r], ha="right", va="center", fontsize=15, color=D)
    for r in range(5):
        col = G if s2[r] == "PAD" else T2
        ax.text(x0 + off + 8 * c + 0.12, y0 + off - (r + .5) * c, s2[r], ha="left", va="center",
                fontsize=15, color=col, weight="bold" if s2[r] == "PAD" else None)
    # axis labels
    ax.annotate("", xy=(x0 + 8 * c, y0 - 5 * c - 0.35), xytext=(x0, y0 - 5 * c - 0.35),
                arrowprops=dict(arrowstyle="->", color=T, lw=2.2))
    ax.text(x0 + 4 * c, y0 - 5 * c - 0.8, "d = 8  (특징 축, 마지막 축)", ha="center", fontsize=17, color=T,
            weight="bold")
    ax.annotate("", xy=(x0 - 1.6, y0 - 5 * c), xytext=(x0 - 1.6, y0),
                arrowprops=dict(arrowstyle="->", color=T, lw=2.2))
    ax.text(x0 - 1.8, y0 - 2.5 * c, "N = 5\n(토큰)", ha="right", va="center", fontsize=17, color=T, weight="bold")
    ax.annotate("", xy=(x0 + off + 0.1, y0 + off + 0.1), xytext=(x0 + 0.1, y0 + 0.1),
                arrowprops=dict(arrowstyle="->", color=A, lw=2.8))
    ax.text(x0 - 0.2, y0 + 0.6, "B = 2 (문장)", ha="right", fontsize=17, color=A, weight="bold")
    ax.text(x0 + 4.9, y0 + off + 0.3, "짧은 문장은 PAD로 길이를 맞춘다", ha="center", fontsize=15, color=G)
    ax.text(x0 + 2.4, y0 - 5 * c - 1.45, "shape = (B, N, d) = (2, 5, 8)", ha="center", fontsize=18, color=D,
            weight="bold", family="DejaVu Sans Mono")
    ax.set_xlim(-0.6, 9.4)
    ax.set_ylim(0.4, 7.1)
    return _save(fig, "batch_axis.png")


# ------------------------------------------------------------------ 3. Broadcasting
def broadcasting():
    fig, ax = plt.subplots(figsize=(9, 6.2))
    _clean(ax)
    c = 0.6
    Am = [[1, 2, 3], [4, 5, 6]]
    b = [[10, 20, 30]]
    R = [[11, 22, 33], [14, 25, 36]]
    y = 5.6
    ax.text(0.1, y + 0.45, "①  (2, 3) + (3,)  →  (2, 3)", fontsize=16, color=T, weight="bold")
    _grid(ax, 0.2, y, 2, 3, c=c, vals=Am, fs=14)
    ax.text(2.3, y - c, "+", fontsize=24, ha="center", va="center", color=D)
    _grid(ax, 2.7, y, 1, 3, c=c, vals=b, fs=14, fc=ACC_BG, ec=A)
    _grid(ax, 2.7, y - c, 1, 3, c=c, vals=b, fs=14, fc="white", ec=A, alpha=0.9)
    for k in range(3):
        ax.add_patch(Rectangle((2.7 + k * c, y - 2 * c), c, c, fc="none", ec=A, lw=1.5, ls="--"))
    ax.text(2.7 + 1.5 * c, y - 2 * c - 0.3, "행 방향으로 복제된 것처럼", ha="center", fontsize=12, color=A)
    ax.text(4.95, y - c, "=", fontsize=24, ha="center", va="center", color=D)
    _grid(ax, 5.35, y, 2, 3, c=c, vals=R, fs=14, fc=M)

    y2 = 2.55
    ax.text(0.1, y2 + 0.45, "②  (2, 1) + (1, 3)  →  (2, 3)", fontsize=16, color=T, weight="bold")
    _grid(ax, 0.2 + c, y2, 2, 1, c=c, vals=[[0], [10]], fs=14, fc=ACC_BG, ec=A)
    ax.text(2.3, y2 - c, "+", fontsize=24, ha="center", va="center", color=D)
    _grid(ax, 2.7, y2 - c / 2, 1, 3, c=c, vals=[[1, 2, 3]], fs=14, fc=ACC_BG, ec=A)
    ax.text(4.95, y2 - c, "=", fontsize=24, ha="center", va="center", color=D)
    _grid(ax, 5.35, y2, 2, 3, c=c, vals=[[1, 2, 3], [11, 12, 13]], fs=14, fc=M)
    ax.text(0.1, 0.75, "규칙: 뒤쪽 축부터 맞춘다 — 크기가 같거나, 한쪽이 1이면 OK", fontsize=13.5, color=D)
    ax.text(0.1, 0.25, "(2, 3) + (2,) 는 오류: 마지막 축 3 ≠ 2", fontsize=13.5, color=A, weight="bold")
    ax.set_xlim(0, 7.6)
    ax.set_ylim(0, 6.3)
    return _save(fig, "broadcasting.png")


# ------------------------------------------------------------------ 4. 행렬곱 shape
def matmul_shape():
    fig, ax = plt.subplots(figsize=(10, 5.2))
    _clean(ax)
    c = 0.55
    y = 4.3
    # A (2,3)
    _grid(ax, 0.3, y, 2, 3, c=c, fc=M, ec=T)
    for k in range(3):
        ax.add_patch(Rectangle((0.3 + k * c, y - c), c, c, fc=ACC_BG, ec=A, lw=2))
    ax.text(0.3 + 1.5 * c, y + 0.3, "A  (2, 3)", ha="center", fontsize=16, color=T, weight="bold")
    ax.text(2.3, y - c, "@", fontsize=24, ha="center", va="center", color=D)
    # B (3,4)
    bx = 2.8
    _grid(ax, bx, y + c / 2, 3, 4, c=c, fc=M, ec=T)
    for r in range(3):
        ax.add_patch(Rectangle((bx + 1 * c, y + c / 2 - (r + 1) * c), c, c, fc=ACC_BG, ec=A, lw=2))
    ax.text(bx + 2 * c, y + c / 2 + 0.3, "B  (3, 4)", ha="center", fontsize=16, color=T, weight="bold")
    ax.text(bx + 4 * c + 0.45, y - c, "=", fontsize=24, ha="center", va="center", color=D)
    # C (2,4)
    cx = bx + 4 * c + 0.9
    _grid(ax, cx, y, 2, 4, c=c, fc=M, ec=T)
    ax.add_patch(Rectangle((cx + 1 * c, y - c), c, c, fc=A, ec=A, lw=2))
    ax.text(cx + 2 * c, y + 0.3, "C  (2, 4)", ha="center", fontsize=16, color=T, weight="bold")
    ax.text(cx + 4 * c + 0.2, y - 0.5 * c, "C[0,1] = A의 0행 · B의 1열\n(길이 3짜리 내적 하나)",
            fontsize=13, color=A, va="center")
    # shape rule (여러 색 텍스트를 한 줄로)
    from matplotlib.offsetbox import AnchoredOffsetbox, HPacker, TextArea
    parts = [("(2, ", D), ("3", A), (") @ (", D), ("3", A), (", 4)  →  (2, 4)", D)]
    boxes = [TextArea(t, textprops=dict(fontsize=26, color=cc, family="DejaVu Sans Mono",
                                         weight="bold" if cc == A else "normal")) for t, cc in parts]
    ab = AnchoredOffsetbox(loc="center left", child=HPacker(children=boxes, align="baseline", pad=0, sep=0),
                           frameon=False, bbox_to_anchor=(0.3, 1.55), bbox_transform=ax.transData, borderpad=0)
    ax.add_artist(ab)
    ax.text(0.3, 0.7, "안쪽 차원(3)이 같아야 곱할 수 있고, 곱하면서 사라진다", fontsize=14.5, color=G)
    ax.set_xlim(0, 10.3)
    ax.set_ylim(0.3, 5.3)
    return _save(fig, "matmul_shape.png")


# ------------------------------------------------------------------ 5. 배치 행렬곱
def batched_matmul():
    fig, ax = plt.subplots(figsize=(9, 5.6))
    _clean(ax)
    c = 0.36

    def stack(x, y, rows, cols, label, n=3, fc=M, ec=T):
        for i in reversed(range(n)):
            _grid(ax, x + i * 0.22, y + i * 0.22, rows, cols, c=c, fc=fc if i == 0 else "#F4FAFB",
                  ec=ec if i == 0 else T2, lw=0.8)
        ax.text(x + cols * c / 2 + 0.2, y + 0.22 * n + 0.15, label, ha="center", fontsize=14, color=T, weight="bold")

    y = 4.4
    stack(0.2, y, 4, 2, "Q  (B,H,T,dₕ)")
    ax.text(1.55, y - 2 * c, "@", fontsize=22, ha="center", va="center", color=D)
    stack(2.0, y - 0.35, 2, 5, "Kᵀ  (B,H,dₕ,S)")
    ax.text(4.7, y - 2 * c, "=", fontsize=22, ha="center", va="center", color=D)
    stack(5.2, y, 4, 5, "점수  (B,H,T,S)", fc=ACC_BG, ec=A)
    ax.text(0.2, 1.75, "앞의 두 축 (B, H) : 그대로 유지 — 같은 계산을 묶음별로 반복", fontsize=14, color=D)
    ax.text(0.2, 1.2, "마지막 두 축 : (T, dₕ) @ (dₕ, S) → (T, S)", fontsize=14, color=D)
    ax.text(0.2, 0.65, "dₕ 는 내적하며 합쳐지는 축 → 결과에서 사라진다", fontsize=14, color=A, weight="bold")
    ax.set_xlim(0, 8.0)
    ax.set_ylim(0.4, 5.6)
    return _save(fig, "batched_matmul.png")


# ------------------------------------------------------------------ 6. 내적 vs cosine + QK^T
def dot_scores():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw=dict(width_ratios=[1, 1.15]))
    q = np.array([1, 2])
    k = np.array([3, -1])
    for v, col, lab, dx in ((q, T, "q=(1,2)", (-0.35, 0.15)), (k, A, "k=(3,−1)", (-1.9, -1.35)),
                            (2 * k, A, "2k=(6,−2)", (-0.6, -0.5))):
        a1.add_patch(FancyArrowPatch((0, 0), tuple(v), arrowstyle="-|>", mutation_scale=18, lw=2.5,
                                     color=col, alpha=1 if lab != "2k=(6,−2)" else 0.45))
        a1.text(v[0] + dx[0], v[1] + dx[1], lab, fontsize=13, color=col, weight="bold")
    a1.axhline(0, color=L, lw=1)
    a1.axvline(0, color=L, lw=1)
    a1.set_xlim(-1, 7)
    a1.set_ylim(-3, 3)
    a1.set_aspect("equal")
    a1.set_title("q·k = 1  →  q·2k = 2\ncos(q,k) = cos(q,2k) = 0.14", fontsize=13.5, color=D)
    a1.tick_params(labelsize=10)
    for s in a1.spines.values():
        s.set_visible(False)
    Q = np.array([[1, 0], [0, 1], [1, 1]])
    K = np.array([[1, 0], [0, 1], [1, 2], [-1, 0]])
    S = Q @ K.T
    cmap = LinearSegmentedColormap.from_list("dv", [A, "#F4F4F4", T])
    a2.imshow(S, cmap=cmap, vmin=-3, vmax=3)
    for i in range(3):
        for j in range(4):
            a2.text(j, i, str(S[i, j]), ha="center", va="center", fontsize=16,
                    color="white" if abs(S[i, j]) >= 2 else D, weight="bold")
    a2.set_xticks(range(4), [f"k{j+1}\n({K[j][0]},{K[j][1]})" for j in range(4)], fontsize=11)
    a2.set_yticks(range(3), [f"q{i+1} ({Q[i][0]},{Q[i][1]})" for i in range(3)], fontsize=11)
    a2.set_title("QKᵀ : (3,2) @ (2,4) → (3,4)\n모든 Query–Key 쌍의 점수", fontsize=13.5, color=D)
    for s in a2.spines.values():
        s.set_visible(False)
    a2.tick_params(length=0)
    fig.tight_layout()
    return _save(fig, "dot_scores.png")


# ------------------------------------------------------------------ 7. softmax / temperature
def softmax_temp():
    z = np.array([2.0, 1.0, 0.0])
    labels = ["고양이", "개", "새"]

    def sm(v):
        e = np.exp(v - v.max())
        return e / e.sum()

    fig, axs = plt.subplots(2, 2, figsize=(9, 6.2))
    panels = [("점수 z (logits)", z, None), ("τ = 0.5 (뾰족)", sm(z / 0.5), 0.5),
              ("τ = 1 (기본 softmax)", sm(z), 1), ("τ = 2 (평평)", sm(z / 2), 2)]
    for ax, (tt, v, tau) in zip(axs.flat, panels):
        col = G if tau is None else (A if tau == 1 else T)
        ax.bar(range(3), v, color=col, width=0.6)
        for i, val in enumerate(v):
            ax.text(i, val + (0.04 if tau else 0.08), f"{val:.3f}" if tau else f"{val:.0f}", ha="center",
                    fontsize=13, color=D, weight="bold")
        ax.set_xticks(range(3), labels, fontsize=12)
        ax.set_ylim(0, 1.08 if tau else 2.5)
        ax.set_title(tt, fontsize=14, color=D)
        ax.tick_params(axis="y", labelsize=10)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    fig.tight_layout(h_pad=1.5)
    return _save(fig, "softmax_temp.png")


# ------------------------------------------------------------------ 8. 미분(접선) + 한 걸음
def _bowl(ax):
    """L(w) = ½(2w − 6)² 골짜기 곡선 (loss_bowl / derivative 공통)."""
    w = np.linspace(-0.3, 4.3, 200)
    Lw = 0.5 * (2 * w - 6) ** 2
    ax.plot(w, Lw, color=T, lw=3)
    ax.text(3.2, 13.5, "L(w) = ½(2w − 6)$^2$", color=T, fontsize=13,
            weight="bold", ha="center")
    ax.set_xlabel("파라미터 w", fontsize=13)
    ax.set_ylabel("손실 L", fontsize=13)
    ax.set_ylim(-0.8, 20)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def derivative():
    # (a) 손실 지형 슬라이드용: 미분·갱신 없이 골짜기 모양과 두 점(w=1, 바닥 w=3)만
    fig, ax = plt.subplots(figsize=(9, 5.8))
    _bowl(ax)
    ax.scatter([1], [8], s=110, color=A, zorder=5)
    ax.text(1.12, 9.0, "지금 위치 w = 1 : L = 8", fontsize=13, color=A, weight="bold")
    ax.scatter([3], [0], s=90, color=G, zorder=5)
    ax.text(3, 1.2, "바닥 w = 3 : L = 0\n(ŷ = 6 = 정답)", fontsize=12.5, color=G, ha="center")
    ax.annotate("", xy=(2.8, 0.5), xytext=(1.2, 7.5),
                arrowprops=dict(arrowstyle="-|>", color=L, lw=1.6, ls="--", mutation_scale=16))
    ax.text(1.75, 4.6, "어느 쪽으로, 얼마나?\n→ Part 4", fontsize=12.5, color=D, ha="left")
    _save(fig, "loss_bowl.png")

    # (b) 미분 슬라이드용: 접선 + 한 걸음
    fig, ax = plt.subplots(figsize=(9, 5.8))
    _bowl(ax)
    # tangent at w=1
    wt = np.linspace(0.1, 1.9, 10)
    ax.plot(wt, 8 - 8 * (wt - 1), color=A, lw=2, ls="--")
    ax.scatter([1], [8], s=110, color=A, zorder=5)
    ax.text(1.12, 9.1, "w = 1 : L = 8\n기울기 dL/dw = −8", fontsize=13, color=A, weight="bold")
    ax.scatter([1.8], [2.88], s=110, color=T, zorder=5)
    ax.annotate("", xy=(1.78, 2.95), xytext=(1.03, 7.8),
                arrowprops=dict(arrowstyle="-|>", color=D, lw=1.8, mutation_scale=16))
    ax.text(1.9, 3.4, "w = 1.8 : L = 2.88\n(예측 ŷ = 3.6)", fontsize=13, color=T, weight="bold")
    ax.text(0.95, 5.0, "w ← w − 0.1×(−8)", fontsize=12.5, color=D, ha="right")
    ax.scatter([3], [0], s=70, color=G, zorder=5)
    ax.text(3, 0.7, "최솟값 w = 3\n(ŷ = 6 = 정답)", fontsize=12, color=G, ha="center")
    return _save(fig, "derivative.png")


# ------------------------------------------------------------------ 9. CE 곡선
def ce_curve():
    fig, ax = plt.subplots(figsize=(9, 5.8))
    p = np.linspace(0.005, 1, 400)
    ax.plot(p, -np.log(p), color=T, lw=3)
    for pp, dx, dy in ((0.9, -0.02, 0.45), (0.5, 0.02, 0.45), (0.1, 0.03, 0.35), (0.01, 0.03, 0.1)):
        v = -np.log(pp)
        ax.scatter([pp], [v], s=90, color=A, zorder=5)
        ax.text(pp + dx, v + dy, f"p={pp} → {v:.2f}", fontsize=13, color=D, weight="bold",
                ha="right" if pp == 0.9 else "left")
    ax.set_xlabel("정답 클래스에 준 확률  p(정답)", fontsize=13)
    ax.set_ylabel("손실  −log p(정답)", fontsize=13)
    ax.set_ylim(0, 5.4)
    ax.text(0.55, 3.6, "확신한 오답일수록\n손실이 급격히 커진다", fontsize=14, color=A, weight="bold")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return _save(fig, "ce_curve.png")


# ------------------------------------------------------------------ 10. 경사하강 경로
def gd_paths():
    fig, axs = plt.subplots(1, 4, figsize=(16, 4.9), sharey=True)
    w = np.linspace(-9, 17, 300)
    cases = [(0.2, "η = 0.2 : 천천히 수렴"), (0.5, "η = 0.5 : 한 번에 도착"), (1.0, "η = 1.0 : 진동"),
             (1.1, "η = 1.1 : 발산")]
    for ax, (eta, tt) in zip(axs, cases):
        ax.plot(w, (w - 3) ** 2, color=T, lw=2.5)
        ws = [-2.0]
        for _ in range(5):
            ws.append(ws[-1] - eta * 2 * (ws[-1] - 3))
        ls = [(x - 3) ** 2 for x in ws]
        for i in range(len(ws) - 1):
            ax.annotate("", xy=(ws[i + 1], ls[i + 1]), xytext=(ws[i], ls[i]),
                        arrowprops=dict(arrowstyle="-|>", color=A, lw=1.6, alpha=0.85, mutation_scale=13))
        ax.scatter(ws, ls, color=A, s=45, zorder=5)
        ax.text(ws[0], ls[0] + 14, "시작 −2", fontsize=13, color=D, ha="center")
        ax.set_title(tt, fontsize=15, color=A if eta >= 1 else T, weight="bold")
        seq = ", ".join(f"{x:g}" for x in [round(v, 2) for v in ws[:4]])
        ax.text(0.5, 0.97, f"w: {seq}…", transform=ax.transAxes, ha="center", va="top", fontsize=14,
                color=D, weight="bold")
        ax.set_ylim(-5, 230)
        ax.set_xlim(-9, 17)
        ax.set_xlabel("w", fontsize=12)
        ax.tick_params(labelsize=10)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axs[0].set_ylabel("L(w) = (w − 3)$^2$", fontsize=12)
    fig.tight_layout()
    return _save(fig, "gd_paths.png")


# ------------------------------------------------------------------ 11. 일반화
def generalization():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 5.2), gridspec_kw=dict(width_ratios=[0.8, 1.2]))
    # split bar
    parts = [("훈련 train", 70, T, "파라미터 학습"), ("검증 val", 15, T2, "설정 선택"),
             ("테스트 test", 15, A, "최종 평가 1회")]
    y = 0
    for name, v, col, role in parts:
        a1.bar(0, v, bottom=y, color=col, width=0.55, edgecolor="white", linewidth=2)
        a1.text(0.36, y + v / 2, f"{name}\n{role}", va="center", fontsize=12.5, color=D)
        y += v
    a1.set_xlim(-0.4, 1.5)
    a1.set_ylim(0, 100)
    a1.axis("off")
    a1.set_title("데이터 나누기 (예: 70/15/15)", fontsize=13.5, color=D)
    # curves
    e = np.linspace(1, 30, 100)
    tr = 2.2 * np.exp(-e / 7) + 0.15
    va = 2.2 * np.exp(-e / 7) + 0.35 + 0.0022 * (e - 10) ** 2 * (e > 10)
    a2.plot(e, tr, color=T, lw=3)
    a2.plot(e, va, color=A, lw=3)
    a2.text(29, tr[-1] + 0.1, "훈련 손실", color=T, fontsize=13, weight="bold", ha="right")
    a2.text(29, va[-1] + 0.1, "검증 손실", color=A, fontsize=13, weight="bold", ha="right")
    i = int(np.argmin(va))
    a2.axvline(e[i], color=G, ls="--", lw=1.2)
    a2.text(e[i] + 0.4, 2.0, "검증 손실이 다시 오르면\n외운 패턴이 밖에서 안 통함", fontsize=12, color=G)
    a2.set_xlabel("학습 epoch", fontsize=12)
    a2.set_ylabel("손실", fontsize=12)
    a2.set_title("설명용 곡선 (실제 실험 결과 아님)", fontsize=12.5, color=G)
    a2.set_ylim(0, 2.6)
    for s in ("top", "right"):
        a2.spines[s].set_visible(False)
    fig.tight_layout()
    return _save(fig, "generalization.png")


def make_all():
    return [f() for f in (tensor_ranks, batch_axis, broadcasting, matmul_shape, batched_matmul, dot_scores,
                          softmax_temp, derivative, ce_curve, gd_paths, generalization)]


if __name__ == "__main__":
    for p in make_all():
        print(p)
