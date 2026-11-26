"""Week 5 — Attention: 원문을 다시 찾아보면? (논문 중심 재구성)

근거: build/research/papers/week5.md (검증된 논문 노트). 새 그림: build/paper_figs_w5.py,
기존 그림: build/week5_assets.py (assets/week5/transformer_arch.png 는 week1.py 에서도 쓴다 — 건드리지 않음).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deckkit  # noqa: E402
deckkit.use_theme("clean")  # Apple 디자인 원칙 테마 — import * 보다 먼저
from deckkit import *  # noqa

A = lambda p: os.path.join(HERE, "assets", p)
OUT = os.path.join(HERE, "..", "lectures", "week05_attention.pptx")

d = Deck(5, "Attention: 원문을 다시 찾아보기", date="2026-11-02", theme="clean")

# ============================================================ 도입
d.question("필요할 때 원문을\n다시 찾아보면?",
           "2014–2019 · 논문으로 읽는 Attention — Bahdanau · Luong · Self-attention · Transformer §3.2–§4 · 해석 논쟁",
           notes="Transformer 파트의 시작. 지난주 Seq2Seq는 입력 전체를 벡터 하나로 압축해야 했다. 오늘은 그 한계를 처음 지적하고 푼 "
                 "Bahdanau et al.(2014)부터 Attention Is All You Need(2017), 그리고 attention 가중치를 설명으로 읽어도 되는지 다툰 "
                 "2019년 두 논문까지, 원문을 따라가며 배운다. 출처: build/research/papers/week5.md (주차 요약).")

d.bridge(["Seq2Seq (Sutskever 2014 · Cho 2014):\nEncoder → **c** → Decoder", "LSTM으로 긴 의존성 완화"],
         ["원문 전체를 **고정 길이 벡터 c 하나**로 압축\n— Bahdanau가 지목한 병목",
          "긴 문장일수록 성능 급락 (Cho et al. 2014b)", "h_t는 h_(t−1)이 필요 — **순차 계산**"],
         ["**출력 단어마다 원문을 다시 찾아보면?**", "그리고 그 참조를 모델의 **본체**로 쓰면?"],
         notes="4주차 복습: Seq2Seq는 인코더 마지막 상태(고정 길이 벡터 c) 하나로 원문 전체를 대신한다. "
               "Bahdanau et al.은 이 고정 길이 벡터가 성능의 병목이라고 '추측'하고(Abstract, §1), Cho et al.(2014b)이 보인 대로 "
               "입력 문장이 길어질수록 성능이 급격히 떨어진다는 점을 출발점으로 삼는다(§1). 두 번째 남은 문제(순차 계산)는 "
               "Transformer 논문 §1이 지적하는 한계다. 출처: Bahdanau et al. (2014/ICLR 2015) Abstract, §1; Vaswani et al. (2017) §1.")

d.roadmap(["Bahdanau 2014: 정렬하며 번역하기", "Luong 2015: global · local과 점수 함수",
           "2016–2017: self-attention과 ConvS2S", "Vaswani 2017 §3.2: Q·K·V와 multi-head",
           "Vaswani 2017 §3.5: 위치 인코딩", "Vaswani 2017 §4: 왜 self-attention인가",
           "2019: attention은 설명인가?"],
          ["Attention의 **점수 → softmax → 가중합**을 손으로 계산한다",
           "Bahdanau(s_(t−1), additive)와 Luong(h_t, dot/general)의 **차이**를 말한다",
           "softmax(QKᵀ/√d_k)V의 **shape**과 √d_k의 **근거 수준**을 설명한다",
           "Multi-head에서 **(B, N, d) → (B, H, N, d_h)** 변환과 Table 3 결과를 읽는다",
           "attention 지도로 **말할 수 있는 것과 없는 것**을 구분한다"],
          notes="오늘은 일곱 Part, 각 Part가 논문 한 편(또는 짧은 논문 묶음)이다. Part 4–6은 같은 논문(Vaswani et al. 2017)의 §3.2, §3.5, §4. "
                "끝나면 할 수 있어야 하는 것은 오른쪽 다섯 가지 — 마지막 셀프 체크에서 다시 확인한다. 출처: week5.md 주차 요약.")

d.paper_map([("2014", "Bahdanau, Cho & Bengio — Jointly Learning to Align and Translate", "출력마다 다른 문맥 c_i, additive 점수",
              "고정 길이 벡터 c 병목 (Seq2Seq)"),
             ("2014", "Graves et al. — Neural Turing Machines (맥락)", "key–메모리 유사도 → softmax → 가중합",
              "신경망에 외부 메모리 읽기"),
             ("2015", "Luong, Pham & Manning — Effective Approaches", "global / local, 점수 함수 4종 비교",
              "Bahdanau 구조의 단순화·비교"),
             ("2016", "Cheng et al. · Parikh et al.", "한 문장 안의 attention (intra = self)", "두 시퀀스 사이에만 쓰던 attention"),
             ("2017", "Gehring et al. — ConvS2S", "순환 없는 병렬 seq2seq, 학습형 위치", "RNN의 순차 계산"),
             ("2017", "Vaswani et al. — Attention Is All You Need", "self-attention만으로 인코더·디코더", "합성곱의 먼 거리 경로"),
             ("2019", "Jain & Wallace · Wiegreffe & Pinter", "attention 지도를 설명으로 읽어도 되나", "heatmap = 설명이라는 가정")],
            notes="시간 순서 = 논문 순서. 한 줄 흐름: 병목(c 하나) → 매번 다른 가중합(2014) → 점수 함수 정리(2015) → 한 문장 안에서도(2016) → "
                  "순환 없이(ConvS2S 2017) → attention만으로(Transformer 2017) → 그 가중치를 설명으로 믿어도 되나?(2019). "
                  "Bahdanau는 arXiv 2014-09, 학회 게재는 ICLR 2015. NTM은 학회 미게재 preprint로 맥락용. 출처: week5.md 주차 요약 표.")

d.glossary([["정렬 (alignment)", "출력 단어와 원문 단어의 대응 — Bahdanau의 용어", "번역할 때 짚어 보는 원문 단어"],
            ["Attention 가중치 α", "각 위치를 얼마나 참고할지 (softmax, 합 1)", "여러 자료에 나눠 준 신뢰 비중"],
            ["annotation h_j", "원문 j번째 단어의 (양방향) 인코더 표현", "원문에 붙인 메모"],
            ["Self-attention", "한 시퀀스가 자기 자신의 위치들을 참조 (= intra-attention)", "문장이 스스로 앞뒤를 살핌"],
            ["Query · Key · Value", "비교 기준 · 비교 대상 · 실제로 섞일 내용", "찾는 것 · 색인 · 책 내용"],
            ["Head", "독립된 Q·K·V 투영 한 벌 (d_h = d/H 차원)", "서로 다른 관점의 독자"],
            ["위치 인코딩 (PE)", "토큰 벡터에 더하는 위치 정보", "좌석 번호표"],
            ["BLEU", "기계 번역 출력과 정답 번역의 n-gram 일치 점수 (높을수록 좋음)", "모범 답안과 겹치는 표현 비율"]],
           notes="오늘 처음 나오는 용어. 논문 용어는 처음 나올 때 다시 풀어 쓴다. 'attention'이라는 말 자체도 Bahdanau 논문에서는 "
                 "'alignment model'의 해석으로 등장한다(§3.1). Self-attention = intra-attention은 Transformer §2와 Cheng et al.(2016)의 표현. "
                 "d_h는 논문의 d_k = d_v(head당 차원). 출처: Bahdanau §3.1; Vaswani §2, §3.2.2; week5.md 강의 표기.")

# ============================================================ Part 1 — Bahdanau
d.part(1, "Bahdanau 2014: 정렬하며 번역하기", "요약본 하나 대신, 출력 단어마다 원문을 다시 보면?",
       notes="Part 1은 Bahdanau, Cho & Bengio (arXiv 2014-09 / ICLR 2015) 한 편. 순서: 논문 카드 → 문제(고정 길이 벡터) → 아이디어(Fig. 1) → 계산(식 5–6, App. A.1.2) → 결과(Fig. 2, Table 1) → 정렬 그림(Fig. 3) → 한계(§6.1)와 NTM. 출처: week5.md [Bahdanau2014], [Graves2014NTM].")

d.paper("Bahdanau, Cho & Bengio (2014)", "Neural Machine Translation by Jointly Learning to Align and Translate",
        "arXiv:1409.0473 (2014-09) · ICLR 2015",
        "Encoder–decoder는 원문 전체를 **고정 길이 벡터**로 압축해야 하고, 이것이 병목이라고 추측 — 긴 문장에서 성능이 급락",
        "출력 단어 y_i마다 원문 annotation h_j들의 **가중합 c_i**를 새로 만든다. 정렬(alignment)을 번역과 **함께 학습**",
        "§3.1 (식 4–6, ‘attention’ 해석 문단) · Figure 2–3 · App. A.1.2 (정렬 모델 식)",
        url="arxiv.org/abs/1409.0473",
        result="WMT'14 영→불: 긴 문장에서도 BLEU가 떨어지지 않음 (Fig. 2). 단, 전체 test에선 Moses에 못 미침",
        notes="서지: ICLR 2015 conference paper, arXiv:1409.0473 (v1 2014-09-01, 읽은 판본 v7). "
              "풀려던 문제: Abstract, §1. 핵심 아이디어: §3.1–3.2. 논문 자체 용어는 'alignment model'이고, 'attention'은 §3.1에서 "
              "'Intuitively, this implements a mechanism of attention in the decoder.'라는 해석으로 처음 나온다. "
              "결과의 정직한 요약은 두 장 뒤 Table 1 슬라이드에서. 출처: Bahdanau et al. (2014/2015) Abstract, §1, §3.1, §5.1.")

s = d.slide("문제: 고정 길이 벡터 하나로 충분한가", lead="Encoder의 위치별 표현 h_1 … h_T를 버리지 않고, 출력 시점마다 다른 가중합 c_t를 만든다",
            stage="문제",
            notes="왼쪽(Seq2Seq): 원문을 다 읽고 벡터 c 하나만 남겨, 그 c로 모든 출력 단어를 만든다. 오른쪽(Bahdanau): 출력 단어마다 남겨 둔 "
                  "원문 표현들을 다른 비중으로 다시 섞는다. 그림의 α 값은 설명용 예시이지 학습 결과가 아니다. "
                  "저자의 표현은 '추측'(conjecture)이다: 고정 길이 벡터가 기본 encoder–decoder의 성능 향상을 막는 병목이라고 추측하고(Abstract), "
                  "Cho et al.(2014b)의 결과대로 입력이 길어질수록 성능이 급격히 떨어진다고 쓴다(§1). "
                  "바뀐 것은 '상태의 개수'(c 하나 → h_1…h_T 전부)와 '접근 규칙'(항상 같은 c → 매번 다른 가중합). "
                  "출처: Bahdanau et al. Abstract, §1; 그림은 기존 강의 도식(week5_assets.py).")
top, bot = s.area.top(3.75, gap=0.2)
s.image(A("week5/bottleneck.png"), top)
L, R = bot.cols(0.5, gap=0.4)
s.callout("**Seq2Seq**: 원문을 읽고 벡터 하나만 남긴 뒤, 그 하나로 모든 출력 단어를 만든다", L, kind="tip", size=15)
s.callout("**Bahdanau**: 출력 단어마다 원문 표현들을 **다른 비중**으로 다시 섞는다 — 실제 계산은 점수 → softmax → 가중합",
          R, kind="tip", size=15)

s = d.slide("아이디어: 양방향 annotation + 정렬 모델", lead="h_j = [→h_j ; ←h_j] 를 남겨 두고, 직전 디코더 상태 s_(t−1)로 각 h_j에 점수를 매긴다",
            stage="아이디어",
            notes="원문 Fig. 1 기반 재구성. 인코더는 양방향 RNN: 정방향은 x_1→x_T, 역방향은 x_T→x_1로 읽고, 두 상태를 이어 붙인 "
                  "h_j = [→h_j ; ←h_j]를 j번째 단어의 annotation이라 부른다 — 앞뒤 문맥을 모두 요약하되 x_j 주변에 초점(§3.2). "
                  "디코더는 단어 y_t를 만들 때 '직전' 상태 s_(t−1)과 각 h_j의 정렬 점수 e[t, j]를 계산하고 softmax로 α를 만든 뒤 c_t를 만든다(§3.1). "
                  "주의: 현재 상태 h_t로 점수를 내는 것은 Luong(2015)이다 — Bahdanau는 s_(t−1). "
                  "정렬을 잠재 변수로 두지 않고 soft alignment로 직접 계산하므로 번역 손실의 gradient가 정렬 모델까지 흘러 함께 학습된다(§3.1). "
                  "출처: Bahdanau et al. §3.1, §3.2, Fig. 1.")
L, R = s.cols(0.6)
s.image(A("week5/paper_bahdanau_arch.png"), L)
s.bullets(["**annotation** h_j: 양방향 RNN 두 상태를 이어 붙임 (§3.2)", "점수 e[t, j] = a(**s_(t−1)**, h_j) — 직전 디코더 상태",
           ("현재 상태 h_t를 쓰는 것은 Luong (Part 2)", 1), "**soft** alignment → 번역 손실로 **함께 학습**",
           "여기서는 **key = value = h_j** (Q/K/V 분리는 나중의 정리)"], R, size=16)

s = d.slide("계산: 식 (5)–(6)과 정렬 모델을 손으로", lead="① 점수 → ② softmax로 비중 → ③ annotation의 가중합",
            stage="계산",
            notes="원문 식: Eq.(5) c_i = Σ_j α_ij h_j, Eq.(6) α_ij = exp(e_ij)/Σ_k exp(e_ik), e_ij = a(s_{i−1}, h_j). "
                  "정렬 모델(App. A.1.2): a(s_{i−1}, h_j) = v_aᵀ tanh(W_a s_{i−1} + U_a h_j). 강의 표기는 i 대신 t. "
                  "App. A.1.2는 'U_a h_j는 i와 무관하므로 미리 계산해 둔다'고 쓴다 — 출력마다 다시 계산하는 것은 W_a s 부분뿐. "
                  "손계산(파이썬 검산): s = (1,0), h_1 = (1,0), h_2 = (0,1), h_3 = (1,1), W_a = U_a = I, v_a = (1,1). "
                  "e_j = tanh 두 성분의 합: e = (tanh2 + tanh0, tanh1 + tanh1, tanh2 + tanh1) = (0.964, 1.523, 1.726). "
                  "α = softmax(e) = (0.204, 0.358, 0.438), c = 0.204·(1,0) + 0.358·(0,1) + 0.438·(1,1) = (0.642, 0.796). "
                  "가장 큰 가중치 하나를 복사하지 않고 여러 위치를 섞는다(soft). "
                  "출처: Bahdanau et al. §3.1 Eq. 5–6, App. A.1.2; 손계산은 week5.md.")
top, bot = s.area.top(1.55, gap=0.3)
s.formula(["e[t, j] = v_aᵀ tanh( W_a s[t−1] + U_a h[j] )     α[t, :] = softmax_j( e[t, :] )",
           "c[t] = Σ_j  α[t, j] · h[j]"], top, size=20)
L, R = bot.cols(0.58, gap=0.4)
s.table(["j", "h_j", "s + h_j", "e_j = Σ tanh(·)", "α_j", "α_j · h_j"],
        [["1", "(1, 0)", "(2, 0)", "0.964", "0.204", "(0.204, 0)"], ["2", "(0, 1)", "(1, 1)", "1.523", "0.358", "(0, 0.358)"],
         ["3", "(1, 1)", "(2, 1)", "1.726", "**0.438**", "(0.438, 0.438)"], ["합", "", "", "", "1.000", "**(0.642, 0.796)**"]],
        L, size=15, align="cccccc", highlight=[3], widths=[0.5, 1.0, 1.0, 1.5, 0.9, 1.7])
s.bullets(["설정: s = (1, 0), W_a = U_a = I, v_a = (1, 1)", "출력마다 **다른 c_t** — 하나의 c가 아니다",
           "가장 큰 것 하나를 복사하지 않고 **섞는다** (soft)", "U_a h_j는 t와 무관 → **미리 계산** (App. A.1.2)"], R, size=15)

s = d.slide("결과: 긴 문장에서도 무너지지 않는다 — 그러나", lead="원문 Fig. 2(길이별 경향)와 Table 1(전체 BLEU)을 함께 읽는다",
            stage="결과",
            notes="실험 설정(§4, App. A–B): WMT'14 영→불, 병렬 코퍼스 850M 단어 중 데이터 선택으로 348M 단어, 단일어 데이터 미사용, 어휘 각 30,000(나머지 [UNK]). "
                  "test = newstest2014 (3003문장). RNNencdec(기존 encoder–decoder)와 RNNsearch(제안)를 각각 길이 30 이하/50 이하 문장으로 학습(-30, -50). "
                  "hidden 1000, 임베딩 620, 미니배치 80, Adadelta, 모델당 약 5일. "
                  "왼쪽 (a)는 원문 Fig. 2의 '경향'만 다시 그린 개념도이고 곡선의 높이는 수치가 아니다: RNNencdec은 길이가 늘수록 급락, "
                  "RNNsearch-50은 '길이 50 이상에서도 성능 저하가 없다'(§5.1), RNNsearch-30이 RNNencdec-50보다도 높다. "
                  "오른쪽 (b) Table 1: 전체(All) 기준 RNNsearch-50 26.75, 더 오래 학습한 RNNsearch-50⋆ 28.45, Moses(구문 기반 통계 번역) 33.30 — "
                  "전체 test에서는 Moses에 '못 미친다'. 'Moses와 비슷하거나 낫다'는 이야기는 모르는 단어가 없는 문장(No UNK)에서 36.15 vs 35.63. "
                  "게다가 Moses는 추가 단일어 코퍼스 418M 단어를 썼다(§5.1). 출처: Bahdanau et al. §4, §5.1, Table 1, Fig. 2, App. A–B.")
top, bot = s.area.top(3.95, gap=0.2)
s.image(A("week5/paper_bahdanau_results.png"), top)
L, R = bot.cols(0.5, gap=0.4)
s.callout("**길이**: RNNencdec은 긴 문장에서 급락, RNNsearch-50은 길이 50 이상에서도 저하 없음 (§5.1)", L, kind="tip", size=15)
s.callout("==정직하게== 전체 test BLEU는 Moses **33.30** > RNNsearch-50⋆ **28.45**. ‘Moses 수준’은 UNK 없는 문장 기준", R,
          kind="warn", size=15)

s = d.slide("정렬을 눈으로: 원문 Fig. 3이 보여 준 것", lead="대체로 대각선, 그러나 어순이 뒤집힌 곳도 찾는다 — 관찰 도구이지 증명은 아니다",
            stage="결과",
            notes="왼쪽 그림은 이 강의의 '설명용 가상 정렬'(한→영)이다. 원문 Figure 3은 RNNsearch-50의 영→불 정렬 4개를 보여 준다. "
                  "원문이 짚은 것(§5.2.1): ① 정렬은 대체로 단조(대각선). ② [European Economic Area] → [zone économique européenne]처럼 어순이 뒤집힌 "
                  "구간도 올바르게 정렬. ③ [the man] → [l' homme]: 'the'를 번역할 때 뒤의 'man'도 함께 보아야 le/la/les/l' 중 무엇인지 정할 수 있다 — "
                  "한 단어에 하나만 대응시키는 hard alignment가 아니라 soft alignment의 장점. "
                  "주의: 큰 α는 '그 위치에 큰 참조 비중이 관찰되었다'는 뜻이지, 그 단어가 예측의 유일한 원인이라는 증명이 아니다 — Part 7에서 다시. "
                  "출처: Bahdanau et al. §5.2.1, Figure 3; 왼쪽 그림은 기존 강의 도식(가상 예시).")
L, R = s.cols(0.55)
s.image(A("week5/alignment.png"), L)
rest = s.card(R, "원문 Fig. 3 (영→불)이 보여 준 것", ["대체로 **단조** (대각선) 정렬",
                                                  "European Economic Area → zone économique européenne: **어순 반전**도 정렬",
                                                  "the man → l' homme: 뒤 단어도 함께 보는 **soft** 정렬"],
              tone="teal", bullets=True, fit_h=True, body_size=15)
s.card(rest, "증명하지 않는 것", ["그 단어가 예측의 **유일한 원인**이라는 것", "→ 관찰과 인과 검증은 다르다 (Part 7)"],
       tone="accent", bullets=True, fit_h=True, body_size=15)

s = d.slide("한계, 그리고 같은 시기의 다른 길", lead="모든 (출력, 입력) 쌍을 계산한다 · [UNK] 문제 — 내용 기반 조회는 NTM(2014)에도 있었다",
            stage="역사",
            notes="저자가 밝힌 한계(§6.1): 출력 단어마다 '모든' 원문 단어의 가중치를 계산해야 한다(T_x × T_y). 번역(15–40단어)에서는 괜찮지만 "
                  "다른 과제에는 제약일 수 있다 → Luong의 local attention, 이후 효율적 attention의 동기. Table 1의 All vs No UNK 차이가 보여 주는 [UNK] 문제. "
                  "'Attention은 Bahdanau가 처음'은 정확하지 않다: 미분 가능한 가중 정렬은 Graves(2013, 손글씨 합성)가 먼저 있었고 저자도 §6.1에서 비교한다. "
                  "Bahdanau의 기여는 '번역에서 비단조 soft alignment를 함께 학습'한 것. "
                  "같은 시기 Neural Turing Machine(Graves, Wayne & Danihelka, arXiv 2014-10, 학회 미게재)은 key k와 메모리 행 M(i)의 코사인 유사도에 "
                  "β를 곱해 softmax한 가중치로 메모리를 읽는다(§3.3.1 Eq. 5–6; Eq. 2 r = Σ w(i) M(i)). "
                  "손계산(검산): k = (1,0), 메모리 행 (1,0), (0,1), (1,1) → cos = (1, 0, 0.707). β = 1 → w = (0.473, 0.174, 0.353), β = 10 → w = (0.949, 0.000, 0.051). "
                  "β는 softmax의 날카로움을 조절한다 — 뒤의 1/√d_k와 같은 '점수 스케일' 자리(유비일 뿐 동기는 다르다). "
                  "출처: Bahdanau §6.1, Table 1; Graves et al. (2014) NTM §3.1, §3.3.1.")
L, R = s.cols(0.47, gap=0.45)
s.card(L, "Bahdanau의 한계 (§6.1)", ["출력마다 **모든** 원문 위치 계산: T_x × T_y", ("번역 길이(15–40단어)에선 괜찮다", 1),
                                    "[UNK] — Table 1의 All vs No UNK 차이", "가중 정렬 자체는 Graves (2013)가 먼저",
                                    ("기여: 번역에서 **비단조 soft 정렬**을 함께 학습", 1)], tone="plain", bullets=True, body_size=18, head_size=19, fit_h=True)
top, bot = R.top(1.0, gap=0.2)
s.formula("w(i) = softmax_i( β · cos(k, M(i)) )", top, size=19)
mid, low = bot.top(1.6, gap=0.3)
s.table(["NTM 손계산", "M(1)=(1,0)", "M(2)=(0,1)", "M(3)=(1,1)"],
        [["cos(k, M(i))", "1", "0", "0.707"], ["β = 1", "0.473", "0.174", "0.353"], ["β = 10", "**0.949**", "0.000", "0.051"]],
        mid, size=14, align="cccc", widths=[1.6, 1.2, 1.2, 1.2])
s.bullets(["NTM (2014-10): key와 메모리의 **유사도 → softmax → 가중합**", "β가 크면 한 칸에 몰린다 → 뒤의 **÷√d_k**와 같은 자리"],
          low, size=15)

# ============================================================ Part 2 — Luong
d.part(2, "Luong 2015: global · local과 점수 함수", "Bahdanau의 구조를 단순하게 만들고, 무엇이 잘 되는지 비교하면?",
       notes="Part 2는 Luong, Pham & Manning (EMNLP 2015). Bahdanau와의 차이(§3.1), global/local(§3.1–3.2), 점수 함수 비교(Eq. 8, Table 4). 출처: week5.md [Luong2015].")

d.paper("Luong, Pham & Manning (2015)", "Effective Approaches to Attention-based Neural Machine Translation",
        "EMNLP 2015 · arXiv:1508.04025",
        "attention 기반 번역에서 **어떤 구조가 유용한지** 충분히 탐색되지 않았다",
        "디코더의 **현재 상태 h_t**로 정렬. **global**(모든 위치) vs **local**(창 하나), 점수 함수 location · dot · general · concat **비교**",
        "§3.1 (점수 함수 + ‘Comparison to Bahdanau’ 문단) · Table 4",
        url="arxiv.org/abs/1508.04025",
        result="WMT'14 영→독 앙상블 23.0 BLEU (당시 최고 21.6 대비). 최고 단일 모델은 local-p + general",
        notes="서지: EMNLP 2015, arXiv:1508.04025 (읽은 판본 v5). 문제: Abstract. 아이디어: §3, §3.1–3.3. "
              "Table 1 (WMT'14 영→독, tokenized BLEU): base 11.3 → … → local-p(general)+feed 19.0 → +unk replace 20.9 → ensemble 8 + unk 23.0 "
              "(기존 최고 Jean et al. 21.6, WMT'14 우승 SMT 20.7). Table 2 (WMT'15 영→독): 앙상블 25.9 vs 24.9. "
              "출처: Luong et al. (2015) Abstract, §3, §4.1, Table 1–2.")

s = d.slide("Bahdanau와 무엇이 다른가", lead="점수에 쓰는 상태가 다르다: Bahdanau는 직전 s_(t−1), Luong은 현재 h_t",
            stage="아이디어",
            notes="Luong §3.1 'Comparison to Bahdanau et al.': Bahdanau 경로는 h_(t−1) → a_t → c_t → h_t (강의 표기로 s_(t−1)에서 점수), "
                  "Luong 경로는 h_t → a_t → c_t → h̃_t → 예측. Luong은 디코더 최상위 LSTM의 현재 상태 h_t로 정렬을 계산하고, "
                  "문맥 c_t와 이어 붙여 h̃_t = tanh(W_c [c_t ; h_t]) (Eq. 5), p(y_t) = softmax(W_s h̃_t) (Eq. 6). "
                  "Input feeding(§3.3, Fig. 4): h̃_t를 다음 시점 입력에 이어 붙여 이전 정렬 결정을 알게 한다. "
                  "또 Luong은 'Bahdanau et al.은 concat 정렬 함수 하나만 실험했다'고 쓴다. "
                  "흔한 오해: 'Luong attention = Bahdanau에서 점수 함수만 바꾼 것' → 상태(h_t vs s_(t−1)), 계산 경로, input feeding, 4층 stacking LSTM 등 구조도 다르다. "
                  "출처: Luong et al. §3.1, §3.3, Eq. 5–6, Fig. 4.")
s.table(["", "Bahdanau et al. (2014/2015)", "Luong et al. (2015)"],
        [["점수에 쓰는 디코더 상태", "**직전** 상태 s_(t−1)", "**현재** 상태 h_t (최상위 LSTM)"],
         ["계산 경로", "s_(t−1) → α_t → c_t → s_t → 예측", "h_t → a_t → c_t → h̃_t → 예측"],
         ["인코더", "양방향 RNN (annotation)", "4층 stacking LSTM"],
         ["점수 함수", "concat(additive) **하나만** 실험", "location · dot · general · concat **비교**"],
         ["추가 장치", "—", "local attention, **input feeding** (h̃_t를 다음 입력에)"]],
        Box(s.area.x, s.area.y, s.area.w, 3.3), widths=[2.8, 4.6, 4.9], size=16)
s.callout("h̃_t = tanh( W_c [c_t ; h_t] ),  p(y_t | y_<t, x) = softmax( W_s h̃_t )   (Luong Eq. 5–6)",
          Box(s.area.x, s.area.y + 3.6, s.area.w, 0.8), kind="tip", size=16)

s = d.slide("Global vs Local attention", lead="모든 원문 위치를 볼까, 예측한 위치 p_t 주변 창만 볼까",
            stage="아이디어",
            notes="원문 Fig. 2(global)·Fig. 3(local) 기반 재구성. Global: 모든 원문 은닉 상태 h̄_s에 대해 a_t(s) = softmax(score(h_t, h̄_s)) (Eq. 7). "
                  "Local: 정렬 위치 p_t를 정하고 창 [p_t − D, p_t + D]만 본다. local-m은 p_t = t(단조 가정), local-p는 "
                  "p_t = S · sigmoid(v_pᵀ tanh(W_p h_t))를 예측하고 Gaussian(σ = D/2)으로 가중한다(Eq. 9–10). 논문 설정 D = 10(§4.1); 그림은 D = 2. "
                  "동기: Bahdanau §6.1이 지적한 '모든 위치 계산' 비용을 줄이는 방향. 출처: Luong et al. §3.1–3.2, Eq. 7, 9–10, §4.1, Fig. 2–3.")
top, bot = s.area.top(3.5, gap=0.25)
s.image(A("week5/paper_luong_global_local.png"), top)
L, R = bot.cols(0.5, gap=0.4)
s.formula("global: a_t(s) = softmax_s( score(h_t, h̄_s) )", L, size=16)
s.formula("local-p: p_t = S · sigmoid( v_pᵀ tanh(W_p h_t) )", R, size=16)

s = d.slide("점수 함수 네 가지를 비교했다", lead="‘Luong = dot’이 아니다 — location · dot · general · concat을 실험으로 비교",
            stage="계산",
            notes="Luong §3.1, Eq. 8 주변: dot = h_tᵀ h̄_s, general = h_tᵀ W_a h̄_s, concat = v_aᵀ tanh(W_a [h_t ; h̄_s]), "
                  "location = softmax(W_a h_t) (원문 상태를 보지 않음). concat은 Bahdanau의 additive와 같은 계열(W[q;k] = W₁q + W₂k). "
                  "손계산(검산): q = (1,0), 원문 상태 (1,0), (0,1), (1,1). dot: e = (1, 0, 1), α = (0.422, 0.155, 0.422). "
                  "general (W = [[0,1],[1,0]]): e = (0, 1, 1), α = (0.155, 0.422, 0.422) — 같은 벡터라도 W가 '무엇을 비슷하다고 볼지'를 바꾼다. "
                  "속도에 대해: Transformer 논문 §3.2.1은 additive와 dot-product의 '이론적 복잡도는 비슷'하지만 dot-product가 최적화된 행렬곱 덕분에 "
                  "실제로 훨씬 빠르고 메모리 효율적이라고 쓴다. Bahdanau도 U_a h_j는 미리 계산한다(App. A.1.2). "
                  "내용 기반 유사도 조회 자체는 NTM(2014)의 코사인 등 이전에도 있었다 — Luong의 기여는 '정리·비교'. "
                  "출처: Luong et al. §3.1, Eq. 8; Vaswani et al. §3.2.1; Bahdanau App. A.1.2; Graves et al. (2014) §3.3.1.")
s.table(["점수 함수", "식 (q = h_t, k = h̄_s)", "특징", "손계산 α (q = (1, 0))"],
        [["location", "softmax(W_a h_t)", "원문 상태를 **보지 않음** — 위치만", "—"],
         ["dot", "qᵀ k", "파라미터 없음, 행렬곱 한 번", "(0.422, 0.155, 0.422)"],
         ["general", "qᵀ W_a k", "학습된 W_a로 비교 공간을 바꿈", "W = [[0,1],[1,0]] → (0.155, 0.422, 0.422)"],
         ["concat (≈ Bahdanau additive)", "v_aᵀ tanh(W_a [q ; k])", "쌍마다 작은 신경망", "—"]],
        Box(s.area.x, s.area.y, s.area.w, 2.85), widths=[2.9, 2.6, 3.4, 3.4], size=15, highlight=[1, 2])
s.callout("이론 복잡도는 additive ≈ dot (Vaswani §3.2.1) — 차이는 **실제 속도·메모리**: dot은 최적화된 행렬곱 한 번으로 모든 쌍을 계산한다.",
          Box(s.area.x, s.area.y + 3.1, s.area.w, 0.9), kind="tip", size=16)

s = d.slide("결과: Table 4 — 무엇이 잘 되었나", lead="dot은 global에서, general은 local에서 최선 — 최고 단일 모델은 local-p + general",
            stage="결과",
            notes="실험 설정(§4.1): WMT'14 영↔독, 학습 4.5M 문장쌍, 어휘 50K, 4층 LSTM 1000 cells, 10 epoch, SGD, 미니배치 128, dropout 0.2, test newstest2014 (2737문장). "
                  "Table 4 (영→독 newstest2014, unk 대체 전/후 BLEU): global(location) 18.1/19.3, global(dot) 18.6/20.5, global(general) 17.3/19.1, "
                  "local-m(dot) perplexity > 7로 학습 실패, local-m(general) 18.6/20.4, local-p(dot) 18.0/19.6, local-p(general) 19.0/20.9. "
                  "저자 해석: 'dot은 global에, general은 local에 좋다'(§5.3). concat은 perplexity 6.7–7.1로 부진 — 각주 15: W_a 일부를 항등으로 단순화한 탓일 수 있다(원인 미규명). "
                  "Table 6: 정렬 오류율 AER과 BLEU는 잘 상관하지 않는다(§5.4) — 정렬이 '사람 정렬과 닮았는가'와 번역 품질은 다른 질문. "
                  "가로축이 15부터 시작함에 주의. 출처: Luong et al. §4.1, §5.3–5.4, Table 4, Table 6.")
L, R = s.cols(0.6)
s.image(A("week5/paper_luong_table4.png"), L)
s.bullets(["global에선 **dot**, local에선 **general**이 최선 (§5.3)", "local-m + dot은 **학습 실패**", "concat은 부진 — 원인 **미규명** (각주 15)",
           "정렬 오류율(AER)과 BLEU는 **잘 상관하지 않음** (Table 6)", "남은 문제: 여전히 RNN → **순차 계산**"], R, size=16)

# ============================================================ Part 3 — 2016–2017 선행 연구
d.part(3, "2016–2017: self-attention과 ConvS2S", "attention을 한 문장 안에서 쓰면? 순환 없이 번역하면? — 2017년 전에 이미 시작됐다",
       notes="Part 3은 2017년 전의 두 흐름: 한 문장 안의 attention(Cheng et al. 2016, Parikh et al. 2016)과 순환 없는 seq2seq(Gehring et al. ConvS2S, ICML 2017). 출처: week5.md [Cheng2016], [Parikh2016], [Gehring2017].")

d.paper("Cheng · Parikh et al. (2016)",
        "Long Short-Term Memory-Networks for Machine Reading · A Decomposable Attention Model for NLI",
        "둘 다 EMNLP 2016 · arXiv:1601.06733 · arXiv:1606.01933",
        "attention은 **두 시퀀스 사이**에서만 썼다. LSTM은 토큰 간 관계를 명시적으로 다루는 장치가 없다",
        "**intra-attention**: 한 문장이 자기 자신의 다른 토큰을 참조. Parikh는 **순환 없이** attention만으로 문장 쌍 분류",
        "Cheng §3 (Eq. 4–6) · Parikh §3.1, §3.4, Table 1",
        result="SNLI 정확도: Cheng LSTMN 86.3% (3.4M 파라미터) = Parikh 86.3% (382K) — 약 1/9 파라미터",
        notes="Cheng, Dong & Lapata (EMNLP 2016): LSTM의 기억 셀 하나를 토큰마다 슬롯이 있는 memory/hidden tape로 바꾸고, 현재 입력이 같은 시퀀스의 "
              "이전 토큰들 h_1..h_(t−1)에 attention한다 — 저자 용어 intra-attention(§3–4). "
              "Parikh, Täckström, Das & Uszkoreit (EMNLP 2016): Attend → Compare → Aggregate, 기본형은 어순 정보를 전혀 쓰지 않는다(Abstract). "
              "Table 1 SNLI test: vanilla 86.3%, 382K; intra-sentence attention 추가 86.8%, 582K. Cheng LSTMN deep fusion 86.3%, 3.4M. "
              "출처: Cheng et al. §3–4, Table 3; Parikh et al. Abstract, §3, Table 1.")

s = d.slide("한 문장 안의 attention: intra-attention", lead="Transformer 논문 §2 스스로 “self-attention, sometimes called intra-attention”을 선행 연구로 든다",
            stage="아이디어",
            notes="Cheng Eq.(4) a_i^t = vᵀ tanh(W_h h_i + W_x x_t + W_h̃ h̃_(t−1)), Eq.(5) s_i^t = softmax(a_i^t), Eq.(6) [h̃_t; c̃_t] = Σ_{i<t} s_i^t [h_i; c_i]. "
                  "→ additive 점수를 쓰는 왼쪽→오른쪽(인과적) self-attention. 다만 LSTMN은 여전히 순환(RNN) 안에 있다. "
                  "Parikh Eq.(1) e_ij = F(ā_i)ᵀ F(b̄_j) — 내적형 점수(F는 피드포워드). intra 버전 Eq.(6)–(7): f_ij = F_intra(a_i)ᵀ F_intra(a_j), "
                  "a′_i = Σ_j softmax_j(f_ij + d_(i−j)) a_j. 거리 의존 편향 d_(i−j)로 '최소한의 순서 정보'를 주며 병렬성 유지(10단어 초과 거리는 같은 bias). "
                  "→ 순환 없는 self-attention + 상대 위치 편향의 이른 사례. "
                  "Transformer v1 §1은 Parikh [25]를 예외로 인용한다: 'In all but a few cases [25], … used in conjunction with a recurrent network'. "
                  "Transformer §2: 'Self-attention, sometimes called intra-attention … has been used successfully' — 첫 인용이 [4] Cheng et al. "
                  "공저자 Jakob Uszkoreit는 Transformer 저자이기도 하다(v2+ 기여 각주: 'Jakob proposed replacing RNNs with self-attention'). "
                  "출처: Cheng et al. §3 Eq. 4–6; Parikh et al. §3.1 Eq. 1, §3.4 Eq. 6–7; Vaswani et al. §1, §2, 기여 각주(v2+).")
rest = s.cards([{"head": "Cheng et al. (2016) — LSTMN", "bullets": True,
                 "body": ["현재 토큰이 **이전 토큰들**에 attention", "점수: additive vᵀ tanh(…)", "왼쪽→오른쪽 (인과적)",
                          "==하지만== 여전히 **LSTM 안**"]},
                {"head": "Parikh et al. (2016) — Decomposable", "tone": "accent", "bullets": True,
                 "body": ["점수: **내적** F(a_i)ᵀ F(b_j)", "**순환 없이** attend → compare → aggregate",
                          "intra 버전: 거리 편향 d_(i−j)로 순서 단서", "SNLI 86.3%, 파라미터 382K"]}],
               cols=2, body_size=16, head_size=18)
s.callout("Transformer v1 §1: “In all but a few cases **[25 = Parikh]**, attention … is used in conjunction with a recurrent network.”",
          Box(rest.x, rest.y + 0.1, rest.w, 0.9), kind="tip", size=15)

d.paper("Gehring et al. (2017)", "Convolutional Sequence to Sequence Learning", "ICML 2017 · arXiv:1705.03122",
        "RNN은 이전 시점 계산에 의존해 시퀀스 안에서 **병렬화가 안 된다**",
        "인코더·디코더 모두 **합성곱**. 순서는 **학습형 절대 위치 임베딩**, 디코더 **층마다** 내적 attention",
        "§3.1 (위치 임베딩) · §3.3 (multi-step attention) · Table 4",
        url="arxiv.org/abs/1705.03122",
        result="WMT'14 영→독 25.16 · 영→불 40.51 BLEU, GPU에서 GNMT보다 최대 한 자릿수 빠른 번역",
        notes="Gehring, Auli, Grangier, Yarats & Dauphin (ICML 2017), 읽은 판본 v3. 문제: §1 — 합성곱은 모든 위치를 병렬 계산하고, 층을 쌓아 "
              "문맥 창을 키운다(창 n을 덮는 데 O(n/k) 층). 결과: Table 1 — 영→독 25.16 (GNMT word-piece 24.61), 영→불 40.51 (GNMT+RL 39.92); "
              "Table 3 — GPU에서 GNMT 대비 최대 한 자릿수 빠른 번역. 출처: Gehring et al. §1, §3.1, §3.3, Table 1, Table 3.")

s = d.slide("ConvS2S: 순환 없이, 위치는 학습해서", lead="모든 위치를 병렬 계산 · 위치 임베딩 p_j를 더한다 · 디코더 층마다 attention",
            stage="결과",
            notes="§3.1: 학습형 절대 위치 임베딩 p_j를 단어 임베딩에 더한다: e = (w_1 + p_1, …, w_m + p_m). 디코더 입력도 동일. "
                  "§3.3 Multi-step attention: 디코더 '층마다' 별도 attention, 점수는 내적 a_ij^l = softmax_j(d_i^l · z_j^u), 문맥 c_i^l = Σ_j a_ij^l (z_j^u + e_j). "
                  "key = 인코더 출력 z_j, value = z_j + e_j — 저자도 'key-value memory network와 닮았다'고 쓴다. Q/K/V 분리 관점이 여기서 보인다. "
                  "Table 4 (위치 임베딩 제거, 영→독): 전체 21.7 → source 제거 21.3, target 제거 21.5, 둘 다 제거 21.2 — 0.5 BLEU만 떨어짐. "
                  "저자 해석(§5.4): 합성곱 창(인코더 27, 디코더 25단어) 안에서 상대 위치를 스스로 학습할 수 있다. "
                  "흔한 오해 '학습형 위치 임베딩은 BERT·GPT부터' → Transformer §3.5(v2+)가 비교 대상으로 인용한 [9]가 바로 ConvS2S. "
                  "남은 문제: 먼 두 위치를 잇는 데 여러 층이 필요(Part 6). 출처: Gehring et al. §3.1, §3.3 Eq. 1–2, §5.4, Table 4; Vaswani §3.5 (v2+).")
L, R = s.cols(0.5, gap=0.45)
s.formula(["e_j = w_j + p_j   (학습형 위치)", "a_ij = softmax_j( d_i · z_j )", "c_i = Σ_j a_ij ( z_j + e_j )"],
          Box(L.x, L.y, L.w, 1.85), size=18)
s.bullets(["key = 인코더 출력 z_j, value = z_j + e_j", ("저자: “key-value memory network와 닮았다”", 1),
           "디코더 **층마다** attention (multi-step)", "남은 문제: 먼 위치를 잇는 데 **여러 층**"],
          Box(L.x, L.y + 2.1, L.w, L.h - 2.1), size=16)
s.table(["위치 임베딩 (Table 4, 영→독)", "BLEU"],
        [["source + target 모두 사용", "21.7"], ["source 제거", "21.3"], ["target 제거", "21.5"], ["**둘 다 제거**", "**21.2**"]],
        Box(R.x, R.y, R.w, 2.3), size=15, align="lc", widths=[3.6, 1.2], highlight=[3])
s.callout("위치 임베딩을 다 빼도 **−0.5 BLEU**뿐 — 합성곱 창 안에서 상대 위치를 스스로 학습 (§5.4). "
          "self-attention에는 이런 창이 없다 → Part 5", Box(R.x, R.y + 2.55, R.w, 1.4), kind="tip", size=15)

# ============================================================ Part 4 — Vaswani §3.2
d.part(4, "Vaswani 2017 §3.2: Q · K · V와 multi-head", "참조 연산만으로 시퀀스의 표현 자체를 만들면?",
       notes="Part 4는 Vaswani et al. (NIPS 2017) §3.2. 판본 차이(v1 vs v2+)를 먼저 짚고, Q·K·V 정의 → scaled dot-product(4토큰 손계산) → √d_k → 세 사용처와 mask → multi-head(d=8, H=2) → Table 3 (A). 출처: week5.md [Vaswani2017].")

d.paper("Vaswani et al. (2017)", "Attention Is All You Need", "NIPS 2017 · arXiv:1706.03762 (v1 2017-06 … v7 2023-08)",
        "순환은 위치를 따라 **순차적** — 한 예제 안에서 병렬화가 안 된다. 합성곱은 먼 위치를 잇는 연산 수가 거리에 따라 는다",
        "순환·합성곱 없이 **stacked self-attention + position-wise FFN**. Scaled dot-product, multi-head, sinusoidal PE",
        "§3.2 (Fig. 2) · §3.5 · §4 Table 1 — 오늘. §3.1, §3.3–3.4, §5 — 다음 주",
        url="arxiv.org/abs/1706.03762",
        result="WMT'14 영→독 28.4 BLEU (big). 주장: “전적으로 self-attention에 의존하는 최초의 transduction 모델” (§2)",
        notes="서지: NIPS 2017, arXiv:1706.03762. 읽은 판본: v1(2017-06-12)을 기준으로 v2–v7과 대조. 문제: §1, §2. 아이디어: §3, §3.1–3.5. "
              "Table 2 (newstest2014): big 28.4 (영→독). 영→불 big은 v1–v4 41.0, v5 이후 초록·Table 2는 41.8 (§6.1 본문은 v7까지 41.0으로 남음). "
              "논문 스스로 additive attention [2], self-attention [4, 25, 26, 20]을 선행 연구로 들며, 주장은 '전적으로 self-attention에 의존하는 최초의 transduction 모델'(§2). "
              "다음 장에서 판본 차이를 정리한다. 출처: Vaswani et al. §1–§3, §6.1, Table 2.")

s = d.slide("판본에 따라 다르다: v1 vs NIPS판(v2+)", lead="W^O · √d_k 각주 · 학습형 PE 비교는 v1에 없다 — 인용할 때는 “NIPS 2017 / arXiv v2+”",
            stage="논문",
            notes="arXiv 판본: v1 2017-06-12, v2 06-19, v3 06-20, v4 06-30, v5 12-06, v6 2023-07-24, v7 2023-08-02. "
                  "v1: √d_k 각주 없음, 본문만 'dot products growing too large in magnitude to result in useful gradients'. "
                  "v2+: 각주 4 추가 — q, k 성분이 평균 0·분산 1인 독립 확률변수면 q·k는 평균 0, 분산 d_k. 본문도 'pushing the softmax function into regions where it has extremely small gradients'로 바뀜. "
                  "MultiHead 식: v1은 Concat(head_1..head_h)만, v2+는 Concat(…)W^O, W^O ∈ R^{h·d_v × d_model}, 'concatenated and once again projected'. "
                  "학습형 위치 임베딩 비교: v1에는 §3.5 문장도, Table 3 (E) 행도 없다. "
                  "Table 3 base d_ff: v1 표에는 1024로 오기(본문 §3.3은 2048). v2+에서 2048로 수정. "
                  "이 강의에서 W^O, √d_k 분산 논증, 학습형 PE 비교를 '원논문'으로 인용할 때는 NIPS 2017판(arXiv v2+)이라고 적는다. "
                  "출처: Vaswani et al. arXiv v1–v7 대조 (week5.md 판본 차이 표).")
s.table(["항목", "v1 (2017-06-12)", "v2 이후 (NIPS 2017판 포함)"],
        [["MultiHead 식의 **W^O**", "없음: Concat(head_1, …, head_h)", "Concat(…) **W^O** — “once again projected”"],
         ["**√d_k 각주** (분산 = d_k)", "없음 — 본문 한 문장뿐", "각주 4: 독립 · 평균 0 · 분산 1 **가정** 하의 계산"],
         ["**학습형 PE 비교**", "없음 (Table 3에 (E) 행 없음)", "§3.5 + Table 3 (E): “nearly identical”"],
         ["Table 3 base d_ff", "1024 (**오기**, 본문은 2048)", "2048"],
         ["영→불 BLEU (big)", "41.0", "v5부터 초록 · Table 2는 41.8 (본문은 41.0으로 남음)"]],
        Box(s.area.x, s.area.y, s.area.w, 3.4), widths=[2.9, 3.9, 5.5], size=15)
s.callout("v1 PDF를 읽다가 W^O나 각주가 안 보이면 — 틀린 게 아니라 **판본 차이**다.",
          Box(s.area.x, s.area.y + 3.7, s.area.w, 0.7), kind="tip", size=16)

s = d.slide("문제: 순차 계산과 먼 거리 — 그리고 attention을 본체로", lead="RNN은 위치를 따라 순차적, 합성곱은 먼 두 위치를 잇는 데 여러 층 — self-attention은 한 층에서 직접",
            stage="문제",
            notes="§1: 순환 모델은 h_t가 h_(t−1)과 위치 t의 입력에 의존하므로 본질적으로 순차적이고, 한 예제 안에서 병렬화를 막는다. 긴 시퀀스에서는 메모리 한계로 배치도 못 늘린다. "
                  "§2: ConvS2S, ByteNet 같은 합성곱 모델은 병렬이지만 먼 두 위치를 잇는 연산 수가 거리에 따라 선형(ConvS2S) 또는 로그(ByteNet)로 는다. "
                  "§2: Transformer는 이를 상수로 줄이지만 'attention 가중 위치를 평균내기 때문에 유효 해상도가 떨어지는' 비용이 있고, 이를 multi-head로 상쇄한다. "
                  "예: '그 동물은 너무 피곤해서 길을 건너지 않았다. 그것은 …'에서 '그것은'의 표현을 만들 때 '동물'을 많이 참고하면 좋다 — self-attention에서는 한 층에서 직접 만난다. "
                  "주의: self-attention은 2017년 전에도 있었다(Part 3). Transformer = attention + FFN + residual + LayerNorm + 위치 정보의 조합 — 제목 'All You Need'를 '다른 계산이 없다'로 읽으면 안 된다. "
                  "출처: Vaswani et al. §1, §2, §3.1.")
rest = s.cards([{"head": "RNN (§1)", "body": ["h_t는 h_(t−1)이 필요 → **순차**", "먼 두 토큰: **n단계**"]},
                {"head": "합성곱 (§2)", "body": ["병렬이지만 먼 위치를 잇는 데", "**여러 층** (거리에 따라 증가)"]},
                {"head": "Self-attention", "tone": "accent", "body": ["한 층에서 **직접** 만난다", "대가: 평균내기 → 해상도 저하", ("→ multi-head로 상쇄 (§2)", 1)]}],
               cols=3, body_size=16, head_size=18)
s.callout("==주의== self-attention은 2017년 전에도 있었다. Transformer = Attention + FFN + 잔차 + 정규화 + 위치 정보의 **조합** — "
          "‘All You Need’는 ‘다른 계산이 없다’는 뜻이 아니다 (§3.1–3.5).", Box(rest.x, rest.y + 0.1, rest.w, 1.1), kind="warn", size=16)

s = d.slide("§3.2의 정의: query와 key-value 쌍", lead="“출력 = value들의 가중합, 가중치 = query와 key의 compatibility”",
            stage="아이디어",
            notes="§3.2: 'An attention function can be described as mapping a query and a set of key-value pairs to an output … The output is computed as a weighted sum of the values, "
                  "where the weight assigned to each value is computed by a compatibility function of the query with the corresponding key.' "
                  "Bahdanau에서는 key = value = h_j였고(Part 1), ConvS2S에서 key와 value가 갈라졌다(Part 3). §3.2가 이것을 Q/K/V로 일반화해 정리한다. "
                  "도서관 비유: Query는 찾고 싶은 것, Key는 색인, Value는 내용. 비유의 한계: Query는 사용자가 입력한 자연어 질문이 아니다(이미지 Encoder에도 Q가 있다). "
                  "Key는 문자열이나 DB 키가 아니다. Value는 원래 임베딩을 그대로 복사한 것이 아니다. 모두 학습된 투영으로 만든 벡터. "
                  "출처: Vaswani et al. §3.2; Bahdanau §3.1; Gehring §3.3.")
s.table(["", "§3.2에서의 역할", "앞 논문에서는", "도서관 비유 · 한계"],
        [["**Query (Q)**", "Key들과 비교할 기준 벡터", "Bahdanau s_(t−1) · Luong h_t", "찾고 싶은 것 — 사용자 **질문이 아니다**"],
         ["**Key (K)**", "compatibility를 계산할 대상", "Bahdanau h_j · ConvS2S z_j", "색인 — 문자열·DB key가 **아니다**"],
         ["**Value (V)**", "가중합으로 실제 섞일 벡터", "Bahdanau h_j · ConvS2S z_j + e_j", "내용 — 임베딩 **복사가 아니다**"]],
        Box(s.area.x, s.area.y, s.area.w, 2.8), widths=[1.5, 3.2, 3.3, 4.3], size=15)
s.callout("Bahdanau에서는 key = value = h_j → ConvS2S에서 둘이 갈라지고 → §3.2가 **Q · K · V**로 정리했다.",
          Box(s.area.x, s.area.y + 3.1, s.area.w, 0.8), kind="key", size=17)

s = d.slide("학습되는 것은 투영 행렬, A는 활성값", lead="Q = X W_Q,  K = X W_K,  V = X W_V — 같은 X, 다른 투영 → Q ≠ K ≠ V",
            stage="계산",
            notes="§3.2.2: head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V), W_i^Q, W_i^K ∈ R^{d_model×d_k}, W_i^V ∈ R^{d_model×d_v}. self-attention에서는 Q = K = V = X(이전 층 출력)를 넣고 "
                  "서로 다른 W로 투영한다(§3.2.3). 강의 표기: X (N, d), W (d, d_h) → (N, d_h). 편향 생략. "
                  "학습되는 파라미터는 W_Q, W_K, W_V, W_O뿐. Q, K, V와 A = softmax(QKᵀ/√d_h)는 입력마다 새로 계산되는 활성값이다 — 추론 때 가중치가 고정되어도 A는 문장마다 다르다. "
                  "W가 다르므로 점수 행렬 QKᵀ도 일반적으로 비대칭: q_A·k_B ≠ q_B·k_A. 설령 Q = K여도 행별 softmax 후엔 비대칭. "
                  "출처: Vaswani et al. §3.2.2–3.2.3.")
L, R = s.cols(0.44)
s.image(A("week5/qkv_proj.png"), L)
s.table(["", "예", "입력마다?", "갱신?"],
        [["파라미터", "W_Q · W_K · W_V · W_O", "아니오 (공유)", "**예**"],
         ["활성값", "Q, K, V", "**예**", "아니오"],
         ["가중치 A", "softmax(QKᵀ/√d_h)", "**예**", "아니오"]],
        Box(R.x, R.y, R.w, 2.1), widths=[1.4, 2.6, 1.5, 1.0], size=14)
s.bullets(["같은 X, 다른 W → Q · K · V는 일반적으로 **다르다**", "점수는 **비대칭**: q_A · k_B ≠ q_B · k_A",
           "**찾는 기준**(Q·K)과 **가져올 내용**(V)을 따로 학습"], Box(R.x, R.y + 2.35, R.w, R.h - 2.35), size=15)

s = d.slide("Scaled dot-product attention: 원문 Fig. 2와 Eq. (1)", lead="Attention(Q, K, V) = softmax(QKᵀ / √d_k) V — 마스크는 §3.2.3에서",
            stage="계산",
            notes="원문 Fig. 2 기반 재구성. 왼쪽: MatMul → Scale → Mask(선택) → SoftMax → MatMul. 오른쪽: h개의 head가 병렬로 attention → Concat → Linear(W^O). "
                  "원문 Eq.(1)은 softmax(QKᵀ/√d_k)V이고 마스크 M은 식에 없다 — §3.2.3에서 '불법 연결에 해당하는 softmax 입력을 −∞로' 설명한다. "
                  "강의 표기 softmax(QKᵀ/√d_h + M)V는 Eq.(1)과 §3.2.3의 마스크를 합친 교육용 표기. d_h(강의) = d_k(논문). "
                  "다섯 단계: ① QKᵀ (N, N) ② ÷√d_k ③ +M ④ 행마다 Key 축 softmax(합 1) ⑤ AV (N, d_h). 행 = Query, 열 = Key. "
                  "W^O(오른쪽 맨 위 Linear)는 v1 식에는 없고 NIPS판(v2+)에 있다. 출처: Vaswani et al. §3.2.1 Eq. 1, §3.2.3, Fig. 2.")
L, R = s.cols(0.64)
s.image(A("week5/paper_vaswani_fig2.png"), L)
s.formula(["softmax( Q Kᵀ / √d_k ) V", "강의 표기: … + M"], Box(R.x, R.y, R.w, 1.3), size=19)
s.bullets(["① QKᵀ: **(N, N)** 점수, 행 = Query · 열 = Key", "② ÷ √d_k  ③ mask: −∞ (§3.2.3)", "④ softmax: 행마다 **Key 축**, 합 1",
           "⑤ A V: **(N, d_h)**", "W^O는 **NIPS판 / arXiv v2+** 식"], Box(R.x, R.y + 1.55, R.w, R.h - 1.55), size=15)

s = d.slide("4토큰 예제: 설정", lead="토큰 A · B · C · D, 특징 2개 — 숫자는 설명용이며 학습 결과가 아니다", stage="계산",
            notes="원자료 시뮬레이터의 예제(모든 숫자 파이썬 검산, week5.md). Q, K, V는 이미 투영이 끝난 값이라고 하자. d_h = 2이므로 스케일은 √2. "
                  "A·B·C·D는 실제 의미가 없는 예시 토큰. 다음 장에서 Query A의 행을 손으로 계산한다. 출처: Vaswani §3.2.1 Eq.(1)을 작은 숫자에 적용.")
L, R = s.cols(0.62)
s.image(A("week5/attn_setup.png"), L)
s.table(["토큰", "q", "k", "v"], [["A", "(1, 0)", "(1, 0)", "(1, 0)"], ["B", "(0, 1)", "(0, 1)", "(0, 1)"],
                                 ["C", "(1, 1)", "(1, 1)", "(2, 2)"], ["D", "(−1, 0.5)", "(−1, 1)", "(−1, 1)"]],
        Box(R.x, R.y, R.w, 2.4), size=15, align="cccc")
s.bullets(["q · k · v는 **투영이 끝난 값**이라고 가정", "d_h = 2 → 스케일 **√2**", "먼저 **Query A**의 행 하나를 손으로"],
          Box(R.x, R.y + 2.65, R.w, R.h - 2.65), size=16)

s = d.slide("Query A를 손으로 계산", lead="점수 → ÷√2 → exp → 합으로 나누기 → Value 가중합", stage="계산",
            notes="q_A = (1, 0). 점수: k_A와 1, k_B와 0, k_C와 1, k_D와 −1. ÷√2: 0.707, 0, 0.707, −0.707. "
                  "exp: 2.028, 1.000, 2.028, 0.493, 합 5.549. softmax: 0.365, 0.180, 0.365, 0.089 (합 1). "
                  "출력 = 0.365·(1,0) + 0.180·(0,1) + 0.365·(2,2) + 0.089·(−1,1) = (1.008, 1.000). "
                  "A와 C에 같은 비중(둘 다 q_A와의 내적 1), D는 반대 방향이라 가장 작은 비중. "
                  "(숙제용) 스케일을 빼면 첫 행 = (0.399, 0.147, 0.399, 0.054) — 더 뾰족해진다. 출처: Vaswani Eq.(1); 검산 week5.md.")
s.takeaway("o_A = 0.365·v_A + 0.180·v_B + 0.365·v_C + 0.089·v_D = (1.008, 1.000)")
s.table(["Key", "q_A · k", "÷ √2", "exp", "softmax α", "α · v"],
        [["A (1, 0)", "1", "0.707", "2.028", "**0.365**", "(0.365, 0)"], ["B (0, 1)", "0", "0", "1.000", "**0.180**", "(0, 0.180)"],
         ["C (1, 1)", "1", "0.707", "2.028", "**0.365**", "(0.731, 0.731)"], ["D (−1, 1)", "−1", "−0.707", "0.493", "**0.089**", "(−0.089, 0.089)"],
         ["합", "", "", "5.549", "1.000", "**(1.008, 1.000)**"]], Box(s.area.x, s.area.y, s.area.w, 3.0),
        widths=[1.6, 1.3, 1.2, 1.2, 1.6, 2.2], size=16, align="cccccc", highlight=[4])
s.bullets(["**A와 C는 같은 비중** — 둘 다 q_A와의 내적이 1", "**D는 반대 방향** → 내적 −1 → 가장 작은 비중 (0.089)",
           "출력 o_A는 네 Value의 **가중합** — 가장 큰 것 하나를 고르지 않는다"],
          Box(s.area.x, s.area.y + 2.75, s.area.w, s.area.h - 2.75), size=16)

s = d.slide("전체 행렬로: 점수 → A → O", lead="나머지 Query도 같은 규칙 — 네 행을 행렬곱 한 번에", stage="계산",
            notes="왼쪽: 점수 QKᵀ/√2 (4×4). 가운데: 행별 softmax A — 각 행의 합 1. 오른쪽: O = AV (4×2). 첫 행이 방금 손으로 계산한 Query A. "
                  "A = [[0.365, 0.180, 0.365, 0.089], [0.141, 0.286, 0.286, 0.286], [0.221, 0.221, 0.449, 0.109], [0.090, 0.259, 0.127, 0.524]], "
                  "O = [[1.008, 1.000], [0.427, 1.145], [1.009, 1.227], [−0.180, 1.038]]. Query D는 자기 자신 D와 B에 큰 비중(0.524, 0.259). "
                  "생각해 보기: Q와 K를 고정하고 V만 바꾸면 A는? 그대로(Q, K, mask만으로 결정). O는? 바뀐다. "
                  "이것이 §3.2.1의 'dot-product는 최적화된 행렬곱으로 구현할 수 있어 빠르다'의 뜻 — 모든 쌍을 한 번에. 출처: Vaswani §3.2.1; 검산 week5.md.")
top, bot = s.area.top(3.4, gap=0.25)
s.image(A("week5/attn_pipeline.png"), top)
s.bullets(["각 행의 합 = 1 (softmax는 행마다), 첫 행 = 방금 손으로 계산한 Query A",
           "생각해 보기: Q·K를 고정하고 **V만** 바꾸면 A는? O는? (답: A 그대로, O는 바뀐다)"], bot, size=16)

s = d.slide("왜 √d_k로 나눌까 — 원문의 논증은 어디까지인가", lead="Britz et al.의 관찰 → 저자의 “We suspect” → (v2+) 각주의 가정 하 계산",
            stage="아이디어",
            notes="§3.2.1의 순서: ① d_k가 작으면 additive와 dot-product가 비슷하지만, d_k가 크면 '스케일 없는' dot-product보다 additive가 낫다는 Britz et al.(2017) [3]의 관찰. "
                  "② 'We suspect that for large values of d_k, the dot products grow large in magnitude, pushing the softmax function into regions where it has extremely small gradients' — 추측. "
                  "③ 각주 4(v2부터, v1에는 없음): q, k 성분이 평균 0·분산 1인 독립 확률변수라면 q·k = Σ q_i k_i는 평균 0, 분산 d_k. 그래서 1/√d_k로 스케일. "
                  "검산(독립 표준정규 성분 20만 샘플): d_h = 4, 16, 64, 256에서 q·k 표준편차 ≈ 2.00, 3.99, 8.00, 15.98; ÷√d_h 후 ≈ 1.00. "
                  "즉 '증명된 최적 스케일'이 아니라 경험적 관찰 + 추측 + 단순화 가정 아래의 분산 계산. 실제 학습된 Q, K가 이 가정을 항상 만족한다는 주장도 아니다. "
                  "또 이 스케일은 생성 때의 temperature와 위치·목적이 다르다. NTM의 β(Part 1)와 같은 자리지만 β는 학습되는 스칼라. "
                  "출처: Vaswani et al. §3.2.1 + 각주 4 (NIPS판 / arXiv v2+); week5.md 검산.")
L, R = s.cols(0.55)
s.image(A("week5/sqrt_scale.png"), L)
s.table(["원문의 단계", "근거의 종류"], [["d_k가 크면 additive > 스케일 없는 dot", "Britz et al. 2017의 **관찰**"],
                                       ["내적이 커져 softmax 기울기가 작아진다", "저자의 **“We suspect”**"],
                                       ["성분 독립 · 분산 1이면 Var(q·k) = d_k", "각주 4 — **가정**, v2+"]],
        Box(R.x, R.y, R.w, 2.2), size=14, widths=[3.4, 2.4])
s.table(["d_h", "q·k 표준편차", "÷ √d_h 후"], [["4", "≈ 2", "≈ 1"], ["64", "≈ 8", "≈ 1"], ["256", "≈ 16", "≈ 1"]],
        Box(R.x, R.y + 2.4, R.w, 1.35), size=14, align="ccc")
s.bullets(["==주의== 증명된 최적값이 아니다", "생성 때 **temperature**와는 목적이 다르다"],
          Box(R.x, R.y + 3.95, R.w, R.h - 3.95), size=15)

s = d.slide("§3.2.3 세 가지 사용처와 decoder의 mask", lead="Q를 어디서 만들고 K · V를 어디서 가져오는가 — 그리고 어디까지 볼 수 있는가",
            stage="계산",
            notes="§3.2.3: ① encoder-decoder attention — query는 이전 디코더 층, key·value는 인코더 출력. (흔히 cross-attention이라 부르지만 원문 용어는 encoder-decoder attention.) "
                  "② encoder self-attention — Q, K, V 모두 이전 인코더 층, 모든 위치. ③ decoder self-attention — 자기회귀 성질을 지키려고 '미래' 위치를 막는다: "
                  "softmax 입력 중 불법 연결을 −∞로(마스크). 4토큰 예제에서 Query B의 행 점수 [0, 0.707, 0.707, 0.707]에 C, D를 −∞로 막으면 "
                  "softmax(0, 0.707) = [0.33, 0.67, 0, 0]. 0으로만 바꾸면 exp(0) = 1이라 가중치가 남는다(오른쪽 패널). "
                  "경계 조건: 어떤 행의 모든 Key가 막히면 softmax가 정의되지 않아 구현에 따라 NaN — 유효한 Query에는 허용된 Key가 최소 하나 있어야 한다. "
                  "S = source 길이, T = target 길이. encoder-decoder attention의 점수 표는 T×S, 출력 길이는 Query 수 T. 자세한 mask와 학습은 다음 주. "
                  "출처: Vaswani et al. §3.2.3; 4토큰 예제 검산 week5.md.")
top, bot = s.area.top(1.95, gap=0.2)
s.table(["원문 용어 (§3.2.3)", "Q의 출처", "K · V의 출처", "볼 수 있는 범위", "점수 표"],
        [["encoder self-attention", "이전 인코더 층", "같은 층", "모든 입력 위치", "S × S"],
         ["decoder (masked) self-attention", "이전 디코더 층", "같은 층", "현재와 **이전** 위치만", "T × T"],
         ["encoder-decoder attention (≈ cross)", "**디코더**", "**인코더** 출력", "모든 source 위치", "**T × S**"]],
        top, widths=[3.7, 2.0, 2.0, 2.8, 1.2], size=14)
L, R = bot.cols(0.72, gap=0.3)
s.image(A("week5/causal.png"), L)
s.bullets(["B 행: **[0.33, 0.67, 0, 0]**", "−∞ → exp = 0 → 정확히 0", "0으로만 바꾸면 **새어 나간다**", "모두 막힌 행 → NaN 주의"],
          R, size=15)

s = d.slide("Multi-head attention (§3.2.2)", lead="d차원을 h개 부분공간으로 나눠 각 head가 독립적으로 attention — 이어 붙여 W^O로 섞는다",
            stage="아이디어",
            notes="§3.2.2: 'Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions. "
                  "With a single attention head, averaging inhibits this.' — §2의 '평균내기로 인한 유효 해상도 저하'를 상쇄하는 장치. "
                  "MultiHead(Q, K, V) = Concat(head_1, …, head_h) W^O (NIPS판/arXiv v2+; v1 식에는 W^O가 없다), head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V). "
                  "h = 8, d_k = d_v = d_model/h = 64. 'head당 차원이 줄어 전체 계산 비용은 전체 차원 single-head와 비슷'. "
                  "주의: 각 head는 모든 토큰 위치를 처리한다. 나누는 것은 토큰이 아니라 '특징 차원'. 그림은 무작위 가중치 예시 — 역할 지정 아님. "
                  "출처: Vaswani et al. §2, §3.2.2 (v1 vs v2+).")
top, bot = s.area.top(1.5, gap=0.3)
s.formula(["head_i = Attention( Q W_i^Q, K W_i^K, V W_i^V )", "MultiHead(Q, K, V) = Concat( head_1, …, head_h ) W^O"], top, size=20)
L, R = bot.cols(0.58, gap=0.35)
s.image(A("week5/heads.png"), L)
s.bullets(["동기 (§3.2.2): single head는 **평균내기** 때문에 여러 부분공간·위치를 함께 보기 어렵다", "각 head는 **모든 토큰**을 본다 — 나누는 건 **특징 차원**",
           "base: h = 8, d_k = d_v = 512/8 = **64**", "W^O: **NIPS판 / arXiv v2+** 식 (v1에는 없음)"], R, size=15)

s = d.slide("d = 8, H = 2, N = 5를 따라가기", lead="(B, N, d) → 투영 → (B, N, H, d_h) → 축 교환 → (B, H, N, d_h)", stage="계산",
            notes="구현에서는 H개의 투영을 하나의 큰 (d, d) 행렬로 묶어 한 번에 계산하고, 결과를 head 축으로 쪼갠 뒤(view) 축을 바꾼다(transpose). "
                  "B=2, N=5, d=8, H=2, d_h=4: X (2,5,8) → Q (2,5,8) → view (2,5,2,4) → transpose (2,2,5,4). 점수 QKᵀ: (2,2,5,4)@(2,2,4,5) → (2,2,5,5). "
                  "A V → (2,2,5,4) → transpose + reshape → (2,5,8) → W_O → (2,5,8). 입력과 출력 shape이 같아서 층을 쌓을 수 있다. "
                  "Q (B,H,T,d_h), K (B,H,S,d_h)이면 QKᵀ는 (B,H,T,S) — d_h는 내적하며 사라진다. 출처: Vaswani §3.2.2 (d_k = d_model/h)를 작은 크기로.")
top, bot = s.area.top(2.55, gap=0.2)
s.image(A("week5/mha_shapes.png"), top)
s.table(["단계", "연산", "shape", "의미"],
        [["입력", "X", "(2, 5, 8)", "문장 2개 · 토큰 5개 · 특징 8개"], ["투영", "X W_Q (d × d)", "(2, 5, 8)", "모든 head의 Q를 한 번에"],
         ["head 분리", "view → transpose", "(2, 2, 5, 4)", "배치 · head · 토큰 · 특징"], ["점수", "Q Kᵀ / √4", "(2, 2, 5, 5)", "head별 위치 관계"],
         ["가중합", "A V", "(2, 2, 5, 4)", "head별 새 표현"], ["결합 · 투영", "concat → W_O", "(2, 5, 8)", "입력과 같은 shape → 쌓을 수 있다"]],
        bot, widths=[1.5, 2.4, 1.7, 4.2], size=13)

s = d.slide("도구: PyTorch로 직접 구현", lead="투영 한 번 → head 축 만들기 → scaled dot-product → 합치기", stage="코드",
            notes="논문이 아닌 '도구' 슬라이드. 직접 구현한 multi-head self-attention. view(B, N, H, d_h).transpose(1, 2)가 핵심 shape 조작이다. softmax의 dim=-1은 Key 축. "
                  "nn.MultiheadAttention(8, 2)의 파라미터는 4 × (8×8 + 8) = 288 (파이썬 검산). 출력 (2, 5, 8), head별 가중치 (2, 2, 5, 5). "
                  "실습: 직접 구현한 결과와 F.scaled_dot_product_attention의 결과가 같은지 확인해 보기. 출처: Vaswani §3.2.1–3.2.2 식을 코드로; 파라미터 수 검산 week5.md.")
L, R = s.cols(0.6)
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
       "print(Wo(O).shape)                        # (2, 5, 8)", L, size=14)
s.bullets(["`view + transpose`: head 축 만들기", "`softmax(dim=-1)`: **Key 축**", "출력 shape = 입력 shape",
           "기대 출력: `torch.Size([2, 5, 8])`", ("head별 가중치 A: (2, 2, 5, 5)", 1),
           "`nn.MultiheadAttention(8, 2)`", ("파라미터 4 × (8·8 + 8) = **288**", 1),
           "확인: `F.scaled_dot_product_attention`", ("`A @ V`와 같은지 `torch.allclose`로", 1)], R, size=15)

s = d.slide("결과: head는 몇 개가 좋은가 — Table 3 (A)", lead="계산량을 고정하면 head 1개는 0.9 BLEU 나쁘고, 너무 많아도 떨어진다",
            stage="결과",
            notes="Table 3 (영→독 dev newstest2013, base: N=6, d=512, d_ff=2048, h=8, d_k=d_v=64 → PPL 4.92, BLEU 25.8, 65M 파라미터). "
                  "(A) 계산량을 고정하고 head 수만 바꿈(d_k = 512/h): h=1 24.9, h=4 25.5, h=8 25.8, h=16 25.8, h=32 25.4. "
                  "원문 §6.2: 'single-head attention is 0.9 BLEU worse than the best setting, quality also drops off with too many heads.' "
                  "(B) d_k만 16 → 25.1, 32 → 25.4: compatibility 판단은 쉽지 않고 내적보다 정교한 함수가 도움이 될 수 있다는 저자 언급. "
                  "d를 고정하고 d_h = d/H면 W_Q·W_K·W_V·W_O의 주요 파라미터 약 4d²는 H와 무관 — d = 512에서 4d² = 1,048,576 (편향 포함 1,050,624) ≈ 105만. "
                  "head 역할에 대해: 저자는 §4 마지막 문단·부록에서 'heads clearly learn to perform different tasks'라고 주장한다 — 근거는 정성적 그림(Part 7). "
                  "구조가 역할을 지정하지는 않는다. 세로축이 24.6부터 시작함에 주의. 출처: Vaswani et al. §6.2, Table 3 (A)(B), §3.2.2, §4; 파라미터 검산 week5.md.")
L, R = s.cols(0.58)
s.image(A("week5/paper_table3a.png"), L)
s.table(["d 고정, H를 늘리면", "변화"], [["투영 파라미터 ≈ 4d²", "**그대로** (d = 512: 약 105만)"],
                                    ["head당 차원 d_h = d/H", "**줄어든다** (512/8 = 64)"],
                                    ["저장하는 점수 표 H · N²", "**늘어난다**"]],
        Box(R.x, R.y, R.w, 1.9), size=14, widths=[2.6, 2.6], align="lc")
s.callout("저자는 “heads **clearly learn** to perform different tasks”라고 썼다 (§4 · 부록) — 근거는 **정성적 그림**. "
          "역할이 구조에 **지정되지는 않는다** → Part 7", Box(R.x, R.y + 2.15, R.w, 1.9), kind="warn", size=15)

# ============================================================ Part 5 — Vaswani §3.5
d.part(5, "Vaswani 2017 §3.5: 위치 인코딩", "Self-attention은 “개가 사람을 물었다”와 “사람이 개를 물었다”를 구분할까?",
       notes="Part 5는 같은 논문의 §3.4–§3.5: 순열 등변성 → 임베딩 + PE(√d_model은 이유 미기재) → sinusoid 식과 d=8 표 → 선형 이동 가설 → Table 3 (E). 출처: Vaswani et al. §3.4–3.5, Table 3 (v2+).")

s = d.slide("문제: self-attention은 순서를 모른다", lead="입력 순서를 섞으면 출력도 똑같이 섞일 뿐 — 순열 등변성", stage="문제",
            notes="§3.5: 'Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens.' "
                  "위치 정보나 위치 의존 mask가 없는 self-attention에 입력 순열 P를 적용하면 Q′=PQ, K′=PK, V′=PV이고, 행 단위 softmax는 행·열이 같이 움직이므로 SA(PX) = P·SA(X). "
                  "입력을 섞으면 출력도 같은 방식으로 섞인다(등변성). 출력이 변하지 않는다는 불변성과 다르다(3주차 CNN의 등변성/불변성). "
                  "ConvS2S는 합성곱 창 안에서 상대 위치를 배울 수 있었지만(Part 3, Table 4), self-attention에는 그런 창이 없다. "
                  "causal mask가 있으면 방향 정보가 생기므로 이 증명을 그대로 적용할 수 없다. 출처: Vaswani et al. §3.5; Gehring et al. §5.4.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("SA(P X) = P · SA(X)        (P: 순서를 섞는 순열)", top, size=24)
rest = s.cards([{"head": "무슨 뜻인가", "tone": "accent", "bullets": True,
                 "body": ["순서를 섞으면 출력도 **똑같이 섞일 뿐**", "각 토큰의 출력은 ‘어떤 토큰들이 있나’만 반영",
                          "“개가 사람을 물었다” vs “사람이 개를 물었다”", ("→ **구분 불가**", 1)]},
                {"head": "구분할 것", "tone": "plain", "bullets": True,
                 "body": ["**등변성**: 섞으면 같이 섞임 (이것)", "**불변성**: 섞어도 그대로", "ConvS2S는 합성곱 창이 상대 위치를 줬다",
                          "causal mask가 있으면 이 증명이 그대로 적용되지 않는다"]}], bot, cols=2, body_size=16, head_size=18)
s.callout("§3.5: 순환도 합성곱도 없으니 위치 정보를 **주입해야(inject)** 한다", Box(rest.x, rest.y, rest.w, 0.8), kind="key", size=17)

s = d.slide("임베딩에 위치를 더한다 (§3.4–§3.5)", lead="x = E[id] · √d_model + PE[pos] — shape은 그대로, 같은 차원에 위치 단서가 섞인다", stage="아이디어",
            notes="§3.5: 위치 인코딩은 임베딩과 같은 차원 d_model이라 둘을 더할 수 있다. 인코더와 디코더 스택의 맨 아래 입력 모두. "
                  "§3.4: 입력·출력 임베딩과 softmax 앞 선형층이 같은 가중치를 공유하고, 'In the embedding layers, we multiply those weights by √d_model.' — "
                  "논문은 이 곱셈의 이유를 적지 않았다. 'PE와 크기를 맞추기 위해'는 흔한 해석일 뿐이다. "
                  "입력 ID (B, S) → 임베딩 (B, S, d) → + PE (S, d) → (B, S, d) (broadcasting, 1주차). "
                  "더한다고 해서 토큰 내용과 위치가 완벽히 분리되어 저장되는 것은 아니다 — 같은 차원에 결합될 뿐. 출처: Vaswani et al. §3.4, §3.5.")
top, bot = s.area.top(1.5, gap=0.35)
s.flow([{"head": "ID", "body": "(B, S)"}, {"head": "임베딩 × √d_model", "body": "(B, S, d)"}, {"head": "+ 위치 벡터 PE", "body": "(S, d) → broadcasting", "tone": "accent"},
        {"head": "블록 입력", "body": "(B, S, d)", "tone": "dark"}], top, body_size=15, head_size=17)
s.bullets(["Encoder와 Decoder **모두** 이 과정을 거친다 (§3.5)", "더해도 **shape은 그대로** (1주차 broadcasting)",
           "× √d_model: §3.4의 설정 — 임베딩 가중치는 softmax 앞 선형층과 **공유**",
           ("==이유는 원문에 없다== — ‘PE와 크기 균형’은 흔한 해석일 뿐", 1),
           "내용과 위치가 **분리 저장**되는 것은 아니다 — 같은 차원에 섞인다"], bot)

s = d.slide("Sinusoidal 위치 인코딩", lead="차원 쌍마다 다른 주파수의 sin/cos — 파장은 2π부터 10000·2π까지 기하급수", stage="계산",
            notes="§3.5: PE(pos, 2i) = sin(pos / 10000^(2i/d_model)), PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model)). 'The wavelengths form a geometric progression from 2π to 10000·2π.' "
                  "(d = 512에서 가장 긴 실제 파장은 2π·10000^(510/512) ≈ 60,611; 10000·2π ≈ 62,832는 극한값.) "
                  "i가 커질수록 주파수가 낮아져 천천히 변한다 — 시계의 초침·분침·시침처럼 여러 속도의 바늘로 위치를 표현. "
                  "d = 8 표(검산): pos 1 = (0.841, 0.540, 0.100, 0.995, 0.010, 1.000, 0.001, 1.000), pos 2 = (0.909, −0.416, 0.199, 0.980, 0.020, 1.000, 0.002, 1.000). "
                  "학습 파라미터 없음(v2+ 기여 각주: 'parameter-free position representation'). 그림은 d = 64 · 32. 출처: Vaswani et al. §3.5; 검산 week5.md.")
top, bot = s.area.top(1.5, gap=0.25)
s.formula(["PE(pos, 2i)   = sin( pos / 10000^(2i/d) )", "PE(pos, 2i+1) = cos( pos / 10000^(2i/d) )"], top, size=21)
L, R = bot.cols(0.62, gap=0.35)
s.image(A("week5/pe.png"), L)
s.table(["d = 8", "차원 0", "차원 1", "차원 2", "차원 3"], [["pos 1", "0.841", "0.540", "0.100", "0.995"],
                                                     ["pos 2", "0.909", "−0.416", "0.199", "0.980"]], Box(R.x, R.y, R.w, 1.65), widths=[0.95, 1, 1.15, 1, 1], size=14, min_size=12, align="ccccc")
s.bullets(["표는 d = 8 (그림은 d = 64 · 32)", "i가 클수록 **느리게** 변한다", ("시계의 초침 · 분침 · 시침", 1), "학습 파라미터 **없음**"],
          Box(R.x, R.y + 1.85, R.w, R.h - 1.85), size=15)

s = d.slide("왜 sin/cos 쌍인가 — 원문의 가설", lead="고정 offset k에 대해 PE_(pos+k)는 PE_pos의 선형 함수 — “상대 위치로 attend하기 쉬울 것”이라는 가설",
            stage="아이디어",
            notes="§3.5: 'We chose this function because we hypothesized it would allow the model to easily learn to attend by relative positions, since for any fixed offset k, PE_(pos+k) can be represented as a linear function of PE_pos.' — 가설(hypothesized). "
                  "검산: 각 차원 쌍 (2i, 2i+1)에 2×2 회전행렬 R_i(k) = [[cos ω_i k, sin ω_i k], [−sin ω_i k, cos ω_i k]] (ω_i = 1/10000^(2i/d))을 적용하면 "
                  "PE_(pos+k) = R(k)·PE_pos가 pos와 무관하게 성립(d = 8, k = 3, pos = 5와 11에서 확인). 이것이 sin과 cos를 '쌍'으로 쓰는 이유. "
                  "두 번째 이유(v2+): 학습보다 긴 길이로 '외삽할 수도 있기(may)' 때문 — 보장이 아니라 기대. "
                  "회전으로 위치를 다루는 아이디어는 이후 RoPE(2021)로 이어진다(후속 변형, 이번 주 범위 밖). 출처: Vaswani et al. §3.5 (v2+ 문장 포함); 검산 week5.md.")
top, bot = s.area.top(1.3, gap=0.3)
s.formula(["[ PE(pos+k, 2i), PE(pos+k, 2i+1) ] = R_i(k) · [ PE(pos, 2i), PE(pos, 2i+1) ]",
           "R_i(k) = [[cos ω_i k, sin ω_i k], [−sin ω_i k, cos ω_i k]],  ω_i = 1 / 10000^(2i/d)"], top, size=17)
rest = s.cards([{"head": "이유 ① 상대 위치 (§3.5)", "bullets": True,
                 "body": ["offset k만큼 이동 = 쌍마다 **회전** R(k)", "R(k)는 pos와 **무관** — 검산: d = 8, k = 3, pos = 5 · 11",
                          "원문 표현: **“we hypothesized”** — 가설"]},
                {"head": "이유 ② 외삽 (v2+)", "tone": "accent", "bullets": True,
                 "body": ["학습보다 긴 길이에 **“may”** extrapolate", "값을 **계산할 수 있다** ≠ 긴 길이에 **일반화한다**",
                          "회전 아이디어 → 이후 RoPE (2021)"]}], bot, cols=2, body_size=16, head_size=18)

s = d.slide("결과: 학습형 위치와 “거의 같다” — Table 3 (E)", lead="위치 단서가 필요하다는 것과 특정 함수가 필수라는 것은 다른 주장", stage="결과",
            notes="§3.5 (NIPS판/arXiv v2+): 'We also experimented with using learned positional embeddings [9] instead, and found that the two versions produced nearly identical results (see Table 3 row (E)).' "
                  "[9]는 ConvS2S(Gehring et al. 2017). Table 3 (E): 학습형 위치 임베딩 PPL 4.92, BLEU 25.7 vs base(sinusoid) PPL 4.92, BLEU 25.8. "
                  "v1에는 이 문장도 (E) 행도 없다. 이후 상대 위치(Shaw et al. 2018), RoPE(2021), ALiBi(2021) 등 다양한 방식이 쓰인다(후속 변형 — 이번 주 노트 범위 밖이라 수치 없음). "
                  "Parikh(2016)의 거리 편향 d_(i−j)는 상대 위치 편향의 이른 사례(Part 3). "
                  "공정한 실험: 순수 self-attention 모듈에 순열을 적용해 등변성을 확인하고, 전체 모델에서는 source와 target 위치 정보를 따로 제거한 조건을 비교한다(ConvS2S Table 4처럼). "
                  "출처: Vaswani et al. §3.5, Table 3 (E) (v2+); Gehring et al. §3.1, Table 4; Parikh et al. §3.4.")
L, R = s.cols(0.42, gap=0.45)
s.table(["Table 3 (영→독 dev)", "PPL", "BLEU"], [["base: sinusoid", "4.92", "**25.8**"], ["(E) 학습형 위치 임베딩", "4.92", "**25.7**"]],
        Box(L.x, L.y, L.w, 1.5), widths=[2.8, 1.0, 1.0], size=15, align="lcc")
s.callout("“nearly identical results” — NIPS판 / arXiv v2+에만 있는 문장과 행", Box(L.x, L.y + 1.75, L.w, 1.0), kind="tip", size=15)
s.bullets(["sinusoid를 고른 이유: **외삽 가능성(may)**", "학습형 비교 대상 [9] = **ConvS2S**"], Box(L.x, L.y + 3.0, L.w, L.h - 3.0), size=15)
s.table(["방식", "아이디어", "예"], [["고정 sinusoidal", "주파수가 다른 sin/cos를 더한다", "Transformer (2017)"],
                                    ["학습형 절대 위치", "위치마다 학습되는 벡터를 더한다", "**ConvS2S (2017)**, Table 3 (E)"],
                                    ["상대 위치 · 거리 편향", "두 토큰의 **거리**를 점수에 반영", "Parikh (2016) d_(i−j), Shaw (2018)"],
                                    ["회전 · 편향 방식", "Q · K를 위치만큼 회전 / 거리 비례 편향", "RoPE (2021), ALiBi (2021)"]],
        Box(R.x, R.y, R.w, 3.3), widths=[2.2, 3.4, 2.6], size=14)

# ============================================================ Part 6 — Vaswani §4
d.part(6, "Vaswani 2017 §4: 왜 self-attention인가", "경로는 짧아졌다 — 대신 무엇을 냈나?",
       notes="Part 6은 같은 논문의 §4 'Why Self-Attention' Table 1과 전체 구조 정리. 출처: Vaswani et al. §4 Table 1, §3.1, Table 2.")

s = d.slide("§4 Table 1: 세 층의 비교", lead="경로 길이 O(1) · 순차 연산 O(1) — 대신 층당 비용 O(n² · d)",
            stage="결과",
            notes="§4 Table 1 (n = 시퀀스 길이, d = 표현 차원, k = 커널, r = 이웃 크기): Self-Attention O(n²·d) / O(1) / O(1); Recurrent O(n·d²) / O(n) / O(n); "
                  "Convolutional O(k·n·d²) / O(1) / O(log_k n); Self-Attention (restricted) O(r·n·d) / O(1) / O(n/r). "
                  "§4: 'n < d일 때(당시 word-piece/BPE 문장 표현에서 흔함) self-attention이 recurrent보다 빠르다' — 즉 n²·d 비용은 공짜가 아니다. 긴 시퀀스는 restricted attention을 향후 과제로. "
                  "합성곱의 O(log_k n)은 dilated 합성곱 기준이고, 연속 커널이면 O(n/k)층(§4 본문). "
                  "'순차 연산 O(1)'은 층 내부·학습 시 이야기다 — 자기회귀 생성(§3)은 여전히 토큰 하나씩 순차적이다. "
                  "그림은 Table 1의 최대 경로 길이를 옮긴 개념도. 출처: Vaswani et al. §3, §4, Table 1, §7.")
top, bot = s.area.top(2.2, gap=0.2)
s.table(["층 종류", "층당 복잡도", "순차 연산", "최대 경로 길이"],
        [["**Self-Attention**", "**O(n² · d)**", "**O(1)**", "**O(1)**"], ["Recurrent", "O(n · d²)", "O(n)", "O(n)"],
         ["Convolutional", "O(k · n · d²)", "O(1)", "O(log_k n)"], ["Self-Attention (restricted)", "O(r · n · d)", "O(1)", "O(n / r)"]],
        top, widths=[3.6, 2.8, 2.4, 2.8], size=15, align="lccc", highlight=[0])
L, R = bot.cols(0.72, gap=0.3)
s.image(A("week5/paper_path_length.png"), L)
s.bullets(["n < d일 때 recurrent보다 빠르다 (§4)", ("긴 n에선 **n²** 비용 → restricted는 향후 과제", 1),
           "O(1) 순차는 **층 내부 · 학습** 이야기", ("생성은 여전히 **토큰 하나씩**", 1)], R, size=14)

s = d.slide("모아 보기: 2017 Transformer — 오늘 배운 곳", lead="Encoder 6층 + Decoder 6층 — 오늘은 입력과 attention, 다음 주는 나머지 전부", stage="정리",
            notes="§3.1: 인코더 N = 6, 디코더 N = 6. 각 sub-layer 출력은 LayerNorm(x + Sublayer(x)), d_model = 512. 층마다 파라미터는 별개(같은 설계 반복 ≠ 가중치 공유). "
                  "base: d = 512, h = 8, d_k = 64, d_ff = 2048(§3.3). v1 Table 3 base 행은 d_ff를 1024로 오기했으니 v1 PDF를 보면 혼동 주의. "
                  "Table 2 (newstest2014 BLEU): big 28.4 (영→독, ConvS2S 25.16, GNMT+RL 24.6), 영→불 big 41.0 (v1–v4) → 41.8 (v5+, 본문은 41.0으로 남음). "
                  "base 학습: 8×P100에서 100K step 약 12시간(§5). "
                  "오늘 배운 것: 임베딩 + 위치 인코딩, multi-head self-attention, encoder-decoder attention의 개념, mask의 원리. "
                  "다음 주: FFN, residual + LayerNorm, 학습(teacher forcing, label smoothing, warmup)과 생성. "
                  "출처: Vaswani et al. §3.1, §3.3, §5, Table 2–3 (v1 vs v2+).")
L, R = s.cols(0.5)
s.image(A("week5/transformer_arch.png"), L)
rest = s.card(R, "오늘 배운 것 ✔", ["Embedding + **위치 인코딩** (§3.4–3.5)", "**Multi-head self-attention** (§3.2)",
                                  "encoder-decoder attention · mask (§3.2.3)"], tone="teal", bullets=True, fit_h=True)
rest = s.card(rest, "다음 주", ["FFN · **Residual + LayerNorm** (§3.1, §3.3)", "학습 · 생성 (§5)"],
              tone="accent", bullets=True, fit_h=True)
s.bullets(["base: d = 512, h = 8, d_k = 64, d_ff = 2048 (v1 표의 1024는 오기)", "Table 2: 영→독 **28.4** BLEU (big)"], rest, size=15)

# ============================================================ Part 7 — 해석 논쟁
d.part(7, "2019: attention은 설명인가?", "heatmap이 보여 주는 것과 증명하지 않는 것",
       notes="Part 7은 attention 가중치를 설명으로 읽어도 되는지에 대한 2019년의 반박(Jain & Wallace, NAACL)과 재반박(Wiegreffe & Pinter, EMNLP). 두 논문 모두 BiLSTM attention 분류기 대상. 출처: week5.md [Jain2019], [Wiegreffe2019].")

d.paper("Jain & Wallace (2019) · Wiegreffe & Pinter (2019)", "Attention is not Explanation · Attention is not not Explanation",
        "NAACL 2019 · EMNLP-IJCNLP 2019",
        "“attention 가중치 = 입력의 중요도”라는 암묵적 가정은 **검증된 적이 없다**",
        "J&W: 중요도 지표와의 상관 + attention을 **바꿔도** 예측이 그대로인지. W&P: 그 실험의 설계와 ‘설명’의 정의를 다시 따진다",
        "J&W §1 (Fig. 1), §6 · W&P §2.1, §3.2 (Table 2), §6",
        result="두 논문 모두 **BiLSTM attention 분류기** 대상 — Transformer multi-head나 번역은 다루지 않았다",
        notes="Jain & Wallace, NAACL-HLT 2019, arXiv:1902.10186 (v3). Wiegreffe & Pinter, EMNLP-IJCNLP 2019, arXiv:1908.04626 (v2). "
              "J&W §1: 충실한(faithful) 설명이라면 (i) gradient·leave-one-out(LOO) 같은 특징 중요도와 상관해야 하고, (ii) 다른 attention 분포는 다른 예측을 낳아야 한다. "
              "J&W §6: seq2seq(번역)는 다루지 않았다, 결과는 특히 RNN 인코더에 대한 것. W&P: 두 논문 모두 RNN(LSTM) attention 대상. "
              "출처: Jain & Wallace §1, §2, §6; Wiegreffe & Pinter Abstract, §2.")

s = d.slide("Jain & Wallace: 바꿔도 예측이 그대로라면?", lead="상관은 약하고, 전혀 다른 attention으로도 같은 예측이 나온다 — “설명으로 취급하지 말라”",
            stage="결과",
            notes="방법(§2, §4): BiLSTM(+ 비교용 단순 평균 인코더, CNN) 위의 additive 또는 scaled dot-product attention으로 분류, QA, NLI. "
                  "(1) attention과 gradient/LOO 중요도의 Kendall τ. (2) attention을 무작위로 치환하거나, 예측을 거의 바꾸지 않으면서 원래와 최대한 다른 적대적 분포를 인스턴스별로 탐색. "
                  "Table 2: BiLSTM에서 attention–gradient τ_g 평균은 대체로 0.1–0.47 (예: SST 0.40, IMDB 0.37, 20News 0.08, CNN 0.20, SNLI 0.36–0.42). 평균(비순환) 인코더에서는 0.48–0.84로 더 높다. "
                  "Figure 1: 부정 영화 리뷰에서 원래 attention('waste')과 전혀 다른 적대적 attention('was')이 같은 예측 0.01. τ_g = 0.29, 무작위 치환 시 출력 변화 중앙값 0.006. "
                  "결론(Abstract): 'standard attention modules do not provide meaningful explanations and should not be treated as though they do'. "
                  "저자가 밝힌 한계(§6): gradient/LOO가 정답은 아니다; 소수의 attention 변형만; seq2seq 미포함; 적대적 가중치는 모델 파라미터 아래에서 '있을 법하지 않을' 수 있다. "
                  "출처: Jain & Wallace (2019) Abstract, §1, §2, §4, §6, Table 2, Figure 1.")
L, R = s.cols(0.5, gap=0.45)
s.table(["데이터 (BiLSTM)", "attention–gradient τ_g"], [["SST", "0.40"], ["IMDB", "0.37"], ["20News", "0.08"], ["CNN (QA)", "0.20"],
                                                       ["SNLI", "0.36–0.42"], ["평균 인코더 (비교)", "0.48–0.84"]],
        Box(L.x, L.y, L.w, 3.0), size=15, align="lc", widths=[2.8, 2.6], highlight=[5])
s.textbox("Kendall τ: 두 순위가 얼마나 같은지 (1 = 완전히 같음, 0 = 무관)", Box(L.x, L.y + 3.15, L.w, 0.7), size=14, color=GRAY)
rest = s.card(R, "Figure 1의 예 (부정 영화 리뷰)", ["원래 attention: **“waste”**에 집중 → 예측 0.01", "적대적 attention: **“was”**에 집중 → 예측 **0.01**",
                                               "무작위 치환 시 출력 변화 중앙값 0.006"], tone="accent", bullets=True, fit_h=True, body_size=15)
s.card(rest, "저자가 밝힌 한계 (§6)", ["gradient · LOO도 정답은 아니다", "**번역(seq2seq) · Transformer는 다루지 않음**",
                                     "적대적 분포는 모델이 실제로 낼 법하지 않을 수 있다"], tone="plain", bullets=True, fit_h=True, body_size=15)

s = d.slide("Wiegreffe & Pinter: 존재는 배타성을 뜻하지 않는다", lead="attention은 ‘유일한(the)’ 설명이 아니라 ‘하나의(an)’ 설명 — 반증되지는 않았다",
            stage="결과",
            notes="W&P §2.1: J&W는 attention 분포를 그것을 계산한 파라미터에서 떼어 내 인스턴스마다 따로 조작했다 → 그런 분포를 내는 적대적 '모델'이 존재한다는 것은 보이지 못했다. "
                  "'Existence does not entail exclusivity': attention은 the explanation이 아니라 an explanation을 준다. "
                  "진단 네 가지(§3–4): (1) uniform attention 기준선 — Table 2: SST 0.831→0.822, AgNews 0.964→0.960, IMDb 0.902→0.879, Diabetes 0.775→0.706. "
                  "균등으로 고정해도 성능이 거의 같은 과제에선 애초에 attention 조작이 설명 문제의 증거가 되지 못한다. (2) 랜덤 시드 분산 보정. "
                  "(3) 학습된 attention을 고정 가중치로 쓰는 비문맥 MLP 진단. (4) 모델 단위로 학습하는 적대적 attention. "
                  "결과: 모델 일관적인 적대적 분포는 찾을 수 있지만 J&W만큼 극단적이지 않고 진단 MLP에서 성능이 나쁘다 → 'prior work does not disprove the usefulness of attention mechanisms for explainability'(Abstract). "
                  "동시에 §6: LSTM의 일부 분류 과제에서 적대적 분포가 존재함을 확인했다 — 'one true, faithful' 설명을 찾는 연구자는 멈칫해야 한다. plausible(그럴듯한) vs faithful(충실한) 구분(§5–6). "
                  "흔한 오해: 제목처럼 'attention은 설명이다'로 결론 낸 것이 아니다. 출처: Wiegreffe & Pinter (2019) Abstract, §2.1, §3–4, Table 2, §5–6.")
L, R = s.cols(0.55)
s.image(A("week5/paper_wp_uniform.png"), L)
s.bullets(["J&W는 분포를 **모델에서 떼어 내** 조작했다 (§2.1)", "균등으로 고정해도 거의 같은 과제 → attention이 **애초에 중요하지 않은** 과제",
           "모델 단위 적대적 학습: 가능하지만 덜 극단적", "**plausible**(그럴듯) vs **faithful**(충실) 구분", "결론: “반증되지 않았다” — ‘설명이다’가 아니다"],
          R, size=15)

s = d.slide("attention 지도를 읽는 네 단계", lead="관찰 → 상관 → 개입 → 대조군 — 큰 α ≠ 큰 영향",
            stage="정리",
            notes="두 논문의 논쟁을 실천 지침으로 정리(week5.md W&P 슬라이드 사용 제안). "
                  "① 관찰: heatmap에서 큰 α — '그 위치에 큰 참조 비중이 관찰되었다'고만 말한다(Bahdanau Fig. 3, Vaswani 부록 Fig. 3–5가 여기에 해당; Vaswani는 'apparently' 등 조심스러운 표현도 쓴다). "
                  "② 상관: gradient·LOO 같은 다른 중요도 지표와 순위가 맞는가(J&W τ). ③ 개입: 그 위치를 가리거나 attention을 바꿔 출력이 변하는가(J&W 치환·적대적 분포, W&P 모델 단위 적대적 학습). "
                  "④ 대조군: uniform attention 기준선, 시드 분산(W&P). "
                  "Transformer에서 추가로: α가 커도 V의 크기·방향이 다르고, 뒤에 W^O, residual, FFN, 다음 층이 있어 가중치 숫자 하나로 최종 출력 변화를 알 수 없다. "
                  "또 두 2019 논문은 BiLSTM 분류기 대상이므로 결론을 Transformer head에 그대로 옮기면 안 된다 — 같은 질문을 Transformer에서 따로 검증해야 한다. "
                  "출처: Jain & Wallace §1, §4; Wiegreffe & Pinter §3–4; Vaswani §4, 부록 Fig. 3–5; Bahdanau §5.2.1.")
top, bot = s.area.top(2.0, gap=0.3)
s.flow([{"head": "① 관찰", "body": "heatmap의 큰 α\n“비중이 관찰됨”"}, {"head": "② 상관", "body": "gradient · LOO와\n순위가 맞나 (τ)"},
        {"head": "③ 개입", "body": "가리기 · 바꾸기 →\n출력이 변하나", "tone": "accent"},
        {"head": "④ 대조군", "body": "uniform 기준선 ·\n시드 분산", "tone": "dark"}], top, body_size=15, head_size=17, gap=0.4)
L, R = bot.cols(0.5, gap=0.4)
s.card(L, "Transformer에서 더 조심할 것", ["α가 커도 **V의 크기 · 방향**이 다르다", "뒤에 W^O · residual · FFN · 다음 층",
                                         "저자의 head 해석(부록)은 ①단계 — 정성적 그림"], tone="plain", bullets=True, body_size=16, fit_h=True)
s.card(R, "두 2019 논문의 범위", ["**BiLSTM** attention 분류기 · QA · NLI", "Transformer multi-head · 번역은 **다루지 않음**",
                                 "→ Transformer에서는 **따로** 검증해야"], tone="accent", bullets=True, body_size=16, fit_h=True)

# ============================================================ 마무리
d.summary(["Bahdanau (2014/ICLR 2015): 출력마다 다른 문맥 c_t = Σ α h_j — 긴 문장에서도 버팀, 단 전체 BLEU는 Moses 아래",
           "Luong (2015): 현재 h_t로 정렬, global/local, 점수 함수 **4종 비교** — 최고 단일은 local-p + general",
           "Self-attention(2016)과 순환 없는 ConvS2S(2017)가 **먼저** 있었다 — Transformer는 **조합**",
           "§3.2: softmax(QKᵀ/√d_k)V, √d_k는 관찰 + 추측 + 가정 · W^O는 NIPS판(v2+) · Table 3(A): h=1은 0.9 낮음",
           "§3.5: self-attention은 순서를 모른다 → sinusoid PE (학습형과 거의 같음, Table 3 E) · §4: 경로 O(1), 비용 O(n²·d)",
           "2019: attention 지도는 **관찰**이다 — 설명이라 하려면 상관 · 개입 · 대조군이 필요"])

d.quiz("셀프 체크 ①", [("Bahdanau와 Luong은 정렬 점수에 디코더의 어떤 상태를 쓰나?", "Bahdanau는 직전 상태 s_(t−1), Luong은 현재 상태 h_t (Luong §3.1)"),
                     ("Bahdanau Table 1에서 RNNsearch는 Moses를 이겼나?", "전체 test에서는 아니다(28.45 vs 33.30). UNK 없는 문장에서만 36.15 vs 35.63"),
                     ("Q: (B, H, T, d_h), K: (B, H, S, d_h)일 때 QKᵀ의 shape은?", "(B, H, T, S) — d_h는 내적하며 사라진다"),
                     ("4토큰 예제에서 mask 후 Query B의 가중치는?", "C, D를 −∞로 막아 softmax(0, 0.707) = [0.33, 0.67, 0, 0]")],
       notes="출처: Luong §3.1; Bahdanau Table 1, §5.1; Vaswani §3.2.1–3.2.3; 4토큰 예제 검산(week5.md).")

d.quiz("셀프 체크 ②", [("√d_k로 나누는 근거는 증명인가?", "아니다. Britz et al.의 관찰 → 저자의 ‘We suspect’ → 각주(v2+)의 독립·분산 1 가정 하 계산"),
                     ("d를 고정하고 head 수를 1에서 8로 늘리면 파라미터와 BLEU는?", "주요 파라미터 ≈ 4d²는 그대로, Table 3(A) dev BLEU 24.9 → 25.8"),
                     ("self-attention의 층당 복잡도와 최대 경로 길이는? (Table 1)", "복잡도 O(n²·d), 경로 O(1) — n < d일 때 recurrent보다 빠르다"),
                     ("Jain & Wallace의 결과를 Transformer head에 그대로 적용해도 되나?", "안 된다 — BiLSTM attention 분류기 대상이고 Transformer·번역은 다루지 않았다")],
       notes="출처: Vaswani §3.2.1 + 각주 4, Table 3 (A), §4 Table 1; Jain & Wallace §2, §6.")

d.misconceptions([["“Attention은 Bahdanau가, self-attention은 Transformer가 발명”", "가중 정렬은 Graves 2013 · NTM 2014, intra-attention은 Cheng · Parikh 2016. 2017년은 **조합**"],
                  ["“Luong attention = dot attention”", "location · dot · general · concat을 **비교**. 최고 단일은 local-p + **general**"],
                  ["“RNNsearch가 Moses를 이겼다”", "전체 test BLEU 28.45 < **33.30**. UNK 없는 문장에서만 앞섬"],
                  ["“√d_k는 증명된 최적 스케일”", "관찰 + **“We suspect”** + 가정 하 분산 계산 (각주는 v2+)"],
                  ["“W^O는 원래 식에 있었다” · “× √d_model은 PE와 크기 맞추기”", "W^O는 **v2부터**. √d_model 곱셈은 **이유가 원문에 없다** (§3.4)"],
                  ["“sinusoid라야 한다 · 외삽을 보장한다”", "학습형과 **거의 같음** (25.7 vs 25.8), 외삽은 “may” 수준"],
                  ["“Attention 지도 = 모델의 설명”", "관찰일 뿐. J&W · W&P 모두 **BiLSTM** 대상 — 상관 · 개입 · 대조군으로 검증"]],
                 notes="출처: Bahdanau §6.1, Table 1; Luong §3.1, Table 4; Cheng §3; Parikh §3.4; Vaswani §3.2.1 각주 4, §3.2.2, §3.4, §3.5, Table 3 (v1 vs v2+); Jain & Wallace §6; Wiegreffe & Pinter §6.")

d.homework([("원문 읽기 ①  Bahdanau §3.1 + Table 1", "식 (4)–(6)을 강의 표기로 옮겨 쓰고, ‘attention’이라는 단어가 나오는 문장을 찾아 적는다. "
                                               "Table 1에서 All과 No UNK 열이 왜 다른 결론을 주는지 3문장으로 제출."),
            ("원문 읽기 ②  Vaswani §3.2.1 + Table 3", "√d_k 문단을 ‘관찰 / 추측 / 가정’으로 나눠 표시한다(v1과 v2+ PDF를 둘 다 열어 각주 4 유무 확인). "
                                                   "Table 3 (A)·(E) 수치를 표로 옮기고 한 줄 해석. 덤: 4토큰 예제에서 √2를 빼고 Query A를 다시 계산."),
            ("원문 읽기 ③  Jain & Wallace §1 · Wiegreffe & Pinter §2.1", "각 논문의 주장을 한 문장씩, 그리고 두 논문이 ‘다루지 않은 것’을 하나씩 적는다. "
                                                                    "attention 지도를 보고 쓴 문장 하나를 네 단계(관찰·상관·개입·대조군)로 고쳐 쓴다.")],
           notes="세 과제 모두 원문의 특정 절·표를 읽고 제출물이 분명하다. 숙제 ②의 덤 정답: 스케일을 빼면 A 첫 행 = (0.399, 0.147, 0.399, 0.054) — 더 뾰족해진다(week5.md 검산). "
                 "PDF: arxiv.org/abs/1409.0473 (Bahdanau), arxiv.org/abs/1706.03762 (v1과 v2 이상을 'v1'·'v2' 링크로 비교), arxiv.org/abs/1902.10186, arxiv.org/abs/1908.04626.")

d.references([["Bahdanau, Cho & Bengio (2014/ICLR 2015). Neural Machine Translation by Jointly Learning to Align and Translate. arXiv:1409.0473", "§3.1, Fig. 2–3, Table 1, App. A.1.2"],
              ["Graves, Wayne & Danihelka (2014). Neural Turing Machines. arXiv:1410.5401", "§3.1, §3.3.1 (Eq. 5–6)"],
              ["Luong, Pham & Manning (2015). Effective Approaches to Attention-based NMT. EMNLP. arXiv:1508.04025", "§3.1, Table 4"],
              ["Cheng, Dong & Lapata (2016). LSTM-Networks for Machine Reading. EMNLP · Parikh et al. (2016). Decomposable Attention. EMNLP", "Cheng §3 · Parikh §3.1, §3.4, Table 1"],
              ["Gehring et al. (2017). Convolutional Sequence to Sequence Learning. ICML. arXiv:1705.03122", "§3.1, §3.3, Table 4"],
              ["Vaswani et al. (2017). Attention Is All You Need. NIPS. arXiv:1706.03762 (v1 vs v2+)", "§3.2 (Fig. 2), §3.4–3.5, §4 Table 1, Table 3"],
              ["Jain & Wallace (2019). Attention is not Explanation. NAACL · Wiegreffe & Pinter (2019). Attention is not not Explanation. EMNLP", "J&W §1, §6 · W&P §2.1, Table 2, §6"]],
             notes="원문은 표에 적은 절과 그림·표만 먼저 읽는다. Vaswani는 판본에 따라 W^O, √d_k 각주, 학습형 PE 비교 유무가 다르므로 인용할 때 'NIPS 2017 / arXiv v2+'라고 적는다. "
                   "학회 쪽수는 원문 PDF에 없는 경우가 있어 생략했다. 출처: week5.md 각 논문 서지.")

d.handoff(["출력마다 원문을 **다시 참조**하는 attention (2014–2015)", "Q · K · V · scaled dot-product ·\nmulti-head · 위치 인코딩 (§3.2, §3.5)",
           "경로 O(1)의 대가 O(n²·d) (§4)"],
          ["attention만으로는 **토큰별 비선형 변환**이 없다", "깊게 쌓으려면? 정답을 **훔쳐보지 않고** 학습하려면? **생성**은?"],
          ["**부품을 모아**", "**전체 Transformer를 조립하면?**", "FFN · Residual · LayerNorm · Mask · 학습 · 생성"],
          notes="다음 주(Week 6): 오늘의 attention 블록에 position-wise FFN, residual, LayerNorm을 붙여 층을 완성하고(Vaswani §3.1, §3.3), "
                "mask와 teacher forcing으로 디코더를 학습시키고(§5), 토큰을 하나씩 생성한다 — 전체 Transformer 조립.")

d.save(OUT)
print("saved", OUT, d.n + 2, "slides")
