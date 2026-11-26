# AI Zero 2 Transformer — 6주 강의 설계 (v3: 논문 기반)

원자료: `build/research/AI_Zero_2_Transformer.html` (텍스트: `build/research/source.txt`)
논문 노트: `build/research/papers/week1.md` … `week6.md` (원문을 읽고 숫자·식마다 §/Table/Figure 출처를 단 노트)
템플릿: `build/clean-template.pptx` (Apple 디자인 원칙) · 빌더: `build/deckkit.py` · 주차 스크립트: `build/weekN.py`
새 그림: `build/paper_figs_wN.py` (논문 그림·표를 도식으로 새로 그린 것 — 원본 이미지는 쓰지 않음)

## 1. 무엇이 바뀌었나 (v2 → v3)

| v2 | v3 |
|---|---|
| 개념 순서대로 설명하고, 논문은 참고 자료 표에만 등장 | 각 Part가 **논문 한 편**을 따라간다: 논문 카드 → 그 논문이 풀려던 문제 → 핵심 아이디어·식 → 손계산 → **원문이 보고한 실험·결과** → 한계와 다음 논문 |
| 숫자 출처가 불분명한 곳이 있었다 | 숫자·식은 원문에서 확인한 것만 쓰고, 발표자 노트마다 출처(§·Eq.·Table·Figure)를 적는다. 원문을 못 구한 논문(Minsky & Papert 1969, Bengio 1994 등)은 정확한 수치를 쓰지 않는다 |
| 교과서식 통념이 그대로 들어간 곳 | 원문과 다른 통념을 바로잡았다 (§4) |
| — | 매 주 **"이번 주의 논문"** 지도 슬라이드, 논문 카드(`Deck.paper`), 논문 읽기 과제(어떤 절·그림을 읽고 무엇을 제출하는지) |

디자인(Apple 디자인 원칙 테마)과 여섯 질문의 뼈대는 v2 그대로다.

## 2. 과정 전체의 뼈대: 여섯 질문

| 주 | 중심 질문 | 시대 | 이번 주의 논문 | 남기는 문제 → 다음 주 |
|---|---|---|---|---|
| 1 | 규칙을 다 쓰지 않고 **배울 수** 있을까? | 1943–1960 | McCulloch & Pitts 1943 · Turing 1950 §7 · Dartmouth 1955 · Widrow & Hoff 1960 · Cauchy 1847 · Robbins & Monro 1951 | 예/아니오를 가르는 뉴런은 무엇을 못 할까? |
| 2 | **직선으로 안 되는** 문제는? | 1958–1990 | Rosenblatt 1958 · Rosenblatt 1962 / Novikoff 1962 · Minsky & Papert 1969 · Cybenko / Hornik 1989 · Rumelhart·Hinton·Williams 1986 · Bridle 1989/90 | 입력이 크고(이미지) 층이 깊어지면? |
| 3 | **공간** 구조와 **깊은** 모델은? | 1980–2016 | Fukushima 1980 · LeCun 1989 · LeCun 1998 · Cortes & Vapnik 1995 · Hinton 2006 · Glorot & Bengio 2010 · Krizhevsky 2012 · Simonyan & Zisserman 2014 · Ioffe & Szegedy 2015 (+ Santurkar 2018) · He 2015 · Ba 2016 | 길이가 제각각인 **순서** 데이터는? |
| 4 | **먼 정보를** 어떻게 기억할까? | 1986–2016 | Sennrich 2016 · Elman 1990 · Hochreiter 1991 / Bengio 1994 / Pascanu 2013 · LSTM 1997 · Gers 2000 · Bengio 2003 · Mikolov 2013 · Cho 2014a · Sutskever 2014 · Cho 2014b | 고정 벡터 하나라는 병목 **가설** |
| 5 | **원문을 다시 찾아보면**? | 2014–2017 | Bahdanau 2014 · Luong 2015 · Cheng / Parikh 2016 · Gehring 2017 · Vaswani 2017 §3.2·§3.5·§4 · Jain & Wallace / Wiegreffe & Pinter 2019 | 블록을 어떻게 조립·학습·생성하나? |
| 6 | **참조만으로** 만들면? | 2017– | Vaswani 2017 §3·§5·§6 · Kingma & Ba 2015 · Szegedy 2016 · Xiong 2020 · Shazeer 2019 · Ainslie 2023 · Dao 2022 · Pope 2022 · GPT-1 · BERT · T5 · ViT · DiT · GLU · RoPE | (과정 마무리) |

## 3. 매 주 공통 구성

1. 표지 → 이번 주의 질문 → (2주차부터) 지난 주에서 이번 주로 → 오늘의 지도 → **이번 주의 논문** → 새 용어
2. Part 1..k — 각 Part = 논문 한 편(짧은 논문은 묶음). 단계 태그: 논문 · 문제 · 아이디어 · 계산 · 결과 · 검증 · 역사 · 코드 · 정리 · 실습.
   논문이 아닌 도구(텐서·shape, PyTorch, 이 과정의 실험)는 "도구" Part로 따로 표시한다.
3. 한 장 요약 → 셀프 체크(정답은 노트) → 흔한 오해 → 논문 읽기 과제 → 참고 자료(읽을 절) → 남은 문제와 다음 질문 → Q & A

## 4. 주차별 Part와 바로잡은 통념

### Week 1 — Tensor와 학습 (58장)
Part: McCulloch–Pitts 1943 · Turing 1950 · Dartmouth 1955 · 도구: Tensor와 shape · Widrow & Hoff 1960 · 경사하강법: Cauchy → LMS · 일반화
- McCulloch–Pitts에는 실수 가중치가 없다(시냅스 개수 + 절대 억제). '가중합 + 임계값'은 현대식 재서술.
- 선형 모델 + 제곱 오차 + 기울기 갱신 + 학습률 안정 조건의 출처는 Rosenblatt 1958이 아니라 Widrow & Hoff 1960.
- Turing 1950은 '평가'(§1)만이 아니라 '가르치는 기계'(§7)를 제안했다. PyTorch 예제는 전체 배치 경사하강이다.

### Week 2 — Perceptron에서 MLP로 (58장)
Part: Perceptron과 수렴 정리 (1958·62) · 직선의 벽과 학습 규칙의 공백 (1969) · MLP와 보편 근사 (1989) · 역전파 (1986) · Softmax (1989/90)
- 1958년 Perceptron은 S→A→R 망(무작위 고정 연결 + 강화). 오차 교정 규칙과 수렴 정리는 Rosenblatt 1962 / Novikoff 1962.
- 1969년의 핵심 결과는 XOR이 아니라 parity·connectedness와 '은닉층을 학습할 규칙의 부재'.
- 1986년 원 설정은 시그모이드·제곱 오차·전체 배치·모멘텀. 역전파 계보(Linnainmaa, Werbos, Parker, Le Cun)를 함께 밝힌다.
- 이 과정의 XOR 실험은 재현 가능한 ReLU 설정(은닉 2/4/8 → 20회 중 2/13/20 성공)으로 바꿨다 — v2의 4/15/19는 재현되지 않았다.

### Week 3 — CNN과 깊은 학습의 조건 (63장)
Part: 합성곱의 탄생 (1980·1989) · LeNet-5 (1998) · SVM (1995) · 깊이의 벽 (2006–2011) · AlexNet·VGG · BatchNorm · ResNet · LayerNorm과 정리
- AlexNet 15.3%는 CNN 7개 앙상블(2개는 외부 데이터 사전학습). 외부 데이터 없는 공식 결과 16.4%, 단일 CNN 18.2%. GoogLeNet은 6.66%.
- 2006 DBN의 미세 조정은 up-down 알고리즘(역전파 미세 조정은 Hinton & Salakhutdinov 2006, Bengio 2007).
- ResNet 2015는 degradation이 기울기 소실 때문이 아니라고 본다. I + ∂F/∂x 해석은 2016년 후속 논문. 원 블록은 덧셈 뒤 ReLU.
- LeNet-5의 S2/S4는 학습되는 평균 subsampling, 출력은 RBF. 1989년 망은 pooling 없이 stride 2. SVM 1995의 새 기여는 soft margin.

### Week 4 — RNN에서 Seq2Seq까지 (57장)
Part: 도구: 문장을 숫자로 · Elman (1990) · 장기 의존성 · LSTM (1997) → forget gate (2000) · 단어의 의미 · Encoder–Decoder
- 1997 LSTM에는 forget gate가 없다(입력·출력 게이트 + 고정 1.0 자기 연결). forget gate는 Gers 2000, 연속 입력에서 셀 상태가 커지는 문제 때문.
- Cho 2014a(GRU, SMT 구문 재점수)와 Cho 2014b(길이별 성능 저하)는 다른 논문.
- '병목'은 Cho 2014b의 가설이다. Sutskever 2014는 35단어 미만에서 저하가 없다고 보고했다.

### Week 5 — Attention (63장)
Part: Bahdanau 2014 · Luong 2015 · self-attention과 ConvS2S (2016–2017) · Vaswani §3.2 · Vaswani §3.5 · Vaswani §4 · attention은 설명인가 (2019)
- W^O, √d_k 각주, 학습형 PE 비교는 arXiv v1에 없고 v2(=NIPS 2017)부터 있다. √d_k 근거는 저자들의 "We suspect".
- ×√d_model의 이유는 논문에 없다. Luong은 점수 함수 네 가지를 비교했고 h_t를 쓴다(Bahdanau는 s_(t−1)).
- Bahdanau의 전체 test BLEU는 Moses보다 낮다(28.45 vs 33.30). 2019년 두 논문은 BiLSTM 분류기를 다뤘다.

### Week 6 — Transformer 완성 (55장)
Part: Vaswani §3 — 조립 · 학습 — §5·Adam·Label smoothing · Vaswani §6 — 결과와 비용 · Xiong 2020 — Post-LN vs Pre-LN · 생성 비용 — KV cache와 그 해법 · 도구: 이 과정의 작은 실험 · 2017 이후
- 파라미터 ≈ 63M과 논문 65M의 차이(~1.9M)는 논문에 설명이 없다(bias·LN은 0.1M). 37k 어휘는 영–독만.
- dropout 0.1은 base만(big 영–독 0.3). 임베딩+PE 합에도 dropout. 영–불 41.8은 후속 판본 수치(v1–v4: 41.0). 체크포인트 평균(5 / 20).
- Pre-LN은 Xiong 이전에도 쓰였고, BERT·GPT-1은 Post-LN. FlashAttention은 정확한 계산이며 FLOPs는 오히려 늘고 메모리 이동이 준다.

## 5. 날짜 (푸터)
W1 2026-10-05, W2 10-12, W3 10-19, W4 10-26, W5 11-02, W6 11-09
