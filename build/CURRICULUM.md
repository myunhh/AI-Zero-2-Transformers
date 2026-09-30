# AI Zero 2 Transformer — 6주 강의 설계 (v2)

원자료: `build/research/AI_Zero_2_Transformer.html` (텍스트: `build/research/source.txt`)
템플릿: `build/Lab-template.pptx` (AICA Lab) · 빌더: `build/deckkit.py` · 주차 스크립트: `build/weekN.py`

## 1. 무엇을 고쳤나 (v1 → v2)

| v1의 문제 | v2의 해결 |
|---|---|
| 1주차에 Softmax·Entropy·QKᵀ 등 **아직 쓸 곳이 없는 수학**을 먼저 몰아서 배움 | 수학은 **필요해지는 순간**에 배운다. 1주차: shape·내적·행렬곱·MSE·미분·경사하강 / 2주차: 연쇄법칙·Softmax·Cross-entropy |
| 계보(역사) 슬라이드가 주차 앞·뒤에 중복되고, 다음 주 내용을 미리 말해버림 | 매 주 **하나의 중심 질문**(원자료의 "여섯 질문")으로 시작하고, 역사는 그 질문에 답한 순간에만 등장 |
| 파트 순서가 개념의 의존 관계와 어긋남 (예: 역전파 설명 전에 "학습으로 찾은 XOR 해", Q/K/V 전에 위치 인코딩, RNN(1990) 전에 Word2Vec(2013)) | 모든 파트를 **문제 → 아이디어 → 계산 → 검증** 순서로 정렬, 앞 개념이 뒤 개념의 재료가 되도록 배치 |
| 주차 간 연결이 "다음 주 예고" 한 줄뿐 | 매 주 마지막 장 = **아직 풀리지 않은 문제**, 다음 주 첫 장 = 그 문제에서 출발 (바통 넘기기) |
| 템플릿 본문 개체 틀을 지우고 자유 도형으로만 구성 | 템플릿의 **제목 슬라이드·구역(제목) 슬라이드·Title and Content·마지막 슬라이드**를 그대로 사용, 본문은 템플릿 **본문 개체 틀과 글머리표**로 작성, 색은 템플릿 헤더/로고 색(01688F·72ABC8·00A3CA·58C4C4)만 사용 |

## 2. 과정 전체의 뼈대: 여섯 질문

| 주 | 중심 질문 (원자료 §01 "여섯 질문") | 시대 | 답이 된 아이디어 | 남기는 문제 → 다음 주 |
|---|---|---|---|---|
| 1 | 규칙을 다 쓰지 않고 **배울 수** 있을까? | 1943–1958 | Tensor, 모델, 손실, 경사하강법, 일반화 | 예/아니오를 가르는 뉴런은 무엇을 못 할까? |
| 2 | **직선으로 안 되는** 문제는? | 1958–1986 | Perceptron → XOR 한계 → MLP·비선형성 → 역전파 → Softmax·CE | 입력이 크고(이미지) 층이 깊어지면? |
| 3 | **공간** 구조를 어떻게 쓰고, **깊은** 모델은 어떻게 학습하나? | 1989–2016 | CNN(지역성·가중치 공유) → (옆길 SVM) → AlexNet의 조건 → Residual·Normalization | 길이가 제각각인 **순서** 데이터는? |
| 4 | 순서를 어떻게 표현하고, **먼 정보를 어떻게 기억**할까? | 1986–2014 | Token·Embedding → RNN → 기울기 소실 → LSTM → 언어모델·Word2Vec → Seq2Seq | 요약 벡터 하나에 다 담을 수 없다 (병목) |
| 5 | 필요할 때 **원문을 다시 찾아보면**? | 2014–2017 | Attention → Self-attention → Q/K/V → Scaled dot-product → Multi-head → 위치 정보 | 블록을 어떻게 조립·학습·생성하나? |
| 6 | **참조만으로** 시퀀스 모델을 만들면? | 2017– | FFN·Residual·LayerNorm → Mask·Teacher forcing → Cross-attn → 학습 → 생성·KV Cache → 실험 → 이후 | (과정 마무리: 다음 학습 방향) |

## 3. 매 주 공통 구성 (예측 가능한 리듬)

1. 표지 (템플릿 Title Slide)
2. 이번 주의 질문 (템플릿 구역 슬라이드)
3. 지난 주 → 남은 문제 → 이번 질문 (1주차는 과정 소개)
4. 과정 지도: 6개 질문 중 현재 위치
5. 오늘의 로드맵 + 학습 목표 ("~을 설명/계산할 수 있다")
6. 오늘의 새 용어 (용어 · 한 줄 뜻 · 비유)
7. Part 1..k — 각 Part는 템플릿 구역 슬라이드로 시작, 내용 슬라이드는 우상단 **단계 태그**(문제 · 아이디어 · 계산 · 검증 · 역사 · 코드)로 현재 위치를 표시
8. 한 장 요약 → 셀프 체크(정답은 노트) → 흔한 오해 → 과제 → 참고 자료 → **남은 문제와 다음 질문**
9. Question ? (템플릿 마지막 슬라이드)

각 슬라이드: 제목 + **핵심 한 줄**(굵은 청록) + 설명(템플릿 글머리표) + 시각 자료. 발표자 노트에는 "더 깊이" 설명과 예상 질문.

## 4. 주차별 흐름

### Week 1 — Tensor와 학습: 컴퓨터가 배운다는 것은?
- 과정 소개: 도착점(Transformer 그림을 설명하는 5가지 능력), 여섯 질문 지도, 공부법(문제→아이디어→계산→검증, 예측 후 확인)
- Part 1 규칙에서 학습으로 (1943 McCulloch–Pitts, 1950 Turing, 1956 Dartmouth / 규칙 vs 학습 / 모델 f_θ와 파라미터)
- Part 2 Tensor: 데이터를 담는 그릇 (스칼라→텐서, shape와 축의 의미 (B,N,d), 원소별 연산·broadcasting, 내적=가중합, 행렬곱과 shape 규칙, PyTorch)
- Part 3 모델과 손실: 얼마나 틀렸나 (ŷ=wx+b, MSE, 손실 곡선)
- Part 4 경사하강법: 틀린 만큼 고치기 (미분=변화율, gradient, 한 걸음 손계산, 학습률, 학습 루프 4단계, PyTorch 학습 루프)
- Part 5 일반화 (train/val/test, 과적합, 학습 방식 vs 아키텍처)
- 남은 문제: "예/아니오를 가르는 뉴런은 어떤 문제를 못 풀까?"

### Week 2 — Perceptron에서 MLP로: 직선으로 안 되는 문제는?
- Part 1 Perceptron(1958): 분류, 계단 함수, 결정 경계=직선, 학습 규칙, AND 학습
- Part 2 XOR(1969): AND/OR/XOR, 불가능 증명(부등식 모순), 『Perceptrons』와 AI 겨울(단일 원인 아님), 병행한 규칙 기반 AI
- Part 3 MLP: 은닉층=새 좌표, 선형층만 쌓으면 하나로 합쳐짐, 활성화 함수, 손으로 만든 XOR 해, shape
- Part 4 역전파(1986): 책임 나누기 문제, 연쇄법칙, 계산 그래프 forward/backward, 한 번의 업데이트, 학습된 XOR·모델 부족 vs 학습 실패, 역사(1970/1974/1986), autograd
- Part 5 확률로 답하기: Sigmoid·Softmax, Temperature, Entropy·Cross-entropy, 왜 MSE 대신 CE, Transformer 출력과의 연결
- 남은 문제: 이미지처럼 큰 입력 / 깊은 층

### Week 3 — CNN과 깊은 학습의 조건
- Part 1 이미지를 MLP로 다루면? (이미지=텐서, FC 파라미터 폭발, 이미지의 성질)
- Part 2 합성곱 (슬라이딩 내적, 공유·지역 연결, 출력 크기 공식, 채널과 파라미터, pooling, 수용 영역, LeNet, 등변성≠불변성, PyTorch, 네 개념 정리)
- Part 3 옆길: SVM(1995) (마진, 커널, 남긴 질문)
- Part 4 깊은 모델이 가능해진 조건 (sigmoid 기울기 곱, 2006 DBN, 2012 AlexNet, 여섯 조건, ILSVRC)
- Part 5 Residual과 Normalization (degradation, y=x+F(x), gradient 경로, 정규화 식, BatchNorm vs LayerNorm)
- 남은 문제: 순서가 있고 길이가 다른 데이터(언어)

### Week 4 — 언어·순서·기억: RNN, LSTM, Seq2Seq
- Part 1 문장을 숫자로 (토큰→ID→벡터, 번호≠의미, one-hot=lookup, 단어 vs 토큰, (B,N)→(B,N,d))
- Part 2 RNN(1986/1990) (순서·가변 길이 문제, 상태 전달, 식과 손계산, 펼친 그림, PyTorch shape)
- Part 3 장기 의존성(1991/1994) (예시, 기울기 곱 소실/폭주, 두 가지 이유)
- Part 4 LSTM(1997/2000) (cell state, 게이트, 갱신 손계산, 해결한 것·남은 것, 사고실험)
- Part 5 단어의 의미를 학습하기 (문장 확률=조건부 확률의 곱, 2003 신경 언어 모델, 2013 Word2Vec, 정적 vs 문맥 표현)
- Part 6 Seq2Seq(2014) (길이가 다른 입출력, Encoder–c–Decoder, 학습 목표, 두 논문, 병목)
- 남은 문제: 요약 벡터 하나의 병목 → "원문을 다시 보면?"

### Week 5 — Attention: 필요할 때 원문을 찾아보기
- Part 1 Attention(2014) (병목 재현, 정렬 점수→softmax→가중합, 손계산, 정렬 heatmap, 점수 함수, "본체로 쓰면?")
- Part 2 Self-attention과 Q/K/V (문장이 자신을 참조, Q/K/V 역할과 비유의 한계, 투영 행렬=파라미터, Q≠K≠V)
- Part 3 Scaled dot-product를 숫자로 (공식 단계 분해, 4토큰 예제, Query 하나 손계산, 전체 행렬, √dₕ, 경계 조건, shape)
- Part 4 Multi-head (여러 관점, head 축 만들기, shape 표 d=8·H=2·N=5, 코드, head 수의 효과)
- Part 5 순서 정보 (순열 등변성, 임베딩+PE, sinusoidal, 다른 방식들)
- Part 6 모아 보기 (2017 구조도에서 오늘 배운 부분, 세 종류 attention)
- 남은 문제: 블록 조립·학습·생성

### Week 6 — Transformer 완성: 조립·학습·생성, 그리고 이후
- Part 1 Encoder 한 층 (FFN, Residual, LayerNorm, Post-LN vs Pre-LN, shape 유지)
- Part 2 Decoder (정답 베끼기 문제, teacher forcing·shift, causal mask −∞, 세 mask, cross-attention, 출력 head)
- Part 3 끝까지 따라가기 (한 샘플 shape 추적, 파라미터 수)
- Part 4 학습 (NLL, 한 step, 원논문 조건, 병렬 학습 이유, 지표)
- Part 5 생성 (자기회귀, 선택 정책, KV Cache, 연산량·메모리)
- Part 6 직접 실험하기 (실습 순서, 9가지 검사, 실험 설계, 최종 프로젝트)
- Part 7 Transformer 이후와 마무리 (Encoder-only/Decoder-only, ViT·DiT, 원형 vs 후속 변형, 여섯 질문 회고, 구술 평가 과제)

## 5. 원자료 → 주차 대응 (빠짐 없음 확인용)

| 원자료 장 | 주차 |
|---|---|
| 00 도입, 01 계보 | W1(과정 소개·Part 1) + 각 주 "역사" 슬라이드에 분산 |
| 02 수학 준비 | W1(벡터·행렬·내적·미분) + W2(연쇄법칙·Softmax·Entropy/CE) + W5(QKᵀ) |
| 03 학습이란 | W1 Part 3–5 |
| 04 Perceptron→MLP | W2 |
| 05 CNN과 깊은 모델 | W3 |
| 06 언어를 벡터로 | W4 Part 1, 5 |
| 07 RNN·LSTM | W4 Part 2–4 |
| 08 Seq2Seq→Attention | W4 Part 6 + W5 Part 1 |
| 09 전체 구조 | W5 Part 6 + W6 도입 |
| 10 위치 정보 | W5 Part 5 |
| 11–13 Q/K/V, SDPA, Multi-head | W5 Part 2–4 |
| 14 FFN·Residual·LN | W6 Part 1 |
| 15 Mask·Teacher forcing | W6 Part 2 |
| 16 Encoder/Decoder 완성 | W6 Part 2–3 |
| 17 학습 | W6 Part 4 |
| 18 추론·KV Cache | W6 Part 5 |
| 19 연산량·메모리 | W6 Part 5 |
| 20–21 실습·실험 | W6 Part 6 (각 주 과제에도 분산) |
| 22 멘토링 운영안 | 매 주 공통 구성·과제 설계에 반영 |
| 23 Transformer 이후 | W6 Part 7 |
| 24 오개념 20가지 | 각 주 "흔한 오해"에 분산 |
| 25 개념 확인 18문항 | 각 주 셀프 체크에 분산 |
| 26 기호 사전, 27 참고문헌 | W6 부록 + 각 주 참고 자료 |

## 6. 날짜 (푸터)
W1 2026-10-05, W2 10-12, W3 10-19, W4 10-26, W5 11-02, W6 11-09
