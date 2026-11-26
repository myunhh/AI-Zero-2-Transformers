# Week 5 — Attention: 원문을 다시 찾아보면? (2014–2017) · 논문 노트

> 작성 기준: 모든 논문은 arXiv 원문 PDF를 받아 `pdftotext -layout`으로 읽었다(scratchpad에만 보관, 저장소에는 넣지 않음).
> 수치·식은 원문에서 옮겼고, 손계산은 파이썬(numpy)으로 검산했다. 강의 표기: B(배치), N(토큰 수), d(=d_model), H(head 수), d_h(head당 차원 = 논문의 d_k = d_v).
> 서지의 학회 쪽수는 원문 PDF(arXiv판)에 적혀 있지 않은 경우가 있어, 그런 쪽수는 "(일반적으로 알려진 값)"으로 표시했다.

---

## 주차 요약 (시간 순서 = 논문 순서)

| 순서 | 논문 | 앞 단계의 어떤 한계를 풀었나 |
|---|---|---|
| 1 | Bahdanau, Cho, Bengio (arXiv 2014-09 / ICLR 2015) | Seq2Seq의 **고정 길이 벡터 c 병목**(긴 문장에서 BLEU 급락) → 출력 단어마다 다른 문맥 c_i를 annotation h_j의 가중합으로 만든다(§1, §3.1). |
| 2 | Graves, Wayne, Danihelka (NTM, arXiv 2014-10) | (동시대 맥락) 신경망에 **외부 메모리**를 붙이고, key와 메모리 행의 **유사도(코사인) → softmax → 가중합**으로 읽는 미분 가능한 "content-based addressing"(§3.3.1). Q·K 내용 기반 조회의 원형. |
| 3 | Luong, Pham, Manning (EMNLP 2015) | Bahdanau 구조를 **단순화·일반화**: global vs local attention, 점수 함수 dot / general / concat / location **비교**, input feeding(§3). |
| 4 | Cheng, Dong, Lapata (EMNLP 2016); Parikh et al. (EMNLP 2016) | attention을 **두 시퀀스 사이**가 아니라 **한 시퀀스 내부**(intra-attention = self-attention)에 적용. Parikh는 순환 없이 attention만으로 SNLI SOTA(파라미터 382K). |
| 5 | Gehring et al. (ConvS2S, ICML 2017) | RNN의 **순차 계산**을 없앤 완전 합성곱 seq2seq. 순서 정보는 **학습형 절대 위치 임베딩**, 디코더 층마다 attention(multi-step). |
| 6 | Vaswani et al. (arXiv 2017-06 / NIPS 2017) | 합성곱도 없애고 **self-attention만으로** 인코더·디코더 표현을 만든다. 먼 위치 사이 경로 길이 O(1), 층당 순차 연산 O(1)(§4 Table 1). Scaled dot-product, multi-head, sinusoidal PE. |
| 7 | Jain & Wallace (NAACL 2019); Wiegreffe & Pinter (EMNLP 2019) | "attention heatmap = 설명"이라는 암묵적 가정을 실험으로 검증 → 반박 → 재반박. heatmap 해석의 한계. |

한 줄 흐름: **병목(c 하나) → 매번 다른 가중합(2014) → 점수 함수 정리(2015) → 한 문장 안에서도(2016) → 순환 없이(2017 ConvS2S) → attention만으로(2017 Transformer) → 그 가중치를 설명으로 믿어도 되나?(2019)**

---

## [Bahdanau2014] Bahdanau, Cho & Bengio (2014/2015) — Neural Machine Translation by Jointly Learning to Align and Translate
- 서지: ICLR 2015 (conference paper). arXiv:1409.0473 (v1 2014-09-01). 읽은 판본: v7 (2016-05-19), https://arxiv.org/pdf/1409.0473v7
- 접근: 원문 확인
- 이 논문이 풀려던 문제: 기존 encoder–decoder는 원문 전체를 **고정 길이 벡터**로 압축해야 하고, 이것이 성능의 **병목**이라고 추측한다(Abstract; §1). Cho et al.(2014b)이 보인 대로 입력 문장이 길어질수록 성능이 급격히 떨어진다(§1).
- 핵심 아이디어:
  - 인코더를 **양방향 RNN**으로 바꾸고, 각 단어 x_j의 annotation h_j = [→h_j ; ←h_j] (앞뒤 문맥을 모두 요약, 주변 단어에 초점)(§3.2).
  - 디코더는 단어 y_i를 만들 때마다 **이전 상태 s_{i−1}** 과 각 h_j의 "정렬 점수" e_ij를 계산하고, softmax 가중치 α_ij로 h_j들을 가중합해 **그 시점만의 문맥 c_i** 를 만든다(§3.1, Eq. 5–6).
  - 정렬(alignment)을 잠재 변수로 두지 않고 **soft alignment**로 직접 계산 → 번역 손실의 gradient가 정렬 모델까지 흘러 **함께 학습**된다(§3.1).
  - 논문 자체의 용어는 "alignment model"이며, "attention"은 §3.1에서 해석으로 등장한다: "Intuitively, this implements a mechanism of attention in the decoder."
  - c_i는 "가능한 정렬에 대한 **기대 annotation**"으로 해석된다(§3.1).
- 핵심 식(논문 표기):
  - Eq.(4) p(y_i | y_1..y_{i−1}, x) = g(y_{i−1}, s_i, c_i),  s_i = f(s_{i−1}, y_{i−1}, c_i)
  - Eq.(5) c_i = Σ_{j=1}^{T_x} α_ij h_j
  - Eq.(6) α_ij = exp(e_ij) / Σ_{k=1}^{T_x} exp(e_ik),  e_ij = a(s_{i−1}, h_j)
  - App. A.1.2: a(s_{i−1}, h_j) = v_aᵀ tanh(W_a s_{i−1} + U_a h_j),  W_a ∈ R^{n×n}, U_a ∈ R^{n×2n}, v_a ∈ R^n. "U_a h_j는 i와 무관하므로 **미리 계산**해 둔다."(App. A.1.2; App. A.2.2에서는 n′ 차원)
  - 강의 표기: e[t, j] = v_aᵀ tanh(W_a s[t−1] + U_a h[j]),  α[t, :] = softmax_j(e[t, :]),  c[t] = Σ_j α[t, j] h[j].  (현재 덱 Part 1 식과 일치)
  - 참고: 여기서는 **key와 value가 같은 h_j** 다. Q/K/V를 분리하는 관점은 이후(key-value memory, ConvS2S, Transformer)의 정리다.
- 실험 설정(§4, App. A–B): WMT'14 영→불. 병렬 코퍼스 850M 단어를 데이터 선택으로 348M 단어로 축소, 단일어 데이터 미사용. 어휘 각 언어 30,000(나머지 [UNK]). dev = newstest2012+2013, test = newstest2014(3003문장). RNNencdec과 RNNsearch를 각각 길이 30 이하 / 50 이하 문장으로 학습(‑30, ‑50). hidden n = 1000(양방향 각 1000), 임베딩 m = 620, maxout 층 l = 500, 정렬 모델 hidden n′ = 1000(App. A.2). 미니배치 80, Adadelta, 각 모델 약 5일 학습, beam search(§4.2). Table 2: 약 108–252시간 GPU 학습.
- 주요 결과:
  - Table 1 (BLEU, test):

    | 모델 | All | No UNK |
    |---|---|---|
    | RNNencdec-30 | 13.93 | 24.19 |
    | RNNsearch-30 | 21.50 | 31.44 |
    | RNNencdec-50 | 17.82 | 26.71 |
    | RNNsearch-50 | 26.75 | 34.16 |
    | RNNsearch-50⋆ (더 오래 학습) | 28.45 | 36.15 |
    | Moses (구문 기반 SMT) | 33.30 | 35.63 |

    → 전체 문장 기준으로는 Moses(33.30)에 **못 미친다**. "Moses와 비슷/능가"는 **UNK 없는 문장**에서(36.15 vs 35.63)의 이야기다. Moses는 추가 단일어 코퍼스 418M 단어를 썼다(§5.1).
  - Figure 2: 문장 길이별 BLEU. RNNencdec은 길이가 늘수록 급락, RNNsearch-50은 "길이 50 이상에서도 성능 저하가 없다"(§5.1). RNNsearch-30이 RNNencdec-50보다도 높다.
  - Figure 3: RNNsearch-50의 정렬 4개. 대체로 **단조(대각선)** 지만, [European Economic Area] → [zone économique européenne]처럼 **어순이 뒤집힌** 정렬도 찾는다(§5.2.1). [the man] → [l' homme]: 'the'를 번역할 때 뒤의 'man'도 함께 보아야 le/la/les/l'을 정할 수 있다 — **soft** alignment의 장점(§5.2.1).
- 저자가 밝힌 한계 / 이후 비판:
  - 출력 단어마다 **모든** 원문 단어의 가중치를 계산해야 한다(T_x × T_y). 번역(15–40단어)에서는 괜찮지만 다른 과제에는 제약일 수 있다(§6.1). → Luong의 local attention, 이후 효율적 attention의 동기.
  - [UNK] 처리 문제(Table 1의 All vs No UNK 차이).
- 흔한 오해 바로잡기:
  - "Attention은 Bahdanau가 처음 만들었다" → 미분 가능한 가중 정렬은 Graves(2013, 손글씨 합성; 단조 이동 Gaussian 창)가 먼저 있었고 저자도 §6.1에서 비교한다. 비슷한 시기 NTM(2014-10)도 있다. Bahdanau의 기여는 **번역에서 비단조 soft alignment를 함께 학습**한 것.
  - "Bahdanau attention은 현재 디코더 상태로 점수를 낸다" → **s_{i−1}(직전 상태)** 를 쓴다. 현재 상태 h_t를 쓰는 것은 Luong.
  - "RNNsearch가 Moses를 이겼다" → 전체 test set에서는 아니다(26.75/28.45 vs 33.30).
- 슬라이드용 손계산 예시(파이썬 검산): s = (1, 0), h_1 = (1, 0), h_2 = (0, 1), h_3 = (1, 1), W_a = U_a = I, v_a = (1, 1).
  e_j = v_aᵀ tanh(s + h_j) → e = (tanh2 + tanh0, tanh1 + tanh1, tanh2 + tanh1) = (0.964, 1.523, 1.726)
  α = softmax(e) = (0.204, 0.358, 0.438),  c = Σ α_j h_j = (0.642, 0.796).
  (같은 벡터로 dot 점수 sᵀh_j를 쓰면 e = (1, 0, 1), α = (0.422, 0.155, 0.422) — 점수 함수에 따라 비중이 달라진다.)
- 다시 그릴 만한 그림: Figure 1(양방향 인코더 위에서 α_t,j로 h_j를 섞어 s_t로 들어가는 구조), Figure 2(문장 길이 vs BLEU, 4개 곡선), Figure 3(a)(영→불 정렬 heatmap, 어순 반전 구간).
- 읽기 안내: §3.1(식 4–6과 "attention" 해석 문단), Figure 2와 Figure 3, App. A.1.2(정렬 모델 식).

---

## [Graves2014NTM] Graves, Wayne & Danihelka (2014) — Neural Turing Machines
- 서지: arXiv:1410.5401 (학회 미게재 preprint). 읽은 판본: v2 (2014-12-10), https://arxiv.org/pdf/1410.5401
- 접근: 원문 확인 (맥락용으로 §3만 정독)
- 이 논문이 풀려던 문제: 신경망에 **외부 메모리**를 붙여 복사·정렬·연관 회상 같은 간단한 알고리즘을 예시로부터 학습하게 한다. 메모리 접근은 "attentional process"이며 전 과정이 미분 가능하다(Abstract; §3).
- 핵심 아이디어: 읽기 head가 메모리 위치들에 합이 1인 가중치 w_t를 내고, 읽은 벡터는 메모리 행들의 볼록 결합(§3.1, Eq. 1–2). 가중치는 **content-based addressing**(key와 각 메모리 행의 유사도)과 location-based addressing(이동·sharpen)을 결합해 만든다(§3.3, Figure 2).
- 핵심 식: Eq.(5) w_t^c(i) = exp(β_t K[k_t, M_t(i)]) / Σ_j exp(β_t K[k_t, M_t(j)]),  Eq.(6) K[u, v] = u·v / (‖u‖·‖v‖) (코사인 유사도). Eq.(2) r_t = Σ_i w_t(i) M_t(i).
  - 강의 표기로: 점수 = β · cos(q, k_i) → softmax → Σ α_i v_i (여기서 key와 value는 같은 메모리 행 M_t(i)). β(key strength)는 **softmax의 날카로움을 조절**한다 — Transformer의 1/√d_k와 같은 "점수 스케일" 역할을 학습 가능한 스칼라로 둔 셈(유비이지 같은 동기는 아님).
- 실험 설정 / 주요 결과: copy, repeat copy, associative recall, priority sort 등 합성 과제에서 LSTM보다 빨리 학습·더 긴 길이로 일반화(§4). (이번 주에는 수치 인용 불필요)
- 흔한 오해 바로잡기: "Query/Key로 내용을 찾는 attention은 Transformer의 발명" → 2014년 NTM에서 이미 key 벡터와 유사도·softmax로 메모리를 읽는다.
- 슬라이드용 손계산 예시(검산): k = (1, 0), 메모리 행 (1,0), (0,1), (1,1). cos = (1, 0, 0.707).
  β = 1 → w = (0.473, 0.174, 0.353);  β = 10 → w = (0.949, 0.000, 0.051). β가 크면 한 칸에 몰린다(√d 스케일 슬라이드와 연결 가능).
- 다시 그릴 만한 그림: Figure 2(addressing 흐름: content → interpolation → shift → sharpen) — 이번 주에는 content 부분만.
- 읽기 안내: §3.1, §3.3.1(Eq. 5–6).

---

## [Luong2015] Luong, Pham & Manning (2015) — Effective Approaches to Attention-based Neural Machine Translation
- 서지: EMNLP 2015, pp. 1412–1421 (쪽: 일반적으로 알려진 값). arXiv:1508.04025 (v1 2015-08-17). 읽은 판본: v5 (2015-09-20), https://arxiv.org/pdf/1508.04025v5
- 접근: 원문 확인
- 이 논문이 풀려던 문제: attention 기반 NMT의 "유용한 구조"가 충분히 탐색되지 않았다(Abstract). 두 계열(global = 모든 원문 위치, local = 일부 창)을 제안하고 점수 함수를 비교한다(§3).
- 핵심 아이디어:
  - 디코더 **최상위 LSTM의 현재 상태 h_t** 로 정렬을 계산: h_t → a_t → c_t → h̃_t → 예측(§3.1, "Comparison to Bahdanau"). Bahdanau는 h_{t−1} → a_t → c_t → h_t 경로.
  - **Global attention**: 모든 원문 은닉 상태 h̄_s에 대해 a_t(s) = softmax(score(h_t, h̄_s)) (Eq. 7).
  - **Local attention**: 정렬 위치 p_t를 정하고 창 [p_t − D, p_t + D]만 본다. local-m: p_t = t(단조 가정). local-p: p_t = S·sigmoid(v_pᵀ tanh(W_p h_t))를 예측하고 Gaussian(σ = D/2)으로 가중(Eq. 9–10). D = 10(§4.1).
  - **Input feeding**: h̃_t를 다음 시점 입력에 이어 붙여 이전 정렬 결정을 알게 한다(§3.3, Figure 4).
- 핵심 식(§3.1, Eq. 8 주변):
  - score(h_t, h̄_s) = h_tᵀ h̄_s  (**dot**)
  - = h_tᵀ W_a h̄_s  (**general**)
  - = v_aᵀ tanh(W_a [h_t ; h̄_s])  (**concat**)
  - a_t = softmax(W_a h_t)  (**location**, Eq. 8 — 원문 상태를 보지 않음)
  - h̃_t = tanh(W_c [c_t ; h_t]) (Eq. 5),  p(y_t | y_<t, x) = softmax(W_s h̃_t) (Eq. 6)
  - 강의 표기: dot = qᵀk, general = qᵀWk, concat = vᵀtanh(W[q; k]) (Bahdanau의 additive와 같은 계열; W[q;k] = W₁q + W₂k).
  - 저자 주: "Bahdanau et al.은 **concat 하나만** 실험했다"(§3.1).
- 실험 설정(§4.1): WMT'14 영↔독, 학습 4.5M 문장쌍(영 116M, 독 110M 단어), 어휘 50K, 길이 50 초과 문장 제거. 4층 stacking LSTM, 1000 cells, 1000차원 임베딩, [−0.1, 0.1] 균등 초기화, 10 epoch(dropout 시 12), SGD lr 1.0, 5 epoch 후 매 epoch 반감, 미니배치 128, gradient norm 5 클리핑, dropout 0.2, Tesla K40에서 약 1K target words/s, 7–10일. dev = newstest2013, test = newstest2014(2737문장)/2015(2169문장).
- 주요 결과:
  - Table 1 (WMT'14 영→독, tokenized BLEU): Base 11.3 → +reverse 12.6 → +dropout 14.0 → +global(location) 16.8 → +feed input 18.1 → local-p(general)+feed 19.0 → +unk replace 20.9 → **ensemble 8 + unk 23.0** (기존 최고 Jean et al. 21.6, WMT'14 우승 SMT 20.7).
  - Table 2 (WMT'15 영→독, NIST BLEU): 앙상블 **25.9** vs 당시 최고(NMT + 5-gram rerank) 24.9.
  - Table 3 (WMT'15 독→영): Base(reverse) 16.9 → +global(location) 19.1 → +feed 20.1 → +global(**dot**)+drop+feed 22.8 → +unk 24.9 (SOTA SMT 29.2에는 미달).
  - Table 4 (점수 함수 비교, 영→독 newstest2014, unk 대체 전/후 BLEU): global(location) 18.1/19.3, global(dot) 18.6/20.5, global(general) 17.3/19.1, local-m(dot) ppl>7 학습 실패, local-m(general) 18.6/20.4, local-p(dot) 18.0/19.6, **local-p(general) 19.0/20.9**. → "dot은 global에, general은 local에 좋다"(§5.3). concat은 ppl 6.7–7.1로 부진(각주 15: W_a 일부를 항등으로 단순화한 탓일 수 있다).
  - Table 6: 정렬 오류율 AER — local-m(general) 0.34, global(location) 0.39, Berkeley Aligner 0.32. AER과 BLEU는 잘 상관하지 않는다(§5.4).
- 저자가 밝힌 한계: concat 부진 원인 미규명(§5.3); 자원 부족으로 모든 조합을 실험하지 못함(§5.3).
- 흔한 오해 바로잡기:
  - "Luong = dot attention" → Luong은 location/dot/general/concat **네 가지를 비교**했고, 최고 단일 모델은 **local-p + general** 이다.
  - "Luong attention = Bahdanau attention에서 점수 함수만 바꾼 것" → 쓰는 상태(h_t vs s_{t−1}), 계산 경로, input feeding, stacking LSTM 등 구조도 다르다.
- 슬라이드용 손계산 예시(검산): q = (1, 0), 원문 상태 (1,0), (0,1), (1,1).
  dot: e = (1, 0, 1), α = (0.422, 0.155, 0.422).  general (W = [[0,1],[1,0]]): e = (0, 1, 1), α = (0.155, 0.422, 0.422). 같은 벡터라도 W가 "무엇을 비슷하다고 볼지"를 바꾼다.
- 다시 그릴 만한 그림: Figure 2(global), Figure 3(local, 창과 p_t), Figure 4(input feeding).
- 읽기 안내: §3.1(점수 함수 3종 + Bahdanau와의 비교 문단), Table 4.

---

## [Cheng2016] Cheng, Dong & Lapata (2016) — Long Short-Term Memory-Networks for Machine Reading
- 서지: EMNLP 2016, pp. 551–561 (쪽: 일반적으로 알려진 값). arXiv:1601.06733 (v1 2016-01-25). 읽은 판본: v7 (2016-09-20)
- 접근: 원문 확인 (self-attention 선행 사례로 §3–4 중심)
- 이 논문이 풀려던 문제: LSTM은 현재 상태 하나가 지금까지를 요약한다고 가정(Markov)하고, 토큰 간 관계를 명시적으로 다루는 장치가 없다(§3).
- 핵심 아이디어: LSTM의 기억 셀 하나를 **토큰마다 슬롯이 있는 memory/hidden tape**로 바꾸고, 현재 입력 x_t가 **같은 시퀀스의 이전 토큰들** h_1..h_{t−1}에 attention해 요약 h̃_t, c̃_t를 만든 뒤 LSTM 갱신에 쓴다 — 저자 용어로 **intra-attention**(§3, §4). 인코더–디코더에서는 intra + inter attention을 결합(shallow / deep fusion, Figure 3).
- 핵심 식(§3): Eq.(4) a_i^t = vᵀ tanh(W_h h_i + W_x x_t + W_h̃ h̃_{t−1}),  Eq.(5) s_i^t = softmax(a_i^t),  Eq.(6) [h̃_t; c̃_t] = Σ_{i=1}^{t−1} s_i^t [h_i; c_i].
  → **additive 점수**를 쓰는, 왼쪽→오른쪽(인과적) self-attention.
- 실험 설정 / 주요 결과: PTB 언어모델, SST 감성분류(5-class 47.9 / 2-class 87.0, 2-layer LSTMN), SNLI(450D deep fusion **86.3%**, 3.4M 파라미터)(Table 1–3).
- 흔한 오해 바로잡기: "self-attention은 Transformer(2017)에서 처음" → Transformer 논문 §2 스스로 "Self-attention, sometimes called intra-attention … has been used successfully"라며 [4] Cheng et al.을 첫 인용으로 든다. 다만 LSTMN은 **여전히 순환(RNN) 안에** 있다.
- 다시 그릴 만한 그림: Figure 1(문장을 읽으며 이전 단어들에 attention하는 모습).
- 읽기 안내: §3 Eq. 4–9, Figure 1.

## [Parikh2016] Parikh, Täckström, Das & Uszkoreit (2016) — A Decomposable Attention Model for Natural Language Inference
- 서지: EMNLP 2016, pp. 2249–2255 (쪽: 일반적으로 알려진 값). arXiv:1606.01933 (v1 2016-06-06). 읽은 판본: v2 (2016-09-25)
- 접근: 원문 확인
- 이 논문이 풀려던 문제: NLI(SNLI)를 깊은 순환/문장 인코더 없이, 단어 단위 정렬로 쪼개 풀 수 있는가(§1).
- 핵심 아이디어: Attend(두 문장 사이 soft 정렬) → Compare → Aggregate. 기본형은 **어순 정보를 전혀 쓰지 않는다**(Abstract). 선택적으로 **intra-sentence attention**을 붙인다(§3.4, Cheng et al.을 인용).
- 핵심 식: Eq.(1) e_ij = F(ā_i)ᵀ F(b̄_j) — **내적형 점수**(F는 피드포워드). Eq.(6) f_ij = F_intra(a_i)ᵀ F_intra(a_j), Eq.(7) a′_i = Σ_j softmax_j(f_ij + d_{i−j}) a_j. **거리 의존 편향 d_{i−j}** 로 "최소한의 순서 정보"를 주며 병렬성을 유지(10단어 초과 거리는 같은 bias로 버킷).
  → 순환 없는 self-attention + **상대 위치 편향**의 이른 사례(이후 Shaw 2018, ALiBi와 개념상 연결).
- 주요 결과(Table 1, SNLI test acc.): vanilla **86.3%, 382K 파라미터** (Cheng LSTMN deep fusion 86.3%, 3.4M와 동률이면서 약 1/9 파라미터); intra-sentence attention 추가 **86.8%, 582K**.
- 흔한 오해 바로잡기: "순환 없이 attention만으로 좋은 성능을 낸 첫 사례는 Transformer" → 분류 과제에서는 Parikh(2016)가 먼저다(Transformer v1 §1이 [25]=Parikh를 예외로 인용: "In all but a few cases [25], … used in conjunction with a recurrent network"). 공저자 Jakob Uszkoreit는 Transformer 저자이기도 하다(Transformer v2+ 기여 각주: "Jakob proposed replacing RNNs with self-attention").
- 읽기 안내: §3.1, §3.4, Table 1.

---

## [Gehring2017] Gehring, Auli, Grangier, Yarats & Dauphin (2017) — Convolutional Sequence to Sequence Learning
- 서지: ICML 2017, PMLR 70 (쪽: 1243–1252, 일반적으로 알려진 값). arXiv:1705.03122. 읽은 판본: v3 (2017-07-25)
- 접근: 원문 확인 (위치 임베딩·attention 중심)
- 이 논문이 풀려던 문제: RNN은 이전 시점 계산에 의존해 시퀀스 내부 병렬화가 안 된다. 합성곱은 모든 위치를 병렬 계산하고, 층을 쌓아 문맥 창을 키운다(창 n을 덮는 데 O(n/k) 층)(§1).
- 핵심 아이디어:
  - 인코더·디코더 모두 GLU 합성곱 블록 + residual(§3.2).
  - 순서 정보: **학습형 절대 위치 임베딩** p_j를 단어 임베딩에 더한다: e = (w_1 + p_1, …, w_m + p_m)(§3.1). 디코더 입력도 동일.
  - **Multi-step attention**: 디코더 **층마다** 별도 attention. 점수는 **내적**: a_ij^l = softmax_j(d_i^l · z_j^u), 문맥 c_i^l = Σ_j a_ij^l (z_j^u + e_j)(§3.3, Eq. 1–2). key = 인코더 출력 z_j, value = z_j + e_j — "key-value memory network와 닮았다"(§3.3).
- 주요 결과: Table 1 — WMT'14 영→독 **25.16** (GNMT word-piece 24.61), 영→불 **40.51** (GNMT+RL 39.92), WMT'16 영→루 30.02. Table 3 — GNMT 대비 GPU에서 최대 한 자릿수 빠른 번역.
  - Table 4 (위치 임베딩 제거, 영→독 dev/test): 전체 21.7 → source 제거 21.3, target 제거 21.5, **둘 다 제거 21.2 (−0.5 BLEU만)**. 저자 해석: 합성곱 창(인코더 27, 디코더 25단어) 안에서 **상대 위치를 스스로 학습**할 수 있다(§5.4).
- 흔한 오해 바로잡기: "학습형 위치 임베딩은 BERT·GPT부터" → Transformer가 비교 대상으로 인용한 [9]가 바로 ConvS2S의 학습형 위치 임베딩이다(Transformer §3.5 v2+).
- 다시 그릴 만한 그림: Figure 1(인코더 합성곱 → 디코더 층별 attention).
- 읽기 안내: §3.1, §3.3, Table 4.

---

## [Vaswani2017] Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser & Polosukhin (2017) — Attention Is All You Need
- 서지: NIPS 2017 (31st Conference on Neural Information Processing Systems, Long Beach; v7 표지), pp. 5998–6008 (쪽: 일반적으로 알려진 값). arXiv:1706.03762.
  읽은 판본: **v1 (2017-06-12)** https://arxiv.org/pdf/1706.03762v1 을 기준으로, v2(06-19)·v3(06-20)·v4(06-30)·v5(12-06)·v6(2023-07-24)·**v7(2023-08-02)** 과 대조.
- 접근: 원문 확인 (v1–v7 모두)
- **판본 차이(이번 주에 중요한 것만)**:

  | 항목 | v1 (2017-06-12) | v2 이후 (NIPS판 포함) |
  |---|---|---|
  | √d_k 각주(분산 = d_k 논증) | **없음**. 본문만 "dot products growing too large in magnitude to result in useful gradients" | 각주 4 추가: q, k 성분이 평균 0·분산 1인 독립 확률변수면 q·k는 평균 0, 분산 d_k. 본문도 "pushing the softmax function into regions where it has extremely small gradients"로 바뀜 |
  | MultiHead 식의 W^O | **없음**: MultiHead = Concat(head_1..head_h) | Concat(…)**W^O**, W^O ∈ R^{h·d_v × d_model}, "concatenated and once again projected" |
  | 학습형 위치 임베딩 비교 | **없음** (§3.5에 문장 없음, Table 3에 (E) 행 없음) | §3.5 "nearly identical results (see Table 3 row (E))" + sinusoid를 고른 이유(외삽 가능성) 추가 |
  | Table 3 base d_ff | 표에 1024로 오기(본문 §3.3은 2048) | 2048로 수정 |
  | 영→불 BLEU (big) | 41.0 (초록·표·본문) | v2 초록 41.2 / 본문 41.17 / 표 41.0 → v3–v4 41.0 → **v5부터 초록·Table 2는 41.8**, 그러나 §6.1 본문은 v7까지 "41.0"으로 남음(판본 내 불일치) |
  | 기여 각주(누가 무엇을) | 없음 | "Noam proposed scaled dot-product attention, multi-head attention and the parameter-free position representation"; "Jakob proposed replacing RNNs with self-attention" |
  | §2 End-to-end memory networks 문단 | 없음 | 추가 |

  → 슬라이드에서 W^O, √d_k 분산 논증, 학습형 PE 비교를 "원논문"으로 인용할 때는 **NIPS 2017판(arXiv v2+)** 이라고 적는 것이 정확하다.

- 이 논문이 풀려던 문제: 순환 모델은 위치를 따라 계산이 **순차적**이라 한 예제 안에서 병렬화가 안 되고, 긴 시퀀스에서는 메모리 한계로 배치도 못 늘린다(§1). 합성곱 모델(ConvS2S, ByteNet)은 병렬이지만 먼 두 위치를 잇는 연산 수가 거리에 따라 선형/로그로 늘어난다(§2).
- 핵심 아이디어:
  - 순환·합성곱 없이 **stacked self-attention + position-wise FFN** 으로 인코더(N=6)·디코더(N=6)를 만든다(§3, §3.1). 각 sub-layer 출력은 LayerNorm(x + Sublayer(x)), d_model = 512.
  - attention을 "query와 key-value 쌍들을 출력으로 사상하는 함수"로 정의: 출력 = value들의 가중합, 가중치 = query와 key의 compatibility(§3.2).
  - **Scaled Dot-Product Attention**(§3.2.1), **Multi-Head Attention**(§3.2.2), 세 가지 사용처(encoder-decoder attention / encoder self-attention / masked decoder self-attention, §3.2.3), **sinusoidal positional encoding**(§3.5).
  - "평균내기로 인한 유효 해상도 저하를 multi-head로 상쇄한다"(§2) — multi-head의 동기.
- 핵심 식:
  - Eq.(1) Attention(Q, K, V) = softmax(QKᵀ / √d_k) V  (§3.2.1). 마스크는 식에 없고 §3.2.3에서 "softmax 입력의 불법 연결을 −∞로" 설명.
  - §3.2.1 비교: additive(Bahdanau)와 dot-product는 "**이론적 복잡도는 비슷**"하지만 dot-product가 최적화된 행렬곱 덕분에 실제로 훨씬 빠르고 메모리 효율적. d_k가 작으면 둘이 비슷, d_k가 크면 **스케일 없는 dot-product보다 additive가 낫다**는 Britz et al.(2017) [3]의 관찰 → "We suspect" 내적이 커져 softmax gradient가 작아진다 → 1/√d_k로 스케일.
  - 각주 4 (v2+): q·k = Σ_{i=1}^{d_k} q_i k_i, 평균 0, 분산 d_k.
  - §3.2.2 MultiHead(Q, K, V) = Concat(head_1, …, head_h) W^O (v2+), head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V), W_i^Q, W_i^K ∈ R^{d_model×d_k}, W_i^V ∈ R^{d_model×d_v}. **h = 8, d_k = d_v = d_model/h = 64**. "head당 차원이 줄어 전체 계산 비용은 전체 차원 single-head와 비슷."
  - §3.4 임베딩: 입력·출력 임베딩과 pre-softmax 선형층이 **같은 가중치를 공유**, 임베딩층에서 그 가중치에 **√d_model을 곱한다**(이유는 적혀 있지 않음).
  - §3.5 PE(pos, 2i) = sin(pos / 10000^{2i/d_model}), PE(pos, 2i+1) = cos(pos / 10000^{2i/d_model}). 파장은 2π부터 10000·2π까지 **기하급수**. 선택 이유: 고정 offset k에 대해 PE_{pos+k}가 PE_pos의 **선형 함수**로 표현되므로 상대 위치로 attend하기 쉬울 것이라는 **가설**. (v2+) 학습형 위치 임베딩[9]과 "거의 동일", sinusoid를 고른 것은 학습보다 긴 길이로 "**외삽할 수도 있기(may)**" 때문.
  - 강의 표기: Attention = softmax(Q Kᵀ/√d_h + M) V, Q, K, V ∈ R^{N×d_h} (head 하나), multi-head는 (B, N, d) → (B, H, N, d_h) → (B, N, d), d_h = d/H.
- §4 Table 1 (n = 시퀀스 길이, d = 표현 차원, k = 커널, r = 이웃 크기):

  | 층 종류 | 층당 복잡도 | 순차 연산 | 최대 경로 길이 |
  |---|---|---|---|
  | Self-Attention | O(n²·d) | O(1) | O(1) |
  | Recurrent | O(n·d²) | O(n) | O(n) |
  | Convolutional | O(k·n·d²) | O(1) | O(log_k n) |
  | Self-Attention (restricted) | O(r·n·d) | O(1) | O(n/r) |

  - "n < d일 때(당시 word-piece/BPE 문장 표현에서 흔함) self-attention이 recurrent보다 빠르다"(§4). 즉 **n²·d 비용**이 공짜가 아니다 — 긴 시퀀스에선 restricted attention을 future work로 언급.
  - 합성곱의 O(log_k n)은 **dilated** 합성곱 기준이고, 연속 커널이면 O(n/k)층(§4 본문).
  - "부수적으로 해석 가능한 모델을 줄 수 있다 … 개별 head가 서로 다른 과제를 수행하도록 **clearly learn**하고, 많은 head가 문장의 구문·의미 구조와 관련된 행동을 보이는 것 같다"(§4 마지막 문단) — 저자 주장. 증거는 부록 그림(정성적).
- 실험 설정(§5): WMT'14 영→독 약 4.5M 문장쌍, BPE 공유 어휘 약 37K; 영→불 36M 문장, word-piece 32K. 배치당 약 25K source + 25K target 토큰. 8×P100. base: 100K step, 약 12시간(step 0.4초). big: 300K step, 3.5일(step 1.0초). Adam(β1 0.9, β2 0.98, ε 1e‑9), warmup 4000의 lrate 식(Eq. 3). residual dropout 0.1, label smoothing 0.1. base는 마지막 5개, big은 20개 체크포인트 평균, beam 4, length penalty α = 0.6.
- 주요 결과:
  - Table 2 (newstest2014 BLEU): Transformer base 27.3 (영→독) / 38.1 (영→불), big **28.4** / **41.0 (v1–v4) → 41.8 (v5+)**. 비교: ConvS2S 25.16 / 40.46, GNMT+RL 24.6 / 39.92, MoE 26.03 / 40.56, ConvS2S 앙상블 26.36 / 41.29. 학습 FLOPs: base 3.3·10^18, big 2.3·10^19.
  - Table 3 (영→독 dev newstest2013, base: N=6, d=512, d_ff=2048, h=8, d_k=d_v=64 → PPL 4.92, BLEU 25.8, 65M 파라미터):
    - (A) 계산량 고정, head 수 변경: h=1 (d_k=512) **24.9**, h=4 25.5, h=16 25.8, h=32 25.4 → "single-head는 최고보다 0.9 BLEU 낮고, head가 너무 많아도 떨어진다."
    - (B) d_k만 16 → 25.1, 32 → 25.4: "compatibility 판단은 쉽지 않고, 내적보다 정교한 함수가 도움이 될 수 있다."
    - (E) (v2+) 학습형 위치 임베딩: PPL 4.92, BLEU **25.7** (base 25.8).
    - big: N=6, d=1024, d_ff=4096, h=16, dropout 0.3, 300K step → PPL 4.33, BLEU 26.4, 213M.
  - Table 4: 영어 구성 성분 파싱(WSJ 23) WSJ only 91.3, semi-supervised 92.7 F1.
- 부록 Attention Visualizations (v1에도 있음, 인코더 self-attention 5/6층): Figure 3 'making … more difficult'의 장거리 의존을 여러 head가 따라감; Figure 4 'its'의 anaphora resolution에 관여하는 것으로 **보이는(apparently)** 두 head; Figure 5 문장 구조와 관련된 것으로 보이는 head 행동, "The heads clearly learned to perform different tasks."
- 저자가 밝힌 한계 / 이후 비판:
  - attention 평균으로 인한 **유효 해상도 저하**(§2) → multi-head로 대응.
  - 긴 입력에서 O(n²) → restricted/local attention을 향후 과제로(§4, §7).
  - Table 3 (B)에서 내적 compatibility가 최선이 아닐 수 있다고 스스로 언급.
  - √d_k 이유는 "We suspect"(추측)이고 각주는 독립·분산 1이라는 **가정** 하의 예시.
  - head 역할 해석은 정성적 그림에 근거 — Jain & Wallace / Wiegreffe & Pinter 이후의 해석 논쟁과 연결(단, 그 두 논문은 BiLSTM attention을 다뤘다).
- 흔한 오해 바로잡기:
  - "Transformer가 attention/self-attention을 발명" → 논문 스스로 additive [2], self-attention [4, 25, 26, 20]을 선행 연구로 든다. 주장은 "**전적으로** self-attention에 의존하는 **최초의 transduction 모델**"(§2).
  - "√d_k는 증명된 최적 스케일" → Britz et al.의 경험적 관찰 + 저자의 추측 + 단순화 가정 아래 분산 계산.
  - "sinusoid라야 한다 / sinusoid가 외삽을 보장한다" → 학습형과 거의 같았고(row E), 외삽은 "may" 수준의 기대.
  - "W^O는 원래 식에 있었다" → v1 식에는 없다(v2부터).
  - "× √d_model은 PE와 크기를 맞추기 위해" → 논문에 **이유가 없다**(§3.4). 흔한 해석일 뿐.
  - "cross-attention" → 논문 용어는 **encoder-decoder attention**(§3.2.3). cross-attention은 이후 관용어.
- 슬라이드용 손계산 예시(파이썬 검산):
  - 4토큰 예제(덱 그대로; q·k·v는 투영 후 값, d_h = 2): S = QKᵀ/√2 =
    [[0.707, 0, 0.707, −0.707], [0, 0.707, 0.707, 0.707], [0.707, 0.707, 1.414, 0], [−0.707, 0.354, −0.354, 1.061]]
    A = [[0.365, 0.180, 0.365, 0.089], [0.141, 0.286, 0.286, 0.286], [0.221, 0.221, 0.449, 0.109], [0.090, 0.259, 0.127, 0.524]]
    O = AV = [[1.008, 1.000], [0.427, 1.145], [1.009, 1.227], [−0.180, 1.038]]. Query A의 exp 합 5.549 ✔.
    (숙제용) 스케일을 빼면 A 첫 행 = (0.399, 0.147, 0.399, 0.054) — 더 뾰족해진다.
  - √d 표 검증(독립 표준정규 성분 20만 샘플): d_h = 4, 16, 64, 256에서 q·k 표준편차 ≈ 2.00, 3.99, 8.00, 15.98; ÷√d_h 후 ≈ 1.00.
  - 파라미터: nn.MultiheadAttention(8, 2) = 4 × (8·8 + 8) = 288 ✔. d = 512에서 4d² = 1,048,576 (편향 포함 1,050,624) ≈ 105만 ✔.
  - PE(d = 8): pos 1 = (0.841, 0.540, 0.100, 0.995, 0.010, 1.000, 0.001, 1.000), pos 2 = (0.909, −0.416, 0.199, 0.980, 0.020, 1.000, 0.002, 1.000) ✔.
  - PE의 선형 이동 성질 검산: 각 차원 쌍 (2i, 2i+1)에 2×2 회전행렬 R_i(k) = [[cos ω_i k, sin ω_i k], [−sin ω_i k, cos ω_i k]] (ω_i = 1/10000^{2i/d})을 적용하면 PE_{pos+k} = R(k)·PE_pos 가 pos와 무관하게 성립(d = 8, k = 3, pos = 5와 11에서 확인). → "왜 sin/cos 쌍인가"를 보여 주는 짧은 슬라이드로 쓸 수 있다(RoPE 예고).
  - 파장 범위: d = 512에서 가장 긴 실제 파장은 2π·10000^{510/512} ≈ 60,611 (논문 표현 "10000·2π ≈ 62,832"는 극한값).
- 다시 그릴 만한 그림: Figure 1(전체 구조 — 이번 주는 입력 임베딩+PE와 attention 블록만 강조), Figure 2(왼쪽 scaled dot-product 흐름: MatMul → Scale → Mask(opt.) → SoftMax → MatMul; 오른쪽 h개 병렬 → Concat → Linear), Table 1(세 층 종류 비교 표를 그대로 표로), 부록 Figure 3–4(의존·대명사 head — "보이는 것" / "증명하지 않는 것" 병기).
- 읽기 안내: §3.2(Figure 2 포함), §3.5, §4 Table 1.

---

## [Jain2019] Jain & Wallace (2019) — Attention is not Explanation
- 서지: NAACL-HLT 2019, pp. 3543–3556 (쪽: 일반적으로 알려진 값). arXiv:1902.10186. 읽은 판본: v3 (2019-05-08)
- 접근: 원문 확인
- 이 논문이 풀려던 문제: attention 가중치가 "입력의 상대적 중요도"를 보여 준다는 암묵적 가정을 **형식적으로 검증**한 적이 없다(§1). 충실한(faithful) 설명이라면 (i) gradient·leave-one-out(LOO) 같은 특징 중요도와 상관해야 하고, (ii) 다른 attention 분포는 다른 예측을 낳아야 한다(§1).
- 핵심 아이디어/방법: BiLSTM(+ 비교용 단순 평균 인코더, CNN) 위의 additive 또는 scaled dot-product attention 분류기, QA, NLI(§2). (1) attention과 gradient/LOO 중요도의 Kendall τ, (2) attention을 무작위 **치환**하거나, 예측을 거의 바꾸지 않으면서 원래와 최대한 다른 **적대적 분포**를 인스턴스별로 탐색(§4).
- 주요 결과:
  - Table 2: BiLSTM에서 attention–gradient τ_g 평균은 대체로 0.1–0.47 (예: SST 0.40, IMDB 0.37, 20News 0.08, CNN 0.20, SNLI 0.36–0.42). 평균(비순환) 인코더에서는 0.48–0.84로 더 높다.
  - Figure 1 예: 부정 영화 리뷰에서 원래 attention("waste")과 전혀 다른 적대적 attention("was")이 **같은 예측 0.01**. τ_g = 0.29, 무작위 치환 시 출력 변화 중앙값 0.006(§1).
  - 결론: "standard attention modules do not provide meaningful explanations and should not be treated as though they do"(Abstract).
- 저자가 밝힌 한계(§6): gradient/LOO가 정답(ground truth)인 것은 아니다; 소수의 attention 변형만 실험; **seq2seq(번역)는 다루지 않았다**; 적대적 가중치는 모델 파라미터 아래에서 "있을 법하지 않을" 수 있다; 결과는 특히 RNN 인코더에 대한 것.
- 흔한 오해 바로잡기: "Transformer attention head도 설명이 아니라고 증명됐다" → 이 논문은 **BiLSTM + 단일 attention 분류기** 중심이고 Transformer multi-head나 번역은 다루지 않았다.
- 읽기 안내: §1(Figure 1), §6 Discussion.

## [Wiegreffe2019] Wiegreffe & Pinter (2019) — Attention is not not Explanation
- 서지: EMNLP-IJCNLP 2019, pp. 11–20 (쪽: 일반적으로 알려진 값). arXiv:1908.04626. 읽은 판본: v2 (2019-09-05)
- 접근: 원문 확인
- 이 논문이 풀려던 문제: Jain & Wallace의 결론은 "설명"의 정의와 실험 설계(자유도)에 달려 있다(Abstract, §2).
- 핵심 주장:
  - J&W는 attention 분포를 **그것을 계산한 파라미터에서 떼어 내** 인스턴스마다 따로 조작했다 → 그런 분포를 내는 **적대적 모델이 존재한다는 것**은 보이지 못했다(§2.1).
  - "**Existence does not entail exclusivity**": attention은 *the* explanation이 아니라 *an* explanation을 준다(§2.1).
  - 네 가지 진단: (1) **uniform attention** 기준선 — 일부 데이터셋에서는 attention을 균등으로 고정해도 성능이 거의 같다(Table 2: SST 0.831→0.822, AgNews 0.964→0.960, IMDb 0.902→0.879, Diabetes 0.775→0.706) → 그런 과제에선 애초에 attention 조작이 설명 문제의 증거가 되지 못한다; (2) 랜덤 시드 분산 보정; (3) 학습된 attention을 고정 가중치로 쓰는 **비문맥 MLP 진단**; (4) 모델 단위로 학습하는 **적대적 attention 학습**(§3–4).
  - 결과: 모델 일관적인 적대적 분포는 찾을 수 있지만 J&W만큼 극단적이지 않고, 진단 MLP에서 성능이 나쁘다 → "prior work does not disprove the usefulness of attention mechanisms for explainability"(Abstract). 동시에 "LSTM의 일부 분류 과제에서 적대적 분포가 존재함을 **확인**했다 — one true, faithful 설명을 찾는 연구자는 멈칫해야 한다"(§6).
  - plausible(그럴듯한) vs faithful(충실한) 설명 구분(§5–6).
- 흔한 오해 바로잡기: "제목대로 attention은 설명이다로 결론" → 아니다. "정의에 따라 다르고, J&W의 실험이 설명 가능성을 **반증하지는 못했다**"는 것. 두 논문 모두 RNN(LSTM) attention 대상.
- 슬라이드 사용 제안: 덱의 "가중치를 해석할 때" 슬라이드에 "관찰(heatmap) / 상관(gradient·LOO) / 개입(가리기·교체) / 대조군(uniform)" 네 단계로 정리.
- 읽기 안내: §2.1, §3.2(Table 2), §6.

---

## 현재 강의자료(build/week5.py)와 원문이 어긋나는 곳

| # | 슬라이드(제목) | 무엇이 문제인가 | 원문 근거 / 제안 |
|---|---|---|---|
| 1 | "점수 함수: 어떻게 비교할까" (표의 '제안' 열) | Dot·General을 "Luong 2015 제안"으로 적었다. Luong은 location/dot/general/concat **네 가지를 비교**했고(내용 기반 유사도 조회 자체는 NTM 2014의 코사인 등 이전에도 있음), 최고 단일 모델은 **local-p + general**, global에서는 dot이 최선이었다. 또 Luong 점수의 기준 상태는 **현재 h_t**, Bahdanau는 **s_{t−1}**. | Luong §3.1("Comparison to Bahdanau": "Bahdanau … only experimented with one alignment function, the concat product"), Table 4; NTM §3.3.1 Eq. 5–6. 제안: '제안' → '정리·비교', 표 아래에 "Luong: dot은 global, general은 local에서 최선(Table 4)" 한 줄. |
| 2 | 같은 슬라이드 ("Additive: 유연하지만 쌍마다 계산") | 속도 차이를 계산량 차이처럼 표현. Transformer 논문은 두 방식의 **이론적 복잡도는 비슷**하고 차이는 최적화된 행렬곱 덕분의 **실제 속도·메모리**라고 쓴다. Bahdanau도 U_a h_j를 미리 계산한다. | Vaswani §3.2.1; Bahdanau App. A.1.2. 제안: "쌍마다 작은 신경망 — 이론 복잡도는 비슷, 실제로는 행렬곱 한 번인 dot이 훨씬 빠름". |
| 3 | "임베딩에 위치를 더한다" (bullet "× √d: 원논문의 관례 — 임베딩 크기를 PE와 맞춘다") | 논문은 √d_model 곱셈의 **이유를 적지 않았다**. 'PE와 크기 맞추기'는 흔한 해석일 뿐. 또 이 곱셈은 §3.4에서 **입력·출력 임베딩과 softmax 앞 선형층의 가중치 공유**와 함께 언급된다. | Vaswani §3.4 ("In the embedding layers, we multiply those weights by √d_model."). 제안: "× √d: 원논문 §3.4의 설정(이유는 명시 안 됨; 흔한 해석은 PE와의 크기 균형)". |
| 4 | "“sin/cos가 정답”은 아니다" (notes "원논문도 학습형 위치 임베딩과 비교했고 비슷한 결과") | 사실이지만 **v2(2017-06-19) 이후**에만 있는 내용(v1에는 문장도, Table 3 (E) 행도 없음). 수치를 같이 주면 좋다. sinusoid 선택 이유(상대 위치 선형 표현 **가설**, 외삽 **가능성**)도 원문 근거로 보강 가능. 학습형 절대 위치는 BERT·GPT 이전에 **ConvS2S(2017)** 가 썼고, Transformer가 비교 대상으로 인용한 것도 ConvS2S[9]다. | Vaswani v2+ §3.5, Table 3 row (E): BLEU 25.7 vs base 25.8, PPL 4.92 동일. Gehring §3.1, Table 4. 제안: 표 '학습형 절대 위치' 행의 예에 "ConvS2S (2017)" 추가, notes에 "(NIPS판/arXiv v2+, Table 3 (E): 25.7 vs 25.8)". |
| 5 | "왜 √d_h로 나눌까" | 내용은 맞으나 출처 맥락이 빠짐: (a) 분산 = d_k 논증은 **각주 4, v2부터**(v1 없음), (b) 출발점은 "d_k가 크면 스케일 없는 dot보다 additive가 낫다"는 **Britz et al. 2017의 경험적 관찰**, (c) 저자 표현은 "We suspect"(추측). | Vaswani §3.2.1 + 각주 4(v2+). 제안: notes에 "원문: Britz et al. 관찰 → 'We suspect' → 각주(가정 하 분산 d_k)" 한 줄. 덱의 '단순화한 가정' 경고는 원문과 일치. |
| 6 | "여러 비교 · 전달 경로 만들기" (MultiHead = Concat(…)·W_O) | 식 자체는 NIPS판과 일치하지만, **v1에는 W^O가 없었다**(v2에서 "once again projected"와 W^O ∈ R^{h d_v × d_model} 추가). 원문 인용 표기는 NIPS판/v2+로. 또 multi-head의 원문 동기("single head는 averaging으로 서로 다른 부분공간·위치를 함께 보지 못한다", §2의 '유효 해상도 저하')를 lead/notes에 쓸 수 있다. | Vaswani v1 vs v2 §3.2.2; §2. |
| 7 | "Head를 늘리면 무엇이 달라지나" | 원문 실험 수치가 없음 → Table 3 (A)를 쓰면 좋다: 계산량 고정에서 h=1 24.9, h=4 25.5, h=8 25.8, h=16 25.8, h=32 25.4 (dev BLEU). "head 1개는 0.9 BLEU 나쁘고, 너무 많아도 떨어진다." 또한 warn 콜아웃("역할은 사후 관찰")은 옳지만, **저자 스스로** §4·부록에서 "heads clearly learn to perform different tasks"라고 주장했다는 점을 밝혀야 균형이 맞다(그 근거는 정성적 그림). | Vaswani §6.2, Table 3 (A); §4 마지막 문단; 부록 Fig. 3–5. |
| 8 | "Self-attention: 문장이 스스로를 참조한다" / summary "경로 길이 1, 순차 의존 없음" | 장점만 있고 비용이 빠짐. 원문 Table 1은 self-attention의 층당 복잡도 **O(n²·d)** (recurrent O(n·d²))를 함께 제시하고, "n < d일 때 더 빠르다"는 조건을 단다. 또 '순차 의존 없음'은 **층 내부/학습 시** 이야기이고, 자기회귀 생성은 여전히 토큰 단위 순차다. | Vaswani §4, Table 1; §3 (auto-regressive). 제안: Table 1을 그대로 옮긴 표 슬라이드 추가(경로 O(1) vs O(n), 순차 O(1) vs O(n), 비용 O(n²d) vs O(nd²)). |
| 9 | "Attention의 세 단계" / "정렬을 눈으로" (출처 맥락) | (a) Bahdanau 논문의 정렬 그림은 **영→불**(Figure 3)이고, 덱의 한→영 그림은 가상 예시임을 notes에 명시돼 있어 OK. 원문 그림에서 보여 준 것: 대체로 **단조**, 일부 **어순 반전**(European Economic Area), [the man]→[l' homme]의 soft 정렬. (b) Bahdanau에서는 key = value = h_j (Q/K/V 분리는 이후 정리) — Part 2로 넘어갈 때 한 줄로 연결하면 좋다. | Bahdanau §5.2.1, Figure 3; §3.1. |
| 10 | references 슬라이드 "[39][40] Attention 해석 관련 연구" / "가중치를 해석할 때" | 정확한 서지로 바꿀 것: Jain & Wallace (NAACL 2019) "Attention is not Explanation", Wiegreffe & Pinter (EMNLP 2019) "Attention is not not Explanation". 두 논문 모두 **BiLSTM attention 분류기** 대상이며 Transformer multi-head·번역은 다루지 않았다. W&P의 결론은 "attention이 설명이다"가 아니라 "J&W 실험이 반증하지 못했다 + 정의(plausible vs faithful)에 달렸다". | Jain §2, §6; Wiegreffe Abstract, §2.1, §6. |
| 11 | references "[17] Bahdanau, Cho & Bengio (2014)" / Part 1 "Attention (2014)" | 연도 표기: arXiv 2014-09, 학회 게재는 **ICLR 2015**. Luong은 Bahdanau를 "2015"로 인용한다. 또 "Attention은 2014" (misconceptions 표)는 Graves 2013(손글씨 합성 정렬)·NTM 2014를 고려하면 "**번역용 soft alignment는 2014**" 정도가 정확. | Bahdanau 표지("Published as a conference paper at ICLR 2015"), §6.1(Graves 2013). |
| 12 | "공식을 다섯 단계로" (softmax(QKᵀ/√d_h + M)V) | 원문 Eq.(1)에는 M이 없다(마스크는 §3.2.3에서 "softmax 입력을 −∞로"). 덱 표기는 교육용 확장으로 무방하나, "원문 Eq.(1) + §3.2.3의 마스크를 합친 표기"라고 notes에 적으면 정확. "cross-attention"도 원문 용어는 "encoder-decoder attention". | Vaswani §3.2.1 Eq.(1), §3.2.3. |
| 13 | "2017 Transformer: 오늘 배운 곳" (base d_ff = 2048) | 덱 값은 맞다(§3.3, v2+ Table 3). 단 v1 Table 3 base 행은 d_ff를 1024로 **오기**했으므로, 학생이 v1 PDF를 보면 혼동할 수 있다는 각주가 유용. 영→불 BLEU를 쓸 경우 v1–v4는 41.0, v5+는 41.8(본문은 41.0으로 남음). | Vaswani v1 Table 3 vs §3.3; v5+ Table 2. |

### 확인 결과 덱과 원문이 일치하는 곳(수정 불필요)
- Bahdanau 식 e = a(s_{t−1}, h_j), softmax, c_t = Σ α h_j; additive vᵀtanh(Ws + Uh) (App. A.1.2와 일치).
- d = 512, H = 8, d_h = 64, N = 6+6, 층별 별도 파라미터(§3.1, §3.2.2, §3.3).
- 세 종류 attention의 Q/K·V 출처와 범위(§3.2.3).
- PE 식과 d = 8 표 값, 4토큰 예제의 모든 숫자, 288 / 약 105만 파라미터, √d 표준편차 표(모두 파이썬 검산).
- "self-attention은 2017년 전에도 있었다", "Attention Is All You Need ≠ 다른 계산이 없다"(FFN·residual·LayerNorm·PE 존재, §3.1–3.5).
