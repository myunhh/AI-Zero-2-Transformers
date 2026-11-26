# Week 6 논문 노트 — Transformer 완성: 조립·학습·생성 — 참조만으로 만들면?

작성: 리서치 에이전트 (2026-11-26). 모든 원문은 scratchpad에서 읽음(저장소에 넣지 않음). 수치 계산은 `python3 -I`로 검산.

---

## 주차 요약 (논문 순서 = 시간 순서, 각 논문이 앞 논문의 어떤 한계를 풀었나)

| 연도 | 논문 | 앞 단계의 한계 → 이 논문의 답 |
|---|---|---|
| 2014/2015 | Kingma & Ba, **Adam** | SGD는 파라미터마다 기울기 크기가 다르면 학습률 하나로 맞추기 어렵다 → 1·2차 모멘트 이동평균 + 편향 보정으로 파라미터별 보폭 조절. Transformer 학습의 기본 optimizer. |
| 2015/2016 | Szegedy et al., **Inception-v3 §7 label smoothing** | one-hot 정답에 CE를 쓰면 logit 차이가 무한히 커지도록 밀어 과신·과적합 → 정답 분포를 (1−ε)δ + ε·u로 완화. Transformer가 ε=0.1로 사용. |
| 2017 | Vaswani et al., **Attention Is All You Need** | RNN Seq2Seq는 위치 방향 순차 계산 때문에 병렬화가 어렵다 → attention + FFN + 잔차 + LayerNorm만으로 Encoder–Decoder 구성, 8 GPU 12시간에 SOTA. |
| 2018 | Radford et al., **GPT-1** | 레이블 데이터가 적다 → 원형의 Decoder 쪽만 써서(cross-attention 없음) 대규모 무레이블 텍스트로 다음 토큰 예측 사전학습 후 미세조정. |
| 2018/2019 | Devlin et al., **BERT** | GPT는 왼→오 단방향이라 문맥 이해 과제에서 손해 → Encoder만 쓰고 MLM(15%, 80/10/10) + NSP로 양방향 사전학습. |
| 2019 | Shazeer, **Multi-Query Attention** | 자기회귀 생성 시 매 step 큰 K/V 텐서를 다시 읽는 메모리 대역폭이 병목 → 모든 head가 K/V 한 벌 공유. |
| 2019/2020 | Raffel et al., **T5** | 과제마다 head·목표가 달라 비교가 어렵다 → 모든 과제를 text-to-text로 통일, Encoder–Decoder + span corruption. |
| 2020 | Xiong et al., **Post-LN vs Pre-LN** | 원형 Post-LN은 warm-up 없으면 발산, warm-up은 왜 필요한가 불명 → 평균장 분석: Post-LN의 출력 근처 기울기가 크다. Pre-LN이면 warm-up 제거 가능. |
| 2020 | Shazeer, **GLU variants** | ReLU FFN 이후 개선 여지 → GEGLU/SwiGLU FFN이 같은 파라미터·연산에서 perplexity 개선. |
| 2020/2021 | Dosovitskiy et al., **ViT** | CNN 없이 순수 Transformer로 이미지를? → 16×16 patch를 token으로, 대규모 데이터(14M–300M장)면 CNN의 귀납 편향 없이도 우수. |
| 2021 | Su et al., **RoFormer/RoPE** | 덧셈형 위치 인코딩은 상대 위치를 내적에 간접 반영 → Q·K를 위치 각도만큼 회전해 내적이 상대 위치 m−n에만 의존. |
| 2022 | Dao et al., **FlashAttention** | N×N 점수 표를 HBM에 쓰고 읽는 IO가 실제 병목 → 타일링·재계산으로 정확한 attention을 HBM 접근 적게. |
| 2022 | Pope et al., **Efficiently Scaling Transformer Inference** | 500B급 모델 추론에서 KV cache가 파라미터보다 커진다 → 분할(partitioning) 전략 + multiquery로 긴 문맥·낮은 지연. |
| 2022/2023 | Peebles & Xie, **DiT** | diffusion은 U-Net 위주 → latent patch를 token으로 한 Transformer, adaLN-Zero 조건 주입, Gflops↑ → FID↓. |
| 2023 | Ainslie et al., **GQA** | MQA는 품질 저하·학습 불안정 → Query head를 G개 그룹으로 나눠 그룹마다 K/V 한 벌. MHA 체크포인트를 5% 추가학습으로 변환. |

---

## [Vaswani2017] Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin (2017) — Attention Is All You Need
- 서지: NIPS 2017 (31st Conference on Neural Information Processing Systems), arXiv:1706.03762. 읽은 판본: **v7 (2 Aug 2023)** https://arxiv.org/pdf/1706.03762 를 주 판본으로, **v1 (12 Jun 2017)** 및 v2–v6과 대조.
- 접근: 원문 확인 (v1–v7 모두 받아 핵심 수치 대조)

### 판본 차이 (v1 vs 이후) — 슬라이드에 숫자 쓸 때 주의
| 항목 | v1 (2017-06) | v2 | v3–v4 | v5–v7 (현행) |
|---|---|---|---|---|
| 초록 EN-FR BLEU | 41.0 | **41.2** | 41.0 | **41.8** |
| Table 2 Transformer(big) EN-FR | 41.0 | 41.0 | 41.0 | **41.8** |
| §6.1 본문 EN-FR | 41.0 | 41.0 | 41.0 | **41.0 (그대로 남음 → 현행판 내부 불일치)** |
| Table 3 base 행 d_ff | **1024 (오타)** | 2048 | 2048 | 2048 |
| Table 3 행 (E) 학습형 위치 임베딩 | **없음** | 있음 (4.92 / 25.7) | 있음 | 있음 |
| Table 3 (A),(D) params 열 | 65를 모든 행에 반복 | 빈칸(=base와 같음) | | |
- 정리: EN-DE 28.4(big)·27.3(base)는 모든 판본 동일. EN-FR은 "41.8 (현행판 초록·Table 2; 초판·§6.1 본문은 41.0)"으로 각주를 다는 것이 안전.

### 이 논문이 풀려던 문제
- 지배적인 시퀀스 변환 모델은 RNN/CNN Encoder–Decoder + attention. RNN은 h_t가 h_{t−1}에 의존하는 순차 계산이라 한 예제 안에서 병렬화가 불가능 (§1, Introduction 2단락).
- 목표: recurrence·convolution 없이 attention만으로 Encoder–Decoder를 만들어 병렬화와 품질을 동시에 (Abstract, §1 마지막 단락).

### 핵심 아이디어 (이번 주 범위: §3.1, §3.3, §3.4, §5, §6)
- **§3.1 스택**: Encoder = 동일 층 N=6개, 층마다 sublayer 2개(multi-head self-attention, position-wise FFN). 각 sublayer 출력은 `LayerNorm(x + Sublayer(x))` — Post-LN. 잔차를 위해 모든 sublayer와 임베딩 출력이 d_model=512.
- Decoder = N=6, Encoder의 2개 sublayer에 **Encoder 스택 출력 위 multi-head attention**(cross-attention)을 3번째로 추가. self-attention은 뒤 위치를 못 보게 mask하고, "output embeddings are offset by one position"과 결합해 위치 i의 예측이 i보다 앞 출력에만 의존 (§3.1 Decoder 단락).
- mask 구현: softmax 입력에서 불법 연결을 **−∞로 설정** (§3.2.3 마지막 문장).
- **§3.3 FFN**: `FFN(x) = max(0, xW1 + b1)W2 + b2` (Eq. 2). 위치마다 동일하게, 층마다 다른 파라미터. "kernel size 1인 convolution 두 개"로도 설명. d_model=512, d_ff=2048.
- **§3.4 임베딩·softmax**: 학습형 임베딩. **두 임베딩 층과 pre-softmax 선형 변환이 같은 가중치 행렬을 공유**(Press & Wolf [30] 유사). **임베딩 층에서는 가중치에 √d_model을 곱한다.**
- §3.5 sinusoidal PE를 임베딩에 더한다. 학습형 위치 임베딩도 "nearly identical results" (Table 3 (E), v2부터).

### 핵심 식
- 논문: `LayerNorm(x + Sublayer(x))` (§3.1) / `FFN(x)=max(0, xW1+b1)W2+b2` (Eq. 2) / `lrate = d_model^−0.5 · min(step_num^−0.5, step_num · warmup_steps^−1.5)` (Eq. 3, §5.3), warmup_steps=4000.
- 강의 표기: X ∈ ℝ^{B×S×d}, U = LN(X + Dropout(MHA(X))), X′ = LN(U + Dropout(FFN(U))); FFN: (B,S,d)→(B,S,d_ff)→(B,S,d); η(t) = d^−½ · min(t^−½, t·w^−³ᐟ²), w=4000. 출력: logits = (D)·Eᵀ (공유 시 W_vocab = Eᵀ), 입력 임베딩 = √d · E[id] + PE.

### 실험 설정 (§5)
- **데이터 (§5.1)**: WMT 2014 EN-DE 약 **4.5M 문장쌍**, BPE **공유 source-target 어휘 약 37,000**. EN-FR **36M 문장**, **32,000 word-piece** 어휘. 길이 비슷한 문장끼리 batch; batch당 **source 약 25,000 + target 약 25,000 토큰**.
- **하드웨어 (§5.2)**: 1대에 **NVIDIA P100 8장**. base: step당 약 **0.4초**, **100,000 step = 12시간**. big: step당 **1.0초**, **300,000 step (3.5일)**.
- **Optimizer (§5.3)**: Adam **β1=0.9, β2=0.98, ε=10⁻⁹** (Adam 기본값 β2=0.999, ε=10⁻⁸과 다름). Eq. 3, warmup_steps=4000.
- **규제 (§5.4)**: Residual dropout — 각 sublayer 출력에 (더하고 정규화하기 전에) dropout, **그리고 Encoder/Decoder 입력의 (임베딩 + PE) 합에도 dropout**. base P_drop=0.1. Label smoothing ε_ls=0.1 — "hurts perplexity … but improves accuracy and BLEU".
- **big 설정** (Table 3 마지막 행): N=6, d_model=1024, d_ff=4096, h=16, **P_drop=0.3**, 300K step, 213M params. 단 **EN-FR big은 P_drop=0.1** (§6.1).
- **추론 (§6.1)**: base는 10분 간격으로 저장한 **마지막 5개 체크포인트 평균**, big은 **마지막 20개 평균**. **beam 4, length penalty α=0.6** (dev에서 선택). 최대 출력 길이 = 입력 길이 + 50, 가능하면 조기 종료.
- 학습 FLOPs 추정 = 학습 시간 × GPU 수 × GPU당 지속 단정밀도 성능(P100 = 9.5 TFLOPS) (§6.1, 각주 5).

### 주요 결과
- **Table 2 (newstest2014)**: Transformer base EN-DE **27.3**, EN-FR **38.1**, 학습비용 **3.3·10¹⁸ FLOPs**; big EN-DE **28.4**, EN-FR **41.8 (현행판; v1–v4 41.0)**, **2.3·10¹⁹ FLOPs**. 비교: ConvS2S Ensemble 26.36 / 41.29 (7.7·10¹⁹ / 1.2·10²¹), GNMT+RL Ensemble 26.30 / 41.16, MoE 26.03 / 40.56.
  - 검산: base 8 × 9.5e12 × 12h×3600 = 3.28e18 ✓, big 8 × 9.5e12 × 3.5d×86400 = 2.30e19 ✓.
- **Table 3 (EN-DE dev newstest2013, beam search, 체크포인트 평균 없음; PPL은 wordpiece 단위)** — base: N 6, d 512, d_ff 2048, h 8, d_k=d_v 64, P_drop 0.1, ε_ls 0.1, 100K → **PPL 4.92, BLEU 25.8, 65M**.

| 행 | 변경 | PPL | BLEU | params(M) |
|---|---|---|---|---|
| (A) | h=1, d_k=d_v=512 | 5.29 | 24.9 | (65) |
| (A) | h=4, 128 | 5.00 | 25.5 | |
| (A) | h=16, 32 | 4.91 | 25.8 | |
| (A) | h=32, 16 | 5.01 | 25.4 | |
| (B) | d_k=16 | 5.16 | 25.1 | 58 |
| (B) | d_k=32 | 5.01 | 25.4 | 60 |
| (C) | N=2 | 6.11 | 23.7 | 36 |
| (C) | N=4 | 5.19 | 25.3 | 50 |
| (C) | N=8 | 4.88 | 25.5 | 80 |
| (C) | d_model=256, d_k=d_v=32 | 5.75 | 24.5 | 28 |
| (C) | d_model=1024, d_k=d_v=128 | 4.66 | 26.0 | 168 |
| (C) | d_ff=1024 | 5.12 | 25.4 | 53 |
| (C) | d_ff=4096 | 4.75 | 26.2 | 90 |
| (D) | P_drop=0.0 | 5.77 | 24.6 | |
| (D) | P_drop=0.2 | 4.95 | 25.5 | |
| (D) | ε_ls=0.0 | 4.67 | 25.3 | |
| (D) | ε_ls=0.2 | 5.47 | 25.7 | |
| (E) | 학습형 위치 임베딩 | 4.92 | 25.7 | |
| big | d 1024, d_ff 4096, h 16, P_drop 0.3, 300K | 4.33 | 26.4 | 213 |

  - 저자 해석 (§6.2): (A) 계산량 고정에서 head 1개는 최고 설정보다 0.9 BLEU 낮고, head가 너무 많아도 떨어진다. (B) d_k를 줄이면 품질 하락 → 호환성 함수가 쉽지 않다. (C)(D) 큰 모델이 좋고 dropout이 과적합 방지에 매우 유용. (E) 거의 동일.
  - (D)의 ε_ls 행이 §5.4 문장을 수치로 보여 준다: ε_ls=0 → PPL **좋아짐**(4.67) but BLEU **나빠짐**(25.3).
- **§6.3 영어 구문 분석 (Table 4, WSJ §23 F1)**: 4층, d_model=1024. WSJ만(약 40K 문장, 어휘 16K) **91.3**; semi-supervised(약 17M 문장, 어휘 32K) **92.7**. 최대 출력 = 입력+300, **beam 21, α=0.3**. RNNG(Dyer et al. 2016, 93.3 generative)를 제외한 기존 모델보다 좋음. 과제별 튜닝은 거의 없음.

### 파라미터 수 검증 (deck "≈ 63M vs 65M")
파이썬 검산 (`d=512, d_ff=2048, h=8, d_k=d_v=64, V=37,000` 공유 임베딩 1벌):
| 항목 | bias·LN 제외 | bias·LN 포함 |
|---|---|---|
| Encoder 층 (4d² + 2d·d_ff) | 3,145,728 (3.15M) ✓ | 3,152,384 |
| Decoder 층 (8d² + 2d·d_ff) | 4,194,304 (4.19M) ✓ | 4,204,032 |
| 6 + 6층 | 44,040,192 (44.0M) ✓ | 44,138,496 |
| 공유 임베딩 37,000×512 | 18,944,000 (18.9M) ✓ | 18,944,000 |
| 합계 | **62.98M** | **63.08M** |
- deck의 층·임베딩 숫자는 맞다. **그러나 "65M과의 차이는 편향·Norm 등"이라는 설명은 틀리다** — bias와 LayerNorm은 합쳐 약 0.1M밖에 안 된다. 남는 약 1.9M은 논문이 설명하지 않는다.
- Table 3 전체를 같은 식으로 계산하면 일관된 패턴이 보인다 (계산 / 논문): N=2 33.7/36, N=4 48.4/50, N=8 77.8/80, d_k=16 56.0/58, d_k=32 58.4/60, d_ff=1024 50.5/53, d_ff=4096 88.3/90, d=256 26.8/28, d=1024 163.9/168, big 214.2/213.
  - d=512 행은 모두 **약 +2M**, d=256은 +1.2M, d=1024는 +4M → 차이가 **d에 비례**한다 = 어휘 행 수가 37,000보다 약 4k 많은 것(≈41k)과 맞는 패턴. 단 big 행(213 < 214)은 이 패턴과 맞지 않는다. **결론: 공식은 Table 3의 상대 변화를 잘 재현하지만, 절대값 65M과의 약 2M 차이의 원인은 논문으로 확정할 수 없다** (실제 tensor2tensor 어휘 크기 등 추정만 가능).
- 주의: 4d²는 h·d_k = d일 때만 성립 (Table 3 (B)는 d_k만 줄여 W_Q·W_K가 작아짐 → 58M, 60M이 공식으로 재현됨).
- "37,000"은 EN-DE BPE 어휘. EN-FR(32,000 word-piece)은 임베딩이 16.4M이 된다.

### 저자가 밝힌 한계 / 이후 비판
- §4: self-attention은 n < d일 때 recurrent보다 빠르다; 매우 긴 시퀀스를 위해 크기 r 이웃만 보는 restricted attention을 향후 과제로 언급. §7: 이미지·오디오·비디오용 local attention, "Making generation less sequential"을 향후 목표로 명시 — 즉 저자들도 **생성은 순차적**임을 인정.
- 이후 비판: Post-LN의 warm-up 의존성(Xiong 2020), 생성 시 KV 메모리 대역폭(Shazeer 2019).

### 흔한 오해 바로잡기
- "attention을 처음 제안" ✗ — Bahdanau 2014 등 기존 Encoder–Decoder에 이미 attention이 있었다 (§1, §2). 새로운 점은 recurrence/convolution을 **완전히 제거**한 것.
- "Transformer는 warm-up 없이도 잘 된다" ✗ — 원형(Post-LN)은 warm-up 4000 step 사용; 없으면 학습이 불안정 (Xiong 2020).
- "41.8이 처음부터 보고된 숫자" ✗ — 초판은 41.0, 현행판에서도 §6.1 본문은 41.0.
- "big도 dropout 0.1" ✗ — big(EN-DE)은 0.3, EN-FR big만 0.1.
- "label smoothing은 perplexity를 개선" ✗ — 논문은 perplexity를 **해친다**고 명시 (Table 3 (D)로 확인).

### 슬라이드용 손계산 예시 (검산 완료)
- 학습률 (d=512, w=4000): step 1 → 1.75e−7, 1000 → 1.75e−4, **4000 → 6.99e−4 (최고)**, 10,000 → 4.42e−4, 100,000 → 1.40e−4. big(d=1024)의 최고점은 4.94e−4.
- 학습비용: 8 GPU × 9.5 TFLOPS × 12 h = 3.28·10¹⁸ ≈ Table 2의 3.3·10¹⁸.
- 파라미터: 위 표.
- 원형 base Decoder self-attention KV cache (FP32, 6층, B=1, 길이 100): 2·6·1·100·8·64·4 B = 2.46 MB.

### 다시 그릴 만한 그림
- Figure 1 (전체 구조: Encoder N×, Decoder N×, Add & Norm, shifted right outputs, 공유 임베딩 화살표 추가 권장).
- Figure 2 (scaled dot-product attention의 Mask(opt.) 위치 — softmax 앞).
- Table 3를 막대/점 그림으로: (A) head 수 vs BLEU, (C) params vs BLEU, (D) ε_ls의 PPL↔BLEU 반대 방향.

### 읽기 안내
- §3.1 + Figure 1 → §5 전체(1쪽) → §6.2 Table 3.

---

## [Kingma2015] Kingma & Ba (2014/2015) — Adam: A Method for Stochastic Optimization
- 서지: ICLR 2015, arXiv:1412.6980. 읽은 판본: v9 (30 Jan 2017) https://arxiv.org/pdf/1412.6980
- 접근: 원문 확인
- 이 논문이 풀려던 문제: 잡음이 크고 희소한 기울기, 고차원 파라미터에서 효율적인 1차 확률적 최적화 (Abstract, §1).
- 핵심 아이디어: 기울기의 지수 이동평균 m_t(1차)와 제곱 기울기의 이동평균 v_t(2차)를 유지, 0 초기화로 생기는 편향을 (1−β^t)로 나눠 보정, 파라미터별로 m̂/√v̂ 크기만큼 이동. 기울기의 대각 스케일 변화에 불변 (Abstract, §2).
- 핵심 식 (Algorithm 1, p.2): m_t ← β1·m_{t−1} + (1−β1)·g_t; v_t ← β2·v_{t−1} + (1−β2)·g_t²; m̂_t ← m_t/(1−β1^t); v̂_t ← v_t/(1−β2^t); θ_t ← θ_{t−1} − α·m̂_t/(√v̂_t + ε). 기본값 α=0.001, β1=0.9, β2=0.999, ε=10⁻⁸.
  - 강의 표기: w ← w − η · m̂/(√v̂ + ε). Transformer는 β2=0.98, ε=10⁻⁹, η는 Eq. 3 스케줄.
- 실험 설정/결과: 로지스틱 회귀(MNIST), MLP, CNN(CIFAR-10) 등에서 SGD+momentum, AdaGrad, RMSProp과 비교 (§6). 이번 주에는 상세 불필요.
- 한계/이후 비판: (일반적으로 알려진 내용) 수렴 증명의 오류가 이후 지적됨(Reddi et al. 2018, AMSGrad); Transformer에서는 초기 adaptive 학습률의 분산이 커서 warm-up이 필요하다는 주장(Liu et al. 2019, RAdam — Xiong 2020이 인용).
- 흔한 오해: "Transformer는 Adam 기본값을 쓴다" ✗ — β2=0.98, ε=1e−9로 바꿨고 학습률은 스케줄.
- 손계산 (검산): 첫 step, g=0.5, β1=0.9, β2=0.98, α=7e−4: m=0.05, v=0.005, m̂=0.5, v̂=0.25 → 이동량 = 7e−4·0.5/0.5 = **7e−4** (첫 step은 기울기 크기와 무관하게 약 α만큼 움직인다 → warm-up이 필요한 직관).
- 그림: Algorithm 1 박스를 의사코드로 재작성.
- 읽기 안내: Algorithm 1, §2.1(보폭 해석), §3(편향 보정).

---

## [Szegedy2016] Szegedy, Vanhoucke, Ioffe, Shlens, Wojna (2016) — Rethinking the Inception Architecture for Computer Vision, §7 Label Smoothing
- 서지: CVPR 2016, arXiv:1512.00567. 읽은 판본: v3 (11 Dec 2015) https://arxiv.org/pdf/1512.00567
- 접근: 원문 확인 (§7만 정독)
- 문제: one-hot 정답에서 CE 최대화는 정답 logit이 다른 모든 logit보다 훨씬 커지도록 밀어 (1) 과적합, (2) 경계된 기울기와 결합해 적응력 저하 — "too confident" (§7).
- 핵심 아이디어/식: 정답 분포를 q′(k|x) = (1−ε)·δ_{k,y} + ε·u(k)로 바꾼다 (§7). 손실 H(q′, p) = (1−ε)H(q, p) + ε·H(u, p) — 두 번째 항이 예측 분포가 사전분포 u에서 멀어지는 것을 벌한다(KL과 상수 차이). 기울기 ∂ℓ/∂z_k = p(k) − q(k) ∈ [−1, 1].
  - 강의 표기: 정답 y, 어휘 |V|, u = 1/|V| → 정답 칸 목표 1−ε+ε/|V|, 나머지 ε/|V|.
- 실험: ImageNet K=1000, u(k)=1/1000, ε=0.1 → top-1·top-5 오류 약 0.2%p 개선 (§7 마지막 단락, Table 3).
- 오해: "label smoothing은 Transformer가 발명" ✗ (이 논문); "정답 외 클래스에만 ε를 나눈다" — 원 정의는 u(k)가 정답 클래스도 포함 (구현마다 다름 → 표기 명시).
- 손계산 (검산): |V|=5, ε=0.1 → 목표 (0.92, 0.02, 0.02, 0.02, 0.02). 예측 p=(0.7, 0.1, 0.1, 0.05, 0.05): hard CE = 0.357, smoothed CE = 0.540 (smoothed loss는 0이 될 수 없다 → label-smoothed loss의 exp를 perplexity로 쓰면 안 되는 이유).
- 읽기 안내: §7 (1쪽).

---

## [Xiong2020] Xiong, Yang, He, Zheng, Zheng, Xing, Zhang, Lan, Wang, Liu (2020) — On Layer Normalization in the Transformer Architecture
- 서지: ICML 2020, PMLR 119 (PDF 표기는 "PMLR 108"), arXiv:2002.04745. 읽은 판본: v2 (29 Jun 2020) https://arxiv.org/pdf/2002.04745
- 접근: 원문 확인
- 문제: Post-LN Transformer는 학습률 warm-up이 필수이고, 최종 성능이 최대 학습률·warm-up 길이에 민감(Popel & Bojar 2018) — 느리고 튜닝 비용 큼. 왜 필요한가? (Abstract, §1)
- 핵심 아이디어: 평균장 이론으로 **초기화 시점** 기울기를 분석. Post-LN은 출력층 근처 파라미터의 기대 기울기가 크고, 큰 학습률을 바로 쓰면 불안정 → warm-up이 이를 피하게 해 준다. Pre-LN(LN을 잔차 안, sublayer 앞에 + 마지막에 final LN)은 기울기가 잘 행동 → warm-up 제거 가능 (Abstract, §3.3).
- 핵심 식: Table 1 (Post-LN: x_{l+1} = LN(x + F(x)); Pre-LN: x_{l+1} = x + F(LN(x)), 끝에 Final LayerNorm). **Theorem 1** (§3.3): 마지막 층 FFN W² 기울기 Frobenius norm 상한 — Post-LN **O(d√(ln d))** (L과 무관), Pre-LN **O(d√(ln d / L))** (층 수가 늘면 감소).
  - 강의 표기: ‖∂L/∂W2_last‖ ≲ d√ln d (Post) vs d√(ln d/L) (Pre).
- 실험 설정: IWSLT14 De-En(§3.2, Adam β=(0.9, 0.98), lr_max 5e−4 또는 1e−3, warm-up 1/500/4000 step, 이후 inverse sqrt), WMT14 En-De(base 설정), BERT 사전학습. Pre-LN은 warm-up 없이 IWSLT 초기 lr 5e−4, WMT 7e−4/1.5e−3 (§4.1).
- 주요 결과:
  - Post-LN은 warm-up 없이는 학습이 안 되고(Adam·SGD 모두, Figure 2), warm-up 4000보다 500이 나쁨. → warm-up의 이점이 Adam 고유가 아니다 (§3.2).
  - Figure 3: 6-6~14-14 모델 초기화 시 마지막 FFN 기울기 norm — Post-LN은 약 1.6으로 일정, Pre-LN은 층 수에 따라 감소. Post-LN은 층 index가 클수록 기대 기울기가 커지고 Pre-LN은 층 간 거의 일정.
  - Pre-LN(warm-up 없음)이 Post-LN과 비슷한 최종 성능(IWSLT BLEU 약 34, val loss 약 4)에 더 빨리 도달: IWSLT에서 Pre-LN 9번째 체크포인트 ≈ Post-LN 15번째 (§4.2).
  - BERT (Figure 5a): 원문 문장은 "Post-LN model achieves 1.69 validation loss at 500k updates while the Pre-LN model achieves similar validation loss at 700k updates … 40% speed-up". 700/500 = 1.4이므로 **두 모델 이름이 뒤바뀐 서술로 보인다**(Pre-LN 500k ≈ Post-LN 700k가 문맥상 맞음). 인용 시 "같은 val loss 1.69에 약 40% 적은 update로 도달"만 쓰고 숫자 배치는 Figure 5a로 확인할 것.
  - RAdam보다 LN 위치 변경의 효과가 "dominates" (§4.2).
- 저자가 밝힌 한계: 이론은 여러 단순화(초기화 시점, 단순화된 attention) 위에 있다(§3.4 첫 문장); 경험적으로 검증.
- 흔한 오해:
  - "Pre-LN은 Xiong et al.이 발명" ✗ — Baevski & Auli 2018, Child et al. 2019, Wang et al. 2019가 이미 제안(§2). 이 논문의 기여는 **warm-up 필요성의 이론적 설명과 warm-up 제거**. Nguyen & Salazar 2019도 독립적으로 관찰.
  - "Pre-LN이 항상 최종 품질이 더 좋다" ✗ — 논문은 "comparable" 최종 성능 + 빠른 수렴을 보고.
  - "후속 모델은 모두 Pre-LN" ✗ — BERT(2018)는 Post-LN(이 논문 §1이 Post-LN 기반 사전학습 모델로 Devlin et al.을 인용). T5·ViT는 Pre-LN (각 논문 확인).
- 손계산: Pre/Post 상한 비 = 1/√L → L=6: 0.41, L=12: 0.29, L=24: 0.20 (상수 무시, 상한끼리의 비임을 명시).
- 다시 그릴 그림: Figure 1 (Post-LN vs Pre-LN 층 도식), Figure 3(c)(d) (층 수 vs 마지막 FFN 기울기 norm).
- 읽기 안내: Table 1 + Figure 1, Theorem 1 해설 문단, Figure 2.

---

## [Radford2018] Radford, Narasimhan, Salimans, Sutskever (2018) — Improving Language Understanding by Generative Pre-Training (GPT-1)
- 서지: OpenAI 기술 보고서(학회 미게재), 2018. 읽은 판본: https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf
- 접근: 원문 확인
- 문제: 레이블 데이터는 적고 무레이블 텍스트는 많다 → 생성적 사전학습 + 판별적 미세조정 (Abstract, §1).
- 핵심 아이디어/식 (§3.1–3.2): L1 = Σ log P(u_i | u_{i−k..i−1}) (Eq. 1); h0 = U·W_e + W_p, h_l = transformer_block(h_{l−1}), P(u) = softmax(h_n W_eᵀ) (Eq. 2 — **출력에 임베딩 전치 = weight tying**). 미세조정 L3 = L2 + λ·L1 (Eq. 5, λ=0.5), 추가 파라미터는 W_y와 구분자 임베딩뿐.
  - 논문은 "multi-layer Transformer **decoder** [34]" (Liu et al. 2018)를 사용한다고 명시 — Decoder-only LM은 GPT-1이 처음이 아니다.
- 실험 설정 (§4.1): BooksCorpus(7,000권 이상 미출간 책 — 긴 연속 텍스트). **12층 decoder-only, masked self-attention, d=768, 12 head, FFN 3072**. Adam max lr 2.5e−4, 처음 2000 update 선형 증가 후 cosine으로 0까지. 100 epoch, batch 64 × 연속 512 토큰. N(0, 0.02) 초기화, BPE 40,000 merges, residual·embedding·attention dropout 0.1, 수정 L2 w=0.01, **GELU**, **학습형 위치 임베딩**. BooksCorpus token perplexity 18.4.
- 주요 결과: 12개 과제 중 9개 SOTA; Story Cloze +8.9%, RACE +5.7%, MultiNLI +1.5% (Abstract), GLUE 72.8 (이전 68.9).
- 오해: "GPT-1 = 117M" — **논문에 파라미터 수가 적혀 있지 않다** (흔히 인용되는 117M은 외부 수치, 슬라이드에 쓰려면 "약, 외부 추정" 표시). "GPT가 Decoder-only를 발명" ✗.
- 읽기 안내: §3.1 Eq. 1–2, §4.1 Model specifications, Figure 1(입력 변환).

## [Devlin2019] Devlin, Chang, Lee, Toutanova (2018/2019) — BERT
- 서지: NAACL-HLT 2019, arXiv:1810.04805. 읽은 판본: arXiv 최신판 https://arxiv.org/pdf/1810.04805
- 접근: 원문 확인
- 문제: GPT처럼 왼→오 단방향 LM은 문장 수준·토큰 수준 이해 과제에서 양쪽 문맥을 못 쓴다 (§1).
- 핵심: **양방향 Transformer encoder**. **MLM**: WordPiece 토큰의 15% 위치를 골라, 그중 80% [MASK], 10% 무작위 토큰, 10% 그대로 → 원 토큰 예측(§3.1 Task #1). [MASK]가 미세조정 때 없다는 불일치를 줄이려는 설계. **NSP**: 50% 실제 다음 문장(IsNext)/50% 무작위(NotNext), [CLS] 표현 C로 분류 (Task #2; 최종 NSP 정확도 97–98%).
- 크기 (§3): **BERT_BASE L=12, H=768, A=12, 110M**; **BERT_LARGE L=24, H=1024, A=16, 340M**. BASE는 GPT와 같은 크기로 비교하려고 선택. WordPiece 30,000 어휘.
- 학습 (§3.1, 부록 A.2): BooksCorpus 800M 단어 + 영어 Wikipedia 2,500M 단어. batch 256 시퀀스 × 512 토큰(=128,000 토큰), 1,000,000 step(약 40 epoch), Adam lr 1e−4, β1 0.9, β2 0.999, warm-up 10,000 step 후 선형 감소, dropout 0.1, gelu. 90% step은 길이 128, 나머지 10%는 512.
- 결과: GLUE 80.5 (+7.7), MultiNLI 86.7, SQuAD v1.1 F1 93.2, v2.0 F1 83.1 (Abstract). Table 5: NSP 제거 시 QNLI·MNLI·SQuAD 성능 하락 (이후 RoBERTa가 NSP 필요성에 반론 — 일반적으로 알려진 내용).
- 오해: "MLM = 정답 누출" ✗ — 입력에서 가린 위치를 복원하는 별도 목표. "BERT는 Pre-LN" ✗ (원형 Post-LN).
- 읽기 안내: Figure 1, §3.1, Figure 3(BERT·GPT·ELMo 비교).

## [Raffel2020] Raffel, Shazeer, Roberts, Lee, Narang, Matena, Zhou, Li, Liu (2019/2020) — Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer (T5)
- 서지: JMLR 21(140):1–67, 2020, arXiv:1910.10683. 읽은 판본: arXiv 최신판 https://arxiv.org/pdf/1910.10683
- 접근: 원문 확인 (§2.1, §2.2, §3.1.4 목표, §3.6 크기 위주)
- 문제: 전이학습 기법(구조·목표·데이터)이 제각각이라 체계적 비교가 어렵다 → 모든 과제를 "텍스트 입력 → 텍스트 출력"으로 통일 (§1, Figure 1: "translate English to German: That is good." → "Das ist gut.").
- 구조 (§2.1): 원형 Encoder–Decoder를 거의 그대로 따르되 — **LN을 각 subcomponent 입력에(Pre-LN)**, **bias 없는 단순화 LN(재스케일만)**, **상대 위치 bias**(32 bucket, 최대 offset 128). Dropout은 FFN 안, skip, attention 가중치, 스택 입출력에.
- 목표 (§3.1.4, Figure 2): **span corruption** — 토큰 15%를 떨어뜨리고, 연속 구간은 고유 sentinel 하나(<X>, <Y>)로 대체; 출력은 sentinel로 구분된 떨어진 구간들 + 마지막 sentinel. 평균 span 길이 3이 약간(유의하게) 좋음 (§3.3.4).
- 데이터: C4 약 750GB 정제 영어 웹 텍스트 (§2.2). SentencePiece 32,000 어휘. 기본 사전학습 2³⁵ ≈ 34B 토큰.
- 크기 (§3.6/§3.7): **Small ≈60M, Base ≈220M (BERT_BASE 크기 encoder+decoder), Large ≈770M, 3B(≈2.8B), 11B** (11B는 d_ff=65,536, 128 head).
- 결과: T5-11B GLUE 평균 90.3, SuperGLUE 88.9 (이전 84.6) (§3.7).
- 오해: "T5는 원형과 똑같다" ✗ — Pre-LN, bias 없는 LN, 상대 위치 bias. "Decoder-only보다 Encoder–Decoder가 보편적으로 우월" — 논문의 비교는 그들 설정(denoising 목표, 비슷한 계산량)에서의 결과.
- 읽기 안내: Figure 1, Figure 2, §3.2(구조 비교: encoder-decoder vs LM vs prefix LM, Figure 3–4).

---

## [Dosovitskiy2021] Dosovitskiy et al. (2020/2021) — An Image is Worth 16x16 Words (ViT)
- 서지: ICLR 2021, arXiv:2010.11929. 읽은 판본: arXiv 최신판 https://arxiv.org/pdf/2010.11929
- 접근: 원문 확인
- 문제: 비전에서 attention은 CNN과 결합되거나 일부만 대체; 순수 Transformer를 이미지 patch 시퀀스에 직접 적용하면? (§1)
- 핵심 (§3.1, Eq. 1–4): 이미지 x ∈ ℝ^{H×W×C} → P×P patch N = HW/P²개를 펼쳐 학습형 선형 투영으로 D차원 "patch embedding". BERT처럼 **학습형 [class] 토큰**을 앞에 붙이고 그 최종 출력이 이미지 표현; 사전학습 head는 은닉층 1개 MLP, 미세조정 head는 선형 1층. **학습형 1D 위치 임베딩**(2D-aware는 유의한 이득 없음). **LN을 각 블록 앞에(Pre-LN)**.
- 크기 (Table 1): **ViT-Base 12층, D 768, MLP 3072, 12 head, 86M**; **ViT-Large 24, 1024, 4096, 16, 307M**; **ViT-Huge 32, 1280, 5120, 16, 632M**. 표기 ViT-L/16 = Large, patch 16×16. patch가 작을수록 시퀀스가 길어져 비싸다.
- 데이터 규모 발견 (§1, §4.3, Figure 3–4): ImageNet(1.3M)만으로 학습하면 같은 크기 ResNet보다 몇 %p 낮음 — 귀납 편향(지역성·이동 등변성) 부족. **14M–300M장(ImageNet-21k, JFT-300M)** 에서는 "large scale training trumps inductive bias". ImageNet 사전학습에서는 ViT-L이 ViT-B보다 나쁘고, JFT-300M에서야 큰 모델의 이점이 온전히 나타난다.
- 결과 (Table 2): ViT-H/14 (JFT) ImageNet **88.55%**, ReaL 90.72%, CIFAR-100 94.55%, VTAB 77.63%, 사전학습 **2.5k TPUv3-core-days** (BiT-L 9.9k, Noisy Student 12.3k). ViT-L/16 (I21k) 85.30%, 0.23k.
- 오해: "ViT가 patch attention을 처음" ✗ — Cordonnier et al. 2020이 2×2 patch로 먼저(§2 관련연구). 최고 성적은 ViT-H/**14**를 해상도 518로 미세조정한 것(§4.2) — 224/16 = 196 patch 예시는 설명용.
- 손계산: 224, P=16 → 14×14 = **196** patch, patch당 16·16·3 = **768** 값; P=14 → 256, 588; P=32 → 49, 3072; 518, P=14 → 1369 patch.
- 읽기 안내: Figure 1, §3.1 Eq. 1–4, Figure 3.

## [Peebles2023] Peebles & Xie (2022/2023) — Scalable Diffusion Models with Transformers (DiT)
- 서지: ICCV 2023, arXiv:2212.09748. 읽은 판본: arXiv 최신판 https://arxiv.org/pdf/2212.09748
- 접근: 원문 확인
- 문제: diffusion 백본은 U-Net 위주; U-Net의 귀납 편향이 필수인가? Transformer로 바꾸고 계산량(Gflops)에 따른 확장성을 본다 (§1).
- 핵심 (§3.2): Stable Diffusion의 VAE latent(256×256×3 → **32×32×4**, downsample 8)를 p×p patch로 "patchify" → 길이 T = (I/p)² 시퀀스 (Figure 4). ViT식 주파수 기반 위치 임베딩. 조건(timestep t, class c) 주입 4가지 비교: in-context, cross-attention(약 15% Gflops 추가), adaLN, **adaLN-Zero** — LN의 γ, β를 t·c 임베딩 합에서 회귀하고, 잔차 연결 직전 스케일 α도 회귀하며 **α를 0으로 초기화 → 블록 전체가 항등 함수로 시작**.
- 크기 (Table 1): DiT-S 12층/384/6 head/1.4 Gflops, DiT-B 12/768/12/5.6, DiT-L 24/1024/16/19.7, DiT-XL 28/1152/16/29.1 (I=32, p=4 기준). p ∈ {2, 4, 8}; p는 Gflops에 크게 영향, 파라미터 수에는 거의 무영향.
- 학습 (§4): class-conditional ImageNet 256/512, AdamW 상수 lr 1e−4, weight decay 없음, batch 256, 수평 뒤집기만; **warm-up·규제 불필요**했다고 보고. ADM 하이퍼파라미터 유지.
- 결과: adaLN-Zero가 모든 학습 단계에서 FID 최저(Figure 5; 400K step XL/2: adaLN-Zero 19.47, adaLN 25.21, cross-attn 26.14, in-context 35.24 — 부록 표). **Gflops와 FID 사이 강한 음의 상관**(Figure 8), 파라미터가 아니라 Gflops가 핵심. DiT-XL/2(118.6 Gflops, 675M params) 7M step, cfg=1.5 → 256×256 **FID 2.27** (이전 LDM 3.60), 512×512 FID 3.04 (ADM 3.85).
- 오해: "DiT = 텍스트-이미지 모델" ✗ (원형은 class conditional). "DiT는 토큰을 하나씩 생성" ✗ — 모든 latent patch의 노이즈를 동시에 예측, 반복은 diffusion step.
- 손계산: latent 32×32×4, p=2 → T=256 token(patch당 16값), p=4 → 64, p=8 → 16.
- 읽기 안내: Figure 3(블록 설계), Figure 4(patchify), Figure 2 좌(Gflops vs FID).

---

## [Shazeer2019] Shazeer (2019) — Fast Transformer Decoding: One Write-Head is All You Need (MQA)
- 서지: arXiv:1911.02150 (학회 미게재). 읽은 판본: v1 (6 Nov 2019)
- 접근: 원문 확인
- 문제: 학습은 길이 방향 병렬이라 빠르지만 **증분(incremental) 생성은 병렬화 불가**하고, 매 step 큰 K/V 텐서를 다시 읽는 **메모리 대역폭**이 병목 (Abstract, §1).
- 핵심/식: §2.3.1 batched MHA: 연산 Θ(bnd²), 메모리 O(bnd + bhn² + d²) → 비율 O(1/k + 1/(bn)) — 좋음. §2.4.1 증분 MHA(n번 호출): 연산 Θ(bnd²), 메모리 Θ(bn²d + nd²) → **비율 Θ(n/d + 1/b)**; n≈d 또는 b≈1이면 1에 가까워 대역폭 병목. **MQA**: 모든 head가 K, V 한 벌 공유 → 메모리 Θ(bnd + bn²k + nd²), 비율 **Θ(1/d + n/(dh) + 1/b)** — 문제 항 n/d를 h배 줄임 (§3.1).
- 실험: WMT14 EN-DE, Encoder–Decoder 6+6층, d_model 1024, h=8, d_k=d_v=128, 100k step; MQA는 파라미터 맞추려고 d_ff 4096→5440. 모든 attention(Encoder self, Decoder self, cross)을 MQA로.
- 결과 (Table 1, 2): dev BLEU MHA 26.7 vs MQA 26.5, test beam4 28.4 vs 28.5; ln(PPL) 1.424 vs 1.439. 디코더 추론 per-token **46µs → 3.8µs**, beam-4 203 → 32µs (TPUv2). 학습 시간은 13.2 vs 13.0µs로 거의 같다. 단순히 head 수·d_k를 줄인 MHA(h=1, h=8/d_k=16)는 품질이 더 나쁨.
- 손계산 (deck 예): L 32, H 32, d_h 128, N 4096, FP16 → MHA 2 GiB, GQA-8 0.5 GiB, MQA 0.0625 GiB.
- 읽기 안내: §2.4.1의 비율 식, §3, Table 2.

## [Ainslie2023] Ainslie, Lee-Thorp, de Jong, Zemlyanskiy, Lebrón, Sanghai (2023) — GQA
- 서지: EMNLP 2023, arXiv:2305.13245. 읽은 판본: arXiv 최신판
- 접근: 원문 확인
- 문제: MQA는 품질 저하·학습 불안정, 그리고 MQA 전용 모델을 처음부터 학습해야 함 (Abstract, §1).
- 핵심: (1) **Uptraining** — MHA 체크포인트의 K, V head를 **평균 풀링**해 하나로 합친 뒤 원 사전학습 계산량의 α(=5%)만큼 추가 학습 (§2.1; 평균이 첫 head 선택·무작위 초기화보다 좋음, Figure 4). (2) **GQA-G**: Query head를 G그룹으로 나눠 그룹마다 K/V head 하나 → GQA-1 = MQA, GQA-H = MHA (§2.2). T5 실험에서 **Decoder self-attention과 cross-attention에만 적용, Encoder self-attention에는 미적용**.
- 결과 (Table 1, T5 XXL, 5% uptraining): 추론 시간/샘플 MHA-XXL 1.51s, **MQA-XXL 0.24s, GQA-8-XXL 0.28s**, MHA-Large 0.37s; 평균 점수 47.2 / 46.6 / **47.1** / 46.0 → GQA-8은 MHA-XXL에 가까운 품질 + MQA에 가까운 속도. uptraining 5%→10%는 이득 체감 (Figure 5).
- 강의 표기: KV bytes = 2·L·B·N·H_kv·d_h·bytes, H_kv = G.
- 오해: "GQA는 Query head를 줄인다" ✗ (deck 표현이 맞음). "GQA는 Llama 2가 발명" ✗.
- 읽기 안내: Figure 2 (MHA/GQA/MQA 도식), Table 1.

## [Dao2022] Dao, Fu, Ermon, Rudra, Ré (2022) — FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness
- 서지: NeurIPS 2022, arXiv:2205.14135. 읽은 판본: arXiv 최신판
- 접근: 원문 확인
- 문제: 근사 attention들은 FLOPs를 줄여도 실제 wall-clock이 빨라지지 않는 경우가 많다 — 병목은 GPU의 느린 HBM(A100: 40–80GB, 1.5–2.0TB/s)과 빠른 on-chip SRAM(192KB/SM, 약 19TB/s) 사이 **메모리 읽기/쓰기(IO)** (Abstract, §2.1, Figure 1).
- 핵심: **정확한(exact)** attention을 **타일링**(K/V 블록을 SRAM에 올리고 Q 블록을 돌며 online softmax 통계 m, ℓ로 누적)과 **역전파 시 재계산**(N×N 행렬을 저장하지 않고 다시 계산)으로, 하나의 커널에 융합 (§3.1, Algorithm 1).
- 핵심 식: Theorem 1 — O(N²d) FLOPs, **O(N) 추가 메모리**. Theorem 2 — HBM 접근: 표준 **Θ(Nd + N²)**, FlashAttention **Θ(N²d²M⁻¹)** (M = SRAM 크기, d ≤ M ≤ Nd). Proposition 3: 모든 M에서 이보다 점근적으로 나은 exact 알고리즘은 없다(하한).
- 결과: Figure 2 (GPT-2 medium, N=1024, d=64, 16 head, batch 64, A100, fwd+bwd): **GFLOPs 66.6 → 75.2 (재계산으로 오히려 증가)**, HBM R/W **40.3GB → 4.4GB**, 실행 **41.7ms → 7.3ms**. 종단 학습: BERT-large(N 512) MLPerf 1.1 기록 대비 15%, GPT-2(N 1K) 3×, LRA(1K–4K) 2.4×. Path-X(16K) 61.4%, Path-256(64K) 63.1% — 처음으로 우연 이상.
- 오해: "FlashAttention은 근사" ✗ (exact). "산술량이 선형" ✗ — FLOPs는 여전히 O(N²d)이며 더 늘 수도; 선형이 되는 것은 **추가 메모리**. deck의 "표를 저장하지 않고 정확히 계산 / 산술량 선형 아님"은 원문과 일치.
- 읽기 안내: Figure 1, Figure 2 좌측 표, Theorem 2.

## [Pope2023] Pope, Douglas, Chowdhery, Devlin, Bradbury, Levskaya, Heek, Xiao, Agrawal, Dean (2022/2023) — Efficiently Scaling Transformer Inference
- 서지: MLSys 2023, arXiv:2211.05102. 읽은 판본: v1 (9 Nov 2022)
- 접근: 원문 확인 (§2, §3.3, §4 위주)
- 문제: 500B+ 모델의 생성 추론 — 엄격한 지연, 긴 문맥에서 지연·처리량·MFU의 절충 (Abstract, §1).
- 핵심 개념 (§2): **prefill**(입력 B×L_input 토큰을 한 번의 forward로 병렬) vs **decode**(L_gen step 순차, step마다 B개 샘플 하나씩). 지연·처리량·**MFU**(관측 처리량 / 하드웨어 최대 FLOPS 기준 이론 처리량). 메모리 비용: 가중치와 **KV cache**를 HBM에 두고 forward마다 한 번씩 읽는다 — 작은 batch·짧은 길이는 가중치 로딩이, **2048+ 토큰·batch 512+에서는 KV cache 로딩이 지배**.
- 수치: 500B+급 모델, batch 512·문맥 2048에서 KV cache **3TB = 파라미터 크기의 3배** (§2). 검산: PaLM 540B(118층) multihead 변형 H=48, d_head=128, bf16 → 2·118·48·128·2B × 512 × 2048 = **3.04TB** ✓ (540B×2B = 1.08TB의 약 3배). Table 1 (64 chip, 메모리 30%를 KV에): 최대 문맥 multihead 1320/330 (batch 128/512), 기본 multiquery 660/165, **최적화 multiquery(batch 방향 분할) 43,000/10,700** → 32× 이상. PaLM 540B: int8 가중치로 64 TPU v4에서 **토큰당 29ms**, 대 batch prefill에서 **MFU 76%**, 문맥 2048.
- 요점: MQA의 메모리 이점은 head 방향으로 분할하면 사라지므로(K/V 한 벌이 모든 chip에 복제) **batch 방향 분할**이 필요 (§3.3).
- 오해: "KV cache는 작다" ✗ — 대 batch·긴 문맥에서 가중치보다 커진다.
- 읽기 안내: §2 (Inference Cost Tradeoffs), Table 1, Figure 4(분할 도식).

---

## [Shazeer2020] Shazeer (2020) — GLU Variants Improve Transformer
- 서지: arXiv:2002.05202 (학회 미게재). 읽은 판본: v1 (12 Feb 2020)
- 접근: 원문 확인
- 핵심 식 (§2, Eq. 6; T5처럼 bias 생략): FFN_GLU = (σ(xW) ⊗ xV)W2, FFN_ReGLU = (max(0, xW) ⊗ xV)W2, **FFN_GEGLU = (GELU(xW) ⊗ xV)W2**, **FFN_SwiGLU = (Swish₁(xW) ⊗ xV)W2**, Bilinear = (xW ⊗ xV)W2. 행렬이 3개라 파라미터·연산을 맞추려고 **d_ff를 2/3로**(T5 base 3072 → 2048).
- 실험: T5 base(12+12층, d 768, h 12), C4 span-filling, 524,288 step.
- 결과 (Table 1, held-out log-perplexity, 524K step): ReLU 1.677, GELU 1.679, Swish 1.683, GLU 1.663, Bilinear 1.648, ReGLU 1.645, **GEGLU 1.633, SwiGLU 1.636**. GLUE 평균: ReLU 83.80 → SwiGLU 84.36, GEGLU 84.12 (Table 2).
- 저자 한계: 왜 되는지 설명 없음 — "we attribute their success, as all else, to divine benevolence" (§4).
- 손계산: 2·d·d_ff = 3·d·d_ff′ → d_ff′ = (2/3)·d_ff; 3072 → 2048.
- 읽기 안내: Eq. 6, Table 1.

## [Su2021] Su, Lu, Pan, Murtadha, Wen, Liu (2021) — RoFormer: Enhanced Transformer with Rotary Position Embedding
- 서지: arXiv:2104.09864 (Neurocomputing 568, 2024 게재 — 일반적으로 알려진 서지). 읽은 판본: v5 (8 Nov 2023)
- 접근: 원문 확인
- 문제: 덧셈형 절대 위치 인코딩은 상대 위치를 내적에 간접적으로만 반영; 상대 위치 인코딩들은 attention 식을 바꿔 linear attention과 맞지 않음 (§1, §2).
- 핵심 식: 목표 ⟨f_q(x_m, m), f_k(x_n, n)⟩ = g(x_m, x_n, m − n) (Eq. 11). 2D 해: f(x_m, m) = (W x_m)e^{imθ} (Eq. 12–13). 일반: f_{q,k}(x_m, m) = R^d_{Θ,m} W_{q,k} x_m (Eq. 14), R은 d/2개의 2×2 회전 블록 대각 행렬 (Eq. 15), **θ_i = 10000^{−2(i−1)/d}** (sinusoidal과 같은 주파수). q_mᵀk_n = x_mᵀ W_q R^d_{Θ,n−m} W_k x_n (Eq. 16) — 상대 위치만 남는다. **덧셈이 아니라 곱셈(회전)**, **Q와 K에만 적용(V는 그대로)**. 성질: 상대 거리에 따른 장기 감쇠(§3.3, §3.4.3), linear attention과 호환.
- 결과: WMT14 EN-DE BLEU Transformer-base 27.3 → RoFormer 27.5 (Table 1); BERT 사전학습 수렴 빠름, 중국어 장문 CAIL2019-SCM에서 이득.
- 손계산: d=8 → θ = (1, 0.1, 0.01, 0.001); 위치 m의 첫 2차원은 m rad 회전.
- 읽기 안내: Eq. 11, Figure 1, Eq. 16.

---

## 현재 강의자료(build/week6.py)와 원문이 어긋나는 곳

| # | 슬라이드 제목 | 무엇이 틀렸나 / 빠졌나 | 원문 근거 |
|---|---|---|---|
| 1 | **파라미터 수를 직접 유도하기** (notes·표) | 층 3.15M, 4.19M, 44.0M, 임베딩 18.9M, 합 ≈63M은 맞다. 그러나 **"65M과의 차이 = 편향·Norm 등"은 틀림**: bias+LN은 약 0.1M(63.08M)뿐. 약 1.9M 차이는 논문으로 설명 불가. Table 3의 다른 행도 공식 대비 d에 비례하는 차이(+1.2/+2/+4M)를 보여 어휘 크기 등 미공개 요인을 시사. → "bias·LN을 넣어도 63.1M — 남는 약 2M은 논문에 설명이 없다(실제 어휘 크기 등 추정)"로 고치고, Table 3 (C)의 N=2/4/8 → 36/50/80M을 공식으로 재현하는 활동을 권장. "37k"는 EN-DE BPE 어휘임을 명시. | §5.1, Table 3; 파이썬 검산(본 노트 Vaswani 항목) |
| 2 | **원논문의 학습 조건** (표·notes) | 표 머리가 "원논문 (base / big)"인데 규제 행이 "dropout 0.1"만 — **big(EN-DE)은 P_drop=0.3**(EN-FR big만 0.1). Dropout은 sublayer 출력 외에 **(임베딩+PE) 합에도** 적용. **EN-FR 41.8은 현행판 수치**: v1–v4와 현행판 §6.1 본문은 41.0 (v2 초록은 41.2) → 각주 필요. 빠진 것: 체크포인트 평균(base 마지막 5개, big 20개), batch ≈25k+25k 토큰, 최대 출력 길이 입력+50. 나머지(β, ε, warm-up 4000, 최고 ≈7e−4, P100×8, 12h/3.5d, 27.3/28.4, beam 4, α 0.6)는 원문과 일치. | §5.1, §5.2, §5.4, §6.1, Table 2/3; arXiv v1–v7 대조 |
| 3 | **Post-LN vs Pre-LN** | 틀린 수치는 없으나 이 슬라이드의 핵심 근거 논문(Xiong 2020)의 결론이 빠짐: Post-LN은 초기화 시 마지막 층 기울기가 O(d√ln d)로 L과 무관하게 커서 **warm-up이 필수**, Pre-LN은 O(d√(ln d/L))로 작아 **warm-up 제거 가능**, 최종 성능은 비슷·수렴은 빠름(BERT에서 같은 val loss까지 약 40% 빠름). 리드 문구 "후속 모델은 Pre-LN"은 과일반화 — **BERT(2018)·GPT-1은 원형 계열(Post-LN)**, T5·ViT는 Pre-LN. Pre-LN은 Xiong 이전(Baevski & Auli 2018, Child 2019, Wang 2019)에 제안됨. | Xiong §1–§4, Theorem 1, Figure 2–3; T5 §2.1; ViT §3.1 |
| 4 | **Decoder 한 층과 출력 head** | weight tying 설명은 맞지만 원문의 다른 절반 — **임베딩 층에서 가중치에 √d_model을 곱한다** — 이 deck 어디에도 없다. 원문은 공유가 **두 임베딩 층과 pre-softmax 선형 변환 세 곳**임. | §3.4 |
| 5 | **Encoder 한 층: 잔차 · Dropout** (notes) | "원형은 각 sublayer 출력에 0.1"만 언급 → (임베딩 + PE) 합 dropout 누락(위 2와 같은 근거). | §5.4 |
| 6 | **원형과 후속 변형을 구분하기** (위치 정보 행) | "sinusoidal 덧셈 → 학습형"을 후속 설계로 제시하지만, **학습형 위치 임베딩은 원논문 자체가 Table 3 (E)에서 시험**(PPL 4.92, BLEU 25.7 vs 25.8, "nearly identical") — sinusoidal을 고른 이유는 더 긴 길이로 외삽할 *가능성*. (단 (E)행은 v2부터 존재.) RoPE는 Q·K에만 곱하는 회전임을 표에 적으면 정확. | §3.5, Table 3 (E); RoFormer Eq. 14–16 |
| 7 | **세 가지 조립 방식** | BERT 목표에 **NSP**(50/50)와 MLM 80/10/10 규칙이 빠짐; "GPT (2018~)"는 맞지만 GPT-1이 Decoder-only의 *최초*는 아님(GPT-1이 Liu et al. 2018 "Transformer decoder"를 인용). T5 목표 "span corruption"은 15%, sentinel 방식. | BERT §3.1; GPT-1 §3.1; T5 §3.1.4 |
| 8 | **ViT와 DiT** | 224/16 → 196, 768은 맞다. 보완: ViT는 [class] 토큰 + 학습형 1D 위치 + Pre-LN을 실제로 사용(“모델마다 다르다”보다 원형 사실을 먼저), "대규모 데이터" = 14M–300M장, ImageNet(1.3M)만으로는 ResNet보다 낮음. DiT는 VAE latent 32×32×4, adaLN-Zero(α=0 초기화 → 항등 블록), FID 2.27(256, cfg 1.5). | ViT §3.1, §4.3, Table 1–2; DiT §3.2, Table 4 |
| 9 | **메모리: attention 표와 KV Cache** | 식과 2 GiB 예는 맞다. 보완 가능: FlashAttention은 FLOPs가 오히려 늘어도(66.6→75.2 GFLOPs) HBM IO 감소(40.3→4.4GB)로 5.7× 빠름 — "이론 MACs ≠ 실측 지연"의 원문 근거. 추가 메모리는 O(N). Pope: 대 batch·긴 문맥에서 KV cache 3TB = 파라미터의 3배. GQA는 원 논문에서 Encoder self-attention에는 미적용. | FlashAttention Figure 2, Thm 1–2; Pope §2, Table 1; GQA §2.2 |
| 10 | **Ablation: 질문을 통제된 비교로** | 원논문 Table 3이 바로 이 표의 원형 — head 수 행은 (A)(계산량 고정: h=1 24.9, h=8 25.8, h=32 25.4), FFN 폭은 (C), dropout·label smoothing은 (D)로 숫자를 붙이면 좋다. 단 Table 3은 단일 실행·dev set·체크포인트 평균 없음. | Table 3, §6.2 |
| 11 | **원논문의 학습 조건** (notes "label smoothing … perplexity는 나빠지지만") | 원문과 일치. Table 3 (D) ε_ls=0 → PPL 4.67(더 좋음)·BLEU 25.3(더 나쁨)로 수치 근거 추가 가능. | §5.4, Table 3 (D) |
| 12 | **References** "[22] … §4 비용" | 이상 없음. 단 EN-FR BLEU를 인용할 판본(v7 권장)을 명시. | — |

### 검산 결과 이상 없음 (원문/계산 일치)
- FFN 식, d_ff 2048, N=6, d_model 512, h 8, d_h 64, dropout 0.1(base), ε_ls 0.1 — §3.1, §3.3, Table 3.
- mask = softmax 입력을 −∞ — §3.2.3. "offset by one position" ↔ teacher forcing shift — §3.1.
- 학습률 최고 6.99e−4 — Eq. 3 계산.
- MACs 표 (N=512: 0.54G / 0.27G / 1.07G; N=2048: 2.15G / 4.29G / 4.29G), KV 2 GiB, NLL 0.516·PPL 1.68, LN (1,2,3,4) 예, causal 재정규화 (0.33, 0.67), ViT 196·768 — 모두 파이썬 검산 일치.
