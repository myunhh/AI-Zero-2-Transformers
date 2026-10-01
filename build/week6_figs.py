"""Week 6 그림 생성: python build/week6_figs.py -> build/assets/week6/*.png"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from deckkit import mpl_setup, PALETTE_HEX as P  # noqa: E402

import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch  # noqa: E402

plt = mpl_setup()
from matplotlib import font_manager as _fm  # noqa: E402
for _f in ("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",):
    if os.path.exists(_f):
        _fm.fontManager.addfont(_f)
_fm.fontManager._findfont_cached.cache_clear()
OUT = os.path.join(HERE, "assets", "week6")
os.makedirs(OUT, exist_ok=True)
TEAL, TEAL2, MINT, DARK, GRAY, ACC, LINE = (P[k] for k in ("TEAL", "TEAL2", "MINT", "DARK", "GRAY", "ACCENT", "LINE"))
MINT2 = "#CFE8EE"
ACC_BG = "#FDF1E8"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)


def blk(ax, x, y, w, h, text, fc=MINT, ec=TEAL, tc=DARK, fs=11, bold=False, lw=1.4, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=lw, ls=ls))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal")


def arr(ax, x1, y1, x2, y2, c=GRAY, lw=1.6, style="-|>", rad=0.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=12,
                                 color=c, lw=lw, connectionstyle=f"arc3,rad={rad}"))


# ------------------------------------------------------------------ 1. LayerNorm 축
def fig_ln_axis():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6))
    for k, ax in enumerate(axes):
        B, N, d = 3, 4, 6
        ax.set_xlim(-0.6, d + 2.2)
        ax.set_ylim(-1.2, N + 0.9 + 0.35 * (B - 1))
        ax.axis("off")
        for b in reversed(range(B)):
            ox, oy = 0.35 * b, 0.35 * b
            for i in range(N):
                for j in range(d):
                    hl = (k == 0 and b == 0 and i == 1) or (k == 1 and j == 2 and i == 1)
                    fc = ACC if hl else (MINT if b else "white")
                    ax.add_patch(Rectangle((j + ox, N - 1 - i + oy), 1, 1, fc=fc, ec=LINE if b else TEAL,
                                           lw=0.8, alpha=1 if (b == 0 or hl) else 0.9))
        ax.text(d / 2, -0.55, "특징 축 d →", ha="center", fontsize=11, color=DARK)
        ax.text(-0.35, N / 2, "토큰 N", rotation=90, ha="center", va="center", fontsize=11, color=DARK)
        ax.text(d + 0.95, N + 0.35, "배치 B\n(겹친 장)", ha="center", fontsize=10, color=GRAY)
        title = "LayerNorm(d): 토큰 하나의 d개 특징" if k == 0 else "BatchNorm: 배치 B를 가로지르는 한 특징"
        ax.set_title(title, fontsize=12, color=ACC if k == 0 else GRAY, fontweight="bold")
    fig.tight_layout()
    save(fig, "ln_axis.png")


# ------------------------------------------------------------------ 2. Post-LN vs Pre-LN
def fig_postpre():
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 5.2))
    for k, ax in enumerate(axes):
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 7.2)
        ax.axis("off")
        cx = 2.0
        ax.text(cx, 6.95, "Post-LN (2017 원형)" if k == 0 else "Pre-LN (후속 변형)", ha="center",
                fontsize=14, fontweight="bold", color=TEAL if k == 0 else ACC)
        ax.text(cx, 0.15, "x", ha="center", fontsize=13, fontweight="bold", color=DARK)
        if k == 0:
            arr(ax, cx, 0.45, cx, 1.35)
            blk(ax, cx - 1.0, 1.4, 2.0, 0.8, "Sublayer F\n(MHA 또는 FFN)", fs=10.5)
            arr(ax, cx, 2.2, cx, 3.05)
            blk(ax, cx - 0.33, 3.1, 0.66, 0.6, "+", fc="white", fs=16, bold=True)
            arr(ax, cx, 3.7, cx, 4.35)
            blk(ax, cx - 1.0, 4.4, 2.0, 0.7, "LayerNorm", fc=ACC_BG, ec=ACC, fs=11, bold=True)
            arr(ax, cx, 5.1, cx, 5.9)
            ax.text(cx, 6.1, "y = LN(x + F(x))", ha="center", fontsize=12, family="monospace", color=DARK)
            # residual path
            ax.plot([cx, 0.4, 0.4], [0.9, 0.9, 3.4], color=TEAL2, lw=2)
            arr(ax, 0.4, 3.4, cx - 0.35, 3.4, c=TEAL2, lw=2)
            ax.text(0.25, 2.1, "잔차 경로", rotation=90, ha="center", va="center", fontsize=10, color=TEAL2)
        else:
            arr(ax, cx, 0.45, cx, 1.3)
            blk(ax, cx - 1.0, 1.35, 2.0, 0.7, "LayerNorm", fc=ACC_BG, ec=ACC, fs=11, bold=True)
            arr(ax, cx, 2.05, cx, 2.6)
            blk(ax, cx - 1.0, 2.65, 2.0, 0.8, "Sublayer F\n(MHA 또는 FFN)", fs=10.5)
            arr(ax, cx, 3.45, cx, 4.05)
            blk(ax, cx - 0.33, 4.1, 0.66, 0.6, "+", fc="white", fs=16, bold=True)
            arr(ax, cx, 4.7, cx, 5.9)
            ax.text(cx, 6.1, "y = x + F(LN(x))", ha="center", fontsize=12, family="monospace", color=DARK)
            ax.plot([cx, 0.4, 0.4], [0.9, 0.9, 4.4], color=TEAL2, lw=2)
            arr(ax, 0.4, 4.4, cx - 0.35, 4.4, c=TEAL2, lw=2)
            ax.text(0.25, 2.6, "정규화 없는 잔차 경로", rotation=90, ha="center", va="center", fontsize=10,
                    color=TEAL2)
            ax.text(3.35, 5.3, "stack 끝에\n최종 Norm을\n두는 경우가 많음", ha="center", fontsize=9, color=GRAY)
    fig.tight_layout()
    save(fig, "postpre_ln.png")


# ------------------------------------------------------------------ 3. Shift 표
def fig_shift():
    toks_in = ["BOS", "I", "am", "a", "student"]
    toks_out = ["I", "am", "a", "student", "EOS"]
    fig, ax = plt.subplots(figsize=(7.4, 3.3))
    ax.set_xlim(-1.9, 5.2)
    ax.set_ylim(-0.3, 3.3)
    ax.axis("off")
    for j in range(5):
        ax.text(j + 0.5, 3.0, f"위치 {j+1}", ha="center", fontsize=11, color=GRAY)
        blk(ax, j + 0.06, 1.75, 0.88, 0.8, toks_in[j], fc=MINT, ec=TEAL, fs=13, bold=True)
        blk(ax, j + 0.06, 0.05, 0.88, 0.8, toks_out[j], fc=ACC_BG, ec=ACC, fs=13, bold=True)
        arr(ax, j + 0.5, 1.72, j + 0.5, 0.9, c=GRAY)
    ax.text(-0.1, 2.15, "Decoder 입력", ha="right", va="center", fontsize=12, fontweight="bold", color=TEAL)
    ax.text(-0.1, 0.45, "예측 정답", ha="right", va="center", fontsize=12, fontweight="bold", color=ACC)
    for j in range(4):
        arr(ax, j + 0.5, 0.88, j + 1.45, 1.72, c=TEAL2, lw=1.2, style="-|>", rad=0.0)
    ax.text(2.5, 1.3, "", ha="center")
    ax.text(5.1, 1.3, "정답이 한 칸 뒤에\n다음 입력으로", ha="left", va="center", fontsize=9.5, color=TEAL2)
    ax.set_xlim(-1.9, 6.4)
    fig.tight_layout()
    save(fig, "shift.png")


# ------------------------------------------------------------------ 4. Causal mask heatmap
def fig_causal():
    toks = ["BOS", "I", "am", "a", "student"]
    n = 5
    fig, ax = plt.subplots(figsize=(5.0, 4.2))
    for i in range(n):
        for j in range(n):
            allowed = j <= i
            row = i == 1
            fc = (ACC if row else TEAL) if allowed else "white"
            ax.add_patch(Rectangle((j, n - 1 - i), 1, 1, fc=fc, ec=LINE, lw=1,
                                   hatch=None if allowed else "///", alpha=0.95 if allowed else 1))
            if not allowed:
                ax.text(j + 0.5, n - 1 - i + 0.5, "-∞", ha="center", va="center", fontsize=11,
                        color=GRAY)
            else:
                ax.text(j + 0.5, n - 1 - i + 0.5, "0", ha="center", va="center", fontsize=11,
                        color="white", fontweight="bold")
    ax.add_patch(Rectangle((0, n - 2), n, 1, fill=False, ec=ACC, lw=3))
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks(np.arange(n) + 0.5)
    ax.set_xticklabels(toks, fontsize=10.5)
    ax.xaxis.tick_top()
    ax.set_yticks(np.arange(n) + 0.5)
    ax.set_yticklabels([f"{t} → {o}" for t, o in zip(toks, ["I", "am", "a", "student", "EOS"])][::-1],
                       fontsize=10.5)
    ax.set_xlabel("Key: 참조할 Decoder 입력 위치 j", fontsize=11, color=DARK, labelpad=10)
    ax.xaxis.set_label_position("top")
    ax.set_ylabel("Query 위치 i (입력 → 예측할 정답)", fontsize=11, color=DARK)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.tight_layout()
    save(fig, "causal_mask.png")


# ------------------------------------------------------------------ 5. Encoder / Decoder layer
def fig_encdec():
    fig, ax = plt.subplots(figsize=(7.6, 6.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10.6)
    ax.axis("off")
    # encoder
    ax.add_patch(FancyBboxPatch((0.3, 2.2), 4.0, 4.6, boxstyle="round,pad=0.05,rounding_size=0.2",
                                fc="#F6FAFB", ec=TEAL, lw=1.6, ls="--"))
    ax.text(0.52, 4.5, "Encoder 층 × L", fontsize=12, fontweight="bold", color=TEAL, rotation=90, ha="center", va="center")
    blk(ax, 0.8, 2.6, 3.0, 0.85, "Self-Attention (MHA)\nQ,K,V ← X · padding mask", fs=9.5)
    blk(ax, 0.8, 3.6, 3.0, 0.5, "Add & LayerNorm", fc=ACC_BG, ec=ACC, fs=10)
    blk(ax, 0.8, 4.45, 3.0, 0.75, "FFN (위치별)", fs=10.5)
    blk(ax, 0.8, 5.35, 3.0, 0.5, "Add & LayerNorm", fc=ACC_BG, ec=ACC, fs=10)
    for y1, y2 in [(3.45, 3.6), (4.1, 4.45), (5.2, 5.35)]:
        arr(ax, 2.3, y1, 2.3, y2, lw=1.2)
    blk(ax, 0.8, 1.0, 3.0, 0.75, "Source Embedding + PE\n(B,S) → (B,S,d)", fc="white", ec=GRAY, fs=9.5)
    arr(ax, 2.3, 1.75, 2.3, 2.6)
    blk(ax, 0.8, 7.4, 3.0, 0.7, "E = 최종 출력 (B,S,d)", fc=MINT2, ec=TEAL, fs=10.5, bold=True)
    arr(ax, 2.3, 5.85, 2.3, 7.4)
    # decoder
    ax.add_patch(FancyBboxPatch((5.4, 2.2), 4.3, 6.0, boxstyle="round,pad=0.05,rounding_size=0.2",
                                fc="#F6FAFB", ec=TEAL, lw=1.6, ls="--"))
    ax.text(5.63, 5.2, "Decoder 층 × L", fontsize=12, fontweight="bold", color=TEAL, rotation=90, ha="center", va="center")
    blk(ax, 5.9, 2.6, 3.3, 0.85, "Masked Self-Attention\ncausal + target padding", fs=9.5)
    blk(ax, 5.9, 3.6, 3.3, 0.45, "Add & LayerNorm", fc=ACC_BG, ec=ACC, fs=10)
    blk(ax, 5.9, 4.3, 3.3, 0.85, "Cross-Attention\nQ = Decoder, K,V = E", fs=9.5)
    blk(ax, 5.9, 5.3, 3.3, 0.45, "Add & LayerNorm", fc=ACC_BG, ec=ACC, fs=10)
    blk(ax, 5.9, 5.95, 3.3, 0.7, "FFN (위치별)", fs=10.5)
    blk(ax, 5.9, 6.85, 3.3, 0.45, "Add & LayerNorm", fc=ACC_BG, ec=ACC, fs=10)
    for y1, y2 in [(3.45, 3.6), (4.05, 4.3), (5.15, 5.3), (5.75, 5.95), (6.65, 6.85)]:
        arr(ax, 7.55, y1, 7.55, y2, lw=1.2)
    blk(ax, 5.9, 1.0, 3.3, 0.75, "Target Embedding + PE\nBOS로 시작하는 shifted 입력", fc="white",
        ec=GRAY, fs=9.5)
    arr(ax, 7.55, 1.75, 7.55, 2.6)
    # E -> cross attention
    ax.plot([3.8, 4.85, 4.85], [7.75, 7.75, 4.72], color=ACC, lw=2)
    arr(ax, 4.85, 4.72, 5.9, 4.72, c=ACC, lw=2)
    pass  # (회전 라벨 제거: 연결선과 겹침)
    # output head
    blk(ax, 5.9, 8.55, 3.3, 0.65, "Linear  W_vocab (d×|V|)", fc=MINT2, ec=TEAL, fs=10)
    blk(ax, 5.9, 9.55, 3.3, 0.65, "Softmax → p(y_t | y_<t, x)", fc=TEAL, ec=TEAL, tc="white", fs=10,
        bold=True)
    arr(ax, 7.55, 7.3, 7.55, 8.55)
    arr(ax, 7.55, 9.2, 7.55, 9.55)
    ax.text(9.3, 8.87, "(B,T,|V|)", fontsize=9, color=GRAY, va="center")
    ax.text(2.3, 0.35, "입력 ID (B,S)", ha="center", fontsize=10, color=GRAY)
    ax.text(7.55, 0.35, "입력 ID (B,T)", ha="center", fontsize=10, color=GRAY)
    arr(ax, 2.3, 0.6, 2.3, 1.0, lw=1.2)
    arr(ax, 7.55, 0.6, 7.55, 1.0, lw=1.2)
    save(fig, "encdec_layer.png")


# ------------------------------------------------------------------ 6. LR schedule
def fig_lr():
    s = np.arange(1, 100001)
    d, w = 512, 4000
    lr = d ** -0.5 * np.minimum(s ** -0.5, s * w ** -1.5)
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    ax.plot(s, lr * 1e4, color=P["TEAL"], lw=2.2)
    ax.axvline(w, color=LINE, lw=1, ls="--")
    pk = d ** -0.5 * w ** -0.5
    ax.plot([w], [pk * 1e4], "o", ms=8, color=ACC, mec="white", mew=2)
    ax.annotate(f"warm-up 끝 (s = 4000)\nη ≈ {pk:.1e}", (w, pk * 1e4), xytext=(14000, 6.4),
                fontsize=10.5, color=DARK, arrowprops=dict(arrowstyle="-", color=GRAY, lw=1))
    ax.text(5500, 0.5, "← warm-up: 선형 증가", ha="left", fontsize=10, color=GRAY)
    ax.text(55000, 2.35, "s^(-1/2)로 감소", ha="center", fontsize=10.5, color=GRAY)
    ax.set_xlabel("학습 step s", fontsize=11)
    ax.set_ylabel("학습률 η (×1e-4)", fontsize=11)
    ax.set_xlim(0, 100000)
    ax.set_ylim(0, 7.8)
    ax.set_xticks([4000, 25000, 50000, 75000, 100000])
    ax.set_xticklabels(["4k", "25k", "50k", "75k", "100k"])
    ax.grid(axis="y", color="#E8EEF1", lw=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_title("d = 512, w = 4000 (원형 Base 설정으로 계산)", fontsize=11, color=GRAY, loc="left")
    save(fig, "lr_schedule.png")


# ------------------------------------------------------------------ 7. KV cache prefill/decode
def fig_kv():
    fig, ax = plt.subplots(figsize=(7.8, 4.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(1.0, 7)
    ax.axis("off")
    # prefill
    ax.text(0.2, 6.6, "① Prefill: 주어진 prefix 전체를 한 번에 처리", fontsize=13, fontweight="bold", color=TEAL)
    toks = ["BOS", "I", "am"]
    for j, t in enumerate(toks):
        blk(ax, 0.3 + j * 1.1, 5.2, 1.0, 0.6, t, fc=MINT, ec=TEAL, fs=12, bold=True)
        blk(ax, 0.3 + j * 1.1, 4.3, 1.0, 0.55, "K,V", fc=MINT2, ec=TEAL, fs=11.5)
        arr(ax, 0.8 + j * 1.1, 5.2, 0.8 + j * 1.1, 4.85, lw=1.1)
    ax.text(3.7, 4.57, "→ 층마다\n   저장", fontsize=11, color=TEAL, va="center", linespacing=1.1)
    ax.text(0.3, 3.75, "TTFT(첫 토큰까지 시간)를 좌우", fontsize=11.5, color=GRAY)
    # cache store
    ax.add_patch(FancyBboxPatch((5.9, 3.9), 5.9, 1.2, boxstyle="round,pad=0.05,rounding_size=0.15",
                                fc=ACC_BG, ec=ACC, lw=1.6))
    ax.text(6.05, 4.83, "KV Cache (층 ℓ = 1..L 각각)", fontsize=11.5, color=ACC, fontweight="bold")
    for j in range(5):
        fc = MINT2 if j < 3 else ("white" if j == 4 else "#F7D9C2")
        blk(ax, 6.05 + j * 1.12, 4.0, 1.0, 0.55, ["K1,V1", "K2,V2", "K3,V3", "K4,V4", "…"][j], fc=fc,
            ec=ACC if j == 3 else TEAL, fs=11)
    # decode
    ax.text(0.2, 3.0, "② Decode: 새 토큰 하나씩 반복", fontsize=13, fontweight="bold", color=ACC)
    blk(ax, 0.3, 1.45, 1.4, 0.7, "새 토큰\n'a'", fc=ACC_BG, ec=ACC, fs=11.5, bold=True)
    arr(ax, 1.7, 1.8, 2.4, 1.8)
    blk(ax, 2.45, 1.45, 1.8, 0.7, "q4, k4, v4만\n새로 계산", fc="white", ec=ACC, fs=11)
    arr(ax, 4.25, 1.8, 5.1, 1.8)
    blk(ax, 5.15, 1.3, 3.2, 1.0, "q4 · [K1 … K4]^T\n→ softmax → V 가중합", fc=MINT, ec=TEAL, fs=11.5)
    arr(ax, 8.35, 1.8, 9.0, 1.8)
    blk(ax, 9.05, 1.45, 2.6, 0.7, "logits → 다음 토큰", fc=TEAL, ec=TEAL, tc="white", fs=11.5, bold=True)
    arr(ax, 4.0, 2.15, 9.2, 4.0, c=ACC, lw=1.4, rad=-0.15)
    ax.text(9.35, 3.45, "k4, v4 추가", fontsize=11, color=ACC, ha="left", va="center")
    arr(ax, 7.2, 3.95, 6.9, 2.35, c=TEAL, lw=1.4)
    ax.text(7.3, 2.95, "과거 K,V 재사용", fontsize=11, color=TEAL)
    save(fig, "kv_cache.png")


# ------------------------------------------------------------------ 8. KV / score memory vs N
def fig_mem():
    N = np.array([512, 1024, 2048, 4096, 8192, 16384])
    L, dh, b, H = 32, 128, 2, 32
    kv_mha = 2 * 1 * L * N * H * dh * b / 2 ** 30
    kv_gqa = 2 * 1 * L * N * 8 * dh * b / 2 ** 30
    score = 1 * H * N.astype(float) ** 2 * b / 2 ** 30
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    ax.plot(N, score, color=GRAY, lw=2, ls="--", marker="s", ms=6)
    ax.plot(N, kv_mha, color=TEAL, lw=2.2, marker="o", ms=7)
    ax.plot(N, kv_gqa, color=ACC, lw=2.2, marker="o", ms=7)
    ax.text(N[-1] * 1.08, score[-1], "score 표 1개\n(1개 층, B·H·N^2)", fontsize=9.5, va="center", color=GRAY)
    ax.text(N[-1] * 1.08, kv_mha[-1], "KV cache\nMHA H_kv=32", fontsize=9.5, va="center", color=TEAL)
    ax.text(N[-1] * 1.08, kv_gqa[-1], "KV cache\nGQA H_kv=8", fontsize=9.5, va="center", color=ACC)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    ax.set_xticks(N)
    ax.set_xticklabels([f"{n//1024}K" if n >= 1024 else str(n) for n in N])
    yt = [2 ** k for k in range(-4, 5)]
    ax.set_yticks(yt)
    ax.set_yticklabels(["1/16", "1/8", "1/4", "1/2", "1", "2", "4", "8", "16"])
    ax.set_ylim(0.05, 20)
    ax.set_xlim(400, N[-1] * 3.3)
    ax.set_xlabel("시퀀스 길이 N", fontsize=11)
    ax.set_ylabel("GiB (FP16, B=1)", fontsize=11)
    ax.grid(color="#E8EEF1", lw=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_title("L=32, d=4096, d_h=128 가정 · 이론 추정(실측 아님)", fontsize=10, color=GRAY, loc="left")
    save(fig, "kv_memory.png")


# ------------------------------------------------------------------ 9. FLOPs term shares
def fig_flops():
    d, dff = 512, 2048
    Ns = [256, 512, 1024, 2048, 4096]
    proj = np.array([4 * n * d * d for n in Ns]) / 1e9
    att = np.array([2 * n * n * d for n in Ns]) / 1e9
    ffn = np.array([2 * n * d * dff for n in Ns]) / 1e9
    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    x = np.arange(len(Ns))
    w = 0.62
    ax.bar(x, proj, w, color=TEAL, label="Q/K/V/O 투영 4Nd^2", ec="white", lw=1.5)
    ax.bar(x, ffn, w, bottom=proj, color=TEAL2, label="FFN 2Nd·d_ff", ec="white", lw=1.5)
    ax.bar(x, att, w, bottom=proj + ffn, color=ACC, label="QK^T + AV 2N^2·d", ec="white", lw=1.5)
    for i in range(len(Ns)):
        tot = proj[i] + ffn[i] + att[i]
        ax.text(i, tot + 0.4, f"{tot:.1f}", ha="center", fontsize=10, color=DARK)
    ax.set_xticks(x)
    ax.set_xticklabels([str(n) for n in Ns])
    ax.set_xlabel("길이 N (d=512, d_ff=2048)", fontsize=11)
    ax.set_ylabel("GMACs / 샘플 / 층", fontsize=11)
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    ax.grid(axis="y", color="#E8EEF1", lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, "flops_terms.png")


# ------------------------------------------------------------------ 10. 세 가지 조립 방식
def fig_archs():
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 4.6))
    specs = [
        ("Encoder-only", "BERT (2018)", [("양방향 Self-Attn", MINT), ("FFN", MINT)], "문맥 표현 → 작업별 head", TEAL,
         "mask: padding만\n목표: 가린 토큰 복원"),
        ("Decoder-only", "GPT 계열 (2018~)", [("Causal Self-Attn", MINT), ("FFN", MINT)], "다음 토큰 logits", ACC,
         "mask: causal\n목표: 다음 토큰 예측"),
        ("Encoder–Decoder", "원형(2017), T5 (2019)", [("Causal Self-Attn", MINT), ("Cross-Attn", ACC_BG),
                                                      ("FFN", MINT)], "조건부 출력 logits", TEAL,
         "mask: causal + padding\n목표: 조건부 생성"),
    ]
    for ax, (name, ex, layers, out, col, desc) in zip(axes, specs):
        ax.set_xlim(0, 4.2)
        ax.set_ylim(0, 6.5)
        ax.axis("off")
        ax.text(2, 6.2, name, ha="center", fontsize=14, fontweight="bold", color=col)
        ax.text(2, 5.75, ex, ha="center", fontsize=10.5, color=GRAY)
        top = 1.3 + 0.95 * len(layers)
        ax.add_patch(FancyBboxPatch((0.5, 1.15), 3.0, top - 1.0, boxstyle="round,pad=0.04,rounding_size=0.15",
                                    fc="#F6FAFB", ec=col, lw=1.5, ls="--"))
        for i, (t, fc) in enumerate(layers):
            blk(ax, 0.7, 1.3 + i * 0.95, 2.6, 0.75, t, fc=fc, ec=ACC if fc == ACC_BG else TEAL, fs=10.5)
        ax.text(3.62, (1.15 + top) / 2, "× L", fontsize=11, color=GRAY, ha="left", va="center")
        blk(ax, 0.7, top + 0.45, 2.6, 0.7, out, fc=col, ec=col, tc="white", fs=10, bold=True)
        arr(ax, 2, top + 0.15, 2, top + 0.45)
        ax.text(2, 0.5, desc, ha="center", va="center", fontsize=10.5, color=DARK, linespacing=1.6)
        if name == "Encoder–Decoder":
            ax.text(0.15, 1.3 + 0.95 * 1 + 0.37, "E→", fontsize=10, color=ACC, fontweight="bold", va="center")
    fig.tight_layout()
    save(fig, "archs.png")


# ------------------------------------------------------------------ 11. ViT patch
def fig_vit():
    fig = plt.figure(figsize=(8.4, 4.0))
    ax = fig.add_axes([0.0, 0.08, 0.36, 0.84])
    yy, xx = np.mgrid[0:224, 0:224]
    img = np.stack([0.55 + 0.35 * np.sin(xx / 30.0), 0.7 + 0.25 * np.cos(yy / 26.0),
                    0.75 + 0.2 * np.sin((xx + yy) / 45.0)], -1)
    c = (xx - 120) ** 2 + (yy - 100) ** 2 < 55 ** 2
    img[c] = [0.88, 0.48, 0.18]
    ax.imshow(np.clip(img, 0, 1), extent=[0, 224, 224, 0])
    for k in range(0, 225, 16):
        ax.axhline(k, color="white", lw=0.8)
        ax.axvline(k, color="white", lw=0.8)
    ax.add_patch(Rectangle((0, 0), 16, 16, fill=False, ec=ACC, lw=2.5))
    ax.set_xticks([0, 224])
    ax.set_yticks([0, 224])
    ax.tick_params(labelsize=11)
    ax.set_title("224×224 이미지 → 16×16 patch", fontsize=13, color=DARK)
    ax2 = fig.add_axes([0.40, 0.0, 0.6, 1.0])
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 6)
    ax2.axis("off")
    ax2.text(0.2, 5.3, "14 × 14 = 196개 patch", fontsize=14, fontweight="bold", color=TEAL)
    ax2.text(0.2, 4.65, "patch 하나(16·16·3 = 768값) → 선형 투영 → d차원 token", fontsize=12, color=DARK)
    labels = ["CLS*", "p1", "p2", "p3", "…", "p196"]
    for i, t in enumerate(labels):
        fc = ACC_BG if i == 0 else MINT
        blk(ax2, 0.2 + i * 1.6, 3.1, 1.35, 0.8, t, fc=fc, ec=ACC if i == 0 else TEAL, fs=13, bold=True)
        blk(ax2, 0.2 + i * 1.6, 2.2, 1.35, 0.55, "+ pos", fc="white", ec=LINE, fs=11.5)
    arr(ax2, 5.0, 2.1, 5.0, 1.55)
    blk(ax2, 1.0, 0.7, 8.0, 0.8, "Transformer Encoder (self-attention + FFN) × L", fc=TEAL, ec=TEAL,
        tc="white", fs=12.5, bold=True)
    ax2.text(0.2, 0.1, "* CLS · pooling · 위치 임베딩 방식은 모델마다 다름", fontsize=11, color=GRAY)
    save(fig, "vit_patch.png")


# ------------------------------------------------------------------ 12. 과정 계보 + 여섯 질문
def fig_genealogy():
    ev = [(1943, "McCulloch–Pitts\n논리 뉴런"), (1958, "Perceptron"), (1986, "역전파 확산"),
          (1989, "CNN·LeNet"), (1997, "LSTM"), (2003, "신경 언어모델"), (2012, "AlexNet"),
          (2013, "Word2Vec"), (2014, "Seq2Seq·\nAttention"), (2015, "ResNet"), (2016, "LayerNorm"),
          (2017, "Transformer"), (2018, "BERT·GPT"), (2020, "ViT·Pre-LN\n분석"), (2022, "FlashAttn·\nDiT"),
          (2023, "GQA")]
    xs = np.arange(len(ev))
    fig, ax = plt.subplots(figsize=(14.5, 4.4))
    ax.set_xlim(-0.7, len(ev) - 0.3)
    ax.set_ylim(-3.0, 2.7)
    ax.axis("off")
    ax.plot([-0.5, len(ev) - 0.5], [0, 0], color=LINE, lw=3, zorder=1)
    for i, (y, t) in enumerate(ev):
        after = y > 2017
        col = ACC if y == 2017 else (GRAY if after else TEAL)
        ax.plot(i, 0, "o", ms=14 if y == 2017 else 11, color=col, mec="white", mew=2, zorder=3)
        up = i % 2 == 0
        ax.text(i, 0.4 if up else -0.4, str(y), ha="center", va="bottom" if up else "top", fontsize=15,
                fontweight="bold", color=col)
        ax.text(i, 0.98 if up else -0.98, t, ha="center", va="bottom" if up else "top", fontsize=12.5,
                color=DARK, linespacing=1.15)
    ax.fill_between([11.5, len(ev) - 0.3], -1.85, 2.7, color="#F3F6F8", zorder=0)
    ax.text(13.5, 2.4, "2017 이후 (확장 학습)", ha="center", fontsize=13, color=GRAY, fontweight="bold")
    qs = [("1주", "배울 수 있을까?", 0, 1.4), ("2주", "직선으로 안 되면?", 1, 2.4),
          ("3주", "공간 구조는?", 3, 3.4), ("4주", "순서·먼 기억은?", 4, 8.4),
          ("5주", "원문을 다시 보면?", 8, 11.4), ("6주", "참조만으로 만들면?", 11, 15.4)]
    span = (len(ev) - 0.3 + 0.6) / 6
    for k, (w, q, a, b) in enumerate(qs):
        a0 = -0.6 + k * span
        col = ACC if k == 5 else TEAL
        bw = span - 0.45
        ax.add_patch(FancyBboxPatch((a0 + 0.08, -2.95), bw, 1.0,
                                    boxstyle="round,pad=0.02,rounding_size=0.12", fc=ACC_BG if k == 5 else MINT,
                                    ec=col, lw=1.2))
        ax.text(a0 + 0.08 + bw / 2, -2.45, f"{w}\n{q}", ha="center", va="center", fontsize=13,
                color=col, fontweight="bold", linespacing=1.35)
        if k < 5:
            arr(ax, a0 + 0.1 + bw, -2.45, a0 + span + 0.06, -2.45, c=GRAY, lw=1.2)
    save(fig, "genealogy.png")


if __name__ == "__main__":
    for f in (fig_ln_axis, fig_postpre, fig_shift, fig_causal, fig_encdec, fig_lr, fig_kv, fig_mem,
              fig_flops, fig_archs, fig_vit, fig_genealogy):
        f()
        print("ok", f.__name__)
