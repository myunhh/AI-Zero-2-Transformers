"""Week 6 — Transformer 완성: 참조만으로 시퀀스 모델을 만들면? (조립 · 학습 · 생성 · 그 이후)"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from deckkit import *  # noqa

A = lambda p: os.path.join(HERE, "assets", p)
OUT = os.path.join(HERE, "..", "lectures", "week06_transformer_complete.pptx")

d = Deck(6, "Transformer 완성: 조립·학습·생성", date="2026-11-09")

# ============================================================ 도입
d.question("참조만으로\n시퀀스 모델을 만들면?",
           "2017 → · FFN · Residual · LayerNorm · Mask · 학습 · 생성 · 그 이후",
           notes="마지막 주. 지난주의 attention 블록에 FFN, residual, LayerNorm을 붙여 층을 완성하고, mask와 teacher forcing으로 정답을 훔쳐보지 않게 학습시키고, "
                 "토큰을 하나씩 생성한다. 그리고 비용을 계산하고, 직접 실험하는 법과 Transformer 이후의 길을 본다. 1주차의 도착점 그림을 오늘 모두 채운다.")

d.bridge(["**Attention**: 점수 → softmax → 가중합", "Q · K · V와 **Multi-head**, shape (B, H, N, d_h)", "Self-attention + **위치 인코딩**"],
         ["attention만으로는 **토큰별 비선형 변환**이 없다", "깊게 쌓기 · 정답을 **훔쳐보지 않고** 학습하기 · **생성**하기"],
         ["**참조만으로 시퀀스 모델을 만들면?**", "조립 → 학습 → 생성 → 그 이후"])

d.roadmap(["Encoder 한 층 완성: FFN · Residual · LayerNorm", "Decoder: 정답을 훔쳐보지 않고 배우기",
           "입력부터 logits까지, 파라미터 세기", "학습: 확률을 정답 쪽으로", "생성과 비용: KV Cache · 연산량 · 메모리",
           "직접 실험하기", "Transformer 이후, 그리고 과정 마무리"],
          ["Encoder / Decoder 한 층의 **모든 sublayer와 shape**을 그린다",
           "**shift + causal mask**가 정답 누출을 막는 방식을 설명한다",
           "파라미터 수와 연산량을 **d, N, d_ff로 유도**한다",
           "학습(병렬)과 **생성(자기회귀)**의 차이, **KV Cache**의 역할을 설명한다",
           "구조의 필요성을 확인하는 **통제된 실험**을 설계한다"])

d.glossary([["FFN", "토큰마다 같은 2층 MLP (d → d_ff → d)", "각자 자리에서 하는 정리"],
            ["Post-LN / Pre-LN", "LayerNorm을 잔차 합 뒤 / sublayer 앞에 두는 배치", "정리를 먼저 할까, 나중에 할까"],
            ["Teacher forcing", "학습 때 이전 정답 토큰을 입력으로 주는 방식", "정답지를 한 칸씩 보여 주며 연습"],
            ["Causal mask", "미래 위치를 참조하지 못하게 점수에 −∞", "아직 안 쓴 답안 가리기"],
            ["Logits", "softmax 전 어휘별 점수 (B, T, |V|)", "후보별 득점"],
            ["NLL · Perplexity", "정답 토큰의 −log 확률 평균 · 그 exp", "평균 놀람 · 헷갈리는 후보 수"],
            ["자기회귀 생성", "방금 만든 토큰을 다음 입력으로 붙여 반복", "한 글자씩 받아쓰기"],
            ["KV Cache", "과거 토큰의 K, V를 저장해 재사용", "이미 쓴 메모 다시 보기"]])

# ============================================================ Part 1
d.part(1, "Encoder 한 층 완성: FFN · Residual · LayerNorm", "Attention이 전부가 아니다 — 위치별 변환과 깊은 계산의 기반을 조립한다")

s = d.slide("오늘 채울 그림", lead="Encoder 층 = self-attention + FFN, 각각 잔차 합 + LayerNorm. Decoder 층은 여기에 masked · cross가 더해진다",
            stage="도입",
            notes="원형 Transformer의 한 층 그림. Encoder 층: (1) multi-head self-attention, (2) FFN — 각 sublayer 뒤에 dropout, 잔차 합, LayerNorm(Post-LN). "
                  "Decoder 층: (1) masked self-attention, (2) cross-attention, (3) FFN. 맨 위 출력 head가 어휘 점수를 낸다. "
                  "원형 base 설정: L = 6 + 6층, d = 512, H = 8, d_h = 64, d_ff = 2048, dropout 0.1, label smoothing 0.1.")
L, R = s.cols(0.58)
s.image(A("week6/encdec_layer.png"), L)
s.table(["원형 base 설정", "값"], [["층 수 (Encoder / Decoder)", "6 / 6"], ["d_model / d_ff", "512 / 2048"], ["head 수 H / d_h", "8 / 64"],
                                  ["dropout / label smoothing", "0.1 / 0.1"]], Box(R.x, R.y, R.w, 2.3), size=15, align="lc")
s.bullets(["오늘은 이 그림의 **모든 상자**를 채운다", "1주차 ‘도착점’ 그림이 바로 이것"], Box(R.x, R.y + 2.55, R.w, R.h - 2.55), size=16)

s = d.slide("FFN: 모은 정보를 토큰마다 변환", lead="FFN(x) = max(0, xW1 + b1)W2 + b2 — 2주차 MLP를 토큰마다 똑같이 적용", stage="계산",
            notes="원형 base: d = 512에서 d_ff = 2048로 넓혔다가 다시 512로. 같은 FFN 파라미터를 모든 위치에 쓰지만 층마다는 별개. "
                  "FFN 자체는 한 위치의 특징 축만 변환하며 다른 위치와 섞지 않는다(개념 확인 11). 위치 간 결합은 attention의 A·V가 한다. "
                  "'attention은 토큰 섞기, FFN은 특징 변환'은 좋은 첫 설명이지만, attention의 투영도 특징을 바꾼다는 점을 함께 기억한다. "
                  "후속 모델은 ReLU 대신 GELU, SwiGLU 등을 쓴다.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("FFN(x) = max(0, x W1 + b1) W2 + b2      d → d_ff → d", top, size=22)
L, R = bot.cols(0.55, gap=0.4)
s.table(["", "Attention (A · V)", "FFN"], [["하는 일", "**위치 간** 정보 결합", "**각 위치**의 비선형 특징 변환"],
                                          ["다른 토큰과 섞나?", "예", "**아니오**"], ["shape", "(B, N, d) 유지", "(B, N, d) → (B, N, d_ff) → (B, N, d)"],
                                          ["파라미터", "W_Q · W_K · W_V · W_O", "W1 (d × d_ff), W2 (d_ff × d)"]], L, size=14, widths=[1.5, 2.4, 3.0])
s.bullets(["2주차 **MLP 그대로**, 토큰마다 적용", "같은 층 안에선 모든 위치가 **같은 FFN**", "층마다는 **별개** 파라미터",
           "base: 512 → **2048** → 512", "후속: GELU · SwiGLU 등"], R)

s = d.slide("Residual: 기존 표현을 보존하는 통로", lead="x + Sublayer(x) — 더하려면 shape이 같아야 하므로 모든 sublayer가 d로 돌아온다", stage="아이디어",
            notes="3주차 ResNet의 잔차 연결 그대로. 각 sublayer(attention, FFN)는 입력에 더할 '변화량'을 만든다. "
                  "원소별로 더하려면 입력과 출력 shape이 같아야 한다 — 그래서 attention의 W_O와 FFN의 W2가 모두 d로 돌아온다. "
                  "잔차 경로는 깊은 모델의 최적화를 돕는 설계지만, 모든 깊이·설정에서 안정성을 보장하지는 않는다.")
rest = s.cards([{"head": "식", "body": ["y = x + Sublayer(x)", "Sublayer = attention 또는 FFN"]},
                {"head": "shape 조건", "body": ["더하려면 **같은 shape**", "→ W_O, W2가 모두 **d**로 복귀"]},
                {"head": "3주차 연결", "tone": "accent", "body": ["ResNet (2015)의 잔차 연결", "기울기·정보가 흐르는 **지름길**"]}],
               cols=3, body_size=17, head_size=18)
s.callout("잔차 경로는 최적화를 **돕는** 설계 — 모든 깊이·설정에서 안정성을 **보장**하지는 않는다.",
          Box(rest.x, rest.y + 0.1, rest.w, 0.8), kind="tip", size=16)

s = d.slide("LayerNorm은 어느 축을 정규화하나", lead="(B, N, d) 입력에서 LayerNorm(d)는 토큰 하나의 d개 특징으로 평균·분산을 낸다", stage="계산",
            notes="토큰 하나 x ∈ ℝ^d에서 평균과 분산을 구해 정규화하고, 학습되는 γ, β로 scale·shift. batch나 sequence 전체를 한꺼번에 정규화하지 않는다(개념 확인 12). "
                  "예: x = (1, 2, 3, 4) → 평균 2.5, 분산 1.25 → (−1.34, −0.45, 0.45, 1.34). γ, β가 적용되므로 최종 출력이 항상 평균 0·분산 1일 필요는 없다. "
                  "γ, β는 d차원 벡터로 모든 토큰이 공유한다(토큰마다 별개 아님). 3주차 BatchNorm과 축이 다르다.")
L, R = s.cols(0.55)
s.image(A("week6/ln_axis.png"), L)
s.formula("LN(x) = γ ⊙ (x − μ) / √(σ² + ε) + β", Box(R.x, R.y, R.w, 0.9), size=17)
s.table(["x", "μ", "σ²", "(x − μ) / σ"], [["(1, 2, 3, 4)", "2.5", "1.25", "(−1.34, −0.45, 0.45, 1.34)"]],
        Box(R.x, R.y + 1.15, R.w, 1.0), size=13, align="cccc")
s.bullets(["**토큰마다** d개 값으로 μ, σ 계산", "γ, β (d차원)는 학습되고 모든 토큰이 **공유**", "batch 전체가 아니다 (≠ BatchNorm)"],
          Box(R.x, R.y + 2.4, R.w, R.h - 2.4), size=15)

s = d.slide("Post-LN vs Pre-LN", lead="원형은 잔차 합 ‘뒤’에 정규화(Post-LN), 후속 모델은 sublayer ‘앞’에(Pre-LN)", stage="검증",
            notes="Post-LN (2017 원형): y = LN(x + F(x)). Pre-LN: y = x + F(LN(x)), 보통 stack 끝에 최종 LN을 하나 더 둔다. "
                  "Pre-LN에서는 잔차 경로가 LN을 거치지 않아 항등 경로가 깨끗하다(3주차 ∂y/∂x = I + ∂F/∂x). 원형 Post-LN은 뒤에 LN이 있어 전체 미분을 그렇게 쓸 수 없다. "
                  "정규화 위치는 초기 기울기와 학습 안정성에 영향을 준다. 원자료 주의: 비교할 때 optimizer, 학습률, warm-up, 깊이를 통제해야 하며 한 설정으로 보편적 우열을 말하지 않는다.")
L, R = s.cols(0.55)
s.image(A("week6/postpre_ln.png"), L)
s.table(["", "Post-LN (원형)", "Pre-LN (후속)"], [["식", "LN(x + F(x))", "x + F(LN(x))"], ["잔차 경로", "LN을 거친다", "**깨끗한** 항등 경로"],
                                              ["stack 끝", "—", "최종 LN 추가가 흔함"]], Box(R.x, R.y, R.w, 2.1), size=14, align="lcc")
s.callout("==주의== 비교할 때 optimizer · 학습률 · **warm-up** · 깊이를 통제한다. 한 설정의 결과로 보편적 우열을 말하지 않는다.",
          Box(R.x, R.y + 2.35, R.w, 1.4), kind="warn", size=15)

s = d.slide("Encoder 한 층: 식과 shape", lead="입력과 출력이 모두 (B, S, d) — 그래서 같은 설계를 L번 쌓을 수 있다", stage="정리",
            notes="Encoder 한 층(원형 Post-LN, dropout 포함): U = LN(X + Dropout(MHA(X, X, X))), X′ = LN(U + Dropout(FFN(U))). "
                  "MHA(·)는 내부 투영을 포함한 모듈 표기. 각 층의 입출력은 (B, S, d). 6층을 쌓아 최종 출력 E를 얻는다. "
                  "'같은 층을 반복'은 같은 설계라는 뜻이지 가중치 공유가 아니다 — 층마다 파라미터는 별개.")
top, bot = s.area.top(1.5, gap=0.3)
s.formula(["U  = LN( X + Dropout( MHA(X, X, X) ) )", "X′ = LN( U + Dropout( FFN(U) ) )"], top, size=22)
mid, low = bot.top(1.8, gap=0.3)
s.flow([{"head": "X", "body": "(B, S, d)"}, {"head": "Self-attention", "body": "+ 잔차 · LN"}, {"head": "FFN", "body": "+ 잔차 · LN"},
        {"head": "X′", "body": "(B, S, d)", "tone": "dark"}, {"head": "× 6층", "body": "최종 출력 **E**", "tone": "accent"}], mid,
       body_size=15, head_size=17, gap=0.35)
s.bullets(["Self-attention으로 **다른 위치의 정보를 모으고**, FFN으로 **각 위치의 표현을 바꾼다**",
           "‘같은 층 반복’ = 같은 설계일 뿐, **층마다 파라미터는 별개**"], low, size=16)

# ============================================================ Part 2
d.part(2, "Decoder: 정답을 훔쳐보지 않고 배우기", "정답 문장을 입력으로 주면서도, 자기 정답을 보지 못하게 하려면?")

s = d.slide("문제: 정답을 통째로 주면?", lead="학습 때 정답 문장 전체를 Decoder에 넣고 한 번에 계산하면 — 각 위치가 자기 정답을 볼 수 있다", stage="문제",
            notes="학습을 빠르게 하려면 정답 문장 전체를 한 번에 넣어 모든 위치를 병렬로 계산하고 싶다(RNN처럼 한 칸씩 기다리지 않고). "
                  "그런데 self-attention은 모든 위치를 볼 수 있으므로, 'am'을 예측해야 하는 위치가 입력 안의 'am'을 그대로 보고 베낄 수 있다 — 정답 누출. "
                  "그러면 훈련 손실은 금방 0이 되지만 실제 생성(정답이 없을 때)에서는 아무것도 못 한다. 해결책 두 가지: 입력을 한 칸 밀기(shift) + 미래 가리기(causal mask).")
rest = s.cards([{"head": "원하는 것", "body": ["정답 문장 전체를 넣고", "모든 위치를 **한 번에** (병렬) 학습"]},
                {"head": "그런데", "tone": "accent", "body": ["self-attention은 **모든 위치**를 본다", "‘am’을 맞혀야 할 위치가 입력의 ‘am’을 **베낀다**"]},
                {"head": "결과", "tone": "plain", "body": ["훈련 손실은 금방 0", "실제 생성에서는 **아무것도 못 한다**"]}],
               cols=3, body_size=16, head_size=18)
s.callout("해결: ① 입력을 **한 칸 밀고**(shift) ② **미래를 가린다**(causal mask)", Box(rest.x, rest.y + 0.1, rest.w, 0.85), kind="key", size=18)

s = d.slide("Teacher forcing: 입력과 정답을 한 칸 어긋나게", lead="Decoder 입력 = BOS + 정답[:-1], 예측 정답 = 정답 + EOS", stage="아이디어",
            notes="'I am a student'를 목표로 할 때, Decoder 입력은 [BOS, I, am, a, student], 예측 정답은 [I, am, a, student, EOS]. "
                  "학습 때 이전 예측 대신 이전 정답을 입력으로 주는 것이 teacher forcing. "
                  "입력이 'I'인 위치의 목표는 'am'이므로 현재 입력(대각선)을 보는 것은 괜찮다(개념 확인 08). 문제는 '뒤에 있는' 입력을 보는 것 → causal mask. "
                  "BOS·EOS·PAD의 실제 이름과 ID는 tokenizer마다 다르다.")
top, bot = s.area.top(2.9, gap=0.25)
s.image(A("week6/shift.png"), top)
s.bullets(["학습 때 **이전 정답**을 입력으로 = **teacher forcing**",
           "입력 ‘I’ 위치의 목표는 ‘am’ → 현재 입력(**대각선**)은 봐도 된다 (개념 확인 08)",
           "문제는 **뒤쪽** 입력을 보는 것 → 다음 장의 causal mask"], bot, size=16)

s = d.slide("Causal mask: softmax 전에 −∞", lead="미래 칸의 점수에 −∞를 더하면 exp(−∞) = 0 — 0을 더하거나 0으로 바꾸면 막히지 않는다", stage="계산",
            notes="허용되지 않는 점수에 −∞를 더하면 softmax 후 가중치가 정확히 0. 점수를 0으로 바꾸면 exp(0) = 1이라 오히려 비중을 받는다(개념 확인 07). "
                  "5주차 4토큰 예제에 causal mask를 적용하면 Query B 행: [0.33, 0.67, 0, 0]. 원래 [0.14, 0.29, 0.29, 0.29]에서 미래(C, D) 비중이 사라지고 나머지가 재정규화된다. "
                  "실수 연산에서는 −∞ 대신 큰 음수를 쓰기도 하는데, dtype(FP16 등)과 수치 안정성을 고려해야 한다.")
L, R = s.cols(0.5)
s.image(A("week6/causal_mask.png"), L)
s.formula("A = softmax( QKᵀ/√d_h + M ),  M = −∞ (미래)", Box(R.x, R.y, R.w, 0.95), size=16)
s.table(["Query B의 행", "A", "B", "C", "D"], [["mask 없음", "0.14", "0.29", "0.29", "0.29"],
                                            ["−∞ mask", "**0.33**", "**0.67**", "0", "0"], ["0으로 바꿈", "exp(0) = 1 → **새어 나감**", "", "", ""]],
        Box(R.x, R.y + 1.2, R.w, 1.7), size=14, align="lcccc", highlight=[2])
s.bullets(["mask는 **softmax 전**에", "FP16에서는 큰 음수의 **dtype** 주의"], Box(R.x, R.y + 3.1, R.w, R.h - 3.1), size=15)

s = d.slide("Causal · Padding · Loss mask는 서로 다르다", lead="무엇을 막고, 어디에 적용하나 — 이름이 비슷해도 역할이 다르다", stage="정리",
            notes="원자료의 표. causal mask는 미래 target 참조를 막고 Decoder self-attention 점수에 적용. source key padding mask는 source의 PAD 위치 참조를 막고 Encoder self-attention과 cross-attention에. "
                  "target key padding mask는 Decoder self-attention에. loss ignore mask는 PAD 정답을 손실과 지표에서 제외. "
                  "주의 1: key padding mask는 PAD 위치 Query의 출력을 0으로 만들지 않는다 — 그 결과를 loss·pooling·평가에 포함하지 않도록 따로 처리. "
                  "주의 2: PyTorch scaled_dot_product_attention의 boolean mask에서 True는 '참조 허용', nn.MultiheadAttention의 attn_mask·key_padding_mask에서 True는 '참조 차단' — 그대로 복사하면 뜻이 뒤집힌다.")
s.table(["mask", "무엇을 막나", "어디에 적용하나"],
        [["Causal", "미래 target 위치 참조", "Decoder self-attention 점수"], ["Source key padding", "source의 PAD 위치 참조", "Encoder self-attention · cross-attention"],
         ["Target key padding", "target의 PAD 위치 참조", "Decoder self-attention"], ["Loss ignore", "PAD 정답을 손실에 포함", "cross-entropy · 지표 집계"]],
        Box(s.area.x, s.area.y, s.area.w, 2.6), widths=[2.4, 3.8, 4.8], size=15)
L, R = Box(s.area.x, s.area.y + 2.9, s.area.w, s.area.h - 2.9).cols(0.5, gap=0.4)
s.callout("padding mask는 PAD **Query의 출력**을 0으로 만들지 않는다 → loss · pooling · 평가에서 따로 제외", L, kind="tip", size=15)
s.callout("==API 주의== `F.scaled_dot_product_attention`: True = **허용** / `nn.MultiheadAttention`: True = **차단**", R, kind="warn", size=15)

s = d.slide("Cross-attention: Decoder가 원문을 참조한다", lead="Q는 Decoder에서, K · V는 Encoder 최종 출력 E에서 — 점수 표는 T × S", stage="아이디어",
            notes="4주차 Seq2Seq의 병목을 푼 5주차 attention이 바로 여기 들어간다. Decoder의 각 위치가 Query가 되어 source 전체(E)를 참조한다. "
                  "점수 표는 T×S, 출력 길이는 Query 수 T. 모든 Decoder 층의 cross-attention은 같은 최종 E를 참조하지만 각 층에 자기만의 투영 가중치가 있다. "
                  "층마다 Encoder를 다시 실행하는 구조가 아니다 — Encoder는 한 번만 실행한다. cross-attention에는 causal mask가 필요 없다(source 전체를 봐도 target 누출이 아님), source padding mask만.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("CrossAttn(D, E) = softmax( (D W_Q)(E W_K)ᵀ / √d_h ) (E W_V)", top, size=20)
rest = s.cards([{"head": "출처", "body": ["Q ← Decoder 표현 (T개)", "K, V ← Encoder 최종 출력 **E** (S개)"]},
                {"head": "shape", "body": ["점수 표 **T × S**", "출력 길이 = Query 수 **T**"]},
                {"head": "구조", "tone": "accent", "body": ["Encoder는 **한 번만** 실행", "모든 Decoder 층이 같은 E를 참조", "층마다 자기 **투영 가중치**"]}],
               bot, cols=3, body_size=16, head_size=18)
s.callout("mask: causal은 **필요 없다** (source는 target의 미래가 아님) — source padding mask만.",
          Box(rest.x, rest.y + 0.1, rest.w, 0.8), kind="tip", size=16)

s = d.slide("Decoder 한 층과 출력 head", lead="masked self → cross → FFN, 그리고 맨 위에서 d → |V| 점수(logits)", stage="정리",
            notes="Decoder 한 층: (1) masked self-attention + 잔차 + LN, (2) cross-attention(E 참조) + 잔차 + LN, (3) FFN + 잔차 + LN. 입출력 (B, T, d). "
                  "출력 head: logits = D W_vocab (+ b), W_vocab은 d × |V|, logits (B, T, |V|). softmax를 하면 다음 토큰 확률. "
                  "원논문은 source/target 임베딩과 출력 선형 변환의 가중치를 공유(weight tying)한다고 설명 — 공유 어휘 등 조건이 맞아야 하는 설계 선택이지 모든 Transformer의 필수는 아니다.")
top, bot = s.area.top(1.95, gap=0.3)
s.formula(["Z1 = LN( Y + MaskedSelfAttn(Y) )", "Z2 = LN( Z1 + CrossAttn(Z1, E) )", "Y′ = LN( Z2 + FFN(Z2) )"], top, size=19)
mid, low = bot.top(1.7, gap=0.3)
s.flow([{"head": "Decoder 출력", "body": "(B, T, d)"}, {"head": "Linear W_vocab", "body": "d × |V|"}, {"head": "logits", "body": "(B, T, |V|)", "tone": "accent"},
        {"head": "softmax", "body": "다음 토큰 확률", "tone": "dark"}], mid, body_size=15, head_size=17)
s.bullets(["**weight tying**: 임베딩과 출력 투영의 가중치 공유 — 조건이 맞을 때의 설계 선택",
           "logits = softmax **전** 점수 → CrossEntropyLoss에는 logits를 넣는다 (2주차)"], low, size=16)

# ============================================================ Part 3
d.part(3, "입력부터 logits까지, 파라미터 세기", "한 샘플을 끝까지 따라가면 shape은 어떻게 변하나? 파라미터는 몇 개인가?")

s = d.slide("한 샘플을 끝까지 추적하기", lead="B = 2, S = 5, T = 3, d = 8, H = 2, |V| = 16 — 길이가 바뀌는 곳은 어디인가?", stage="계산",
            notes="원자료의 추적 표. source ID (2, 5) → 임베딩 + PE (2, 5, 8) → Encoder 최종 E (2, 5, 8). target 입력 ID (2, 3) (BOS 포함, 한 칸 민 입력) → (2, 3, 8). "
                  "Decoder self-attention 표 (2, 2, 3, 3) (causal mask), cross-attention 표 (2, 2, 3, 5) (source 5개 참조), Decoder 출력 (2, 3, 8), logits (2, 3, 16). "
                  "표준 블록은 source/target 길이를 보존한다. 길이가 섞이는 곳은 cross-attention 점수 표(T×S)뿐이고, 출력은 Query 길이 T.")
s.table(["단계", "shape", "메모"],
        [["source ID", "(2, 5)", "padding된 입력"], ["source 임베딩 + PE", "(2, 5, 8)", "8차원 표현"],
         ["Encoder 최종 출력 E", "(2, 5, 8)", "입력의 문맥 표현"], ["target 입력 ID", "(2, 3)", "BOS 포함, 한 칸 민 입력"],
         ["Decoder self-attention 표", "(2, 2, 3, 3)", "causal mask 적용"], ["Cross-attention 표", "(2, 2, 3, **5**)", "source 5개 위치 참조"],
         ["Decoder 최종 출력", "(2, 3, 8)", "Query 위치 수 **3** 유지"], ["logits", "(2, 3, 16)", "위치마다 16개 후보 점수"]],
        widths=[3.4, 2.4, 4.6], size=15, align="lcl", highlight=[5])

s = d.slide("파라미터 수를 직접 유도하기", lead="attention 4d² + FFN 2d·d_ff — d_ff = 4d면 Encoder 층 ≈ 12d², Decoder 층 ≈ 16d²", stage="계산",
            notes="bias·Norm·임베딩 제외. self-attention의 W_Q, W_K, W_V, W_O = 4d². FFN = 2·d·d_ff = 8d²(d_ff = 4d). Encoder 층 ≈ 12d², Decoder 층은 cross-attention이 더해져 ≈ 16d². "
                  "base (d = 512, d_ff = 2048): Encoder 층 3.15M, Decoder 층 4.19M, 6 + 6층 = 44.0M. 공유 어휘 약 37,000 × 512 = 18.9M 임베딩(공유) → 합 약 63M. 논문 보고 65M과 가깝다(편향·Norm 등 차이). "
                  "숫자를 외우기보다 다른 d와 층 수에도 같은 계산을 할 수 있어야 한다.")
top, bot = s.area.top(1.05, gap=0.3)
s.formula("층당 ≈ 4d² (attention) + 2·d·d_ff (FFN)", top, size=24)
L, R = bot.cols(0.55, gap=0.4)
s.table(["항목 (d = 512, d_ff = 2048)", "파라미터"], [["Encoder 층 (≈ 12d²)", "3.15M"], ["Decoder 층 (≈ 16d², cross 포함)", "4.19M"],
                                                   ["6 + 6층", "44.0M"], ["공유 임베딩 (≈ 37k × 512)", "18.9M"], ["합계 (bias · Norm 제외)", "**≈ 63M** (논문 65M)"]],
        L, size=15, align="lc", highlight=[4])
s.bullets(["d를 2배로 → 층 파라미터 **4배** (d²)", "층 수 L을 2배로 → **2배**", "attention 가중치 A는 파라미터가 **아니다**",
           "외우지 말고 **유도**할 수 있으면 된다"], R)

# ============================================================ Part 4
d.part(4, "학습: 확률을 정답 쪽으로", "구조가 계산을 정한다면, 목표와 optimizer는 무엇을 학습할지 정한다")

s = d.slide("다음 토큰의 음의 로그 가능도", lead="정답 토큰에 준 확률의 −log를 PAD 아닌 토큰 수로 평균 — 2주차 cross-entropy 그대로", stage="계산",
            notes="L = −(1/|valid|) Σ log p(y_t | y_<t, x). PAD가 아닌 토큰 수로 정규화한다. 예: 정답 'I am a student EOS'에 준 확률이 0.5, 0.4, 0.6, 0.7, 0.9라면 "
                  "−log는 0.693, 0.916, 0.511, 0.357, 0.105, 평균 0.516, perplexity = exp(0.516) ≈ 1.68. "
                  "구현: CrossEntropyLoss에는 softmax 전 logits를 넣는다(개념 확인 14). (B, T, |V|) logits를 (B·T, |V|)로, 정답을 (B·T)로 펼치고 ignore_index=PAD. "
                  "긴 시퀀스와 짧은 시퀀스를 어떤 단위로 평균하는지 집계 규칙을 명시한다.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("L = −(1 / |valid|) · Σ_t  log p(y_t | y_<t, x)", top, size=24)
L, R = bot.cols(0.55, gap=0.4)
s.table(["정답 토큰", "I", "am", "a", "student", "EOS"], [["p(정답)", "0.5", "0.4", "0.6", "0.7", "0.9"],
                                                      ["−log p", "0.693", "0.916", "0.511", "0.357", "0.105"]], Box(L.x, L.y, L.w, 1.3),
        size=14, align="cccccc")
s.bullets(["평균 NLL = **0.516**, perplexity = e^0.516 ≈ **1.68**"], Box(L.x, L.y + 1.5, L.w, 0.7), size=16)
s.callout("PAD 토큰은 분모와 분자에서 **제외** — 집계 단위(토큰 평균 / 문장 평균)를 명시한다.", Box(L.x, L.y + 2.3, L.w, 1.0), kind="tip", size=15)
s.bullets(["CrossEntropyLoss에는 **logits** (개념 확인 14)", "(B, T, |V|) → **(B·T, |V|)**", "정답 (B, T) → **(B·T)**",
           "`ignore_index = PAD`", ("loss와 accuracy 양쪽에서", 1)], R)

s = d.slide("한 학습 step의 순서", lead="batch → forward → masked CE → backward → step — 1주차 학습 루프 그대로", stage="코드",
            notes="원자료의 코드. model.train()으로 dropout을 켜고, 기울기를 지우고, source와 한 칸 민 target 입력으로 logits를 계산한다. "
                  "loss는 펼친 logits와 정답으로 cross-entropy(ignore_index=PAD). backward로 기울기, clip_grad_norm_으로 기울기 크기를 1.0으로 제한(교육용 보호 장치), step으로 갱신. "
                  "원자료 주의: 이 짧은 코드가 원논문의 학습 recipe 전체와 같다는 뜻은 아니다.")
L, R = s.cols(0.62)
s.code("model.train()\n"
       "optimizer.zero_grad(set_to_none=True)\n"
       "logits = model(source_ids, target_input_ids)  # (B, T, |V|)\n"
       "loss = F.cross_entropy(\n"
       "    logits.reshape(-1, vocab_size),   # (B*T, |V|)\n"
       "    target_labels.reshape(-1),        # (B*T,)\n"
       "    ignore_index=PAD)\n"
       "loss.backward()\n"
       "torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)\n"
       "optimizer.step()", L, size=13)
cb = s.last_code_box
s.callout("gradient clipping은 교육용 보호 장치 — 이 코드가 원논문 recipe 전체는 아니다.", Box(L.x, cb.b + 0.25, L.w, 0.8), kind="tip", size=15)
s.bullets(["1주차: forward → loss → backward → update", "`target_input_ids` = BOS + 정답[:-1]", "`target_labels` = 정답 + EOS",
           "clip: 기울기 **폭주** 방지 (4주차)"], R)

s = d.slide("왜 학습은 병렬로 할 수 있나", lead="학습 때는 정답 prefix가 모두 주어진다 — shift + mask로 모든 위치의 다음 토큰을 한 번에 예측", stage="아이디어",
            notes="학습에서는 모든 이전 정답 토큰이 이미 주어지므로, 위치별 입력을 한꺼번에 넣고 causal mask로 의존성을 제한해 여러 위치의 다음 토큰 예측을 한 번의 forward로 계산한다. "
                  "미래 정답 값이 텐서 안에 '존재'하는 것과, 해당 Query가 그것을 '참조'하는 것은 다르다 — mask가 참조를 막는다. RNN은 h_t를 위해 h_(t−1)을 기다려야 했다(4주차 ③). "
                  "생성에서는 다음 입력 토큰이 아직 정해지지 않아 자기회귀 순차성이 남는다. 둘은 모순이 아니다(개념 확인 15). "
                  "또 층 사이에는 이전 층 출력에 대한 의존이 있으므로 '모든 계산을 한 번에 병렬화한다'고 말하지 않는다.")
rest = s.cards([{"head": "학습 (teacher forcing)", "bullets": True,
                 "body": ["정답 prefix가 **모두 주어짐**", "shift + causal mask로 모든 위치를 **한 번에**", "RNN처럼 한 칸씩 기다리지 않는다"]},
                {"head": "생성 (추론)", "tone": "accent", "bullets": True,
                 "body": ["다음 입력 토큰이 **아직 없다**", "하나 만들고 붙이고 다시 계산 — **순차적**", "→ Part 5"]}], cols=2, body_size=17, head_size=19)
s.callout("둘은 **모순이 아니다** (개념 확인 15). 단, 층 사이의 의존은 남으므로 ‘모든 계산이 한 번에 병렬’은 아니다.",
          Box(rest.x, rest.y + 0.1, rest.w, 0.9), kind="key", size=16)

s = d.slide("원논문의 학습 조건", lead="Adam(β1 0.9, β2 0.98) · warm-up 4000 후 감소 · dropout 0.1 · label smoothing 0.1", stage="역사",
            notes="Vaswani et al. §5. 학습률 lrate = d^−0.5 · min(step^−0.5, step · warmup^−1.5): 처음 4000 step은 선형 증가, 이후 step^−1/2로 감소. d = 512면 최고점 약 7.0 × 10^−4. "
                  "label smoothing 0.1은 정답을 확률 1로 몰아가지 않게 완화 — perplexity는 나빠지지만 정확도·BLEU는 좋아졌다고 보고. "
                  "하드웨어: NVIDIA P100 8장, base 100k step 약 12시간, big 300k step 약 3.5일. 결과: WMT'14 영→독 BLEU 27.3(base), 28.4(big), 영→프 41.8(big). 추론: beam 4, 길이 페널티 α = 0.6. "
                  "이 조건들은 모델 구조와 별도의 실험 조건이다.")
L, R = s.cols(0.52)
s.image(A("week6/lr_schedule.png"), L)
s.table(["항목", "원논문 (base / big)"], [["Optimizer", "Adam β1 0.9, β2 0.98, ε 1e−9"], ["학습률", "warm-up 4000 → step^−1/2 감소 (최고 ≈ 7e−4)"],
                                        ["규제", "dropout 0.1 · label smoothing 0.1"], ["하드웨어", "P100 × 8 · base 약 12시간 · big 약 3.5일"],
                                        ["결과 (BLEU)", "영→독 27.3 / 28.4 · 영→프 41.8 (big)"]], R, size=14, widths=[1.4, 3.6])

s = d.slide("무엇을 기록할까 — 지표와 점검 순서", lead="teacher-forced 지표와 실제 생성 성능은 다르다. loss가 안 떨어지면 작은 과적합부터", stage="검증",
            notes="NLL(PAD·평균 단위·smoothing 여부 명시), perplexity(같은 tokenizer·데이터에서만 비교, label-smoothed loss의 exp와 섞지 않기), token accuracy(한 시퀀스의 작은 오류를 가릴 수 있음), "
                  "exact match(시퀀스 전체 정답 비율, EOS·길이 기준 필요), 실제 생성 성능(생성한 prefix 기반 — teacher-forced 평가와 별도). "
                  "model.eval()은 dropout 등을 평가 모드로, torch.no_grad()는 autograd 기록을 끈다 — 역할이 다르다. "
                  "loss가 안 떨어지면: 1–4개 샘플 과적합 확인 → 데이터 정렬, target shift, mask 방향, logits shape, ignore_index, optimizer에 파라미터가 들어갔는지. 곧바로 층 수나 GPU를 늘리지 않는다.")
L, R = s.cols(0.55, gap=0.4)
s.table(["지표", "주의"], [["NLL", "PAD · 평균 단위 · smoothing 명시"], ["Perplexity", "같은 tokenizer · 데이터에서만 비교"],
                          ["Token accuracy", "작은 오류를 가릴 수 있다"], ["Exact match", "EOS · 길이 기준 필요"],
                          ["생성 성능", "teacher-forced 평가와 **별도**"]], L, size=14, widths=[1.6, 3.4])
s.card(R, "loss가 안 떨어질 때", ["① 샘플 **1–4개**를 과적합시킬 수 있나?", "② 데이터 정렬 · **target shift**", "③ **mask 방향** · logits shape",
                               "④ ignore_index · optimizer에 파라미터 포함?", "⑤ 그 다음에 크기 · GPU"], tone="accent", bullets=False, body_size=15, fit_h=True)
s.callout("`model.eval()` = dropout 등 평가 모드 · `torch.no_grad()` = autograd 기록 끄기 — **역할이 다르다**",
          Box(s.area.x, s.area.b - 0.9, s.area.w, 0.9), kind="tip", size=15)

# ============================================================ Part 5
d.part(5, "생성과 비용: KV Cache · 연산량 · 메모리", "학습 때의 정답 prefix가 없다 — 토큰을 하나씩 만들면 무엇이 반복되나?")

s = d.slide("자기회귀 생성: 토큰을 하나씩", lead="source는 한 번 인코딩, BOS에서 시작해 마지막 위치의 logits로 다음 토큰을 고르고 붙이기를 반복",
            stage="아이디어",
            notes="추론에서는 source를 Encoder로 한 번 처리하고 BOS로 Decoder를 시작한다. 마지막 위치의 logits에서 다음 토큰을 고른 뒤 prefix에 붙이고 다시 Decoder를 실행한다. "
                  "EOS가 나오거나 최대 길이에 도달하면 멈춘다. 다음 입력이 방금 생성한 결과에 의존하므로 이 루프는 순차적이다. "
                  "원자료 오개념 17: 'Transformer는 모든 토큰을 동시에 생성한다' — 학습의 위치 병렬성과 자기회귀 생성은 다르다. "
                  "Teacher forcing과의 차이: 생성에서는 잘못 만든 토큰이 다음 입력이 된다.")
top, bot = s.area.top(1.9, gap=0.35)
s.flow([{"head": "Encoder", "body": "source → E\n(한 번만)"}, {"head": "Decoder", "body": "prefix [BOS, I, am]"},
        {"head": "마지막 위치 logits", "body": "(|V|,) 점수"}, {"head": "토큰 선택", "body": "“a”", "tone": "accent"},
        {"head": "붙이고 반복", "body": "[BOS, I, am, a] …\nEOS까지", "tone": "dark"}], top, body_size=14, head_size=16, gap=0.35)
s.bullets(["다음 입력이 **방금 만든 토큰**에 의존 → 루프는 **순차적**",
           "==오개념== “Transformer는 모든 토큰을 동시에 생성한다” — 학습의 병렬성과 다르다",
           "생성에서는 **잘못 만든 토큰이 다음 입력**이 된다 → teacher-forced 정확도와 생성 성능이 다른 이유"], bot)

s = d.slide("토큰 선택은 모델과 별도의 정책", lead="같은 모델, 같은 logits라도 어떻게 고르느냐에 따라 결과가 달라진다", stage="정리",
            notes="greedy: 매번 가장 높은 점수 — 단순하지만 전체 시퀀스 확률의 최적해를 보장하지 않는다. sampling: 분포에서 표본 추출 — 다양하지만 결과가 매번 다르다. "
                  "temperature: logits/τ로 분포 조절(2주차) — 학습을 새로 하는 것이 아니다. top-k/top-p: 상위 후보만 남기고 샘플링. beam search: 여러 후보 prefix 유지 — 계산이 늘고 길이 정규화가 영향. "
                  "원논문 번역: beam 4, 길이 페널티 α = 0.6. 이들은 출력 분포를 '사용하는' 방식이지 모델 가중치를 바꾸는 학습이 아니다.")
s.table(["정책", "방법", "특징"], [["Greedy", "가장 높은 점수의 토큰", "단순, 전체 최적은 **보장 안 됨**"], ["Sampling", "분포에서 표본 추출", "다양하지만 매번 다르다"],
                                  ["Temperature τ", "softmax(logits / τ) 후 선택", "분포의 뾰족함 조절 (2주차) — **재학습 아님**"],
                                  ["Top-k · Top-p", "상위 후보만 남기고 샘플링", "엉뚱한 저확률 토큰 방지"],
                                  ["Beam search", "여러 후보 prefix 유지", "계산 증가 · 길이 정규화 영향 (원논문: beam 4, α 0.6)"]],
        Box(s.area.x, s.area.y, s.area.w, 3.4), widths=[2.0, 3.8, 5.0], size=15)
s.callout("정책은 출력 분포를 **사용하는 방식**이지 Q/K/V 가중치를 바꾸는 학습이 아니다. 비교 전에 과제의 평가 목표부터 정한다.",
          Box(s.area.x, s.area.y + 3.65, s.area.w, 0.9), kind="tip", size=16)

s = d.slide("KV Cache: 바뀌지 않는 것을 보관", lead="과거 토큰의 각 층 K, V는 새 토큰이 와도 그대로 — 저장해 두고 새 토큰의 Q만 계산", stage="아이디어",
            notes="고정 가중치와 causal mask 아래에서 기존 prefix 토큰의 각 층 K, V는 새 미래 토큰이 추가되어도 변하지 않는다. 저장해 두면 매번 과거 prefix 전체를 다시 계산하지 않는다. "
                  "Prefill: 주어진 prefix 전체를 한 번에 처리해 cache를 채우는 단계(TTFT, 첫 토큰까지 시간을 좌우). Decode: 새 토큰 하나씩, 새 Q로 저장된 K들을 참조. "
                  "Q는 현재 토큰에 대해서만 필요하므로 cache하지 않는다. Encoder–Decoder에서는 cross-attention의 K, V도 source가 고정이면 재사용. "
                  "남는 것: 생성 루프 자체와 새 Query가 늘어나는 과거 Key 전부를 참조하는 비용(개념 확인 17). "
                  "주의: 같은 token prefix라도 모델 가중치·adapter·position ID·mask가 다르면 cache 재사용이 유효하지 않을 수 있다.")
top, bot = s.area.top(3.0, gap=0.25)
s.image(A("week6/kv_cache.png"), top)
L, R = bot.cols(0.5, gap=0.4)
s.bullets(["저장: 과거의 **K, V** (층마다)", "저장 안 함: **Q** (현재 토큰만 필요)", "Prefill → TTFT · Decode → 토큰당 지연"], L, size=15)
s.bullets(["남는 것: **생성 루프** + 새 Q가 **모든 과거 K** 참조", "==주의== 가중치 · adapter · position · mask가 다르면 cache를 **공유하면 안 된다**"], R, size=15)

s = d.slide("“Transformer는 O(N²)”만으로는 부족하다", lead="한 블록 MACs ≈ 4Nd² (투영) + 2N²d (attention) + 2N·d·d_ff (FFN)", stage="계산",
            notes="길이 N, 폭 d의 dense self-attention 블록 forward의 주요 행렬곱(MAC, 곱셈-누산 1회 ≈ 2 FLOPs). Q/K/V/O 투영 4Nd², attention의 QKᵀ와 AV 2N²d, FFN 2Nd·d_ff. "
                  "d = 512, d_ff = 2048: N = 512에서 투영 0.54G, attention 0.27G, FFN 1.07G — 짧은 길이에서는 FFN·투영이 더 크다. N이 커질수록 N² 항이 지배한다. "
                  "N을 2배로 하면 attention 항은 4배, 투영·FFN 항은 2배(개념 확인 16). 이 식은 Encoder 스타일 한 블록 forward — backward·optimizer·생성 루프 전체 비용이 아니다.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("MACs ≈ 4·N·d²  +  2·N²·d  +  2·N·d·d_ff", top, size=24)
L, R = bot.cols(0.55, gap=0.4)
s.image(A("week6/flops_terms.png"), L)
s.table(["N (d = 512)", "투영", "attention", "FFN"], [["512", "0.54G", "0.27G", "1.07G"], ["1024", "1.07G", "1.07G", "2.15G"],
                                                    ["2048", "2.15G", "**4.29G**", "4.29G"]], Box(R.x, R.y, R.w, 1.7), size=14, align="cccc")
s.bullets(["N × 2 → attention **×4**, 나머지 **×2**", "짧을 때는 FFN · 투영이 더 크다", "forward 한 블록 기준 — 전체 비용 아님"],
          Box(R.x, R.y + 1.95, R.w, R.h - 1.95), size=15)

s = d.slide("메모리: attention 표와 KV Cache", lead="점수 표 하나 = B·H·N² 원소 · KV Cache = 2 · L · B · N · H_kv · d_h · bytes", stage="계산",
            notes="일반 구현에서 점수 표 하나를 명시적으로 저장하면 B·H·N² 원소. FlashAttention은 타일 단위 계산으로 거대한 표 전체를 HBM에 저장하지 않고 같은(정확한) dense attention을 계산한다 — 산술량을 선형으로 만드는 것은 아니다. "
                  "KV Cache: K와 V를 각각 저장하므로 2. 예: L = 32층, d = 4096 (H = 32, d_h = 128), N = 4096, B = 1, FP16(2 bytes) → 2 GiB. "
                  "GQA는 여러 Query head가 적은 KV head를 공유해 cache를 줄인다(H_kv = 8이면 1/4). 식은 순수 K/V 데이터만의 크기. "
                  "측정할 때: 같은 batch·dtype·길이·생성 길이·device·kernel·warm-up을 기록하고 GPU 동기화. 파라미터 감소율, FLOPs 감소율, 실제 지연 감소율은 서로 다르다.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("KV bytes = 2 · L · B · N · H_kv · d_h · bytes", top, size=24)
L, R = bot.cols(0.55, gap=0.4)
s.image(A("week6/kv_memory.png"), L)
s.bullets(["예: L 32, d 4096, N 4096, FP16 → **2 GiB**", "**GQA**: KV head 공유 → cache 감소", "FlashAttention: 표를 저장하지 않고 **정확히** 계산",
           ("산술량이 선형이 되는 것은 아님", 1), "측정: batch · dtype · 길이 · device · warm-up **통제**", ("이론 MACs ≠ 실측 지연", 1)], R, size=15)

# ============================================================ Part 6
d.part(6, "직접 실험하기", "구조가 왜 필요한지, 어떤 증거로 보일 수 있을까?")

s = d.slide("작은 Transformer 실습: 아홉 가지 검사", lead="수열 뒤집기 [3, 7, 5] → [5, 7, 3, EOS] — 학습 전에 구조부터 검증한다", stage="실습",
            notes="원자료의 transformer_lab.py: 명시적 Q/K/V, causal·padding mask, Post-LN, sinusoidal 위치, cross-attention, loss, greedy 생성을 포함한 교육용 Encoder–Decoder. "
                  "d = 64, H = 4, Encoder/Decoder 각 2층, Adam. 외부 데이터 없이 정수 수열을 뒤집는다. 원논문의 축소 재현이 아니다. "
                  "실행: python transformer_lab.py --mode check (구조 검사), --mode train --steps 400 --device cpu. 검사에서는 dropout을 끄고 허용 오차를 명시한다.")
L, R = s.cols(0.4)
s.code("# 1. 구조 검사 (학습 없이)\n"
       "python transformer_lab.py --mode check\n\n"
       "# 2. CPU에서 작은 모델 학습\n"
       "python transformer_lab.py --mode train \\\n"
       "    --steps 400 --device cpu\n\n"
       "# 설정: d=64, H=4, 2+2층, Adam", L, size=12)
cb = s.last_code_box
s.bullets(["교육용 구현 — 원논문 재현 **아님**", "검사 때 **dropout 끄기**, 허용 오차 명시"], Box(L.x, cb.b + 0.25, L.w, L.b - cb.b - 0.25), size=15)
s.table(["검사", "확인하는 성질"], [["Shape", "Q/K/V · attention 출력 차원"], ["Row sum", "dropout 전 attention 행 합 = 1"],
                                  ["Future weight zero", "causal mask의 미래 가중치 = 0"], ["PyTorch reference", "직접 구현 = F.scaled_dot_product_attention"],
                                  ["Permutation equivariance", "위치·mask 없는 SA의 순열 대응"], ["Cross query length", "cross 출력 길이 = Query 길이"],
                                  ["Masked value independence", "가려진 Key의 Value를 바꿔도 출력 불변"],
                                  ["Full-model causal invariance", "미래 target을 바꿔도 이전 logits 불변"], ["Backward gradient", "Encoder 투영까지 기울기 전달"]],
        R, size=13, widths=[2.4, 3.6])

s = d.slide("첫 결과를 해석하는 법", lead="400 step에서 손실은 내려갔지만 완전한 수열 생성은 아직 — 두 지표는 다르다", stage="검증",
            notes="원자료의 실제 실행 사례(PyTorch 2.10 CPU, seed 7, batch 32, 400 step, 단일 실행): 훈련 batch NLL 2.90 → 1.23. "
                  "평가: 훈련 길이 3–8에서 NLL 1.045, teacher-forced 토큰 정확도 56.8%, greedy exact match 6.9%(5/72). 더 긴 9–12에서 1.764, 33.8%, 0%(0/72). "
                  "400 step은 실행 예시이지 충분한 학습이 아니다. 길이를 늘렸을 때 성능이 떨어져도 구현 오류라고 단정하지 않는다 — 학습 분포 밖이다. "
                  "코드 리뷰: 한 명은 mask, 한 명은 shape, 한 명은 loss·metric, 한 명은 생성을 맡아 '어느 검사로 어떤 성질을 확인했는지' 제출.")
s.table(["평가 길이", "Raw NLL", "teacher-forced 토큰 정확도", "greedy exact match"],
        [["3–8 (훈련 범위)", "1.045", "56.8%", "6.9% (5 / 72)"], ["9–12 (더 긴 입력)", "1.764", "33.8%", "**0%** (0 / 72)"]],
        Box(s.area.x, s.area.y, s.area.w, 1.5), widths=[2.6, 1.6, 3.4, 3.2], size=16, align="lccc")
s.cards([{"head": "읽는 법 ①", "body": ["훈련 NLL 2.90 → 1.23으로 **내려갔지만**", "완전한 수열 생성은 **아직**"]},
         {"head": "읽는 법 ②", "body": ["토큰 정확도와 **exact match**는 다르다", "생성은 오류가 **누적**된다"]},
         {"head": "읽는 법 ③", "tone": "accent", "body": ["긴 입력에서 떨어져도 **구현 오류로 단정 X**", "학습 분포 밖 — 단일 실행 · 400 step"]}],
        Box(s.area.x, s.area.y + 1.8, s.area.w, s.area.h - 1.8), cols=3, body_size=16, head_size=17)

s = d.slide("Ablation: 질문을 통제된 비교로", lead="“Transformer가 더 좋다”가 아니라 — 어떤 조건에서 어떤 부품이 어떤 지표에 영향을 주는가", stage="실습",
            notes="원자료의 실험 설계 표. 변경 변수 하나, 통제할 것, 볼 지표를 정한다. 구성 요소 제거는 파라미터 수와 계산량도 함께 바꾸므로 구조의 효과인지 용량의 효과인지 분리하는 추가 대조군이 필요할 수 있다. "
                  "권장 진행: 작은 고정 batch 과적합 → 새 수열 평가 → 길이별 평가 → 구조 변경 → 여러 seed 반복(3개 이상 제안, seed만 늘린다고 편향된 실험이 해결되지는 않는다).")
s.table(["변경 변수", "통제할 것", "볼 지표"],
        [["평가 길이 늘리기", "모델 · 학습 데이터 · 생성 규칙", "길이별 토큰 정확도 / exact match"], ["위치 정보 제거 (source / target 각각)", "나머지 구조 · seed · 학습량", "순서 민감 과제 성능"],
         ["Head 수 H (d 고정)", "파라미터 규모 · step", "품질 · 지연 · 점수 표 저장량"], ["Causal mask 제거", "shift된 입력 유지", "훈련 loss와 실제 생성의 괴리"],
         ["FFN · Residual 제거", "깊이 · 초기화 · optimizer", "학습 곡선 · 기울기 규모"], ["Post-LN / Pre-LN", "깊이 · warm-up · 학습률", "불안정성 · 최종 품질"]],
        Box(s.area.x, s.area.y, s.area.w, 3.5), widths=[3.4, 3.4, 4.0], size=14)
s.callout("부품을 빼면 **파라미터 수·연산량도 바뀐다** → 구조의 효과인지 용량의 효과인지 분리하는 대조군이 필요할 수 있다.",
          Box(s.area.x, s.area.y + 3.75, s.area.w, 0.85), kind="warn", size=15)

s = d.slide("실험 기록과 최종 프로젝트", lead="작은 과제 · 최소 기록 필드 · 네 가지 그림 · 검증 가능한 설명", stage="실습",
            notes="과제: 복사(output = input), 반전(순서 뒤집기), 기호 치환(정해진 매핑) — 필요한 순서 정보와 전역 의존성이 다르다. "
                  "최소 기록 필드: run_id, git_commit, seed, task, 길이, 구조(layers, d_model, heads, d_ff, position_type, mask_policy, norm_placement), optimizer·lr·batch·precision·device, "
                  "teacher_forced_nll, token_accuracy, greedy_exact_match, prefill_ms, decode_ms_per_token, peak_memory_mb, notes. 측정하지 않은 값을 추정치처럼 채우지 않는다(이론 MACs vs 실측 latency 표시). "
                  "네 가지 그림: 길이–정확도, step–loss, 품질–지연, 길이–메모리. 최종 프로젝트 배점(제안): 문제와 가설 20, 구현 정확성 30, 실험 설계와 결과 25, 해석과 한계 15, 설명 발표 10. "
                  "예상과 다른 결과라도 조건과 설명을 정확히 정리했다면 좋은 연구 연습이다.")
s.cards([{"head": "작은 과제", "bullets": True, "body": ["복사: output = input", "반전: 순서 뒤집기", "기호 치환: 정해진 매핑"]},
         {"head": "최소 기록 필드", "bullets": True, "body": ["run_id · commit · seed · task", "구조 · mask · norm 위치", "NLL · 정확도 · exact match · 지연 · 메모리"]},
         {"head": "네 가지 그림", "bullets": True, "body": ["길이 – 정확도", "step – loss", "품질 – 지연 · 길이 – 메모리"]},
         {"head": "최종 프로젝트 배점 (제안)", "tone": "accent", "bullets": True,
          "body": ["가설 20 · **구현 정확성 30**", "실험 25 · 해석과 한계 15", "설명 발표 10"]}], cols=4, body_size=14, head_size=16)
s.callout("성공 기준: 예상과 다른 결과라도 **조건과 가능한 설명을 정확히** 정리했다면 좋은 연구 연습이다. "
          "정해 둔 결론에 맞춰 데이터나 조건을 숨기지 않는다. 측정하지 않은 값을 추정치처럼 채우지 않는다.",
          Box(s.area.x, s.area.y + 2.35, s.area.w, 1.2), kind="key", size=16)
s.callout("최종 발표의 세 질문: ① 어느 가정에서만 결론이 성립하나? ② 차이가 파라미터 수·학습량 때문일 가능성은? ③ 모델이 실패한 입력 하나를 보여 줄 수 있나?",
          Box(s.area.x, s.area.y + 3.8, s.area.w, 1.0), kind="tip", size=15)

# ============================================================ Part 7
d.part(7, "Transformer 이후, 그리고 과정 마무리", "원형에서 무엇을 유지하고, 무엇을 바꾸었나? — 그리고 여섯 질문을 다시 본다")

s = d.slide("세 가지 조립 방식", lead="Encoder-only · Decoder-only · Encoder–Decoder — 반쪽을 떼는 것이 아니라 mask · 목표 · head가 함께 달라진다",
            stage="정리",
            notes="Encoder-only(BERT, 2018): 양방향 self-attention, 가려진 토큰 복원(masked LM)으로 사전학습 후 작업별 head. "
                  "Decoder-only(GPT, 2018~): causal self-attention, 다음 토큰 예측. 일반적인 순수 텍스트 Decoder-only에는 원형의 cross-attention이 없다. "
                  "Encoder–Decoder(원형 2017, T5 2019): 입력을 읽고 조건부 출력 생성(text-to-text, span corruption 등). "
                  "BERT의 masked LM은 '미래 정답을 보고 다음 토큰을 예측'하는 누출과 다르다 — 입력에서 가린 위치를 복원하는 별도 목표. 무엇이 입력이고 무엇이 정답인지로 판단한다.")
L, R = s.cols(0.55)
s.image(A("week6/archs.png"), L)
s.table(["구조", "mask · 목표", "예"], [["Encoder-only", "양방향 · 가려진 토큰 복원", "BERT (2018)"], ["Decoder-only", "causal · 다음 토큰 예측", "GPT (2018~)"],
                                     ["Encoder–Decoder", "조건부 생성 (text-to-text)", "원형 (2017) · T5 (2019)"]], Box(R.x, R.y, R.w, 2.1), size=14, widths=[2.0, 2.8, 1.8])
s.bullets(["Decoder-only에는 보통 **cross-attention이 없다**", "BERT의 masked LM ≠ 정답 누출", ("무엇이 입력이고 무엇이 정답인가로 판단", 1)],
          Box(R.x, R.y + 2.35, R.w, R.h - 2.35), size=15)

s = d.slide("ViT와 DiT: 무엇을 token이라 부를까", lead="이미지 patch도 token이 된다 — 같은 블록, 다른 입력과 다른 생성 과정", stage="역사",
            notes="ViT(Dosovitskiy et al., 2020): 224×224 이미지를 16×16 patch로 나누면 14×14 = 196개 patch, 각 patch(16·16·3 = 768개 값)를 d차원으로 선형 투영해 token처럼 넣는다. "
                  "CLS 사용·위치 임베딩·pooling은 모델마다 다르다. 3주차 CNN의 구조적 가정(지역성) 없이도 대규모 데이터에서는 잘 작동한다. "
                  "DiT(Peebles & Xie, 2022/2023): diffusion 모델에서 noisy latent patch와 timestep, 조건을 받아 denoising에 필요한 값을 예측하는 Transformer. 토큰 생성 루프와 다른 계산. "
                  "원형 DiT는 class conditioning을 다룬다 — 모든 DiT가 텍스트 조건 모델은 아니다.")
L, R = s.cols(0.55)
s.image(A("week6/vit_patch.png"), L)
rest = s.card(R, "ViT (2020)", ["224×224 → 16×16 patch **196개**", "patch 하나 = 768개 값 → **d차원 투영**", "CNN의 지역성 가정 없이 대규모 데이터로"],
              bullets=True, fit_h=True)
s.card(rest, "DiT (2022/2023)", ["noisy latent patch + timestep + 조건", "diffusion의 **denoising** 예측", "토큰 생성 루프와 **다른** 계산"],
       tone="accent", bullets=True, fit_h=True)

s = d.slide("원형과 후속 변형을 구분하기", lead="변형이 있다는 것 ≠ 특정 조합이 모든 모델의 표준", stage="정리",
            notes="이 과정의 원형 기준과 대표적 후속 설계. FFN 활성화 ReLU → GELU, SwiGLU. 정규화 Post-LN → Pre-LN, RMSNorm. 위치 sinusoidal 덧셈 → 학습형, RoPE(Q·K 회전으로 내적에 상대 위치 반영). "
                  "head 구성 MHA → GQA/MQA(KV head 공유로 cache·대역폭 절충, Query head까지 줄이는 것과 다름). FlashAttention: 정확한 attention을 IO 효율적으로 — 산술량이 선형이 되는 것은 아님. "
                  "원자료: 본 강의의 목표를 달성하기 전에 이들을 세부 구현까지 확장하지 않는다. 원형 표에 꽂아 넣고 무엇이 바뀌는지 설명할 수 있을 정도로만.")
s.table(["부품", "원형 (2017)", "후속 설계의 예", "하지 않는 주장"],
        [["FFN 활성화", "ReLU", "GELU · SwiGLU", "attention을 대체하지 않는다"], ["정규화", "LayerNorm · Post-LN", "Pre-LN · RMSNorm", "보편적 우열이 아니다"],
         ["위치 정보", "sinusoidal 덧셈", "학습형 · **RoPE** (상대 위치)", "위치 정보를 없애는 것이 아니다"],
         ["Head 구성", "Q/K/V head 수 동일 (MHA)", "**GQA** · MQA (KV head 공유)", "Query head까지 줄이는 것이 아니다"],
         ["Attention 계산", "표를 저장하는 dense 계산", "**FlashAttention** (IO 효율)", "산술량이 선형이 되는 것이 아니다"]],
        Box(s.area.x, s.area.y, s.area.w, 3.2), widths=[1.8, 2.6, 3.0, 3.4], size=15)
s.callout("범위 제한: 이 과정의 목표를 달성하기 전에 RoPE · GQA · FlashAttention을 세부 구현까지 확장하지 않는다 — "
          "원형 표에 꽂아 넣고 **무엇이 바뀌는지** 설명할 수 있으면 충분하다.", Box(s.area.x, s.area.y + 3.5, s.area.w, 1.0), kind="tip", size=16)

s = d.slide("여섯 질문으로 다시 보기", lead="1943 → 2017 → 이후: 각 구조는 이전 구조가 남긴 질문에 대한 답이었다", stage="정리",
            notes="과정 전체 회고. W1 규칙을 다 쓰지 않고 배울 수 있을까? → 텐서·손실·경사하강법. W2 직선으로 안 되면? → MLP·역전파. W3 공간·깊이는? → CNN·ResNet·Norm. "
                  "W4 먼 정보를 기억하려면? → RNN·LSTM·Seq2Seq. W5 원문을 다시 보면? → Attention·Q/K/V·Multi-head. W6 참조만으로 만들면? → Transformer. "
                  "그리고 Transformer 안에는 이 모든 답이 들어 있다: 텐서·학습 루프(W1), MLP=FFN·softmax·CE(W2), Residual·LayerNorm(W3), 임베딩·Encoder–Decoder(W4), attention(W5). "
                  "원자료 주의: 계보는 교육적 연결이며, 각 모델이 이전 모델을 완전히 대체했다는 주장이 아니다.")
top, bot = s.area.top(2.4, gap=0.3)
s.image(A("week6/genealogy.png"), top)
s.table(["Transformer 안의 부품", "처음 배운 곳"], [["텐서 · 손실 · 경사하강 · 학습 루프", "Week 1"], ["FFN(=MLP) · 역전파 · softmax + cross-entropy", "Week 2"],
                                               ["Residual · LayerNorm", "Week 3"], ["임베딩 · 다음 토큰 확률 · Encoder–Decoder", "Week 4"],
                                               ["Attention · Q/K/V · Multi-head · 위치 인코딩", "Week 5"]], bot, widths=[7, 2], size=14, align="lc")

s = d.slide("마지막 설명 과제", lead="빈 종이에 입력 ID부터 다음 토큰까지 — 각 구간의 shape, 파라미터, mask를 적고 설명한다", stage="실습",
            notes="원자료의 마지막 설명 과제와 구술 평가. 빈 종이에 입력 ID → 임베딩 + PE → Encoder → Decoder self / cross attention → FFN → logits → 다음 토큰을 그린다. "
                  "각 구간의 shape, 학습 파라미터, mask를 적고 학습과 생성의 차이를 다른 사람에게 설명한다. 설명 중 막힌 곳이 복습할 곳이다. "
                  "구술 평가: 처음 보는 d, H, S, T 설정을 주고 입력부터 logits까지 따라가게 한 뒤, '위치 정보 제거', '잘못된 mask', 'KV Cache 추가' 중 하나를 바꾸면 무엇이 달라지는지 설명. "
                  "더 좋은 설명의 형식: '이 head는 주어를 이해한다' 대신 '이 입력들에서 특정 위치에 높은 가중치가 관찰되었다'.")
top, bot = s.area.top(1.8, gap=0.3)
s.flow([{"head": "ID", "body": "(B, S)"}, {"head": "임베딩 + PE", "body": "(B, S, d)"}, {"head": "Encoder × L", "body": "E (B, S, d)"},
        {"head": "Decoder × L", "body": "masked self · cross · FFN"}, {"head": "logits", "body": "(B, T, |V|)"},
        {"head": "다음 토큰", "body": "선택 정책", "tone": "dark"}], top, body_size=13, head_size=15, gap=0.3)
L, R = bot.cols(0.5, gap=0.4)
s.card(L, "각 구간에 적을 것", ["입력 · 출력 **shape**", "학습되는 **파라미터**", "정보가 이동하는 **방향**", "**mask**가 막는 연결"], bullets=True)
s.card(R, "구술 평가 (원자료)", ["처음 보는 d, H, S, T로 입력 → logits 추적", "하나를 바꾸면? 위치 정보 제거 / 잘못된 mask / KV Cache 추가",
                              "“이 head는 주어를 이해한다” → “특정 위치에 높은 가중치가 **관찰**되었다”"], tone="accent", bullets=True)

# ============================================================ 마무리
d.summary(["층 = attention(위치 간 결합) + **FFN**(위치별 변환), 각각 **잔차 합 + LayerNorm** — shape (B, N, d) 유지",
           "**shift + causal mask(−∞)**로 정답을 훔쳐보지 않고 모든 위치를 병렬 학습",
           "Cross-attention: Q는 Decoder, K·V는 Encoder 출력 E — 점수 표 T × S",
           "파라미터 ≈ 층당 4d² + 2d·d_ff, 연산 ≈ 4Nd² + 2N²d + 2Nd·d_ff — **O(N²)만이 아니다**",
           "생성은 **자기회귀**: KV Cache가 과거 K·V 재계산을 줄이지만 루프는 남는다",
           "구조의 필요성은 **통제된 실험**으로 — 계보는 여섯 질문과 그 답의 연결"])

d.quiz("셀프 체크 ①", [("Causal mask에서 미래 점수를 0으로만 바꾸면? (개념 확인 07)", "exp(0) = 1이므로 차단되지 않는다 — softmax 전에 −∞로 처리해야 한다"),
                     ("정답을 한 칸 이동시킨 Decoder에서 대각선 참조는? (08)", "허용할 수 있다 — 현재 입력은 다음 정답보다 한 칸 앞이다"),
                     ("FFN은 어떤 계산인가? (11)", "각 토큰 위치의 특징에 적용하는 비선형 변환 — 위치 간 결합은 하지 않는다"),
                     ("LayerNorm(d)의 전형적인 정규화 범위는? (12)", "각 토큰의 d개 특징 (batch 전체가 아니다)")])

d.quiz("셀프 체크 ②", [("CrossEntropyLoss에 일반적으로 전달하는 값은? (14)", "정규화 전 logits (softmax를 두 번 하지 않는다)"),
                     ("Transformer의 병렬 학습과 자기회귀 생성은 모순인가? (15)", "아니다 — 학습은 정답 prefix가 주어져 병렬, 생성은 다음 입력이 없어 순차"),
                     ("N을 2배로, d를 고정하면 주요 항은? (16)", "attention 곱셈 항(N²d)은 4배, 투영·FFN 항(Nd²)은 2배"),
                     ("KV Cache가 하는 일은? (17)", "과거 위치의 K/V 재계산을 줄인다 — 생성 루프와 새 Query의 과거 참조 비용은 남는다")])

d.misconceptions([["“FFN은 다른 토큰을 다시 섞는다”", "FFN은 각 위치의 특징을 **독립적으로** 변환한다"],
                  ["“미래 점수를 0으로 만들면 mask가 된다”", "softmax 전에 **−∞** — exp(0) = 1"],
                  ["“학습 입력에 정답이 있으면 무조건 누출”", "**shift**된 목표와 허용 범위(mask)를 함께 본다"],
                  ["“Transformer는 모든 토큰을 동시에 생성한다”", "학습의 위치 병렬성 ≠ **자기회귀** 생성"],
                  ["“Attention이 N²이므로 비용도 N²뿐”", "투영 · FFN의 **Nd²** 항과 기타 비용이 있다"],
                  ["“KV Cache가 있으면 과거 문맥 비용이 사라진다”", "재계산은 줄지만 새 Q의 **과거 참조**는 남는다"],
                  ["“Attention heatmap은 모델의 생각을 증명한다”", "**관찰** 자료 — 인과 설명은 별도 검증"]],
                 notes="원자료 오개념 12, 15–20과 실무 경고 신호: 너무 빨리 낮아지는 loss, PAD를 맞히는 높은 정확도, EOS 없이 계속되는 생성, batch를 바꾸자 크게 달라지는 결과.")

d.homework([("mask 오류 실험 (원자료 운영안 9회차)", "causal mask를 일부러 제거하고 학습 — 훈련 loss와 실제 greedy 생성 결과의 괴리를 기록한다."),
            ("실습 검사 통과", "transformer_lab.py의 아홉 검사를 실행하고, 각 검사가 어떤 성질을 확인하는지 한 줄씩 설명한다."),
            ("Ablation 보고서 (10회차)", "위치 정보 제거 또는 head 수 변경 하나를 골라 통제 조건 · seed 3개 · 네 그림 중 둘을 포함해 보고한다.")])

d.references([["[22] Vaswani et al. (2017). Attention Is All You Need", "Fig.1 · §3 구조 · §4 비용 · §5 학습 · §6.2 변형 실험"],
              ["[15] Seq2Seq → [17] Bahdanau → [22] Transformer → [19][20] ResNet · LayerNorm", "원자료 권장 읽기 순서"],
              ["[27] The Annotated Transformer · [28] PyTorch MHA / SDPA 문서", "mask의 boolean 의미 확인"],
              ["[31] BERT (2018) · [32] GPT (2018) · [33] T5 (2019)", "구조 · 목표의 차이"],
              ["[34] ViT (2020) · [41] DiT (2022) · [35]–[38] RoPE · GQA · FlashAttention", "원형 표에서 무엇이 바뀌었나"]])

d.handoff(["여섯 질문을 따라", "텐서 → MLP → CNN → RNN → Attention → **Transformer**", "그림의 모든 상자를 **왜 필요한지**로 설명"],
          ["언어 생성 → Decoder-only · KV Cache", "시각 → patch · 위치 · pooling", "효율 → 실제 병목 · kernel · 메모리 이동", "생성 모델 → diffusion과 DiT"],
          ["**관심 분야 하나를 골라**", "원형 표에 꽂아 넣고", "무엇이 바뀌었는지 설명해 보기"],
          notes="과정 마무리. 원자료의 '다음 학습 방향을 고르는 기준'. 관심 분야에 따라 다음 단계를 고르되, 먼저 원형 Transformer를 입력부터 출력까지 설명할 수 있는지 스스로 확인한다.")

d.save(OUT)
print("saved", OUT, d.n + 2, "slides")
