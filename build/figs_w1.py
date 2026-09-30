"""Week 1 추가 그림: 공부 시간 → 점수 예제 (y = 2x + 1)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from deckkit import mpl_setup, HEX
plt = mpl_setup()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "week1")
x = np.array([1., 2., 3., 4.]); y = np.array([3., 5., 7., 9.])

# 경사하강법 (PyTorch 슬라이드와 같은 설정: w=b=0, lr=0.05)
w, b, lr = 0.0, 0.0, 0.05
hist = {}
losses = []
for step in range(501):
    yh = w * x + b
    L = np.mean((yh - y) ** 2)
    losses.append(L)
    if step in (0, 1, 2, 500):
        hist[step] = (w, b, L)
    gw = np.mean(2 * (yh - y) * x); gb = np.mean(2 * (yh - y))
    w -= lr * gw; b -= lr * gb

# 1) 데이터만
fig, ax = plt.subplots(figsize=(5.2, 4.2))
ax.scatter(x, y, s=90, color=HEX["ORANGE"], zorder=3)
for xi, yi in zip(x, y):
    ax.annotate(f"({xi:.0f}, {yi:.0f})", (xi, yi), textcoords="offset points", xytext=(8, -14), fontsize=11, color=HEX["INK"])
ax.set_xlim(0, 5); ax.set_ylim(0, 11)
ax.set_xlabel("공부 시간 x (시간)", fontsize=12); ax.set_ylabel("점수 y", fontsize=12)
ax.set_title("규칙을 모르는 채로 받은 데이터 4개", fontsize=13, color=HEX["TEAL"])
ax.grid(alpha=0.25)
fig.savefig(os.path.join(OUT, "data_scatter.png")); plt.close(fig)

# 2) 학습 과정
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
a1.scatter(x, y, s=80, color=HEX["ORANGE"], zorder=3, label="데이터")
xs = np.linspace(0, 5, 50)
cols = {0: "#B8C4CC", 1: HEX["SKY"], 2: HEX["CYAN"], 500: HEX["TEAL"]}
for st, (ww, bb, LL) in hist.items():
    a1.plot(xs, ww * xs + bb, color=cols[st], lw=2.5 if st == 500 else 1.8,
            label=f"step {st}: w={ww:.2f}, b={bb:.2f}")
a1.set_xlim(0, 5); a1.set_ylim(-0.5, 11); a1.grid(alpha=0.25)
a1.set_xlabel("공부 시간 x"); a1.set_ylabel("점수"); a1.legend(fontsize=9.5, loc="upper left")
a1.set_title("직선이 데이터 쪽으로 이동한다", color=HEX["TEAL"], fontsize=13)
a2.plot(range(501), losses, color=HEX["TEAL"], lw=2)
a2.set_yscale("log"); from matplotlib.ticker import FuncFormatter; a2.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}")); a2.set_xlabel("step"); a2.set_ylabel("손실 L (MSE, log 눈금)")
a2.set_title("손실은 계속 줄어든다", color=HEX["TEAL"], fontsize=13); a2.grid(alpha=0.25)
for st in (0, 1, 2):
    a2.scatter([st], [losses[st]], color=cols[st] if st else "#8A99A3", zorder=3)
    a2.annotate(f"{losses[st]:.2f}", (st, losses[st]), textcoords="offset points", xytext=(8, 4), fontsize=10)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fit_progress.png")); plt.close(fig)
print({k: tuple(round(v, 3) for v in t) for k, t in hist.items()})
