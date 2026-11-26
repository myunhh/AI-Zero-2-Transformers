"""Week 4 — 언어·순서·기억: RNN에서 Seq2Seq까지 — 먼 정보를 기억하려면? (논문 중심 판)

근거: build/research/papers/week4.md (검증된 논문 노트). 새 그림: build/paper_figs_w4.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deckkit  # noqa: E402
deckkit.use_theme("clean")  # Apple 디자인 원칙 테마 — import * 보다 먼저
from deckkit import *  # noqa

A = lambda p: os.path.join(HERE, "assets", p)
OUT = os.path.join(HERE, "..", "lectures", "week04_rnn_lstm_seq2seq.pptx")

d = Deck(4, "언어·순서·기억: RNN에서 Seq2Seq까지", date="2026-10-26", theme="clean")

# ============================================================ 도입
d.question("먼 정보를\n기억하려면?",
           "1990–2016 · Elman · LSTM · Gers · Bengio · Word2Vec · Cho · Sutskever — 논문으로 따라가는 RNN에서 Seq2Seq까지",
           notes="이미지는 격자였지만 언어는 순서다. 문장마다 길이가 다르고, 멀리 떨어진 단어가 서로 의존한다. "
                 "오늘은 이 문제를 푼 논문들을 시간 순서로 읽는다: Elman(1990)의 단순 순환망, Hochreiter(1991)·Bengio(1994)의 장기 의존성 분석, "
                 "LSTM(1997)과 forget gate(2000), 신경망 언어 모델(2003)과 Word2Vec(2013), 그리고 2014년의 Encoder–Decoder 논문 세 편. "
                 "마지막에 고정 벡터 하나로 문장을 요약하는 방식이 남긴 문제(병목 '가설')가 다음 주 Attention의 출발점이다. "
                 "출처: build/research/papers/week4.md 주차 요약 표.")

d.bridge(["CNN: **고정 크기 창**(receptive field)으로 지역 패턴", "가중치 공유 · 깊은 망: ReLU · **Residual** · Norm"],
         ["**언어**는 격자가 아니라 순서, 길이도 제각각", "고정 창 밖의 **먼 단어** 의존 — “그 책은 … (20단어) … 재미있었다”"],
         ["**순서를 어떻게 표현하고,**", "**먼 정보를 어떻게 기억할까?**"],
         notes="3주차 복습: CNN은 고정 크기 창 안에서만 보고, 위치마다 같은 필터를 쓴다(가중치 공유). 깊은 망은 ReLU·Residual·정규화로 학습했다. "
               "남은 문제: 문장은 길이가 제각각이고, 창 밖에 있는 먼 단어가 의미를 정한다. 창을 키우거나 층을 쌓는 대신, "
               "읽은 내용을 '상태'로 들고 다니면 어떨까? — Elman(1990)이 바로 이 질문을 '시간을 어떻게 표현할까'로 던졌다. "
               "출처: Elman (1990) pp.180–181 'The Problem with Time'.")

d.roadmap(["도구: 토큰 · 임베딩 · 부분단어 (Sennrich 2016)", "Elman (1990): 단순 순환망", "장기 의존성: 왜 먼 정보를 잃나 (1991 · 1994 · 2013)",
           "LSTM (1997) → forget gate (2000)", "단어의 의미: 신경망 LM (2003) · Word2Vec (2013)",
           "Encoder–Decoder: Cho · Sutskever · Cho (2014)"],
          ["토큰 ID와 **임베딩 lookup**을 구분하고 BPE 병합을 손으로 해 본다",
           "Elman 망의 context와 RNN 상태 갱신을 **손으로** 계산한다",
           "기울기 소실·폭주의 조건과 **clipping**의 역할을 말한다",
           "1997 LSTM(**CEC**, 게이트 2개)과 2000년 **forget gate**를 구분한다",
           "언어 모델의 목표·perplexity와 Word2Vec의 **유추 평가**를 설명한다",
           "Encoder–Decoder의 결과와 **병목 가설의 근거·반대 증거**를 말한다"])

d.paper_map([
    ("1990", "Elman · Finding Structure in Time", "은닉층을 복사하는 단순 순환망", "시간을 입력 위치로 펼치면 길이 고정·위치 의존"),
    ("1991 · 1994", "Hochreiter · Bengio, Simard & Frasconi", "기울기가 시간을 거슬러 곱해진다", "RNN이 왜 긴 지연을 못 배우나"),
    ("1997", "Hochreiter & Schmidhuber · LSTM", "CEC + 입력·출력 게이트", "지수적 기울기 소실"),
    ("2000", "Gers, Schmidhuber & Cummins", "forget gate", "연속 입력에서 셀 상태가 끝없이 커짐"),
    ("2003", "Bengio et al. · Neural Probabilistic LM", "단어 벡터 + 다음 단어 확률", "n-gram의 차원의 저주"),
    ("2013", "Pascanu, Mikolov & Bengio", "소실·폭주 조건, norm clipping", "기울기 폭주의 실용 해법"),
    ("2013", "Mikolov et al. · Word2Vec", "CBOW · Skip-gram, 유추 평가", "신경망 LM은 너무 느리다"),
    ("2014.06", "Cho et al. · RNN Encoder–Decoder", "가변 길이 ↔ 가변 길이, 게이트 유닛(GRU)", "고정 길이 입출력"),
    ("2014.09", "Sutskever, Vinyals & Le · Seq2Seq", "4층 LSTM, 입력 뒤집기, BLEU 34.81", "SMT 보조가 아닌 순수 신경망 번역"),
    ("2014.09", "Cho et al. · On the Properties of NMT", "긴 문장·미등록어에서 저하 → 병목 가설", "순수 NMT는 어디서 약한가"),
    ("2016", "Sennrich, Haddow & Birch · BPE (도구)", "부분단어 단위", "고정 어휘의 희귀어·UNK"),
], notes="오늘 읽을 논문 지도. 각 논문은 바로 앞 방법의 한계에서 출발한다. Sennrich(2016)는 연대상 Attention 이후 논문이지만, "
         "토큰화라는 '도구'를 설명하려고 Part 1에서 먼저 짧게 본다. 시간 메모: arXiv 기준 Cho(1406.1078, 2014-06) → Bahdanau Attention(1409.0473, 2014-09-01) "
         "→ Cho b(1409.1259) → Sutskever(1409.3215). Seq2Seq와 Attention은 거의 같은 달에 나왔다. 출처: week4.md 주차 요약 표·시간 메모.")

d.glossary([["토큰 · 어휘 |V|", "모델이 처리하는 텍스트 조각과 그 전체 목록", "레고 블록 · 블록 상자"],
            ["임베딩 E", "토큰마다 하나씩 있는 학습되는 벡터 표 (|V|, d)", "사전의 뜻풀이 (숫자판)"],
            ["은닉 상태 h · context", "지금까지 읽은 내용의 요약 (Elman은 이를 context로 복사)", "읽으면서 쓰는 메모"],
            ["장기 의존성", "멀리 떨어진 위치 사이의 관계", "앞 문장의 주어와 뒤의 동사"],
            ["CEC", "자기 연결 1.0으로 오차가 일정하게 흐르는 기억 칸", "새지 않는 물통"],
            ["게이트", "0~1 비중으로 정보 흐름을 조절하는 값 (입력으로 계산됨)", "수도꼭지"],
            ["perplexity", "평균 몇 개 후보 중에서 고르는 셈인지 (낮을수록 좋다)", "객관식 보기 수"],
            ["BLEU", "기계 번역과 정답 번역의 단어열 겹침 점수 (높을수록 좋다)", "답안과 모범답안 겹침"],
            ["Encoder–Decoder", "입력을 요약하는 부분과 출력을 생성하는 부분", "통역사의 듣기와 말하기"]])

# ============================================================ Part 1 (도구)
d.part(1, "도구: 문장을 숫자로", "토큰 · 임베딩 · 부분단어 — 논문이 아닌 도구 (부분단어: Sennrich 2016)",
       notes="도구 Part: 토큰·임베딩은 특정 논문의 결과가 아니라 오늘 모든 논문이 공통으로 쓰는 입력 처리다. 부분단어만 Sennrich et al. (2016) 논문으로 본다(연대상 Attention 이후). 출처: week4.md Sennrich2016 항목.")

s = d.slide("텍스트가 벡터가 되기까지", lead="문자열 → 토큰 → 정수 ID → 학습되는 벡터. 모델이 계산하는 것은 마지막 벡터다", stage="아이디어",
            notes="[도구 Part — 특정 논문의 결과가 아니라 오늘 모든 논문이 공통으로 쓰는 입력 처리] "
                  "문장을 tokenizer(토큰화기)로 토큰으로 자르고, 각 토큰에 사전 번호(ID)를 붙이고, 그 번호로 임베딩 표에서 벡터를 꺼낸다. "
                  "배치 B개 문장, 길이 N이면 ID 텐서는 (B, N), 임베딩 후 (B, N, d). 예시 ID 숫자는 설명용이다. "
                  "오늘 예문 '나는 학교에 간다'는 어절 단위 3토큰으로 통일한다 — 실제 tokenizer는 더 잘게 자른다(부분단어, 뒤의 Sennrich 2016). "
                  "출처: 일반 개념(1주차 텐서 shape와 연결). 임베딩 표를 신경망과 함께 학습하는 아이디어의 출처는 Part 5의 Bengio et al. (2003) §2.")
top, bot = s.area.top(1.6, gap=0.45)
s.flow([{"head": "문자열", "body": "“나는 학교에 간다”"}, {"head": "토큰", "body": "[나는, 학교에, 간다]"},
        {"head": "ID", "body": "[12, 305, 88]\nshape (N,) = (3,)"},
        {"head": "벡터", "body": "E[ID] → (3, d)", "tone": "dark"}], top, body_size=15, head_size=18)
gt = s.table(["단계", "shape (배치 B, 길이 N)", "학습되나?"], [["토큰 ID", "(B, N) — 정수", "아니오 — tokenizer가 정함"],
                                                        ["임베딩 표 E", "(|V|, d)", "**예** — 파라미터"],
                                                        ["임베딩 결과", "(B, N, d)", "E에서 꺼낸 값 (활성값)"]],
             Box(bot.x, bot.y, bot.w, 2.0), widths=[1.6, 2.6, 3.2], size=17)

s = d.slide("번호는 의미가 아니다", lead="ID 100이 ID 10보다 ‘열 배’인 것은 아니다 — ID는 표에서 벡터를 꺼내는 주소", stage="문제",
            notes="[도구] ID를 그대로 숫자로 계산에 넣으면 '305번 학교가 12번 나보다 크다' 같은 엉뚱한 관계가 생긴다. "
                  "one-hot: 어휘 크기 |V|의 벡터에서 자기 위치만 1. one-hot 행벡터에 임베딩 표 E(|V|, d)를 곱하면 E의 해당 행이 그대로 나온다 = 행 lookup. "
                  "실제로는 큰 one-hot을 만들지 않고 행을 바로 꺼낸다. Elman(1990)의 단어 실험도 각 단어를 서로 직교하는 31비트 one-hot으로 넣었다(p.195) — "
                  "그래서 그가 찾은 구조는 입력 모양이 아니라 '순서'에서 나온 것이다(Part 2). 출처: 일반 개념; Elman (1990) pp.195–197.")
L, R = s.cols(0.66)
s.image(A("week4/onehot_lookup.png"), L)
s.bullets(["ID를 그대로 쓰면 크기 관계가 **엉터리**", "**one-hot**: 자기 자리만 1인 벡터", "one-hot @ E = E의 **그 행**",
           ("실제로는 행을 바로 꺼냄 (lookup)", 1), "E (|V|, d)는 **학습되는 파라미터**",
           ("그림은 설명용 작은 어휘 (|V| = 5)", 1)], R)

d.paper("Sennrich et al. (2016)", "Neural Machine Translation of Rare Words with Subword Units",
        "ACL 2016 · arXiv 1508.07909 · Sennrich, Haddow & Birch",
        "번역 모델의 어휘는 3–5만 단어로 고정인데, 이름·합성어·차용어는 끝이 없다. 모르는 단어는 UNK가 된다.",
        "압축 기법 BPE(Gage 1994)를 단어 분할에 적용: 글자에서 시작해 **가장 빈번한 인접 쌍을 반복 병합**. 병합 횟수가 유일한 하이퍼파라미터.",
        "§3.2 (1쪽, Algorithm 1), Table 2의 OOV 열",
        url="arxiv.org/abs/1508.07909",
        result="영→독: 단어+UNK 20.6 → BPE 22.8 BLEU(단일), 미등록어 F1 0.0 → 33.6. 단, 기반 모델은 Attention NMT(2016).",
        notes="Sennrich, Haddow & Birch (2016), ACL. 풀려던 문제: NMT 어휘는 보통 30,000–50,000단어로 고정, 번역은 열린 어휘 문제. 기존 해법은 UNK + 사전 백오프(초록, §1). "
              "아이디어: BPE(Gage 1994)를 단어 분할에 적용(§3.2). 단어 끝 기호 </w>, 단어 경계를 넘는 쌍은 세지 않음, 최종 어휘 = 글자 수 + 병합 횟수. "
              "결과(Table 2, 영→독 newstest2015, 단일/앙상블8): 단어+UNK 20.6/22.8, 단어+사전 22.0/24.2, BPE-60k 21.5/24.5, BPE-J90k 22.8/24.7; OOV unigram F1 UNK 0.0 → BPE-J90k 33.6. "
              "주의: BPE 자체는 Gage(1994)의 압축 기법이고 Sennrich는 이를 NMT 분할에 적용했다. 이 논문의 번역 모델은 attention 기반(Bahdanau et al.)이라 연대상 오늘 논문들보다 뒤다 — '도구'로 먼저 본다.")

s = d.slide("BPE 병합을 손으로", lead="원문 Algorithm 1의 작은 사전 — 가장 자주 붙어 나오는 두 기호를 하나로, 열 번 반복", stage="계산",
            notes="원문 Algorithm 1의 예제 사전: {'l o w </w>': 5, 'l o w e r </w>': 2, 'n e w e s t </w>': 6, 'w i d e s t </w>': 3}. "
                  "인접 쌍의 빈도를 세면 (e, s)는 newest 6 + widest 3 = 9로 최다 → 'es'로 병합. 이어서 (es, t) 9, (est, </w>) 9, (l, o) 7, (lo, w) 7, "
                  "(n, e) 6, (ne, w) 6, (new, est</w>) 6, (low, </w>) 5, (w, i) 3. 10회 후: low</w>, low e r </w>, newest</w>, wi d est</w>. "
                  "동점은 먼저 센 쌍이 선택된다(Python max의 동작). 시험 때는 학습한 병합을 같은 순서로 적용 → 처음 보는 'lower'도 'low' + 'er</w>' 같은 아는 조각으로 나뉜다(원문 예). "
                  "주의: 빈도 기반이라 형태소처럼 쪼개진다는 보장은 없다(예: unhappiness → un + happi + ness는 설명용 예시일 뿐). "
                  "출처: Sennrich et al. (2016) §3.2, Algorithm 1; 손계산은 week4.md에서 검산.")
L, R = s.cols(0.56, gap=0.4)
s.table(["순서", "병합할 쌍", "빈도", "새 기호"],
        [["1", "e + s", "9", "es"], ["2", "es + t", "9", "est"], ["3", "est + </w>", "9", "est</w>"],
         ["4", "l + o", "7", "lo"], ["5", "lo + w", "7", "low"], ["6 · 7", "n + e → ne + w", "6", "new"],
         ["8", "new + est</w>", "6", "newest</w>"], ["9", "low + </w>", "5", "low</w>"], ["10", "w + i", "3", "wi"]],
        L, widths=[0.9, 2.6, 0.9, 1.9], size=15, align="clcl")
cb = s.code("vocab = {'l o w </w>': 5,\n"
            "         'l o w e r </w>': 2,\n"
            "         'n e w e s t </w>': 6,\n"
            "         'w i d e s t </w>': 3}", Box(R.x, R.y, R.w, 1.6), size=15)
s.bullets(["(e, s): newest 6 + widest 3 = **9** → 최다", "10회 후: **low</w>** · low e r </w> · **newest</w>** · wi d **est</w>**",
           "처음 보는 **lower** → low + er</w>", ("UNK 없이 아는 조각으로", 1),
           "==주의== 빈도 기반 — 형태소 분할 보장 없음"], Box(R.x, s.last_code_box.b + 0.25, R.w, R.b - s.last_code_box.b - 0.25), size=16)

# ============================================================ Part 2 Elman
d.part(2, "Elman (1990): 단순 순환망", "시간을 입력의 ‘자리’가 아니라 처리에 미치는 ‘효과’로 표현하면?",
       notes="Elman (1990) 'Finding Structure in Time' — 시간을 입력의 자리로 펼치지 않고, 은닉층을 context로 복사해 처리에 미치는 효과로 표현한다. 출처: Elman (1990) pp.180–184.")

s = d.slide("문제: 시간을 공간으로 펼치면", lead="Elman이 지적한 세 가지 — 버퍼가 필요하고, 길이가 고정되고, 한 칸 밀리면 다른 벡터가 된다",
            stage="문제",
            notes="Elman(1990) 'The Problem with Time'(pp.180–181): 당시 흔한 방법은 시간을 입력 벡터의 위치(공간)로 펼치는 것. "
                  "(1) 입력을 버퍼에 모아 두었다가 한꺼번에 넣어야 하고, (2) 최대 길이가 고정되며, (3) [0111000000]과 [0001110000]처럼 "
                  "같은 패턴이 한 칸 밀리기만 해도 공간적으로 먼 벡터가 된다. 3주차 CNN의 고정 창도 같은 고민의 한 형태다. "
                  "또 토큰 벡터를 더하거나 평균 내면 '개가 사람을 물었다'와 '사람이 개를 물었다'가 구분되지 않는다(순서 정보 소실) — 이것은 강의 예시. "
                  "출처: Elman (1990) pp.180–181.")
top, bot = s.area.top(2.3, gap=0.35)
s.cards([{"head": "① 버퍼가 필요", "body": ["입력을 모아 두었다가 한꺼번에", "→ 언제 처리할지 외부에서 정해야"]},
         {"head": "② 길이가 고정", "body": ["벡터 크기 = 최대 길이", "→ 더 긴 문장은 못 넣는다"]},
         {"head": "③ 위치 의존", "body": ["[0111000000]", "[0001110000]", "→ 같은 패턴인데 먼 벡터"], "tone": "accent"}],
        top, cols=3, body_size=17, head_size=19, fit_h=False)
s.callout("Elman의 제안: 시간을 명시적 입력 차원이 아니라 **처리에 미치는 효과**로 — 지난 처리의 흔적(상태)을 다음 처리에 넘긴다",
          Box(bot.x, bot.y, bot.w, 0.9), kind="key", size=17)
s.callout("강의 예: 단어 벡터를 **평균** 내면 “개가 사람을 물었다” = “사람이 개를 물었다” — 순서가 사라진다",
          Box(bot.x, s.last_callout_box.b + 0.3, bot.w, 0.7), kind="warn", size=15)

d.paper("Elman (1990)", "Finding Structure in Time", "Cognitive Science 14, 179–211",
        "연결주의 모델에서 시간을 어떻게 표현할까 — 시간을 입력 벡터의 자리로 펼치는 방식의 한계.",
        "은닉층 활성값을 한 시점 뒤 **context unit으로 그대로 복사**(1.0 고정, 학습 안 함)하고, context가 다시 은닉층에 들어간다. 과제는 대부분 **다음 입력 예측**.",
        "“Networks with Memory” (pp.182–184), “Discovering lexical classes from word order” (pp.194–201, Fig.7)",
        result="다음 단어 예측만으로 은닉 표현이 명사/동사, 생물/무생물 등으로 군집 (Fig.7).",
        notes="Elman (1990), Cognitive Science 14, 179–211. DOI 10.1207/s15516709cog1402_1. "
              "구조(pp.182–184, Fig.2): 은닉층 활성을 한 단계 뒤 context unit으로 일대일 복사(고정 가중치 1.0, 학습 안 함), context가 은닉층 전체에 입력. "
              "context 초기값 0.5, 활성함수는 0~1 logistic(p.182 각주 2). 주의: RNN을 Elman이 '발명'한 것은 아니다 — 원문 스스로 Jordan(1986) 등 선행 제안을 든다(p.182). "
              "Elman의 기여는 은닉층 복사 context + 예측 과제 + 은닉 표현 분석. 학습은 context를 '복사된 입력'으로 보고 시간 방향으로 오차를 거슬러 보내지 않는다(p.182).")

s = d.slide("아이디어: 은닉층을 context로 복사한다", lead="Jordan은 출력을, Elman은 은닉층을 되먹인다 — 다음 시점의 은닉층은 ‘지난 은닉층’을 함께 본다",
            stage="아이디어",
            notes="Elman Fig.1(Jordan 1986: 출력 → state units)과 Fig.2(Elman: 은닉 → context units)를 나란히 다시 그렸다. "
                  "식으로 쓰면 h(t) = f(W_xh x(t) + W_ch c(t)), c(t) = h(t−1), y(t) = f(W_hy h(t)), f = logistic(원문에는 식 번호가 없다). "
                  "복사 연결은 1.0 고정이라 학습하지 않는다. 학습은 일반 역전파로, context를 그냥 '입력'처럼 취급한다 — 오차를 시간 방향으로 거슬러 전파하지 않는다. "
                  "이 점이 뒤에서 중요하다: LSTM 1997은 이를 'Elman's training procedure'라 부르며 긴 지연 과제에서 실패했다고 보고(Table 1 ELM 행: 성공 0%). "
                  "Jordan(1986) 원문은 미확인이며 Elman Fig.1 설명으로만 확인. 출처: Elman (1990) pp.182–184, Fig.1·Fig.2, 각주 2; LSTM 1997 §5, Table 1.")
L, R = s.cols(0.68, gap=0.3)
s.image(A("week4/paper_elman_fig12.png"), L)
s.bullets(["context(t) = 은닉(t−1) — **복사**", ("가중치 1.0 고정 · 초기값 0.5", 1), "활성함수: 0~1 **logistic**",
           "과제: **다음 입력 예측**", "학습: context를 입력처럼 취급", ("시간 방향 역전파 **없음**", 1),
           "선행: Jordan (1986) — Elman이 처음은 아니다"], R, size=16)

s = d.slide("RNN 상태 갱신을 손으로", lead="같은 규칙을 시점마다 반복 — 현대 표기(tanh)와 Elman 원형(logistic, 초기값 0.5)",
            stage="계산",
            notes="위 그림은 펼친(unrolled) RNN의 현대 표기: h_t = tanh(x_t W_x + h_(t−1) W_h + b), 모든 시점이 같은 W_x, W_h, b를 재사용. "
                  "왼쪽 표(현대 tanh): W_x = 1, W_h = 0.5, b = 0, h_0 = 0, 입력 (1, 0, 0). h1 = tanh(1) = 0.762, h2 = tanh(0.5·0.762) = tanh(0.381) = 0.363, "
                  "h3 = tanh(0.5·0.363) = 0.180 — 첫 입력의 흔적이 점점 옅어진다(Part 3로 연결). "
                  "오른쪽 표(Elman 원형): h_t = σ(2·x_t + 1·c_t − 1), c_1 = 0.5(원문 초기값), 입력 (1, 0, 1). h1 = σ(1.5) = 0.818, h2 = σ(0 + 0.818 − 1) = 0.455, "
                  "h3 = σ(2 + 0.455 − 1) = 0.811. 같은 입력 1인데 앞 문맥에 따라 h가 다르다(0.818 vs 0.811). 가중치 2, 1, −1은 설명용. "
                  "출처: 현대 표기는 일반 관례; Elman (1990) p.182 각주 2(초기값 0.5, logistic). 두 손계산 모두 week4.md에서 검산.")
top, bot = s.area.top(1.9, gap=0.25)
s.image(A("week4/rnn_unrolled.png"), top)
L, R = bot.cols(0.5, gap=0.4)
s.textbox("**현대 표기** h = tanh(x·1 + h·0.5),  첫 h = 0", Box(L.x, L.y, L.w, 0.42), size=15, color=TEAL, gap=0)
s.table(["t", "x", "계산", "h_t"], [["1", "1", "tanh(1 + 0)", "**0.762**"], ["2", "0", "tanh(0.5·0.762)", "**0.363**"],
                                     ["3", "0", "tanh(0.5·0.363)", "**0.180**"]], Box(L.x, L.y + 0.45, L.w, 1.75), size=15,
        widths=[0.6, 0.6, 2.6, 1.2], align="cccc")
s.textbox("**Elman 원형** h = σ(2x + c − 1),  첫 context = 0.5", Box(R.x, R.y, R.w, 0.42), size=15, color=TEAL, gap=0)
s.table(["t", "x", "계산", "h_t"], [["1", "1", "σ(2 + 0.5 − 1)", "**0.818**"], ["2", "0", "σ(0 + 0.818 − 1)", "**0.455**"],
                                     ["3", "1", "σ(2 + 0.455 − 1)", "**0.811**"]], Box(R.x, R.y + 0.45, R.w, 1.75), size=15,
        widths=[0.6, 0.6, 2.6, 1.2], align="cccc")
s.textbox("왼쪽: 첫 입력의 흔적이 **점점 옅어진다** (→ Part 3)   ·   오른쪽: 같은 입력 1도 문맥에 따라 **0.818 vs 0.811**",
          Box(bot.x, bot.y + 2.35, bot.w, 0.5), size=15, color=GRAY, gap=0)

s = d.slide("결과: 다음 단어 예측만으로 품사가 생긴다", lead="단어는 서로 직교하는 one-hot — 그런데 은닉 표현을 군집하면 명사/동사, 생물/무생물이 나뉜다",
            stage="결과",
            notes="Elman의 네 시뮬레이션은 모두 '다음 것 예측'. (1) XOR-in-time: 1-2-1 망, 3,000비트 열 600회 — 예측 가능한 매 셋째 비트에서만 오차가 낮다(Fig.3). "
                  "(2) b→ba, d→dii, g→guuu 글자열: 6-20-6 — 모음 예측 오차는 낮고 자음은 높다(Fig.4). (3) 단어 경계: 1,270단어 = 4,963글자, 5-20-5 — 새 단어 시작에서 오차가 튄다(Fig.6). "
                  "(4) 단어 순서: 13개 범주·29단어·15개 템플릿으로 10,000문장(약 2.7만 단어 — 원문 쪽마다 27,534/27,354/27,454로 다르게 인쇄), 31-150-31, 6회 학습. "
                  "실제 다음 단어 기준 RMS 0.88은 무의미(모두 꺼도 1.0). 가능한 다음 단어들의 확률 벡터와 비교하면 RMS 0.053(SD 0.100), 코사인 0.916(p.198). "
                  "150차원 은닉 활성을 단어별로 평균해 계층 군집하면 그림 같은 구조(Fig.7, p.200). 처음 보는 단어 'zog'를 man 자리에 넣으면 zog의 표현이 man 근처로 간다(Fig.8). "
                  "한계: 단어별 평균 군집이 통계적 인공물일 수 있다는 Plate의 지적(p.199 각주 6) → 토큰 단위로 재확인(p.205). 수치 정밀도와 반복 활성함수에 의한 지수적 감쇠로 기억은 유한(p.204). "
                  "출처: Elman (1990) pp.185–206, Fig.3–8, Table 3·4.")
L, R = s.cols(0.55)
s.image(A("week4/paper_elman_tree.png"), L)
s.table(["실험 (모두 다음 것 예측)", "관찰"],
        [["XOR-in-time (1-2-1)", "예측 가능한 셋째 비트만 오차↓"],
         ["단어 경계 (5-20-5)", "새 단어 시작에서 오차↑"],
         ["단어 순서 (31-150-31)", "가능한 다음 단어와 RMS **0.053**"]],
        Box(R.x, R.y, R.w, 2.0), widths=[2.5, 2.7], size=14)
s.bullets(["입력은 **직교 one-hot** → 구조는 **순서만으로** 학습", "처음 보는 ‘zog’도 man 자리에 쓰면 man 근처로",
           "==한계== 기억이 유한 — 활성함수가 반복되며 **지수적 감쇠** (p.204)"], Box(R.x, R.y + 2.25, R.w, R.h - 2.25), size=15)

s = d.slide("PyTorch: 임베딩 → RNN의 shape", lead="(B, N) 정수 → (B, N, d) 벡터 → 모든 시점의 상태 (B, N, d_h) + 마지막 상태",
            stage="코드",
            notes="[도구] nn.Embedding(10000, 8): 파라미터 10,000 × 8 = 80,000. ids (2, 5) → x (2, 5, 8). 같은 ID는 항상 같은 벡터(문맥 없음). "
                  "nn.RNN(input_size=8, hidden_size=16, batch_first=True): out (2, 5, 16)은 모든 시점의 h, h_n (1, 2, 16)은 마지막 h(층 수 1). "
                  "파라미터 W_x (8×16) + W_h (16×16) + 편향 2개(16 + 16) = 416 — 길이 N과 무관. nn.LSTM은 게이트 4개분이라 1,664(4배). "
                  "주의: nn.RNN은 tanh + 시간 방향 역전파(BPTT)를 쓰는 현대형이다. Elman 원형은 logistic + 시간 방향 역전파 없음. "
                  "출처: PyTorch 문서 관례; 파라미터 수는 week4.md 검산 메모(416, 1,664 모두 확인).")
L, R = s.cols(0.6)
s.code("import torch, torch.nn as nn\n"
       "emb = nn.Embedding(10000, 8)      # |V|=10000, d=8\n"
       "rnn = nn.RNN(input_size=8, hidden_size=16,\n"
       "             batch_first=True)\n"
       "ids = torch.tensor([[12, 7, 305, 9, 88],\n"
       "                    [ 4, 51,  6, 0,  0]])  # 0 = PAD\n"
       "x = emb(ids)                      # (2, 5, 8)\n"
       "out, h_n = rnn(x)\n"
       "print(out.shape, h_n.shape)  # (2,5,16) (1,2,16)\n"
       "print(sum(p.numel() for p in rnn.parameters()))  # 416", L, size=15)
cb = s.last_code_box
s.flow([{"head": "ids (B, N)"}, {"head": "Embedding", "tone": "dark"}, {"head": "x (B, N, d)"},
        {"head": "RNN", "tone": "dark"}, {"head": "out (B, N, d_h)"}],
       Box(L.x, cb.b + 0.3, L.w, 0.75), head_size=14, gap=0.3)
s.bullets(["`emb(ids)` = 표에서 **행 꺼내기**", ("파라미터 |V| × d = 80,000", 1), "`out`: 시점마다의 h → 문맥 표현",
           "`h_n`: 마지막 h → 문장 **요약**", "RNN 파라미터 **416**", ("= 8·16 + 16·16 + 16 + 16, 길이와 무관", 1),
           "nn.LSTM은 4배: **1,664**"], R, size=17)

# ============================================================ Part 3 장기 의존성
d.part(3, "장기 의존성: 왜 먼 정보를 잃나", "Hochreiter (1991) · Bengio et al. (1994) · Pascanu et al. (2013)",
       notes="장기 의존성: Hochreiter (1991, Diplom 논문)와 Bengio et al. (1994)는 원문 미확인 — LSTM 1997 §3.1과 Pascanu et al. (2013) §2를 통해 읽는다. 출처: week4.md.")

d.paper("Hochreiter (1991) · Bengio et al. (1994)", "Untersuchungen zu dynamischen neuronalen Netzen · Learning Long-Term Dependencies with Gradient Descent is Difficult",
        "Diplom 논문 (TU München) · IEEE Trans. Neural Networks 5(2), 157–166",
        "RNN을 경사하강으로 학습하면 왜 긴 시간 간격의 의존을 못 배우나?",
        "두 연구가 독립적으로 분석: 오차가 시간을 거슬러 갈 때 **같은 종류의 인자가 반복해서 곱해져** 지수적으로 소실되거나 폭주한다.",
        "두 원문 모두 이번에 직접 확인하지 못함 → LSTM (1997) §3.1이 요약한 Hochreiter 분석과 Pascanu (2013) §2로 읽는다",
        lead="두 개의 독립된 분석 — 경사하강으로 먼 의존을 배우기는 왜 어려운가",
        notes="[원문 미확인] Hochreiter(1991)는 독일어 Diplom 논문(덱의 '석사 논문'은 근사 표현), Bengio, Simard & Frasconi(1994)는 원문 접근 실패. "
              "그래서 정확한 수치·인용은 쓰지 않는다. 내용은 2차 출처로: LSTM 1997 §3.1.2–3.1.5 'Outline of Hochreiter's Analysis (1991, pp.19–21)', "
              "LSTM 1997 §3.1.3 '(A very similar, more recent analysis was presented by Bengio et al., 1994.)', "
              "Pascanu et al. 2013 초록·§2(소실/폭주 문제는 Bengio et al. 1994에 자세히; Bengio 1994의 유도는 단일 은닉 유닛의 경우만, §2.1). "
              "LSTM 1997 §2.5에 따르면 Bengio 1994는 simulated annealing 등 경사하강 대안과 latch·two-sequence 문제를 시험했다.")

s = d.slide("시간을 거슬러 기울기가 곱해진다", lead="q단계 뒤로 가는 오차 = 인자 f′·w를 q번 곱한 것 — 1보다 작으면 소실, 크면 폭주",
            stage="계산",
            notes="Hochreiter 분석(LSTM 1997 §3.1 경유): 유닛 u에서 q단계 뒤 v까지 가는 오차의 배율은 경로마다 ∏_{m=1..q} f′(net) · w의 합(Eq.3.2). "
                  "모든 m에서 |f′·w| > 1이면 지수적 폭주, < 1이면 지수적 소실(§3.1.3). logistic의 f′ 최대값은 0.25이므로 |w| < 4.0이면 소실 경향. "
                  "큰 초기 가중치나 큰 학습률도 장거리/단거리 오차 비율을 바꾸지 못한다(§3.1.3). "
                  "그림: 인자가 0.9면 0.9^50 ≈ 0.005(소실), 1.1이면 1.1^50 ≈ 117(폭주) — 검산 완료. 3주차에 깊이 방향에서 본 문제가 시간 방향에서 다시 나타난 것. "
                  "Elman 망은 애초에 시간 방향 역전파를 하지 않았고, 원문도 '반복 적용되는 활성함수에 의한 지수적 감쇠'를 기억의 한계로 들었다(p.204). "
                  "출처: Hochreiter & Schmidhuber (1997) §3.1.2–3.1.3, Eq.3.2 (Hochreiter 1991 요약); Elman (1990) p.204.")
L, R = s.cols(0.55)
s.image(A("week4/grad_decay.png"), L)
s.formula("∂오차 / q단계 전 ≈ Π (f′ · w)", Box(R.x, R.y, R.w, 0.8), size=19)
s.bullets(["펼친 RNN = 시간 방향으로 **아주 깊은 망**", "|f′·w| < 1 → **소실**, > 1 → **폭주**",
           ("0.9⁵⁰ ≈ 0.005 · 1.1⁵⁰ ≈ 117", 1), "logistic f′ ≤ **0.25** → |w| < 4면 소실 경향",
           "큰 가중치·학습률로도 **비율은 못 바꾼다**", "3주차 깊이 문제가 **시간 방향**에서 재등장"],
          Box(R.x, R.y + 1.0, R.w, R.h - 1.0), size=16)

s = d.slide("Pascanu et al. (2013): 조건과 clipping", lead="소실·폭주를 고유값으로 정확히 말하고, 폭주는 기울기 ‘크기’만 잘라서 막는다",
            stage="논문",
            notes="Pascanu, Mikolov & Bengio (2013) 'On the difficulty of training Recurrent Neural Networks', ICML 2013, arXiv 1211.5063. "
                  "§2.1: x_k = W_rec σ(x_(k−1)) + W_in u_k + b에서 야코비안 ∂x_(k+1)/∂x_k = W_recᵀ diag(σ′(x_k)). |σ′| ≤ γ일 때 "
                  "W_rec의 최대 고유값 절댓값 λ1 < 1/γ이면 장기 기울기 소실의 충분조건, λ1 > 1/γ는 폭주의 필요조건. tanh는 γ = 1, sigmoid는 γ = 1/4. "
                  "Algorithm 1(§3.2, norm clipping): ‖ĝ‖ ≥ threshold면 ĝ ← threshold·ĝ/‖ĝ‖. Mikolov(2012 박사논문)의 원소별 clipping을 변형한 것이라고 밝힘. "
                  "임계값은 평균 노름 통계로 정하는 휴리스틱, 민감하지 않다고 보고. 손계산: g = (3, 4, 12), ‖g‖ = 13 > 5 → 5/13·g = (1.154, 1.538, 4.615) — 방향 유지, 크기만 5(검산 완료). "
                  "Sutskever et al. (2014) §3.4도 정확히 이 규칙(임계값 5)을 썼다. 주의: clipping은 폭주용이다. 소실에는 정규화 항(§3.3)을 제안했지만 강의에서는 생략 — 소실은 LSTM/게이트 쪽.")
L, R = s.cols(0.5, gap=0.45)
s.formula(["λ₁ < 1/γ  → 소실 (충분조건)", "λ₁ > 1/γ  → 폭주 (필요조건)"], Box(L.x, L.y, L.w, 1.2), size=19)
s.bullets(["λ1: W_rec의 가장 큰 고유값의 크기", "γ: 활성함수 도함수의 최대값", ("tanh γ = 1 · sigmoid γ = 1/4", 1),
           "Bengio (1994)의 유도는 **은닉 유닛 1개**의 경우 (Pascanu §2.1)"], Box(L.x, L.y + 1.4, L.w, L.h - 1.4), size=16)
s.textbox("**Algorithm 1** — norm clipping (임계값 5)", Box(R.x, R.y, R.w, 0.42), size=16, color=TEAL, gap=0)
s.table(["", "값"], [["g", "(3, 4, 12)"], ["‖g‖", "13  > 5"], ["g ← 5 · g / 13", "**(1.154, 1.538, 4.615)**"]],
        Box(R.x, R.y + 0.5, R.w, 1.6), widths=[2.0, 3.0], size=16, align="lc")
s.callout("방향은 그대로, **크기만** 5로. 원소별 clipping은 Mikolov (2012), Sutskever (2014)도 임계값 5 사용.\n"
          "==주의== clipping은 **폭주**용 — 소실은 못 고친다", Box(R.x, R.y + 2.4, R.w, 1.6), kind="warn", size=15)

s = d.slide("장기 의존성이 어려운 이유들", lead="학습 신호 · 정보 표현 · 계산 의존성 — 서로 다른 문제이고, 해결한 논문도 다르다", stage="정리",
            notes="① 학습 신호: 먼 위치까지 기울기가 작아지거나 커진다 → 폭주는 clipping(Mikolov 2012 원소별, Pascanu et al. 2013 노름), 소실은 기억 경로와 게이트(LSTM 1997, Gers 2000). "
                  "② 정보 표현: 고정 크기 상태 h 하나에 필요한 정보를 다 담아야 한다 → Cho et al. 2014b가 '가장 명백한 설명 가설'로 제시, 직접 참조(Attention, 5주차). "
                  "③ 계산 의존성: h_t를 구하려면 h_(t−1)이 먼저 필요 → 병렬화 어려움 → 비순환 구조(Transformer, 6주차). "
                  "출처: Pascanu et al. (2013) §3.2; LSTM 1997 §3–4; Cho et al. (2014b) §5.1. 표의 세 줄은 강의의 정리 틀이다.")
s.table(["어려움", "무엇이 문제인가", "해결 방향 (논문)", "등장"],
        [["① 학습 신호", "먼 위치까지 기울기가 소실·폭주", "폭주: **clipping** (Mikolov 2012 · Pascanu 2013)\n소실: **기억 경로 · 게이트** (LSTM 1997 · 2000)", "**오늘**"],
         ["② 정보 표현", "고정 크기 상태 하나에 모든 정보를 담아야", "병목 **가설** (Cho 2014b) → **직접 참조**", "**Attention** (5주차)"],
         ["③ 계산 의존성", "h_t는 h_(t−1)이 있어야 — 순차 계산", "비순환 · 병렬화 가능한 구조", "**Transformer** (6주차)"]],
        Box(s.area.x, s.area.y, s.area.w, 3.3), widths=[1.7, 3.0, 5.3, 2.3], size=15)
s.callout("이 표가 앞으로 3주의 지도다: ① → LSTM (오늘), ② → Attention, ③ → Transformer",
          Box(s.area.x, s.area.y + 3.6, s.area.w, 0.8), kind="key", size=17)

# ============================================================ Part 4 LSTM
d.part(4, "LSTM (1997) → forget gate (2000)", "오차가 줄지도 커지지도 않고 흐르는 칸을 만들면? 그리고 그 칸은 언제 비우나?",
       notes="LSTM 1997(CEC + 입력·출력 게이트, forget gate 없음)과 Gers et al. 2000(forget gate)을 구분해서 본다. 출처: LSTM 1997 §3.2, §4.1; Gers 2000 §3.")

d.paper("Hochreiter & Schmidhuber (1997)", "Long Short-Term Memory", "Neural Computation 9(8), 1735–1780",
        "BPTT·RTRL로 긴 시간 간격을 학습하면 오차 역류가 부족하고 감쇠해 실패한다 — 최소 지연 10단계만 되어도.",
        "자기 연결 1.0의 **상수 오차 회전목마(CEC)** + 셀을 보호하는 곱셈 **입력 게이트·출력 게이트**. forget gate는 **없다**.",
        "§3.2 (CEC 유도, 2쪽), §4.1–4.2 (memory cell과 게이트의 이유), Table 2",
        result="지연 100단계 과제: RTRL·BPTT 0% vs LSTM 100% (Table 2). 최소 지연 1,000단계까지 성공 (Table 3).",
        notes="Hochreiter & Schmidhuber (1997), Neural Computation 9(8), 1735–1780. DOI 10.1162/neco.1997.9.8.1735. "
              "문제: '불충분하고 감쇠하는 오차 역류'(초록, §1), 표준 방법은 최소 지연 10단계만 되어도 실패(§5 실험 2 개요). "
              "아이디어: CEC(§3.2.1–3.2.2) + 곱셈 입력/출력 게이트(§4.1, Fig.1), 게이트를 공유하는 memory cell block(§4.4). "
              "학습은 RTRL 변형 + 절단(truncated) 기울기: 셀 입력 쪽으로 들어온 오차는 시간 방향으로 더 보내지 않고 CEC 안에서만 거슬러 흐른다(§4.5), 가중치·시간당 O(1)(§4.6). "
              "흔한 오해: '1997 LSTM = f, i, o 세 게이트'는 틀림 — 1997년은 입력·출력 게이트 2개 + 자기 연결 1.0 고정, 상태는 더하기만.")

s = d.slide("아이디어: 상수 오차 회전목마 (CEC)", lead="f′(net) · w = 1이 되게 — 항등 활성 + 자기 연결 1.0. 그리고 칸을 지키는 두 게이트",
            stage="아이디어",
            notes="CEC 유도(§3.2.1): 자기 연결 하나에서 오차가 줄지도 커지지도 않고 흐르려면 f′(net)·w_jj = 1 → f는 항등함수, w_jj = 1.0. "
                  "그런데 CEC만 두면 같은 입력 가중치가 '저장'과 '무시'를, 같은 출력 가중치가 '읽기'와 '방해 막기'를 동시에 맡아 충돌한다(input/output weight conflict, §3.2.2). "
                  "그래서 곱셈 입력 게이트(셀 내용을 무관한 입력으로부터 보호)와 곱셈 출력 게이트(다른 유닛을 셀 내용으로부터 보호)를 붙인다(§4.1, Fig.1). "
                  "원문 식(§4.1): s_c(0) = 0, s_c(t) = s_c(t−1) + y^in(t)·g(net_c(t)), y^c(t) = y^out(t)·h(s_c(t)). 강의 표기로 c_t = c_(t−1) + i_t·g_t — 즉 f ≡ 1. "
                  "손계산(검산 완료): 시점 1에 i = 1, g = 0.8 저장, 이후 세 시점 i = 0 → s = 0.8, 0.8, 0.8, 0.8. 입력 게이트가 닫혀 있으면 값이 그대로 보존되고, ∂s_t/∂s_(t−1) = 1이라 오차도 그대로 흐른다. "
                  "그림은 원문 Fig.1 기반 재구성. 출처: LSTM 1997 §3.2.1–3.2.2, §4.1, Fig.1.")
L, R = s.cols(0.6)
s.image(A("week4/paper_lstm1997.png"), L)
s.bullets(["f′·w = 1 → **항등 + 1.0 고정** = CEC", "CEC만 두면 쓰기·지키기가 **충돌**", ("입력 게이트: 무관한 입력을 막는다", 1),
           ("출력 게이트: 셀 내용이 남을 방해 못 하게", 1)], Box(R.x, R.y, R.w, 2.5), size=16)
s.table(["t", "1", "2", "3", "4"], [["i, g", "1, 0.8", "0, ·", "0, ·", "0, ·"], ["s", "**0.8**", "**0.8**", "**0.8**", "**0.8**"]],
        Box(R.x, R.y + 2.65, R.w, 1.1), widths=[1.0, 1.2, 1.0, 1.0, 1.0], size=15, align="ccccc")
s.textbox("입력 게이트가 닫히면 값이 보존, **∂s_t/∂s_(t−1) = 1**", Box(R.x, R.y + 3.85, R.w, 0.6), size=15, color=GRAY, gap=0)

s = d.slide("결과: 긴 지연 과제에서만 차이가 난다", lead="모두 인공 과제 — 지연이 길어질수록 기존 방법은 0%, LSTM은 학습 시간이 아주 천천히 늘 뿐",
            stage="결과",
            notes="실험 설정(§5): 모두 온라인 학습, logistic, 초기 가중치 [−0.2, 0.2] 또는 [−0.1, 0.1]. 과제: 내장 Reber 문법, 장지연 기호열(2a–2c), Bengio 1994의 two-sequence 문제와 변형, 덧셈·곱셈 문제, 시간 순서 분류. "
                  "Table 1(Reber): RTRL 'some fraction', Elman net(ELM) 0%(>200,000회), RCC 50%; LSTM 97–100%. "
                  "Table 2(과제 2a): p = 10에서 RTRL 0%; p = 100에서 RTRL·BPTT 0%(> 500만 회), 청커 CH 33%, LSTM 100%(5,040회). "
                  "Table 3(과제 2c): 최소 지연 1,000단계까지 성공(q = 1000, p = 1000: 49,000회). Table 7(덧셈): T = 100/500/1000, 2,560개 테스트 중 오답 1/0/1개. "
                  "한계(§6.1): 절단 LSTM은 멀리 떨어진 두 입력의 XOR처럼 부분 목표로 쪼갤 수 없는 과제를 잘 못 푼다; 블록마다 게이트 2개 추가 비용; 정확한 시점 세기(99 vs 100단계 전)는 어렵다. "
                  "주의: '1000단계를 기억한다'는 인공 과제 결과다(자연어에서의 보장 아님). 출처: LSTM 1997 §5, Table 1·2·3·7, §6.1.")
s.table(["과제 (원문 표)", "기존 방법", "LSTM"],
        [["내장 Reber 문법 (Table 1)", "Elman 망 **0%** · RTRL 일부 · RCC 50%", "**97–100%**"],
         ["장지연 기호열, 지연 p = 100 (Table 2)", "RTRL · BPTT **0%** (500만 회 이상)", "**100%** (5,040회)"],
         ["최소 지연 1,000단계 (Table 3)", "—", "성공 (49,000회)"],
         ["덧셈 문제 T = 1000 (Table 7)", "—", "2,560개 중 오답 **1개**"]],
        Box(s.area.x, s.area.y, s.area.w, 2.9), widths=[4.4, 4.7, 3.0], size=16)
L, R = Box(s.area.x, s.area.y + 3.2, s.area.w, s.area.h - 3.2).cols(0.5, gap=0.4)
s.callout("**저자가 밝힌 한계** (§6.1): 멀리 떨어진 두 입력의 XOR처럼 쪼갤 수 없는 과제, 정확한 시점 세기(99 vs 100), 게이트 비용",
          L, kind="tip", size=15)
s.callout("==주의== 모두 **인공 과제**. “LSTM은 1000단계를 기억한다”를 자연어에 대한 보장으로 읽지 않는다",
          R, kind="warn", size=15)

d.paper("Gers et al. (2000)", "Learning to Forget: Continual Prediction with LSTM", "Neural Computation 12(10), 2451–2471 · Gers, Schmidhuber & Cummins",
        "1997 LSTM은 시작·끝이 표시된 시퀀스에선 되지만, **끊김 없는 연속 입력**에선 셀 상태가 한없이 커져 망이 무너진다.",
        "CEC의 고정 자기 연결 1.0을 **학습되는 곱셈 게이트(forget gate)**로 바꾼다. 편향은 양수로 초기화 — 처음엔 1997처럼, 잊는 법을 배운 뒤 잊는다.",
        "§1 둘째 문단 (문제 제기), §3.1 (Eq.6–7), Table 2",
        result="연속 Reber 문법: 표준 LSTM 0% → forget gate 18%, + 학습률 감쇠 62% (Table 2).",
        notes="Gers, Schmidhuber & Cummins (2000), Neural Computation 12(10), 2451–2471. DOI 10.1162/089976600300015015. 읽은 판본: 저자 홈페이지 프리프린트. "
              "문제(초록, §1 p.2): 외부에서 리셋해 줄 교사가 없는 연속 스트림에서 내부 상태가 커진다. "
              "아이디어(§3, p.5): 고정 1.0을 학습되는 게이트 y^φ로 대체, 다른 게이트처럼 sigmoid(0~1). 즉시 리셋뿐 아니라 서서히 잊기도 가능. "
              "forget gate 편향은 양수로 초기화 → 학습 초기에는 y^φ ≈ 1. 중요: forget gate의 원래 동기는 '기울기'가 아니라 '연속 스트림에서 상태 폭주를 막고 자원을 재사용'하는 것.")

s = d.slide("문제와 아이디어: 잊지 못하면 상태가 커진다", lead="매 시점 0.25씩 들어오는 스트림 — 더하기만 하면 100단계 뒤 25, f = 0.9면 2.5에서 멈춘다",
            stage="아이디어",
            notes="손계산(검산 완료): 매 시점 i·g = 0.25가 들어오는 스트림 100단계. f ≡ 1(1997): c = 25.0으로 계속 증가. f = 0.9: c → 0.25/(1 − 0.9) = 2.5에 수렴(100단계 후 2.4999). "
                  "상태가 커지면 출력 squashing h(s)가 포화되어 셀이 쓸모없어진다 — 그래서 외부 리셋 없이 스스로 비울 수단이 필요. "
                  "Eq.6–7(§3.1): net_φ(t) = Σ w_φm y^m(t−1), y^φ(t) = f_φ(net_φ(t)), s_c(t) = y^φ(t)·s_c(t−1) + y^in(t)·g(net_c(t)). "
                  "강의 표기 c_t = f_t ⊙ c_(t−1) + i_t ⊙ g_t. 고정 상태 감쇠(자기 가중치 0.9)도 시험했지만 원칙이 없고 실험적으로도 도움이 안 됐다(p.5, Table 2) — 핵심은 '학습되는' 게이트. "
                  "출처: Gers et al. (2000) 초록, §1, §3.1 Eq.6–7, p.5; 그림은 week4.md 손계산을 그린 것.")
L, R = s.cols(0.55)
s.image(A("week4/paper_gers_growth.png"), L)
s.image(A("week4/paper_lstm2000.png"), Box(R.x, R.y, R.w, 2.7))
s.bullets(["고정 1.0 → **학습되는 게이트 y^φ**", "편향 **양수 초기화**: 처음엔 1997처럼", "원래 동기: 기울기가 아니라",
           ("연속 스트림에서 **상태 폭주**를 막고 셀을 재사용", 1)], Box(R.x, R.y + 2.9, R.w, R.h - 2.9), size=16)

s = d.slide("결과: 연속 스트림에서 forget gate만 풀었다", lead="경계 표시 없이 이어 붙인 Reber 문자열 — 리셋해 주지 않으면 표준 LSTM은 0%",
            stage="결과",
            notes="실험(§4.2 p.10–11): 연속 내장 Reber 문법(CERG) — Reber 문자열을 경계 표시 없이 이어 붙인 스트림. 오답 하나 또는 10^5번째 기호에서 스트림 종료. "
                  "7입력-7출력, 메모리 블록 4개 × 셀 2개, 조정 가능한 가중치 424개. Table 2(p.12, 각 100회 독립 학습, 완벽 해 비율): "
                  "외부 리셋을 준 표준 LSTM 74%, 표준 LSTM(리셋 없음) 0%, 상태 감쇠(자기 가중치 0.9) 0%, forget gate 18%, + 학습률 감쇠 62%. "
                  "BPTT 등은 비연속 ERG에서도 실패해 비교에서 제외. 외부 리셋은 '정답 경계를 알려 주는' 특혜라 공정한 비교 대상은 0% 쪽이다. "
                  "이후 Graves 계열 LSTM이 여기에 peephole 등을 더한 형태가 표준이 되었다(Sutskever 2014 §2: 'We use the LSTM formulation from Graves'). "
                  "출처: Gers et al. (2000) §4.2, Table 2.")
L, R = s.cols(0.6)
s.image(A("week4/paper_gers_table2.png"), L)
s.bullets(["외부 리셋 74%는 **경계를 알려 준** 특혜", "공정한 비교: 리셋 없음 **0%** vs forget **18% → 62%**",
           "고정 감쇠 0.9는 **0%** — 핵심은 ‘학습되는’ 게이트", "이후 Graves 계열 형태가 표준으로", ("Sutskever (2014)도 이 형식을 사용", 1)], R, size=16)

s = d.slide("오늘날의 표준형: 게이트 셋", lead="1997의 입력·출력 게이트 + 2000의 forget gate — 모두 같은 입력 [h_(t−1), x_t]에서 계산",
            stage="계산",
            notes="이 그림과 식은 1997 원형이 아니라 forget gate(Gers 2000)를 포함하고 이후 널리 쓰이게 된 '후일 표준형'이다(Graves 계열은 peephole 등 차이가 있다). "
                  "f, i, o는 sigmoid라 0~1(비중), g는 tanh라 −1~1(새로 쓸 후보 값). 게이트는 사람이 정한 스위치가 아니라 입력과 이전 상태로 매번 계산된다. "
                  "대응: 1997 원형 = 이 식에서 f ≡ 1로 고정. c(내부 기억)와 h(밖으로 내보내는 상태)를 구분하는 것이 핵심. 3주차 Residual의 '더하는 지름길'과 닮았다. "
                  "출처: LSTM 1997 §4.1(입력·출력 게이트, 셀 식), Gers et al. (2000) §3.1 Eq.6–7(forget gate); 표기는 강의 통일 표기.")
L, R = s.cols(0.58)
s.image(A("week4/lstm_cell.png"), L)
s.formula(["f = σ([h, x] W_f + b_f)   ← 2000", "i = σ([h, x] W_i + b_i)   ← 1997",
           "o = σ([h, x] W_o + b_o)   ← 1997", "g = tanh([h, x] W_g + b_g) ← 1997"], Box(R.x, R.y, R.w, 2.1), size=17)
s.bullets(["게이트는 스위치가 아니라 **매번 계산**되는 값", "1997 원형 = 이 식에서 **f ≡ 1**",
           "c: 내부 기억 · h: 밖으로 내보내는 상태", ("3주차 Residual의 지름길과 닮았다", 1)],
          Box(R.x, R.y + 2.3, R.w, R.h - 2.3), size=16)

s = d.slide("셀 갱신을 손으로", lead="f = 0.9면 기억이 거의 그대로, f = 0.5면 절반 — c가 한 단계 거슬러 갈 때 곱해지는 것은 f 하나",
            stage="계산",
            notes="예: 이전 기억 c = 2.0, f = 0.9, i = 0.1, g = 0.5 → c_t = 0.9·2.0 + 0.1·0.5 = 1.85. o = 0.5 → h_t = 0.5·tanh(1.85) = 0.5·0.952 = 0.476. "
                  "f = 0.5였다면 c_t = 1.0 + 0.05 = 1.05, h_t = 0.391 — 기억이 절반으로. ⊙는 원소별 곱. (모두 검산 완료) "
                  "기울기: ∂c_t/∂c_(t−1) = f. 1997 원형은 f ≡ 1이라 이 값이 정확히 1 — 그것이 CEC의 원래 논리(§3.2.1). "
                  "2000년 forget gate는 이 1을 학습되는 값으로 바꿨다 — 동기는 연속 스트림의 상태 폭주였지, 기울기 개선이 아니었다. "
                  "출처: Gers et al. (2000) Eq.7 (강의 표기); LSTM 1997 §3.2.1; 손계산은 week4.md 검산 메모.")
top, bot = s.area.top(0.9, gap=0.3)
s.formula("c_t = f ⊙ c_(t−1) + i ⊙ g        h_t = o ⊙ tanh(c_t)", top, size=22)
L, R = bot.cols(0.6, gap=0.4)
s.table(["", "f = 0.9 (보존)", "f = 0.5"], [["c_(t−1)", "2.0", "2.0"], ["i, g", "0.1, 0.5", "0.1, 0.5"],
                                          ["c_t = f·c_(t−1) + i·g", "1.8 + 0.05 = **1.85**", "1.0 + 0.05 = **1.05**"],
                                          ["h_t = 0.5·tanh(c_t)", "**0.476**", "0.391"]], L, size=15, align="lcc", highlight=[2],
        widths=[2.8, 2.1, 2.1])
s.bullets(["∂c_t / ∂c_(t−1) = **f**", ("f ≈ 1 → 기억도 기울기도 오래 유지", 1), "1997 원형: f ≡ 1 → 정확히 **1** (CEC)",
           "2000: 이 1을 **학습되는 값**으로", ("동기는 상태 폭주 방지", 1), "RNN은 매번 W_h·tanh′를 곱했다"], R, size=16)

s = d.slide("LSTM이 해결한 것과 남은 것", lead="장기 의존성을 ‘학습하기 쉽게’ 만들었다 — 완벽한 기억도, 병렬 계산도 아니다", stage="정리",
            notes="해결: ① 학습 신호 — CEC의 덧셈 경로로 긴 지연 인공 과제에서 기존 방법이 0%인 곳을 풀었다(LSTM 1997 Table 2·3). "
                  "이후 2000년대 후반~2014년에 음성·필기·번역 등에서 널리 쓰였고, 번역에서는 Sutskever et al.(2014)가 4층 LSTM을 썼다(이번 주 원문으로 확인되는 것은 Sutskever). "
                  "남은 것: ② 정보 표현 — 여전히 고정 크기 c, h. ③ 계산 의존성 — h_t는 h_(t−1)이 있어야 계산된다. "
                  "GRU: Cho et al.(2014a)의 게이트 유닛(reset·update 2개)을 이후 문헌이 'gated recurrent unit'이라 불렀다 — 원 논문에 GRU라는 이름은 없다(Part 6). "
                  "출처: LSTM 1997 §5–6; Sutskever et al. (2014) §2; Cho et al. (2014a) §2.3, 각주 1.")
top, bot = s.area.top(3.0, gap=0.3)
s.cards([{"head": "해결한 것", "bullets": True,
          "body": ["① **학습 신호**: 덧셈 경로(CEC)로 긴 지연 학습", "인공 과제에서 기존 0% → LSTM 100%", "번역에도 쓰임 (Sutskever 2014, 4층 LSTM)"]},
         {"head": "남은 것", "tone": "accent", "bullets": True,
          "body": ["② **고정 크기** 상태 c, h에 모든 것을", "③ h_t는 h_(t−1)이 필요 — **순차 계산**",
                   "완벽한 기억을 **보장하지 않는다**"]}], top, cols=2, body_size=18, head_size=20, fit_h=False)
s.callout("더 단순한 게이트 유닛(reset·update 2개)은 Cho et al. (2014a)에서 — 후에 GRU라 불림. 같은 남은 문제를 공유한다.",
          Box(bot.x, bot.y, bot.w, 0.8), kind="tip", size=16)

# ============================================================ Part 5 의미
d.part(5, "단어의 의미: 다음 단어를 맞히다 보면", "Bengio et al. (2003) 신경망 언어 모델 · Mikolov et al. (2013) Word2Vec",
       notes="Bengio et al. (2003) 신경망 언어 모델과 Mikolov et al. (2013a) Word2Vec — 다음 단어(또는 주변 단어) 예측으로 단어 벡터를 학습한다. 출처: Bengio 2003 §2; Mikolov 2013a §3.")

d.paper("Bengio et al. (2003)", "A Neural Probabilistic Language Model", "JMLR 3, 1137–1155 · Bengio, Ducharme, Vincent & Jauvin",
        "**차원의 저주**: 시험 문장은 학습 문장과 대부분 다르다. n-gram은 짧은 조각을 이어 붙일 뿐, 문맥이 짧고 단어 간 유사성을 못 쓴다.",
        "각 단어에 실수 벡터 C(i)를 주고, 앞 n−1개 단어 벡터로 다음 단어 확률을 내는 신경망 g를 **C와 함께** 학습. 비슷한 단어 → 비슷한 벡터 → 본 적 없는 문장도 높은 확률.",
        "§1.1 (차원의 저주와 분산 표현), §2 (Fig.1, Eq.1), Table 1",
        result="Brown 시험 perplexity 252 vs 최고 n-gram 312 (약 24% 개선, 저자 표현).",
        notes="Bengio, Ducharme, Vincent & Jauvin (2003), JMLR 3, 1137–1155. (NIPS 2000 학회판이 먼저 있음 — 원문 미확인.) "
              "문제(초록, §1): 단어열 결합분포 학습의 차원의 저주. 아이디어(§2): C(|V|×m, 자유 파라미터)와 g를 함께 최대우도로 학습. "
              "주의 1: 이 모델은 RNN이 아니라 고정 창(n−1개) MLP다 — 저자는 g가 순환망일 수도 있다고 언급만(§2). "
              "주의 2: '임베딩은 Word2Vec에서 처음'은 틀렸지만 '2003이 최초'도 아니다. Bengio 2003 스스로 Hinton(1986), Elman(1990)을 분산 표현의 선구로, "
              "Miikkulainen & Dyer(1991), Xu & Rudnicky(2000)를 신경망 언어 모델의 선행으로 든다(§1.2). 기여는 대규모 확률적 언어 모델로 n-gram을 능가한 것.")

s = d.slide("목표: 문장 = 조건부 확률의 곱", lead="P(문장) = P(첫 단어) × P(둘째 | 첫째) × … — 그 평균적인 ‘헷갈림’이 perplexity",
            stage="계산",
            notes="확률의 연쇄법칙: 문장 전체 확률 = 앞 토큰들이 주어졌을 때 다음 토큰 확률의 곱. Bengio 2003은 이를 앞 n−1개로 근사해 P̂(w_t | w_(t−1), …, w_(t−n+1))을 학습. "
                  "예(검산 완료): P(나는) = 0.2, P(학교에|나는) = 0.3, P(간다|나는 학교에) = 0.5 → 0.03. −log로 쓰면 3.51(2주차 cross-entropy의 합). "
                  "perplexity = exp(−(1/3) Σ log p) = 3.22 — '평균 3.2개 후보 중 고르는 정도'. 낮을수록 좋다. Bengio Table 1의 252는 '평균 252개 후보 중 고르는 셈'. "
                  "텍스트만 있으면 (앞부분 → 다음 토큰) 정답 쌍을 저절로 만들 수 있다 — 자기지도학습. "
                  "주의: 이 확률 분해는 RNN만의 성질이 아니다. 목표(확률 분해)와 아키텍처(MLP, RNN, Transformer)를 분리해서 본다. "
                  "출처: Bengio et al. (2003) §2 Eq.1 앞의 확률 분해, §4 perplexity 정의; 숫자는 강의 예시.")
top, bot = s.area.top(0.95, gap=0.3)
s.formula("P(w_1, …, w_T) = Π_t  P(w_t | w_<t)", top, size=24)
L, R = bot.cols(0.54, gap=0.4)
s.table(["항", "확률 (예시)"], [["P(나는)", "0.2"], ["P(학교에 | 나는)", "0.3"], ["P(간다 | 나는 학교에)", "0.5"],
                              ["곱 = P(문장)", "**0.03**  (−log = 3.51)"], ["perplexity = e^(3.51/3)", "**3.22**"]],
        Box(L.x, L.y, L.w, 2.6), size=16, align="lc", highlight=[4])
s.bullets(["정답 쌍이 텍스트에서 **저절로** → 자기지도학습", "−log 합 = 2주차 **cross-entropy**",
           "perplexity 3.22 ≈ 평균 **3.2개 후보** 중 고르기", ("낮을수록 좋다 — Table 1의 252와 비교", 1),
           "==주의== 목표(확률 분해) ≠ 아키텍처", ("MLP · RNN · Transformer 모두 같은 목표", 1)], R, size=16)

s = d.slide("구조와 결과: 고정 창 MLP가 n-gram을 이겼다", lead="y = b + Wx + U tanh(d + Hx),  x = 앞 n−1개 단어 벡터를 이어 붙인 것 — 계산의 대부분은 출력층",
            stage="결과",
            notes="Eq.1(§2): P̂(w_t | …) = softmax(y), y = b + W x + U tanh(d + H x), x = (C(w_(t−1)), …, C(w_(t−n+1))). W = 0이면 직접 연결 없음. "
                  "강의 표기: ids (B, n−1) → E[ids] (B, n−1, d) → reshape (B, (n−1)d) → tanh 은닉 → softmax |V|. C = nn.Embedding. "
                  "파라미터(검산 완료): |V| = 16,383, n = 5, m = 30, h = 100, 직접 연결 없음 → C 491,490 + H 12,000 + d 100 + U 1,638,300 + b 16,383 = 2,158,273(약 216만, 출력층 U가 76%). "
                  "실험(§4): Brown 1,181,041단어(학습 80만/검증 20만/시험 181,041), |V| = 16,383. Table 1: MLP10(n = 5, h = 100, m = 30, trigram과 혼합) 252, 혼합 없는 MLP9 276; "
                  "최고 n-gram(class-based back-off) 312, Kneser-Ney 5-gram 321, 보간 trigram 336 → 저자 표현 약 24%. "
                  "Table 2(AP News 약 1,400만 단어): MLP10 109 vs KN 5-gram 117 → 저자 표현 약 8%(직접 계산하면 7.3%). AP는 40 CPU로 약 3주에 5 epoch. "
                  "한계(§5.1): 계산 대부분이 출력 softmax(|V|×h) — 이것이 Word2Vec의 출발점. 출처: Bengio et al. (2003) §2 Eq.1, §4, Table 1·2, §5.")
L, R = s.cols(0.47, gap=0.4)
s.flow([{"head": "앞 n−1개\n단어 ID"}, {"head": "C 표\nm = 30"},
        {"head": "tanh\nh = 100"}, {"head": "softmax\n|V|", "tone": "dark"}],
       Box(L.x, L.y, L.w, 1.0), head_size=15, gap=0.25)
s.table(["파라미터", "개수"], [["C (단어 벡터)", "491,490"], ["H, d (은닉)", "12,100"], ["U (출력층 가중치)", "**1,638,300  (76%)**"],
                             ["b (출력 편향)", "16,383"], ["합계", "**2,158,273**"]], Box(L.x, L.y + 1.3, L.w, 2.2), size=15, align="lr", highlight=[2])
s.textbox("C = Part 1의 **nn.Embedding** · 순환 없음 (고정 창 MLP)", Box(L.x, L.y + 3.7, L.w, 0.5), size=15, color=GRAY, gap=0)
s.image(A("week4/paper_bengio_ppl.png"), R)

d.paper("Mikolov et al. (2013a)", "Efficient Estimation of Word Representations in Vector Space", "ICLR 2013 Workshop · arXiv 1301.3781",
        "신경망 LM으로 단어 벡터를 얻기엔 너무 비싸다 (RNNLM 하나에 CPU 8주). 계산 대부분이 비선형 은닉층과 출력층에 있다.",
        "은닉층을 없앤 **log-linear** 모델 두 가지 — CBOW(주변 → 가운데), Skip-gram(가운데 → 주변) — 와 계층적 softmax로 **수십억 단어**를 학습.",
        "§3 (두 모델, 1쪽), §4.1 (유추 테스트셋과 채점), Table 3",
        url="arxiv.org/abs/1301.3781",
        result="유추 정확도: Skip-gram 1000차원 · 60억 단어 65.6% (Table 6).",
        notes="Mikolov, Chen, Corrado & Dean (2013), ICLR Workshop, arXiv 1301.3781. 문제: RNNLM 하나에 단일 CPU 8주(§4.3), 계산 대부분이 비선형 은닉층(§2.1–2.2). "
              "아이디어(§3, Fig.1): 비선형 은닉층을 없앤 log-linear 모델, 출력은 계층적 softmax(Huffman 트리)로 log2(V)만 계산. "
              "주의: 'Word2Vec = negative sampling'이 아니다 — 1301.3781은 계층적 softmax, negative sampling은 후속 Mikolov et al. (2013b, NIPS, 1310.4546). "
              "또 '딥러닝'이라기보다 은닉층을 없앤 '얕은' 모델이 핵심이다.")

s = d.slide("아이디어: CBOW와 Skip-gram", lead="은닉층을 빼고 예제당 비용을 줄인다 — CBOW Q = N×D + D×log2(V)  vs  NNLM의 N×D×H + H×V",
            stage="아이디어",
            notes="CBOW(§3.1): 앞 4개 + 뒤 4개 단어 벡터의 평균으로 가운데 단어를 분류 — 순서 무시(bag-of-words). "
                  "Skip-gram(§3.2): 가운데 단어로 앞뒤 범위 R(1~C에서 무작위, C = 10) 안의 단어를 각각 분류 — 먼 단어는 덜 뽑힌다. "
                  "예제당 학습 비용: NNLM Q = N×D + N×D×H + H×V(Eq.2), CBOW Q = N×D + D×log2(V)(Eq.4), Skip-gram Q = C×(D + D×log2(V))(Eq.5). "
                  "대입 예(검산 완료, 원문 수치 아닌 자릿수 비교용): V = 10^6, D = 300, N = 8 → CBOW ≈ 8,379, Skip-gram(C = 10) ≈ 62,795; "
                  "NNLM(N = 10, D = H = 500, 전체 softmax) ≈ 5.0×10^8. 후속 2013b: negative sampling — 실제 문맥 단어 1개와 잡음 단어 k개(작은 데이터 5–20, 큰 데이터 2–5)를 로지스틱 회귀로 구분(Eq.4), "
                  "잡음 분포는 유니그램^(3/4), 빈도 높은 단어 subsampling(Eq.5). 그림은 원문 Fig.1 기반 재구성. "
                  "출처: Mikolov et al. (2013a) §2–3, Eq.2·4·5, Fig.1; Mikolov et al. (2013b) §2.2, Eq.4–5.")
top, bot = s.area.top(3.3, gap=0.25)
s.image(A("week4/paper_w2v_arch.png"), top)
s.table(["모델 (V = 10⁶, D = 300)", "예제당 비용 Q (원문 식에 대입)"],
        [["CBOW (N = 8)", "≈ **8,379**"], ["Skip-gram (C = 10)", "≈ **62,795**"], ["NNLM (N = 10, D = H = 500, 전체 softmax)", "≈ 5.0 × 10⁸"]],
        Box(bot.x, bot.y, 7.4, bot.h), widths=[4.3, 3.1], size=14, align="lr")
s.callout("후속 2013b: **negative sampling** — 진짜 문맥 1개 vs 가짜 k개를 구분 (전체 softmax 대신)",
          Box(bot.x + 7.7, bot.y, bot.w - 7.7, bot.h), kind="tip", size=14)

s = d.slide("결과: 유추 테스트와 그 채점", lead="b − a + c에 가장 가까운 단어가 정답과 ‘정확히’ 같아야 정답 — 질문 단어 셋은 후보에서 뺀다",
            stage="결과",
            notes="테스트셋(§4.1, Table 1): 의미 5종(수도-나라, 통화, 도시-주, 남-여 등) 8,869문항, 문법 9종(비교급, 최상급, 과거형, 복수형 등) 10,675문항. "
                  "채점: X = vec(b) − vec(a) + vec(c)에 코사인으로 가장 가까운 단어(질문 단어 자신은 제외 — 'we discard the input question words')가 정확히 일치할 때만 정답(동의어도 오답). "
                  "Table 3(같은 데이터 3.2억 단어, 640차원): 의미/문법 RNNLM 9/36, NNLM 23/53, CBOW 24/64, Skip-gram 55/59. "
                  "Table 6(DistBelief): Skip-gram 1000차원·60억 단어 65.6%(2.5일 × 125 코어), CBOW 63.7%, NNLM 100차원 50.8%(14일 × 180 코어). Table 2: 차원과 데이터를 함께 늘려야 한다. "
                  "흔한 오해: king − man + woman ≈ queen은 이 논문의 결과가 아니라 Mikolov, Yih & Zweig(2013, NAACL)의 결과로 인용된 것(§1.1 [20]). 본문 예시는 France − Paris + Italy = Rome 등(Table 8). "
                  "질문 단어를 제외하지 않으면 답이 king 자신이 되는 경우가 많다는 후속 비판이 있다(일반적으로 알려진 내용, 원문 미확인). "
                  "왼쪽 그림은 설명용 2D 그림이지 실제 학습 벡터의 투영이 아니다. 한계(§4.1, §5): 형태 정보가 없어 100%는 불가능, Table 8 예시도 약 60%. "
                  "출처: Mikolov et al. (2013a) §1.1, §4.1, Table 1·2·3·6·8.")
L, R = s.cols(0.4, gap=0.35)
s.image(A("week4/analogy.png"), Box(L.x, L.y, L.w, 3.2))
s.textbox(["설명용 2D 그림 (실제 벡터 아님)", "king/queen 예: Mikolov, Yih & Zweig (2013) — 이 논문은 **인용**",
           "본문 예: France − Paris + Italy = **Rome**"], Box(L.x, L.y + 3.3, L.w, L.h - 3.3), size=14, color=GRAY, gap=0.15)
s.image(A("week4/paper_w2v_table3.png"), Box(R.x, R.y, R.w, 3.6))
s.bullets(["문항: 의미 **8,869** + 문법 **10,675** · 동의어도 오답", "최고: Skip-gram 1000차원 · 60억 단어 **65.6%** (Table 6)"],
          Box(R.x, R.y + 3.75, R.w, R.h - 3.75), size=15)

# ============================================================ Part 6 Encoder–Decoder
d.part(6, "Encoder–Decoder: 길이가 다른 입력과 출력", "Cho et al. (2014a) · Sutskever et al. (2014) · Cho et al. (2014b)",
       notes="2014년의 세 논문: Cho 2014a(Encoder–Decoder, 게이트 유닛, SMT 구문쌍 재점수화), Sutskever 2014(4층 LSTM, 뒤집기, BLEU 34.81), Cho 2014b(길이 분석 → 병목 가설). 출처: 1406.1078, 1409.3215, 1409.1259.")

d.paper("Cho et al. (2014a)", "Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation",
        "EMNLP 2014 · arXiv 1406.1078 · Cho, van Merriënboer, Gulcehre, Bahdanau, Bougares, Schwenk & Bengio",
        "기존 신경망 번역 보조 모델은 입력·출력 길이가 고정(예: 7단어). 가변 길이 → 가변 길이를 다루는 일반 모델이 필요.",
        "인코더 RNN이 끝까지 읽은 요약 **c**, 디코더가 **매 시점 c에 조건화**해 생성. 새 **게이트 은닉 유닛**(reset · update). 쓰임새는 SMT 구문쌍 **점수 매기기**.",
        "§2.2–2.3 (1쪽), Table 1",
        url="arxiv.org/abs/1406.1078",
        result="Moses 구문표 재점수화: 시험 BLEU 33.30 → 34.64 (+CSLM+RNN). 직접 번역은 하지 않음.",
        notes="Cho et al. (2014a), EMNLP 2014, arXiv 1406.1078. 문제(§2.2, §3.2): Schwenk(2012) 등 기존 모델은 고정 길이. "
              "아이디어(§2.2): h⟨t⟩ = f(h⟨t−1⟩, y_(t−1), c), P(y_t | y_(t−1), …, y_1, c) = g(h⟨t⟩, y_(t−1), c), 목표 max (1/N) Σ log p_θ(y_n | x_n)(Eq.4). "
              "쓰임새(§3.1): 번역을 직접 생성하지 않고, SMT(Moses) 구문표의 각 구문쌍에 점수를 추가 특징으로 매김. "
              "실험(§4.1.1): WMT'14 영→불, 3.48억 단어, 어휘 각 15,000, 은닉 1,000, 임베딩 100차원, 약 3일 학습. "
              "Table 1(BLEU dev/test): Moses 30.64/33.30, +RNN 31.20/33.87, +CSLM+RNN 31.48/34.64, +WP 31.50/34.54. "
              "흔한 오해: (1) 긴 문장 성능 저하는 이 논문이 아니라 Cho et al. 2014b(1409.1259)의 결과. (2) 순수 신경망 번역기가 아니라 SMT 보조. "
              "(3) 'GRU'라는 이름은 이 논문에 없다. (4) 최초의 Encoder–Decoder도 아니다 — 저자 스스로 Kalchbrenner & Blunsom(2013)을 가장 가까운 선행으로 든다(§3.2).")

s = d.slide("아이디어: 요약 벡터를 어떻게 넘기나", lead="Cho는 c를 디코더의 매 시점에, Sutskever는 v로 디코더를 초기화만 — 둘 다 고정 길이 벡터 하나",
            stage="아이디어",
            notes="Cho et al. (2014a) §2.2: 디코더의 은닉 상태와 출력 모두 매 시점 c에 조건화 — h⟨t⟩ = f(h⟨t−1⟩, y_(t−1), c). "
                  "Sutskever et al. (2014) Eq.1 앞: 'the initial hidden state is set to v' — 인코더 마지막 은닉 상태 v로 디코더 LSTM을 초기화만 하고, 입력은 뒤집어서 넣는다. "
                  "공통점: 입력 문장 전체가 고정 길이 벡터 하나(c 또는 v)로 압축된다. 디코더는 BOS(여기서는 <s>)에서 시작해 직전 출력을 다음 입력으로 넣고, EOS가 나오면 멈춘다 — 출력 길이를 스스로 정한다. "
                  "Encoder–Decoder는 특정 신경망 종류가 아니라 '입력 표현'과 '출력 생성'의 역할 분담이다 — Transformer도 이 구조를 쓴다(6주차). "
                  "그림은 Cho Fig.1과 Sutskever Fig.1(A B C → W X Y Z) 기반 재구성. 출처: Cho et al. (2014a) §2.2; Sutskever et al. (2014) §2, Eq.1, Fig.1.")
L, R = s.cols(0.68)
s.image(A("week4/paper_encdec_compare.png"), L)
s.bullets(["공통: 입력 전체 → **고정 길이** 벡터 하나", "Cho: c가 디코더 **매 시점**의 입력", "Sutskever: v는 **초기 상태**로만",
           "디코더: 직전 출력 → 다음 입력", ("**EOS**가 나오면 멈춤 — 길이를 스스로", 1), "Encoder–Decoder = **역할 분담**"], R, size=16)

s = d.slide("계산: 게이트 은닉 유닛 (후에 GRU)", lead="h = z ⊙ h_prev + (1 − z) ⊙ h̃ — z 하나가 ‘유지’와 ‘교체’를 나눈다 (Cho 2014a Eq.7)",
            stage="계산",
            notes="Cho et al. (2014a) §2.3 Eq.5–8(유닛 j별): r = σ(W_r x + U_r h⟨t−1⟩), z = σ(W_z x + U_z h⟨t−1⟩), h⟨t⟩ = z·h⟨t−1⟩ + (1 − z)·h̃⟨t⟩, h̃ = φ(W x + U(r ⊙ h⟨t−1⟩)). "
                  "해석: r ≈ 0이면 이전 상태를 무시하고 현재 입력으로 리셋, z가 이전 상태를 얼마나 가져갈지 결정 — 'LSTM의 memory cell과 비슷하게', leaky integration의 적응형 변형. "
                  "짧은 의존을 잡는 유닛은 r이 자주 활성, 긴 의존을 잡는 유닛은 z가 대부분 활성. 게이트 없는 tanh 유닛으로는 의미 있는 결과를 못 얻었다(§2.3 끝). "
                  "관례 주의: 원문은 z가 '이전 상태' 쪽 계수. PyTorch nn.GRU도 h = (1−z)⊙n + z⊙h_prev로 같은 관례. 일부 교재는 z와 1−z를 바꿔 쓴다 — 이 강의는 원문 관례로 통일. "
                  "손계산(검산 완료): h_prev = 0.8, h̃ = −0.5. z = 0.9 → 0.72 − 0.05 = 0.67(대부분 유지). z = 0.1 → 0.08 − 0.45 = −0.37(대부분 교체). "
                  "LSTM의 f와 i가 z와 1−z 하나로 묶인 셈. 'GRU' 이름은 이후 문헌(예: Chung et al. 2014 — 원문 미확인)에서 정착. 출처: Cho et al. (2014a) §2.3, Eq.5–8, 각주 1.")
top, bot = s.area.top(1.5, gap=0.3)
s.formula(["r = σ(W_r x + U_r h_prev)      z = σ(W_z x + U_z h_prev)",
           "h̃ = tanh(W x + U (r ⊙ h_prev))    h = z ⊙ h_prev + (1 − z) ⊙ h̃"], top, size=19)
L, R = bot.cols(0.55, gap=0.4)
s.table(["", "z = 0.9", "z = 0.1"], [["h_prev, h̃", "0.8, −0.5", "0.8, −0.5"],
                                    ["z·h_prev + (1−z)·h̃", "0.72 − 0.05", "0.08 − 0.45"],
                                    ["h", "**0.67** (유지)", "**−0.37** (교체)"]], Box(L.x, L.y, L.w, 2.2), size=16, align="lcc",
        highlight=[2], widths=[2.6, 1.9, 1.9])
s.bullets(["**r** (reset): 0이면 이전 상태를 무시", "**z** (update): 이전 상태를 얼마나 유지", ("LSTM의 f·i를 z·(1−z) 하나로", 1),
           "원 논문에 **‘GRU’라는 이름은 없다**", "관례: z = 이전 상태 쪽 (원문 · PyTorch)"], R, size=16)

d.paper("Sutskever et al. (2014)", "Sequence to Sequence Learning with Neural Networks", "NIPS 2014 · arXiv 1409.3215 · Sutskever, Vinyals & Le",
        "DNN은 입출력 차원이 고정이어야 한다 — 번역처럼 길이를 미리 모르는 열 → 열 문제를 일반적으로 풀려면?",
        "LSTM이 입력을 읽어 v를 만들고 다른 LSTM이 v에서 출력을 생성. 세 가지 차이: 인코더·디코더 분리, **4층** 깊은 LSTM, **입력 문장 뒤집기**.",
        "§2 마지막 문단 (세 가지 차이), §3.3 (뒤집기), Table 1·2",
        url="arxiv.org/abs/1409.3215",
        result="순수 신경망 번역으로 SMT 기준선 33.30을 넘김: 34.81 BLEU (5개 앙상블, 빔 12).",
        notes="Sutskever, Vinyals & Le (2014), NIPS, arXiv 1409.3215. Eq.1: p(y_1…y_T′ | x_1…x_T) = Π p(y_t | v, y_1…y_(t−1)). EOS로 길이를 정함. "
              "세 가지 차이(§2): (1) 인코더/디코더 LSTM 분리, (2) 4층(층마다 perplexity 약 10% 감소), (3) 입력을 뒤집어 넣음(출력은 그대로). LSTM은 Graves 형식(forget gate 포함). "
              "실험(§3.1, §3.4–3.5): WMT'14 영→불 1,200만 문장, 어휘 입력 16만·출력 8만(나머지 UNK), 층당 1,000셀, 임베딩 1,000차원, 파라미터 3.84억, "
              "SGD lr 0.7, 배치 128, gradient norm > 5면 5로 스케일, 8 GPU 약 10일. 주의: Seq2Seq가 최초 Encoder–Decoder는 아니다 — Kalchbrenner & Blunsom(2013), Cho et al.(2014a)이 앞선다(§1).")

s = d.slide("아이디어: 입력을 뒤집으면 왜 좋아지나", lead="뒤집기: test perplexity 5.8 → 4.7, BLEU 25.9 → 30.6 — 평균 거리는 같고 ‘최소’ 거리가 줄어든다",
            stage="아이디어",
            notes="§3.3: 입력을 뒤집자 test perplexity 5.8 → 4.7, BLEU 25.9 → 30.6. 저자들의 설명은 가설: '최소 시간 지연(minimal time lag)을 줄여서' — 완전한 설명은 없다고 밝힘. "
                  "원문 예 'a b c → α β γ': a와 α 사이 토큰 수가 정방향 'a b c <EOS> α'에서 3개, 역방향 'c b a <EOS> α'에서 1개. "
                  "강의 예: 정방향 'I am a student <EOS> 나는' — I와 '나는' 사이 4개; 역방향 — 1개. 반면 student와 '학생' 사이는 역방향에서 2개 → 5개로 멀어진다. "
                  "흔한 오해: '뒤집기 = 평균 거리 단축'이 아니다 — 평균은 그대로, 앞쪽 단어끼리의 최소 거리가 줄어든다. 첫 출력 단어들이 쉽게 맞춰지면 나머지 학습이 쉬워진다는 직관. "
                  "학습 목표: (1/|S|) Σ log p(T|S) 최대화, 추론은 argmax를 왼→오 빔 서치로(§3.2). 학습 때 디코더 입력에 정답의 이전 토큰을 넣는다(teacher forcing — 6주차). "
                  "출처: Sutskever et al. (2014) §3.2–3.3; 강의 예는 week4.md 손계산.")
top, bot = s.area.top(3.5, gap=0.2)
s.image(A("week4/paper_reverse.png"), top)
L, R = bot.cols(0.5, gap=0.4)
s.formula("p(y | x) = Π_t p(y_t | v, y_<t)", Box(L.x, L.y, L.w, 0.8), size=19)
s.textbox("학습: 정답 번역의 −log 확률 합 · 추론: 빔 서치 · 정답 이전 토큰을 넣어 학습 (teacher forcing, 6주차)",
          Box(L.x, L.y + 0.9, L.w, bot.h - 0.9), size=14, color=GRAY, gap=0)
s.callout("원문의 설명도 **가설**: “최소 시간 지연을 줄여서” — 완전한 설명은 없다고 저자가 밝힘 (§3.3)",
          Box(R.x, R.y, R.w, bot.h), kind="tip", size=15)

s = d.slide("결과: 순수 신경망 번역이 SMT 기준선을 넘다", lead="단일 모델은 아직 기준선 아래 — 뒤집기 + 5개 앙상블 + 빔 12에서 34.81",
            stage="결과",
            notes="Table 1(직접 번역, WMT'14 영→불 ntst14 BLEU): 단일 정방향 LSTM(빔 12) 26.17, 단일 역방향 30.59, 역방향 5개 앙상블 빔 1 33.00, 빔 2 34.50, 빔 12 34.81. "
                  "SMT 기준선 33.30. 같은 표에 Bahdanau et al.의 당시 수치 28.45가 비교 대상으로 실림(같은 달 공개된 Attention 논문 — 5주차). "
                  "Table 2(SMT 1000-best 재점수화): 단일 정방향 35.61, 단일 역방향 35.85, 5개 앙상블 36.5, WMT'14 최고 37.0, 오라클 ~45, Cho et al. (2014a) 34.54. "
                  "저자 표현: 대규모 번역 과제에서 순수 신경망 번역이 구문 기반 SMT 기준선을 상당한 차이로 처음 넘었다(§3.6) — 단, OOV(어휘 8만 밖)를 처리 못 하는 상태에서. "
                  "Fig.2: 인코더 은닉 상태의 PCA — 어순에 민감하고 능동/수동 변환에는 비교적 불변. "
                  "문장 길이(Fig.3 왼쪽): '35단어 미만에서는 성능 저하가 없고, 가장 긴 문장에서만 약간' — 다음 장들에서 Cho 2014b와 비교. "
                  "출처: Sutskever et al. (2014) Table 1·2, §3.6–3.7, Fig.2–3.")
L, R = s.cols(0.64)
s.image(A("week4/paper_s2s_table1.png"), L)
s.bullets(["단일 역방향 **30.59** < 기준선 33.30", "앙상블 5 · 빔 12: **34.81**", "SMT 1000-best 재점수화: **36.5**",
           ("WMT’14 최고 37.0 · Cho (2014a) 34.54", 1), "한계: 어휘 8만 밖은 **UNK**", "길이: **35단어 미만 저하 없음** (Fig.3)"], R, size=16)

d.paper("Cho et al. (2014b)", "On the Properties of Neural Machine Translation: Encoder–Decoder Approaches",
        "SSST-8 Workshop (EMNLP 2014) · arXiv 1409.1259 · Cho, van Merriënboer, Bahdanau & Bengio",
        "막 등장한 순수 NMT는 어떤 문장에서 잘하고 어디서 약한가? 어휘 크기는 어떤 영향을 주나?",
        "두 인코더(게이트 RNN, grConv)로 같은 조건의 번역을 학습하고 **문장 길이·미등록어 수별로** 성능을 나눠 본다.",
        "초록, §5.1 전체 (1쪽), Table 1",
        url="arxiv.org/abs/1409.1259",
        result="짧고 미등록어 없는 문장은 꽤 잘하지만, 길이와 미등록어가 늘수록 급격히 저하. 해석은 고정 벡터 용량 부족이라는 ‘가설’.",
        notes="Cho, van Merriënboer, Bahdanau & Bengio (2014b), SSST-8, arXiv 1409.1259. Cho et al. 2014a(1406.1078, GRU·구문쌍 재점수화)와 다른 논문이다. "
              "설정(§4.1–4.2): RNNenc(게이트 은닉 유닛 1,000개)와 grConv(2,000개), 디코더는 둘 다 게이트 RNN, 길이 정규화 빔 서치(빔 10). "
              "계산 효율 때문에 양쪽 문장이 30단어 이하인 쌍만 학습, 어휘 각 30,000, 임베딩 620차원, 약 110시간 학습, 입력 뒤집기 없음. "
              "결과: 초록·§5.1, Fig.4 a–c. 해석(§5.1): 'The most obvious explanatory hypothesis' — 고정 길이 벡터가 길고 복잡한 문장을 담기에 용량이 부족하다는 가설. "
              "반대로 구문 기반 SMT는 긴 문장에서 BLEU가 오히려 높았다(Fig.5). grConv는 문법 구조를 비지도로 학습(§5.2).")

s = d.slide("결과: 같은 달, 서로 다른 그림", lead="Cho 2014b는 길이·UNK에 따른 급격한 저하를, Sutskever는 35단어 미만에서 저하 없음을 보고했다",
            stage="결과",
            notes="Cho 2014b Table 1(a) 전체 길이 test BLEU: RNNenc 13.92, grConv 9.97, Moses 33.30; UNK 없는 문장만: RNNenc 23.45, grConv 18.22, Moses 35.63. "
                  "Table 1(b) 10–20단어: RNNenc 20.99 vs Moses 32.00, UNK 없으면 27.03 vs 35.40. 길이별 곡선(Fig.4)은 원문 그림을 직접 볼 것 — 정확한 곡선 값은 노트에 없어 다시 그리지 않았다. "
                  "두 실험의 조건 차이: Cho 2014b는 30단어 이하로만 학습(긴 문장은 학습 분포 밖이기도 함 — 논문이 명시적으로 분리하지 않음), 뒤집기 없음, 1층 1,000유닛 규모. "
                  "Sutskever는 4층 LSTM, 3.84억 파라미터, 입력 뒤집기, 1,200만 문장. 그리고 Sutskever 자신도 긴 문장에서 실패할 줄 알았는데 뒤집기로 잘 됐다고 쓴다(§3.7, §5). "
                  "출처: Cho et al. (2014b) Table 1, §4.1–4.2, §5.1, Fig.4; Sutskever et al. (2014) Fig.3 캡션, §3.7.")
L, R = s.cols(0.52, gap=0.4)
s.image(A("week4/paper_cho14b_table1.png"), L)
s.table(["", "Cho et al. (2014b)", "Sutskever et al. (2014)"],
        [["학습 문장", "**30단어 이하**만", "1,200만 문장"], ["모델", "게이트 RNN 1,000유닛", "**4층** LSTM, 3.84억"],
         ["입력 뒤집기", "없음", "**있음**"], ["길이 관찰", "길수록 **급격히 저하**", "**35단어 미만 저하 없음**"],
         ["희귀어 · UNK", "많을수록 저하", "많을수록 저하 (Fig.3)"]],
        Box(R.x, R.y, R.w, 3.4), widths=[1.6, 2.2, 2.4], size=14)
s.callout("두 결과는 실험 조건이 달라 **직접 비교할 수 없다** — 길이 효과와 학습 분포 밖 효과가 섞여 있다",
          Box(R.x, R.y + 3.6, R.w, 1.1), kind="warn", size=15)

s = d.slide("정리: 병목은 ‘가설’이었다", lead="고정 벡터 하나에 문장 전체 — 저하의 가장 그럴듯한 설명이지만, 크기·요령으로 상당히 완화된다",
            stage="정리",
            notes="병목 주장의 정확한 위상: Cho 2014b가 '가장 명백한 설명 가설'로 제시(§5.1) — 상관 관찰 + 가설이지 증명이 아니다. "
                  "근거: 길이·UNK가 늘수록 저하(Fig.4), 같은 조건의 SMT는 긴 문장에서 오히려 BLEU가 높음(Fig.5). "
                  "반대 증거: 같은 달 Sutskever는 큰 4층 LSTM + 뒤집기로 35단어 미만에서 저하 없음(Fig.3). "
                  "균형 잡힌 결론: 병목은 실재할 수 있지만 모델 크기·학습 요령으로 완화되는 정도가 크다 → 근본적인 해결 방향은 '출력할 때마다 입력의 위치별 표현을 다시 참조'하는 것. "
                  "Bahdanau et al.(2014, Attention)은 이 논문 저자들(Cho, Bengio)과 같은 그룹이며 바로 이 문제를 동기로 삼았다 — 다음 주. "
                  "예: '나는'을 쓸 때는 I가, '학생'을 쓸 때는 student가 필요한데 디코더가 받는 것은 늘 같은 c 하나. "
                  "출처: Cho et al. (2014b) §5.1, Fig.4–5; Sutskever et al. (2014) Fig.3, §3.7; Bahdanau 관계는 week4.md Cho2014b 항목.")
top, bot = s.area.top(2.9, gap=0.3)
L, R = top.cols(0.5, gap=0.4)
s.image(A("week4/seq2seq.png"), L)
s.cards([{"head": "근거 (Cho 2014b)", "bullets": True, "body": ["길이·UNK ↑ → BLEU 급락", "SMT는 긴 문장에서 오히려 ↑"]},
         {"head": "반대 증거 (Sutskever)", "tone": "accent", "bullets": True, "body": ["4층 · 뒤집기", "35단어 미만 저하 없음"]}],
        R, cols=2, body_size=15, head_size=16, fit_h=False)
s.callout("질문: 인코더의 위치별 표현 h_1 … h_S를 **버리지 말고**, 출력할 때마다 **필요한 곳을 다시 찾아보면?** → Bahdanau et al. (2014), 5주차",
          Box(bot.x, bot.y, bot.w, 1.0), kind="key", size=17)

# ============================================================ 마무리
d.summary(["토큰 ID는 **주소**, 임베딩 E는 학습되는 표 · 부분단어(BPE)로 UNK를 줄인다 (Sennrich 2016)",
           "Elman (1990): 은닉층을 **context로 복사** — 다음 단어 예측만으로 품사 구조",
           "기울기는 시간을 거슬러 **곱해진다** (1991 · 1994) · 폭주엔 **clipping** (Pascanu 2013)",
           "LSTM (1997): **CEC + 입력·출력 게이트**, 더하기만 · forget gate는 **2000년**",
           "언어 모델 = 다음 단어 확률의 곱 (2003: 252 vs 312) · Word2Vec: 얕고 크게 (2013)",
           "Encoder–Decoder (2014): 고정 벡터 하나 — 긴 문장 저하는 **병목 가설** → Attention"],
          notes="한 줄씩 학생이 자기 말로 다시 설명하게 한다. 4번: forget gate의 동기는 연속 스트림에서 셀 상태가 한없이 커지는 문제(Gers 2000). "
                "6번: 병목은 Cho 2014b의 '가장 명백한 설명 가설'(30단어 이하 학습, 뒤집기 없음)이고, Sutskever 2014는 35단어 미만에서 저하가 없다고 보고 — 반대 증거도 함께 말한다. "
                "출처: 각 Part의 논문 노트(week4.md).")

d.quiz("셀프 체크", [("1997년 LSTM의 셀 상태 갱신 식은? forget gate는 누가, 왜 도입했나?",
                     "s_c(t) = s_c(t−1) + y^in·g — 더하기만(f ≡ 1). forget gate는 Gers, Schmidhuber & Cummins(2000)가 끊김 없는 연속 입력에서 셀 상태가 한없이 커지는 문제를 막으려고 도입 (LSTM 1997 §4.1; Gers 2000 초록·§3)"),
                    ("어휘 30,000, d = 512인 임베딩 표의 파라미터 수와, ids (4, 20)의 출력 shape은?", "15,360,000개, (4, 20, 512)"),
                    ("W_h = 0.5인 1차원 tanh RNN에서 첫 입력의 흔적이 줄어드는 이유와, 이를 일반화한 조건은?",
                     "매 시점 0.5와 tanh′를 곱하므로 0.762 → 0.363 → 0.180. 일반적으로 |f′·w| < 1이면 소실(Hochreiter 분석, LSTM §3.1), Pascanu: λ1 < 1/γ이면 소실의 충분조건"),
                    ("gradient clipping으로 기울기 소실도 해결되는가?", "아니다. norm clipping(Pascanu 2013 Algorithm 1)은 폭주를 막는다 — 방향은 그대로, 크기만 임계값으로. 소실은 CEC·게이트 쪽"),
                    ("Seq2Seq에서 문장이 길면 번역이 나빠진다는 주장의 근거와 반대 증거는?",
                     "근거: Cho 2014b — 길이·UNK가 늘수록 급격한 저하, '고정 벡터 용량 부족'은 가장 명백한 설명 '가설'(30단어 이하로만 학습, 뒤집기 없음). 반대: Sutskever 2014 — 4층 LSTM+뒤집기로 35단어 미만 저하 없음. 결론: 병목은 가설이며 완화 가능 → 근본 해결은 Attention"),
                    ("Word2Vec 유추 평가에서 정답으로 치는 조건은?", "vec(b) − vec(a) + vec(c)에 코사인으로 가장 가까운 단어(질문 단어 셋 제외)가 정답과 정확히 일치할 때만 — 동의어도 오답 (Mikolov 2013a §4.1)")],
       notes="출처: 각 정답 괄호 안. 6번은 오해 '“king − man + woman”은 이 논문의 결과'와 함께 짚는다.")

d.misconceptions([["“RNN은 Elman이 발명했다”", "Jordan (1986) 등이 앞선다. 기여는 **context 복사 + 예측 + 표현 분석**"],
                  ["“1997 LSTM은 f, i, o 세 게이트”", "1997은 **입력·출력 게이트 + CEC(1.0 고정)**, 더하기만. forget gate는 **2000년**"],
                  ["“forget gate는 기울기 소실 때문에 생겼다”", "원래 동기는 **연속 스트림에서 셀 상태 폭주** (Gers 2000)"],
                  ["“clipping은 소실도 해결한다”", "**폭주**용 (Pascanu 2013). 소실은 기억 경로·게이트"],
                  ["“임베딩은 Word2Vec(또는 2003)이 처음”", "Bengio 2003 스스로 Hinton 1986 · Elman 1990 등을 선행으로 든다"],
                  ["“king − man + woman은 Word2Vec 논문 결과”", "Mikolov, Yih & Zweig (2013)의 결과로 **인용**. 질문 단어는 후보에서 **제외**"],
                  ["“Cho 2014가 GRU와 길이 저하를 함께”", "GRU·Encoder–Decoder는 **2014a**(구문쌍 재점수화), 길이 분석은 **2014b**"],
                  ["“Seq2Seq는 긴 문장에서 반드시 무너진다”", "병목은 **가설**. Sutskever는 35단어 미만 **저하 없음**을 보고"]])

d.homework([("논문 읽기 1 — Elman (1990) pp.194–201, Fig.7",
             "제출: 직교 one-hot 입력인데 품사 군집이 생긴 이유 3문장 + 각주 6(Plate)의 비판과 대응(p.205)"),
            ("논문 읽기 2 — LSTM (1997) §3.2·§4.1 + Gers (2000) §1·§3.1",
             "제출: 두 셀 갱신 식 비교 + i·g = 0.25일 때 f = 1, f = 0.9의 c_1…c_10 표 (예측 먼저)"),
            ("논문 읽기 3 — Cho (2014b) §5.1 + Sutskever (2014) §3.3·§3.7, Fig.3",
             "제출: 병목의 근거·반대 증거 표 + 실험 조건 차이 3가지 — “병목은 증명되었나?”")],
           notes="과제 1–3은 논문의 특정 절·그림을 읽고 제출물이 분명한 질문에 답하는 형식. "
                 "선택 실습(구두 안내): 맨 앞 숫자를 끝에서 다시 출력하는 복사 과제로 같은 크기의 RNN·LSTM을 길이 5·10·20에서 비교 — LSTM 1997의 장지연 과제를 축소한 것(원자료 운영안의 복사·반전 과제), 결론을 미리 정하지 않는다. "
                 "출처: Elman (1990) pp.194–206; LSTM 1997 §3.2, §4.1; Gers (2000) §1, §3.1; Cho (2014b) §5.1; Sutskever (2014) §3.3, §3.7.")

d.references([["Elman (1990). Finding Structure in Time. Cognitive Science 14", "pp.182–184 (Networks with Memory), pp.194–201 · Fig.7"],
              ["Hochreiter & Schmidhuber (1997). Long Short-Term Memory. Neural Computation 9(8)", "§3.1 (Hochreiter 1991 요약), §3.2, §4.1–4.2, Table 2"],
              ["Bengio, Simard & Frasconi (1994). IEEE TNN 5(2) — 원문 미확인", "Pascanu (2013) §2 · LSTM §2.5의 요약으로"],
              ["Gers, Schmidhuber & Cummins (2000). Learning to Forget. Neural Computation 12(10)", "§1 둘째 문단, §3.1 Eq.6–7, Table 2"],
              ["Pascanu, Mikolov & Bengio (2013). On the difficulty of training RNNs. ICML", "§2.1 (조건), §3.2 Algorithm 1"],
              ["Bengio, Ducharme, Vincent & Jauvin (2003). A Neural Probabilistic LM. JMLR 3", "§1.1, §2 (Fig.1, Eq.1), Table 1"],
              ["Mikolov et al. (2013a) arXiv 1301.3781 · (2013b) NIPS, 1310.4546", "2013a §3, §4.1, Table 3 · 2013b §2.2"],
              ["Cho et al. (2014a) EMNLP, 1406.1078 · (2014b) SSST-8, 1409.1259", "2014a §2.2–2.3, Table 1 · 2014b 초록, §5.1, Table 1"],
              ["Sutskever, Vinyals & Le (2014). Seq2Seq. NIPS, 1409.3215", "§2 마지막 문단, §3.3, Table 1·2, Fig.3"],
              ["Sennrich, Haddow & Birch (2016). Subword Units. ACL, 1508.07909", "§3.2 Algorithm 1, Table 2"]],
             notes="처음부터 모든 실험을 읽기보다 표에 적은 절과 그림만 먼저 읽는다. Hochreiter (1991) Diplom 논문과 Bengio et al. (1994)은 이번에 원문을 확인하지 못해 2차 출처(LSTM 1997 §3.1, §2.5; Pascanu 2013 §2)로만 인용했다. "
                   "출처: build/research/papers/week4.md 각 논문의 서지·읽기 안내.")

d.handoff(["토큰 → 임베딩 → 순환 상태 (Elman 1990)", "CEC · 게이트로 **긴 지연 학습** (1997 · 2000)", "Encoder–Decoder로 **길이가 다른** 입출력 (2014)"],
          ["입력 전체를 **고정 벡터 하나**로 — 병목 **가설**", "h_t는 h_(t−1)이 필요 — **순차 계산**"],
          ["**필요할 때 원문을**", "**다시 찾아보면?**", "Bahdanau et al. (2014)\nAttention"],
          notes="다음 주: Bahdanau, Cho & Bengio(2014, arXiv 1409.0473) — 인코더의 위치별 표현을 남겨 두고, 출력할 때마다 다른 비중으로 다시 참조하는 Attention. "
                "Cho 2014b의 병목 가설을 동기로 삼은 같은 그룹의 논문이며, Sutskever Table 1에 당시 수치 28.45로 실려 있다. 그리고 그것을 모델의 본체로 삼은 Transformer로 이어진다. "
                "출처: week4.md 시간 메모, Cho2014b 항목.")

d.save(OUT)
print("saved", OUT, d.n + 2, "slides")
