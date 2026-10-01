"""Week 4 그림 생성: python build/assets/week4/make_figs.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))
from deckkit import PALETTE_HEX as P, mpl_setup  # noqa: E402

plt = mpl_setup()
plt.rcParams["mathtext.default"] = "it"  # 수식은 DejaVu 사용(− 기호 지원)
import numpy as np  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

TEAL, TEAL2, MINT, DARK, GRAY, ACC, LINE = (P[k] for k in
                                            ("TEAL", "TEAL2", "MINT", "DARK", "GRAY", "ACCENT", "LINE"))
ACC_BG = "#FDF1E8"
MINT2 = "#CFE8EE"


def out(name):
    return os.path.join(HERE, name)


def rbox(ax, x, y, w, h, fc=MINT, ec=None, lw=1.5, text=None, fs=13, tc=DARK, bold=False, r=0.08):
    b = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc,
                       ec=ec or fc, lw=lw)
    ax.add_patch(b)
    if text is not None:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc,
                fontweight="bold" if bold else "normal")
    return b


def arr(ax, x1, y1, x2, y2, c=TEAL2, lw=2.0, ms=16, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms,
                                 color=c, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0))


# ------------------------------------------------------------------ 1. one-hot @ E = lookup
def onehot_lookup():
    E = np.array([[0.2, -0.5, 0.1], [0.9, 0.3, -0.2], [-0.4, 0.8, 0.5],
                  [0.7, -0.1, 0.6], [-0.3, -0.6, 0.4]])
    words = ["<pad>", "나는", "학교", "간다", "학생"]
    oh = np.zeros(5)
    oh[3] = 1
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.set_xlim(0, 19.2)
    ax.set_ylim(0.9, 7.6)
    ax.axis("off")
    cw, ch = 1.0, 0.95
    # one-hot row (1x5)
    x0, y0 = 0.3, 4.2
    for j in range(5):
        fc = ACC if j == 3 else "white"
        rbox(ax, x0 + j * cw, y0, cw * 0.95, ch, fc=fc, ec=LINE, text=f"{int(oh[j])}", fs=17,
             tc="white" if j == 3 else DARK, bold=j == 3, r=0.05)
        ax.text(x0 + j * cw + cw * 0.47, y0 - 0.3, f"{j}", ha="center", va="top", fontsize=13, color=GRAY)
    ax.text(x0 + 2.5 * cw, y0 + ch + 0.35, "one-hot (id = 3)\nshape (1, |V|=5)", ha="center",
            va="bottom", fontsize=14.5, color=DARK)
    ax.text(5.85, y0 + ch / 2, "@", ha="center", va="center", fontsize=28, color=TEAL, fontweight="bold")
    # E (5x3) — 행 레이블은 표 왼쪽 바깥에
    ex, ey = 8.3, 1.2
    for i in range(5):
        yy = ey + (4 - i) * ch * 1.08
        hl = i == 3
        ax.text(ex - 0.35, yy + ch / 2, f"{i} {words[i]}", ha="right", va="center", fontsize=14,
                color=ACC if hl else GRAY, fontweight="bold" if hl else "normal")
        for j in range(3):
            rbox(ax, ex + j * cw * 1.25, yy, cw * 1.18, ch * 0.95, fc=ACC_BG if hl else MINT,
                 ec=ACC if hl else MINT2, lw=2 if hl else 1, text=f"{E[i, j]:+.1f}", fs=15,
                 tc=DARK, bold=hl, r=0.05)
    ax.text(ex + 1.85, ey + 5 * ch * 1.08 + 0.25, "E  shape (|V|=5, d=3)\n설명용 작은 어휘", ha="center",
            va="bottom", fontsize=14.5, color=DARK, linespacing=1.3)
    ax.text(12.9, y0 + ch / 2, "=", ha="center", va="center", fontsize=30, color=TEAL, fontweight="bold")
    # result
    rx = 13.9
    for j in range(3):
        rbox(ax, rx + j * cw * 1.25, y0, cw * 1.18, ch, fc=ACC, text=f"{E[3, j]:+.1f}", fs=16,
             tc="white", bold=True, r=0.05)
    ax.text(rx + 1.85, y0 + ch + 0.35, "x = E[3]\nshape (1, d=3)", ha="center", va="bottom",
            fontsize=14.5, color=DARK)
    ax.text(rx + 1.85, y0 - 0.5, "곱셈 대신 3번 행을\n바로 꺼내면(lookup) 같다", ha="center", va="top",
            fontsize=14, color=ACC, fontweight="bold", linespacing=1.3)
    fig.savefig(out("onehot_lookup.png"), facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ 2. analogy plot
def analogy():
    pts = {"man": (1.0, 1.0), "woman": (1.6, 2.6), "king": (4.0, 1.4), "queen": (4.6, 3.0),
           "서울": (7.2, 0.8), "한국": (8.4, 1.9), "파리": (6.6, 3.0), "프랑스": (7.8, 4.1)}
    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    for w, (x, y) in pts.items():
        c = TEAL if w in ("man", "woman", "king", "queen") else TEAL2
        ax.scatter([x], [y], s=110, color=c, zorder=3)
        ax.text(x + 0.12, y - 0.28, w, fontsize=14, color=DARK, fontweight="bold")
    def a(p, q, c, ls="-"):
        ax.annotate("", xy=pts[q], xytext=pts[p],
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=2.2, ls=ls, shrinkA=6, shrinkB=6))
    a("man", "woman", ACC)
    a("king", "queen", ACC)
    a("man", "king", GRAY, "--")
    a("woman", "queen", GRAY, "--")
    a("서울", "한국", TEAL2)
    a("파리", "프랑스", TEAL2)
    ax.text(0.3, 1.9, "성별 방향", color=ACC, fontsize=15, rotation=62, fontweight="bold")
    ax.text(6.3, 1.25, "수도→국가", color=TEAL2, fontsize=15, rotation=42, fontweight="bold")
    ax.set_xlim(0, 9.8)
    ax.set_ylim(0, 4.9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("임의의 축 1", color=GRAY)
    ax.set_ylabel("임의의 축 2", color=GRAY)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("king - man + woman ≈ queen", fontsize=14, color=DARK)
    fig.savefig(out("analogy.png"), facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ 3. RNN unrolled
def rnn_unrolled():
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 9.2)
    ax.axis("off")
    toks = ["나는", "학교에", "간다", "…"]
    xs = [2.2, 7.2, 12.2, 17.2]
    ax.text(11.0, 8.6, r"모든 셀이 같은 규칙:  $h_t = \tanh(x_t W_x + h_{t-1} W_h + b)$   (같은 $W_x, W_h, b$ 재사용)",
            ha="center", va="center", fontsize=13, color=TEAL)
    rbox(ax, 0.1, 3.5, 1.2, 1.2, fc="white", ec=LINE, text="$h_0$\n= 0", fs=12, tc=GRAY)
    for k, (x, t) in enumerate(zip(xs, toks)):
        last = k == 3
        lab = "$h_t$" if last else f"$h_{k + 1}$"
        xl = f"$x_t$" if last else f"$x_{k + 1}$"
        rbox(ax, x, 3.2, 2.6, 1.8, fc=MINT, ec=TEAL, lw=2, text="RNN 셀", fs=14, tc=DARK, bold=True)
        rbox(ax, x + 0.3, 0.3, 2.0, 1.2, fc="white", ec=LINE, text=f"{xl}\n{t}", fs=12.5)
        arr(ax, x + 1.3, 1.55, x + 1.3, 3.15)
        rbox(ax, x + 0.55, 6.3, 1.5, 1.0, fc=ACC if last else TEAL, text=lab, fs=15, tc="white", bold=True)
        arr(ax, x + 1.3, 5.05, x + 1.3, 6.25)
        px = 1.3 if k == 0 else xs[k - 1] + 2.6
        arr(ax, px + 0.05, 4.1, x - 0.05, 4.1, c=ACC, lw=2.5)
        if k:
            lab_prev = "$h_{t-1}$" if last else f"$h_{k}$"
            ax.text((px + x) / 2, 4.35, lab_prev, ha="center", va="bottom", fontsize=13, color=ACC)
    ax.text(20.0, 4.1, "시간 →", fontsize=13, color=GRAY, va="center")
    fig.savefig(out("rnn_unrolled.png"), facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ 4. gradient decay
def grad_decay():
    k = np.arange(0, 51)
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    for f, c, lab in ((1.1, ACC, "배율 1.1 → 폭주 (exploding)"), (1.0, GRAY, "배율 1.0 → 유지"),
                      (0.9, TEAL, "배율 0.9 → 소실 (vanishing)")):
        ax.plot(k, f ** k, color=c, lw=3, label=lab)
    ax.set_yscale("log")
    ax.set_xlabel("거슬러 올라간 시점 수 k", fontsize=13)
    ax.set_ylabel("gradient 크기 배율 (로그 축)", fontsize=13)
    for kk, f, c in ((50, 0.9, TEAL), (50, 1.1, ACC), (10, 0.9, TEAL)):
        v = f ** kk
        ax.scatter([kk], [v], color=c, zorder=4, s=50)
        txt = f"{f}의 {kk}제곱 ≈ {v:.3g}"
        off, ha = ((-10, 12), "right") if f > 1 else (((-10, -22), "right") if kk == 50 else ((8, 10), "left"))
        ax.annotate(txt, (kk, v), xytext=off, textcoords="offset points",
                    ha=ha, fontsize=12, color=c, fontweight="bold")
    ax.grid(alpha=0.3, which="major")
    ax.legend(loc="upper left", fontsize=12, frameon=False)
    ax.set_ylim(1e-3, 1e3)
    ax.set_yticks([1e-3, 1e-2, 1e-1, 1, 10, 100, 1000])
    ax.set_yticklabels(["0.001", "0.01", "0.1", "1", "10", "100", "1000"])
    ax.minorticks_off()
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.savefig(out("grad_decay.png"), facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ 5. LSTM cell
def lstm_cell():
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    ax.set_xlim(0, 21)
    ax.set_ylim(0.9, 11.4)
    ax.axis("off")
    rbox(ax, 2.2, 1.2, 16.2, 9.6, fc="#F7FBFC", ec=LINE, lw=1.5, r=0.3)
    # cell state highway
    yc = 9.2
    arr(ax, 0.2, yc, 20.6, yc, c=ACC, lw=4, ms=22)
    ax.text(0.3, yc + 0.45, r"$c_{t-1}$", fontsize=14, color=ACC, fontweight="bold")
    ax.text(19.3, yc + 0.45, r"$c_t$", fontsize=14, color=ACC, fontweight="bold")
    ax.text(11.0, yc + 1.05, "cell state: 덧셈으로 갱신되는 기억 경로", fontsize=12.5, color=ACC,
            ha="center", fontweight="bold")

    def op(x, y, s):
        ax.add_patch(plt.Circle((x, y), 0.55, fc="white", ec=ACC, lw=2.5, zorder=4))
        ax.text(x, y, s, ha="center", va="center", fontsize=17, color=ACC, fontweight="bold", zorder=5)

    op(5.6, yc, "×")
    op(10.5, yc, "+")
    # gates
    gates = [(5.6, r"$f_t=\sigma$", "보존 (forget)"), (8.9, r"$i_t=\sigma$", "쓰기 (input)"),
             (12.1, r"$g_t=\tanh$", "후보 값"), (15.3, r"$o_t=\sigma$", "읽기 (output)")]
    gy = 3.6
    for x, lab, desc in gates:
        rbox(ax, x - 1.45, gy - 0.45, 2.9, 1.9, fc=TEAL if "sigma" in lab else TEAL2, r=0.1)
        ax.text(x, gy + 0.9, lab, ha="center", va="center", fontsize=14.5, color="white")
        ax.text(x, gy + 0.05, desc, ha="center", va="center", fontsize=13, color="white",
                fontweight="bold")
    # f -> x
    arr(ax, 5.6, gy + 1.45, 5.6, yc - 0.6)
    # i, g -> multiply -> +
    op(10.5, 6.9, "×")
    arr(ax, 8.9, gy + 1.45, 10.1, 6.5)
    arr(ax, 12.1, gy + 1.45, 10.9, 6.5)
    arr(ax, 10.5, 7.45, 10.5, yc - 0.6)
    # output path
    rbox(ax, 14.1, 6.6, 2.2, 1.0, fc=MINT2, text="tanh", fs=12.5)
    arr(ax, 15.2, yc - 0.1, 15.2, 7.65, c=ACC, lw=2)
    op(17.3, 5.6, "×")
    arr(ax, 15.2, 6.55, 16.8, 5.8)
    arr(ax, 15.3, gy + 1.45, 16.8, 5.4)
    arr(ax, 17.85, 5.6, 20.6, 5.6, c=TEAL, lw=3.5, ms=20)
    ax.text(19.0, 5.95, r"$h_t$", fontsize=15, color=TEAL, fontweight="bold")
    # inputs bus
    ax.plot([0.2, 15.3], [2.0, 2.0], color=GRAY, lw=2)
    for x, _, _ in gates:
        arr(ax, x, 2.0, x, gy - 0.47, c=GRAY, lw=1.6, ms=12)
    ax.text(0.3, 2.35, r"$[h_{t-1}, x_t]$", fontsize=14, color=DARK, fontweight="bold")
    fig.savefig(out("lstm_cell.png"), facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ 6. Seq2Seq bottleneck
def seq2seq():
    # 아래쪽 설명 문장은 슬라이드 글머리표가 대신한다 (그림에는 토큰·화살표만)
    fig, ax = plt.subplots(figsize=(12, 4.3))
    ax.set_xlim(0, 23.6)
    ax.set_ylim(1.1, 9.9)
    ax.axis("off")
    src = ["I", "am", "a", "student"]
    tgt_in = ["BOS", "나는", "학생", "이다"]
    tgt_out = ["나는", "학생", "이다", "EOS"]
    ex = [0.4 + i * 2.3 for i in range(4)]
    for i, (x, w) in enumerate(zip(ex, src)):
        rbox(ax, x, 3.6, 1.8, 1.5, fc=TEAL, text="Enc", fs=15, tc="white", bold=True)
        ax.text(x + 0.9, 1.75, w, ha="center", fontsize=16, color=DARK)
        arr(ax, x + 0.9, 2.5, x + 0.9, 3.55, c=GRAY)
        if i:
            arr(ax, x - 0.5, 4.35, x - 0.02, 4.35)
    ax.text(ex[0] + 0.9, 6.9, "Encoder (S = 4)", ha="left", fontsize=15, color=TEAL, fontweight="bold")
    # context
    cx = 10.2
    arr(ax, ex[-1] + 1.85, 4.35, cx - 0.05, 4.35, c=ACC, lw=3)
    rbox(ax, cx, 3.3, 1.7, 2.1, fc=ACC, text="c", fs=24, tc="white", bold=True)
    ax.text(cx + 0.85, 6.0, "고정 길이\n문맥 벡터", ha="center", fontsize=14.5, color=ACC, fontweight="bold")
    ax.text(cx + 0.85, 2.4, "병목!", ha="center", fontsize=16, color=ACC, fontweight="bold")
    dx = [13.4 + i * 2.6 for i in range(4)]
    arr(ax, cx + 1.75, 4.35, dx[0] - 0.02, 4.35, c=ACC, lw=3)
    for i, x in enumerate(dx):
        rbox(ax, x, 3.6, 1.8, 1.5, fc=TEAL2, text="Dec", fs=15, tc="white", bold=True)
        ax.text(x + 0.9, 1.75, tgt_in[i], ha="center", fontsize=15.5, color=GRAY)
        arr(ax, x + 0.9, 2.5, x + 0.9, 3.55, c=GRAY)
        arr(ax, x + 0.9, 5.15, x + 0.9, 6.45, c=TEAL)
        rbox(ax, x + 0.1, 6.5, 1.6, 0.95, fc="white", ec=TEAL, text=tgt_out[i], fs=15, bold=True)
        if i:
            arr(ax, x - 0.78, 4.35, x - 0.02, 4.35)
    ax.text(dx[0], 8.1, "Decoder (T = 3 토큰 + EOS)", ha="left", fontsize=15, color=TEAL2, fontweight="bold")
    ax.text(dx[0], 9.25, r"$p(y_t \mid y_{<t}, c)$", ha="left", fontsize=15, color=DARK, fontweight="bold")
    fig.savefig(out("seq2seq.png"), facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    onehot_lookup()
    analogy()
    rnn_unrolled()
    grad_decay()
    lstm_cell()
    seq2seq()
    print("ok")
