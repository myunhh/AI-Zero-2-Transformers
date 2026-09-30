"""Week 5 — Attention: 필요할 때 원문을 다시 찾아보면?"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from deckkit import *  # noqa

A = lambda p: os.path.join(HERE, "assets", p)
OUT = os.path.join(HERE, "..", "lectures", "week05_attention.pptx")

d = Deck(5, "Attention: 원문을 다시 찾아보기", date="2026-11-02")

# ============================================================ 도입
d.question("필요할 때 원문을\n다시 찾아보면?",
           "2014–2017 · Attention · Self-attention · Q/K/V · Multi-head · 위치 정보",
           notes="Transformer 파트의 시작. 지난주 Seq2Seq는 입력 전체를 벡터 하나로 압축해야 했다. 오늘은 그 압축을 풀어 버린다: "
                 "입력의 위치별 표현을 모두 남겨 두고, 필요할 때마다 다른 비중으로 다시 참조한다. "
                 "이 한 가지 아이디어가 Self-attention, Q/K/V, Multi-head로 자라나 Transformer의 중심이 된다.")

d.bridge(["문장을 토큰·임베딩으로", "RNN · LSTM으로 순서와 기억", "Seq2Seq: Encoder → **c** → Decoder"],
         ["모든 입력을 **고정 벡터 c 하나**로 압축 — 병목", "h_t는 h_(t−1)이 필요 — **순차 계산**"],
         ["**필요할 때 원문을 다시 찾아보면?**", "그리고 그것을 모델의 **본체**로 쓰면?"])

d.roadmap(["Attention (2014): 출력마다 다른 요약", "Self-attention과 Q · K · V", "Scaled dot-product를 숫자로",
           "Multi-head와 tensor shape", "순서 정보: 위치 인코딩", "모아 보기: 2017 Transformer의 윤곽"],
          ["Attention의 **점수 → softmax → 가중합**을 손으로 계산한다",
           "Q · K · V의 역할과 **투영 행렬**(파라미터) vs **A**(활성값)를 구분한다",
           "softmax(QKᵀ/√d_h)V의 **shape**을 단계마다 말한다",
           "Multi-head에서 **(B, N, d) → (B, H, N, d_h)** 변환을 설명한다",
           "Self-attention에 **위치 정보**가 필요한 이유를 설명한다"])

d.glossary([["Attention 가중치 α", "각 위치를 얼마나 참고할지 (합 1)", "여러 자료에 나눠 준 신뢰 비중"],
            ["정렬 (alignment)", "출력 위치와 입력 위치의 대응", "번역할 때 짚어 보는 원문 단어"],
            ["Self-attention", "한 시퀀스가 자기 자신의 모든 위치를 참조", "문장이 스스로 앞뒤를 살핌"],
            ["Query (Q)", "비교의 기준이 되는 벡터", "찾고 싶은 것"],
            ["Key (K)", "비교 대상이 되는 벡터", "책의 색인"],
            ["Value (V)", "가중합으로 실제 전달되는 벡터", "책의 내용"],
            ["Head", "독립된 Q·K·V 투영 한 벌", "서로 다른 관점의 독자"],
            ["위치 인코딩 (PE)", "토큰 벡터에 더하는 위치 정보", "좌석 번호표"]])

# ============================================================ Part 1
d.part(1, "Attention: 출력마다 다른 요약", "2014 — 요약본 하나 대신, 원문 전체를 남겨 두고 매번 다시 보면?")

s = d.slide("요약본 하나 vs 원문 다시 보기", lead="Encoder의 위치별 표현 h_1 … h_S를 버리지 않고, 출력 시점마다 다른 가중합 c_t를 만든다",
            stage="아이디어",
            notes="왼쪽(Seq2Seq): 책을 읽고 요약문 하나만 남긴 뒤 그 요약문으로 모든 질문에 답한다. 오른쪽(Attention): 답할 때마다 남겨 둔 원문의 여러 위치를 다른 비중으로 참고한다. "
                  "원자료 주의: 이것은 계산 경로를 이해하기 위한 비유일 뿐, 모델이 사람처럼 책을 이해한다는 증거가 아니다. 실제로 실행되는 것은 정렬 점수 → softmax → 벡터 가중합. "
                  "결국 바뀐 것은 '상태의 개수'(c 하나 → h_1…h_S 전부)와 '접근 규칙'(항상 같은 c → 매번 다른 가중합)이다.")
top, bot = s.area.top(3.75, gap=0.2)
s.image(A("week5/bottleneck.png"), top)
L, R = bot.cols(0.5, gap=0.4)
s.callout("**고정 문맥 벡터**: 책을 읽고 요약문 하나만 남긴 뒤, 그 요약문으로 모든 질문에 답한다", L, kind="tip", size=15)
s.callout("**Attention**: 답할 때마다 남겨 둔 원문의 여러 위치를 **다른 비중**으로 다시 본다 (비유일 뿐 — 실제는 점수 → softmax → 가중합)",
          R, kind="tip", size=15)

s = d.slide("Attention의 세 단계", lead="① 정렬 점수 → ② softmax로 비중 → ③ 값의 가중합", stage="계산",
            notes="Decoder의 현재 상태 s_(t−1)과 Encoder의 각 위치 h_j를 비교해 점수 e를 매긴다(점수 함수 a). softmax로 합이 1인 비중 α를 만들고(2주차), "
                  "h_j들을 α로 가중합해 이번 시점만의 문맥 벡터 c_t를 만든다. "
                  "예: α = (0.1, 0.2, 0.7), 값 v1=(1,0), v2=(0,1), v3=(2,2) → 0.1·(1,0) + 0.2·(0,1) + 0.7·(2,2) = (1.5, 1.6). "
                  "가장 큰 가중치의 토큰 하나를 골라 복사하는 것과 다르다 — soft attention은 대부분 여러 위치를 섞는다.")
top, bot = s.area.top(1.55, gap=0.3)
s.formula(["e[t, j] = a( s[t−1], h[j] )     α[t, j] = softmax_j( e[t, j] )", "c[t] = Σ_j  α[t, j] · h[j]"], top, size=21)
L, R = bot.cols(0.52, gap=0.4)
s.table(["위치 j", "α", "값 v_j", "α · v_j"], [["1", "0.1", "(1, 0)", "(0.1, 0)"], ["2", "0.2", "(0, 1)", "(0, 0.2)"],
                                           ["3", "0.7", "(2, 2)", "(1.4, 1.4)"], ["합", "1.0", "", "**(1.5, 1.6)**"]],
        L, size=15, align="cccc", highlight=[3])
s.bullets(["하나의 c가 아니라 출력마다 **다른 c_t**", "가장 큰 것 하나를 **복사하는 게 아니다**", ("여러 위치를 비중대로 **섞는다** (soft)", 1),
           "점수 함수 a: 작은 신경망, 내적 등 (다음 장)"], R)

s = d.slide("정렬(alignment)을 눈으로", lead="각 출력 단어가 어느 입력 단어에 비중을 두었는지 — 관찰 도구이지 증명은 아니다", stage="검증",
            notes="행은 Decoder 출력 위치, 열은 Encoder 입력 위치, 칸의 값은 α. 어순이 달라도 '고양이가'는 'cat'에, '매트'는 'mat'에 큰 비중을 둔다(설명용 가상 정렬). "
                  "Bahdanau et al.의 논문 그림이 이런 정렬을 보여 주었다. 원자료 주의: heatmap에는 '이 그림이 보여주는 것'과 '증명하지 않는 것'을 함께 적는다. "
                  "큰 α는 '그 위치에 큰 참조 비중이 관찰되었다'는 뜻이지, 그 단어가 예측의 유일한 원인이라는 뜻이 아니다.")
L, R = s.cols(0.58)
s.image(A("week5/alignment.png"), L)
rest = s.card(R, "보여주는 것", ["출력 위치마다 **어느 입력에** 큰 비중을 두었나", "어순이 달라도 대응을 찾는다"], tone="teal",
              bullets=True, fit_h=True)
s.card(Box(rest.x, rest.y, rest.w, rest.h), "증명하지 않는 것", ["그 단어가 예측의 **유일한 원인**이라는 것", "모델이 사람처럼 **이해**했다는 것",
                                                        "→ 관찰과 인과 검증을 구분 (원자료 개념 확인 18)"], tone="accent", bullets=True, fit_h=True)

s = d.slide("점수 함수: 어떻게 비교할까", lead="Bahdanau(2014)는 작은 신경망으로, Luong(2015)은 내적으로 — Transformer는 내적을 택한다", stage="역사",
            notes="Bahdanau, Cho, Bengio(2014) 'Neural Machine Translation by Jointly Learning to Align and Translate': 작은 신경망(additive)으로 점수를 계산. "
                  "Luong, Pham, Manning(2015): 내적(dot), 학습된 행렬을 사이에 둔 bilinear(general) 등 여러 점수 함수 비교. "
                  "내적은 행렬곱 한 번으로 모든 쌍의 점수를 동시에 계산할 수 있어 빠르다(1주차: 행렬곱 = 내적 여러 개). Transformer는 여기에 스케일(√d_h)을 더한다.")
s.table(["점수 함수", "식", "특징", "제안"],
        [["Additive (작은 신경망)", "vᵀ tanh(W s + U h)", "유연하지만 쌍마다 계산", "Bahdanau et al. 2014"],
         ["Dot (내적)", "sᵀ h", "행렬곱 한 번으로 **모든 쌍**", "Luong et al. 2015"],
         ["General (bilinear)", "sᵀ W h", "학습된 W로 비교 공간을 바꿈", "Luong et al. 2015"],
         ["Scaled dot", "qᵀ k / √d_h", "내적 + 크기 보정", "**Transformer 2017**"]],
        Box(s.area.x, s.area.y, s.area.w, 3.0), widths=[2.4, 2.4, 3.6, 2.4], size=16, highlight=[3])
s.callout("1주차 복습: 행렬곱 = 내적 여러 개를 **한 번에** → 모든 (출력, 입력) 쌍의 점수를 행렬곱 하나로.",
          Box(s.area.x, s.area.y + 3.3, s.area.w, 0.9), kind="tip", size=16)

s = d.slide("Attention을 본체로 쓰면?", lead="보조 장치였던 ‘참조 연산’으로 시퀀스의 표현 자체를 만들 수 있을까?", stage="아이디어",
            notes="원자료의 표: RNN의 중심 질문은 '정보를 어떻게 보존·갱신할까', RNN+Attention은 '현재 필요한 정보를 어느 입력 위치에서 가져올까', "
                  "Transformer는 '참조 연산으로 시퀀스의 표현 자체를 만들 수 있을까'. 4주차 표의 ③(순차 계산)까지 해결하려면 순환을 없애야 한다. "
                  "원자료 주의: self-attention은 2017년 전에도 있었다. Transformer는 이 계산을 FFN·잔차·정규화·위치 정보와 조합한 비순환 Encoder–Decoder다. "
                  "제목 'Attention Is All You Need'를 문자 그대로 'Attention 외에는 아무 계산이 없다'로 이해하면 안 된다.")
s.table(["구조", "중심 질문", "남는 문제"],
        [["RNN / LSTM", "정보를 어떻게 **보존·갱신**할까?", "고정 크기 상태 · 순차 계산"],
         ["RNN + Attention (2014)", "현재 필요한 정보를 **어느 입력 위치**에서 가져올까?", "순환은 여전히 순차적"],
         ["Transformer (2017)", "**참조 연산만으로** 시퀀스의 표현 자체를 만들 수 있을까?", "→ 오늘 · 다음 주"]],
        Box(s.area.x, s.area.y, s.area.w, 2.6), widths=[2.6, 5.6, 3.2], size=16, highlight=[2])
s.callout("==주의== self-attention은 2017년 전에도 있었다. Transformer = Attention + FFN + 잔차 + 정규화 + 위치 정보의 **조합**. "
          "‘All You Need’는 ‘다른 계산이 없다’는 뜻이 아니다.", Box(s.area.x, s.area.y + 2.9, s.area.w, 1.2), kind="warn", size=16)

# ============================================================ Part 2
d.part(2, "Self-attention과 Q · K · V", "문장이 자기 자신의 모든 위치를 참조한다면?")

s = d.slide("Self-attention: 문장이 스스로를 참조한다", lead="모든 토큰이 같은 문장의 모든 토큰을 보고, 필요한 정보를 섞어 새 표현을 만든다", stage="아이디어",
            notes="예: '그 동물은 너무 피곤해서 길을 건너지 않았다. 그것은 …'에서 '그것은'의 표현을 만들 때 '동물'을 많이 참고하면 좋다. "
                  "self-attention에서는 각 위치가 Query가 되어 같은 문장의 모든 위치(Key)와 비교하고, 비중대로 Value를 섞는다. "
                  "RNN에서는 먼 두 토큰이 만나려면 N단계를 거쳐야 했지만, self-attention은 한 층에서 직접 만난다(경로 길이 1). 그리고 모든 위치를 동시에 계산할 수 있다(순차 의존 없음).")
rest = s.cards([{"head": "예시", "tone": "plain", "body": ["“그 **동물**은 너무 피곤해서 길을 건너지 않았다. **그것**은 …”",
                                                         "‘그것’의 표현을 만들 때 ‘동물’을 많이 참고하면 좋다"]},
                {"head": "RNN", "body": ["먼 두 토큰이 만나려면 **N단계**를 거친다", "h_t는 h_(t−1)이 필요 → **순차**"]},
                {"head": "Self-attention", "tone": "accent", "body": ["한 층에서 **직접** 만난다 (경로 1)", "모든 위치를 **동시에** 계산"]}],
               cols=3, body_size=16, head_size=18)
s.callout("질문: 같은 입력 X에서 ‘비교할 기준’과 ‘가져올 내용’을 어떻게 만들까? → **Q · K · V**",
          Box(rest.x, rest.y + 0.1, rest.w, 0.9), kind="key", size=17)

s = d.slide("Q · K · V의 역할과 비유의 한계", lead="Query는 비교의 기준, Key는 비교 대상, Value는 실제로 전달될 내용", stage="아이디어",
            notes="도서관 비유: Query는 찾고 싶은 것, Key는 책의 색인, Value는 책의 내용. 색인과 잘 맞는 책일수록 그 내용을 많이 가져온다. "
                  "원자료가 강조하는 비유의 한계: Query는 사용자가 입력한 자연어 질문이 아니다(이미지 Encoder에도 Q가 있다). Key는 문자열이나 데이터베이스 키가 아니다. "
                  "Value는 원래 임베딩을 그대로 복사한 것이 아니다. 모두 학습된 투영으로 만든 벡터이며, 'Query가 중요한 토큰을 찾는다'고만 말하면 목적 함수와 중요도를 혼동한다.")
s.table(["", "계산에서의 역할", "도서관 비유", "비유의 한계"],
        [["**Query (Q)**", "현재 위치가 Key들과 비교할 벡터", "찾고 싶은 것", "사용자가 입력한 **질문이 아니다** — 이미지 모델에도 있다"],
         ["**Key (K)**", "각 위치를 비교하기 위한 벡터", "책의 색인", "단어 문자열이나 DB key가 **아니다**"],
         ["**Value (V)**", "가중합으로 실제 결합될 벡터", "책의 내용", "원래 임베딩을 그대로 **복사하지 않는다**"]],
        Box(s.area.x, s.area.y, s.area.w, 2.9), widths=[1.4, 3.2, 1.8, 4.6], size=16)
s.callout("모두 **학습된 투영**으로 만든 벡터다. ‘중요도’라는 말은 어떤 기준의 중요도인지 정한 뒤에 쓴다 — 실제로는 loss를 줄이도록 학습된 내적 점수일 뿐.",
          Box(s.area.x, s.area.y + 3.2, s.area.w, 1.1), kind="warn", size=16)

s = d.slide("학습되는 것은 투영 행렬", lead="Q = X W_Q,  K = X W_K,  V = X W_V — 같은 X에서 세 가지 다른 벡터", stage="계산",
            notes="한 head에서 X가 (N, d), W_Q와 W_K가 (d, d_h)라면 Q, K는 (N, d_h). V의 차원 d_v는 d_h와 달라도 되지만 원형과 이 과정에서는 같게 둔다. 편향은 생략. "
                  "학습되는 파라미터는 W_Q, W_K, W_V(그리고 뒤의 W_O)뿐이다. Q, K, V 자체는 입력마다 새로 계산되는 활성값이다. "
                  "2주차의 선형층과 같다 — 차이는 이 결과를 '비교'와 '전달'에 쓴다는 것.")
L, R = s.cols(0.55)
s.image(A("week5/qkv_proj.png"), L)
s.formula(["Q = X · W_Q", "K = X · W_K", "V = X · W_V"], Box(R.x, R.y, R.w, 1.7), size=22)
s.bullets(["X: (N, d) · W: (d, d_h) → (N, d_h)", "**W_Q, W_K, W_V**: 학습되는 파라미터", "**Q, K, V**: 입력마다 계산되는 활성값",
           "2주차 선형층과 같은 계산"], Box(R.x, R.y + 1.95, R.w, R.h - 1.95), size=16)

s = d.slide("Self-attention이라고 Q = K = V는 아니다", lead="원본 X가 같아도 투영이 다르면 값이 다르다 — ‘A가 B를 보는 비중’ ≠ ‘B가 A를 보는 비중’", stage="검증",
            notes="W_Q, W_K, W_V가 다르므로 같은 X에서 나온 Q, K, V는 일반적으로 다르다. 그래서 점수 행렬 QKᵀ도 대칭이 아니다: 'A가 B를 보는 점수' q_A·k_B와 'B가 A를 보는 점수' q_B·k_A는 다르다. "
                  "설령 Q=K여서 점수가 대칭이어도, 행마다 정규화하는 softmax 이후에는 일반적으로 대칭이 아니다. "
                  "왜 점수용(Q, K)과 내용용(V)을 나눌까? 어떤 특징으로 다른 토큰을 찾을지와, 그 토큰에서 어떤 정보를 전달할지를 따로 학습하는 자유를 준다. "
                  "이것은 설계 선택이지, 각 축이 미리 '주어', '동사' 같은 의미를 갖는다는 뜻이 아니다.")
rest = s.cards([{"head": "Q ≠ K ≠ V", "body": ["같은 X, 다른 W_Q · W_K · W_V", "→ 값이 일반적으로 **다르다**"]},
                {"head": "점수는 비대칭", "body": ["q_A · k_B ≠ q_B · k_A", "‘A가 B를 봄’ ≠ ‘B가 A를 봄’", "softmax 후에도 비대칭"]},
                {"head": "왜 나누나?", "tone": "accent", "body": ["**찾는 기준**(Q·K)과 **가져올 내용**(V)을 따로 학습",
                                                                 "축마다 미리 정해진 의미는 **없다**"]}],
               cols=3, body_size=16, head_size=18)
s.callout("원자료 개념 확인 04: Self-attention의 Q, K, V는 같은 원본에서 **서로 다른 투영**으로 만들 수 있다.",
          Box(rest.x, rest.y + 0.1, rest.w, 0.8), kind="tip", size=16)

s = d.slide("파라미터 vs 활성값", lead="정적인 파라미터로 동적인 정보 결합을 계산한다 — Attention 가중치 A는 학습 표가 아니다", stage="정리",
            notes="W_Q, W_K, W_V, W_O는 학습 후 고정되는 파라미터로 모든 입력에 공유된다. Q, K, V와 attention 가중치 A = softmax(QKᵀ/√d_h)는 입력마다 새로 계산되는 활성값이다. "
                  "추론할 때 가중치가 고정되어 있어도 A는 문장마다 다르다. A는 gradient 경로에 포함되지만 '학습된 attention 표'가 따로 저장되어 있는 것이 아니다. "
                  "1주차 오개념 'Attention 가중치는 파라미터다'가 틀린 이유.")
s.table(["", "예", "입력마다 바뀌나?", "optimizer가 갱신하나?"],
        [["파라미터", "W_Q, W_K, W_V, W_O", "아니오 — 모든 입력에 **공유**", "**예**"],
         ["활성값", "Q, K, V", "**예** — 입력·이전 층에 따라 계산", "아니오"],
         ["Attention 가중치", "A = softmax(QKᵀ / √d_h)", "**예** — 문장마다 다르다", "아니오 (gradient 경로에는 포함)"]],
        Box(s.area.x, s.area.y, s.area.w, 2.5), widths=[2.0, 3.0, 3.4, 3.0], size=16)
s.callout("추론 때 모델 가중치는 고정되어 있어도 **A는 입력마다 다르다** → ‘정적인 파라미터로 동적인 결합’",
          Box(s.area.x, s.area.y + 2.8, s.area.w, 0.9), kind="key", size=17)

# ============================================================ Part 3
d.part(3, "Scaled dot-product를 숫자로", "공식은 한 줄 — 점수, 스케일, mask, 확률, 가중합의 다섯 단계로 나눠 읽는다")

s = d.slide("공식을 다섯 단계로", lead="Attention(Q, K, V) = softmax(QKᵀ / √d_h + M) V", stage="계산",
            notes="① 점수: QKᵀ — 모든 Query와 모든 Key의 내적 (N, N). ② 스케일: √d_h로 나눈다. ③ mask M: 보면 안 되는 칸에 −∞를 더한다(6주차 자세히, 오늘은 선택 사항). "
                  "④ softmax: 행마다(=Query마다) Key 축으로 정규화 → 각 행의 합 1. ⑤ 가중합: A V — 각 Query의 출력은 Value들의 가중합 (N, d_h). "
                  "원자료: 행은 Query, 열은 Key. 유효한 Key가 있고 dropout 전이면 각 행의 합은 1.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("Attention(Q, K, V) = softmax( Q Kᵀ / √d_h + M ) · V", top, size=24)
mid, low = bot.top(1.9, gap=0.3)
s.flow([{"head": "① 점수", "body": "Q Kᵀ\n(N, N)"}, {"head": "② 스케일", "body": "÷ √d_h"},
        {"head": "③ mask", "body": "+ M (−∞)\n6주차"}, {"head": "④ softmax", "body": "행마다 Key 축\n합 = 1", "tone": "accent"},
        {"head": "⑤ 가중합", "body": "A V\n(N, d_h)", "tone": "dark"}], mid, body_size=14, head_size=16, gap=0.35)
s.bullets(["**행 = Query**, **열 = Key** — softmax는 **Key 축**(원자료 개념 확인 06)",
           "shape: Q (N, d_h) · Kᵀ (d_h, N) → **(N, N)** → A V → **(N, d_h)**"], low, size=17)

s = d.slide("4토큰 예제: 설정", lead="토큰 A · B · C · D, 특징 2개 — 숫자는 설명용이며 학습 결과가 아니다", stage="계산",
            notes="원자료 시뮬레이터의 예제. Q, K, V는 이미 투영이 끝난 값이라고 하자. d_h = 2이므로 스케일은 √2. "
                  "A·B·C·D는 실제 의미가 없는 예시 토큰. K와 V를 고정하고 Query 하나씩 계산해 본다. 다음 장에서 Query A의 행을 손으로 계산한다.")
L, R = s.cols(0.62)
s.image(A("week5/attn_setup.png"), L)
s.table(["토큰", "q", "k", "v"], [["A", "(1, 0)", "(1, 0)", "(1, 0)"], ["B", "(0, 1)", "(0, 1)", "(0, 1)"],
                                 ["C", "(1, 1)", "(1, 1)", "(2, 2)"], ["D", "(−1, 0.5)", "(−1, 1)", "(−1, 1)"]],
        Box(R.x, R.y, R.w, 2.4), size=15, align="cccc")
s.bullets(["d_h = 2 → 스케일 **√2**", "먼저 **Query A**의 행 하나를 손으로"], Box(R.x, R.y + 2.65, R.w, R.h - 2.65), size=16)

s = d.slide("Query A를 손으로 계산", lead="점수 → ÷√2 → exp → 합으로 나누기 → Value 가중합", stage="계산",
            notes="q_A = (1, 0). 점수: k_A와 1, k_B와 0, k_C와 1, k_D와 −1. ÷√2: 0.707, 0, 0.707, −0.707. "
                  "exp: 2.028, 1.000, 2.028, 0.493, 합 5.549. softmax: 0.365, 0.180, 0.365, 0.089 (합 1). "
                  "출력 = 0.365·(1,0) + 0.180·(0,1) + 0.365·(2,2) + 0.089·(−1,1) = (1.008, 1.000). "
                  "A와 C에 같은 비중(둘 다 q_A와의 내적 1), D는 반대 방향이라 가장 작은 비중.")
s.takeaway("o_A = 0.365·v_A + 0.180·v_B + 0.365·v_C + 0.089·v_D = (1.008, 1.000)")
s.table(["Key", "q_A · k", "÷ √2", "exp", "softmax α", "α · v"],
        [["A (1, 0)", "1", "0.707", "2.028", "**0.365**", "(0.365, 0)"], ["B (0, 1)", "0", "0", "1.000", "**0.180**", "(0, 0.180)"],
         ["C (1, 1)", "1", "0.707", "2.028", "**0.365**", "(0.731, 0.731)"], ["D (−1, 1)", "−1", "−0.707", "0.493", "**0.089**", "(−0.089, 0.089)"],
         ["합", "", "", "5.549", "1.000", "**(1.008, 1.000)**"]], widths=[1.6, 1.3, 1.2, 1.2, 1.6, 2.2], size=16, align="cccccc",
        highlight=[4])

s = d.slide("전체 행렬로: 점수 → A → O", lead="나머지 Query도 같은 규칙 — 네 행을 행렬곱 한 번에", stage="계산",
            notes="왼쪽: 점수 QKᵀ/√2 (4×4). 가운데: 행별 softmax A — 각 행의 합 1. 오른쪽: O = AV (4×2). 첫 행이 방금 손으로 계산한 Query A. "
                  "Query D는 자기 자신 D와 B에 큰 비중(0.524, 0.259). "
                  "Think before: Q와 K를 고정하고 V만 바꾸면 A는? 그대로(Q, K, mask만으로 결정). O는? 바뀐다. 단, 전체 self-attention에서 X를 바꾸면 Q, K, V가 함께 바뀐다.")
top, bot = s.area.top(3.4, gap=0.25)
s.image(A("week5/attn_pipeline.png"), top)
s.bullets(["각 행의 합 = 1 (softmax는 행마다), 첫 행 = 방금 손으로 계산한 Query A",
           "생각해 보기: Q·K를 고정하고 **V만** 바꾸면 A는? O는? (답: A 그대로, O는 바뀐다)"], bot, size=16)

s = d.slide("왜 √d_h로 나눌까", lead="성분이 독립이고 분산 1이면 내적의 분산은 d_h — 차원이 크면 점수가 커져 softmax가 뾰족해진다",
            stage="아이디어",
            notes="단순화한 가정: q, k의 성분이 서로 독립이고 평균 0, 분산 1. 그러면 q·k = Σ q_r k_r의 분산은 d_h, 표준편차는 √d_h. "
                  "d_h = 4면 2, 64면 8, 256이면 16 — 점수 차이가 커져 softmax가 거의 한 칸에 몰린다(2주차 temperature가 아주 작은 경우와 비슷). 그러면 기울기도 작아진다. "
                  "√d_h로 나누면 표준편차가 다시 1 근처. 원자료 주의: 실제 학습된 Q, K가 이 가정을 항상 만족한다는 주장은 아니다. 또 이 스케일은 생성 때의 temperature와 위치·목적이 다르다.")
L, R = s.cols(0.6)
s.image(A("week5/sqrt_scale.png"), L)
s.table(["d_h", "q·k 표준편차", "÷ √d_h 후"], [["4", "≈ 2", "≈ 1"], ["16", "≈ 4", "≈ 1"], ["64", "≈ 8", "≈ 1"], ["256", "≈ 16", "≈ 1"]],
        Box(R.x, R.y, R.w, 2.2), size=15, align="ccc")
s.bullets(["스케일 없으면 softmax가 **한 칸에 몰림**", ("→ 기울기도 작아진다", 1), "==주의== 단순화한 가정 — 항상 성립하진 않는다",
           "생성 때 **temperature**와는 목적이 다르다"], Box(R.x, R.y + 2.45, R.w, R.h - 2.45), size=15)

s = d.slide("가중치를 해석할 때와 경계 조건", lead="큰 α ≠ 큰 영향 · 모든 Key가 막히면 softmax가 정의되지 않는다", stage="검증",
            notes="α_j가 크면 V_j의 기여 비중이 커지지만, V의 크기와 방향이 다르고 뒤에는 W_O, residual, FFN, 다음 층이 있다. 가중치 숫자 하나로 최종 출력 변화를 다 알 수 없다. "
                  "경계 조건: 어떤 행의 모든 Key가 mask로 가려지면 softmax의 확률 분포가 정의되지 않아 구현에 따라 NaN이나 0이 된다 → 유효한 Query에는 허용된 Key가 적어도 하나 있도록 설계. "
                  "attention dropout 뒤에는 개별 행의 합이 1이 아닐 수 있다.")
s.cards([{"head": "해석할 때", "bullets": True, "body": ["α가 커도 **V의 크기·방향**이 다르다", "뒤에 W_O · residual · FFN · 다음 층이 있다",
                                                       "heatmap은 **관찰 도구** — 인과는 따로 검증"]},
         {"head": "경계 조건", "tone": "accent", "bullets": True,
          "body": ["모든 Key가 가려진 행 → softmax **정의 안 됨** (NaN 등)", "→ 유효한 Query엔 허용된 Key를 **최소 하나**",
                   "attention dropout 뒤엔 행 합이 1이 아닐 수 있다"]}], cols=2, body_size=17, head_size=19)
s.area = Box(s.area.x, s.area.y + 2.75, s.area.w, s.area.h - 2.75)
s.callout("원자료 개념 확인 18: 큰 attention 가중치를 봤다면 — ‘그 위치에 큰 참조 비중이 **관찰**되었다’고 말하고, "
          "인과 해석은 **추가 검증**한다 (예: 그 위치를 가리거나 바꿔 출력 변화를 측정).",
          Box(s.area.x, s.area.y, s.area.w, 1.2), kind="key", size=16)

# ============================================================ Part 4
d.part(4, "Multi-head와 tensor shape", "한 번의 softmax는 한 가지 비교 방식 — 여러 관점으로 동시에 보려면?")

s = d.slide("여러 비교 · 전달 경로 만들기", lead="d차원을 H개 부분공간으로 나눠 각 head가 독립적으로 attention — 결과를 이어 붙여 W_O로 섞는다",
            stage="아이디어",
            notes="하나의 attention은 행마다 하나의 분포(한 가지 비교 방식)만 만든다. Multi-head는 서로 다른 투영 H벌로 H개의 attention을 병렬로 수행한다. "
                  "head_i = Attention(X W_Q^i, X W_K^i, X W_V^i), 출력 = Concat(head_1 … head_H) W_O. "
                  "원자료 주의: 각 head는 모든 토큰 위치를 처리한다. head 1에 앞쪽 토큰, head 2에 뒤쪽 토큰을 나누는 것이 아니다. 나누는 것은 '특징 차원'이다. "
                  "그림: 같은 X, 다른 투영 → 서로 다른 참조 패턴(무작위 가중치 예시 — 역할 지정 아님).")
top, bot = s.area.top(1.5, gap=0.3)
s.formula(["head_i = Attention( X W_Q^i, X W_K^i, X W_V^i )", "MultiHead(X) = Concat( head_1, …, head_H ) · W_O"], top, size=21)
L, R = bot.cols(0.6, gap=0.35)
s.image(A("week5/heads.png"), L)
s.bullets(["각 head는 **모든 토큰**을 본다", ("토큰을 나누는 게 아니라 **특징 차원**을 나눈다", 1), "d_h = d / H",
           "W_O: 여러 head의 결과를 **섞는** 투영", "그림은 무작위 가중치 예시 — 역할 지정 아님"], R, size=16)

s = d.slide("d = 8, H = 2, N = 5를 따라가기", lead="(B, N, d) → 투영 → (B, N, H, d_h) → 축 교환 → (B, H, N, d_h)", stage="계산",
            notes="구현에서는 H개의 투영을 하나의 큰 (d, d) 행렬로 묶어 한 번에 계산하고, 결과를 head 축으로 쪼갠다(view) 뒤 축을 바꾼다(transpose). "
                  "B=2, N=5, d=8, H=2, d_h=4: X (2,5,8) → Q (2,5,8) → view (2,5,2,4) → transpose (2,2,5,4). 점수 QKᵀ: (2,2,5,4)@(2,2,4,5) → (2,2,5,5). "
                  "A V → (2,2,5,4) → transpose + reshape → (2,5,8) → W_O → (2,5,8). 입력과 출력 shape이 같아서 층을 쌓을 수 있다. "
                  "개념 확인 05: Q (B,H,T,d_h), K (B,H,S,d_h)이면 QKᵀ는 (B,H,T,S) — d_h는 내적하며 사라진다.")
top, bot = s.area.top(2.45, gap=0.2)
s.image(A("week5/mha_shapes.png"), top)
s.table(["단계", "연산", "shape", "의미"],
        [["입력", "X", "(2, 5, 8)", "문장 2개 · 토큰 5개 · 특징 8개"], ["투영", "X W_Q (d × d)", "(2, 5, 8)", "모든 head의 Q를 한 번에"],
         ["head 분리", "view → transpose", "(2, 2, 5, 4)", "배치 · head · 토큰 · 특징"], ["점수", "Q Kᵀ / √4", "(2, 2, 5, 5)", "head별 위치 관계"],
         ["가중합", "A V", "(2, 2, 5, 4)", "head별 새 표현"], ["결합 · 투영", "concat → W_O", "(2, 5, 8)", "입력과 같은 shape → 쌓을 수 있다"]],
        bot, widths=[1.5, 2.4, 1.7, 4.2], size=13)

s = d.slide("PyTorch로 직접 구현", lead="투영 한 번 → head 축 만들기 → scaled dot-product → 합치기", stage="코드",
            notes="직접 구현한 multi-head self-attention. view(B, N, H, d_h).transpose(1, 2)가 핵심 shape 조작이다. softmax의 dim=-1은 Key 축. "
                  "nn.MultiheadAttention(8, 2)의 파라미터는 4 × (8×8 + 8) = 288. 출력 (2, 5, 8), head별 가중치 (2, 2, 5, 5). "
                  "실습: 직접 구현한 결과와 F.scaled_dot_product_attention의 결과가 같은지 확인해 보기.")
L, R = s.cols(0.62)
s.code("import torch, torch.nn as nn\n"
       "B, N, d, H = 2, 5, 8, 2;  dh = d // H\n"
       "X = torch.randn(B, N, d)\n"
       "Wq, Wk, Wv, Wo = (nn.Linear(d, d) for _ in range(4))\n\n"
       "def split(t):  # (B,N,d) -> (B,H,N,dh)\n"
       "    return t.view(B, N, H, dh).transpose(1, 2)\n"
       "Q, K, V = split(Wq(X)), split(Wk(X)), split(Wv(X))\n"
       "S = Q @ K.transpose(-2, -1) / dh ** 0.5   # (2,2,5,5)\n"
       "A = S.softmax(dim=-1)                     # Key 축\n"
       "O = (A @ V).transpose(1, 2).reshape(B, N, d)\n"
       "print(Wo(O).shape)                        # (2, 5, 8)", L, size=12.5)
s.bullets(["`view + transpose`: head 축 만들기", "`softmax(dim=-1)`: **Key 축**", "출력 shape = 입력 shape",
           "`nn.MultiheadAttention(8, 2)`", ("파라미터 4 × (8·8 + 8) = **288**", 1)], R)

s = d.slide("Head를 늘리면 무엇이 달라지나", lead="d를 고정하고 d_h = d/H면 파라미터와 주요 연산량은 그대로 — head당 차원이 줄고 점수 표는 늘어난다",
            stage="검증",
            notes="W_Q, W_K, W_V, W_O의 주요 파라미터는 약 4d²로 H와 무관(d=512면 약 105만). attention 곱셈량 H·N²·d_h = N²d도 그대로. "
                  "반면 명시적으로 저장하는 attention 표의 원소 수는 H·N²라 head 수에 비례해 늘 수 있다. head당 차원은 512/8 = 64로 줄어든다. "
                  "원자료 주의: 어떤 head에서 특정 패턴이 관찰될 수는 있지만 '1번은 문법, 2번은 의미' 같은 역할이 구조에 지정되어 있지 않다. 관찰 · 해석 · 인과 검증을 구분해 보고한다. "
                  "개념 확인 10: 같은 d에서 H를 늘리면 주요 투영 파라미터는 유지되고 head당 차원은 줄어든다.")
s.table(["d를 고정하고 H를 늘리면", "변화"], [["투영 파라미터 (≈ 4d²)", "**그대로** (d = 512 → 약 105만)"],
                                          ["attention 곱셈량 (H · N² · d_h = N² d)", "**그대로**"],
                                          ["head당 차원 d_h = d / H", "**줄어든다** (512 / 8 = 64)"],
                                          ["저장하는 점수 표 (H · N²)", "**늘어난다**"]],
        Box(s.area.x, s.area.y, s.area.w, 2.4), widths=[5, 5], size=16, align="lc")
s.callout("head의 역할은 **미리 정해지지 않는다** — ‘1번은 문법, 2번은 의미’는 구조가 아니라 사후 관찰이다. "
          "관찰 · 해석 · 인과 검증을 구분해서 보고한다.", Box(s.area.x, s.area.y + 2.7, s.area.w, 1.1), kind="warn", size=16)

# ============================================================ Part 5
d.part(5, "순서 정보: 위치 인코딩", "Self-attention은 “개가 사람을 물었다”와 “사람이 개를 물었다”를 구분할까?")

s = d.slide("Self-attention은 순서를 모른다", lead="입력 순서를 섞으면 출력도 똑같이 섞일 뿐 — 순열 등변성", stage="문제",
            notes="위치 정보나 위치 의존 mask가 없는 self-attention에 입력 순열 P를 적용하면 Q′=PQ, K′=PK, V′=PV이고, 행 단위 softmax는 행·열이 같이 움직이므로 SA(PX) = P·SA(X). "
                  "입력을 섞으면 출력도 같은 방식으로 섞인다(등변성). 출력이 변하지 않는다는 불변성과 다르다(3주차 CNN의 등변성/불변성 구분과 같은 논리). "
                  "즉 각 토큰의 출력은 '어떤 토큰들이 있는가'만 보고 '어떤 순서인가'는 모른다 — 순서를 따로 알려 줘야 한다. "
                  "원자료 주의: causal mask가 있으면 방향 정보가 생기므로 이 증명을 그대로 적용할 수 없다. 개념 확인 13.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("SA(P X) = P · SA(X)        (P: 순서를 섞는 순열)", top, size=24)
rest = s.cards([{"head": "무슨 뜻인가", "tone": "accent", "bullets": True,
                 "body": ["순서를 섞으면 출력도 **똑같이 섞일 뿐**", "각 토큰의 출력은 ‘어떤 토큰들이 있나’만 반영",
                          "“개가 사람을 물었다” vs “사람이 개를 물었다” → **구분 불가**"]},
                {"head": "구분할 것", "tone": "plain", "bullets": True,
                 "body": ["**등변성**: 섞으면 같이 섞임 (이것)", "**불변성**: 섞어도 그대로", "3주차 CNN의 이동 등변성과 같은 논리",
                          "causal mask가 있으면 이 증명이 그대로 적용되지 않는다"]}], bot, cols=2, body_size=16, head_size=18)
s.callout("그래서 순서를 **따로 알려 줘야** 한다 → 위치 인코딩", Box(rest.x, rest.y, rest.w, 0.8), kind="key", size=17)

s = d.slide("임베딩에 위치를 더한다", lead="x = E[id] · √d + PE[pos] — shape은 그대로, 같은 차원에 위치 단서가 섞인다", stage="아이디어",
            notes="원형 Transformer는 임베딩에 √d를 곱하고 같은 차원(d)의 위치 벡터를 더한다. Encoder와 Decoder 모두. "
                  "입력 ID (B, S) → 임베딩 (B, S, d) → + PE (S, d) → (B, S, d) (broadcasting, 1주차). "
                  "원자료 주의: 더한다고 해서 토큰 내용과 위치가 완벽히 분리되어 저장된다는 뜻은 아니다. 같은 차원에 결합될 뿐이다.")
top, bot = s.area.top(1.95, gap=0.3)
s.flow([{"head": "ID", "body": "(B, S)"}, {"head": "임베딩 × √d", "body": "(B, S, d)"}, {"head": "+ 위치 벡터 PE", "body": "(S, d) → broadcasting", "tone": "accent"},
        {"head": "블록 입력", "body": "(B, S, d)", "tone": "dark"}], top, body_size=15, head_size=17)
s.bullets(["Encoder와 Decoder **모두** 이 과정을 거친다", "더해도 **shape은 그대로** (1주차 broadcasting)",
           "==주의== 내용과 위치가 **분리 저장**되는 것은 아니다 — 같은 차원에 섞인다", "그럼 PE는 어떤 벡터로? → 다음 장"], bot)

s = d.slide("Sinusoidal 위치 인코딩", lead="차원 쌍마다 다른 주파수의 sin/cos — 앞쪽 차원은 빠르게, 뒤쪽은 느리게 변한다", stage="계산",
            notes="PE(pos, 2i) = sin(pos / 10000^(2i/d)), PE(pos, 2i+1) = cos(pos / 10000^(2i/d)). i가 커질수록 주파수가 낮아져 천천히 변한다 — 시계의 초침·분침·시침처럼 여러 속도의 바늘로 위치를 표현. "
                  "d = 8, pos = 1: (sin 1, cos 1, sin 0.1, cos 0.1, …) = (0.841, 0.540, 0.100, 0.995, …). pos = 2: (0.909, −0.416, …). "
                  "왼쪽 heatmap: 위치(세로) × 차원(가로), 오른쪽: 몇 개 차원의 곡선.")
top, bot = s.area.top(1.5, gap=0.25)
s.formula(["PE(pos, 2i)   = sin( pos / 10000^(2i/d) )", "PE(pos, 2i+1) = cos( pos / 10000^(2i/d) )"], top, size=21)
L, R = bot.cols(0.62, gap=0.35)
s.image(A("week5/pe.png"), L)
s.table(["d = 8", "차원 0", "차원 1", "차원 2", "차원 3"], [["pos 1", "0.841", "0.540", "0.100", "0.995"],
                                                     ["pos 2", "0.909", "−0.416", "0.199", "0.980"]], Box(R.x, R.y, R.w, 1.3), size=13, align="ccccc")
s.bullets(["i가 클수록 **느리게** 변한다", ("시계의 초침 · 분침 · 시침", 1), "학습 파라미터 **없음**"], Box(R.x, R.y + 1.5, R.w, R.h - 1.5), size=15)

s = d.slide("“sin/cos가 정답”은 아니다", lead="위치 단서가 필요하다는 것과 특정 함수가 필수라는 것은 다른 주장", stage="역사",
            notes="원논문도 학습형 위치 임베딩과 비교했고 비슷한 결과를 보고했다. 이후 상대 위치 방식, RoPE(회전 위치 임베딩, 2021), ALiBi(2021) 등 다양한 방식이 쓰인다(후속 변형). "
                  "원자료 주의: 고정 함수가 더 긴 길이의 값을 계산할 수 있다고 해서, 학습보다 긴 길이에 잘 일반화한다는 보장은 없다. "
                  "공정한 실험: 먼저 dropout을 끈 순수 self-attention 모듈에 순열을 적용해 등변성을 확인하고, 전체 모델에서는 source와 target 위치 정보를 따로 제거한 조건을 비교한다.")
s.table(["방식", "아이디어", "예"], [["고정 sinusoidal", "주파수가 다른 sin/cos를 더한다", "원형 Transformer (2017)"],
                                    ["학습형 절대 위치", "위치마다 학습되는 벡터를 더한다", "원논문의 비교 실험, BERT · GPT"],
                                    ["상대 위치", "두 토큰의 **거리**를 점수에 반영", "Shaw et al. (2018) 등"],
                                    ["회전 · 편향 방식", "Q · K를 위치만큼 회전 / 거리 비례 편향", "RoPE (2021), ALiBi (2021)"]],
        Box(s.area.x, s.area.y, s.area.w, 2.7), widths=[2.4, 4.8, 3.6], size=15)
s.callout("==주의== 긴 길이의 값을 **계산할 수 있다** ≠ 긴 길이에 **일반화한다**. 위치 정보 제거 실험은 source · target을 따로 통제한다.",
          Box(s.area.x, s.area.y + 3.0, s.area.w, 1.0), kind="warn", size=16)

# ============================================================ Part 6
d.part(6, "모아 보기: 2017 Transformer의 윤곽", "오늘 배운 부품이 전체 그림의 어디에 있을까?")

s = d.slide("2017 Transformer: 오늘 배운 곳", lead="Encoder 6층 + Decoder 6층 — 오늘은 입력과 attention, 다음 주는 나머지 전부", stage="정리",
            notes="Vaswani et al.(2017). 원형은 Encoder 6층 + Decoder 6층. 각 층은 같은 설계를 반복하지만 파라미터는 층마다 별개('같은 층'이 가중치 공유를 뜻하지 않는다). "
                  "오늘 배운 것: 토큰 임베딩 + 위치 인코딩, (multi-head) self-attention, cross-attention의 개념. "
                  "다음 주: FFN, residual + LayerNorm, masked self-attention, 출력 head, 학습과 생성. base 설정: d = 512, H = 8, d_h = 64, d_ff = 2048.")
L, R = s.cols(0.5)
s.image(A("week5/transformer_arch.png"), L)
rest = s.card(R, "오늘 배운 것 ✔", ["Token Embedding + **위치 인코딩**", "**Multi-head self-attention**", "Cross-attention의 개념 (다음 장)"],
              tone="teal", bullets=True, fit_h=True)
rest = s.card(rest, "다음 주", ["FFN · **Residual + LayerNorm**", "**Masked** self-attention · teacher forcing", "출력 head · 학습 · 생성 · KV cache"],
              tone="accent", bullets=True, fit_h=True)
s.bullets(["base: d = 512, H = 8, d_h = 64, d_ff = 2048", "층마다 파라미터는 **별개**"], rest, size=15)

s = d.slide("세 종류의 Attention", lead="Q를 어디서 만들고 K · V를 어디서 가져오는가 — 그리고 어디까지 볼 수 있는가", stage="정리",
            notes="원자료의 표. Encoder self-attention: Q, K, V 모두 Encoder 입력 표현에서, 유효한 입력 토큰 전체를 본다. "
                  "Decoder masked self-attention: Decoder 입력에서, 현재 위치와 이전 위치만(다음 주 mask). Cross-attention: Q는 Decoder, K·V는 Encoder 최종 출력에서, 유효한 source 전체. "
                  "Self/Cross는 Q와 K·V의 '출처' 차이, Causal/Bidirectional은 '참조 허용 범위' 차이 — 서로 다른 분류 축이다. "
                  "Cross-attention 점수 표는 T×S, 출력 길이는 Query 수 T (개념 확인 09: Q 길이 3, K/V 길이 5 → 출력 길이 3).")
s.table(["종류", "Q의 출처", "K · V의 출처", "볼 수 있는 범위", "점수 표"],
        [["Encoder self-attention", "Encoder 입력 표현", "같은 표현", "유효한 입력 토큰 **전체**", "S × S"],
         ["Decoder masked self-attention", "Decoder 입력 표현", "같은 표현", "현재 위치와 **이전** 위치만", "T × T"],
         ["Cross-attention", "**Decoder** 표현", "**Encoder** 최종 출력", "유효한 source 전체", "**T × S**"]],
        Box(s.area.x, s.area.y, s.area.w, 2.6), widths=[2.9, 2.2, 2.2, 3.0, 1.2], size=15)
s.callout("Self / Cross = **출처**의 차이, Causal / 양방향 = **범위**의 차이 — 서로 다른 축. "
          "Cross-attention의 출력 길이는 **Query 수 T** (source 길이 S가 아니다).", Box(s.area.x, s.area.y + 2.9, s.area.w, 1.1), kind="key", size=16)

# ============================================================ 마무리
d.summary(["Attention = **점수 → softmax → 가중합**: 출력마다 다른 요약 c_t (2014)",
           "Self-attention: 모든 위치가 직접 만난다 — **경로 1**, 순차 의존 없음",
           "Q · K · V는 같은 X의 **다른 투영**, 학습되는 것은 W_Q · W_K · W_V · W_O (A는 활성값)",
           "softmax(QKᵀ/√d_h)V: (N, d_h)·(d_h, N) → **(N, N)** → **(N, d_h)**, softmax는 Key 축",
           "Multi-head: (B, N, d) → **(B, H, N, d_h)** → 다시 (B, N, d), 역할은 미리 정해지지 않는다",
           "Self-attention은 순서를 모른다(**등변**) → **위치 인코딩**을 더한다"])

d.quiz("셀프 체크 ①", [("Self-attention의 Q, K, V는 항상 같은 숫자인가? (개념 확인 04)", "아니다. 같은 X에서 서로 다른 투영 W_Q, W_K, W_V로 만들어 일반적으로 다르다"),
                     ("Q: (B, H, T, d_h), K: (B, H, S, d_h)일 때 QKᵀ의 shape은? (05)", "(B, H, T, S) — d_h는 내적하며 사라진다"),
                     ("Attention의 softmax는 보통 어느 축인가? (06)", "각 Query에 대한 Key 축 — Query마다 Key들에 비중을 나눈다"),
                     ("Q 길이 3, K/V 길이 5인 cross-attention의 출력 길이는? (09)", "3 — 출력은 Query 하나당 한 벡터")])

d.quiz("셀프 체크 ②", [("같은 d에서 head 수 H를 늘리면? (10)", "주요 투영 파라미터는 유지, head당 차원 d_h = d/H는 줄고 점수 표 수는 늘 수 있다"),
                     ("위치 정보와 위치 의존 mask가 없는 self-attention의 순열 성질은? (13)", "순열 등변성: SA(PX) = P·SA(X) — 출력도 같은 순열로 섞인다"),
                     ("어떤 head에서 큰 attention 가중치를 관찰했다. 무엇이라고 말할 수 있나? (18)", "그 위치에 큰 참조 비중이 관찰되었다고 말하고, 인과 해석은 추가 검증한다"),
                     ("q_A = (1, 0)이고 모든 Key가 k = (0, 1)이면 attention 가중치는?", "모든 점수가 0 → softmax가 균등 → 모든 Key에 같은 비중 (1/N)")])

d.misconceptions([["“Attention 가중치는 학습되는 파라미터다”", "파라미터는 W_Q · W_K · W_V · W_O. **A는 입력마다 계산**되는 활성값"],
                  ["“Self-attention이면 Q = K = V”", "같은 X에서 **다른 투영**. 점수 행렬도 일반적으로 비대칭"],
                  ["“Multi-head는 토큰을 head별로 나눠 본다”", "모든 head가 **모든 토큰**을 본다. 나누는 것은 특징 차원"],
                  ["“Head 1은 문법, head 2는 의미 담당”", "역할은 **미리 정해지지 않는다** — 관찰·해석·인과 검증을 구분"],
                  ["“Transformer가 attention을 발명했다”", "Attention은 2014, self-attention도 그 전에 있었다. 2017년은 **조합**"],
                  ["“위치 인코딩은 sin/cos여야 한다”", "학습형 · 상대 위치 · RoPE 등 여러 방식. 필요한 것은 **위치 단서**"]])

d.homework([("손계산 (원자료 운영안 6회차)", "4토큰 예제에서 Query B, C의 행을 손으로 계산해 전체 행렬 그림과 맞춰 본다. √2 스케일을 빼면 어떻게 바뀌는지도."),
            ("shape 추적", "d = 12, H = 3, B = 2, N = 7일 때 multi-head의 모든 단계 shape을 표로 쓰고, 코드로 확인한다."),
            ("순열 실험", "dropout을 끈 nn.MultiheadAttention에 토큰 순서를 섞은 입력을 넣고 SA(PX) = P·SA(X)를 확인한다. 위치 인코딩을 더하면?")],
           notes="원자료 운영안 6·7회차 산출물: 정렬 점수·softmax·가중합 손계산, 위치·Q/K/V·Multi-head 실험.")

d.references([["[17] Bahdanau, Cho & Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate", "§3 정렬 모델, 정렬 그림"],
              ["[18] Luong, Pham & Manning (2015). Effective Approaches to Attention-based NMT", "점수 함수 비교"],
              ["[22] Vaswani et al. (2017). Attention Is All You Need", "§3.2 Attention, §3.5 위치 인코딩, Fig.1–2"],
              ["[27] The Annotated Transformer · [28] PyTorch nn.MultiheadAttention 문서", "shape과 구현 대조"],
              ["[39][40] Attention 해석 관련 연구 (원자료 참고문헌)", "heatmap 해석의 한계"]])

d.handoff(["출력마다 원문을 **다시 참조**하는 Attention", "모든 위치가 직접 만나는 **Self-attention**", "Q·K·V · Multi-head · 위치 인코딩"],
          ["attention만으로는 **토큰별 비선형 변환**이 없다", "깊게 쌓으면? 정답을 **훔쳐보지 않고** 학습하려면? **생성**은?"],
          ["**참조만으로**", "**시퀀스 모델을 만들면?**", "FFN · Residual · LayerNorm · Mask · 학습 · 생성"],
          notes="다음 주: 오늘의 attention 블록에 FFN, residual, LayerNorm을 붙여 층을 완성하고, mask와 teacher forcing으로 Decoder를 학습시키고, 토큰을 하나씩 생성한다.")

d.save(OUT)
print("saved", OUT, d.n + 2, "slides")
