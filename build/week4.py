"""Week 4 — 언어·순서·기억: 순서를 어떻게 표현하고, 먼 정보를 어떻게 기억할까?"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from deckkit import *  # noqa

A = lambda p: os.path.join(HERE, "assets", p)
OUT = os.path.join(HERE, "..", "lectures", "week04_rnn_lstm_seq2seq.pptx")

d = Deck(4, "언어·순서·기억: RNN에서 Seq2Seq까지", date="2026-10-26")

# ============================================================ 도입
d.question("순서를 어떻게 표현하고,\n먼 정보를 어떻게 기억할까?",
           "1986–2014 · Token · Embedding · RNN · LSTM · 언어 모델 · Seq2Seq",
           notes="이미지는 격자였지만 언어는 순서다. 길이도 문장마다 다르고, 멀리 떨어진 단어가 서로 의존한다. "
                 "오늘은 문장을 숫자로 바꾸는 법부터 시작해, 순서를 따라 기억을 전달하는 RNN과 LSTM, 그리고 번역을 위한 Seq2Seq까지 간다. "
                 "마지막에 Seq2Seq가 남기는 문제가 다음 주 Attention의 출발점이다.")

d.bridge(["CNN: 지역성·가중치 공유라는 **구조적 가정**", "깊은 학습의 조건: 데이터·GPU·ReLU", "**Residual · LayerNorm**"],
         ["**언어**는 격자가 아니라 순서, 길이도 제각각", "“그 책은 … (20단어) … 재미있었다” — **먼 단어**의 의존"],
         ["**순서를 어떻게 표현하고,**", "**먼 정보를 어떻게 기억할까?**"])

d.roadmap(["문장을 숫자로: 토큰과 임베딩", "RNN: 순서를 따라 상태 전달 (1986/1990)", "장기 의존성: 왜 먼 정보를 잃나 (1991/1994)",
           "LSTM: 보존·쓰기·읽기의 조절 (1997)", "단어의 의미를 학습하기 (2003/2013)", "Seq2Seq: 길이가 다른 입출력 (2014)"],
          ["토큰 ID와 **임베딩 lookup**을 구분하고 shape (B, N) → (B, N, d)를 말한다",
           "RNN 상태 갱신을 **손으로** 두세 단계 계산한다",
           "장기 의존성이 어려운 **세 가지 이유**를 구분한다",
           "LSTM의 c와 h, **덧셈 경로**의 역할을 설명한다",
           "Seq2Seq의 **고정 벡터 병목**을 설명한다"])

d.glossary([["토큰", "모델이 처리하는 텍스트 조각 (단어·부분단어·글자)", "레고 블록 한 조각"],
            ["어휘 |V|", "토큰의 전체 목록과 그 크기", "사전"],
            ["임베딩 E", "토큰마다 하나씩 있는 학습되는 벡터 표 (|V|, d)", "사전의 뜻풀이 (숫자판)"],
            ["은닉 상태 h", "지금까지 읽은 내용을 요약한 벡터", "읽으면서 쓰는 메모"],
            ["장기 의존성", "멀리 떨어진 위치 사이의 관계", "앞 문장의 주어와 뒤의 동사"],
            ["게이트", "0~1 비중으로 정보 흐름을 조절하는 값 (계산됨)", "수도꼭지"],
            ["언어 모델", "다음 토큰의 확률을 예측하는 모델", "문장 이어 쓰기"],
            ["Encoder–Decoder", "입력을 표현하는 부분과 출력을 생성하는 부분", "통역사의 듣기와 말하기"]])

# ============================================================ Part 1
d.part(1, "문장을 숫자로: 토큰과 임베딩", "“나는 학교에 간다”를 모델이 계산할 수 있는 숫자로 바꾸려면?")

s = d.slide("텍스트가 벡터가 되기까지", lead="문자열 → 토큰 → 정수 ID → 학습되는 벡터. 모델이 계산하는 것은 마지막 벡터다", stage="아이디어",
            notes="문장을 토큰으로 자르고(토큰화), 각 토큰에 사전의 번호(ID)를 붙이고, 그 번호로 임베딩 표에서 벡터를 꺼낸다. "
                  "배치 B개 문장, 길이 N이면 ID 텐서는 (B, N), 임베딩 후 (B, N, d). 1주차의 (B, N, d)가 바로 여기서 나온다. "
                  "예시 ID 숫자는 설명용이다.")
top, bot = s.area.top(2.0, gap=0.35)
s.flow([{"head": "문자열", "body": "“나는 학교에 간다”"}, {"head": "토큰", "body": "[나, 는, 학교, 에, 간다]"},
        {"head": "ID", "body": "[12, 7, 305, 9, 88]\nshape (N,) = (5,)"},
        {"head": "벡터", "body": "E[ID] → (5, d)", "tone": "dark"}], top, body_size=15, head_size=18)
s.table(["단계", "shape (배치 B, 길이 N)", "학습되나?"], [["토큰 ID", "(B, N) — 정수", "아니오 (tokenizer가 정함)"],
                                                   ["임베딩 표 E", "(|V|, d)", "**예** — 파라미터"],
                                                   ["임베딩 결과", "(B, N, d)", "E에서 꺼낸 값 (활성값)"]],
        bot, widths=[1.6, 2.6, 2.8], size=16)

s = d.slide("번호는 의미가 아니다", lead="ID 100이 ID 10보다 ‘열 배’인 것은 아니다 — ID는 표에서 벡터를 꺼내는 주소", stage="문제",
            notes="ID를 그대로 숫자로 계산에 넣으면 '305번 학교가 12번 나보다 크다' 같은 엉뚱한 관계가 생긴다. "
                  "one-hot: 어휘 크기 |V|의 벡터에서 자기 위치만 1. one-hot 행벡터에 임베딩 표 E(|V|, d)를 곱하면 E의 해당 행이 그대로 나온다 = 행 lookup. "
                  "그래서 실제로는 큰 one-hot을 만들지 않고 행을 바로 꺼낸다. E의 값은 학습되는 파라미터이고, 학습을 통해 비슷한 쓰임의 토큰이 비슷한 벡터를 갖게 된다.")
L, R = s.cols(0.6)
s.image(A("week4/onehot_lookup.png"), L)
s.bullets(["ID를 그대로 쓰면 크기 관계가 **엉터리**", "**one-hot**: 자기 자리만 1인 벡터", "one-hot @ E = E의 **그 행**",
           ("수학적으로 같다 → 실제로는 행을 바로 꺼냄 (lookup)", 1), "E (|V|, d)는 **학습되는 파라미터**"], R)

s = d.slide("단어와 토큰은 항상 같지 않다", lead="어떤 단위로 자르느냐는 어휘 크기와 시퀀스 길이 사이의 절충", stage="아이디어",
            notes="단어 단위는 직관적이지만 어휘가 매우 커지고 처음 보는 단어(희귀어)를 다루기 어렵다. 글자/byte 단위는 어휘가 작지만 시퀀스가 길어진다. "
                  "subword는 그 사이의 절충: 자주 나오는 조각은 통째로, 드문 단어는 쪼갠다. unhappiness → un + happi + ness는 설명용 예시로, 특정 tokenizer의 실제 결과가 아니다. "
                  "주의: tokenizer와 모델 가중치는 짝이다. 같은 ID가 다른 토큰을 가리키게 바꾸면 학습한 임베딩과 출력 head의 의미가 어긋난다.")
s.table(["단위", "장점", "비용"], [["단어 (word)", "익숙한 의미 단위, 짧은 시퀀스", "큰 어휘 · 희귀어 문제"],
                                 ["글자 · byte", "작은 어휘, 어떤 문자열도 표현", "시퀀스가 **길어진다**"],
                                 ["부분단어 (subword)", "어휘 크기와 길이의 **절충**", "언어·학습 데이터에 따라 분할이 달라짐"]],
        Box(s.area.x, s.area.y, s.area.w, 2.3), widths=[2.2, 4.3, 4.3], size=16)
L, R = Box(s.area.x, s.area.y + 2.6, s.area.w, s.area.h - 2.6).cols(0.5, gap=0.4)
s.callout("예: unhappiness → un + happi + ness\n(분할 설명용 예시 — 특정 tokenizer의 실제 결과가 아님)", L, kind="tip", size=16)
s.callout("==주의== tokenizer와 모델 가중치는 **짝**이다. ID 매핑을 바꾸면 학습한 임베딩과 출력의 의미가 어긋난다.", R,
          kind="warn", size=16)

s = d.slide("PyTorch: nn.Embedding", lead="(B, N) 정수 → (B, N, d) 벡터. 파라미터는 |V| × d", stage="코드",
            notes="nn.Embedding(num_embeddings=|V|, embedding_dim=d). 어휘 10,000개, d=8이면 파라미터 80,000개. "
                  "입력은 정수 ID 텐서 (B, N), 출력은 (B, N, d). 같은 ID는 항상 같은 벡터가 나온다(아직 문맥 없음). "
                  "문맥에 따라 표현이 달라지는 것은 이후 계산(RNN, Transformer 블록)의 몫이다 — Part 5.")
L, R = s.cols(0.58)
s.code("import torch, torch.nn as nn\n"
       "emb = nn.Embedding(10000, 8)      # |V| = 10000, d = 8\n"
       "ids = torch.tensor([[12, 7, 305, 9, 88],\n"
       "                    [ 4, 51,  6, 0,  0]])  # 0 = PAD\n"
       "x = emb(ids)\n"
       "print(ids.shape, x.shape)  # (2, 5)  (2, 5, 8)\n"
       "print(emb.weight.shape)    # (10000, 8) -> 80,000개\n"
       "print(torch.equal(x[0, 1], emb.weight[7]))  # True", L, size=13)
cb = s.last_code_box
s.callout("짧은 문장은 PAD 토큰으로 길이를 맞춘다 (1주차 batch 그림).", Box(L.x, cb.b + 0.25, L.w, 0.7), kind="tip", size=15)
s.bullets(["`emb(ids)` = 표에서 **행 꺼내기**", "`x[0, 1]` = `emb.weight[7]`", "파라미터 = |V| × d",
           "같은 ID → 항상 **같은 벡터**", ("문맥 반영은 이후 계산의 몫", 1)], R)

# ============================================================ Part 2
d.part(2, "RNN: 순서를 따라 상태 전달", "1986 · 1990 — 길이가 제각각이고 순서가 의미를 바꾸는 입력을 어떻게 처리할까?")

s = d.slide("MLP나 CNN으로 문장을 읽으면?", lead="같은 단어라도 순서가 바뀌면 뜻이 바뀐다. 문장마다 길이도 다르다", stage="문제",
            notes="'개가 사람을 물었다'와 '사람이 개를 물었다'는 같은 토큰들로 이루어졌지만 뜻이 정반대다. 토큰 벡터를 더하거나 평균 내면 둘이 구분되지 않는다. "
                  "MLP는 입력 크기가 고정이라 길이가 다른 문장을 그대로 넣을 수 없다. CNN은 고정된 창 크기만큼만 본다 — 먼 단어의 관계를 보려면 층을 많이 쌓아야 한다. "
                  "필요한 것: 길이와 무관한 같은 규칙으로, 순서대로 읽으며 지금까지의 내용을 기억하는 구조.")
rest = s.cards([{"head": "순서가 의미를 바꾼다", "body": ["“개가 사람을 물었다”", "“사람이 개를 물었다”", "→ 토큰 집합은 같다"]},
                {"head": "길이가 제각각", "body": ["“안녕” (2토큰)", "“오늘 날씨가 정말 좋네요” (6토큰)", "→ MLP는 입력 크기 고정"]},
                {"head": "먼 단어의 의존", "body": ["“그 **책**은 … (20단어) … **재미있었다**”", "→ CNN은 고정된 창만 본다"],
                 "tone": "accent"}], cols=3, body_size=16, head_size=18)
s.callout("필요한 것: 길이와 무관한 **같은 규칙**으로, **순서대로** 읽으며 지금까지를 **기억**하는 구조",
          Box(rest.x, rest.y + 0.1, rest.w, 0.9), kind="key", size=17)

s = d.slide("아이디어: 같은 셀을 반복하며 상태를 넘긴다", lead="각 시점에서 (현재 입력, 이전 상태) → 새 상태. 같은 가중치를 모든 시점에 재사용",
            stage="아이디어",
            notes="RNN(순환 신경망)은 토큰을 하나씩 읽으며 은닉 상태 h를 갱신한다. h는 '지금까지 읽은 내용의 요약 메모'. "
                  "모든 시점이 같은 가중치 W_x, W_h, b를 쓰므로 길이가 달라도 같은 규칙이 적용된다(CNN이 위치마다 같은 필터를 쓴 것과 비슷한 공유). "
                  "Jordan(1986)은 출력을 되먹임하는 구조를, Elman(1990) 'Finding Structure in Time'은 은닉 상태를 되먹임하는 단순 순환망을 제시했다. "
                  "이전 상태가 다르므로 같은 토큰도 문맥에 따라 다른 표현을 갖게 된다.")
top, bot = s.area.top(2.6, gap=0.3)
s.image(A("week4/rnn_unrolled.png"), top)
s.bullets(["h = 지금까지 읽은 내용의 **요약 메모**", "모든 시점이 **같은 W_x, W_h, b** — 길이가 달라도 같은 규칙",
           "이전 상태가 다르므로 **같은 토큰도 다른 표현**", "Jordan (1986) · **Elman (1990)** ‘Finding Structure in Time’"], bot, size=16)

s = d.slide("RNN 상태 갱신을 손으로", lead="h_t = tanh(x_t W_x + h_(t−1) W_h + b) — 첫 입력의 흔적이 점점 옅어진다", stage="계산",
            notes="1차원 예시: W_x = 1, W_h = 0.5, b = 0, h_0 = 0. 입력 x = (1, 0, 0). "
                  "t=1: h1 = tanh(1·1 + 0.5·0) = 0.762. t=2: h2 = tanh(0 + 0.5·0.762) = tanh(0.381) = 0.363. t=3: h3 = tanh(0.5·0.363) = 0.180. "
                  "첫 입력의 흔적이 매 단계 절반 이하로 줄어든다. W_h를 키우면 오래 남지만 너무 크면 값과 기울기가 폭주한다 — Part 3의 문제로 이어진다.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("h_t = tanh( x_t · W_x  +  h_(t−1) · W_h  +  b )", top, size=24)
L, R = bot.cols(0.55, gap=0.4)
s.table(["t", "입력 x_t", "계산", "h_t"], [["1", "1", "tanh(1·1 + 0.5·0)", "**0.762**"], ["2", "0", "tanh(0 + 0.5·0.762)", "**0.363**"],
                                        ["3", "0", "tanh(0 + 0.5·0.363)", "**0.180**"]], Box(L.x, L.y, L.w, 2.0), size=15, align="cccc")
s.bullets(["설정: W_x = 1, W_h = 0.5, b = 0, h_0 = 0"], Box(L.x, L.y + 2.2, L.w, 0.8), size=15)
s.bullets(["첫 입력의 흔적이 **점점 옅어진다**", "W_h를 키우면 오래 남지만", ("너무 크면 값·기울기가 **폭주**", 1),
           "→ 먼 정보를 다루기 어려운 이유 (Part 3)"], R)

s = d.slide("PyTorch: nn.RNN의 shape", lead="(B, N, d) 입력 → 모든 시점의 상태 (B, N, d_h) + 마지막 상태", stage="코드",
            notes="nn.RNN(input_size=d, hidden_size=d_h, batch_first=True). 입력 (2, 5, 8) → output (2, 5, 16): 모든 시점의 h, h_n (1, 2, 16): 마지막 시점의 h(층 수 1). "
                  "파라미터: W_x (8×16) + W_h (16×16) + 편향 2개(16+16) = 416. 길이 N과 무관하다. "
                  "LSTM은 게이트 4개분이라 1,664개(4배).")
L, R = s.cols(0.58)
s.code("import torch, torch.nn as nn\n"
       "rnn = nn.RNN(input_size=8, hidden_size=16,\n"
       "             batch_first=True)\n"
       "x = torch.randn(2, 5, 8)         # (B, N, d)\n"
       "out, h_n = rnn(x)\n"
       "print(out.shape)   # (2, 5, 16)  모든 시점의 h\n"
       "print(h_n.shape)   # (1, 2, 16)  마지막 h\n"
       "print(sum(p.numel() for p in rnn.parameters()))  # 416", L, size=13)
cb = s.last_code_box
s.callout("`out[:, -1]`와 `h_n[0]`은 같은 값이다 (한 층, 단방향) — 직접 확인해 보기", Box(L.x, cb.b + 0.25, L.w, 0.8), kind="tip", size=15)
s.bullets(["`out`: 시점마다의 h → 문맥 표현", "`h_n`: 마지막 h → 문장 **요약**", "파라미터 416 = 8·16 + 16·16 + 16 + 16",
           ("길이 N과 **무관**", 1), "nn.LSTM은 4배: 1,664"], R)

# ============================================================ Part 3
d.part(3, "장기 의존성: 왜 먼 정보를 잃나", "1991 · 1994 — “그 책은 … 재미있었다”, 멀리 떨어진 관계도 학습할 수 있을까?")

s = d.slide("시간을 거슬러 기울기가 곱해진다", lead="k단계 전까지 가려면 같은 종류의 인자를 k번 곱한다 — 0.9⁵⁰ ≈ 0.005, 1.1⁵⁰ ≈ 117", stage="문제",
            notes="RNN을 시간 방향으로 펼치면 아주 깊은 망이 된다. 50단계 전의 입력에 기울기가 도달하려면 시점마다 W_h와 tanh 도함수의 곱을 50번 거친다. "
                  "그 인자가 대략 0.9면 0.9^50 ≈ 0.005로 소실, 1.1이면 1.1^50 ≈ 117로 폭주. 3주차에 깊이 방향에서 본 문제가 시간 방향에서 다시 나타난 것. "
                  "Hochreiter(1991, 석사 논문)와 Bengio, Simard, Frasconi(1994)가 이 어려움을 분석했다. 원자료 주의: '정보가 오래되면 사라진다'는 비유로 끝내지 말고, 행렬 곱과 활성화 미분이 반복된다는 계산으로 이해한다.")
L, R = s.cols(0.58)
s.image(A("week4/grad_decay.png"), L)
s.bullets(["펼친 RNN = 시간 방향으로 **아주 깊은 망**", "인자 0.9 → 50단계: **0.005** (소실)", "인자 1.1 → 50단계: **117** (폭주)",
           "3주차 깊이 문제가 **시간 방향**에서 재등장", "Hochreiter (1991), Bengio et al. (1994)", ("비유가 아니라 **곱셈의 반복**으로 이해", 1)], R)

s = d.slide("장기 의존성이 어려운 이유들", lead="학습 신호 · 정보 표현 · 계산 의존성 — 서로 다른 문제이고, 해결 방향도 다르다", stage="정리",
            notes="원자료의 표. ① 학습 신호: 먼 위치까지 기울기가 작아지거나 커진다 → 기억 경로, 게이트, gradient clipping(폭주 시 기울기 크기 제한). "
                  "② 정보 표현: 고정 크기 상태 h 하나에 필요한 모든 정보를 담아야 한다 → 상태 설계, 외부 기억, 직접 참조(Attention). "
                  "③ 계산 의존성: h_t를 구하려면 h_(t−1)이 먼저 필요 → 순차 계산, 병렬화 어려움 → 비순환 구조(Transformer). "
                  "이 세 줄이 이후 LSTM(①), Attention(②), Transformer(③)로 이어지는 지도다.")
s.table(["어려움", "무엇이 문제인가", "해결 방향의 예", "등장"],
        [["① 학습 신호", "먼 위치까지 기울기가 작아지거나 커진다", "기억 경로 · 게이트 · gradient clipping", "**LSTM** (오늘)"],
         ["② 정보 표현", "고정 크기 상태 하나에 필요한 정보를 다 담아야 한다", "상태 설계 · 외부 기억 · **직접 참조**", "**Attention** (5주차)"],
         ["③ 계산 의존성", "h_t를 구하려면 h_(t−1)이 먼저 필요 — 순차 계산", "비순환 · 병렬화 가능한 구조", "**Transformer** (5·6주차)"]],
        Box(s.area.x, s.area.y, s.area.w, 3.2), widths=[1.7, 4.0, 3.6, 2.2], size=16)
s.callout("이 표가 앞으로 3주의 지도다: ① → LSTM, ② → Attention, ③ → Transformer",
          Box(s.area.x, s.area.y + 3.5, s.area.w, 0.8), kind="key", size=17)

# ============================================================ Part 4
d.part(4, "LSTM: 보존·쓰기·읽기의 조절", "1997 — 무엇을 지키고, 무엇을 새로 쓰고, 무엇을 꺼낼지 학습하면?")

s = d.slide("LSTM 셀 한눈에 보기", lead="곱셈으로 조절하고 덧셈으로 갱신하는 ‘기억 통로’ c를 따로 둔다", stage="아이디어",
            notes="Hochreiter & Schmidhuber(1997). 핵심은 cell state c라는 별도의 기억 통로. c는 매 시점 '곱하고 더하는' 방식으로만 바뀐다. "
                  "게이트 세 개가 비중을 정한다: forget f(이전 기억을 얼마나 보존), input i(새 후보 g를 얼마나 쓸지), output o(기억을 밖으로 얼마나 꺼낼지). "
                  "c(내부 기억)와 h(밖으로 내보내는 상태)를 구분하는 것이 입문자의 핵심 포인트. 3주차 Residual의 '더하는 지름길'과 닮았다.")
L, R = s.cols(0.62)
s.image(A("week4/lstm_cell.png"), L)
s.bullets(["**c**: 내부 기억 통로 (cell state)", "**h**: 밖으로 내보내는 상태", "**f** 보존 · **i** 쓰기 · **o** 읽기",
           "c는 **곱하고 더하는** 방식으로만 갱신", ("3주차 Residual의 지름길과 닮았다", 1)], R)

s = d.slide("게이트는 입력으로 계산된다", lead="네 값 모두 같은 입력 [h_(t−1), x_t]에서, 서로 다른 가중치로", stage="계산",
            notes="f, i, o는 sigmoid라 0~1(비중), g는 tanh라 −1~1(새로 쓸 후보 값). 게이트는 사람이 정한 스위치가 아니라 입력과 이전 상태로 매번 계산된다. "
                  "원자료 주의: 이 식은 forget gate를 포함한 널리 쓰이는 후속 형태다. forget gate는 Gers, Schmidhuber, Cummins(2000)가 도입했고, 1997년 원형에는 없었다. "
                  "입문 단계에서는 식을 외우기보다 c와 h의 차이, 곱으로 조절, 덧셈으로 갱신, 순차 의존이 남는다는 점을 설명할 수 있으면 된다.")
top, bot = s.area.top(1.55, gap=0.3)
s.formula(["f = σ([h, x] W_f + b_f)     i = σ([h, x] W_i + b_i)",
           "g = tanh([h, x] W_g + b_g)  o = σ([h, x] W_o + b_o)"], top, size=20)
L, R = bot.cols(0.55, gap=0.4)
s.symbols([("f", "forget: 이전 기억 보존 비중 (0~1)"), ("i", "input: 새 후보를 쓰는 비중 (0~1)"),
           ("g", "새로 쓸 후보 값 (−1~1)"), ("o", "output: 밖으로 꺼내는 비중 (0~1)"), ("[h, x]", "이전 상태와 현재 입력을 이어 붙인 벡터")],
          L, size=15)
s.bullets(["게이트는 스위치가 아니라 **매번 계산**되는 값", "==주의== forget gate는 **2000년** Gers et al.이 도입",
           ("1997 원형에는 없었다", 1), "식 암기보다 **c·h 구분, 곱·덧셈 경로**를 설명할 수 있으면 충분"], R)

s = d.slide("셀 갱신을 손으로", lead="c_t = f ⊙ c_(t−1) + i ⊙ g,   h_t = o ⊙ tanh(c_t)", stage="계산",
            notes="예: 이전 기억 c = 2.0. f = 0.9, i = 0.1, g = 0.5 → c_t = 0.9·2.0 + 0.1·0.5 = 1.85. 기억이 거의 그대로 보존된다. "
                  "o = 0.5 → h_t = 0.5·tanh(1.85) = 0.5·0.952 = 0.476. f = 0.5였다면 c_t = 1.0 + 0.05 = 1.05로 기억이 절반으로. "
                  "⊙는 원소별 곱. 핵심: c_t는 c_(t−1)에 f를 곱하고 무언가를 '더하는' 방식이라, f가 1에 가까우면 기억과 기울기가 오래 유지된다(∂c_t/∂c_(t−1) = f).")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("c_t = f ⊙ c_(t−1) + i ⊙ g        h_t = o ⊙ tanh(c_t)", top, size=22)
L, R = bot.cols(0.55, gap=0.4)
s.table(["", "f = 0.9 (보존)", "f = 0.5"], [["c_(t−1)", "2.0", "2.0"], ["i, g", "0.1, 0.5", "0.1, 0.5"],
                                          ["c_t = f·c + i·g", "1.8 + 0.05 = **1.85**", "1.0 + 0.05 = **1.05**"],
                                          ["h_t = 0.5·tanh(c_t)", "**0.476**", "0.391"]], L, size=15, align="lcc", highlight=[2])
s.bullets(["f ≈ 1이면 기억이 **거의 그대로**", "∂c_t / ∂c_(t−1) = **f**", ("f ≈ 1 → 기울기도 오래 유지", 1),
           "RNN은 매번 W_h와 tanh′를 곱했다", "c는 **곱하고 더할 뿐** → 긴 경로에 유리"], R)

s = d.slide("LSTM이 해결한 것과 남은 것", lead="장기 의존성을 ‘학습하기 쉽게’ 만들었다 — 완벽한 기억도, 병렬 계산도 아니다", stage="검증",
            notes="LSTM은 ① 학습 신호 문제를 크게 줄였고 1997~2014년 음성 인식, 번역 등에서 표준이 되었다. "
                  "하지만 ② 정보 표현: 여전히 고정 크기 c, h에 담아야 한다. ③ 계산 의존성: h_t는 h_(t−1)이 있어야 계산된다 — 긴 시퀀스를 병렬로 학습하기 어렵다. "
                  "원자료: LSTM은 장기 의존성을 학습하기 위한 설계이지, 모든 긴 문맥을 완벽하게 기억한다는 보장이 아니다.")
rest = s.cards([{"head": "해결한 것", "bullets": True,
                 "body": ["① **학습 신호**: 덧셈 기억 경로로 긴 의존성 학습이 쉬워짐", "음성 인식 · 번역 등에서 오랫동안 표준"]},
                {"head": "남은 것", "tone": "accent", "bullets": True,
                 "body": ["② **고정 크기** 상태 c, h에 모든 것을 담아야 한다", "③ h_t는 h_(t−1)이 필요 — **순차 계산**",
                          "완벽한 기억을 **보장하지 않는다**"]}], cols=2, body_size=17, head_size=19)
s.callout("GRU (Cho et al., 2014)는 게이트를 2개로 줄인 변형 — 같은 남은 문제를 공유한다.",
          Box(rest.x, rest.y + 0.1, rest.w, 0.8), kind="tip", size=16)

s = d.slide("사고실험: 맨 앞 숫자 기억하기", lead="길이를 5 → 10 → 20 → 40으로 늘리며, 어디서부터 어려워지는지 측정한다", stage="검증",
            notes="원자료의 사고실험: 문장 맨 앞의 숫자를 끝에서 다시 출력하는 과제. 입력 길이를 늘리며 학습과 일반화가 어려워지는 지점을 찾는다. "
                  "작은 RNN과 LSTM의 크기·학습량을 같게 통제하고, 길이에 따른 정확도 곡선을 기록한다. "
                  "중요: 'Transformer가 항상 이긴다'는 결론을 미리 정하지 않는다. 실험 설계의 태도를 연습하는 과제다.")
top, bot = s.area.top(1.9, gap=0.35)
s.flow([{"head": "입력", "body": "7, a, c, b, …, d\n(길이 N)"}, {"head": "모델", "body": "RNN / LSTM\n(크기·학습량 동일)"},
        {"head": "출력", "body": "마지막에 **7**을 다시 출력"}, {"head": "기록", "body": "N = 5, 10, 20, 40별 정확도", "tone": "dark"}],
       top, body_size=15, head_size=17)
s.bullets(["**통제**: 모델 크기, 학습 step, 데이터 수를 같게", "**측정**: 길이별 정확도 곡선 — 어디서 무너지나?",
           "RNN과 LSTM의 곡선을 비교하고 **이유를 설명**", "==주의== ‘새 모델이 항상 이긴다’는 결론을 미리 정하지 않는다"], bot)

# ============================================================ Part 5
d.part(5, "단어의 의미를 학습하기", "2003 · 2013 — 좋은 단어 벡터는 어디서 오나? 다음 단어를 맞히다 보면")

s = d.slide("문장 = 조건부 확률의 연결", lead="P(문장) = P(첫 단어) × P(둘째 | 첫째) × … — 다음 토큰 예측의 반복", stage="계산",
            notes="확률의 연쇄법칙으로 문장 전체의 확률을 '앞 토큰들이 주어졌을 때 다음 토큰의 확률'의 곱으로 쓸 수 있다. "
                  "예: P(나는)=0.2, P(학교에|나는)=0.3, P(간다|나는 학교에)=0.5 → 0.03. −log로 쓰면 3.51(2주차 cross-entropy의 합). "
                  "텍스트만 있으면 (앞부분 → 다음 토큰) 정답 쌍을 무한히 만들 수 있다 — 자기지도학습. "
                  "원자료 주의: 이 확률 분해는 RNN만의 성질이 아니다. 확률 모델의 목표와 그것을 계산하는 아키텍처를 분리해서 본다. 번역처럼 입력 x가 있으면 각 항에 x를 추가로 조건화한다.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("P(y_1, …, y_T) = Π_t  P(y_t | y_<t)", top, size=26)
L, R = bot.cols(0.52, gap=0.4)
s.table(["항", "확률 (예시)"], [["P(나는)", "0.2"], ["P(학교에 | 나는)", "0.3"], ["P(간다 | 나는 학교에)", "0.5"],
                              ["곱 = P(문장)", "**0.03**  (−log = 3.51)"]], Box(L.x, L.y, L.w, 2.3), size=16, align="lc")
s.bullets(["정답 쌍이 텍스트에서 **저절로** 생긴다 → 자기지도학습"], Box(L.x, L.y + 2.5, L.w, L.h - 2.5), size=16)
s.bullets(["(나는) → 학교에", "(나는 학교에) → 간다", "−log 합 = 2주차 **cross-entropy**",
           "==주의== 목표(확률 분해) ≠ 아키텍처(RNN 등)", ("Transformer도 같은 목표를 쓴다", 1),
           "번역: 모든 항에 입력 x를 조건으로"], R)

s = d.slide("2003: 신경망 언어 모델", lead="단어 벡터와 다음 단어 예측을 함께 학습 — 임베딩은 Word2Vec에서 처음 나온 것이 아니다", stage="역사",
            notes="Bengio, Ducharme, Vincent, Jauvin(2003) 'A Neural Probabilistic Language Model'. 앞의 n−1개 단어를 임베딩으로 바꾸고, MLP로 다음 단어의 softmax 확률을 예측한다. "
                  "임베딩 표 E도 역전파로 함께 학습된다. 결과적으로 비슷한 문맥에 나오는 단어들이 비슷한 벡터(분산 표현)를 갖게 된다. "
                  "원자료 주의: '임베딩은 Word2Vec에서 처음 등장했다'는 틀린 말이다.")
top, bot = s.area.top(1.9, gap=0.35)
s.flow([{"head": "앞 단어들", "body": "“나는 학교에”"}, {"head": "임베딩 lookup", "body": "E에서 벡터 꺼내기 (학습됨)"},
        {"head": "MLP", "body": "은닉층 (2주차)"}, {"head": "Softmax", "body": "다음 단어 확률 |V|개", "tone": "dark"}],
       top, body_size=15, head_size=17)
s.bullets(["Bengio et al. (2003) ‘A Neural Probabilistic Language Model’", "임베딩 E도 **역전파로 함께** 학습된다",
           "비슷한 문맥의 단어 → 비슷한 벡터 (**분산 표현**)", "==주의== 임베딩은 Word2Vec(2013)에서 **처음 나온 것이 아니다**"], bot)

s = d.slide("2013: Word2Vec", lead="주변 문맥으로 단어를(CBOW), 단어로 주변 문맥을(Skip-gram) — 표현 학습을 대규모로 효율적으로", stage="역사",
            notes="Mikolov et al.(2013). 목표를 단순화해 수십억 단어 규모에서 빠르게 단어 벡터를 학습했다. CBOW는 주변 단어로 가운데 단어를, Skip-gram은 가운데 단어로 주변 단어를 예측. "
                  "유명한 예: king − man + woman ≈ queen. 그림은 설명용 2D 그림이지 실제 학습 벡터가 아니다. "
                  "원자료 주의: 특정 벡터 차원이 사람이 붙인 의미(성별, 국가)와 일대일로 대응할 필요는 없다.")
L, R = s.cols(0.55)
s.image(A("week4/analogy.png"), L)
s.table(["방식", "입력 → 예측"], [["CBOW", "주변 단어 → **가운데** 단어"], ["Skip-gram", "가운데 단어 → **주변** 단어"]],
        Box(R.x, R.y, R.w, 1.4), size=15)
s.bullets(["Mikolov et al. (2013)", "목표를 단순화해 **대규모·고속** 학습", "king − man + woman ≈ queen",
           ("그림은 설명용 2D — 실제 벡터 아님", 1), "차원 하나가 사람의 의미와 **일대일일 필요 없다**"],
          Box(R.x, R.y + 1.65, R.w, R.h - 1.65), size=15)

s = d.slide("정적 표현 vs 문맥 표현", lead="임베딩 직후 ‘배’는 늘 같은 벡터 — 문맥 계산을 거친 뒤에야 먹는 배·타는 배가 갈린다", stage="아이디어",
            notes="기본 임베딩은 같은 토큰에 항상 같은 벡터를 준다(정적). 'river bank'와 'bank account', '배를 먹었다'와 '배를 탔다'의 뜻이 달라지려면 "
                  "주변 입력을 참조한 뒤의 표현이 필요하다. RNN에서는 h_t가, Transformer에서는 이후 블록들의 출력이 그 역할을 한다. "
                  "원자료: '단어 의미가 모두 임베딩 표 안에 저장된다'보다 'lookup과 문맥 계산이 함께 표현을 만든다'가 더 정확하다.")
rest = s.cards([{"head": "정적 표현 (임베딩 lookup 직후)", "tone": "plain", "bullets": True,
                 "body": ["“배를 먹었다” 의 배 = E[배]", "“배를 탔다” 의 배 = E[배]", "→ **같은 벡터**"]},
                {"head": "문맥 표현 (문맥 계산 이후)", "bullets": True,
                 "body": ["RNN: h_t가 앞 내용을 반영", "Transformer: 이후 블록이 주변을 참조", "→ **다른 벡터**"]}],
               cols=2, body_size=17, head_size=18)
s.callout("의미는 임베딩 표에 ‘저장’된 것이 아니라, **lookup + 문맥 계산**이 함께 만든다.",
          Box(rest.x, rest.y + 0.1, rest.w, 0.8), kind="key", size=17)

# ============================================================ Part 6
d.part(6, "Seq2Seq: 길이가 다른 입력과 출력", "2014 — “I am a student” → “나는 학생이다”, 길이가 다르면?")

s = d.slide("번역: 입력과 출력의 길이가 다르다", lead="RNN은 입력 하나에 출력 하나 — 번역은 S개를 읽고 T개를 써야 한다", stage="문제",
            notes="번역, 요약, 질의응답은 입력 길이 S와 출력 길이 T가 다르고, 어순도 다르다. "
                  "'I am a student'(S=4) → '나는 학생 이다'(T=3, 토큰화 예시). RNN처럼 시점마다 하나씩 출력하면 길이와 어순을 맞출 수 없다. "
                  "해결 아이디어: 먼저 입력 전체를 다 읽고(encode), 그 다음 출력을 한 토큰씩 생성(decode)한다.")
rest = s.cards([{"head": "입력 (영어, S = 4)", "tone": "plain", "body": "I · am · a · student"},
                {"head": "출력 (한국어, T = 3)", "body": "나는 · 학생 · 이다"},
                {"head": "어려움", "tone": "accent", "body": ["길이가 다르다 (S ≠ T)", "어순이 다르다", "시점마다 1:1 출력 불가"]}],
               cols=3, body_size=17, head_size=18)
s.callout("아이디어: 입력을 **끝까지 다 읽고**(Encoder), 그 다음 출력을 **한 토큰씩** 생성(Decoder)",
          Box(rest.x, rest.y + 0.1, rest.w, 0.9), kind="key", size=17)

s = d.slide("Encoder → 문맥 벡터 c → Decoder", lead="Encoder가 입력을 고정 길이 벡터 c로 요약, Decoder가 c와 이전 출력으로 다음 토큰을 만든다",
            stage="아이디어",
            notes="Encoder RNN이 입력을 끝까지 읽은 마지막 상태를 문맥 벡터 c로 쓴다. Decoder RNN은 c에서 시작해 BOS(시작) 토큰을 받고 첫 단어를 예측, "
                  "그 단어를 다음 입력으로 넣어 다음 단어를 예측… EOS(끝) 토큰이 나오면 멈춘다 — 그래서 출력 길이를 스스로 정한다. "
                  "원자료: Encoder–Decoder는 특정 신경망 종류가 아니라 '입력 표현'과 '출력 생성'의 역할 분담이다. Transformer도 이 구조를 쓴다.")
top, bot = s.area.top(2.9, gap=0.3)
s.image(A("week4/seq2seq.png"), top)
s.bullets(["Encoder: 입력 S개를 읽고 마지막 상태 = **c**", "Decoder: c + 이전 출력 → 다음 토큰, **EOS**가 나오면 멈춤",
           "Encoder–Decoder는 신경망 종류가 아니라 **역할 분담** — Transformer도 이 구조"], bot, size=16)

s = d.slide("학습 목표와 2014년의 두 논문", lead="p(y | x) = Π p(y_t | y_<t, c) — 앞에서 본 조건부 확률의 곱에 입력 조건 c를 더했다", stage="계산",
            notes="학습 목표: 정답 번역의 각 토큰에 대한 −log 확률의 합(cross-entropy). 학습 때는 Decoder 입력에 모델 예측 대신 정답의 이전 토큰을 넣는다(teacher forcing, 6주차 자세히). "
                  "Sutskever, Vinyals, Le(2014): 4층 LSTM Encoder–Decoder, 입력 문장을 뒤집어 넣는 요령으로 성능 향상, WMT'14 영→프 BLEU 34.8(앙상블), 기존 SMT 후보 재정렬 시 36.5. "
                  "Cho et al.(2014): RNN Encoder–Decoder와 GRU 제안. 원자료: Bahdanau Attention 논문도 2014년 거의 같은 시기에 공개 — 수업 순서가 긴 역사적 간격을 뜻하지 않는다.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("p(y | x) = Π_t  p(y_t | y_<t, c)", top, size=26)
s.cards([{"head": "Sutskever, Vinyals & Le (2014)", "bullets": True,
          "body": ["4층 LSTM Encoder–Decoder", "입력 문장을 **뒤집어** 넣는 요령", "WMT’14 영→프 BLEU **34.8** (앙상블)"]},
         {"head": "Cho et al. (2014)", "bullets": True,
          "body": ["RNN Encoder–Decoder", "**GRU** 제안 (게이트 2개)", "긴 문장에서 성능 저하 관찰"]},
         {"head": "같은 해 (→ 5주차)", "tone": "accent", "bullets": True,
          "body": ["Bahdanau et al. (2014) Attention", "거의 **같은 시기**에 공개", "수업 순서 ≠ 긴 시간 간격"]}], bot, cols=3,
        body_size=15, head_size=16)

s = d.slide("병목: 질문이 달라도 요약본은 하나", lead="출력 위치마다 필요한 입력 정보가 다른데, Decoder는 고정 길이 c 하나만 받는다", stage="문제",
            notes="'나는'을 쓸 때는 'I'가, '학생'을 쓸 때는 'student'가 필요하다. 그런데 Decoder가 받는 것은 문장 전체를 압축한 c 하나뿐이다. "
                  "문장이 10단어든 50단어든 c의 크기는 같다 — 긴 문장일수록 정보를 잃는다(Cho et al. 2014의 관찰). "
                  "Part 3 표의 ② '정보 표현' 문제가 번역에서 가장 선명하게 드러난 것. 다음 주 질문: Encoder의 위치별 표현 h_1…h_S를 버리지 말고, 필요할 때마다 다시 찾아보면?")
rest = s.cards([{"head": "“나는”을 쓸 때", "body": ["필요한 입력: **I**"]}, {"head": "“학생”을 쓸 때", "body": ["필요한 입력: **student**"]},
                {"head": "“이다”를 쓸 때", "body": ["필요한 입력: **am**"]},
                {"head": "하지만 받는 것은", "tone": "accent", "body": ["항상 **같은 c 하나**", "문장이 길어도 크기 고정"]}],
               cols=4, body_size=17, head_size=17)
s.callout("질문: Encoder의 위치별 표현 h_1 … h_S를 **버리지 말고**, 출력할 때마다 **필요한 곳을 다시 찾아보면?**",
          Box(rest.x, rest.y + 0.15, rest.w, 1.0), kind="key", size=18)

# ============================================================ 마무리
d.summary(["토큰 ID는 **주소**, 임베딩 E(|V|, d)가 학습되는 표 — (B, N) → (B, N, d)",
           "RNN: 같은 규칙으로 **상태 h**를 넘기며 읽는다 — 길이와 무관",
           "장기 의존성의 세 어려움: **학습 신호 · 정보 표현 · 계산 의존성**",
           "LSTM: **덧셈 기억 경로 c**와 게이트로 ① 학습 신호를 완화 — ②③은 남는다",
           "언어 모델 = 다음 토큰 확률의 곱, 임베딩은 이 목표로 **함께 학습** (2003, 2013)",
           "Seq2Seq: 길이가 다른 입출력 — 하지만 **고정 벡터 c 하나**가 병목"])

d.quiz("셀프 체크", [("LSTM 이후에도 남아 있는 핵심 제약은? (원자료 개념 확인 03)", "h_t가 h_(t−1)에 의존하는 순차 계산, 고정 크기 상태에 정보를 담아야 하는 점"),
                   ("어휘 30,000, d = 512인 임베딩 표의 파라미터 수와, ids (4, 20)의 출력 shape은?", "15,360,000개, (4, 20, 512)"),
                   ("W_h = 0.5인 1차원 RNN에서 첫 입력의 흔적이 줄어드는 이유는?", "매 시점 0.5와 tanh를 거치며 곱해지므로 점점 작아진다"),
                   ("LSTM에서 f = 1, i = 0이면 c_t는?", "c_(t−1) 그대로 — 기억을 완전히 보존"),
                   ("Seq2Seq에서 문장이 길수록 번역이 나빠지는 이유는?", "입력 전체를 고정 길이 벡터 c 하나로 압축해야 하기 때문 (병목)")])

d.misconceptions([["“토큰 ID가 크면 의미도 크다”", "ID는 **lookup 주소**일 뿐, 계산에는 학습된 벡터가 들어간다"],
                  ["“임베딩은 Word2Vec에서 처음 나왔다”", "2003 신경 언어 모델 등에서 이미 **함께 학습**되었다"],
                  ["“단어 의미는 임베딩 표에 모두 저장된다”", "lookup과 **문맥 계산**이 함께 표현을 만든다"],
                  ["“LSTM은 긴 문맥을 완벽하게 기억한다”", "학습을 **쉽게** 하는 설계일 뿐, 보장은 없다. 순차 계산도 남는다"],
                  ["“다음 토큰 확률 분해는 RNN의 성질이다”", "확률 모델의 **목표**다. Transformer도 같은 목표를 쓴다"],
                  ["“1997 LSTM에 forget gate가 있었다”", "forget gate는 2000년 Gers et al.이 도입한 후속 형태"]])

d.homework([("복사 · 반전 과제 설계 (원자료 운영안 5회차)", "입력 수열을 그대로/거꾸로 출력하는 데이터셋을 만들고, 길이 5·10·20에서 작은 RNN과 LSTM의 정확도를 비교한다."),
            ("RNN 손계산", "W_x = 1, W_h = 0.9, 입력 (1, 0, 0, 0, 0)에서 h_1…h_5를 계산하고 W_h = 0.5일 때와 비교한다."),
            ("토큰화 비교", "한국어 문장 하나를 글자 단위와 공개 tokenizer 하나로 나눠 보고 토큰 수를 비교한다 (ID 숫자로 품질을 판단하지 않기).")],
           notes="원자료 주의: 실제 tokenizer와 교육용 문자 tokenizer를 명확히 구분해 표시한다.")

d.references([["[06] Elman (1990). Finding Structure in Time. Cognitive Science", "단순 순환망의 구조"],
              ["[08] Bengio, Simard & Frasconi (1994). Learning Long-Term Dependencies with Gradient Descent is Difficult", "도입부"],
              ["[09] Hochreiter & Schmidhuber (1997). Long Short-Term Memory · Gers et al. (2000) forget gate", "셀 구조 그림"],
              ["[11] Bengio et al. (2003). A Neural Probabilistic Language Model · [14] Mikolov et al. (2013) Word2Vec", "모델 구조 그림"],
              ["[15] Sutskever, Vinyals & Le (2014) · [16] Cho et al. (2014)", "Encoder–Decoder 구조, 길이별 성능"]])

d.handoff(["토큰 → 임베딩으로 문장을 숫자로", "RNN · LSTM으로 **순서와 기억**을", "Seq2Seq로 **길이가 다른** 입출력을"],
          ["모든 입력을 **고정 벡터 c 하나**로 압축 (병목)", "h_t는 h_(t−1)이 필요 — **순차 계산**"],
          ["**필요할 때 원문을**", "**다시 찾아보면?**", "Attention (2014) → Self-attention"],
          notes="다음 주: Encoder의 위치별 표현을 남겨 두고, 출력할 때마다 다른 비중으로 다시 참조하는 Attention. 그리고 그것을 모델의 본체로 삼은 Transformer의 핵심 연산.")

d.save(OUT)
print("saved", OUT, d.n + 2, "slides")
