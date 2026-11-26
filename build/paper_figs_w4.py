"""Week 4 논문 그림 (독립 실행): python paper_figs_w4.py → build/assets/week4/paper_*.png

논문 원본 이미지는 쓰지 않고, 원문 그림·표의 구조를 matplotlib 도식으로 새로 그린다.
근거: build/research/papers/week4.md
  - Elman (1990) Fig.1(Jordan)·Fig.2(Elman SRN)              → paper_elman_fig12.png
  - Elman (1990) Fig.7 (은닉 표현 계층 군집, 단순화)            → paper_elman_tree.png
  - Hochreiter & Schmidhuber (1997) Fig.1 (memory cell, CEC)  → paper_lstm1997.png
  - Gers, Schmidhuber & Cummins (2000) §3 (forget gate)       → paper_lstm2000.png
  - Gers et al. (2000) 손계산: f ≡ 1 vs f = 0.9 상태 크기       → paper_gers_growth.png
  - Gers et al. (2000) Table 2 (연속 Reber, 완벽 해 비율)       → paper_gers_table2.png
  - Bengio et al. (2003) Table 1 (Brown 시험 perplexity)       → paper_bengio_ppl.png
  - Mikolov et al. (2013a) Fig.1 (CBOW / Skip-gram)           → paper_w2v_arch.png
  - Mikolov et al. (2013a) Table 3 (의미/문법 정확도)           → paper_w2v_table3.png
  - Cho et al. (2014a) §2.2 vs Sutskever et al. (2014) Eq.1   → paper_encdec_compare.png
  - Sutskever et al. (2014) §3.3 (입력 뒤집기와 거리)           → paper_reverse.png
  - Sutskever et al. (2014) Table 1 (직접 번역 BLEU)            → paper_s2s_table1.png
  - Cho et al. (2014b) Table 1(a) (전체 / UNK 없는 문장 BLEU)   → paper_cho14b_table1.png
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
plt.rcParams["font.family"] = ["NanumGothic", "DejaVu Sans"]  # 한글 + 기호 fallback
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Arc  # noqa: E402

OUT = os.path.join(HERE, "assets", "week4")
T, T2, A, G, D = P["TEAL"], P["TEAL2"], P["ACCENT"], P["GRAY"], P["DARK"]
M, M2, LN = P["MINT"], P.get("MINT2", "#D6E6FA"), P["LINE"]
ACC_BG = P.get("ACC_BG", "#FFF3EA")
BG = P.get("BG", "#F5F5F7")


def _save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    fig.savefig(p, facecolor="white")
    plt.close(fig)
    print("saved", p)
    return p


def _arrow(ax, p, q, color=G, lw=2.0, style="-|>", ms=16, ls="-", rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=color, lw=lw,
                                 linestyle=ls, shrinkA=0, shrinkB=0,
                                 connectionstyle=f"arc3,rad={rad}"))


def _box(ax, x, y, w, h, text="", fc=M2, ec=None, fs=16, tc=D, bold=True, lw=1.8, r=0.12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc,
                                ec=ec or fc, lw=lw))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc,
                fontweight="bold" if bold else "normal")


# ------------------------------------------------------------------ 1. Jordan(Fig.1) vs Elman(Fig.2)
def elman_fig12():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.6))
    for k, ax in enumerate(axes):
        ax.set_xlim(0, 10); ax.set_ylim(0, 9.4); ax.axis("off")
        jordan = k == 0
        ax.text(5, 9.0, "Jordan (1986): 출력 → state" if jordan else "Elman (1990): 은닉 → context",
                ha="center", va="center", fontsize=19, fontweight="bold", color=G if jordan else T)
        # 층 상자
        _box(ax, 3.0, 6.4, 4.0, 1.1, "출력 (output)", fc=M2, fs=16)
        _box(ax, 3.0, 3.8, 4.0, 1.1, "은닉 (hidden)", fc=T if not jordan else M2,
             tc="white" if not jordan else D, fs=16)
        _box(ax, 0.6, 1.0, 3.6, 1.1, "입력 (input)", fc=BG, ec=LN, fs=16)
        side = "state" if jordan else "context"
        _box(ax, 5.8, 1.0, 3.6, 1.1, side, fc=ACC_BG, ec=A, fs=17, tc=A)
        _arrow(ax, (2.4, 2.1), (4.0, 3.8), color=G, lw=2.2)
        _arrow(ax, (7.6, 2.1), (6.0, 3.8), color=G, lw=2.2)
        _arrow(ax, (5.0, 4.9), (5.0, 6.4), color=G, lw=2.2)
        if jordan:   # 출력 → state 되먹임
            ax.plot([7.0, 9.6, 9.6], [6.95, 6.95, 2.1], color=A, lw=2.6)
            _arrow(ax, (9.6, 2.6), (9.6, 2.12), color=A, lw=2.6)
            ax.text(9.75, 4.6, "출력을\n되먹임", ha="left", va="center", fontsize=14, color=A)
        else:        # 은닉 → context 복사 (고정 1.0)
            ax.plot([7.0, 9.6, 9.6], [4.35, 4.35, 2.1], color=A, lw=2.6, ls="--")
            _arrow(ax, (9.6, 2.6), (9.6, 2.12), color=A, lw=2.6)
            ax.text(9.75, 3.25, "복사\n(1.0 고정)", ha="left", va="center", fontsize=14, color=A,
                    fontweight="bold")
        ax.text(5, 0.35, "한 시점 뒤 state가 은닉층에 다시 들어간다" if jordan
                else "context(t) = 은닉(t−1)  ·  초기값 0.5  ·  학습 안 함",
                ha="center", va="center", fontsize=14, color=G if jordan else D)
    fig.text(0.5, -0.02, "Elman (1990) Fig.1·Fig.2 기반 재구성 — 대부분의 과제는 '다음 입력 예측'",
             ha="center", fontsize=13, color=G)
    fig.tight_layout()
    return _save(fig, "paper_elman_fig12.png")


# ------------------------------------------------------------------ 2. Elman Fig.7 단순화 계층 군집
def elman_tree():
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    ax.set_xlim(-0.2, 10.6); ax.set_ylim(-0.6, 8.9); ax.axis("off")
    leaves = ["목적어 필수", "목적어 선택", "목적어 불가", "사람", "큰 동물", "작은 동물", "먹는 것", "깨지는 것"]
    ys = {name: 8.0 - i * 1.0 for i, name in enumerate(leaves)}
    lx = 6.6   # 잎 x
    for name, y in ys.items():
        verb = leaves.index(name) < 3
        ax.text(lx + 0.15, y, name, ha="left", va="center", fontsize=17,
                color=A if verb else T, fontweight="bold")

    def join(a, b, x, col=G):
        """두 노드 (y, x0) 를 x에서 묶어 새 노드 반환"""
        (ya, xa), (yb, xb) = a, b
        ax.plot([xa, x, x, xb], [ya, ya, yb, yb], color=col, lw=2.4, solid_joinstyle="miter")
        return ((ya + yb) / 2, x)

    L = {n: (y, lx) for n, y in ys.items()}
    v12 = join(L["목적어 필수"], L["목적어 선택"], 5.6, A)
    verbs = join(v12, L["목적어 불가"], 4.6, A)
    animal = join(L["큰 동물"], L["작은 동물"], 5.7, T)
    alive = join(L["사람"], animal, 4.9, T)
    thing = join(L["먹는 것"], L["깨지는 것"], 5.3, T)
    nouns = join(alive, thing, 3.6, T)
    root = join(verbs, nouns, 1.6, G)
    ax.plot([root[1] - 0.8, root[1]], [root[0], root[0]], color=G, lw=2.4)
    ax.text(verbs[1] - 0.12, verbs[0] + 0.35, "동사", ha="right", fontsize=17, color=A, fontweight="bold")
    ax.text(nouns[1] - 0.12, nouns[0] + 0.35, "명사", ha="right", fontsize=17, color=T, fontweight="bold")
    ax.text(alive[1] - 0.1, alive[0] + 0.3, "생물", ha="right", fontsize=14, color=T)
    ax.text(thing[1] - 0.1, thing[0] + 0.3, "무생물", ha="right", fontsize=14, color=T)
    ax.text(animal[1] - 0.1, animal[0] + 0.3, "동물", ha="right", fontsize=14, color=T)
    ax.text(5.0, -0.35, "Elman (1990) Fig.7 기반 단순화 재구성 — 가로 거리는 설명용(원문 수치 아님)",
            ha="center", fontsize=13, color=G)
    return _save(fig, "paper_elman_tree.png")


# ------------------------------------------------------------------ 3·4. LSTM memory cell 1997 / 2000
def _cell(forget):
    fig, ax = plt.subplots(figsize=(12, 6.2))
    ax.set_xlim(0, 24); ax.set_ylim(-1.4, 11.8); ax.set_aspect("equal"); ax.axis("off")
    yc = 4.6
    # 셀 입력 g
    ax.text(0.6, yc, r"$net_c$", ha="left", va="center", fontsize=18, color=D)
    _arrow(ax, (2.3, yc), (3.1, yc), color=G, lw=2.2)
    _box(ax, 3.1, yc - 0.75, 2.0, 1.5, "g", fc=M2, fs=22)
    _arrow(ax, (5.1, yc), (6.25, yc), color=G, lw=2.2)
    # 입력 게이트 곱
    ax.add_patch(Circle((7.0, yc), 0.75, fc="white", ec=T, lw=2.6))
    ax.text(7.0, yc, "×", ha="center", va="center", fontsize=24, color=T, fontweight="bold")
    _box(ax, 6.0, 0.6, 2.0, 1.4, r"$y^{in}$", fc=T, tc="white", fs=19)
    _arrow(ax, (7.0, 2.0), (7.0, yc - 0.75), color=T, lw=2.4)
    ax.text(7.0, 0.15, "입력 게이트", ha="center", va="center", fontsize=14, color=T)
    _arrow(ax, (7.75, yc), (9.4, yc), color=G, lw=2.2)
    # CEC 상태 s_c
    ax.add_patch(Circle((9.4 + 0.0, yc), 0.0, fc="none"))
    _box(ax, 9.4, yc - 1.0, 3.0, 2.0, "", fc=ACC_BG, ec=A, lw=2.6)
    ax.text(10.9, yc + 0.25, r"$s_c$", ha="center", va="center", fontsize=24, color=A, fontweight="bold")
    ax.text(10.9, yc - 0.55, "+ (덧셈)", ha="center", va="center", fontsize=14, color=A)
    # 자기 연결 루프
    ax.add_patch(Arc((10.9, yc + 1.0), 2.6, 3.2, theta1=0, theta2=180, color=A, lw=2.8))
    _arrow(ax, (9.62, yc + 1.25), (9.62, yc + 1.02), color=A, lw=2.8, ms=18)
    if forget:
        ax.add_patch(Circle((10.9, yc + 2.6), 0.62, fc="white", ec=T, lw=2.6))
        ax.text(10.9, yc + 2.6, "×", ha="center", va="center", fontsize=22, color=T, fontweight="bold")
        _box(ax, 13.0, yc + 3.1, 2.2, 1.3, r"$y^{\varphi}$", fc=T, tc="white", fs=19)
        _arrow(ax, (13.0, yc + 3.75), (11.5, yc + 2.9), color=T, lw=2.4)
        ax.text(15.4, yc + 3.75, "forget gate (학습됨)", ha="left", va="center", fontsize=15, color=T,
                fontweight="bold")
    else:
        ax.text(10.9, yc + 2.95, "1.0 (고정)", ha="center", va="center", fontsize=17, color=A, fontweight="bold")
        ax.text(10.9, yc + 3.75, "CEC: 상수 오차 회전목마", ha="center", va="center", fontsize=15, color=A)
    # 출력: h(s) → × y_out
    _arrow(ax, (12.4, yc), (13.6, yc), color=G, lw=2.2)
    _box(ax, 13.6, yc - 0.75, 2.0, 1.5, "h", fc=M2, fs=22)
    _arrow(ax, (15.6, yc), (16.75, yc), color=G, lw=2.2)
    ax.add_patch(Circle((17.5, yc), 0.75, fc="white", ec=T, lw=2.6))
    ax.text(17.5, yc, "×", ha="center", va="center", fontsize=24, color=T, fontweight="bold")
    _box(ax, 16.5, 0.6, 2.0, 1.4, r"$y^{out}$", fc=T, tc="white", fs=19)
    _arrow(ax, (17.5, 2.0), (17.5, yc - 0.75), color=T, lw=2.4)
    ax.text(17.5, 0.15, "출력 게이트", ha="center", va="center", fontsize=14, color=T)
    _arrow(ax, (18.25, yc), (20.0, yc), color=T, lw=2.6)
    ax.text(20.2, yc, r"$y^{c}$", ha="left", va="center", fontsize=20, color=T, fontweight="bold")
    if forget:
        eq = r"$s_c(t) = y^{\varphi}(t)\cdot s_c(t-1) + y^{in}(t)\cdot g(net_c(t))$"
        cap = "Gers, Schmidhuber & Cummins (2000) §3 기반 재구성 — 고정 1.0을 학습되는 게이트로 바꿈"
    else:
        eq = r"$s_c(t) = s_c(t-1) + y^{in}(t)\cdot g(net_c(t))$"
        cap = "Hochreiter & Schmidhuber (1997) Fig.1 기반 재구성 — forget gate 없음"
    ax.text(12.0, 11.1, eq, ha="center", va="center", fontsize=19, color=D)
    ax.text(12.0, -1.0, cap, ha="center", va="center", fontsize=13, color=G)
    return fig


def lstm1997():
    return _save(_cell(False), "paper_lstm1997.png")


def lstm2000():
    return _save(_cell(True), "paper_lstm2000.png")


# ------------------------------------------------------------------ 5. 잊지 못하면 상태가 커진다
def gers_growth():
    t = np.arange(0, 101)
    c1 = 0.25 * t
    c9 = np.zeros_like(t, dtype=float)
    for k in range(1, 101):
        c9[k] = 0.9 * c9[k - 1] + 0.25
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.plot(t, c1, color=A, lw=3.6, label="f ≡ 1 (1997 원형): 더하기만")
    ax.plot(t, c9, color=T, lw=3.6, label="f = 0.9 (forget gate)")
    ax.axhline(2.5, color=T, lw=1.4, ls=":")
    ax.scatter([100, 100], [c1[-1], c9[-1]], color=[A, T], s=70, zorder=5)
    ax.text(70, 25.0, "100단계 후 c = 25.0 (계속 증가) →", ha="right", va="center", fontsize=16, color=A, fontweight="bold")
    ax.text(97, 4.0, "c → 0.25 / (1 − 0.9) = 2.5 에 수렴", ha="right", va="bottom", fontsize=16, color=T,
            fontweight="bold")
    ax.set_xlabel("시점 t (매 시점 i·g = 0.25가 들어오는 끊김 없는 스트림)", fontsize=15)
    ax.set_ylabel("셀 상태 c", fontsize=15)
    ax.tick_params(labelsize=13)
    ax.set_ylim(0, 27.5); ax.set_xlim(0, 103)
    ax.grid(alpha=0.35)
    ax.legend(fontsize=15, frameon=False, loc="center left", bbox_to_anchor=(0.0, 0.62))
    return _save(fig, "paper_gers_growth.png")


# ------------------------------------------------------------------ 6. Gers 2000 Table 2
def gers_table2():
    labs = ["표준 LSTM + 외부 리셋\n(경계를 알려 줌)", "표준 LSTM\n(리셋 없음)", "상태 감쇠 LSTM\n(자기 가중치 0.9)",
            "forget gate LSTM", "forget gate\n+ 학습률 감쇠"]
    vals = [74, 0, 0, 18, 62]
    cols = [G, A, A, T2, T]
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    y = np.arange(len(labs))[::-1]
    ax.barh(y, vals, color=cols, height=0.62)
    for yy, v in zip(y, vals):
        ax.text(v + 1.5, yy, f"{v}%", va="center", fontsize=17, fontweight="bold", color=D)
    ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=14)
    ax.set_xlim(0, 88)
    ax.set_xlabel("완벽한 해를 찾은 비율 (독립 학습 100회 중)", fontsize=15)
    ax.tick_params(axis="x", labelsize=13)
    ax.set_title("연속 내장 Reber 문법 (경계 표시 없는 스트림)", fontsize=16, color=D, loc="left")
    fig.text(0.98, 0.0, "Gers et al. (2000) Table 2 기반", ha="right", fontsize=12, color=G)
    return _save(fig, "paper_gers_table2.png")


# ------------------------------------------------------------------ 7. Bengio 2003 Table 1
def bengio_ppl():
    labs = ["신경망 MLP10\n(MLP9 + trigram 혼합)", "신경망 MLP9\n(혼합 없음)", "class-based back-off\n(최고 n-gram)",
            "Kneser-Ney 5-gram", "보간 trigram"]
    vals = [252, 276, 312, 321, 336]
    cols = [T, T2, G, G, G]
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    y = np.arange(len(labs))[::-1]
    ax.barh(y, vals, color=cols, height=0.6)
    for yy, v in zip(y, vals):
        ax.text(v + 4, yy, str(v), va="center", fontsize=17, fontweight="bold", color=D)
    ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=14)
    ax.set_xlim(0, 380)
    ax.set_xlabel("시험 perplexity (낮을수록 좋다)", fontsize=15)
    ax.tick_params(axis="x", labelsize=13)
    ax.set_title("Brown 말뭉치 (|V| = 16,383)", fontsize=16, color=D, loc="left")
    fig.text(0.98, 0.0, "Bengio et al. (2003) Table 1 기반", ha="right", fontsize=12, color=G)
    return _save(fig, "paper_bengio_ppl.png")


# ------------------------------------------------------------------ 8. Word2Vec Fig.1
def w2v_arch():
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.6))
    ctx = [r"$w(t-2)$", r"$w(t-1)$", r"$w(t+1)$", r"$w(t+2)$"]
    ys = [7.2, 5.4, 3.6, 1.8]
    for k, ax in enumerate(axes):
        ax.set_xlim(0, 10); ax.set_ylim(0, 9.4); ax.axis("off")
        cbow = k == 0
        ax.text(5, 8.9, "CBOW: 주변 → 가운데" if cbow else "Skip-gram: 가운데 → 주변",
                ha="center", va="center", fontsize=19, fontweight="bold", color=T)
        cx = 1.6 if cbow else 8.4
        mx = 5.0
        ox = 8.4 if cbow else 1.6
        for lab, y in zip(ctx, ys):
            _box(ax, cx - 1.3, y - 0.55, 2.6, 1.1, lab, fc=BG, ec=LN, fs=16, bold=False)
        _box(ax, mx - 1.0, 3.4, 2.0, 2.2, "평균\n(SUM)" if cbow else "투영\n(벡터)", fc=M2, fs=16)
        _box(ax, ox - 1.3, 4.5 - 0.6, 2.6, 1.2, r"$w(t)$", fc=T, tc="white", fs=18)
        for y in ys:
            if cbow:
                _arrow(ax, (cx + 1.3, y), (mx - 1.0, 4.5 + (y - 4.5) * 0.25), color=G, lw=2)
            else:
                _arrow(ax, (mx + 1.0, 4.5 + (y - 4.5) * 0.25), (cx - 1.3, y), color=G, lw=2)
        if cbow:
            _arrow(ax, (mx + 1.0, 4.5), (ox - 1.3, 4.5), color=T, lw=2.6)
        else:
            _arrow(ax, (ox + 1.3, 4.5), (mx - 1.0, 4.5), color=T, lw=2.6)
        ax.text(5, 0.55, "순서 무시 · 은닉층(비선형) 없음" if cbow else "먼 단어는 덜 뽑음 (최대 거리 C = 10)",
                ha="center", va="center", fontsize=14.5, color=D)
    fig.text(0.5, -0.02, "Mikolov et al. (2013a) Fig.1 기반 재구성 — 그림은 앞뒤 2개씩 (실험의 CBOW는 앞뒤 4개씩)",
             ha="center", fontsize=13, color=G)
    fig.tight_layout()
    return _save(fig, "paper_w2v_arch.png")


# ------------------------------------------------------------------ 9. Word2Vec Table 3
def w2v_table3():
    models = ["RNNLM", "NNLM", "CBOW", "Skip-gram"]
    sem = [9, 23, 24, 55]
    syn = [36, 53, 64, 59]
    x = np.arange(4)
    w = 0.38
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.bar(x - w / 2, sem, w, color=T, label="의미 관계 (예: 나라–수도)")
    ax.bar(x + w / 2, syn, w, color=P.get("MID", "#9CC5F2"), label="문법 관계 (예: 비교급·복수형)")
    for i in range(4):
        ax.text(x[i] - w / 2, sem[i] + 1.2, f"{sem[i]}", ha="center", fontsize=16, fontweight="bold", color=D)
        ax.text(x[i] + w / 2, syn[i] + 1.2, f"{syn[i]}", ha="center", fontsize=16, fontweight="bold", color=D)
    ax.set_xticks(x); ax.set_xticklabels(models, fontsize=16)
    ax.set_ylabel("정확도 (%) — 정확히 일치할 때만 정답", fontsize=14)
    ax.set_ylim(0, 78); ax.tick_params(axis="y", labelsize=13)
    ax.legend(fontsize=14, frameon=False, loc="upper left")
    ax.set_title("같은 데이터(3.2억 단어)·같은 차원(640)에서 비교", fontsize=15, color=D, loc="left")
    fig.text(0.98, 0.0, "Mikolov et al. (2013a) Table 3 기반", ha="right", fontsize=12, color=G)
    return _save(fig, "paper_w2v_table3.png")


# ------------------------------------------------------------------ 10. Cho 2014a vs Sutskever 2014 조건화
def encdec_compare():
    fig, axes = plt.subplots(2, 1, figsize=(12.5, 7.4))
    for k, ax in enumerate(axes):
        cho = k == 0
        ax.set_xlim(0, 25); ax.set_ylim(0, 6.6); ax.axis("off")
        title = ("Cho et al. (2014a): 요약 c를 디코더의 '매 시점'에 넣는다" if cho
                 else "Sutskever et al. (2014): v로 디코더를 '초기화'만 한다  (입력은 뒤집어서)")
        ax.text(0.2, 6.25, title, ha="left", va="center", fontsize=17, fontweight="bold", color=T if cho else D)
        src = ["A", "B", "C"] if cho else ["C", "B", "A"]
        xs = [1.2, 3.6, 6.0]
        for x, s in zip(xs, src):
            _box(ax, x, 2.1, 1.6, 1.3, "", fc=T)
            ax.text(x + 0.8, 0.9, s, ha="center", va="center", fontsize=18, color=D)
            _arrow(ax, (x + 0.8, 1.35), (x + 0.8, 2.1), color=G, lw=2)
        for x in xs[:-1]:
            _arrow(ax, (x + 1.6, 2.75), (x + 2.4, 2.75), color=T2, lw=2.2)
        # 요약
        _box(ax, 9.0, 1.9, 1.9, 1.7, "c" if cho else "v", fc=A, tc="white", fs=24)
        _arrow(ax, (7.6, 2.75), (9.0, 2.75), color=A, lw=2.6)
        ax.text(9.95, 1.3, "고정 길이 벡터", ha="center", va="center", fontsize=13.5, color=A)
        out = ["W", "X", "Y", "Z"]
        dx = [12.6, 15.4, 18.2, 21.0]
        prev = ["<s>", "W", "X", "Y"]
        for x, o, p in zip(dx, out, prev):
            _box(ax, x, 2.1, 1.6, 1.3, "", fc=T2)
            ax.text(x + 1.15, 4.75, o, ha="center", va="center", fontsize=18, color=D, fontweight="bold")
            _arrow(ax, (x + 1.15, 3.4), (x + 1.15, 4.35), color=T2, lw=2)
            ax.text(x + 0.8, 0.9, p, ha="center", va="center", fontsize=15, color=G)
            _arrow(ax, (x + 0.8, 1.3), (x + 0.8, 2.1), color=G, lw=1.8)
        for x in dx[:-1]:
            _arrow(ax, (x + 1.6, 2.75), (x + 2.8, 2.75), color=T2, lw=2.2)
        if cho:
            _arrow(ax, (10.9, 2.75), (12.6, 2.75), color=A, lw=2.4)
            ax.plot([9.95, 9.95, dx[-1] + 0.4], [3.6, 3.95, 3.95], color=A, lw=1.8, ls="--")
            for x in dx:
                _arrow(ax, (x + 0.4, 3.95), (x + 0.4, 3.42), color=A, lw=1.8, ms=13)
            ax.text(23.0, 2.75, "+ EOS", ha="left", va="center", fontsize=14, color=G)
        else:
            _arrow(ax, (10.9, 2.75), (12.6, 2.75), color=A, lw=2.6)
            ax.text(11.75, 3.25, "초기 상태", ha="center", va="bottom", fontsize=13, color=A)
            ax.text(23.0, 2.75, "+ EOS", ha="left", va="center", fontsize=14, color=G)
    fig.text(0.5, 0.0, "Cho et al. (2014a) §2.2 Fig.1, Sutskever et al. (2014) Fig.1·Eq.1 기반 재구성 — 두 방식 모두 고정 벡터 하나",
             ha="center", fontsize=12.5, color=G)
    fig.tight_layout()
    return _save(fig, "paper_encdec_compare.png")


# ------------------------------------------------------------------ 11. 입력 뒤집기와 거리
def reverse_dist():
    fig, axes = plt.subplots(2, 1, figsize=(12.5, 4.5))
    rows = [("정방향", ["I", "am", "a", "student", "<EOS>", "나는", "학생", "이다"]),
            ("역방향\n(입력만 뒤집음)", ["student", "a", "am", "I", "<EOS>", "나는", "학생", "이다"])]
    for ax, (name, toks) in zip(axes, rows):
        ax.set_xlim(-3.7, 22); ax.set_ylim(-1.25, 2.35); ax.axis("off")
        ax.text(-3.6, 0.5, name, ha="left", va="center", fontsize=15, fontweight="bold", color=D)
        xs = [2.0 + i * 2.5 for i in range(len(toks))]
        for i, (x, t) in enumerate(zip(xs, toks)):
            src = i < 4
            hi = t in ("I", "나는")
            fc = (A if hi else T) if src or t == "<EOS>" else (A if hi else T2)
            if t == "<EOS>":
                fc = G
            _box(ax, x - 1.1, 0.0, 2.2, 1.0, t, fc=fc, tc="white", fs=15)
        i0, i1 = toks.index("I"), toks.index("나는")
        gap = i1 - i0 - 1
        ax.plot([xs[i0], xs[i0], xs[i1], xs[i1]], [1.05, 1.75, 1.75, 1.05], color=A, lw=2.2)
        ax.text((xs[i0] + xs[i1]) / 2, 2.05, f"I ↔ 나는: 사이에 {gap}개", ha="center", va="center", fontsize=15,
                color=A, fontweight="bold")
        j0, j1 = toks.index("student"), toks.index("학생")
        g2 = j1 - j0 - 1
        ax.plot([xs[j0], xs[j0], xs[j1], xs[j1]], [-0.05, -0.6, -0.6, -0.05], color=G, lw=1.8)
        ax.text((xs[j0] + xs[j1]) / 2, -1.0, f"student ↔ 학생: 사이에 {g2}개", ha="center", va="center",
                fontsize=14, color=G)
    fig.text(0.5, -0.01, "Sutskever et al. (2014) §3.3 기반 — 평균 거리는 그대로, 맨 앞 단어들 사이의 '최소' 거리가 줄어든다",
             ha="center", fontsize=13, color=G)
    fig.tight_layout()
    return _save(fig, "paper_reverse.png")


# ------------------------------------------------------------------ 12. Sutskever Table 1
def s2s_table1():
    labs = ["단일 LSTM, 정방향 (빔 12)", "단일 LSTM, 역방향", "역방향 5개 앙상블, 빔 1",
            "역방향 5개 앙상블, 빔 2", "역방향 5개 앙상블, 빔 12", "Bahdanau et al. (당시 수치)"]
    vals = [26.17, 30.59, 33.00, 34.50, 34.81, 28.45]
    cols = [T2, T2, T, T, T, G]
    fig, ax = plt.subplots(figsize=(10, 5.4))
    y = np.arange(len(labs))[::-1]
    ax.barh(y, vals, color=cols, height=0.62)
    for yy, v in zip(y, vals):
        ax.text((v if abs(v - 33.3) > 0.6 else 33.3) + 0.3, yy, f"{v:.2f}", va="center", fontsize=16, fontweight="bold", color=D)
    ax.axvline(33.30, color=A, lw=2.4, ls="--")
    ax.text(33.55, len(labs) - 0.35, "구문 기반 SMT 기준선 33.30", ha="left", va="bottom", fontsize=14,
            color=A, fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=14)
    ax.set_xlim(20, 40.5)
    ax.set_ylim(-0.6, len(labs) + 0.2)
    ax.set_xlabel("BLEU (WMT'14 영→불 ntst14, 높을수록 좋다)", fontsize=15)
    ax.tick_params(axis="x", labelsize=13)
    fig.text(0.98, -0.05, "Sutskever et al. (2014) Table 1 기반", ha="right", fontsize=12, color=G)
    return _save(fig, "paper_s2s_table1.png")


# ------------------------------------------------------------------ 13. Cho 2014b Table 1(a)
def cho14b_table1():
    groups = ["전체 문장", "미등록어(UNK) 없는 문장"]
    data = {"RNNenc (게이트 RNN)": ([13.92, 23.45], T), "grConv": ([9.97, 18.22], P.get("MID", "#9CC5F2")),
            "Moses (구문 기반 SMT)": ([33.30, 35.63], G)}
    x = np.arange(2)
    w = 0.26
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    for k, (name, (v, c)) in enumerate(data.items()):
        xx = x + (k - 1) * w
        ax.bar(xx, v, w, color=c, label=name)
        for xi, vi in zip(xx, v):
            ax.text(xi, vi + 0.6, f"{vi:.2f}", ha="center", fontsize=14.5, fontweight="bold", color=D)
    ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=16)
    ax.set_ylabel("시험 BLEU", fontsize=15)
    ax.set_ylim(0, 54); ax.set_yticks(range(0, 41, 10)); ax.tick_params(axis="y", labelsize=13)
    ax.legend(fontsize=14, frameon=False, loc="upper left", ncol=3)
    ax.set_title("30단어 이하 문장쌍으로만 학습 · 입력 뒤집기 없음", fontsize=15, color=D, loc="left")
    fig.text(0.98, 0.0, "Cho et al. (2014b) Table 1(a) 기반", ha="right", fontsize=12, color=G)
    return _save(fig, "paper_cho14b_table1.png")


ALL = [elman_fig12, elman_tree, lstm1997, lstm2000, gers_growth, gers_table2, bengio_ppl, w2v_arch,
       w2v_table3, encdec_compare, reverse_dist, s2s_table1, cho14b_table1]

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for f in ALL:
        if not only or f.__name__ in only:
            f()
