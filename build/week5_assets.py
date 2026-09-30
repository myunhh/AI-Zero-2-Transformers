"""Week 5 figures -> build/assets/week5/*.png (run: python build/week5_assets.py)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from deckkit import PALETTE_HEX as P, mpl_setup  # noqa: E402

import numpy as np  # noqa: E402

plt = mpl_setup()
from matplotlib import font_manager  # noqa: E402
font_manager.fontManager.addfont("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf")
plt.rcParams["font.family"] = ["NanumGothic", "DejaVu Sans"]
plt.rcParams["mathtext.fontset"] = "dejavusans"
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

OUT = os.path.join(HERE, "assets", "week5")
os.makedirs(OUT, exist_ok=True)
TEAL, TEAL2, MINT, DARK, GRAY, ACC, LINE = (P[k] for k in ("TEAL", "TEAL2", "MINT", "DARK", "GRAY", "ACCENT", "LINE"))
MINT2 = "#CFE8EE"
ACC_BG = "#FDF1E8"
CMAP = LinearSegmentedColormap.from_list("tealmap", ["#FFFFFF", "#CFE8EE", "#3FA7B8", "#0F6C8C"])


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)


def rbox(ax, x, y, w, h, text="", fc=MINT, ec=None, fs=12, color=DARK, bold=False, lw=1.2, r=0.08):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec or fc, lw=lw))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
                fontweight="bold" if bold else "normal")


def arr(ax, x1, y1, x2, y2, color=TEAL2, lw=2.0, ms=14, style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, shrinkA=0, shrinkB=0))


def softmax(x):
    e = np.exp(x - x.max(-1, keepdims=True))
    return e / e.sum(-1, keepdims=True)


def mat(ax, M, rows, cols, title=None, fmt="{:.2f}", cmap=CMAP, vmin=None, vmax=None,
        hl_row=None, mask=None, fs=13, title_color=DARK):
    M = np.asarray(M, float)
    show = np.where(np.isfinite(M), M, np.nan)
    ax.imshow(show, cmap=cmap, vmin=vmin if vmin is not None else np.nanmin(show),
              vmax=vmax if vmax is not None else np.nanmax(show), aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            if mask is not None and mask[i, j]:
                ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fc="#EEEEEE", ec="white", lw=1))
                txt = "−∞" if not np.isfinite(v) else fmt.format(v)
                ax.text(j, i, txt, ha="center", va="center", fontsize=fs, color=GRAY)
                continue
            norm = (v - np.nanmin(show)) / (np.nanmax(show) - np.nanmin(show) + 1e-9)
            ax.text(j, i, fmt.format(v).replace("-", "−"), ha="center", va="center", fontsize=fs,
                    color="white" if norm > 0.62 else DARK, fontweight="bold")
    ax.set_xticks(range(len(cols)), cols, fontsize=12)
    ax.set_yticks(range(len(rows)), rows, fontsize=12)
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    if hl_row is not None:
        ax.add_patch(plt.Rectangle((-.5, hl_row - .5), M.shape[1], 1, fill=False, ec=ACC, lw=3))
    if title:
        ax.set_title(title, fontsize=15, color=title_color, fontweight="bold", pad=10)


# ------------------------------------------------------------------ numbers
Q = np.array([[1, 0], [0, 1], [1, 1], [-1, .5]], float)
K = np.array([[1, 0], [0, 1], [1, 1], [-1, 1]], float)
V = np.array([[1, 0], [0, 1], [2, 2], [-1, 1]], float)
TOK = ["A", "B", "C", "D"]
S = Q @ K.T
SS = S / np.sqrt(2)
A = softmax(SS)
O = A @ V


# 1. bottleneck vs attention -------------------------------------------------
def fig_bottleneck():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    for ax in axes:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6.2)
        ax.axis("off")
    src = ["나는", "학교에", "간다", "<eos>"]
    # (a) fixed vector
    ax = axes[0]
    ax.set_title("(a) Seq2Seq: 고정 문맥 벡터 c 하나", fontsize=16, color=DARK, fontweight="bold")
    for j, w in enumerate(src):
        x = 0.4 + j * 1.35
        rbox(ax, x, 0.4, 1.15, 0.6, w, fc="white", ec=LINE, fs=12)
        rbox(ax, x, 1.5, 1.15, 0.8, f"$h_{j+1}$", fc=MINT2, fs=14, bold=True, color=TEAL)
        arr(ax, x + .575, 1.0, x + .575, 1.5, lw=1.5, ms=10)
        if j:
            arr(ax, x - .2, 1.9, x, 1.9, lw=1.5, ms=10)
    rbox(ax, 2.9, 3.2, 1.3, 0.9, "c", fc=ACC, fs=20, bold=True, color="white")
    arr(ax, 4.9, 2.3, 4.2, 3.3, color=ACC, lw=2.5)
    for t, w in enumerate(["I", "go", "to", "school"]):
        x = 5.8 + t * 1.05
        rbox(ax, x, 4.6, 0.9, 0.8, f"$s_{t+1}$", fc=MINT2, fs=14, bold=True, color=TEAL)
        ax.text(x + .45, 5.75, w, ha="center", fontsize=12, color=DARK)
        arr(ax, 4.2, 3.65, x + .1, 4.6, color=ACC, lw=1.4, ms=10)
    ax.text(0.4, 3.6, "입력 전체를\n벡터 하나로 요약", fontsize=13, color=GRAY)
    # (b) attention
    ax = axes[1]
    ax.set_title("(b) Attention: 출력 시점마다 다른 가중합 $c_t$", fontsize=16, color=DARK, fontweight="bold")
    wts = [0.05, 0.15, 0.75, 0.05]
    for j, w in enumerate(src):
        x = 0.4 + j * 1.35
        rbox(ax, x, 0.4, 1.15, 0.6, w, fc="white", ec=LINE, fs=12)
        rbox(ax, x, 1.5, 1.15, 0.8, f"$h_{j+1}$", fc=MINT2, fs=14, bold=True, color=TEAL)
        arr(ax, x + .575, 1.0, x + .575, 1.5, lw=1.5, ms=10)
        ax.plot([x + .575, 6.6], [2.3, 3.55], color=ACC, lw=1 + 9 * wts[j], alpha=.85, solid_capstyle="round")
        ax.text(x + .575, 2.62, f"α={wts[j]:.2f}", ha="center", fontsize=11, color=ACC, fontweight="bold",
                bbox=dict(fc="white", ec="none", pad=1.5))
    rbox(ax, 6.1, 3.55, 1.0, 0.8, "$c_3$", fc=ACC, fs=18, bold=True, color="white")
    rbox(ax, 7.8, 3.55, 1.0, 0.8, "$s_3$", fc=MINT2, fs=14, bold=True, color=TEAL)
    arr(ax, 7.1, 3.95, 7.8, 3.95, color=ACC, lw=2)
    ax.text(8.3, 4.7, "“school”\n생성 시점", ha="center", fontsize=12, color=DARK)
    ax.text(6.0, 1.1, "위치별 표현 $h_1…h_S$를\n버리지 않고 보관", fontsize=13, color=GRAY)
    ax.text(0.4, 5.6, "가중치는 설명용 예시(학습 결과 아님)", fontsize=11, color=GRAY)
    fig.tight_layout()
    save(fig, "bottleneck.png")


# 2. alignment heatmap -------------------------------------------------------
def fig_alignment():
    src = ["The", "cat", "sat", "on", "the", "mat", "<eos>"]
    tgt = ["고양이가", "매트", "위에", "앉았다", "<eos>"]
    W = np.array([
        [.10, .78, .04, .02, .02, .02, .02],
        [.02, .03, .03, .07, .15, .68, .02],
        [.02, .02, .08, .74, .08, .04, .02],
        [.03, .06, .80, .05, .02, .02, .02],
        [.02, .02, .03, .02, .02, .04, .85],
    ])
    W = W / W.sum(1, keepdims=True)
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    mat(ax, W, tgt, src, fmt="{:.2f}", fs=11, vmin=0, vmax=1)
    ax.xaxis.tick_top()
    ax.set_xlabel("Source (Encoder 위치 j)", fontsize=13)
    ax.xaxis.set_label_position("top")
    ax.set_ylabel("Target (Decoder 시점 t)", fontsize=13)
    ax.text(3, 5.05, "설명용 가상 정렬 — 어순이 달라도 필요한 위치를 다시 찾는다", ha="center",
            fontsize=11, color=GRAY)
    fig.tight_layout()
    save(fig, "alignment.png")


# 3. transformer architecture (top -> bottom) --------------------------------
def fig_arch():
    fig, ax = plt.subplots(figsize=(11, 8.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.4)
    ax.axis("off")

    def col(x, head, emb, layers, out, out_shape):
        rbox(ax, x, 7.5, 4.4, 0.7, head, fc=TEAL, fs=14, bold=True, color="white")
        rbox(ax, x, 6.45, 4.4, 0.75, emb, fc="white", ec=LINE, fs=12)
        arr(ax, x + 2.2, 6.45, x + 2.2, 6.1, ms=10)
        ax.add_patch(FancyBboxPatch((x, 6.05 - 1.05 * len(layers) - .25), 4.4, 1.05 * len(layers) + .25,
                                    boxstyle="round,pad=0,rounding_size=0.1", fc="#F4FAFB", ec=TEAL2,
                                    lw=1.8, ls="--"))
        ax.text(x + 4.3, 6.05 - 1.05 * len(layers) - .2, "× 6 층", ha="right", va="bottom", fontsize=13,
                color=TEAL, fontweight="bold")
        y = 6.05
        for i, (t, fc) in enumerate(layers):
            y -= 1.05
            rbox(ax, x + .2, y + .12, 3.4, 0.8, t, fc=fc, fs=12, bold=True, color=DARK)
            if i < len(layers) - 1:
                arr(ax, x + 1.9, y + .12, x + 1.9, y - .1, ms=10)
        yb = 6.05 - 1.05 * len(layers) - .25
        arr(ax, x + 2.2, yb, x + 2.2, yb - .4, ms=10)
        rbox(ax, x, yb - 1.15, 4.4, 0.75, f"{out}\n{out_shape}", fc=ACC_BG if "logits" in out else MINT2,
             fs=12, bold=True, color=ACC if "logits" in out else TEAL)
        return yb

    col(0.2, "ENCODER · Source", "Token Embedding + PE\n(B,S) → (B,S,d)",
        [("Self-attention\n+ residual · LayerNorm", MINT2), ("Feed-forward\n+ residual · LayerNorm", MINT)],
        "Encoder memory E", "(B,S,d)")
    col(6.4, "DECODER · Shifted target", "Token Embedding + PE\n(B,T) → (B,T,d)",
        [("Masked self-attention\n+ residual · LayerNorm", MINT2),
         ("Cross-attention ← E\n+ residual · LayerNorm", ACC_BG),
         ("Feed-forward\n+ residual · LayerNorm", MINT)],
        "Linear → vocabulary logits", "(B,T,d) → (B,T,|V|)")
    # E -> cross attention
    arr(ax, 4.6, 2.95, 6.6, 4.45, color=ACC, lw=2.5, ms=16)
    ax.text(5.5, 2.2, "K, V ← E\nQ ← Decoder", fontsize=12, color=ACC, fontweight="bold", ha="center")
    ax.set_ylim(0.8, 8.4)
    ax.text(0.2, 0.95, "위→아래로 읽기 · 층마다 파라미터는 별개 · 최종 E가 모든 Decoder 층의 cross-attention으로 전달",
            fontsize=11.5, color=GRAY)
    save(fig, "transformer_arch.png")


# 4. sinusoidal PE -------------------------------------------------------------
def pe_table(n, d):
    pos = np.arange(n)[:, None]
    i = np.arange(d // 2)[None, :]
    ang = pos / (10000 ** (2 * i / d))
    pe = np.zeros((n, d))
    pe[:, 0::2] = np.sin(ang)
    pe[:, 1::2] = np.cos(ang)
    return pe


def fig_pe():
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8), gridspec_kw=dict(width_ratios=[1.05, 1]))
    ax = axes[0]
    pe = pe_table(50, 64)
    im = ax.imshow(pe, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    ax.set_xlabel("차원 인덱스 (짝수=sin, 홀수=cos)", fontsize=12)
    ax.set_ylabel("위치 pos", fontsize=12)
    ax.set_title("PE 행렬 (d=64, pos 0–49)", fontsize=14, fontweight="bold", color=DARK)
    fig.colorbar(im, ax=ax, fraction=.04)
    ax = axes[1]
    d = 32
    pos = np.linspace(0, 40, 400)
    cols = [TEAL, ACC, GRAY]
    for c, i in zip(cols, (1, 3, 6)):
        f = 1 / (10000 ** (2 * i / d))
        ax.plot(pos, np.sin(pos * f), color=c, lw=2.4, label=f"i={i} sin")
        ax.plot(pos, np.cos(pos * f), color=c, lw=2.0, ls="--", label=f"i={i} cos")
    ax.set_xlabel("위치 pos", fontsize=12)
    ax.set_title("d=32: 차원쌍 i가 커질수록 느리게 변한다", fontsize=14, fontweight="bold", color=DARK)
    ax.legend(ncol=3, fontsize=10, loc="lower left", frameon=False)
    ax.set_ylim(-1.55, 1.15)
    ax.grid(alpha=.25)
    fig.tight_layout()
    save(fig, "pe.png")


# 5. Q/K/V projection ------------------------------------------------------------
def fig_qkv():
    fig, ax = plt.subplots(figsize=(10, 4.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0.85, 5.8)
    ax.axis("off")
    rbox(ax, 0.2, 1.6, 1.6, 2.6, "X\n(N, d)", fc=MINT2, fs=16, bold=True, color=TEAL)
    ax.text(1.0, 1.25, "같은 입력 표현", ha="center", fontsize=12, color=GRAY)
    names = [("W_Q", "Q", "비교의 기준", TEAL), ("W_K", "K", "비교 대상", TEAL2), ("W_V", "V", "전달할 내용", ACC)]
    for k, (w, q, desc, c) in enumerate(names):
        y = 4.3 - k * 1.65
        arr(ax, 1.8, 2.9, 3.2, y + .45, ms=12)
        rbox(ax, 3.2, y, 1.9, 0.9, "", fc="white", ec=c, lw=2)
        ax.text(4.15, y + .45, f"$W_{q}$  (d, $d_h$)", ha="center", va="center", fontsize=14, color=c,
                fontweight="bold")
        arr(ax, 5.1, y + .45, 6.2, y + .45, color=c, ms=12)
        rbox(ax, 6.2, y, 1.5, 0.9, "", fc=c, fs=15)
        ax.text(6.95, y + .45, f"{q}  (N, $d_h$)", ha="center", va="center", fontsize=14, color="white",
                fontweight="bold")
        ax.text(7.9, y + .45, desc, va="center", fontsize=14, color=DARK)
    ax.text(3.2, 5.45, "학습되는 파라미터", fontsize=12, color=GRAY, fontweight="bold")
    ax.text(6.2, 5.45, "입력마다 계산되는 활성값", fontsize=12, color=GRAY, fontweight="bold")
    save(fig, "qkv_proj.png")


# 6. 4-token setup ---------------------------------------------------------------
def fig_setup():
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 5.6))
    for ax, M, name, c in zip(axes, (Q, K, V), ("Q (Query)", "K (Key)", "V (Value)"), (TEAL, TEAL2, ACC)):
        mat(ax, M, TOK, ["$f_1$", "$f_2$"], title=name, fmt="{:g}", fs=15, title_color=c,
            hl_row=0 if name.startswith("Q") else None)
    fig.suptitle("4 tokens × 2 features — 숫자는 설명용(학습 결과 아님)", fontsize=12, color=GRAY, y=0.01)
    fig.tight_layout()
    save(fig, "attn_setup.png")


# 7. pipeline S/√2 -> A -> O -------------------------------------------------------
def fig_pipeline():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.8), gridspec_kw=dict(width_ratios=[4, 4, 2.2]))
    mat(axes[0], SS, [f"q_{t}" for t in TOK], [f"k_{t}" for t in TOK], title=r"① 점수 $QK^\top/\sqrt{2}$", fs=14, hl_row=0)
    mat(axes[1], A, [f"q_{t}" for t in TOK], [f"k_{t}" for t in TOK], title="② A = 행별 softmax (합=1)",
        fs=14, vmin=0, vmax=0.6, hl_row=0)
    mat(axes[2], O, [f"o_{t}" for t in TOK], ["$f_1$", "$f_2$"], title="③ O = A V", fs=14, hl_row=0)
    for ax in axes[:2]:
        ax.set_xlabel("Key 축 (softmax 방향 →)", fontsize=12)
    fig.tight_layout(w_pad=3)
    save(fig, "attn_pipeline.png")


# 8. causal mask ---------------------------------------------------------------------
def fig_causal():
    fut = np.triu(np.ones((4, 4), bool), 1)
    Sm = np.where(fut, -np.inf, SS)
    Ac = softmax(np.where(fut, -1e9, SS))
    Az = softmax(np.where(fut, 0.0, SS))
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.8))
    rows = [f"q_{t}" for t in TOK]
    colsn = [f"k_{t}" for t in TOK]
    mat(axes[0], Sm, rows, colsn, title="① 미래 Key를 −∞로", fs=14, mask=fut)
    mat(axes[1], Ac, rows, colsn, title="② softmax → 미래 가중치 정확히 0", fs=14, vmin=0, vmax=1, mask=fut)
    mat(axes[2], Az, rows, colsn, title="✗ 0으로만 바꾸면: exp(0)=1", fs=14, vmin=0, vmax=1,
        title_color=ACC)
    for i in range(4):
        for j in range(4):
            if fut[i, j]:
                axes[2].add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fill=False, ec=ACC, lw=2.5))
    fig.tight_layout(w_pad=3)
    save(fig, "causal.png")


# 9. why sqrt(d_h) ----------------------------------------------------------------------
def fig_sqrt():
    rng = np.random.default_rng(0)
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    rng2 = np.random.default_rng(0)
    ax = axes[0]
    dhs = [4, 16, 64, 256]
    raw, sc = [], []
    for dh in dhs:
        q = rng.standard_normal((20000, dh))
        k = rng.standard_normal((20000, dh))
        s = (q * k).sum(1)
        raw.append(s.std())
        sc.append((s / np.sqrt(dh)).std())
    x = np.arange(len(dhs))
    ax.bar(x - .2, raw, .38, color=ACC, label="q·k (스케일 없음)")
    ax.bar(x + .2, sc, .38, color=TEAL, label=r"q·k / $\sqrt{d_h}$")
    for xi, r, s_ in zip(x, raw, sc):
        ax.text(xi - .2, r + .3, f"{r:.1f}", ha="center", fontsize=11, color=ACC)
        ax.text(xi + .2, s_ + .3, f"{s_:.1f}", ha="center", fontsize=11, color=TEAL)
    ax.set_xticks(x, [f"$d_h$={d}" for d in dhs], fontsize=12)
    ax.set_ylabel("점수의 표준편차", fontsize=12)
    ax.set_title(r"성분 평균 0·분산 1 가정: 표준편차 ≈ $\sqrt{d_h}$", fontsize=14, fontweight="bold", color=DARK)
    ax.legend(frameon=False, fontsize=11)
    ax.grid(axis="y", alpha=.25)
    ax = axes[1]
    dh = 64
    q = rng2.standard_normal(dh)
    k = rng2.standard_normal((8, dh))
    s = k @ q
    a_raw = softmax(s)
    a_sc = softmax(s / np.sqrt(dh))
    order = np.argsort(-a_sc)
    xx = np.arange(8)
    ax.bar(xx - .2, a_raw[order], .38, color=ACC, label="softmax(q·k)")
    ax.bar(xx + .2, a_sc[order], .38, color=TEAL, label=r"softmax(q·k/$\sqrt{d_h}$)")
    ax.set_xticks(xx, [f"k{j+1}" for j in range(8)], fontsize=11)
    ax.set_ylim(0, 1.05)
    ax.set_title("$d_h$=64, Key 8개: 스케일이 없으면 한 곳에 몰림", fontsize=14, fontweight="bold", color=DARK)
    ax.legend(frameon=False, fontsize=11)
    ax.grid(axis="y", alpha=.25)
    fig.tight_layout()
    save(fig, "sqrt_scale.png")
    return a_raw.max(), a_sc.max()


# 10. multi-head shapes --------------------------------------------------------------
def fig_mha():
    fig, ax = plt.subplots(figsize=(14, 4.6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    steps = [
        ("X", "(B,N,d)\n(2,5,8)", MINT2, TEAL),
        ("선형 투영\nQ·K·V", "(B,N,d)\n(2,5,8)", "white", TEAL),
        ("view\nHead 분리", "(B,N,H,dₕ)\n(2,5,2,4)", MINT2, TEAL),
        ("transpose(1,2)", "(B,H,N,dₕ)\n(2,2,5,4)", MINT2, TEAL),
        ("Head별\nAttention", "A: (2,2,5,5)\nO: (2,2,5,4)", ACC_BG, ACC),
        ("transpose\n+ reshape", "(B,N,d)\n(2,5,8)", MINT2, TEAL),
        ("W_O", "(B,N,d)\n(2,5,8)", "white", TEAL),
    ]
    bw, gap = 1.62, 0.33
    for i, (h, shp, fc, c) in enumerate(steps):
        x = 0.1 + i * (bw + gap)
        rbox(ax, x, 2.3, bw, 1.25, h, fc=fc, ec=c, fs=12.5, bold=True, color=c)
        ax.text(x + bw / 2, 1.75, shp, ha="center", va="center", fontsize=12, color=DARK, family="DejaVu Sans Mono")
        if i < len(steps) - 1:
            arr(ax, x + bw + .03, 2.92, x + bw + gap - .03, 2.92, ms=11)
    # head split illustration
    ax.text(7.0, 4.25, "d=8 특징을 H=2개의 부분공간(각 $d_h$=4)으로 — 토큰(N=5)은 나누지 않는다", ha="center",
            fontsize=13, color=DARK, fontweight="bold")
    for h in range(2):
        for t in range(5):
            for f in range(4):
                x0 = 3.0 + h * 4.6 + f * 0.33
                ax.add_patch(plt.Rectangle((x0, 0.15 + (4 - t) * 0.2 - 0.05), 0.3, 0.17,
                                           fc=TEAL if h == 0 else ACC, alpha=.35 + .12 * f, ec="white"))
        ax.text(3.0 + h * 4.6 + 1.5, 0.55, f"head {h+1}: 5 토큰 × 4 특징", va="center", fontsize=12,
                color=TEAL if h == 0 else ACC, fontweight="bold")
    save(fig, "mha_shapes.png")


# 11. heads' patterns (random init, illustrative) ----------------------------------------
def fig_heads():
    rng = np.random.default_rng(3)
    N, d, H = 5, 8, 2
    dh = d // H
    X = rng.standard_normal((N, d))
    Wq = rng.standard_normal((d, d)) * .8
    Wk = rng.standard_normal((d, d)) * .8
    toks = ["t1", "t2", "t3", "t4", "t5"]
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 5.0))
    for h in range(H):
        q = (X @ Wq)[:, h * dh:(h + 1) * dh]
        k = (X @ Wk)[:, h * dh:(h + 1) * dh]
        Ah = softmax(q @ k.T / np.sqrt(dh))
        mat(axes[h], Ah, toks, toks, title=f"head {h+1}  (N×N = 5×5)", fs=15, vmin=0, vmax=1)
        axes[h].tick_params(labelsize=14)
    fig.suptitle("같은 X, 다른 투영 → 다른 참조 패턴 (무작위 가중치 예시: 역할 지정 아님)", fontsize=13,
                 color=GRAY, y=-0.02)
    fig.tight_layout()
    save(fig, "heads.png")


if __name__ == "__main__":
    fig_bottleneck()
    fig_alignment()
    fig_arch()
    fig_pe()
    fig_qkv()
    fig_setup()
    fig_pipeline()
    fig_causal()
    print("sqrt max weights raw/scaled:", fig_sqrt())
    fig_mha()
    fig_heads()
    print(sorted(os.listdir(OUT)))
