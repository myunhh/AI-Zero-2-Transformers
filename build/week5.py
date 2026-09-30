"""Week 5 — Attention과 Transformer의 핵심.  run: python build/week5.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from deckkit import *  # noqa: F401,F403,E402
from deckkit import ACCENT, ACCENT_BG, DARK, GRAY, MINT, TEAL, TEAL2, WHITE, Deck, X0, X1, Y0, Y1, W  # noqa: E402

A = os.path.join(HERE, "assets", "week5")
OUT = os.path.join(os.path.dirname(HERE), "lectures", "week05_attention_transformer.pptx")


def img(name):
    return os.path.join(A, name)


d = Deck(5, "Attention과 Transformer의 핵심",
         "고정 벡터 병목에서 Scaled Dot-Product · Multi-head Attention까지", date="2026-11-02")

# ============================================================ 도입
d.flow("지난 주 복습: Seq2Seq", [
    {"head": "입력 토큰", "body": "나는 / 학교에 / 간다\n길이 S"},
    {"head": "Embedding", "body": "ID → 벡터\n(one-hot 대신 밀집 표현)"},
    {"head": "Encoder RNN·LSTM", "body": "순서대로 읽으며\nhidden state 갱신"},
    {"head": "문맥 벡터 c", "body": "입력 전체를\n고정 길이 벡터 하나로", "accent": True},
    {"head": "Decoder", "body": "c와 이전 출력으로\n다음 토큰 생성 (길이 T)"},
], lead="4주차: 순서가 있는 데이터를 벡터로 읽고, 다른 길이의 출력으로 바꾸기",
    below=["**LSTM**: 게이트로 장기 기억 경로를 개선했지만, 현재 상태가 이전 상태에 의존하는 ==순차 계산==은 남는다",
           "**Seq2Seq**(2014): 입력 길이 S와 출력 길이 T가 달라도 된다 — Encoder–Decoder는 특정 신경망이 아니라 ‘역할 분담’ 구조",
           "**관찰**: Cho et al.(2014)의 분석 — 문장이 길어질수록 기본 Encoder–Decoder의 번역 품질이 떨어졌다",
           "**남은 문제**: 문장이 길어져도 요약본은 c 하나. 출력 위치마다 필요한 입력 정보가 다른데?"],
    caption="오늘의 출발점: 요약본 하나로 충분한가?",
    notes="지난 주에는 RNN과 LSTM으로 순서를 읽고, Seq2Seq로 길이가 다른 입력과 출력을 연결했습니다. "
          "Encoder는 입력 전체를 고정 길이 벡터 c에 담고, Decoder는 그 c와 이전 출력만 보고 번역을 이어 갑니다. "
          "Cho et al.(2014)의 분석에서도 기본 Encoder–Decoder는 문장이 길어질수록 성능이 떨어졌습니다. "
          "오늘은 이 병목을 푸는 Attention에서 시작해 Attention을 본체로 삼은 Transformer의 핵심 연산까지 갑니다.")

d.timeline("오늘의 위치: AI 계보", [
    (2013, "Word2Vec", "Mikolov et al. — CBOW·Skip-gram으로 단어 표현을 효율적으로 학습 (Embedding의 최초 발명은 아님)"),
    (2014, "Seq2Seq", "Cho et al. · Sutskever et al. — Encoder가 입력을 고정 벡터 c로 요약, Decoder가 출력 생성"),
    (2014, "Additive Attention", "Bahdanau · Cho · Bengio — 출력마다 입력 위치를 다시 정렬해 가중합 (arXiv 2014 / ICLR 2015)"),
    (2015, "Luong Attention", "Luong · Pham · Manning — global/local attention, dot·general·concat 점수 비교 (EMNLP 2015)"),
    ("2015–16", "ResNet · LayerNorm", "He et al. · Ba et al. — 잔차 연결과 정규화가 깊은 계산의 학습을 돕다"),
    (2017, "ConvS2S", "Gehring et al. — 합성곱만으로 순환 없이 병렬 시퀀스 변환"),
    (2017, "Transformer", "Vaswani et al. (NeurIPS 2017) — Attention·FFN·잔차·정규화·위치 정보를 결합"),
], highlight=[2, 6], lead="2014 Attention → 2017 “Attention Is All You Need”: 정보를 이동시키는 방식도 설계할 수 있다",
    notes="Bahdanau 논문(arXiv 2014년 9월)과 Sutskever의 Seq2Seq(2014년 9월)는 거의 같은 시기에 공개되었습니다. 수업 순서가 긴 역사적 간격을 뜻하지는 않습니다. "
          "2015–2017년에는 ResNet·LayerNorm이 깊은 모델의 학습을, ConvS2S가 순환 없는 병렬 처리를 보여 주었습니다. 병렬화를 시도한 것이 Attention만은 아닙니다. "
          "2017년 Transformer는 Attention을 처음 발명한 논문이 아니라, Attention·FFN·잔차·정규화·위치 정보를 결합한 시퀀스 변환 아키텍처입니다.")

d.cards("오늘의 학습 목표", [
    {"head": "병목 → Attention", "body": "고정 문맥 벡터의 한계를 설명하고 점수 → Softmax → 가중합을 손으로 계산한다"},
    {"head": "Transformer 지도", "body": "Encoder–Decoder 정보 흐름, 입출력 shape, 세 종류 Attention을 구분한다"},
    {"head": "위치 정보", "body": "위치 정보가 없으면 왜 순서를 구분하지 못하는지와 sinusoidal PE를 설명한다"},
    {"head": "Q · K · V", "body": "학습되는 투영 행렬, 파라미터 vs 활성값, cross-attention의 출처를 구분한다"},
    {"head": "Scaled Dot-Product", "body": "softmax(QKᵀ/√dₕ)V를 4토큰 예제로 계산하고 √dₕ와 mask의 역할을 말한다", "accent": True},
    {"head": "Multi-head · Shape", "body": "(B,N,d) → (B,H,N,dₕ) → (B,N,d) shape을 축 이름으로 추적한다"},
], numbered=True, cols=3, footer="오늘의 핵심 계산: Attention(Q,K,V) = softmax(QKᵀ/√dₕ)V 를 실제 숫자로",
    notes="오늘 목표는 여섯 가지입니다. 핵심은 다섯 번째, 공식 하나를 실제 숫자로 계산해 보는 것입니다. "
          "FFN·Residual·LayerNorm·mask 세부·학습·추론은 다음 주에 다루므로, 오늘은 Attention 연산과 shape에 집중합니다. "
          "각 파트가 끝날 때마다 ‘방금 계산을 자기 말로 설명할 수 있는가’를 확인하겠습니다.")

# ============================================================ Part 01
d.section("01", "병목에서 Attention으로", "질문이 달라져도 요약본은 하나 — 원문을 다시 찾아보면?",
          notes="첫 파트는 2014–2015년 Attention의 등장입니다. 수식은 세 줄뿐이고, 핵심은 ‘상태의 개수와 접근 규칙을 바꿨다’는 점입니다.")

s = d.blank("병목: 요약본은 하나뿐",
            notes="번역의 각 출력 위치에서 필요한 입력 정보는 다릅니다. ‘school’을 생성할 때는 ‘학교에’가, ‘go’를 생성할 때는 ‘간다’가 더 중요할 것입니다. "
                  "Attention은 Encoder의 위치별 표현 h₁…hₛ를 버리지 않고 남겨 두고, 현재 Decoder 상태에 맞게 매번 다른 가중합 cₜ를 만듭니다. "
                  "책 비유는 계산 경로를 이해하기 위한 것일 뿐, 모델이 사람처럼 책을 이해한다는 증거가 아닙니다. "
                  "수업 활동: 문장 전체를 숫자 5개로 요약하게 한 뒤 여러 종류의 질문을 던지고, 이어서 단어마다 숫자 5개를 남기게 하면 무엇이 달라지는지 물어보세요.")
d._image_fit(s, img("bottleneck.png"), X0, Y0, W, 4.25)
bw = (W - 0.5) / 3
boxes = [
    ("비유 · 고정 문맥 벡터", "책을 읽고 **요약문 하나**만 남긴 뒤, 그 요약문으로 모든 질문에 답한다.", MINT, TEAL),
    ("비유 · Attention", "답할 때마다 남겨 둔 **원문의 여러 위치**를 서로 다른 비중으로 다시 참조한다.", MINT, TEAL),
    ("비유의 한계", "모델이 사람처럼 이해한다는 뜻이 아니다. 실제 계산은 ==정렬 점수 → Softmax → 벡터 가중합==.", ACCENT_BG, ACCENT),
]
for i, (h, b, fc, hc) in enumerate(boxes):
    x = X0 + i * (bw + 0.25)
    d.box(s, x, 5.4, bw, 1.5, fill=fc)
    d.text(s, x + 0.15, 5.45, bw - 0.3, 0.45, h, size=15, bold=True, color=hc, anchor="m")
    d.text(s, x + 0.15, 5.9, bw - 0.3, 0.95, b, size=14, min_size=10)

d.formula("Attention: 점수 → 비중 → 가중합", [
    "e[t,j] = a( s[t−1], h[j] )",
    "α[t,j] = exp(e[t,j]) / Σₖ exp(e[t,k])",
    "c[t]   = Σⱼ α[t,j] · h[j]",
], parts=[("e[t,j]", "정렬 점수: Decoder 상태 s[t−1]과 입력 위치 j가 얼마나 맞는가"),
          ("α[t,j]", "Softmax로 만든 비중 — 양수, 입력 위치 축으로 합 1"),
          ("c[t]", "시점 t 전용 문맥 벡터 — 위치별 표현 h[j]의 가중합"),
          ("a( · )", "점수 함수: 작은 신경망, 내적, 학습된 bilinear 변환 등")],
    example=["α = (0.1, 0.2, 0.7)", "v1=(1,0), v2=(0,1), v3=(2,2)",
             "Σ α·v = (0.1+1.4, 0.2+1.4) = **(1.5, 1.6)**",
             "v3를 그대로 복사한 것이 ==아니다== — 여러 위치를 섞는다"],
    takeaway="하나의 c가 아니라, 출력 시점마다 다른 c[t]",
    notes="Bahdanau et al.(2014)의 핵심 식입니다. 점수 e를 Softmax로 비중 α로 바꾸고, Encoder 위치별 표현 h의 가중합으로 문맥 벡터 cₜ를 만듭니다. "
          "오른쪽 예제를 학생과 함께 손으로 계산해 보세요. 결과 (1.5, 1.6)은 어떤 v와도 같지 않습니다. 가장 큰 가중치 하나를 골라 복사하는 hard selection과 다르다는 점이 요점입니다. "
          "a는 원논문에서 작은 신경망(additive)이고, 이후 내적·bilinear 형태도 쓰입니다.")

d.image("정렬(Alignment)과 점수 함수", img("alignment.png"), img_w_ratio=0.54,
        side={"head": "점수 함수 a는 여러 가지", "body": [
            "**Bahdanau (2014)** additive: `vᵀ tanh(W s + U h)` — 작은 신경망, 양방향 RNN Encoder",
            "**Luong (2015)**: `dot` sᵀh · `general` sᵀWh · `concat`",
            "Luong은 전체를 보는 **global**과 일부 창만 보는 **local** attention도 비교",
            "Transformer의 점수 = Luong의 dot에 `1/√dₕ` 스케일을 더한 형태",
            "Heatmap은 ==관찰 도구==일 뿐, 예측의 인과적 설명과 같지 않다",
        ]},
        caption="그림: 설명용 가상 정렬(학습 결과 아님)",
        notes="Attention 가중치를 행렬로 그리면 출력 단어가 어느 입력 위치를 참조했는지 볼 수 있습니다. 영어와 한국어처럼 어순이 달라도 필요한 위치를 다시 찾는다는 것이 핵심입니다. "
              "그림의 숫자는 설명용으로 만든 값입니다. 원논문 Appendix와 Figure 3에 실제 정렬 예시가 있습니다. "
              "Luong et al.(2015)는 점수 함수를 dot/general/concat으로 정리했고, 이 중 dot이 이후 Transformer의 내적 점수로 이어집니다. "
              "질문 대비: heatmap이 높으면 그 단어 ‘때문에’ 번역했다고 말할 수 있나? → 관찰과 인과 설명은 별개입니다(Jain & Wallace 2019).")

d.table("Attention을 본체로 쓰면?", ["설계", "중심 질문", "계산의 특징"], [
    ["LSTM (1997)", "정보를 어떻게 보존하고 갱신할까?", "게이트로 기억 경로 설계, 순차 의존성 유지"],
    ["RNN + Attention (2014–15)", "현재 필요한 정보를 어느 입력 위치에서 가져올까?", "Encoder 위치별 표현 보관 + 시점별 가중합"],
    ["ConvS2S (2017)", "순환 없이 시퀀스를 병렬로 처리할 수 있을까?", "합성곱으로 비순환 Encoder–Decoder"],
    ["Transformer (2017)", "참조 연산으로 시퀀스의 표현 자체를 만들 수 있을까?", "Self-attention + FFN + 잔차 + 정규화 + 위치 정보"],
], col_widths=[2.6, 4.6, 5.0], highlight_rows=[3], size=19,
    lead="Self-attention은 2017년 이전에도 있었다 — Transformer는 ‘조합’의 설계",
    takeaway="“All You Need” ≠ Attention 외에는 아무 계산도 없다",
    notes="LSTM은 ‘어떻게 기억할까’, RNN+Attention은 ‘어디서 가져올까’, Transformer는 ‘참조만으로 표현을 만들 수 있을까’를 묻습니다. "
          "Self-attention(intra-attention)은 Cheng et al.(2016), Lin et al.(2017) 등에서 이미 쓰였고 원논문도 이를 인용합니다. "
          "2017년 Transformer는 이 계산을 FFN·잔차·정규화·위치 정보와 조합해 순환 없는 Encoder–Decoder를 만든 것입니다. 제목을 문자 그대로 읽지 않도록 강조하세요.")

# ============================================================ Part 02
d.section("02", "Transformer, 전체를 먼저 보기", "입력에서 확률까지 한 번 따라간 뒤, 블록을 확대한다",
          notes="Q/K/V 계산에 들어가기 전에 전체 지도를 먼저 봅니다. 오늘은 입력과 출력, 그리고 cross-attention의 화살표 방향만 확실히 잡으면 됩니다.")

d.image("2017년 Encoder–Decoder", img("transformer_arch.png"), img_w_ratio=0.6,
        lead="원형: Encoder 6층 + Decoder 6층 — 같은 설계를 반복하지만 층마다 파라미터는 별개",
        side={"head": "블록의 역할 한 문장", "body": [
            "**Embedding**: 토큰 ID → 벡터",
            "**위치 정보**: 순서 단서를 더한다",
            "**Attention**: 위치 간 정보 결합",
            "**FFN**: 위치별 비선형 변환",
            "**Residual · Norm**: 깊은 계산의 경로와 스케일",
            "**출력 head**: 어휘에 대한 점수(logits)",
            "Transformer ≠ LLM: 구조 vs 역할",
        ]},
        notes="원형 Transformer는 번역 같은 시퀀스 변환을 위해 제안되었습니다. 그림은 원논문과 달리 위에서 아래로 읽습니다. "
              "Source는 번역 대상 입력이고, Decoder에는 target이 한 칸 이동(shift)되어 들어갑니다. 자세한 이유는 다음 주에 다룹니다. "
              "최종 Encoder 출력 E는 모든 Decoder 층의 cross-attention으로 전달되어 K와 V를 만듭니다. 학생에게 화살표 방향을 직접 말하게 해 보세요. "
              "‘동일한 층’이라는 표현을 가중치 공유로 오해하지 않도록 합니다. Transformer는 계산 구조이고, 언어 모델은 시퀀스 확률을 학습하는 역할입니다.")

d.table("입력과 출력의 계약", ["기호", "의미", "수업 예시", "원논문 base"], [
    ["B", "Batch size", "2", "약 25k source + 25k target 토큰/배치"],
    ["S · T", "Source 길이 · Target 입력 길이", "5 · 3", "가변"],
    ["N", "일반 시퀀스 길이(self-attention)", "5", "가변"],
    ["d", "d_model, 토큰 표현 차원", "8", "512"],
    ["H", "Head 수", "2", "8"],
    ["dₕ", "Head당 차원 = d / H", "4", "64"],
    ["d_ff", "FFN 내부 차원", "32", "2048"],
    ["|V|", "Vocabulary 크기", "16 (실습)", "공유 BPE 약 37k (EN–DE)"],
    ["L", "층 수 (원논문 기호는 N)", "—", "Encoder 6 · Decoder 6"],
], col_widths=[1.3, 4.4, 2.2, 4.4], highlight_rows=[3, 4, 5, 6],
    lead="코드와 수식에서 같은 기호는 같은 뜻 — 층 수는 L, 시퀀스 길이는 N",
    notes="앞으로 모든 shape은 이 기호로 읽습니다. 수업 예시는 손으로 계산할 수 있게 d=8, H=2로 작게 잡았습니다. "
          "원논문 base 모델은 d=512, H=8, dₕ=64, d_ff=2048, 층 6+6이고 파라미터는 약 6500만 개입니다. "
          "원논문은 층 수에도 N을 쓰지만 우리는 혼동을 줄이려고 층 수를 L, 시퀀스 길이를 N으로 씁니다. "
          "입력 ID는 (B,S), Embedding 후 (B,S,d), 출력 logits는 (B,T,|V|)라는 계약을 기억하세요.")

d.table("세 종류의 Attention", ["종류", "Q를 만드는 원본", "K · V를 만드는 원본", "허용되는 참조"], [
    ["Encoder self-attention", "현재 Encoder 입력 표현", "같은 표현", "유효한 입력 토큰 전체"],
    ["Decoder masked self-attention", "현재 Decoder 입력 표현", "같은 표현", "현재 위치와 이전 위치"],
    ["Encoder–Decoder cross-attention", "Decoder self-attention 후 표현", "Encoder 최종 출력 E", "유효한 source 전체"],
], col_widths=[3.4, 3.2, 2.9, 2.8], size=21, highlight_rows=[2],
    lead="같은 연산, 다른 출처와 다른 허용 범위",
    takeaway="Self/Cross = Q와 K·V의 출처 축 · Causal/Bidirectional = 참조 허용 범위 축",
    notes="세 Attention은 계산식이 같고, Q와 K·V를 어디서 가져오는지와 어디까지 볼 수 있는지만 다릅니다. "
          "두 분류 축을 섞지 않도록 합니다. Cross-attention이 항상 causal인 것도, self-attention이 항상 양방향인 것도 아닙니다. "
          "Mask의 구현 세부(padding mask, causal mask)는 다음 주에 다루고, 오늘은 4토큰 예제에서 causal mask의 효과만 숫자로 확인합니다.")

# ============================================================ Part 03
d.section("03", "토큰에 순서 정보를 더하기", "위치 정보가 없는 Self-attention의 성질부터 확인한다",
          notes="Transformer에는 순환이 없습니다. 그렇다면 ‘몇 번째 토큰인가’는 어디서 알까요? 이 질문에서 위치 정보가 나옵니다.")

d.formula("Embedding lookup 이후", "X⁽⁰⁾ = Dropout( √d · E[ids] + PE )",
          parts=[("ids", "토큰 ID, shape (B,S)"),
                 ("E[ids]", "Embedding 표 (|V|,d)에서 행 조회 → (B,S,d)"),
                 ("√d", "원형 Transformer의 Embedding 스케일"),
                 ("PE", "같은 차원 d의 위치 벡터 (S,d) — 배치 축으로 broadcast"),
                 ("Dropout", "원형 base 설정 p = 0.1")],
          example=["B=2, S=5, d=8", "ids: (2,5)", "E[ids]: (2,5,8)", "× √8 ≈ 2.83", "+ PE (5,8) → **(2,5,8)**",
                   "원논문 d=512: √512 ≈ 22.6", "더해도 shape는 그대로"],
          takeaway="위치를 ‘더한다’ ≠ 내용과 위치를 완벽히 분리해 저장한다",
          notes="입력 ID (B,S)는 Embedding을 거쳐 (B,S,d)가 됩니다. 원형은 여기에 √d를 곱하고 같은 차원의 위치 벡터를 더합니다. Encoder와 Decoder 모두 같은 과정을 거칩니다. "
                "위치 벡터를 더해도 shape는 바뀌지 않습니다. 같은 차원에 내용과 위치 단서가 섞여 들어가는 것이지, 두 정보가 따로 칸을 나눠 저장되는 것은 아닙니다. "
                "PE는 배치마다 같으므로 (S,d)가 (B,S,d)로 broadcast된다는 1주차 개념을 다시 짚어 주세요.")

d.formula("왜 위치 정보가 필요한가", ["SA(PX) = softmax( P Q Kᵀ Pᵀ / √dₕ ) P V", "        = P · SA(X)"],
          parts=[("P", "순열 행렬: 토큰 순서를 섞는다 (Q′=PQ, K′=PK, V′=PV)"),
                 ("SA", "위치 정보와 위치 의존 mask가 없는 self-attention"),
                 ("등변성", "입력을 섞으면 출력도 ==같은 방식으로 섞인다=="),
                 ("불변성", "출력이 아예 안 변함 — 등변성과 다르다 (mean pooling 등을 붙일 때)")],
          example=["X = [x_A, x_B, x_C]", "→ [o_A, o_B, o_C]", "섞은 X = [x_C, x_A, x_B]", "→ [o_C, o_A, o_B]",
                   "각 토큰의 출력은 ‘어느 자리에 있었는지’와 무관", "“dog bites man” vs “man bites dog”을 구분할 단서가 없다"],
          takeaway="순서를 구분하려면 위치 단서가 필요하다 (단, causal mask가 있으면 이 증명은 그대로 성립하지 않음)",
          notes="행 단위 Softmax는 행과 열을 같은 순열로 섞어도 대응해서 움직이므로 SA(PX) = P·SA(X)가 성립합니다. 이것이 순열 등변성입니다. "
                "‘PE가 없으면 입력을 섞어도 출력이 그대로’라는 흔한 오개념(14번)을 바로잡으세요. 출력이 그대로인 것이 아니라 똑같이 섞입니다. "
                "Python으로 무작위 W와 순열 P를 만들어 allclose(SA(PX), P@SA(X))를 확인하는 것이 좋은 실습입니다. "
                "Causal mask가 있으면 방향 정보가 생기므로 이 증명을 그대로 적용할 수 없습니다.")

d.image("Sinusoidal position encoding", img("pe.png"),
        lead="PE(pos,2i) = sin(pos / 10000^(2i/d)),   PE(pos,2i+1) = cos(pos / 10000^(2i/d))",
        caption="d=8, pos=1 예: PE = [0.841, 0.540, 0.100, 0.995, 0.010, 1.000, 0.001, 1.000] — 차원쌍마다 주파수가 다르다",
        notes="짝수 차원은 sin, 홀수 차원은 cos이고, 차원쌍 i가 커질수록 주파수가 낮아져 천천히 변합니다. "
              "왼쪽 heatmap에서 앞쪽 차원은 위치마다 빠르게, 뒤쪽 차원은 거의 일정하게 변하는 것을 보세요. 오른쪽은 d=32에서 i=1, 3, 6의 곡선이며 실선이 sin, 점선이 cos입니다. "
              "캡션의 숫자는 d=8, pos=1을 직접 계산한 값입니다. 1/10000^(2i/8)이 1, 0.1, 0.01, 0.001이 되므로 sin·cos 값을 손으로 확인할 수 있습니다. "
              "여러 주파수의 조합이 각 위치에 고유한 패턴을 만들어 줍니다.")

d.cards("“Sin/cos가 정답”은 아니다", [
    {"head": "학습형 위치 임베딩", "body": ["원논문 Table 3 (E): 학습형으로 바꿔도 dev BLEU 25.7 vs 25.8 — 거의 같은 결과",
                                          "이후 RoPE(2021) 등 다른 방식도 널리 쓰인다"]},
    {"head": "긴 길이 일반화 보장 없음", "body": ["고정 함수라 더 긴 위치의 값을 ‘계산’할 수는 있다",
                                           "≠ 훈련보다 긴 길이에서 잘 ‘일반화’한다 — 원논문도 가능성으로만 언급"]},
    {"head": "Mask도 위치 단서", "body": ["Causal mask는 방향·경계에 대한 구조적 정보를 준다",
                                    "“PE를 지우면 모든 Transformer가 순서를 모른다”는 mask를 무시한 말"]},
    {"head": "공정한 제거 실험", "accent": True, "body": ["먼저 dropout을 끈 순수 self-attention 모듈에 순열 적용",
                                                    "전체 모델은 source·target 위치 정보를 따로 제거한 조건도 비교"]},
], cols=2, footer="위치 단서가 필요하다는 주장 ≠ 특정 함수가 필수라는 주장",
    notes="원논문은 sinusoid를 선택한 이유로 ‘학습 때보다 긴 길이로 외삽할 수도 있다’는 가능성을 들었지만, 이는 보장이 아닙니다. "
          "Table 3의 (E)행에서 학습형 위치 임베딩은 base와 거의 같은 결과였습니다. 이후 RoPE(2021) 같은 다른 방식도 널리 쓰입니다. "
          "위치 정보 제거 실험을 설계할 때는 source 위치, decoder 위치, causal mask, 학습 과정이 함께 관여한다는 점을 기억하세요.")

# ============================================================ Part 04
d.section("04", "Q · K · V와 Scaled Dot-Product", "같은 입력에서 비교 기준과 가져올 정보를 따로 만든다",
          notes="이제 Attention 한 번의 계산을 정확히 봅니다. Q/K/V의 정의 → 4토큰 숫자 예제 → √dₕ와 mask 순서로 갑니다.")

d.image("학습되는 것은 투영 행렬", img("qkv_proj.png"), img_w_ratio=0.58,
        side={"head": "Q = X W_Q,  K = X W_K,  V = X W_V", "body": [
            "한 Head에서 X: `(N,d)`, W_Q·W_K: `(d,dₕ)` → Q·K: `(N,dₕ)`",
            "V의 차원 dᵥ는 dₕ와 달라도 되지만 원형과 실습은 **dᵥ = dₕ** (base 64)",
            "개념 수식에서는 bias 생략",
            "W는 ==학습되는 파라미터==, Q·K·V는 입력마다 계산되는 ==활성값==",
        ]},
        notes="Q, K, V는 입력 X에 서로 다른 학습 행렬 W_Q, W_K, W_V를 곱해 만듭니다. 학습되는 것은 행렬 W이고, Q·K·V 자체는 입력이 바뀔 때마다 새로 계산됩니다. "
              "Shape를 소리 내어 읽게 하세요. (N,d) @ (d,dₕ) = (N,dₕ). 안쪽 차원 d가 맞아야 곱할 수 있습니다. "
              "원논문 base에서는 d=512, dₕ=dᵥ=64입니다.")

d.table("Q · K · V의 역할과 비유의 한계", ["벡터", "계산에서의 역할", "비유의 한계"], [
    ["Query", "현재 위치가 Key들과 비교할 벡터", "사용자가 입력한 자연어 질문 자체가 아님"],
    ["Key", "각 위치를 비교하기 위한 벡터", "단어 문자열이나 database key와 동일하지 않음"],
    ["Value", "가중합으로 실제 결합될 벡터", "원래 Embedding을 그대로 복사할 필요 없음"],
], col_widths=[1.8, 5.0, 5.5], size=21,
    lead="이름은 검색 비유에서 왔지만, 정의는 계산 역할로",
    takeaway="Query는 외부 질문이 아니라 비교의 기준 — ‘질문’이 없는 이미지 Encoder에도 Q가 있다",
    notes="Query·Key·Value라는 이름은 검색 시스템 비유에서 왔습니다. 하지만 비유를 너무 믿으면 ‘Query는 사용자의 질문’ 같은 오개념(8번)이 생깁니다. "
          "‘Query가 중요한 토큰을 찾는다’에서 멈추면 목적 함수와 중요도를 혼동합니다. 실제로는 학습된 내적 점수로 가중합을 만들고, 그 결과가 최종 loss를 줄이는 방향으로 학습됩니다. "
          "‘중요도’라는 말을 쓸 때는 어떤 기준의 중요도인지 먼저 정의하게 하세요.")

d.compare("Self-attention이라고 Q=K=V는 아니다", {
    "head": "Q ≠ K ≠ V, 점수도 비대칭", "body": [
        "원본 X가 같아도 W_Q, W_K, W_V가 다르면 값이 다르다",
        "QKᵀ는 일반적으로 비대칭: 4토큰 예제에서 `q_B·k_D = 1`, `q_D·k_B = 0.5`",
        "점수가 대칭이어도 행별 Softmax 후엔 비대칭: `S[A,B] = S[B,A] = 0` → `A[A,B] = 0.18`, `A[B,A] = 0.14`",
        "Softmax는 행(Query)마다 따로 정규화 — 각 Query가 자기 행 안에서 비중을 나눈다",
    ]}, {
    "head": "왜 점수용과 내용용을 나눌까", "accent": True, "body": [
        "**어떤 특징으로 찾을지**(Q·K)와 **무엇을 전달할지**(V)를 따로 학습할 자유",
        "비교 기준과 가져올 특징을 같은 좌표계에 묶지 않아도 된다",
        "Q·K 공간은 ‘누구와 관련 있나’, V 공간은 ‘무엇을 보낼까’ — dᵥ가 dₕ와 달라도 되는 이유",
        "각 축이 ‘주어’, ‘동사’, ‘중요도’로 미리 지정된 것은 ==아니다== — 표현 설계의 선택",
    ]}, vs="≠",
    notes="Self-attention은 Q, K, V를 같은 시퀀스에서 만든다는 뜻이지 세 값이 같다는 뜻이 아닙니다(오개념 7번). "
          "‘A가 B를 보는 비중’과 ‘B가 A를 보는 비중’은 다를 수 있습니다. 예제 숫자는 잠시 후 4토큰 예제에서 직접 확인합니다. "
          "점수와 내용을 나누는 것은 표현 설계의 선택입니다. 축의 의미는 학습 결과이지 사전에 정해진 것이 아닙니다.")

d.table("파라미터와 활성값의 차이", ["구분", "예", "입력마다 바뀌나?", "학습으로 갱신되나?"], [
    ["파라미터", "W_Q, W_K, W_V, W_O", "같은 모델 forward에서는 공유", "Optimizer가 갱신"],
    ["활성값", "X, Q, K, V", "입력과 이전 층에 따라 계산", "그 자체가 고정 학습 표는 아님"],
    ["Attention 가중치", "A = softmax(QKᵀ/√dₕ)", "입력마다 계산", "gradient 경로에 포함되지만 고정 표는 아님"],
], col_widths=[2.2, 3.2, 3.4, 3.5], size=20, highlight_rows=[2],
    lead="‘weight’라는 한 단어로 W와 A를 뭉뚱그리지 않는다",
    takeaway="추론 때 W가 고정되어도 A는 입력마다 다르다 — 정적인 파라미터로 동적인 정보 결합을 계산",
    notes="‘attention weight’라는 말은 학습 파라미터 W가 아니라 입력별로 계산되는 A를 뜻하는 경우가 많습니다. "
          "학습이 끝나 W가 고정되어도, 문장이 바뀌면 A는 달라집니다. 이것이 Attention이 ‘동적인’ 연산이라는 의미입니다. "
          "학생에게 그림을 그릴 때 고정 파라미터 W와 입력별 활성값 A를 다른 색으로 표시하게 하세요.")

d.formula("Cross-attention: 출처가 바뀐다", "Q = D W_Q,   K = E W_K,   V = E W_V",
          parts=[("D", "Decoder 쪽 T개 위치의 표현 (B,T,d)"),
                 ("E", "Encoder 최종 출력 S개 위치 (B,S,d)"),
                 ("QKᵀ", "점수 행렬 (B,T,S): 행 = Decoder Query, 열 = Source Key"),
                 ("출력", "(B,T,d): 출력 위치 수 = Query 수 T")],
          example=["B=2, T=3, S=5, d=8 (Head 1개)", "Q: (2,3,8)", "K, V: (2,5,8)", "QKᵀ: (2,3,5)",
                   "A V: (2,3,5)@(2,5,8) → **(2,3,8)**", "source 길이 5로 출력 길이가 바뀌지 ==않는다=="],
          takeaway="Cross-attention의 출력 길이는 항상 Query 길이 T",
          notes="Cross-attention에서는 Q는 Decoder에서, K와 V는 Encoder 출력 E에서 옵니다. 그래서 점수 행렬은 T×S입니다. "
                "출력은 Query 하나당 벡터 하나이므로 길이 T가 유지됩니다. 개념 확인 9번 문제와 직결됩니다. "
                "Shape를 숫자로만 외우면 cross-attention에서 틀리기 쉽습니다. 축 이름(T, S)으로 읽게 하세요.")

d.formula("Scaled Dot-Product Attention", ["A = softmax_key( QKᵀ / √dₕ + M )", "O = A V"],
          parts=[("Q, K", "Query (T,dₕ) · Key (S,dₕ)"),
                 ("QKᵀ", "(T,S) 점수 표: 행 = Query, 열 = Key"),
                 ("√dₕ", "점수 크기를 조절하는 스케일"),
                 ("M", "mask: 허용 0, 차단 −∞"),
                 ("softmax_key", "Key 축(마지막 축)으로 정규화 → 각 행 합 1 (dropout 전)"),
                 ("O = AV", "(T,dᵥ): 각 행 = 그 Query가 만든 Value의 가중합")],
          takeaway="점수 → 스케일 → mask → 확률 → 가중합, 다섯 단계를 분리해서 읽는다",
          notes="공식은 짧지만 계산은 다섯 단계입니다. 내적으로 점수를 만들고, √dₕ로 나누고, mask를 더하고, Key 축으로 Softmax를 하고, V와 곱합니다. "
                "행은 Query, 열은 Key입니다. Softmax는 Key 축을 따라 적용하므로, 유효한 Key가 있고 dropout 전이라면 각 행의 합은 1입니다. "
                "원논문 식 (1)은 softmax(QKᵀ/√d_k)V이고, 우리는 d_k 대신 Head 차원 dₕ로 씁니다.")

d.image("4토큰 예제: Query A를 손으로", img("attn_setup.png"), img_w_ratio=0.55,
        side={"head": "q_A = (1, 0), dₕ = 2", "body": [
            "① 점수 q_A·k: `[1, 0, 1, −1]`",
            "② ÷ √2: `[0.71, 0, 0.71, −0.71]`",
            "③ exp: `[2.03, 1, 2.03, 0.49]`, 합 5.55",
            "④ softmax: `[0.365, 0.180, 0.365, 0.089]`",
            "⑤ o_A = 0.365·(1,0) + 0.180·(0,1) + 0.365·(2,2) + 0.089·(−1,1) = ==(1.01, 1.00)==",
            "확인: 가중치 합 = 1 · k_A와 k_C는 점수가 같아 가중치도 같다",
        ], "bullets": False},
        notes="A·B·C·D는 의미가 없는 예시 토큰이고, 숫자도 학습 결과가 아니라 설명용입니다. "
              "Query A=(1,0)을 선택해 네 Key와 내적하면 [1,0,1,−1]입니다. √2로 나누고 exp를 취해 합으로 나누면 가중치가 나옵니다. "
              "A와 C의 Key가 q_A와 같은 점수를 받으므로 같은 가중치 0.365를 받습니다. 마지막으로 V의 가중합을 구하면 (1.01, 1.00)입니다. "
              "학생이 계산기를 들고 ③, ④를 직접 해 보게 하세요. 결과를 보기 전에 ‘어떤 Key가 가장 클까’를 먼저 예측하게 합니다.")

d.image("전체 행렬로: 점수 → A → O", img("attn_pipeline.png"),
        lead="나머지 Query도 같은 규칙 — 네 행을 한 번의 행렬곱으로",
        caption="각 행의 A 합 = 1 (표시값은 반올림) · O의 각 행 = 해당 Query가 만든 V의 가중합 · 주황 테두리 = 앞 장의 Query A",
        notes="앞 장에서 한 행을 계산했다면, 행렬곱은 네 Query를 동시에 처리할 뿐입니다. QKᵀ는 (4,2)@(2,4)=(4,4), A V는 (4,4)@(4,2)=(4,2)입니다. "
              "q_B는 k_B, k_C, k_D와 같은 점수를 받아 세 곳에 0.29씩 나눠 줍니다. q_D는 k_D를 가장 많이 봅니다. "
              "생각해 볼 질문: Q와 K를 고정하고 V만 바꾸면 A와 O는? → A는 Q, K, mask로만 결정되므로 그대로이고, O = AV는 바뀝니다.")

d.image("Causal mask: 미래 Key 차단", img("causal.png"),
        lead="Query는 자기 위치와 이전 Key만 참조 — 차단은 Softmax ==전에== −∞로",
        caption="q_A는 k_A만 볼 수 있어 o_A = v_A = (1, 0) · 오른쪽: 0으로만 바꾸면 exp(0)=1이라 미래 Key가 여전히 가중치를 받는다",
        notes="Causal mask는 미래 위치의 점수에 −∞(구현에서는 매우 작은 값)를 더합니다. exp(−∞)=0이므로 Softmax 이후 그 칸은 정확히 0입니다. "
              "오른쪽 그림처럼 점수를 0으로만 바꾸면 exp(0)=1이 되어 미래 Key가 오히려 상당한 비중을 받습니다(오개념 15번, 개념 확인 7번). "
              "또 Key mask와 Query는 다릅니다. 예를 들어 D Key를 차단해도 D Query의 출력이 자동으로 사라지지는 않습니다. "
              "Decoder에서 mask가 왜 필요한지와 target shift는 다음 주에 자세히 다룹니다.")

d.image("왜 √dₕ로 나눌까", img("sqrt_scale.png"),
        lead="q, k 성분이 독립·평균 0·분산 1이면 Var(q·k) = dₕ → Var(q·k / √dₕ) = 1",
        caption="dₕ가 커질수록 점수가 커져 Softmax가 지나치게 뾰족해진다 — 스케일은 이를 완화하려는 장치(학습된 Q/K가 가정을 정확히 따른다는 뜻은 아님)",
        notes="단순화한 가정에서 dₕ개 항의 합인 내적은 분산이 dₕ입니다. 왼쪽 그림처럼 표준편차가 √dₕ로 커지고, √dₕ로 나누면 1 근처로 돌아옵니다. "
              "오른쪽은 dₕ=64에서 Key 8개에 대한 무작위 예시입니다. 스케일이 없으면 가중치 0.98이 한 곳에 몰리고, 스케일 후에는 최대 0.35로 퍼집니다. 뾰족한 Softmax는 gradient가 매우 작아지는 문제로 이어집니다. "
              "원논문 §3.2.1은 큰 d_k에서 스케일 없는 내적 attention이 additive attention보다 나빠지는 이유를 이렇게 설명합니다. "
              "4토큰 예제에서도 q_A를 4배 키우면 가중치가 [0.485, 0.029, 0.485, 0.002]로 뾰족해집니다.")

d.cards("가중치 해석과 경계 조건", [
    {"head": "높은 α ≠ 큰 영향", "body": "V의 크기·방향이 다르고 뒤에 W_O, residual, FFN, 다음 층이 있다 — 숫자 하나로 출력 변화를 다 알 수 없다"},
    {"head": "Heatmap ≠ 인과 설명", "body": "유용한 관찰 도구지만 예측의 이유를 증명하지 않는다 (Jain & Wallace 2019; Wiegreffe & Pinter 2019)"},
    {"head": "모든 Key가 가려진 행", "body": "Softmax 분포가 정의되지 않음 → 구현마다 NaN·0 — 유효한 Query마다 허용 Key ≥ 1개", "accent": True},
    {"head": "Dropout 이후 행 합", "body": "Attention dropout 후에는 행 합이 정확히 1이 아닐 수 있다 → 단위 테스트는 dropout을 끄고"},
    {"head": "V만 바꾸면?", "body": "A는 Q·K·mask로만 결정 → 그대로. O = AV는 바뀐다 (단, X를 바꾸면 Q·K·V가 함께 바뀜)"},
    {"head": "Q를 키우면?", "body": "q_A × 4 → A = [0.485, 0.029, 0.485, 0.002]: 분포가 뾰족, entropy ↓ — 낮은 entropy ≠ 좋은 예측"},
], cols=3, footer="Heatmap에는 ‘이 그림이 보여주는 것’과 ‘증명하지 않는 것’을 한 문장씩 붙인다",
    notes="가중치가 크면 해당 V의 기여 비중이 커지지만, V의 크기와 방향이 다르고 뒤에 여러 연산이 있으므로 가중치 하나로 최종 출력 변화를 알 수 없습니다. "
          "모든 Key가 가려진 행은 Softmax가 정의되지 않으므로 입력과 mask를 설계할 때 주의합니다. PyTorch 등 구현에 따라 NaN이 나올 수 있습니다. "
          "아래 두 카드는 시뮬레이터 질문입니다. 학생이 먼저 예측하고 나서 숫자로 확인하게 하세요.")

# ============================================================ Part 05
d.section("05", "Multi-head와 Tensor Shape", "토큰을 나누는 것이 아니라, 투영된 표현의 부분공간을 병렬로 처리한다",
          notes="마지막 파트입니다. Multi-head는 새로운 연산이 아니라 같은 Attention을 여러 부분공간에서 병렬로 하는 것입니다. 핵심은 shape 추적입니다.")

d.formula("여러 비교·전달 경로 만들기", ["head_h = Attention( X W_Q⁽ʰ⁾, X W_K⁽ʰ⁾, X W_V⁽ʰ⁾ )",
                                     "MHA(X) = Concat( head_1, …, head_H ) W_O"],
          parts=[("W_Q⁽ʰ⁾", "Head h의 투영 (d, dₕ) — 입력은 원래 d차원 전체"),
                 ("head_h", "(N, dₕ): 모든 토큰 위치를 처리"),
                 ("Concat", "(N, H·dₕ) = (N, d)"),
                 ("W_O", "(d, d): 여러 Head의 특징을 결합")],
          example=["원논문 base: d=512, H=8", "→ dₕ = 512/8 = **64**", "각 Head: N개 토큰 전부 × 64 특징",
                   "Concat: 8 × 64 = 512", "Head 1 = 앞쪽 토큰, Head 2 = 뒤쪽 토큰 ==아님=="],
          takeaway="Multi-head는 토큰을 나누지 않고, 투영된 특징의 부분공간을 나눈다",
          notes="각 Head는 자기만의 W_Q, W_K, W_V로 d차원 입력 전체를 dₕ차원으로 투영하고, 모든 토큰 위치에 대해 Attention을 계산합니다. "
                "여러 Head의 결과를 이어 붙인 뒤 W_O로 섞습니다. 이렇게 하면 여러 종류의 비교·전달 경로를 동시에 가질 수 있습니다. "
                "오개념 11번 ‘Multi-head는 토큰을 Head별로 나눈다’를 여기서 바로잡으세요.")

d.image("한 번 투영하고 Head 축을 만든다", img("mha_shapes.png"),
        lead="(B,N,d) → 선형 투영 → (B,N,H,dₕ) → 축 교환 → (B,H,N,dₕ)",
        caption="여러 Head의 투영을 큰 행렬 하나로 묶어 계산 = 독립된 선형 투영 H개를 병렬로 계산하는 것과 같다",
        notes="구현에서는 Head마다 따로 곱하지 않고, (d,d) 크기 행렬 하나로 한 번에 투영한 뒤 마지막 축을 (H,dₕ)로 쪼갭니다. "
              "그다음 transpose로 Head 축을 앞으로 보내 (B,H,N,dₕ)를 만들면, 마지막 두 축에 대해 행렬곱을 하는 것만으로 Head별 Attention이 병렬 계산됩니다. "
              "되돌릴 때는 transpose 후 reshape합니다. reshape 전에 transpose가 필요한지, 메모리 배치와 축의 의미가 맞는지 확인하는 습관이 중요합니다.")

d.table("d=8, H=2, N=5를 직접 따라가기", ["단계", "Shape", "축의 의미"], [
    ["입력 X", "(2, 5, 8)", "문장 2개, 토큰 5개, 특징 8개"],
    ["Q·K·V 투영", "(2, 5, 8)", "투영 후 전체 특징 폭"],
    ["Head 분리 (view + transpose)", "(2, 2, 5, 4)", "Batch, Head, Token, Feature"],
    ["QKᵀ → A", "(2, 2, 5, 5)", "Head별 위치 관계 (Query × Key)"],
    ["A V", "(2, 2, 5, 4)", "Head별 새 표현"],
    ["Head 결합 (transpose + reshape)", "(2, 5, 8)", "원래 d로 결합"],
    ["W_O 투영", "(2, 5, 8)", "여러 Head의 특징 결합"],
    ["Cross (T=3, S=5)일 때 A", "(2, 2, 3, 5)", "Query 쪽 T, Key 쪽 S"],
], col_widths=[4.2, 2.6, 5.5], highlight_rows=[3, 7],
    lead="B=2, N=5, d=8, H=2 → dₕ = 4",
    takeaway="축을 숫자가 아니라 이름으로 읽는다 — (B, H, Query, Key)",
    notes="각 축을 숫자가 아니라 이름으로 읽게 합니다. (2,2,5,5)는 ‘배치 2, Head 2, Query 5, Key 5’입니다. "
          "마지막 행은 cross-attention의 경우입니다. Q는 (2,2,3,4), K·V는 (2,2,5,4)이므로 A는 (2,2,3,5)가 되고 출력은 (2,3,8)입니다. "
          "원논문 base로 바꾸면 (B,N,512) → (B,8,N,64)입니다. 개념 확인 5번과 연결됩니다.")

d.code("코드로 shape 확인 (PyTorch)", """import torch, torch.nn.functional as F
B, N, d, H = 2, 5, 8, 2; dh = d // H
x = torch.randn(B, N, d)                  # (2,5,8)
W_qkv = torch.nn.Linear(d, 3*d, bias=False)
W_o = torch.nn.Linear(d, d, bias=False)
q, k, v = W_qkv(x).chunk(3, dim=-1)       # 각 (2,5,8)
sp = lambda t: t.view(B, N, H, dh).transpose(1, 2)
q, k, v = sp(q), sp(k), sp(v)             # (2,2,5,4)
s = q @ k.transpose(-2, -1) / dh**0.5     # (2,2,5,5)
A = torch.softmax(s, dim=-1)              # Key 축
o = A @ v                                 # (2,2,5,4)
ref = F.scaled_dot_product_attention(q, k, v)
print(torch.allclose(o, ref, atol=1e-6))  # True
y = W_o(o.transpose(1, 2).reshape(B, N, d))  # (2,5,8)""",
       explain=["`chunk`: 한 번 투영 후 Q·K·V로 나눔",
                "`sp`: `view` → `transpose(1,2)`로 Head 축을 앞으로",
                "`softmax(dim=-1)`: 마지막 축 = ==Key 축==",
                "공식 구현 `scaled_dot_product_attention`과 결과 일치",
                "결합 전 `transpose`를 빼먹으면 토큰과 Head가 섞인다"],
       notes="앞 장의 shape 표를 코드 14줄로 옮긴 것입니다. 실제로 실행해 보면 직접 계산한 o와 PyTorch의 scaled_dot_product_attention 결과가 일치합니다. "
             "softmax(dim=-1)의 마지막 축이 정말 Key 축인지 확인하는 것이 실무에서 가장 흔한 점검 항목입니다. "
             "과제: 결합 단계에서 transpose를 빼고 reshape만 하면 어떤 일이 생기는지 확인해 보세요. shape는 맞지만 의미가 틀립니다.")

d.image("Head 수와 Head의 역할", img("heads.png"), img_w_ratio=0.6,
        side={"head": "d 고정, dₕ = d/H로 H를 늘리면", "body": [
            "투영 파라미터 ≈ `4d²` **유지** (d=512 → 약 105만)",
            "주요 곱셈량 `H·N²·dₕ = N²d` **유지**",
            "저장하는 Attention 표 `H·N²`은 **증가** (N=100: H=1 → 1만, H=8 → 8만)",
            "Head당 차원 dₕ는 **감소** (512/8 = 64)",
            "역할은 미리 지정되지 않는다: ==관찰 · 해석 · 인과 검증==을 구분해 보고",
        ]},
        notes="d를 고정하고 dₕ=d/H로 두면 네 투영 행렬(W_Q, W_K, W_V, W_O)의 파라미터는 약 4d²로 그대로이고, 주요 곱셈량도 N²d로 같습니다. "
              "하지만 명시적으로 저장하는 Attention 표의 원소 수는 HN²이라 Head 수에 따라 늘고, 커널 효율도 달라집니다. 같은 d에서 Head를 늘리는 실험과 dₕ를 고정하고 d를 늘리는 실험은 다릅니다. "
              "왼쪽 그림은 무작위 가중치로 만든 두 Head의 패턴입니다. 서로 다른 패턴이 보이지만, ‘1번은 문법, 2번은 의미’ 같은 역할이 아키텍처에 지정된 것은 아닙니다. "
              "Heatmap에는 ‘이 그림이 보여주는 것’과 ‘증명하지 않는 것’을 한 문장씩 붙이게 하세요.")

# ============================================================ 마무리
d.table("흔한 오개념 바로잡기", ["#", "흔한 표현", "더 정확한 설명"], [
    ["6", "Transformer가 Attention을 처음 만들었다", "이전 attention을 중심으로 비순환 구조를 조합했다"],
    ["7", "Self-attention은 Q=K=V다", "원본 표현은 같아도 학습 투영이 다르다"],
    ["8", "Query는 사용자의 질문 문장이다", "Attention에서 비교 기준이 되는 벡터의 역할이다"],
    ["9", "Attention은 가장 중요한 토큰 하나를 고른다", "일반적인 soft attention은 Value들의 연속 가중합이다"],
    ["10", "Attention score는 항상 대칭이다", "서로 다른 Q/K와 행별 Softmax 때문에 일반적으로 아니다"],
    ["11", "Multi-head는 토큰을 Head별로 나눈다", "특징 투영을 나누며 각 Head는 전체 위치를 처리한다"],
    ["14", "PE가 없으면 입력을 섞어도 출력이 그대로다", "출력도 같은 순열로 움직이는 등변성을 갖는다"],
    ["15", "미래 점수를 0으로 만들면 mask가 된다", "Softmax 전 −∞ 등으로 차단한다 (exp(0)=1)"],
    ["20", "Attention heatmap은 모델의 생각을 증명한다", "관찰 자료이며 인과 설명은 별도 검증이 필요하다"],
], col_widths=[0.7, 5.3, 6.3], size=17,
    notes="원자료의 오개념 20가지 중 오늘 내용과 관련된 9개입니다. 번호는 원자료 번호를 그대로 썼습니다. "
          "학생에게 왼쪽 문장만 보여 주고 무엇이 틀렸는지 먼저 말하게 한 뒤 오른쪽을 공개하면 좋습니다. "
          "모든 항목을 오늘 한 계산이나 shape로 반박할 수 있는지 확인해 보세요.")

d.quiz("개념 확인 ①", [
    ("**04.** Self-attention의 Q, K, V는?  (A) 항상 같은 숫자  (B) 같은 원본에서 서로 다른 투영으로 만들 수 있다  (C) 사용자가 세 개를 따로 입력",
     "B. 원본 X를 공유해도 W_Q, W_K, W_V가 다르므로 결과는 일반적으로 다르다."),
    ("**05.** Q: (B,H,T,dₕ), K: (B,H,S,dₕ)일 때 QKᵀ는?  (A) (B,H,dₕ,dₕ)  (B) (B,H,S,T)  (C) (B,H,T,S)",
     "C. dₕ는 내적하면서 합쳐지고, T개 Query와 S개 Key의 관계 표가 남는다."),
    ("**06.** Attention의 Softmax는 보통 어느 축?  (A) 각 Query에 대한 Key 축  (B) Batch 축  (C) Head 축",
     "A. 각 Query가 여러 Key를 어떤 비중으로 참조할지 정해야 하므로 Key 축에서 정규화한다."),
    ("**07.** Causal mask에서 미래 점수를 0으로만 바꾸면?  (A) 완전히 차단된다  (B) exp(0)=1이므로 차단되지 않는다  (C) 과거 토큰도 제거된다",
     "B. Softmax 이후 확률을 0으로 만들려면 Softmax 전에 −∞ 등으로 처리한다."),
], notes="원자료 개념 확인 04–07번입니다. 답을 고르게 한 뒤, 정답보다 틀린 선택지가 왜 틀렸는지를 설명하게 하세요.")

d.quiz("개념 확인 ②", [
    ("**08.** 정답을 한 칸 이동시킨 Decoder에서 대각선 참조는?  (A) 항상 정답 누출  (B) Encoder에서만 가능  (C) 현재 입력이 다음 정답보다 한 칸 앞이므로 허용할 수 있다",
     "C. 현재 입력 위치의 토큰과 그 위치에서 예측할 정답은 다르다. Shift와 causal mask를 함께 해석한다(6주차에 자세히)."),
    ("**09.** Q 길이 3, K/V 길이 5인 Cross-attention의 출력 길이는?  (A) 3  (B) 5  (C) 8",
     "A. 출력은 Query 하나당 벡터 하나이므로 Query 길이를 보존한다."),
    ("**10.** 같은 d에서 Head 수 H를 늘리면?  (A) 각 Head가 일부 token만 본다  (B) 주요 투영 파라미터는 유지, Head당 차원은 감소  (C) 전체 d가 자동으로 늘어난다",
     "B. dₕ=d/H를 쓰면 전체 투영 폭은 그대로이고 Head당 차원이 작아진다. Explicit attention 표 수는 늘 수 있다."),
    ("**생각해 보기.** 4토큰 예제에서 Q와 K를 고정하고 V만 바꾸면 A는 바뀌는가? O는?",
     "A는 Q, K, mask만으로 결정되므로 바뀌지 않는다. O = AV는 일반적으로 바뀐다."),
], notes="08번은 다음 주 target shift와 연결되는 예고 문제입니다. 지금은 ‘현재 입력 토큰과 예측할 정답은 한 칸 차이’라는 점만 짚으세요. "
         "마지막 문항은 앞의 4토큰 예제를 다시 떠올리게 하는 문제입니다.")

s = d.blank("이번 주 과제와 참고 자료",
            notes="과제는 제출 결과가 분명한 형태로 냈습니다. ‘논문 읽고 정리’ 대신 Figure 1에 Q/K/V 출처를 표시하고 식 (1)의 shape를 쓰는 식입니다. "
                  "참고 자료는 오늘 범위의 원논문만 추렸습니다. 읽는 순서는 Seq2Seq → Bahdanau → Attention Is All You Need 순이 좋습니다. "
                  "Transformer 논문은 Figure 1–2와 §3을 중심으로 읽게 하세요.")
lw = 5.6
d.box(s, X0, Y0 + 0.05, lw, Y1 - Y0 - 0.05, fill=ACCENT_BG)
d.text(s, X0 + 0.2, Y0 + 0.15, lw - 0.4, 0.5, "이번 주 과제", size=19, bold=True, color=ACCENT, anchor="m")
d.text(s, X0 + 0.2, Y0 + 0.75, lw - 0.4, Y1 - Y0 - 0.9, [
    "**손계산**: 4토큰 예제에서 Query B, C, D의 A와 O를 계산하고 causal mask를 켠 결과와 비교",
    "**그림에 표시**: 원논문 Figure 1에서 cross-attention의 Q / K·V 출처와 각 화살표의 shape 적기",
    "**코드 검사**: 무작위 W와 순열 P로 `SA(PX) = P·SA(X)`를 `allclose`로 확인",
    "**Shape 구술**: d=512, H=8, S=7, T=4일 때 입력부터 cross-attention 출력까지 축 이름으로 설명",
], size=15, bullets=True, min_size=11, para_gap=0.5)
rx = X0 + lw + 0.3
rw = X1 - rx
d.box(s, rx, Y0 + 0.05, rw, Y1 - Y0 - 0.05, fill=MINT)
d.text(s, rx + 0.2, Y0 + 0.15, rw - 0.4, 0.5, "참고 자료 (원자료 번호)", size=19, bold=True, color=TEAL, anchor="m")
d.text(s, rx + 0.2, Y0 + 0.75, rw - 0.4, Y1 - Y0 - 0.9, [
    "[15] Cho et al. (2014) RNN Encoder–Decoder — arXiv:1406.1078",
    "[16] Sutskever, Vinyals & Le (2014) Seq2Seq — arXiv:1409.3215",
    "[17] Bahdanau, Cho & Bengio (2014 / ICLR 2015) Jointly Learning to Align and Translate — arXiv:1409.0473",
    "[18] Luong, Pham & Manning (2015) Attention-based NMT — arXiv:1508.04025",
    "[21] Gehring et al. (2017) ConvS2S — arXiv:1705.03122",
    "[22] Vaswani et al. (2017) Attention Is All You Need — arXiv:1706.03762 (Fig. 1–2, §3)",
    "[27][28] PyTorch scaled_dot_product_attention · MultiheadAttention 문서",
    "[39] Jain & Wallace (2019) · [40] Wiegreffe & Pinter (2019) Attention과 설명",
], size=13, bullets=True, min_size=9, para_gap=0.3)

d.summary("오늘의 정리", [
    "**병목 → Attention**: 위치별 표현을 남기고 출력 시점마다 점수 → Softmax → 가중합으로 다른 c[t]를 만든다",
    "**Transformer(2017)**: Attention을 본체로, FFN·잔차·정규화·위치 정보를 조합한 Encoder 6 + Decoder 6",
    "**위치 정보**: PE 없는 self-attention은 순열 등변 — sinusoidal PE는 하나의 선택지일 뿐",
    "**Q·K·V**: 같은 X라도 학습된 W_Q·W_K·W_V로 따로 투영; cross-attention은 Q ← Decoder, K·V ← Encoder",
    "**softmax(QKᵀ/√dₕ)V**: 행 = Query, Key 축 Softmax, √dₕ로 뾰족함 완화, mask는 Softmax 전 −∞",
    "**Multi-head**: (B,N,d) → (B,H,N,dₕ) → (B,N,d) — 토큰이 아니라 특징 부분공간을 나눈다",
], next_week="6주차 Transformer 완성 — FFN · Residual · LayerNorm, mask와 teacher forcing, 학습, 추론(KV cache), 그리고 그 이후",
    notes="오늘은 Attention의 등장부터 Transformer의 핵심 연산까지 왔습니다. 여섯 문장을 학생이 자기 말로 다시 설명할 수 있는지 확인하세요. "
          "다음 주에는 블록의 나머지 부품인 FFN, Residual, LayerNorm을 붙이고, mask와 teacher forcing으로 학습하는 법, 한 토큰씩 생성하는 추론과 KV cache, 그리고 ViT·DiT 같은 Transformer 이후의 흐름까지 다룹니다.")

d.save(OUT)
print("saved", OUT, "content slides:", d.n)
