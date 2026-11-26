"""Week 2 논문 그림 (독립 실행): build/assets/week2/*.png

논문 그림은 원본 이미지를 쓰지 않고 matplotlib 도식으로 새로 그린다.
모든 수치는 build/research/papers/week2.md 의 검산 값과 같아야 하며, 아래 assert로 확인한다.
사용: cd build && python paper_figs_w2.py
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
from matplotlib import font_manager as _fm  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402

_b = "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"
if os.path.exists(_b):
    _fm.fontManager.addfont(_b)
plt.rcParams["font.family"] = ["DejaVu Sans", "NanumGothic"]
plt.rcParams["font.size"] = 16
plt.rcParams["axes.labelsize"] = 17
plt.rcParams["xtick.labelsize"] = 15
plt.rcParams["ytick.labelsize"] = 15
plt.rcParams["legend.fontsize"] = 15
plt.rcParams["axes.unicode_minus"] = True

OUT = os.path.join(HERE, "assets", "week2")
os.makedirs(OUT, exist_ok=True)
TEAL, TEAL2, ACC, GRAY, DARK = P["TEAL"], P["TEAL2"], P["ACCENT"], P["GRAY"], P["DARK"]
MINT, MINT2, LINE, BG, MID, OFF = P["MINT"], P.get("MINT2"), P["LINE"], P.get("BG"), P.get("MID"), P.get("OFF")
ACC_MID = P.get("ACC_MID")
BLUES = LinearSegmentedColormap.from_list("theme_blues", ["#FFFFFF", MINT, MINT2, MID])
PTS = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)   # 노트의 순서 (0,0),(0,1),(1,0),(1,1)
SRC = dict(fontsize=12, color=GRAY, style="italic")


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)


def clean(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)


def scatter_labels(ax, y, pts=PTS, s=300):
    for (a, b), t in zip(pts, y):
        ax.scatter(a, b, s=s, zorder=5, color=ACC if t else "white", edgecolor=ACC if t else TEAL, lw=2.5,
                   marker="o" if t else "s")


def style(ax, lim=(-0.4, 1.4), title=None):
    ax.set_xlim(*lim); ax.set_ylim(*lim); ax.set_aspect("equal")
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xlabel("x₁"); ax.set_ylabel("x₂", rotation=0, labelpad=10)
    clean(ax)
    if title:
        ax.set_title(title, color=DARK, fontsize=18, fontweight="bold")


def shade_linear(ax, w, b, lim=(-0.4, 1.4)):
    g = np.linspace(*lim, 300)
    X, Y = np.meshgrid(g, g)
    Z = w[0] * X + w[1] * Y + b
    if np.allclose(w, 0):
        ax.add_patch(Rectangle((lim[0], lim[0]), lim[1] - lim[0], lim[1] - lim[0],
                               color=MINT if b >= 0 else "white", zorder=0))
        return
    ax.contourf(X, Y, (Z >= 0).astype(float), levels=[-0.5, 0.5, 1.5], colors=["white", MINT], zorder=0)
    ax.contour(X, Y, Z, levels=[0], colors=[TEAL], linewidths=2.8, zorder=1)


# ---------------------------------------------------------------- 1. Rosenblatt 1958: S → A → R
def fig_sar():
    rng = np.random.default_rng(3)
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    ax.set_xlim(0, 12.5); ax.set_ylim(-1.0, 6.4); ax.set_aspect("equal"); ax.axis("off")
    # S: 망막 6x6
    on = {(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (3, 1), (4, 1), (4, 2), (4, 3), (4, 4), (2, 4), (3, 4)}
    cs = 0.42
    sx, sy = 0.5, 1.4
    cells = []
    for i in range(6):
        for j in range(6):
            x, y = sx + j * cs, sy + (5 - i) * cs
            ax.add_patch(Rectangle((x, y), cs * 0.92, cs * 0.92, fc=TEAL if (i, j) in on else "white", ec=LINE, lw=1.2))
            cells.append((x + cs * 0.46, y + cs * 0.46))
    ax.text(sx + 3 * cs, 4.35, "S-points (망막)", ha="center", fontsize=18, color=DARK, fontweight="bold")
    ax.text(sx + 3 * cs, 0.85, "자극(빛 패턴)", ha="center", fontsize=15, color=GRAY)
    # A-units
    ay = np.linspace(0.5, 5.3, 8)
    ax_x = 6.0
    act = [1, 0, 1, 1, 0, 0, 1, 0]
    for k, y in enumerate(ay):
        for c in rng.choice(len(cells), 4, replace=False):
            ax.plot([cells[c][0], ax_x - 0.3], [cells[c][1], y], color=OFF if not act[k] else "#C7C7CC", lw=1.0, zorder=1)
    for k, y in enumerate(ay):
        ax.add_patch(Circle((ax_x, y), 0.28, fc=TEAL2 if act[k] else "white", ec=TEAL, lw=2, zorder=3))
    ax.text(ax_x, 5.85, "A-units (연합 세포)", ha="center", fontsize=18, color=DARK, fontweight="bold")
    ax.text(3.6, 4.95, "무작위 연결 · 고정", ha="center", fontsize=16, color=GRAY)
    ax.text(ax_x, -0.35, "임계값 θ 이상이면 발화 (0/1)", ha="center", fontsize=14, color=GRAY)
    # R-units
    rx = 10.2
    ry = [4.1, 1.7]
    for k, y in enumerate(ay):
        for j, r in enumerate(ry):
            if (k + j) % 2 == 0 or k in (2, 5):
                ax.plot([ax_x + 0.3, rx - 0.45], [y, r], color=ACC if act[k] and j == 0 else TEAL2,
                        lw=3.2 if act[k] and j == 0 else 1.4, alpha=1 if act[k] and j == 0 else 0.55, zorder=2)
    for j, (r, lab) in enumerate(zip(ry, ["R₁", "R₂"])):
        ax.add_patch(Circle((rx, r), 0.45, fc=ACC if j == 0 else "white", ec=ACC if j == 0 else TEAL, lw=2.5, zorder=3))
        ax.text(rx, r, lab, ha="center", va="center", fontsize=20, color="white" if j == 0 else DARK, zorder=4)
    ax.add_patch(FancyArrowPatch((rx + 0.75, 3.75), (rx + 0.75, 2.05), arrowstyle="<|-|>", mutation_scale=18,
                                 color=GRAY, lw=1.8, ls="--"))
    ax.text(rx + 0.95, 2.9, "상호\n억제", fontsize=14, color=GRAY, va="center")
    ax.text(rx, 5.85, "R-units (반응)", ha="center", fontsize=18, color=DARK, fontweight="bold")
    ax.text(8.1, 5.0, "학습: value V 강화", ha="center", fontsize=16, color=ACC, fontweight="bold")
    ax.text(rx, 0.75, "총 입력 Σ V·a가 큰\n반응이 이긴다", ha="center", fontsize=14, color=GRAY, va="top")
    ax.text(12.4, -0.95, "Rosenblatt (1958) Fig. 1–2 기반 재구성 (단순화)", ha="right", **SRC)
    save(fig, "w2p_sar.png")


# ---------------------------------------------------------------- 2. 오류 교정 규칙으로 AND 학습 (η=1)
def perceptron_run(y, epochs=100):
    w = np.zeros(2); b = 0.0; upd = 0; log = []; done = None
    for ep in range(1, epochs + 1):
        err = 0
        for x, t in zip(PTS, y):
            yh = int(w @ x + b >= 0)
            if yh != t:
                w = w + (t - yh) * x; b += (t - yh); upd += 1; err += 1
                log.append((upd, ep, w.copy(), b))
        if err == 0:
            done = ep
            break
    return upd, done, w, b, log


def fig_and_learning():
    y = [0, 0, 0, 1]
    upd, ep, w, b, log = perceptron_run(y)
    assert (upd, ep, tuple(w), b) == (11, 6, (2.0, 1.0), -3.0), (upd, ep, w, b)
    snaps = [log[1], log[4], log[7], log[10]]
    fig, axs = plt.subplots(1, 4, figsize=(17, 5.0))
    for ax, (k, e, ww, bb) in zip(axs, snaps):
        shade_linear(ax, ww, bb)
        scatter_labels(ax, y)
        acc = sum(int(ww @ x + bb >= 0) == t for x, t in zip(PTS, y))
        style(ax, title=f"{k}번째 갱신 후" + (" (끝)" if k == 11 else ""))
        tail = "다음 에폭(6) 오류 0" if k == 11 else f"에폭 {e}"
        ax.set_xlabel(f"w=({ww[0]:g}, {ww[1]:g}), b={bb:g}".replace("-", "−") + f"\n정답 {acc}/4 · {tail}",
                      fontsize=15, color=DARK)
        ax.set_ylabel("")
    fig.tight_layout(w_pad=2.0)
    save(fig, "w2p_and_learning.png")
    xor = perceptron_run([0, 1, 1, 0])
    assert xor[0] == 398 and xor[1] is None
    return upd, ep


# ---------------------------------------------------------------- 3. Novikoff 수렴 정리: 선형 하한 vs 제곱근 상한
def fig_novikoff():
    Xt = np.c_[PTS, np.ones(4)]
    t = np.array([-1, -1, -1, 1])
    u = np.array([1, 1, -1.5]); u = u / np.linalg.norm(u)
    gam = (t * (Xt @ u)).min(); R = np.linalg.norm(Xt, axis=1).max()
    kmax = (R / gam) ** 2
    assert abs(gam - 0.2425) < 1e-4 and abs(kmax - 51) < 1e-6
    # 실제 AND 학습 궤적(0/1 규칙 = ±1 규칙과 같은 갱신)
    _, _, _, _, log = perceptron_run([0, 0, 0, 1])
    ks = np.array([l[0] for l in log])
    proj = np.array([np.r_[l[2], l[3]] @ u for l in log])
    norm = np.array([np.linalg.norm(np.r_[l[2], l[3]]) for l in log])
    assert np.all(proj >= gam * ks - 1e-9) and np.all(norm <= R * np.sqrt(ks) + 1e-9)
    k = np.linspace(0, 64, 400)
    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    ax.plot(k, gam * k, color=TEAL, lw=3, label="해 방향 성분의 하한  γ·k   (선형으로 자람)")
    ax.plot(k, R * np.sqrt(k), color=ACC, lw=3, label="길이의 상한  R·√k   (제곱근으로만 자람)")
    ax.axvspan(kmax, 64, color=OFF, zorder=0)
    ax.axvline(kmax, color=GRAY, lw=1.5, ls="--")
    ax.text(kmax + 0.8, 1.2, "k > (R/γ)² = 51\n하한 > 상한 → 불가능", fontsize=15, color=DARK)
    ax.scatter(ks, proj, s=55, color=TEAL, zorder=5, label="실제 AND 학습: u·w (11번 갱신)")
    ax.scatter(ks, norm, s=55, color=ACC, marker="s", zorder=5, label="실제 AND 학습: ‖w‖")
    ax.set_xlim(0, 64); ax.set_ylim(0, 16)
    ax.set_xlabel("갱신 횟수 k"); ax.set_ylabel("크기")
    ax.legend(loc="upper left", frameon=False, fontsize=14)
    ax.grid(alpha=0.25); clean(ax)
    ax.text(64, -3.1, "Novikoff (1962) §IV 식 (5)(6)의 현대식 재서술 · AND, u ∝ (1, 1, −1.5)", ha="right", **SRC)
    save(fig, "w2p_novikoff.png")


# ---------------------------------------------------------------- 4. 차수 2 특징이면 XOR도 평면 하나
def fig_order2():
    fig = plt.figure(figsize=(8.6, 6.4))
    ax = fig.add_subplot(projection="3d")
    y = [0, 1, 1, 0]
    g = np.linspace(-0.2, 1.2, 12)
    X1, X2 = np.meshgrid(g, g)
    X3 = (X1 + X2 - 0.5) / 2          # x1 + x2 − 2·x3 = 0.5
    ax.plot_surface(X1, X2, X3, color=MID, alpha=0.30, edgecolor="none")
    for (a, b), tt in zip(PTS, y):
        c = a * b
        ax.scatter(a, b, c, s=260, color=ACC if tt else "white", edgecolor=ACC if tt else TEAL, lw=2.5,
                   marker="o" if tt else "s", depthshade=False)
        ax.text(a + 0.06, b + 0.06, c + 0.12, f"({a:g},{b:g})", fontsize=14, color=DARK)
    ax.set_xlabel("x₁", labelpad=8); ax.set_ylabel("x₂", labelpad=8); ax.set_zlabel("φ₃ = x₁·x₂", labelpad=10)
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1]); ax.set_zticks([0, 1])
    ax.view_init(elev=18, azim=-58)
    ax.set_title("x₁ + x₂ − 2·x₁x₂ = 0.5 (평면 하나)", color=DARK, fontsize=18, fontweight="bold")
    fig.text(0.98, 0.03, "PDP 8장 Table 2(p.320)의 착안을 그림으로", ha="right", **SRC)
    save(fig, "w2p_order2.png")


# ---------------------------------------------------------------- 5. 연결성(connectedness): 국소 창으로는 구별이 어렵다
def _spiral(n):
    """n×n 안에 한 칸 간격으로 감기는 사각 나선 경로(칸 목록)."""
    i, j = 0, 0
    path = [(0, 0)]
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    lens = [n - 1, n - 1, n - 1]
    m = n - 3
    while m > 0:
        lens += [m, m]
        m -= 2
    for k, L in enumerate(lens):
        di, dj = dirs[k % 4]
        for _ in range(L):
            i, j = i + di, j + dj
            path.append((i, j))
    return None, path


def fig_connected():
    n = 13
    _, path = _spiral(n)
    A = np.zeros((n, n)); B = np.zeros((n, n))
    for (i, j) in path:
        A[i, j] = 1; B[i, j] = 1
    # B: 경로 중간의 한 칸을 비워 두 조각으로
    cut = path[len(path) // 2]
    B[cut] = 0
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 5.9))
    for ax, M, tt in zip(axs, (A, B), ("한 덩어리 (연결됨)", "두 조각 (끊김 한 칸)")):
        ax.imshow(M, cmap=LinearSegmentedColormap.from_list("m", ["white", TEAL]), vmin=0, vmax=1)
        ax.set_xticks(np.arange(-0.5, n, 1), minor=True); ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
        ax.grid(which="minor", color=OFF, lw=0.8); ax.tick_params(which="both", length=0)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.set_title(tt, fontsize=19, color=DARK, fontweight="bold")
        # 국소 창 3×3 하나 표시
        ax.add_patch(Rectangle((1.5, 4.5), 3, 3, fill=False, ec=ACC, lw=3))
    axs[1].add_patch(Rectangle((cut[1] - 0.5, cut[0] - 0.5), 1, 1, fill=False, ec=ACC, lw=3, ls="--"))
    fig.text(0.5, 0.06, "주황 창(3×3)처럼 일부만 보는 특징은 두 그림에서 똑같이 반응한다 — '전체가 이어졌나'는 전역 성질",
             ha="center", fontsize=15, color=DARK)
    fig.text(0.98, 0.0, "Minsky & Papert (1969) 표지의 두 나선 도형에서 착안한 직관용 그림 (원문 그림 아님)", ha="right", **SRC)
    fig.subplots_adjust(bottom=0.14, top=0.9, wspace=0.12)
    save(fig, "w2p_connected.png")


# ---------------------------------------------------------------- 6. 보편 근사: 가파른 시그모이드 계단의 합
def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))


def stair(xs, N, k=1000.0):
    F = lambda x: np.sin(2 * np.pi * x)
    g = np.arange(N + 1) / N
    c = (g[:-1] + g[1:]) / 2
    G = F(0) * np.ones_like(xs)
    for i in range(1, N + 1):
        G = G + (F(g[i]) - F(g[i - 1])) * sigmoid(k * (xs - c[i - 1]))
    return G


def fig_ua():
    xs = np.linspace(0, 1, 200001)
    f = np.sin(2 * np.pi * xs)
    errs = {N: np.abs(stair(xs, N) - f).max() for N in (5, 20, 100)}
    assert [round(errs[N], 4) for N in (5, 20, 100)] == [0.5558, 0.1261, 0.0114], errs
    fig, axs = plt.subplots(1, 2, figsize=(14, 5.4), gridspec_kw=dict(width_ratios=[1.55, 1]))
    ax = axs[0]
    xp = np.linspace(0, 1, 4001)
    ax.plot(xp, np.sin(2 * np.pi * xp), color=DARK, lw=3, label="f(x) = sin 2πx")
    ax.plot(xp, stair(xp, 5), color=ACC, lw=2.5, label="은닉 5개")
    ax.plot(xp, stair(xp, 20), color=TEAL, lw=2.5, label="은닉 20개")
    ax.set_xlabel("x"); ax.set_ylabel("출력")
    ax.legend(frameon=False, loc="lower left"); ax.grid(alpha=0.25); clean(ax)
    ax.set_title("가파른 시그모이드 N개를 계단처럼 쌓기", fontsize=18, color=DARK, fontweight="bold")
    ax = axs[1]
    Ns = [5, 20, 100]
    bars = ax.bar([str(n) for n in Ns], [errs[n] for n in Ns], color=[ACC, TEAL, TEAL2], width=0.6)
    for bb, n in zip(bars, Ns):
        ax.text(bb.get_x() + bb.get_width() / 2, errs[n] + 0.015, f"{errs[n]:.3g}", ha="center", fontsize=17,
                color=DARK, fontweight="bold")
    ax.set_xlabel("은닉 유닛 수 N"); ax.set_ylabel("최대 오차")
    ax.set_ylim(0, 0.65); clean(ax)
    ax.set_title("유닛을 늘리면 오차가 준다", fontsize=18, color=DARK, fontweight="bold")
    fig.tight_layout(w_pad=3)
    fig.text(0.99, -0.02, "구성: σ(1000(x − c_k)), c_k = 구간 중점 — Cybenko (1989) Thm 2의 '존재'를 손으로 확인하는 예 (원문 그림 아님)",
             ha="right", **SRC)
    save(fig, "w2p_ua.png")
    return errs


# ---------------------------------------------------------------- 7. RHW 1986 대칭 검출망
W_L = np.array([14.2, -3.6, 7.2, -7.2, 3.6, -14.2])
W_R = np.array([-14.2, 3.6, -7.1, 7.1, -3.6, 14.2])


def symmetry_check():
    ok = 0; sym_min, asym_max = 1, 0
    for n in range(64):
        x = np.array([(n >> (5 - i)) & 1 for i in range(6)], float)
        h = sigmoid(np.array([W_L @ x - 1.1, W_R @ x - 1.1]))
        o = sigmoid(-8.8 * h.sum() + 6.4)
        sym = np.all(x == x[::-1])
        ok += int((o > 0.5) == sym)
        if sym:
            sym_min = min(sym_min, o)
        else:
            asym_max = max(asym_max, o)
    return ok, sym_min, asym_max


def fig_symmetry():
    ok, smin, amax = symmetry_check()
    assert ok == 64 and round(smin, 3) == 0.881 and round(amax, 3) == 0.156, (ok, smin, amax)
    fig, axs = plt.subplots(1, 2, figsize=(14.5, 5.6), gridspec_kw=dict(width_ratios=[1, 1.25]))
    ax = axs[0]
    ax.set_xlim(-0.6, 6.6); ax.set_ylim(-1.0, 4.6); ax.set_aspect("equal"); ax.axis("off")
    xin = np.arange(6) + 0.0
    for i, x in enumerate(xin):
        for j, hx in enumerate((1.6, 4.4)):
            w = (W_L if j == 0 else W_R)[i]
            ax.plot([x, hx], [0.6, 2.4], color=TEAL if w > 0 else ACC, lw=0.6 + abs(w) / 4, alpha=0.8)
        ax.add_patch(Circle((x, 0.45), 0.28, fc="white", ec=TEAL, lw=2, zorder=3))
        ax.text(x, -0.15, f"{i + 1}", ha="center", va="top", fontsize=15, color=GRAY)
    for j, hx in enumerate((1.6, 4.4)):
        ax.plot([hx, 3.0], [2.7, 3.85], color=ACC, lw=2.6)
        ax.add_patch(Circle((hx, 2.55), 0.32, fc=TEAL2, ec=TEAL, lw=2, zorder=3))
        ax.text(hx + (-0.5 if j == 0 else 0.5), 2.55, f"은닉 {j + 1}", ha="right" if j == 0 else "left", va="center", fontsize=14, color=DARK)
    ax.add_patch(Circle((3.0, 4.0), 0.32, fc=ACC, ec=ACC, zorder=3))
    ax.text(3.75, 4.0, "출력: 대칭?", fontsize=15, color=DARK, va="center")
    ax.text(3.0, -0.75, "입력 6칸 (0/1)   — 선 굵기 = |가중치|, 파랑 +, 주황 −", ha="center", fontsize=13, color=GRAY)
    ax = axs[1]
    pos = np.arange(1, 7)
    ax.bar(pos - 0.2, W_L, width=0.38, color=TEAL, label="은닉 1")
    ax.bar(pos + 0.2, W_R, width=0.38, color=TEAL2, label="은닉 2")
    for p, v in zip(pos, W_L):
        ax.text(p - 0.2, v + (0.6 if v > 0 else -1.6), f"{v:g}".replace("-", "−"), ha="center", fontsize=12.5, color=DARK)
    ax.axhline(0, color=GRAY, lw=1)
    ax.set_xticks(pos); ax.set_xlabel("입력 위치"); ax.set_ylabel("가중치")
    ax.set_ylim(-18, 18); clean(ax); ax.legend(frameon=False, loc="upper center", ncol=2)
    ax.set_title("거울 위치끼리 크기 같고 부호 반대 · 1 : 2 : 4", fontsize=17, color=DARK, fontweight="bold")
    fig.tight_layout(w_pad=2)
    fig.text(0.99, -0.03, "Rumelhart, Hinton & Williams (1986) Fig. 1 기반 재구성 — 가중치는 원문 그림의 값", ha="right", **SRC)
    save(fig, "w2p_symmetry.png")
    return ok, smin, amax


# ---------------------------------------------------------------- 8. 이 과정의 실험: ReLU MLP로 XOR
X4 = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
Y4 = np.array([[0], [1], [1], [0]], float)


def train_relu_xor(hidden, seed, lr=0.5, steps=3000):
    """ReLU 은닉층 + sigmoid 출력, 이진 cross-entropy, 전체 배치 경사하강법. 가중치 N(0,1), 편향 0."""
    rng = np.random.default_rng(seed)
    W1 = rng.normal(0, 1, (2, hidden)); b1 = np.zeros((1, hidden))
    W2 = rng.normal(0, 1, (hidden, 1)); b2 = np.zeros((1, 1))
    losses = []
    for _ in range(steps):
        Z = X4 @ W1 + b1; H = np.maximum(0, Z)
        p = sigmoid(H @ W2 + b2)
        losses.append(-np.mean(Y4 * np.log(p + 1e-9) + (1 - Y4) * np.log(1 - p + 1e-9)))
        d = (p - Y4) / 4
        gW2 = H.T @ d; gb2 = d.sum(0, keepdims=True)
        dZ = (d @ W2.T) * (Z > 0)
        W1 -= lr * (X4.T @ dZ); b1 -= lr * dZ.sum(0, keepdims=True); W2 -= lr * gW2; b2 -= lr * gb2
    params = (W1, b1, W2, b2)
    ok = bool(np.all((predict_relu(params, X4).ravel() > 0.5) == Y4.ravel().astype(bool)))
    return params, np.array(losses), ok


def predict_relu(params, X):
    W1, b1, W2, b2 = params
    return sigmoid(np.maximum(0, X @ W1 + b1) @ W2 + b2)


def fig_xor_relu():
    counts = {h: sum(train_relu_xor(h, s)[2] for s in range(20)) for h in (2, 4, 8)}
    assert counts == {2: 2, 4: 13, 8: 20}, counts
    seed = next(s for s in range(20) if train_relu_xor(4, s)[2])
    params, losses, _ = train_relu_xor(4, seed)
    fig, axs = plt.subplots(1, 2, figsize=(13.5, 5.4), gridspec_kw=dict(width_ratios=[1, 1.1]))
    ax = axs[0]
    g = np.linspace(-0.4, 1.4, 300)
    X, Y = np.meshgrid(g, g)
    Pp = predict_relu(params, np.c_[X.ravel(), Y.ravel()]).reshape(X.shape)
    ax.contourf(X, Y, Pp, levels=np.linspace(0, 1, 11), cmap=BLUES, alpha=0.9, zorder=0)
    ax.contour(X, Y, Pp, levels=[0.5], colors=[TEAL], linewidths=2.8)
    scatter_labels(ax, [0, 1, 1, 0], pts=X4)
    style(ax, title=f"학습된 2-4-1 ReLU MLP (seed {seed})")
    ax = axs[1]
    hs = [2, 4, 8]
    bars = ax.bar([f"은닉 {h}개" for h in hs], [counts[h] for h in hs], color=[ACC, TEAL2, TEAL], width=0.6)
    for bb, h in zip(bars, hs):
        ax.text(bb.get_x() + bb.get_width() / 2, counts[h] + 0.4, f"{counts[h]}/20", ha="center", fontsize=19,
                color=DARK, fontweight="bold")
    ax.set_ylim(0, 23); ax.set_ylabel("성공한 seed 수 (20개 중)"); clean(ax)
    ax.set_title("은닉 유닛이 많을수록 잘 찾는다", fontsize=18, color=DARK, fontweight="bold")
    fig.tight_layout(w_pad=3)
    fig.text(0.99, -0.03, "이 과정의 실험 (paper_figs_w2.py): ReLU · BCE · 전체 배치 GD lr 0.5 · 3000 step · N(0,1) 초기화 · seed 0–19",
             ha="right", **SRC)
    save(fig, "w2p_xor_relu.png")
    return counts, seed


# ---------------------------------------------------------------- 9. Bridle: 하드 max vs soft max
def fig_softmax():
    z = np.array([2.0, 1.0, 0.0])
    p = np.exp(z) / np.exp(z).sum()
    assert [round(v, 3) for v in p] == [0.665, 0.245, 0.090]
    hard = np.array([1.0, 0.0, 0.0])
    lab = ["고양이", "개", "새"]
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 5.0))
    ax = axs[0]
    bars = ax.bar(lab, hard, color=[ACC, OFF, OFF], width=0.6)
    for bb, v in zip(bars, hard):
        ax.text(bb.get_x() + bb.get_width() / 2, v + 0.03, f"{v:g}", ha="center", fontsize=18, color=DARK)
    ax.set_ylim(0, 1.2); ax.set_title("max (winner-take-all)", fontsize=19, color=DARK, fontweight="bold")
    ax = axs[1]
    bars = ax.bar(lab, p, color=[TEAL, TEAL2, MID], width=0.6)
    for bb, v in zip(bars, p):
        ax.text(bb.get_x() + bb.get_width() / 2, v + 0.03, f"{v:.3f}", ha="center", fontsize=18, color=DARK)
    ax.set_ylim(0, 1.2); ax.set_title("soft max (미분 가능)", fontsize=19, color=DARK, fontweight="bold")
    for a in axs:
        clean(a)
    fig.tight_layout(w_pad=2.5)
    fig.text(0.99, -0.03, "Bridle (1989/90) p.213의 설명을 그림으로 — z = [2, 1, 0]", ha="right", **SRC)
    save(fig, "w2p_softmax.png")


if __name__ == "__main__":
    fig_sar()
    print("AND:", fig_and_learning())
    fig_novikoff()
    fig_order2()
    fig_connected()
    print("UA errors:", fig_ua())
    print("symmetry:", fig_symmetry())
    print("XOR ReLU:", fig_xor_relu())
    fig_softmax()
    print("saved to", OUT)
