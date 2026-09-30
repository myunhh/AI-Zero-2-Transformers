"""Week 6 — Transformer 완성: 학습·추론·그 이후.
실행: python build/week6_figs.py && python build/week6.py -> lectures/week06_transformer_complete.pptx
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from deckkit import *  # noqa: E402,F401
from deckkit import _set_run_font, _no_bullet  # noqa: E402

A = os.path.join(HERE, "assets", "week6")
OUT = os.path.join(HERE, "..", "lectures", "week06_transformer_complete.pptx")


def img(name):
    return os.path.join(A, name)


d = Deck(week=6, title="Transformer 완성: 학습·추론·그 이후",
         subtitle="AI Zero 2 Transformer · 6주차 (과정 마무리)", date="2026-11-09")


# ------------------------------------------------------------------ helpers (deckkit 조합)
def fbox(s, x, y, w, h, lines, size=20):
    """고정폭 수식 상자."""
    d.box(s, x, y, w, h, fill=CODE_BG, line=LINE)
    tb = s.shapes.add_textbox(Inches(x + 0.15), Inches(y + 0.05), Inches(w - 0.3), Inches(h - 0.1))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(4)
        _no_bullet(p)
        r = p.add_run()
        r.text = ln
        _set_run_font(r, size=size, bold=True, color=DARK, mono=True)
    return tb


def panel(s, x, y, w, h, head, body, accent=False, size=15, bullets=True):
    d.box(s, x, y, w, h, fill=ACCENT_BG if accent else MINT)
    d.text(s, x + 0.2, y + 0.1, w - 0.4, 0.5, head, size=16, bold=True,
           color=ACCENT if accent else TEAL, anchor="m")
    d.text(s, x + 0.2, y + 0.65, w - 0.35, h - 0.75, body, size=size, bullets=bullets, min_size=10,
           para_gap=0.35)


# ================================================================== 도입
d.cards("지난 주 복습: Attention의 핵심", [
    {"head": "Attention = 가중합", "tag": "병목 해소",
     "body": ["점수 → Softmax → Value 가중합", "출력 위치마다 입력 전체를 다시 참조", "고정 문맥 벡터 하나의 병목을 푼다", "가중치 A는 입력마다 계산되는 값"]},
    {"head": "Q · K · V 투영", "tag": "역할 분리",
     "body": ["같은 X라도 W_Q, W_K, W_V가 다르다", "`softmax(QKᵀ/√dₕ)·V`", "√dₕ로 점수 분산 조절", "Softmax는 Key 축(마지막 축)"]},
    {"head": "Multi-head", "tag": "dₕ = d/H",
     "body": ["특징 투영을 H개로 나눈다", "각 head는 **전체 위치**를 처리", "concat → W_O로 다시 d차원", "H를 늘려도 d가 같으면 dₕ만 줄어듦"]},
    {"head": "Shape 추적", "tag": "d=8, H=2, N=5", "accent": True,
     "body": ["X `(B,5,8)` → Q `(B,2,5,4)`", "QKᵀ `(B,2,5,5)`: Query×Key 표", "합치기 → `(B,5,8)`: 길이·폭 유지", "Cross: 출력 길이 = Query 길이"]},
], lead="5주차: 고정 벡터 병목 → Attention → Transformer의 핵심 연산",
    footer="오늘: 이 블록에 FFN·Residual·Norm·Mask를 붙여 학습·추론까지 완성한다",
    notes="지난 주에는 Seq2Seq의 고정 문맥 벡터 병목에서 출발해 Attention을 가중합으로 이해했고, Q/K/V 투영과 "
          "Multi-head의 shape를 d=8, H=2, N=5 예시로 추적했습니다. 오늘은 그 Attention 블록이 실제 Transformer가 되기 "
          "위해 필요한 나머지 부품(FFN, Residual, LayerNorm, Mask)과 학습·추론 절차를 완성합니다. "
          "시작 전에 학생에게 QKᵀ의 shape와 Softmax 축을 한 번 더 말하게 하면 좋습니다.")

d.timeline("오늘의 위치: 2017년 원형과 그 이후", [
    (2014, "Attention", "Bahdanau 등: 정렬과 문맥 가중합"),
    (2015, "ResNet", "잔차 연결로 깊은 모델 최적화"),
    (2016, "LayerNorm", "특징 축 정규화 (Ba 등)"),
    (2017, "Transformer", "Attention·FFN·잔차·정규화·위치 정보의 조합"),
    (2018, "BERT · GPT", "Encoder-only / Decoder-only 사전학습"),
    (2020, "ViT · Pre-LN", "이미지 patch를 token으로 / 정규화 위치 분석"),
    (2022, "FlashAttn · DiT", "IO 효율 exact attention / Diffusion + Transformer"),
], highlight=[3], lead="6주차는 2017년 원형을 완성하고, 이후 갈래를 '비교하는 틀'로 연결한다",
    notes="5주차까지는 2014년 Attention에서 2017년 Transformer의 핵심 연산까지 왔습니다. 오늘은 2017년 원형의 블록을 "
          "끝까지 조립하고 학습·추론을 다룬 뒤, 2018년 BERT·GPT, 2020년 ViT와 Pre-LN 분석(Xiong 등), 2022년 "
          "FlashAttention과 DiT(arXiv 2022, ICCV 2023)로 이어지는 길을 봅니다. 이후 연구는 최신 순위표가 아니라 원형과 "
          "무엇이 달라졌는지 비교하는 틀로만 다룬다는 점을 먼저 밝힙니다.")

d.cards("학습 목표", [
    {"head": "블록 완성", "body": "FFN·Residual·LayerNorm의 역할과 Post-LN / Pre-LN의 차이를 설명한다"},
    {"head": "누출 없는 학습", "body": "Target shift와 causal mask(−∞)를 이해하고 세 종류 mask를 구분한다"},
    {"head": "조립과 계산", "body": "Encoder·Decoder 층의 shape를 추적하고 파라미터 수 ≈ 4d²+2d·d_ff를 유도한다"},
    {"head": "학습 recipe", "body": "NLL 손실, 학습 step 순서, 원논문 학습 조건과 평가 지표를 설명한다"},
    {"head": "추론과 효율", "body": "자기회귀 생성, KV Cache, 연산량과 메모리를 따로 계산한다"},
    {"head": "실험과 그 이후", "accent": True,
     "body": "작은 Transformer 실험을 설계하고 BERT·GPT·ViT·DiT를 원형과 비교한다"},
], numbered=True,
    notes="오늘 목표는 여섯 가지입니다. 앞의 다섯은 2017년 원형 Transformer를 입력부터 다음 토큰까지 완전히 설명하는 것이고, "
          "마지막은 그 지식을 실험과 후속 모델 읽기로 옮기는 것입니다. 수업 끝에 빈 종이에 전체 구조를 그리는 과제로 "
          "목표 달성 여부를 확인합니다.")

# ================================================================== Part 01
d.section("01", "블록 완성: FFN · Residual · Norm · Mask",
          "Attention이 전부가 아니다 — 위치별 변환, 깊은 계산의 기반, 정답 누출 방지",
          notes="첫 파트에서는 Attention 주변의 부품을 채웁니다. FFN, Residual, LayerNorm으로 한 블록을 완성하고, "
                "Decoder 학습에 꼭 필요한 target shift와 mask를 다룹니다. 원자료 14–15장에 해당합니다.")

d.formula("FFN: 위치별 비선형 변환", "FFN(x) = max(0, x·W₁ + b₁)·W₂ + b₂",
          parts=[("x", "한 위치의 d차원 벡터 (행벡터 관례)"),
                 ("W₁ (d×d_ff)", "확장: 원형 Base 512 → 2048"),
                 ("max(0,·)", "ReLU 비선형성 — 없으면 두 선형층이 하나로 합쳐진다"),
                 ("W₂ (d_ff×d)", "축소: 다시 d=512 → residual과 더할 수 있다")],
          example=["파라미터 ≈ 2·d·d_ff = 2·512·2048 ≈ **2.1M**",
                   "모든 위치에 같은 W₁, W₂ / 층마다는 별도",
                   "**Attention A·V**: 위치 간 정보 결합",
                   "**Q/K/V, W_O**: 특징 공간 선형 투영",
                   "**FFN**: 위치별 특징 변환, 길이 유지"],
          lead="모인 정보를 각 위치에서 비선형적으로 바꾼다 [22 §3.3]",
          takeaway="Attention = token mixing, FFN = feature transformation (단, 투영도 특징을 바꾼다)",
          notes="FFN은 각 위치에 똑같이 적용되는 2층 MLP입니다. d=512를 d_ff=2048로 넓혔다가 다시 512로 줄이는데, "
                "마지막이 d로 돌아와야 residual 합이 가능합니다. FFN 자체는 위치 간 결합을 하지 않지만, 입력 x가 이미 "
                "Attention을 거쳐 다른 토큰 정보를 담고 있을 수 있습니다. '토큰 믹싱 vs 특징 변환'은 첫 설명으로 좋지만 "
                "Q/K/V 투영도 특징을 바꾼다는 점을 함께 말해 줍니다.")

# --- LayerNorm (custom)
s = d.blank("LayerNorm은 어느 축을 정규화하나",
            notes="LayerNorm(d)는 (B,N,d) 입력에서 각 토큰의 마지막 d축으로 평균과 분산을 구합니다. BatchNorm처럼 배치 전체의 "
                  "같은 특징을 묶지 않습니다. x=(1,2,3,4)로 손계산하면 평균 2.5, 분산 1.25이고 정규화 결과는 약 ±1.34, ±0.45입니다. "
                  "γ=2, β=1을 적용하면 평균 1, 분산 4가 되므로 최종 출력이 항상 평균 0·분산 1일 필요는 없습니다. "
                  "γ, β는 토큰마다 따로 있는 것이 아니라 특징 축에 공유됩니다. [20][30]")
d.lead(s, "토큰 하나 x ∈ ℝᵈ의 d개 특징으로 평균·분산을 구한다 — Batch·sequence 전체가 아니다")
d._image_fit(s, img("ln_axis.png"), X0, 1.8, 6.6, 3.35)
d.text(s, X0, 5.25, 6.6, 1.7, [
    "**γ, β**: 학습되는 scale·shift — 특징 축에 공유 (토큰마다 별개 아님)",
    "**ε**: 0으로 나누는 수치 문제 완화",
    "그림의 주황 칸 = 평균·분산을 함께 계산하는 묶음"], size=15, bullets=True, min_size=11)
fbox(s, 7.4, 1.8, X1 - 7.4, 1.7, ["μ = (1/d)·Σ x_r", "σ² = (1/d)·Σ (x_r − μ)²",
                                  "LN(x) = γ⊙(x − μ)/√(σ² + ε) + β"], size=15)
panel(s, 7.4, 3.65, X1 - 7.4, 3.3, "숫자로 확인: x = (1, 2, 3, 4)", [
    "μ = 2.5,  σ² = 1.25",
    "정규화 → (−1.34, −0.45, 0.45, 1.34)",
    "γ=1, β=0 → 평균 0 · 분산 ≈ 1",
    "γ=2, β=1 → (−1.68, 0.11, 1.89, 3.68) → 평균 1 · 분산 ≈ 4",
    "→ 최종 출력이 항상 평균 0·분산 1은 아니다"], accent=True, size=15)

d.image("Residual과 Post-LN vs Pre-LN", img("postpre_ln.png"),
        lead="잔차 y = x + Dropout(F(x)) — 정규화를 어디에 두느냐가 다르다",
        side={"head": "기억할 것", "body": [
            "잔차 합은 원소별 덧셈 → 입력과 F(x)의 **shape가 같아야** 한다 (각 sublayer가 d로 복귀)",
            "잔차는 깊은 모델의 최적화를 돕지만 모든 설정의 안정성을 보장하는 마법은 아니다 [19]",
            "원형은 **Post-LN**. Pre-LN은 Norm을 sublayer 입력 안으로 옮기고 stack 끝에 최종 Norm을 두는 경우가 많다",
            "정규화 위치는 초기 gradient·학습 안정성에 영향 (Xiong 등 2020) — 비교 시 optimizer·학습률·warm-up·깊이를 통제 [25]"]},
        img_w_ratio=0.52,
        notes="Residual은 기존 표현을 보존하는 통로입니다. 더하려면 shape가 같아야 하므로 원형의 모든 sublayer는 d차원으로 "
              "돌아옵니다. Post-LN은 합한 뒤 정규화하고(y=LN(x+F(x))), Pre-LN은 sublayer 입력을 정규화한 뒤 더합니다"
              "(y=x+F(LN(x))). Pre-LN에서는 잔차 경로에 정규화가 끼지 않아 초기 gradient가 안정적이라는 분석이 있지만, "
              "한 설정의 결과로 보편적 우열을 결론 내리지 않도록 합니다.")

d.image("Decoder 입력과 정답을 한 칸 어긋나게", img("shift.png"),
        lead="Teacher forcing: 이전 '정답' 토큰을 입력으로 — 정답은 한 칸 뒤에 있다",
        side={"head": "왜 학습은 병렬로 되나", "body": [
            "입력이 I인 위치의 목표는 am → 현재 입력(대각선)을 보는 것은 **괜찮다**",
            "첫 위치가 뒤의 I를 보면 자기 정답을 보는 **누출**",
            "학습에서는 정답 prefix가 이미 모두 주어짐 → 모든 위치의 다음 토큰 예측을 한 번에 계산하고 mask로 의존성만 제한",
            "미래 값이 tensor에 **있는 것** ≠ Query가 **접근하는 것**",
            "BOS·EOS·PAD의 이름·ID는 tokenizer마다 다르다"]},
        img_w_ratio=0.55,
        notes="설명용 문장 I am a student로 Decoder 입력은 BOS부터, 정답은 EOS까지 한 칸 어긋나게 둡니다. 학습 때 이전 정답을 "
              "입력으로 쓰는 것을 teacher forcing이라 합니다. 정답 prefix가 모두 있으므로 위치별 예측을 병렬로 계산하고, "
              "causal mask로 미래 접근만 막습니다. 생성 때는 다음 입력이 아직 없으므로 순차성이 남고, 층 사이의 의존성도 "
              "있으므로 '모든 계산을 한 번에 병렬화한다'고 말하지 않습니다. [26]")

# --- Causal mask (custom)
s = d.blank("Causal mask는 Softmax 이전에: −∞",
            notes="정답 누출 탐지기 그림에서 행은 Query 위치, 열은 참조할 Decoder 입력 위치입니다. 예측할 위치 2(입력 I, 정답 am)는 "
                  "BOS와 I만 볼 수 있습니다. 차단은 Softmax 전에 점수에 −∞를 더하는 방식이어야 exp(−∞)=0으로 가중치가 사라집니다. "
                  "점수를 0으로 바꾸면 exp(0)=1이라 미래 가중치가 남습니다. FP16에서 큰 음수를 직접 쓸 때는 dtype 범위와 "
                  "수치 안정성을 확인합니다. 실습으로 causal mask만 제거해 보면 훈련 손실은 낮아지지만 실제 생성은 망가지는 "
                  "누출 효과를 볼 수 있습니다(결과 정도는 데이터에 따라 다름). [27]")
d.lead(s, "정답 누출 탐지기: 예측할 위치 2(입력 I → 정답 am)는 BOS와 I만 참조한다")
d._image_fit(s, img("causal_mask.png"), X0, 1.75, 5.3, 5.2)
cw = (X1 - 6.1 - 0.25) / 2
fbox(s, 6.1, 1.8, X1 - 6.1, 1.3, ["M_ij = 0 (j ≤ i),  −∞ (j > i)",
                                  "A = softmax(QKᵀ/√dₕ + M)"], size=17)
cw = (X1 - 6.1 - 0.25) / 2
panel(s, 6.1, 3.25, cw, 2.55, "−∞를 더하면 (정답)", [
    "점수 [2, 1, 3]", "→ [2, 1, −∞]", "softmax → [0.73, 0.27, **0.00**]", "미래 가중치 정확히 0"],
      size=13, bullets=False)
panel(s, 6.1 + cw + 0.25, 3.25, cw, 2.55, "0으로 바꾸면 (오류)", [
    "점수 [2, 1, 3]", "→ [2, 1, 0]", "softmax → [0.67, 0.24, ==0.09==]", "exp(0)=1 → 차단이 아니다"],
      accent=True, size=13, bullets=False)
b = d.box(s, 6.1, 5.95, X1 - 6.1, 1.0, fill=TEAL)
d.text_in(b, "대각선(j = i)은 허용: target이 한 칸 shift되어 있으므로 현재 입력 ≠ 현재 정답", size=15,
          color=WHITE, bold=True, align="c", margin=0.2)

d.table("Causal · Padding · Loss mask는 다르다", ["구분", "무엇을 막나", "어디에 적용하나"], [
    ["Causal mask", "미래 target 위치 참조", "Decoder self-attention 점수"],
    ["Source key padding mask", "source의 채움(PAD) 위치 참조", "Encoder self-attention / cross-attention"],
    ["Target key padding mask", "target의 채움 위치 참조", "Decoder self-attention"],
    ["Loss ignore mask", "PAD 정답이 학습 손실에 포함되는 것", "Cross-entropy 및 metric 집계"],
    ["API: F.scaled_dot_product_attention", "boolean attn_mask에서 True = 참조 **허용**", "PyTorch 함수형 SDPA [27]"],
    ["API: nn.MultiheadAttention", "attn_mask·key_padding_mask에서 True = 참조 **차단**", "PyTorch 모듈 [28]"],
], col_widths=[4.4, 4.4, 3.5], size=16, highlight_rows=[4, 5],
    lead="Key padding mask는 PAD Query의 출력을 0으로 만들지 않는다 → loss·pooling·평가에서 따로 제외",
    takeaway="이름이 같아 보여도 그대로 복사하면 의미가 뒤집힌다 — 이 강의 직접 구현은 allow=True(허용)로 통일",
    notes="네 가지 mask는 막는 대상과 적용 위치가 다릅니다. Key padding mask는 PAD 위치를 Key로 참조하지 못하게 할 뿐, "
          "PAD 위치 Query의 출력을 자동으로 0으로 만들지 않으므로 loss·pooling·평가에서 별도로 빼야 합니다. "
          "API마다 boolean 의미가 반대라는 점도 중요합니다. PyTorch scaled_dot_product_attention은 True가 허용, "
          "nn.MultiheadAttention의 attn_mask/key_padding_mask는 True가 차단입니다. 이 강의 실습 코드는 allow=True(허용)로 통일합니다. [27][28][29]")

# ================================================================== Part 02
d.section("02", "Encoder·Decoder 조립과 학습",
          "모든 부품을 수식과 shape로 다시 조립하고, 확률을 학습 목표로 바꾼다",
          notes="두 번째 파트는 원자료 16–17장입니다. 한 층의 수식, 출력 head, 한 샘플의 shape 추적, 파라미터 수를 유도한 뒤 "
                "학습 손실과 한 학습 step, 원논문의 학습 조건과 지표를 다룹니다.")

d.image("Encoder 한 층, Decoder 한 층", img("encdec_layer.png"),
        lead="각 sublayer = Dropout → 잔차 합 → LayerNorm (원형 Post-LN)",
        side=["Encoder: `U = LN₁(X + Drop(MHA(X,X,X)))`, `X′ = LN₂(U + Drop(FFN(U)))` — 입출력 `(B,S,d)`",
              "Decoder: masked self → cross `MHA(U, E, E)` → FFN, 각각 Add & LN (3개)",
              "모든 Decoder 층이 Encoder **최종** 출력 E를 참조 — 층마다 Encoder를 다시 실행하지 않음, cross 투영은 층마다 별도",
              "출력 head: `Z = D·W_vocab + b`, W_vocab `d×|V|` → logits `(B,T,|V|)`",
              "원논문은 embedding과 출력층의 **weight tying** — 공유 어휘 등 조건이 맞아야 하는 설계 선택"],
        img_w_ratio=0.5,
        notes="Encoder 층은 self-attention과 FFN 두 sublayer, Decoder 층은 masked self-attention, cross-attention, FFN "
              "세 sublayer입니다. 여기서 MHA(Q원본,K원본,V원본)는 내부 투영을 포함한 모듈 표기입니다. Cross-attention의 "
              "K, V는 Encoder stack의 최종 출력 E에서 오며, 각 Decoder 층은 자신만의 cross-attention 투영 가중치를 가집니다. "
              "마지막 선형층 W_vocab이 d를 |V|개 점수로 바꾸고 softmax가 다음 토큰 확률을 줍니다. 모든 Transformer가 "
              "weight tying을 쓰는 것은 아닙니다. [22 §3.1, §3.4]")

d.table("한 샘플을 끝까지 추적하기", ["구간", "Shape", "해석"], [
    ["Source IDs", "(2, 5)", "padding된 입력"],
    ["Source embedding + PE", "(2, 5, 8)", "8차원 표현"],
    ["Encoder 최종 출력 E", "(2, 5, 8)", "입력의 문맥 표현"],
    ["Target prefix IDs", "(2, 3)", "BOS 포함, 오른쪽으로 이동한 입력"],
    ["Decoder self-attention 표", "(2, 2, 3, 3)", "causal mask 적용"],
    ["Cross-attention 표", "(2, 2, 3, 5)", "source 5개 위치 참조"],
    ["Decoder 최종 출력", "(2, 3, 8)", "Query 위치 수 3 유지"],
    ["Vocabulary logits", "(2, 3, 16)", "각 위치에서 16개 후보 점수"],
], col_widths=[4, 2.5, 5.5], size=17, highlight_rows=[5],
    lead="B=2, S=5, T=3, d=8, H=2, |V|=16",
    takeaway="표준 블록은 길이를 바꾸지 않는다 — target이 늘어나는 것은 생성 루프가 토큰을 추가하기 때문",
    notes="5주차의 d=8, H=2 설정으로 한 배치를 끝까지 따라갑니다. Cross-attention 표 (2,2,3,5)는 T=3개 Query가 S=5개 "
          "source Key를 보는 표이고, 출력은 Query 길이 3을 유지합니다. 보드 활동: 빈 Encoder/Decoder 박스를 보여 주고 "
          "Attention의 출처, mask, residual, FFN, output head를 채우게 한 뒤 '어느 단계에서 길이가 바뀌나?'를 묻습니다.")

d.formula("파라미터 수를 직접 유도하기", "params / 층 ≈ 4d² + 2d·d_ff",
          parts=[("4d²", "Self-attention W_Q, W_K, W_V, W_O (각 d×d)"),
                 ("2d·d_ff", "FFN W₁ (d×d_ff) + W₂ (d_ff×d)"),
                 ("d_ff = 4d", "Encoder 층 ≈ 12d², Decoder 층 ≈ 16d² (cross +4d²)"),
                 ("제외", "bias · LayerNorm · Embedding — 행렬 원소 수의 근사")],
          example=["원형 Base: d=512, d_ff=2048",
                   "4d² ≈ 1.05M, 2d·d_ff ≈ 2.10M",
                   "Encoder 층 ≈ **3.15M**, Decoder 층 ≈ **4.19M**",
                   "6 + 6층 ≈ 44.0M",
                   "+ 공유 embedding 37K×512 ≈ 18.9M",
                   "합계 ≈ 63M ↔ 논문 보고 ==65M=="],
          lead="원형 Base: Encoder/Decoder 각 6층, H=8, dₕ=64, dropout 0.1, label smoothing 0.1",
          takeaway="숫자를 외우기보다 다른 d·층 수에도 같은 계산을 적용할 수 있어야 한다",
          notes="Self-attention의 네 투영 행렬이 4d², FFN이 2d·d_ff이므로 d_ff=4d이면 Encoder 층 약 12d², cross-attention이 "
                "더해진 Decoder 층 약 16d²입니다. Base에 대입하면 층당 3.15M, 4.19M이고 12개 층 합이 약 44M입니다. 약 37,000개 "
                "공유 BPE 어휘 embedding(약 18.9M)을 더하면 63M 정도로, 논문의 65M과 가깝습니다(bias·Norm 포함 여부에 따라 "
                "차이). Python으로 재계산해 확인한 수치입니다. [22 §3, Table 3]")

d.formula("다음 토큰의 음의 로그 가능도", "𝓛 = −(1/N_valid) · Σ log p_θ(y_t | y_<t, x)",
          parts=[("p_θ(y_t|…)", "정답 토큰에 모델이 준 확률 (softmax 출력)"),
                 ("y ≠ PAD", "PAD 정답은 합에서 제외 (ignore_index)"),
                 ("N_valid", "PAD가 아닌 토큰 수로 평균 — 집계 규칙을 명시"),
                 ("logits", "CrossEntropyLoss에는 softmax 전 logits, (B·T, |V|)로 펼침")],
          example=["정답 확률 p = [0.7, 0.5, 0.9, 0.2]",
                   "−log p = [0.36, 0.69, 0.11, 1.61]",
                   "평균 NLL ≈ **0.69**",
                   "Perplexity = exp(0.69) ≈ **2.0**",
                   "p=1이면 0, p가 작을수록 급격히 커진다"],
          lead="Loss = −Σ log p: 정답 토큰의 확률을 높이는 것이 학습 목표",
          takeaway="PAD 제외는 loss와 accuracy 계산 양쪽에 반영한다",
          notes="학습 목표는 각 위치에서 정답 다음 토큰의 로그 확률을 높이는 것, 즉 음의 로그 가능도(NLL)를 줄이는 것입니다. "
                "PAD가 아닌 토큰 수로 정규화하며, 긴 시퀀스와 짧은 시퀀스를 어떤 단위로 평균하는지에 따라 가중이 달라지므로 "
                "집계 규칙을 명시합니다. PyTorch CrossEntropyLoss는 softmax 전 logits를 받습니다. 예시에서 네 토큰의 평균 NLL "
                "0.69는 perplexity 약 2, 즉 '평균적으로 두 후보 중 고르는 정도의 불확실성'으로 읽을 수 있습니다. [29]")

d.code("한 학습 step의 순서", """model.train()             # dropout 켜기
optimizer.zero_grad(set_to_none=True)
# (B,T,|V|) logits
logits = model(source_ids, target_input_ids)
loss = F.cross_entropy(
    logits.reshape(-1, vocab_size),  # (B·T,|V|)
    target_labels.reshape(-1),       # (B·T,)
    ignore_index=PAD,
)
loss.backward()           # gradient 계산
nn.utils.clip_grad_norm_(
    model.parameters(), 1.0)
optimizer.step()          # 파라미터 갱신""", code_size=16,
       lead="Batch → Forward(logits) → Loss(masked CE) → Backward(gradient) → Step(θ 갱신)",
       explain=["역전파는 gradient 계산, **optimizer가 갱신**",
                "Gradient clipping은 교육용 보호 장치 — 원논문 recipe와 동일하다는 뜻이 아님",
                "`model.eval()`: dropout 등 모듈 동작을 평가 모드로",
                "`torch.no_grad()` / `inference_mode()`: autograd 기록 끄기 — **역할이 다르다**",
                "functional SDPA는 평가 때 `dropout_p=0.0`을 명시해야 할 수 있다"],
       notes="한 step은 train 모드 → gradient 초기화 → forward → masked cross-entropy → backward → (clipping) → optimizer "
             "step 순서입니다. logits (B,T,|V|)를 (B·T,|V|)로, 정답을 (B·T)로 펼쳐 class 축을 맞춥니다. 평가 때 "
             "model.eval()과 torch.no_grad()는 서로 다른 일을 하므로 둘 다 필요할 수 있습니다. [27][29]")

d.image("원논문의 학습 조건", img("lr_schedule.png"),
        lead="η(s) = d^(−1/2) · min(s^(−1/2), s · w^(−3/2)),  w = 4000",
        side={"head": "Vaswani 등 2017 §5", "body": [
            "Adam β₁=0.9, β₂=0.98, ε=10⁻⁹",
            "warm-up 4000 step 선형 증가 → s^(−1/2) 감소",
            "Residual dropout 0.1 (Base)",
            "Label smoothing 0.1: perplexity는 나빠지지만 정확도·BLEU는 개선",
            "8×P100: Base 100K step(약 12시간), Big 300K step(3.5일)",
            "WMT14 BLEU: EN–DE 27.3(Base) / 28.4(Big), EN–FR 41.8(Big)"]},
        img_w_ratio=0.55,
        notes="원논문은 Adam(β₁=0.9, β₂=0.98, ε=10⁻⁹)과 warm-up 후 감소하는 학습률을 씁니다. d=512, w=4000이면 최고 학습률은 "
              "약 7.0×10⁻⁴입니다(재계산). Label smoothing은 정답을 확률 1로 몰지 않게 하며, 논문은 perplexity는 나빠지지만 "
              "정확도와 BLEU는 좋아진다고 보고합니다. 학습 loss 하나가 평가 목표 전체를 대변하지 않는다는 사례입니다. "
              "이 조건들은 모델 구조와 별개인 실험 조건입니다. [22 §5–6][24]")

d.table("어떤 지표를 기록할까", ["지표", "의미", "주의점"], [
    ["Loss / NLL", "정답 토큰의 로그 가능도", "PAD · 평균 단위 · smoothing 여부 명시"],
    ["Perplexity", "exp(평균 NLL)", "raw NLL로 계산, 같은 tokenizer·데이터·집계에서만 비교"],
    ["Token accuracy", "맞힌 토큰의 비율", "한 시퀀스의 작은 오류를 가릴 수 있음"],
    ["Exact match", "시퀀스 전체가 정확한 비율", "EOS와 길이 기준을 정해야 함"],
    ["실제 생성 성능", "생성한 prefix에 기반한 결과", "teacher-forced 평가와 별도로 측정"],
], col_widths=[2.6, 4, 5.6], size=19,
    lead="Label-smoothed loss를 exp한 값을 perplexity로 섞지 않는다",
    takeaway="loss가 안 떨어지면: 1–4개 샘플 과적합부터 → shift · mask 방향 · logits shape · ignore_index · optimizer 점검",
    notes="Perplexity는 raw NLL로 계산해야 해석이 됩니다. Token accuracy는 teacher forcing 조건의 값이라 실제 생성 성능과 "
          "다릅니다. 학습 loss가 떨어지지 않으면 층 수나 GPU를 늘리기 전에 작은 샘플 과적합부터 확인하고, 그마저 안 되면 "
          "데이터 정렬, target shift, mask 방향, logits shape, ignore_index, optimizer에 파라미터가 들어갔는지를 점검합니다.")

# ================================================================== Part 03
d.section("03", "추론과 효율: 생성 · KV Cache · 비용",
          "병렬 학습과 순차 생성이 공존하는 이유, 그리고 연산량과 메모리를 분리해서 보기",
          notes="세 번째 파트는 원자료 18–19장입니다. 자기회귀 생성과 토큰 선택 정책, KV Cache의 정확한 역할, "
                "그리고 O(N²)만으로는 부족한 비용 분석을 다룹니다.")

d.flow("추론: 토큰을 하나씩 생성하기", [
    {"head": "Encoder 1회", "body": "source → E (B,S,d)\n이후 모든 step에서 재사용"},
    {"head": "BOS로 시작", "body": "prefix = [BOS]\n정답 prefix는 없다"},
    {"head": "마지막 위치 logits", "body": "다음 토큰 선택\n(선택 정책은 모델과 별개)"},
    {"head": "append · 반복", "body": "prefix에 붙이고 반복\nEOS 또는 최대 길이에서 종료", "accent": True},
], lead="다음 입력이 방금 생성한 결과에 의존 → 자기회귀(autoregressive) 루프",
    below=["**Greedy**: 최고 점수 선택 — 단순하지만 전체 시퀀스 최적 보장 없음 · **Beam search**: 후보 prefix 여러 개 유지, "
           "계산↑ (원논문: beam 4, 길이 패널티 α=0.6)",
           "**Sampling**: 분포에서 추출 — 다양성↑, 결과 변동 · **Temperature**: logits/τ로 분포 조절 — 재학습이 아니다",
           "선택 정책은 출력 분포를 **사용하는 방식** — Q/K/V 가중치를 바꾸는 학습과 다르다"],
    caption="Greedy와 beam을 비교하기 전에 과제의 평가 목표부터 정한다",
    notes="추론에서는 source를 Encoder로 한 번 처리하고 BOS로 Decoder를 시작합니다. 마지막 위치 logits에서 다음 토큰을 골라 "
          "prefix에 붙이고, EOS나 최대 길이에서 멈춥니다. 토큰을 고르는 정책은 모델과 별개입니다. 원논문 번역 실험은 "
          "beam size 4, length penalty α=0.6을 썼습니다. 정답 prefix를 주었을 때의 token accuracy와 처음부터 생성했을 때의 "
          "exact match를 같이 보여 주면 teacher forcing과 생성의 차이를 체감할 수 있습니다. [22 §6.1][26]")

d.image("KV Cache: Prefill과 Decode", img("kv_cache.png"),
        lead="과거 prefix의 층별 K, V는 새 토큰이 와도 바뀌지 않는다 → 저장해서 재사용",
        side={"head": "저장하는 것과 남는 것", "body": [
            "과거 K, V 불변 → prefix forward 반복을 줄인다",
            "**Q는 캐시하지 않음** (현재 토큰만 필요)",
            "Enc–Dec: E와 cross-attn K, V 재사용",
            "**남는 것**: 순차 루프, 과거 Key 참조 비용",
            "가중치·adapter·position ID·mask가 다르면 같은 prefix라도 **공유 불가**",
            "측정: TTFT(prefill) / token당 지연(decode)"]},
        img_w_ratio=0.64,
        notes="KV Cache는 과거 토큰의 K, V가 미래 토큰 추가로 바뀌지 않는다는 성질을 이용합니다. Cache를 쓰든 안 쓰든 "
              "올바른 구현은 같은 결과를 목표로 하며, 수치 오차·커널 차이 정도만 생길 수 있습니다. Prefill은 주어진 prefix를 "
              "한꺼번에 처리하는 단계, Decode는 토큰을 하나씩 늘리는 단계로 병목이 다르므로 TTFT와 token당 지연을 나눠 "
              "기록합니다. 이 강의의 Python 실습은 흐름을 보이려고 KV Cache 없이 prefix를 재계산하며, Cache 적용은 확장 과제입니다. [26][37]")

d.image("“Transformer는 O(N²)”만으로는 부족하다", img("flops_terms.png"),
        lead="MACs / 샘플 / 층 = 4Nd² + 2N²d + 2Nd·d_ff  (1 MAC ≈ 2 FLOPs, Norm·Softmax·bias 제외)",
        side={"head": "항마다 따로 읽기", "body": [
            "`4Nd²`: Q/K/V + output 투영 — N×d @ d×d 네 번",
            "`2N²d`: QKᵀ와 AV — H·N²·dₕ 곱 두 번",
            "`2Nd·d_ff`: FFN 확장·축소",
            "d 고정, N 2배 → Attention 항 **×4**, 투영·FFN 항 **×2**",
            "d_ff = 4d이면 N = 6d(=3072)에서 Attention 항이 나머지와 같아진다",
            "Encoder 한 블록 dense forward 식 — backward·optimizer·생성 루프 총비용 아님"]},
        img_w_ratio=0.5,
        notes="길이 N, 폭 d의 dense self-attention 블록에서 주요 행렬 곱을 직접 세면 4Nd² + 2N²d + 2Nd·d_ff MAC입니다. "
              "d=512, d_ff=2048에서 N=512이면 투영·FFN 항이 대부분이고, N=4096이 되어야 Attention 항이 가장 커집니다(Python 재계산). "
              "그래서 'O(N²)'만 말하면 짧은 입력에서의 실제 비용 구조를 놓칩니다. 계산기 활동: d를 고정하고 N을 두 배로, "
              "다음엔 N을 고정하고 d를 두 배로 바꿔 각 항이 몇 배가 되는지 먼저 쓰게 합니다.")

# --- KV cache bytes (custom)
s = d.blank("KV Cache의 저장량",
            notes="K와 V를 각각 저장하므로 2가 붙고, 층 수 L, 배치 B, 길이 N, KV head 수 H_kv, head 차원 dₕ, 원소당 bytes를 "
                  "곱합니다. MHA에서는 H_kv·dₕ = d이므로 2·L·B·N·d·bytes입니다. 원형 Base 디코더(6층, d=512)는 N=1024, FP16에서 "
                  "12 MiB에 불과하지만, L=32·d=4096 가정의 큰 모델은 N=4096에서 2 GiB, 배치 8이면 16 GiB입니다. GQA로 KV head를 "
                  "8개로 줄이면 1/4이 됩니다. 순수 K/V 데이터만의 크기이며 allocator·padding·metadata는 제외입니다. [37]")
d.lead(s, "K와 V를 각각 저장하므로 2 — 길이 N과 배치 B에 선형으로 늘어난다")
fbox(s, X0, 1.8, W, 1.2, ["bytes_KV = 2 · B · L · N · H_kv · dₕ · b",
                          "MHA (H_kv·dₕ = d)  →  2 · L · B · N · d · bytes"], size=19)
d._image_fit(s, img("kv_memory.png"), X0, 3.15, 6.4, 3.8)
panel(s, 7.2, 3.15, X1 - 7.2, 3.8, "숫자로 확인 (FP16, b=2)", [
    "원형 Base 디코더: L=6, d=512, N=1024 → **12 MiB**",
    "L=32, d=4096, N=4096, B=1 → **2 GiB**, B=8 → ==16 GiB==",
    "GQA H_kv=8 (H=32) → 0.5 GiB",
    "비교: score 표 1개 B·H·N² = 1 GiB / 층 (N=4096, H=32)",
    "순수 K/V만 — allocator·padding·metadata 제외"], accent=True, size=14)

d.cards("측정할 때 구분할 것", [
    {"head": "Explicit 표 ≠ 실제 메모리", "body": ["score 표 = B·H·N² 원소 ≠ peak memory",
              "activation·gradient·optimizer state 추가",
              "FlashAttention: 표를 HBM에 두지 않고 **같은** 계산 — 산술량은 그대로 [38]"]},
    {"head": "경로 길이 ≠ 학습 보장", "body": ["RNN: 먼 위치 사이 여러 time step",
              "Self-attention: 한 층에서 직접 연결",
              "짧은 경로 ≠ 원하는 관계 학습 보장 [22 §4]"]},
    {"head": "측정 통제", "body": ["batch·dtype·길이·device·kernel·warm-up 기록",
              "GPU timing은 동기화 후 측정",
              "'이론 MACs'와 '실측 latency' 구분"]},
    {"head": "Research lens", "accent": True,
     "body": ["토큰 절반 → Attention 항 ≈ 1/4, 나머지 ≈ 1/2",
              "overhead·kernel·데이터 이동 → 지연은 덜 준다",
              "파라미터↓ ≠ FLOPs↓ ≠ latency↓"]},
], cols=2, lead="Big-O, 저장량, 병렬성, 지연 시간은 서로 다른 질문이다",
    notes="연산량 계산기 값은 이론 추정이지 실제 지연·GPU peak memory 예측기가 아닙니다. FlashAttention은 정확한 attention을 "
          "IO 효율적으로 계산할 뿐, dense 상호작용의 산술량을 줄이지는 않습니다. 경로 길이가 짧다는 것과 원하는 의미 관계를 "
          "잘 학습한다는 것은 다릅니다. 실험에서는 조건을 기록하고, 식으로 비율을 예측한 뒤 실행 시간은 따로 잽니다.")

# ================================================================== Part 04
d.section("04", "작은 Transformer 실습과 실험 설계",
          "외부 데이터 없이 수열을 뒤집으며 Attention부터 생성까지 확인하고, 질문을 통제된 비교로 바꾼다",
          notes="네 번째 파트는 원자료 20–21장입니다. 교육용 transformer_lab.py를 실행하고 검사하며 결과를 해석한 뒤, "
                "ablation 실험과 최종 프로젝트를 설계합니다.")

s = d.blank("실습: 작은 Transformer 실행", notes="실습 파일은 명시적 Q/K/V, causal·padding mask, Post-LN, sinusoidal position, cross-attention, loss, greedy "
             "generation을 모두 포함하는 작은 Encoder–Decoder입니다(d=64, H=4, 각 2층, 출력 head는 embedding과 묶지 않음). "
             "먼저 --mode check로 아홉 검사를 통과시키고 학습합니다. 검사에서는 dropout을 끄고 허용 오차를 명시합니다. "
             "자료 제작 시 PyTorch 2.10.0/CPU에서 아홉 검사를 통과했지만, 이것이 다른 장치의 성능이나 400 step 수렴을 "
             "보장하지는 않습니다. 코드 리뷰는 mask·shape·loss/metric·generation을 한 명씩 맡겨 설명하게 합니다.")
d.lead(s, "[3,7,5] → [5,7,3,EOS] 뒤집기 · d=64, H=4, 각 2층, Post-LN · 원논문 재현이 아닌 교육용 · KV Cache 없음")
d.box(s, X0, 1.8, 7.2, 2.55, fill=CODE_BG, line=LINE, radius=0.05)
lines = ["# 1. 모듈 단위 검사 — 학습 없이 구조 검증",
         "python transformer_lab.py --mode check",
         "# 2. CPU에서 작은 모델 학습",
         "python transformer_lab.py --mode train \\",
         "    --steps 400 --device cpu",
         "# 3. CUDA가 있으면: --device auto --seed 7"]
tb = s.shapes.add_textbox(Inches(X0 + 0.15), Inches(1.9), Inches(6.9), Inches(2.4))
for i, ln in enumerate(lines):
    p = tb.text_frame.paragraphs[0] if i == 0 else tb.text_frame.add_paragraph()
    _no_bullet(p)
    r = p.add_run()
    r.text = ln
    _set_run_font(r, size=15, color="5E8C6A" if ln.startswith("#") else DARK, mono=True)
panel(s, X0, 4.5, 7.2, 2.45, "코드를 읽는 순서", [
    "① `attention()`: (B,H,T,S) 점수 행렬이 만들어지는 곳",
    "② `MultiHead.split()`: reshape + transpose",
    "③ `EncoderBlock` / `DecoderBlock`: residual과 Norm 위치",
    "④ `make_batch()`의 shifted target → `generate()`의 prefix 확장"], size=15)
panel(s, X0 + 7.45, 1.8, W - 7.45, 5.15, "반드시 통과할 아홉 검사", [
    "**Shape**: Q/K/V·출력 차원",
    "**Row sum**: dropout 전 행 합 = 1",
    "**Future weight zero**: 미래 가중치 0",
    "**PyTorch reference**: SDPA와 일치",
    "**Permutation equivariance**",
    "**Cross query length** = Query 길이",
    "**Masked value independence**",
    "**Full-model causal invariance**: 미래 target을 바꿔도 이전 logits 불변",
    "**Backward gradient**: encoder 투영까지"], accent=True, size=14)

d.stats("첫 결과를 해석하는 방법", [
    ("1.045", "3–8 길이(훈련 범위)\n평가 raw NLL"),
    ("56.8%", "teacher-forced\ntoken accuracy"),
    ("6.9%", "greedy exact match\n(5 / 72)"),
    ("0 / 72", "9–12 긴 입력\nexact match (NLL 1.764)"),
], lead="PyTorch 2.10.0 CPU · seed 7 · batch 32 · 400 step 단일 실행 — 원논문 성능이 아니다",
    below=["훈련 NLL 2.90(step 1) → 1.23(step 400)이지만 완전한 수열 생성은 아직 못함 — **loss와 생성 성능은 같지 않다**",
           "길이를 늘려 떨어져도 구현 오류라 단정 X (외삽 문제일 수 있음) / 훈련 길이에서 잘 맞혀도 길이 일반화가 증명된 것 X",
           "다음 단계: 학습량 늘리기 · 작은 고정 샘플 과적합 검사 · 위치 정보의 역할 확인"],
    notes="원자료 제작 시 실제 실행 사례입니다. 각 길이 구간 평가 예시는 72개이며, 9–12 구간의 token accuracy는 33.82%였습니다. "
          "400 step은 실행 예시일 뿐 충분한 학습의 보장이 아니고, 이 결과만으로 Transformer의 구조적 한계를 결론 내리지 않습니다. "
          "교육용 코드는 mask 검증을 위해 GPU 동기화가 있으므로 그대로 성능 벤치마크로 쓰지 않습니다.")

d.table("실험으로 구조의 필요성 확인하기", ["실험", "변경 변수", "통제할 것", "볼 지표"], [
    ["긴 입력", "평가 길이", "모델 · 학습 데이터 · 생성 규칙", "길이별 token accuracy / exact match"],
    ["위치 정보", "source / target PE 각각 제거", "나머지 구조 · seed · 학습량", "순서 민감 과제 성능"],
    ["Head 수", "H 변경, d 고정", "파라미터 근사 규모 · step", "품질 · 지연 · explicit 표 저장량"],
    ["Mask 오류", "causal mask 의도적 제거", "shifted input 유지", "훈련 loss와 실제 생성의 괴리"],
    ["FFN 제거", "FFN 유무", "파라미터·연산량 변화 별도 보고", "학습 곡선과 최종 성능"],
    ["Residual 제거", "skip path 유무", "깊이 · 초기화 · optimizer", "수렴 양상 · gradient 규모"],
    ["정규화 위치", "Post-LN / Pre-LN", "깊이 · warm-up · 학습률", "불안정성 · 최종 품질"],
], col_widths=[2.2, 3.2, 3.4, 3.8], size=16,
    lead="질문 고정: 어떤 데이터·길이·학습량에서 어떤 구조가 어떤 지표에 영향을 주나",
    takeaway="부품 제거는 파라미터·연산량도 바꾼다 → 구조 효과와 용량 효과를 분리할 대조군",
    notes="'Transformer가 더 좋다'가 아니라 통제된 비교 질문으로 바꿉니다. RNN Seq2Seq, Attention Seq2Seq, 작은 Transformer를 "
          "비교할 수 있고, 구현이 부담스러우면 기준 모델을 제공하고 한 모델만 작성하게 합니다. Pre-LN/Post-LN 비교도 한 설정으로 "
          "보편적 우열을 결론 내리지 않습니다. [25]")

d.code("작은 task와 기록 규칙", """# 실험마다 남길 최소 필드
run_id, git_commit, seed, task, vocab_size
train_lengths, eval_lengths,
train_examples_or_steps
architecture, layers, d_model, heads,
d_ff, position_type, mask_policy,
norm_placement, dropout, optimizer,
learning_rate, batch_size, precision,
device, torch_version
teacher_forced_nll, token_accuracy,
greedy_exact_match, prefill_ms,
decode_ms_per_token, peak_memory_mb
notes, known_limitations""",
       lead="복사(output=input) · 반전(순서 뒤집기) · 기호 치환(정해진 매핑)부터",
       explain=["세 과제는 필요한 순서 정보·전역 의존성이 다르다",
                "데이터 규칙 명시: 입력 길이 · 어휘 · 중복 비율 · EOS",
                "진행: 고정 batch 과적합 → 새 수열 → 길이별 평가 → 구조 변경 → seed 3개 이상",
                "**네 가지 그림**: 길이–정확도 · step–loss · 품질–지연 · 길이–메모리 (평균·변동 폭·표본 수)",
                "측정 안 한 값은 채우지 않는다 — '이론 MACs' vs '실측 latency' 표시"],
       code_size=16,
       notes="작은 task부터 시작합니다. 복사는 output=input, 반전은 순서 뒤집기, 기호 치환은 정해진 매핑으로 토큰을 바꾸는 과제로 "
             "필요한 순서 정보가 다릅니다. seed 개수만 늘린다고 편향된 실험이 해결되지는 않습니다. 그래프의 범위를 바꿔 효과를 "
             "과장하지 않도록 하고, 각 그림은 한 가지 질문만 답하게 분리합니다.")

d.table("최종 프로젝트 제출안", ["산출물", "포함할 내용", "제안 배점"], [
    ["문제와 가설", "무엇을 비교하는지, 예상과 반증 조건", "20"],
    ["구현 정확성", "shape · mask · gradient 검사, 재현 명령", "30"],
    ["실험 설계와 결과", "통제 변수 · seed · metric · 그래프", "25"],
    ["해석과 한계", "실패 사례, 대안 설명, 일반화 범위", "15"],
    ["설명 발표", "아키텍처를 입력부터 출력까지 추적", "10"],
], col_widths=[3, 7, 2], size=20,
    lead="더 높은 모델 점수보다 검증 가능한 실험과 설명을 평가한다",
    takeaway="발표 세 질문: ① 어느 가정에서만 성립? ② 파라미터·학습량 차이 때문은 아닌가? ③ 실패 입력 하나를 계산 흐름으로 설명할 수 있나?",
    notes="배점은 멘토링 운영을 위한 제안입니다. 예상과 다른 결과를 얻어도 실험 조건과 가능한 설명을 정확히 정리했다면 좋은 연구 "
          "연습이며, 정해 둔 결론에 맞춰 데이터나 조건을 숨기지 않습니다. 구술 평가에서는 처음 보는 d, H, S, T 설정으로 입력부터 "
          "logits까지 추적하게 하고, 위치 정보 제거·잘못된 mask·KV Cache 추가 중 하나의 효과를 설명하게 합니다.")

# ================================================================== Part 05
d.section("05", "Transformer 이후와 과정 마무리",
          "원형에서 무엇을 유지하고 무엇을 바꾸었는지 — 그리고 6주의 계보를 다시 연결한다",
          notes="마지막 파트는 원자료 23–27장입니다. 후속 구조를 원형과 비교하는 틀을 세우고, 오개념·개념 확인·마지막 설명 과제로 "
                "과정 전체를 정리합니다.")

s = d.blank("세 가지 조립 방식", notes="BERT, GPT, T5는 같은 부품을 쓰지만 mask와 학습 목표, output head, 데이터가 함께 다릅니다. BERT의 masked language "
              "modeling은 입력에서 가린 위치를 복원하는 목표라서, '미래 정답을 보고 다음 토큰을 예측하는' 누출과 다릅니다. "
              "각 설명은 대표 원형 연구 기준이며 모든 후속 변형의 정의는 아닙니다. [31][32][33]")
d.lead(s, "구조 · 입력 · 학습 목표를 따로 비교한다 — Encoder-only / Decoder-only는 '반쪽 떼기'가 아니다")
d._image_fit(s, img("archs.png"), X0, 1.7, W, 3.35)
hw = (W - 0.3) / 2
panel(s, X0, 5.15, hw, 1.8, "함께 바뀌는 것", [
    "mask · 학습 목표 · 위치 표현 · 정규화 · output head · 데이터",
    "원형 Decoder = self + cross + FFN / 순수 텍스트 Decoder-only = causal self + FFN"], size=14)
panel(s, X0 + hw + 0.3, 5.15, hw, 1.8, "판별 기준: 무엇이 입력이고 무엇이 정답인가", [
    "BERT MLM: 입력에서 가린 위치 **복원** — 미래 정답 누출과 다른 목표",
    "GPT: 다음 토큰 예측 · T5: text-to-text, span corruption"], accent=True, size=14)

d.image("ViT와 DiT: 무엇을 token이라 부를까", img("vit_patch.png"),
        lead="ViT(2020): 문자열 대신 patch 벡터를 token으로 — 224×224, 16×16 patch → 196개",
        side={"head": "DiT: 같은 block, 다른 생성 과정", "body": [
            "입력: noisy latent patch + timestep + 조건 정보",
            "출력: denoising에 필요한 값 예측 — 토큰 생성 루프와 다른 계산",
            "원형 DiT는 class conditioning, 여러 conditioning 방식 비교 → 모든 DiT가 텍스트·cross-attention을 쓰는 것은 아님",
            "token 위치 · layer 깊이 · denoising timestep은 서로 다른 축",
            "Peebles & Xie, arXiv 2022 / ICCV 2023"]},
        img_w_ratio=0.63,
        notes="이미지를 16×16 patch로 나누면 224×224 이미지는 14×14=196개 patch가 되고, 각 patch(16·16·3=768개 값)를 선형 투영해 "
              "token으로 씁니다. CLS 사용, 위치 임베딩, pooling은 모델별로 확인해야 하며 모든 Vision Transformer가 CLS를 갖는 것은 "
              "아닙니다. ViT는 arXiv 2020, ICLR 2021입니다. DiT는 diffusion의 denoising 예측에 Transformer block을 쓰며, "
              "timestep과 class 조건을 넣는 방식을 비교합니다. [34 §3][41 §3]")

d.table("원형과 후속 변형을 구분하기", ["항목", "2017 원형", "후속 변형 예", "겨냥하는 문제", "하지 않는 주장"], [
    ["FFN 활성화", "ReLU", "GELU, SwiGLU", "gate가 있는 특징 변환", "Attention을 대체하지 않음"],
    ["정규화", "LayerNorm, Post-LN", "Pre-LN, RMSNorm", "깊은 모델의 학습 안정성", "모든 설정에서 우월하지 않음"],
    ["위치 정보", "sinusoidal 더하기", "학습형 위치, RoPE", "Q·K 내적에 상대 위치 반영", "위치 정보를 없애지 않음"],
    ["Head 구성", "Q/K/V head 수 같음", "GQA, MQA", "KV head 공유로 cache·대역폭 절충", "Query head까지 줄이지 않음"],
    ["Attention 계산", "명시적 score 표", "FlashAttention", "정확한 attention을 IO 효율적으로", "산술량을 선형으로 만들지 않음"],
], col_widths=[2.0, 2.4, 2.4, 3.0, 3.0], size=16,
    lead="후속 구조를 읽는 질문: 무엇이 바뀌었나 · 어떤 문제를 겨냥하나 · 무엇을 주장하지 않나",
    takeaway="RoPE: ⟨R(m)q, R(n)k⟩ = qᵀR(n−m)k — 위치를 더하지 않고 Q·K를 회전시켜 상대 위치를 내적에 반영",
    notes="후속 변형이 존재한다고 특정 조합이 모든 모델의 표준이라는 뜻은 아닙니다. 각 변형을 원형 표의 한 칸에 꽂아 넣고 무엇이 "
          "바뀌는지 설명할 수 있을 정도로만 다룹니다. SwiGLU 등 GLU 변형(Shazeer 2020), RoPE(Su 등 2021), GQA(Ainslie 등 2023), "
          "FlashAttention(Dao 등 2022)이 대표 예입니다. GQA는 Grouped-query Attention이며 시각 질의응답 데이터셋 GQA와 다릅니다. "
          "강의 목표를 달성하기 전에는 세부 구현까지 확장하지 않습니다. [35][36][37][38]")

d.table("자주 생기는 오개념: Transformer 편", ["#", "흔한 표현", "더 정확한 설명"], [
    ["12", "FFN은 다른 토큰을 다시 섞는다", "FFN 자체는 각 위치의 특징을 독립적으로 변환한다"],
    ["13", "LayerNorm은 Batch 전체를 정규화한다", "전형적 Transformer에서는 각 token의 마지막 특징 축을 정규화한다"],
    ["15", "미래 점수를 0으로 만들면 mask가 된다", "Softmax 전 −∞ 등으로 차단한다 — exp(0)은 1이다"],
    ["16", "학습 입력에 정답이 있으면 무조건 누출이다", "shift된 목표와 허용 정보 범위를 함께 봐야 한다"],
    ["17", "Transformer는 모든 토큰을 동시에 생성한다", "teacher-forced 학습의 위치 병렬성과 자기회귀 생성은 다르다"],
    ["18", "Attention이 N²이므로 전체 비용도 N²뿐이다", "선형 투영·FFN의 Nd² 항과 기타 비용이 있다"],
    ["19", "KV Cache가 있으면 과거 문맥 비용이 사라진다", "과거 K/V 재계산을 줄이지만 새 Q의 문맥 참조는 남는다"],
    ["20", "Attention heatmap은 모델의 생각을 증명한다", "관찰 자료이며 인과 설명은 별도 검증이 필요하다 [39][40]"],
], col_widths=[0.6, 5, 6.4], size=16,
    lead="틀린 문장을 정확한 계산 언어로 바꿔 본다 (원자료 오개념 20가지 중 12–20)",
    takeaway="실무 점검: softmax 축 = Key 축? · reshape 순서 · eval() ≠ no_grad · attention PAD mask와 loss PAD 제외 둘 다 · teacher-forced ≠ 생성 성능",
    notes="원자료의 오개념 20가지 중 6주차 내용과 직결되는 것들입니다. 실무에서 추가로 틀리기 쉬운 것: softmax(dim=-1)의 "
          "마지막 축이 정말 Key 축인지, reshape가 token과 head를 의도대로 합치는지, model.eval()과 gradient 비활성화의 구분, "
          "padding mask와 loss의 PAD 제외 둘 다 적용했는지, teacher forcing 평가를 생성 성능으로 보고하지 않았는지. "
          "경고 신호: 너무 빨리 낮아지는 loss, PAD를 맞히는 높은 accuracy, EOS 없이 계속되는 생성, 모든 위치가 비슷한 출력.")

d.compare("더 좋은 설명의 형식", {
    "head": "피할 표현", "accent": True, "body": [
        "“이 Head는 주어를 이해한다”",
        "“이 구조는 항상 빠르다”",
        "“train loss가 낮으니 생성도 잘한다”",
        "“Attention heatmap이 모델의 생각을 보여 준다”"]}, {
    "head": "더 정확한 표현", "body": [
        "“이 입력들에서 특정 위치에 높은 가중치가 **관찰**되었다”",
        "“이 장치·길이·dtype에서 이 방식으로 **측정**했을 때 지연이 줄었다”",
        "“teacher-forced NLL과 greedy exact match를 **따로** 보고한다”",
        "“heatmap은 관찰 자료 — 인과 설명은 추가 **검증**이 필요하다”"]},
    takeaway="사실 · 관찰 · 가설을 분리하면 연구와 강의가 모두 명확해진다",
    notes="강의와 보고서에서 쓰는 문장의 형식을 바꾸는 연습입니다. '이해한다', '항상'처럼 검증 범위를 넘는 표현 대신, 어떤 입력·장치·"
          "조건에서 무엇을 관찰·측정했는지를 씁니다. Attention 가중치에는 V의 크기와 방향, output projection, residual과 후속 층도 "
          "관여하므로 큰 가중치 하나로 인과를 결론 내리지 않습니다.")

d.quiz("개념 확인 11–14", [
    ("FFN은 어떤 계산인가? (A) 위치 간 Value 가중합 (B) 시간 step 순환 갱신 (C) 각 위치 특징의 비선형 변환",
     "C. 동일 FFN을 각 위치에 적용 — 입력에 문맥이 있을 수 있지만 FFN 자체는 새 위치 결합을 하지 않는다."),
    ("LayerNorm(d)의 전형적인 정규화 범위는? (A) 각 token의 d개 특징 (B) Batch 전체의 같은 특징 (C) token ID 번호",
     "A. (B,N,d) 입력이면 마지막 d축의 평균·분산."),
    ("위치·mask가 없는 self-attention에서 입력 순서를 섞으면? (A) 출력이 완전히 같다 (B) 출력도 같은 순열로 섞인다 (C) 0이 된다",
     "B. SA(PX) = P·SA(X), 순열 등변성 — 불변성과 구분."),
    ("CrossEntropyLoss에 일반적으로 전달하는 값은? (A) softmax를 두 번 한 확률 (B) argmax token ID (C) 정규화 전 logits",
     "C. logits를 전달하고 PAD 제외(ignore_index)와 class 축을 확인."),
], lead="답을 고르고, 왜 다른 보기가 틀렸는지 계산으로 설명한다",
    notes="원자료 개념 확인 11–14번입니다. 정답보다 틀린 보기가 왜 틀렸는지 계산 언어로 설명하게 합니다.")

d.quiz("개념 확인 15–18", [
    ("병렬 학습과 자기회귀 생성은? (A) 동시에 성립할 수 있다 (B) 서로 모순이다 (C) 둘 다 미래 정답이 필요하다",
     "A. 학습은 정답 prefix가 주어져 위치별 병렬, 생성은 다음 입력이 아직 없어 순차."),
    ("d를 고정하고 N을 2배로 하면 주요 항은? (A) 모두 4배 (B) Attention 곱셈 항 4배, 투영·FFN 항 2배 (C) 모두 2배",
     "B. N²d와 Nd² 항이 함께 있다. 실제 시간에는 overhead·kernel 특성도 작용."),
    ("KV Cache가 하는 일은? (A) 미래 정답을 미리 저장 (B) Attention을 제거 (C) 과거 위치의 K/V 재계산을 줄임",
     "C. 새 Query의 문맥 참조와 자기회귀 루프는 남는다."),
    ("큰 Attention 가중치를 관찰했다면? (A) 큰 참조 비중이 '관찰'되었다고 말하고 인과는 추가 검증 (B) 유일한 원인 (C) 사람처럼 이해",
     "A. V·output projection·residual·후속 층도 관여 — 관찰과 인과 검증을 구분."),
], lead="16번은 앞의 비용 막대그래프, 17번은 KV Cache 그림으로 돌아가 확인",
    notes="원자료 개념 확인 15–18번입니다. 16번은 4Nd² + 2N²d + 2Nd·d_ff 식에 N 대신 2N을 넣어 직접 확인하게 합니다.")

# --- 마지막 설명 과제 + 기호 사전 (custom)
s = d.blank("마지막 설명 과제와 기호 사전",
            notes="이번 주 과제이자 과정의 마지막 과제입니다. 빈 종이에 입력 ID부터 다음 토큰까지 그리고 각 구간의 shape, 학습 파라미터, "
                  "mask를 적은 뒤 학습과 생성의 차이를 다른 사람에게 설명합니다. 설명 중 막힌 위치가 복습할 장입니다. 그림에는 입력·출력 "
                  "shape, 학습되는 파라미터, 정보가 이동하는 방향, mask가 막는 연결 네 가지를 반드시 적습니다. 오른쪽 기호 사전으로 "
                  "표기를 통일합니다. 'Layer'가 block 전체인지 sublayer인지, 0-based인지 1-based인지도 명시하게 합니다.")
d.lead(s, "이번 주 과제: 빈 종이에 전체 흐름을 그리고, 다른 사람에게 설명하기")
steps = ["입력 ID", "Embedding\n+ PE", "Encoder\n× L", "Decoder\nself (causal)", "Cross-attn\nK,V = E",
         "FFN", "logits\n(B,T,|V|)", "다음 토큰"]
n = len(steps)
ag = 0.22
bw = (W - ag * (n - 1)) / n
for i, t in enumerate(steps):
    bx = X0 + i * (bw + ag)
    b = d.box(s, bx, 1.8, bw, 0.95, fill=ACCENT_BG if i == n - 1 else MINT,
              line=ACCENT if i == n - 1 else None)
    d.text_in(b, t.split("\n"), size=13, bold=True, color=ACCENT if i == n - 1 else TEAL, align="c", margin=0.04)
    if i < n - 1:
        d.arrow(s, bx + bw + 0.02, 2.275, bx + bw + ag - 0.02, 2.275)
panel(s, X0, 3.0, 5.4, 3.95, "각 구간에 적을 네 가지", [
    "입력·출력 **shape**",
    "학습되는 **파라미터** (W와 입력별 A를 구분)",
    "정보가 이동하는 **방향**",
    "**mask**가 막는 연결",
    "마지막: 학습(teacher forcing)과 생성(자기회귀)의 차이 설명",
    "용어 확인: 'Layer'는 block인지 sublayer인지, token은 문자열 조각인지 patch인지"], size=15)
syms = [("B", "배치 크기"), ("S / T", "source / target 길이"), ("N", "일반 시퀀스 길이"),
        ("L", "층 수"), ("d", "모델 차원 (d_model)"), ("H / dₕ", "head 수 / head 차원"),
        ("d_ff", "FFN 내부 폭"), ("|V|", "어휘 크기 (Value V와 구분)"), ("E / D", "Encoder 출력 / Decoder 표현"),
        ("A / M", "Attention 가중치 / 더하는 mask")]
gx = X0 + 5.7
gw = (X1 - gx - 0.2) / 2
gh = 0.7
for k, (sym, mean) in enumerate(syms):
    r, c = divmod(k, 2)
    x = gx + c * (gw + 0.2)
    y = 3.0 + r * (gh + 0.11)
    d.box(s, x, y, 1.05, gh, fill=TEAL)
    d.text(s, x, y, 1.05, gh, sym, size=15, bold=True, color=WHITE, align="c", anchor="m", min_size=10)
    d.box(s, x + 1.1, y, gw - 1.1, gh, fill=MINT)
    d.text(s, x + 1.15, y, gw - 1.2, gh, mean, size=14, anchor="m", min_size=10)

d.image("과정 전체의 계보: 1943 → 2017 → 이후", img("genealogy.png"),
        lead="여섯 질문이 여섯 주를 이끌었다 — 각 구조는 앞 구조의 한계에 대한 답",
        caption="실제 연구사는 서로 영향을 주고 병행한 여러 경로의 합이다 (CNN → RNN → Transformer로 '교체'된 것이 아님)",
        notes="과정 전체를 한 장으로 되돌아봅니다. 규칙을 다 쓰지 않고 배울 수 있을까(1주, 학습·Tensor) → 직선으로 안 되는 문제는"
              "(2주, Perceptron과 MLP·역전파) → 공간 구조는(3주, CNN·ResNet·정규화) → 순서와 먼 기억은(4주, RNN·LSTM·Seq2Seq) → "
              "필요할 때 원문을 찾아보면(5주, Attention) → 참조만으로 시퀀스 표현을 만들면(6주, Transformer)의 순서였습니다. "
              "연도는 대표 논문 기준이며 역전파가 1986년에 처음 발명된 것은 아니고, Word2Vec이 embedding을 처음 만든 것도 아닙니다. "
              "2017년 이후 칸은 확장 학습으로 구분합니다.")

d.table("다음 학습 방향과 읽을 원문", ["관심 방향", "이어서 볼 것", "원문 (읽을 부분)"], [
    ["원형 다시 읽기", "구조 · 계산 경로 · 학습 recipe",
     "Vaswani 등 2017 [22]: Fig 1–2·§3 구조, §4 경로·계산, §5 학습, §6.2 변형"],
    ["학습 안정성", "Residual · LayerNorm · Pre-LN", "He 등 2015 [19], Ba 등 2016 [20], Xiong 등 2020 [25]"],
    ["언어 생성", "Decoder-only · KV Cache · GQA", "Radford 등 2018 [32], Ainslie 등 2023 [37]"],
    ["표현 사전학습", "Encoder-only · text-to-text", "Devlin 등 2018 [31], Raffel 등 2019 [33]"],
    ["시각 표현", "patch · 공간 위치 · CLS와 pooling", "Dosovitskiy 등 2020 [34] §3, Fig 1"],
    ["생성 모델", "diffusion 목표 · timestep conditioning", "Peebles & Xie 2022 [41] §3, Fig 3"],
    ["모델 최적화", "실제 병목 · kernel · 메모리 이동", "Dao 등 2022 [38], Shazeer 2020 [36], Su 등 2021 [35]"],
    ["해석", "attention은 설명인가", "Jain & Wallace 2019 [39], Wiegreffe & Pinter 2019 [40]"],
], col_widths=[2.2, 3.8, 6.2], size=16,
    lead="읽는 순서: Seq2Seq → Bahdanau Attention → Attention Is All You Need → Residual / LayerNorm → 공식 구현",
    notes="관심사에 따라 다음 방향을 고릅니다. 언어 생성이면 Decoder-only와 KV Cache, 시각이면 patch·공간 위치·CLS와 pooling, "
          "최적화면 실제 병목·kernel·메모리 이동, 생성 모델이면 diffusion 목표와 timestep conditioning입니다. 처음부터 모든 논문의 "
          "모든 실험을 읽기보다 질문에 맞는 그림·식·절을 지정해 읽습니다. 공식 구현 참고: TensorFlow Transformer 튜토리얼 [26], "
          "PyTorch SDPA·MultiheadAttention·CrossEntropyLoss·LayerNorm 문서 [27–30]. API 문서는 버전마다 바뀔 수 있으므로 "
          "설치한 버전에서 mask와 shape 규약을 다시 확인합니다. 원자료의 식·손계산·toy model 결과는 교육용 재구성이며 원논문의 실험 결과가 아닙니다.")

d.summary("오늘의 정리 · 과정의 정리", [
    "FFN은 위치별 비선형 변환, Residual은 표현 보존 통로, LayerNorm은 토큰의 d축 정규화 — 원형은 Post-LN",
    "Target을 한 칸 shift하고 causal mask(Softmax 전 −∞)로 막으면 정답 누출 없이 병렬 학습할 수 있다",
    "층당 파라미터 ≈ 4d² + 2d·d_ff: Encoder ≈ 12d², Decoder ≈ 16d² — 원형 Base 약 65M",
    "학습은 PAD 제외 NLL 최소화 · 원논문: Adam(0.9, 0.98), warm-up 4000, dropout·label smoothing 0.1",
    "생성은 자기회귀 — KV Cache(2·L·B·N·d·bytes)는 재계산을 줄이지만 순차성과 문맥 참조 비용은 남는다",
    "BERT·GPT·T5·ViT·DiT는 같은 부품을 다른 mask·목표·token으로 조합한 것 — 원형 표에 꽂아 비교한다",
], next_week="과정 종료 — 최종 프로젝트 발표와 구술 평가: 처음 보는 d·H·S·T로 입력부터 logits까지 설명하기",
    notes="오늘은 2017년 원형을 입력 ID부터 다음 토큰까지 완성했고, 학습과 추론의 차이, 비용 분석, 후속 구조 읽는 법까지 "
          "다뤘습니다. 6주 과정 전체로 보면 '왜 이 계산이 필요한가?'라는 질문에 답하며 Tensor에서 Transformer까지 왔습니다. "
          "다음 주는 없으며, 최종 프로젝트 발표와 구술 평가로 과정을 마무리합니다.")

d.save(OUT)
print("saved", os.path.abspath(OUT), "content slides:", d.n)
