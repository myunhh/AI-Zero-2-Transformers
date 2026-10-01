"""Week 2 그림 생성: build/assets/week2/*.png"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deckkit import PALETTE_HEX as P, mpl_setup  # noqa: E402

plt = mpl_setup()
from matplotlib import font_manager as _fm  # noqa: E402
_b = "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"
if os.path.exists(_b):
    _fm.fontManager.addfont(_b)
# 수식 기호(ŷ, −, ᵀ, 아래첨자)는 DejaVu, 한글은 NanumGothic으로 대체
plt.rcParams["font.family"] = ["DejaVu Sans", "NanumGothic"]
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "week2")
os.makedirs(OUT, exist_ok=True)
TEAL, TEAL2, ACC, GRAY, DARK, MINT, LINE = (P[k] for k in ("TEAL", "TEAL2", "ACCENT", "GRAY", "DARK", "MINT", "LINE"))
PTS = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], float)
plt.rcParams["font.size"] = 13


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)


def scatter_labels(ax, y, s=260, show_xy=False):
    for (a, b), t in zip(PTS, y):
        ax.scatter(a, b, s=s, zorder=5, color=ACC if t else "white", edgecolor=ACC if t else TEAL, lw=2.5,
                   marker="o" if t else "s")


def style(ax, lim=(-0.4, 1.4), title=None):
    ax.set_xlim(*lim); ax.set_ylim(*lim); ax.set_aspect("equal")
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xlabel("x₁"); ax.set_ylabel("x₂", rotation=0, labelpad=10)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    if title:
        ax.set_title(title, color=DARK, fontsize=15, fontweight="bold")


def shade_linear(ax, w, b, lim=(-0.4, 1.4)):
    g = np.linspace(*lim, 300)
    X, Y = np.meshgrid(g, g)
    Z = (w[0] * X + w[1] * Y + b) >= 0
    ax.contourf(X, Y, Z.astype(float), levels=[-0.5, 0.5, 1.5], colors=["white", MINT], zorder=0)
    ax.contour(X, Y, (w[0] * X + w[1] * Y + b), levels=[0], colors=[TEAL], linewidths=2.5, zorder=1)


# ---------------------------------------------------------------- 1. perceptron diagram
def fig_perceptron():
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.6); ax.axis("off")
    ins = [("x₁", 4.3, "w₁"), ("x₂", 2.8, "w₂"), ("1", 1.3, "b")]
    for lab, y, wl in ins:
        ax.add_patch(Circle((1.0, y), 0.45, color=MINT, ec=TEAL, lw=2))
        ax.text(1.0, y, lab, ha="center", va="center", fontsize=18, color=DARK)
        ax.add_patch(FancyArrowPatch((1.5, y), (4.05, 2.8), arrowstyle="-|>", mutation_scale=18, color=TEAL2, lw=2))
        ly = {4.3: 3.85, 2.8: 3.0, 1.3: 1.75}[y]
        ax.text(2.55, ly, wl, fontsize=17, color=ACC, fontweight="bold", ha="center")
    ax.add_patch(Circle((4.6, 2.8), 0.6, color=TEAL, ec=TEAL))
    ax.text(4.6, 2.8, "Σ", ha="center", va="center", fontsize=26, color="white")
    ax.text(4.9, 1.45, "z = w₁x₁ + w₂x₂ + b", ha="center", fontsize=13, color=GRAY)
    ax.add_patch(FancyArrowPatch((5.2, 2.8), (6.35, 2.8), arrowstyle="-|>", mutation_scale=18, color=TEAL2, lw=2))
    ax.add_patch(FancyBboxPatch((6.4, 2.1), 1.5, 1.4, boxstyle="round,pad=0.05", fc=MINT, ec=TEAL, lw=2))
    t = np.linspace(-1, 1, 50)
    ax.plot(6.65 + (t + 1) * 0.5, 2.35 + (t >= 0) * 0.85, color=ACC, lw=3)
    ax.text(7.15, 3.75, "계단 함수", ha="center", fontsize=13, color=GRAY)
    ax.add_patch(FancyArrowPatch((7.95, 2.8), (8.9, 2.8), arrowstyle="-|>", mutation_scale=18, color=TEAL2, lw=2))
    ax.text(9.3, 2.8, "ŷ", ha="center", va="center", fontsize=22, color=DARK)
    ax.text(9.3, 2.1, "0 또는 1", ha="center", fontsize=12, color=GRAY)
    ax.text(5, 5.2, "ŷ = 1[ z ≥ 0 ]", ha="center", fontsize=19, color=DARK, fontweight="bold")
    save(fig, "perceptron.png")


# ---------------------------------------------------------------- 2. perceptron training on AND
def fig_perceptron_train():
    y = np.array([0, 0, 0, 1])
    w = np.zeros(2); b = 0.0; eta = 0.5
    snaps = []
    upd = 0
    for ep in range(20):
        err = 0
        for x, t in zip(PTS, y):
            yh = int(w @ x + b >= 0)
            if yh != t:
                w = w + eta * (t - yh) * x; b = b + eta * (t - yh); upd += 1; err += 1
                if upd in (2, 5, 8):
                    snaps.append((w.copy(), b, f"{upd}번 갱신 후"))
        if err == 0:
            break
    snaps.append((w.copy(), b, f"수렴: {upd}번 갱신"))
    fig, axs = plt.subplots(2, 2, figsize=(8.4, 8.2))
    for ax, (ww, bb, tt) in zip(axs.ravel(), snaps):
        if np.allclose(ww, 0):
            ax.add_patch(plt.Rectangle((-0.4, -0.4), 1.8, 1.8, color=MINT if bb >= 0 else "white", zorder=0))
        else:
            shade_linear(ax, ww, bb)
        scatter_labels(ax, y)
        acc = np.mean([(int(ww @ x + bb >= 0) == t) for x, t in zip(PTS, y)])
        style(ax, title=tt)
        ax.title.set_fontsize(17)
        # 네 패널 모두 같은 축이므로 x₁ 대신 상태 캡션을 축 이름 자리에 둔다
        ax.set_xlabel(f"w=({ww[0]:g},{ww[1]:g}), b={bb:g}\n정확도 {acc*100:.0f}%", fontsize=13, color=DARK,
                      labelpad=6)
    fig.tight_layout(h_pad=1.5, w_pad=1.5)
    save(fig, "perceptron_train.png")
    return snaps


# ---------------------------------------------------------------- 3. half-plane
def fig_halfplane():
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    w = np.array([1.0, 1.0]); b = -1.5
    lim = (-0.5, 2.0)
    shade_linear(ax, w, b, lim)
    ax.annotate("", xy=(1.25, 1.25), xytext=(0.75, 0.75),
                arrowprops=dict(arrowstyle="-|>", color=ACC, lw=3, mutation_scale=22))
    ax.text(1.28, 1.05, "w = (1, 1)\n(경계에 수직)", color=ACC, fontsize=13, fontweight="bold")
    ax.text(1.35, 1.75, "ŷ = 1 영역\nw·x + b ≥ 0", color=TEAL, fontsize=13, ha="center")
    ax.text(-0.42, -0.42, "ŷ = 0 영역\nw·x + b < 0", color=GRAY, fontsize=13)
    # 경계선(x₁+x₂=1.5)과 평행하게, 선에서 약 0.35 떨어뜨려 놓는다
    ax.text(0.72, 0.28, "경계: x₁ + x₂ − 1.5 = 0", color=TEAL, fontsize=13, fontweight="bold", rotation=-45,
            ha="center", va="center", rotation_mode="anchor")
    ax.set_xlim(*lim); ax.set_ylim(*lim); ax.set_aspect("equal")
    ax.set_xlabel("x₁"); ax.set_ylabel("x₂", rotation=0)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, "halfplane.png")


# ---------------------------------------------------------------- 4. AND / OR / XOR
def fig_and_or_xor():
    cfg = [("AND", [0, 0, 0, 1], (1, 1, -1.5)), ("OR", [0, 1, 1, 1], (1, 1, -0.5)), ("XOR", [0, 1, 1, 0], None)]
    fig, axs = plt.subplots(1, 3, figsize=(12.5, 4.5))
    for ax, (nm, y, wb) in zip(axs, cfg):
        if wb:
            shade_linear(ax, wb[:2], wb[2])
        else:
            g = np.linspace(-0.4, 1.4, 10)
            for (a, c, bb), ls in zip([(1, 1, -0.5), (1, 1, -1.5), (1, -1, 0.5)], ["--", ":", "-."]):
                ax.plot(g, (-a * g - bb) / c, color=GRAY, ls=ls, lw=1.8)
            ax.text(0.5, 0.5, "?", fontsize=40, color=ACC, ha="center", va="center", fontweight="bold")
        scatter_labels(ax, y)
        style(ax, title=nm + (" — 직선 한 개로 분리 가능" if wb else " — 어떤 직선도 실패"))
        ax.title.set_fontsize(13)
        if not wb:
            ax.title.set_color(ACC)
    fig.tight_layout()
    save(fig, "and_or_xor.png")


# ---------------------------------------------------------------- 5. XOR experiment: linear vs ReLU
def relu(z):
    return np.maximum(0, z)


def f_xor(x1, x2):
    s = x1 + x2
    return relu(s) - 2 * relu(s - 1)


def fig_xor_experiment():
    y = [0, 1, 1, 0]
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 5.0))
    ax = axs[0]
    shade_linear(ax, (1, 1), -0.5)
    scatter_labels(ax, y)
    for (a, b), t in zip(PTS, y):
        p = int(a + b - 0.5 >= 0)
        ax.text(a + 0.09, b + 0.1, f"예측 {p}", fontsize=12, color=ACC if p != t else DARK,
                fontweight="bold" if p != t else "normal")
    style(ax, title="선형: w₁=1, w₂=1, b=−0.5 → 3/4 정답")
    ax = axs[1]
    g = np.linspace(-0.4, 1.4, 400)
    X, Y = np.meshgrid(g, g)
    F = f_xor(X, Y)
    ax.contourf(X, Y, (F >= 0.5).astype(float), levels=[-0.5, 0.5, 1.5], colors=["white", MINT], zorder=0)
    ax.contour(X, Y, F, levels=[0.5], colors=[TEAL], linewidths=2.5)
    scatter_labels(ax, y)
    for (a, b), t in zip(PTS, y):
        ax.text(a + 0.09, b + 0.1, f"f={f_xor(a, b):g}", fontsize=12, color=DARK)
    style(ax, title="비선형: ReLU(s) − 2·ReLU(s−1), s = x₁+x₂ → 4/4")
    for a in axs:
        a.title.set_fontsize(13.5)
    fig.tight_layout()
    save(fig, "xor_experiment.png")


# ---------------------------------------------------------------- 6. hidden space
def fig_hidden():
    y = [0, 1, 1, 0]
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.9))
    scatter_labels(axs[0], y)
    style(axs[0], title="원래 공간 (x₁, x₂)")
    H = np.array([[relu(a + b), relu(a + b - 1)] for a, b in PTS])
    ax = axs[1]
    g = np.linspace(-0.3, 2.3, 300)
    X, Y = np.meshgrid(g, g)
    Z = X - 2 * Y - 0.5
    ax.contourf(X, Y, (Z >= 0).astype(float), levels=[-0.5, 0.5, 1.5], colors=["white", MINT], zorder=0)
    ax.contour(X, Y, Z, levels=[0], colors=[TEAL], linewidths=2.5)
    labs = ["(0,0)", "(1,0)·(0,1)", "", "(1,1)"]
    for (h1, h2), t, lb in zip(H, y, labs):
        ax.scatter(h1, h2, s=260, zorder=5, color=ACC if t else "white", edgecolor=ACC if t else TEAL, lw=2.5,
                   marker="o" if t else "s")
        if lb:
            ax.text(h1 - 0.05, h2 - 0.28 if lb.startswith("(1,0)") else h2 + 0.12, lb, fontsize=12, color=DARK,
                    ha="center" if lb.startswith("(1,0)") else "left")
    ax.text(1.55, 0.35, "h₁ − 2h₂ = 0.5", color=TEAL, fontsize=13, fontweight="bold", rotation=16)
    ax.set_xlim(-0.3, 2.3); ax.set_ylim(-0.3, 1.5); ax.set_aspect("equal")
    ax.set_xticks([0, 1, 2]); ax.set_yticks([0, 1])
    ax.set_xlabel("h₁ = ReLU(x₁+x₂)"); ax.set_ylabel("h₂ = ReLU(x₁+x₂−1)")
    ax.set_title("은닉 공간 (h₁, h₂) — 직선 하나로 분리", color=DARK, fontsize=15, fontweight="bold")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    save(fig, "hidden_space.png")


# ---------------------------------------------------------------- 7. trained numpy MLP on XOR
def train_xor(hidden=4, seed=0, lr=0.5, steps=3000):
    rng = np.random.default_rng(seed)
    X = PTS; Y = np.array([[0], [1], [1], [0]], float)
    W1 = rng.normal(0, 1, (2, hidden)); b1 = np.zeros((1, hidden))
    W2 = rng.normal(0, 1, (hidden, 1)); b2 = np.zeros((1, 1))
    losses = []
    for _ in range(steps):
        Z = X @ W1 + b1; H = np.tanh(Z)
        logit = H @ W2 + b2; p = 1 / (1 + np.exp(-logit))
        loss = -np.mean(Y * np.log(p + 1e-9) + (1 - Y) * np.log(1 - p + 1e-9))
        losses.append(loss)
        d = (p - Y) / len(X)
        gW2 = H.T @ d; gb2 = d.sum(0, keepdims=True)
        dH = d @ W2.T; dZ = dH * (1 - H ** 2)
        gW1 = X.T @ dZ; gb1 = dZ.sum(0, keepdims=True)
        W1 -= lr * gW1; b1 -= lr * gb1; W2 -= lr * gW2; b2 -= lr * gb2
    return (W1, b1, W2, b2), np.array(losses)


def predict(params, X):
    W1, b1, W2, b2 = params
    return 1 / (1 + np.exp(-(np.tanh(X @ W1 + b1) @ W2 + b2)))


def fig_trained():
    params, losses = train_xor(seed=1)
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.8), gridspec_kw=dict(width_ratios=[1, 1.15]))
    ax = axs[0]
    g = np.linspace(-0.4, 1.4, 300)
    X, Y = np.meshgrid(g, g)
    Pp = predict(params, np.c_[X.ravel(), Y.ravel()]).reshape(X.shape)
    cf = ax.contourf(X, Y, Pp, levels=np.linspace(0, 1, 11), cmap="GnBu", alpha=0.55, zorder=0)
    ax.contour(X, Y, Pp, levels=[0.5], colors=[TEAL], linewidths=2.5)
    scatter_labels(ax, [0, 1, 1, 0])
    pp = predict(params, PTS).ravel()
    for (a, b), v in zip(PTS, pp):
        ax.text(a + 0.08, b + 0.1, f"p={v:.2f}", fontsize=11.5, color=DARK)
    style(ax, title="학습된 2-4-1 MLP의 결정 경계")
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04); cb.set_label("p(y=1)")
    ax = axs[1]
    ax.plot(losses, color=ACC, lw=2.5)
    ax.set_xlabel("step"); ax.set_ylabel("BCE loss")
    ax.set_title("손실 곡선 (경사하강법, lr=0.5)", color=DARK, fontsize=15, fontweight="bold")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    save(fig, "mlp_trained.png")
    # 여러 seed 성공률 (노트용)
    ok = {}
    for hdim in (2, 4):
        s = 0
        for seed in range(20):
            prm, _ = train_xor(hidden=hdim, seed=seed)
            s += int(np.all((predict(prm, PTS).ravel() > 0.5) == np.array([0, 1, 1, 0], bool)))
        ok[hdim] = s
    return pp, losses[0], losses[-1], ok


# ---------------------------------------------------------------- 8. computation graph (tiny MLP)
def fig_graph():
    fig, ax = plt.subplots(figsize=(12.2, 4.9))
    ax.set_xlim(0, 12.7); ax.set_ylim(0, 5.3); ax.axis("off")
    nodes = [("x", 1.0, "[1, 1]", "입력"), ("z", 3.8, "[1.5, −0.5]", "z = xW$_1$+b$_1$"), ("h", 6.6, "[1.5, 0]", "h = ReLU(z)"),
             ("ŷ", 9.2, "3", "ŷ = hW$_2$+b$_2$"), ("L", 11.7, "0.5", "L = ½(ŷ−y)$^2$")]
    grads = {"z": "[2, 0]", "h": "[2, 1]", "ŷ": "1", "L": "1"}
    for nm, x, fv, lab in nodes:
        ax.add_patch(FancyBboxPatch((x - 0.95, 2.05), 1.9, 1.2, boxstyle="round,pad=0.05", fc=MINT, ec=TEAL, lw=2))
        ax.text(x, 2.88, nm, ha="center", va="center", fontsize=23, color=TEAL, fontweight="bold")
        ax.text(x, 2.38, fv, ha="center", va="center", fontsize=16, color=DARK)
        ax.text(x, 3.55, lab, ha="center", fontsize=15, color=GRAY)
        if nm in grads:
            ax.text(x, 1.35, f"∂L/∂{nm} = {grads[nm]}", ha="center", fontsize=16, color=ACC, fontweight="bold")
    for (a, xa, *_), (b, xb, *_) in zip(nodes[:-1], nodes[1:]):
        ax.add_patch(FancyArrowPatch((xa + 1.0, 2.95), (xb - 1.0, 2.95), arrowstyle="-|>", mutation_scale=18, color=TEAL2, lw=2.2))
        ax.add_patch(FancyArrowPatch((xb - 1.0, 2.3), (xa + 1.0, 2.3), arrowstyle="-|>", mutation_scale=18, color=ACC, lw=1.8, ls="--"))
    ax.text(2.4, 4.3, "W₁=[[1,−1],[0.5,0.5]], b₁=0", fontsize=15, color=DARK, ha="center")
    ax.text(7.9, 4.3, "W₂=[[2],[1]], b₂=0", fontsize=15, color=DARK, ha="center")
    ax.text(11.7, 4.3, "정답 y = 2", fontsize=15, color=DARK, ha="center")
    ax.text(6.35, 0.45, "∂L/∂W₂ = hᵀ·1 = [[1.5],[0]]      ∂L/∂W₁ = xᵀ·[2, 0] = [[2, 0],[2, 0]]", ha="center",
            fontsize=16, color=ACC, fontweight="bold")
    ax.text(0.0, 5.0, "→ forward(값)", color=TEAL2, fontsize=15, fontweight="bold")
    ax.text(3.2, 5.0, "⇠ backward(gradient)", color=ACC, fontsize=15, fontweight="bold")
    save(fig, "graph.png")


# ---------------------------------------------------------------- 9. activations
def fig_act():
    z = np.linspace(-5, 5, 400)
    sig = 1 / (1 + np.exp(-z))
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.6))
    ax = axs[0]
    ax.plot(z, sig, color=TEAL2, lw=3, label="sigmoid")
    ax.plot(z, np.tanh(z), color=GRAY, lw=2.5, ls="--", label="tanh")
    ax.plot(z, relu(z), color=ACC, lw=3, label="ReLU")
    ax.set_ylim(-1.2, 3); ax.set_title("활성화 함수 σ(z)", color=DARK, fontsize=15, fontweight="bold")
    ax = axs[1]
    ax.plot(z, sig * (1 - sig), color=TEAL2, lw=3, label="sigmoid′ (최대 0.25)")
    ax.plot(z, 1 - np.tanh(z) ** 2, color=GRAY, lw=2.5, ls="--", label="tanh′ (최대 1)")
    zz = np.where(z > 0, 1.0, 0.0)
    ax.plot(z[z < 0], zz[z < 0], color=ACC, lw=3); ax.plot(z[z > 0], zz[z > 0], color=ACC, lw=3, label="ReLU′ (0 또는 1)")
    # 범례가 ReLU′ = 1 선 위에 겹치지 않도록 위쪽 여백을 둔다
    ax.set_ylim(-0.1, 1.75); ax.set_yticks([0, 0.5, 1.0])
    ax.set_title("도함수 σ′(z) — gradient에 곱해지는 값", color=DARK, fontsize=15, fontweight="bold")
    for ax, loc in zip(axs, ("upper left", "upper right")):
        ax.axhline(0, color=LINE, lw=1); ax.axvline(0, color=LINE, lw=1)
        ax.legend(frameon=False, fontsize=11.5, loc=loc); ax.set_xlabel("z")
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.tight_layout()
    save(fig, "activations.png")


if __name__ == "__main__":
    fig_perceptron()
    print("perceptron snaps:", fig_perceptron_train())
    fig_halfplane(); fig_and_or_xor(); fig_xor_experiment(); fig_hidden()
    print("trained:", fig_trained())
    fig_graph(); fig_act()
    print(sorted(os.listdir(OUT)))
