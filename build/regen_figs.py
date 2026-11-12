"""모든 그림을 그림별 글자 크기 배율로 다시 만든다.

그림은 슬라이드에 넣을 때 축소되므로, 원래 스크립트의 글자 크기에 배율을 곱해
투영 화면에서도 읽히게 한다. 글자가 빽빽한 도식은 겹치지 않도록 배율을 낮게 둔다.
사용: python regen_figs.py [week2_figs.py ...]  (인자를 주면 그 스크립트의 그림만)
"""
import os
import runpy
import sys

import matplotlib
matplotlib.use("Agg")
from matplotlib.font_manager import FontProperties

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = 1.45
SCALE = {"derivative": 1.3, "qkv": 1.25, "fig_graph": 1.15, "fig_perceptron": 1.1, "fig_xor_experiment": 1.1,
         "fig_trained": 1.2, "fig_alexnet": 1.1, "fig_norm_axes": 1.0, "fig_degradation": 1.15, "grad_decay": 1.2,
         "lstm_cell": 1.05, "onehot_lookup": 1.1, "seq2seq": 1.15, "fig_bottleneck": 1.2, "fig_mha": 1.1,
         "fig_qkv": 1.25, "fig_archs": 1.2, "fig_postpre": 1.25, "fig_shift": 1.1, "fig_encdec": 1.0,
         "fig_kv": 1.0, "fig_vit": 1.0, "fig_genealogy": 1.0, "fig_ln_axis": 1.0}
_cur = [DEFAULT]
_orig = FontProperties.get_size_in_points
FontProperties.get_size_in_points = lambda self: _orig(self) * _cur[0]

MODULES = {"week1_assets.py": ["tensor_ranks", "batch_axis", "broadcasting", "matmul_shape", "batched_matmul",
                               "dot_scores", "softmax_temp", "derivative", "ce_curve", "gd_paths", "generalization"],
           "week2_figs.py": ["fig_perceptron", "fig_perceptron_train", "fig_halfplane", "fig_and_or_xor",
                             "fig_xor_experiment", "fig_hidden", "fig_trained", "fig_graph", "fig_act"],
           "week3_figs.py": ["fig_image_tensor", "fig_conv_sliding", "fig_params", "fig_pool", "fig_receptive",
                             "fig_lenet", "fig_equivariance", "fig_svm", "fig_kernel", "fig_alexnet", "fig_relu_grad",
                             "fig_ilsvrc", "fig_degradation", "fig_residual", "fig_norm_axes"],
           "assets/week4/make_figs.py": ["onehot_lookup", "analogy", "rnn_unrolled", "grad_decay", "lstm_cell",
                                         "seq2seq"],
           "week5_assets.py": ["fig_bottleneck", "fig_alignment", "fig_arch", "fig_pe", "fig_qkv", "fig_setup",
                               "fig_pipeline", "fig_causal", "fig_sqrt", "fig_mha", "fig_heads"],
           "week6_figs.py": ["fig_ln_axis", "fig_postpre", "fig_shift", "fig_causal", "fig_encdec", "fig_lr", "fig_kv",
                             "fig_mem", "fig_flops", "fig_archs", "fig_vit", "fig_genealogy"]}

ONLY = set(sys.argv[1:])
sys.path.insert(0, HERE)
import deckkit  # noqa: E402
# clean(Apple) 테마로 바꾼 주차의 그림 — 테마 전환은 되돌릴 수 없으므로 마지막에 그린다
CLEAN = {"week1_assets.py", "figs_w1.py", "week2_figs.py", "week3_figs.py", "assets/week4/make_figs.py"}
order = sorted(MODULES.items(), key=lambda kv: kv[0] in CLEAN)
for script, funcs in order:
    if script in CLEAN and deckkit.STYLE != "apple":
        deckkit.use_theme("clean")
    if ONLY and script not in ONLY and os.path.basename(script) not in ONLY:
        continue
    path = os.path.join(HERE, script)
    cwd = os.getcwd()
    os.chdir(os.path.dirname(path))
    try:
        g = runpy.run_path(path, run_name="figmod")
        for f in funcs:
            _cur[0] = SCALE.get(f, DEFAULT)
            g[f]()
            print(f"{script}:{f} x{_cur[0]}")
    finally:
        os.chdir(cwd)

if not ONLY or "figs_w1.py" in ONLY:
    deckkit.use_theme("clean")
    _cur[0] = 1.3
    runpy.run_path(os.path.join(HERE, "figs_w1.py"), run_name="__main__")

# 1주차 도착점 슬라이드는 5주차 구조도를 쓰므로 clean 색으로 사본을 따로 그린다 (5주차 원본은 그대로 둔다)
if not ONLY or "figs_w1.py" in ONLY or "week1_assets.py" in ONLY:
    import shutil
    deckkit.use_theme("clean")
    w5 = os.path.join(HERE, "assets", "week5", "transformer_arch.png")
    keep = w5 + ".keep"
    shutil.copy(w5, keep)
    cwd = os.getcwd()
    os.chdir(HERE)
    try:
        _cur[0] = SCALE.get("fig_arch", DEFAULT)
        runpy.run_path(os.path.join(HERE, "week5_assets.py"), run_name="figmod")["fig_arch"]()
    finally:
        os.chdir(cwd)
    shutil.move(w5, os.path.join(HERE, "assets", "week1", "transformer_arch.png"))
    shutil.move(keep, w5)
    print("week1/transformer_arch.png (clean copy of week5 fig_arch)")
