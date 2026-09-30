# Week 4 연구 노트 — 언어·순서·기억: Word2Vec, RNN, LSTM, Seq2Seq (2026-10-26)

빌드 스크립트 `build/week4.py`가 이 노트를 그대로 옮긴다(슬라이드별 발표자 노트 전문은 스크립트의 `notes=`에 있다).

## 1. 원자료 범위와 소제목 커버리지 (source.txt 줄 번호)

| 줄 | 소제목 (`##`) | 슬라이드 |
|---|---|---|
| 160–162 | 시간·일반화·기억·공간을 다루는 여러 길 (Elman RNN, LSTM, forget gate 후속) | 2 타임라인, 17 Jordan/Elman, 27 게이트(1997 vs 2000) |
| 166–168 | 분산 표현과 깊은 모델의 학습 (2003 신경 언어 모델) | 12 NPLM |
| 172–174 | AlexNet과 Word2Vec (Embedding은 Word2Vec이 처음 아님) | 9, 10, 12, 37 |
| 178–180 | Encoder–Decoder와 Attention (Seq2Seq·Bahdanau 거의 동시기, 가변 길이·조건부 생성) | 32–35, 요약 |
| 830–831 | 언어를 벡터로 바꾸기 | Part 01 표지(4), 5 |
| 834–867 | 번호는 의미가 아니다 (E∈R^{|V|×d}, x_i=E[id_i], one-hot@E = lookup) | 6, 7, 20 |
| 869–889 | 단어와 토큰은 항상 같지 않다 (Word/Char·Byte/Subword 표, tokenizer–가중치 짝) | 8 |
| 891–895 | Word2Vec에서 배울 것 (CBOW/Skip-gram, 차원≠사람 의미, 정적 임베딩의 bank 문제) | 9, 10, 15 |
| 897–973 | 문장을 생성하는 것은 조건부 확률의 연결 (∏p(y_t|y_<t), p(y|x), 자기지도, 목표≠아키텍처) | 13, 14 |
| 975–980 | Contextual representation은 어디에서 달라질까 (+토큰화 실습 주의) | 15, 8(노트) |
| 985–986 | RNN과 LSTM: 순서와 기억 (유지 문제 vs 순차 계산 문제 구분) | Part 03 표지(16) |
| 989–1025 | 이전 상태가 다음 상태로 전달된다 (h_t = tanh(x_t W_x + h_{t−1} W_h + b)) | 18, 19, 20 |
| 1027–1085 | 장기 의존성이 어려운 두 이유 (학습 신호·정보 표현 + 계산 의존성 표, Jacobian 곱) | 21, 22, 23, 24 |
| 1087–1262 | LSTM: 보존·쓰기·읽기를 조절하기 (게이트 식, c/h 구분, 한계) | 26, 27, 28, 29 |
| 1264–1269 | 간단한 사고실험 (+ Gate 수식을 외워야 하나요?) | 30, 29(노트) |
| 1274–1318 | Seq2Seq에서 Attention으로 / 길이가 달라도 입력과 출력을 연결하기 | 31, 32, 33, 34 |
| 1320–1322 (예고만) | 병목: 질문이 달라져도 요약본은 하나 — Attention 계산은 5주차 | 35, 40 |
| 3804–3869 | 오개념 #1, #4, #5 (+ Embedding 표에 의미 전부 저장, LSTM 완벽 기억) | 36, 37 |
| 3906–3908 | 개념 확인 03 | 36 Q1 |
| 3569–3689 | 멘토링 4·5회차: Token ID·Embedding·다음 토큰 쌍 / 복사·반전 과제 설계 | 38 과제 |
| 82643(HTML teacher) | 수업의 전환 질문(문장 전체를 5개 숫자로 요약) | 35 |

## 2. 검증한 사실 (연도·인물·논문)
- **1986 Jordan**, "Serial Order: A Parallel Distributed Processing Approach", ICS Report 8604, UC San Diego — 출력을 상태로 되먹임(Jordan network). (웹 확인)
- **1990 Elman**, "Finding Structure in Time", *Cognitive Science* 14(2) — 은닉 상태를 context unit으로 복사해 되먹임 [06].
- **1990 Werbos**, "Backpropagation Through Time: What It Does and How to Do It" — BPTT 정리(노트에서만 언급).
- **1991 Hochreiter** 학위논문(Diplomarbeit, TU München) — 기울기 소실 분석. **1994 Bengio, Simard & Frasconi**, "Learning Long-Term Dependencies with Gradient Descent is Difficult", *IEEE TNN* 5(2).
- **1997 Hochreiter & Schmidhuber**, "Long Short-Term Memory", *Neural Computation* 9(8) [08]. 원형에는 forget gate 없음.
- **2000 Gers, Schmidhuber & Cummins**, "Learning to Forget" — forget gate 도입 [09]. 강의 식은 이 후속 형태.
- **2003 Bengio, Ducharme, Vincent & Jauvin**, "A Neural Probabilistic Language Model", *JMLR* 3 — 단어 특징 벡터(공유 행렬 C)와 다음 단어 확률을 함께 학습 [11]. → "Word2Vec이 Embedding 발명"은 오개념 #4.
- **2013 Mikolov, Chen, Corrado & Dean**, "Efficient Estimation of Word Representations in Vector Space" (arXiv 1301.3781, 2013-01) — CBOW/Skip-gram, king − man + woman ≈ queen 예시 [14].
- **2013 Pascanu, Mikolov & Bengio**, "On the difficulty of training RNNs" (ICML) — gradient clipping(노트).
- **2014-06 Cho et al.**, "Learning Phrase Representations using RNN Encoder–Decoder" (EMNLP 2014) — RNN Encoder–Decoder, reset/update gate 유닛(이후 GRU로 불림) [15].
- **2014-09 Sutskever, Vinyals & Le**, "Sequence to Sequence Learning with Neural Networks" (NIPS 2014) — 4층 LSTM, 입력 순서 뒤집기, WMT'14 En→Fr BLEU 34.8(LSTM 5개 앙상블 직접 번역), SMT 1000-best 재순위화 36.5 [16]. (웹 확인)
- **2014-09 Bahdanau, Cho & Bengio** (ICLR 2015) — 고정 길이 벡터 병목 → 정렬 학습. 5주차에서 다룸. Seq2Seq와 거의 동시기 공개 [17].

## 3. 수식과 수치 예제 (행벡터 관례)
- Embedding: `E ∈ R^{|V|×d}`, `x_i = E[id_i]`; |V|=5, d=3, id=3 → one-hot [0,0,0,1,0] @ E = E[3] = [0.7, −0.1, 0.6].
- 조건부 확률 연결: `p(y_1..y_T) = ∏ p(y_t | y_<t)`; 0.2 × 0.3 × 0.6 = 0.036, −log 0.036 ≈ 3.32.
- 조건부 생성: `p(y|x) = ∏ p(y_t | y_<t, x)`; "I am a student" → [나는, 학생, 이다, EOS] 학습 쌍 4개.
- RNN: `h_t = tanh(x_t W_x + h_{t−1} W_h + b)`; 스칼라 W_x=1, W_h=0.5, b=0, x=(1,0,0) → h = 0.762, 0.364, 0.180.
- 기울기 곱: `∂h_t/∂h_{t−k} = ∏_{j=t−k+1}^{t} ∂h_j/∂h_{j−1}`; 0.9^10 ≈ 0.349, 0.9^50 ≈ 0.0052, 1.1^50 ≈ 117.
- LSTM: `c_t = f_t⊙c_{t−1} + i_t⊙g_t`, `h_t = o_t⊙tanh(c_t)`; c_{t−1}=2.0, f=0.9, i=0.2, g=0.5 → c_t=1.9; o=0.6 → h_t = 0.6·tanh(1.9) ≈ 0.574.

## 4. 슬라이드 개요 (본문 40장 + 표지 + Question)
1 지난 주 복습(cards) · 2 오늘의 위치(timeline 1986→2014) · 3 학습 목표(cards)
**Part 01 언어를 벡터로** 4 표지 · 5 텍스트→벡터 파이프라인(flow) · 6 번호는 의미가 아니다(formula) · 7 one-hot@E=lookup(image) · 8 단어와 토큰(table) · 9 Word2Vec CBOW vs Skip-gram(compare) · 10 단어 벡터의 기하(image)
**Part 02 문장은 조건부 확률의 연결** 11 표지 · 12 2003 신경 언어 모델(flow) · 13 연쇄 확률(formula) · 14 입력이 있는 생성·자기지도(formula) · 15 정적 vs 문맥 표현(compare)
**Part 03 RNN과 장기 의존성** 16 표지 · 17 순서를 다루는 초기 설계(cards) · 18 RNN 점화식(formula) · 19 펼친 RNN(image) · 20 PyTorch shape(code) · 21 장기 의존성이 어려운 이유(table) · 22 Jacobian 곱(formula) · 23 소실·폭주 그래프(image) · 24 두 이유 비교(compare)
**Part 04 LSTM** 25 표지 · 26 LSTM 셀(image) · 27 게이트 식(formula) · 28 셀 갱신(formula) · 29 개선 vs 남은 것(compare) · 30 사고실험(cards)
**Part 05 Seq2Seq와 병목** 31 표지 · 32 가변 길이 연결(formula) · 33 Encoder→c→Decoder(image) · 34 2014년 두 논문(stats) · 35 병목 문제 제기(cards)
**마무리** 36 개념 확인(quiz) · 37 오개념 바로잡기(table) · 38 이번 주 과제(cards) · 39 참고 자료(table) · 40 오늘의 정리(summary → 5주차 Attention)

## 5. 개념 확인 (정답은 슬라이드 노트)
1. LSTM 이후에도 남아 있는 핵심 제약은? → 이전 상태에 대한 순차 계산 의존성 (개념 확인 03, 정답 A)
2. 토큰 ID 100은 ID 10보다 의미가 10배 큰가? → 아니다. ID는 lookup 주소, 계산에는 E[id] 벡터
3. 매 시점 기울기 배율이 0.9이면 50시점 전 신호는? → 0.9^50 ≈ 0.005, 사실상 소실
4. "Word2Vec이 Embedding을 발명했다"는? → 틀림. 2003 NPLM 등 이전 신경 언어 모델도 분산 표현 학습
5. Seq2Seq에서 입력 길이 S와 출력 길이 T는 같아야 하나? → 아니다. 병목은 길이가 아니라 모든 정보를 고정 크기 c 하나에 담는 것

## 6. 오개념 (3804–3885 중 4주차 해당 + 본문 경고)
- #1 CNN→RNN→Transformer 교체 서사 → 서로 다른 데이터 구조·목표에 맞춘 계보가 병행
- #4 Word2Vec이 Embedding을 발명 → 이전 신경 언어 모델도 분산 표현 학습
- #5 LSTM이 순차 계산 문제도 해결 → 장기 기억 경로 개선, 순환 의존성은 남음
- (본문) 단어 의미가 모두 Embedding 표에 저장 → lookup + 문맥 계산이 함께 표현을 만든다
- (본문) LSTM은 긴 문맥을 완벽히 기억 → 학습을 돕는 설계일 뿐 보장 아님
- (본문) 확률 분해 ∏p(y_t|y_<t)는 RNN만의 성질 → 목표와 아키텍처를 분리

## 7. 참고 자료 (원자료 번호)
[06] Elman 1990 · [08] Hochreiter & Schmidhuber 1997 · [09] Gers et al. 2000 · [11] Bengio et al. 2003 · [14] Mikolov et al. 2013 · [15] Cho et al. 2014 · [16] Sutskever et al. 2014 · [17] Bahdanau et al. 2014(다음 주) · [23] Sennrich et al. 2016 · [42] Goodfellow et al. Ch.10
추가(원자료 목록 외, 검증 완료): Jordan 1986 ICS Report 8604; Bengio, Simard & Frasconi 1994; Pascanu et al. 2013.
