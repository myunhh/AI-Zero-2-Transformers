# Week 3 논문 노트 — CNN과 깊은 학습의 조건: 공간과 깊이는? (1980–2016)

작성: 리서치 에이전트. 모든 수치는 아래 각 항목의 "읽은 판본"에서 직접 옮겼고, 계산 예시는 파이썬(`python3 -I`)으로 검산했다.
원문 PDF는 scratchpad에만 두었다(저장소에 넣지 않음).

## 주차 요약 (시간 순서 = 논문 순서, 각 논문이 앞 논문의 어떤 한계를 풀었나)

| # | 연도 | 논문 | 앞 단계의 한계 → 이 논문의 답 |
|---|---|---|---|
| 1 | 1980 | Fukushima, Neocognitron | 기존 패턴 인식 모델(퍼셉트론·cognitron)은 **위치가 바뀌면** 다른 패턴으로 인식 → S-cell(국소 특징, 같은 가중치 공유) + C-cell(주변 S-cell 반응 모으기)의 계층으로 **위치 이동에 둔감**하게. 단, 비지도 자기조직화(역전파 없음). |
| 2 | 1989 | LeCun et al., Zip code | Neocognitron·이전 Bell Labs 시스템은 특징(커널)을 손으로 설계하거나 비지도 규칙으로 학습 → **역전파로 합성곱 커널 전체를 학습**, 실제 우편번호 9,298장. |
| 3 | 1998 | LeCun, Bottou, Bengio, Haffner, LeNet-5 | 1989 망은 작은 16×16 USPS → MNIST(6만/1만) 표준 벤치마크, 7층 LeNet-5(약 6만 파라미터), 여러 분류기와 체계적 비교. |
| 4 | 1995 | Cortes & Vapnik, SVM | 1965/1992의 최적 초평면(마진)·커널 방법은 **오류 없이 분리되는 데이터**만 다룸 → **soft margin**으로 분리 불가능한 데이터까지 확장. 숫자 인식에서 특수 설계 신경망과 대등. |
| 5 | 2006 | Hinton, Osindero, Teh, DBN | 깊은 방향성 신뢰망은 추론(explaining away)이 어려워 학습 불가 → RBM을 **한 층씩 탐욕적으로** 쌓고 up-down 알고리즘으로 미세 조정. MNIST 1.25%. |
| 6 | 2010–11 | Glorot & Bengio / Nair & Hinton / Glorot, Bordes, Bengio | 왜 랜덤 초기화 + 경사하강이 깊은 망에서 실패하나? → sigmoid 포화·층별 분산 불균형 진단, **normalized(Xavier) 초기화**, **ReLU**로 사전학습 없이도 깊은 지도학습 가능. |
| 7 | 2012 | Krizhevsky, Sutskever, Hinton, AlexNet | 작은 데이터셋·CPU 한계 → ImageNet 120만 장 + GPU 2대 + ReLU + dropout + 증강. ILSVRC-2012 top-5 15.3% (2위 26.2%). |
| 8 | 2014 | Simonyan & Zisserman, VGG | AlexNet의 큰 첫 필터(11×11, stride 4) → **3×3만 깊게 쌓기**(16–19층). |
| 9 | 2015 | Ioffe & Szegedy, BatchNorm (+ Santurkar 2018 비판) | 깊은 망은 학습률·초기화에 민감 → 미니배치 통계로 층 입력 정규화, 14배 적은 step. 'internal covariate shift' 설명은 2018년에 반박됨. |
| 10 | 2015 | He et al., ResNet | BN·좋은 초기화로 수렴은 하지만 깊을수록 **훈련 오류가 커지는 degradation** → 잔차 학습 F(x)+x, 152층, ILSVRC-2015 3.57%. |
| 11 | 2016 | Ba, Kiros, Hinton, LayerNorm | BN은 배치 크기에 의존, RNN에 적용 어려움 → **샘플 하나 안의 은닉 유닛들**로 정규화, 학습·추론 동일. |

---

## [Fukushima1980] K. Fukushima (1980) — Neocognitron: A Self-organizing Neural Network Model for a Mechanism of Pattern Recognition Unaffected by Shift in Position
- 서지: Biological Cybernetics 36, 193–202 (1980). DOI 10.1007/BF00344251. 읽은 판본: https://www.cs.princeton.edu/courses/archive/spr08/cos598B/Readings/Fukushima1980.pdf (스캔본, 텍스트 레이어 있음)
- 접근: 원문 확인
- 이 논문이 풀려던 문제: 기존 모델(Rosenblatt 1962, 저자의 cognitron 1975 등)은 "위치 이동이나 모양 왜곡에 심하게 영향받는다". 같은 패턴도 다른 위치에 있으면 다른 패턴으로 취급했다(p.193 서론). 시각 피질의 Hubel–Wiesel 계층(simple → complex cell)을 본뜬 모델로 이를 해결하려 함.
- 핵심 아이디어:
  - 입력층 U0 뒤에 (S-층, C-층) 모듈을 여러 개 쌓는다(§2, Fig.1–2).
  - **S-cell**: 앞층의 국소 영역에서 특징을 뽑는다. 같은 cell-plane 안의 모든 S-cell은 "같은 공간 분포의 입력 시냅스"를 가지며 위치만 평행이동 — 오늘날의 **가중치 공유 + 특징 맵**과 같은 구조(§2, Fig.3; p.196 "all the S-cells in the same S-plane have identical set of input synapses").
  - **C-cell**: 대응 S-plane의 이웃 S-cell들로부터 고정(학습 안 함) 연결을 받아, "그중 하나라도 크게 반응하면" 반응 → 작은 이동에 둔감(p.196). 오늘날 **pooling의 조상**.
  - 층이 깊어질수록 수용 영역은 커지고 cell-plane당 세포 수(해상도)는 줄어든다. 마지막 C-층은 plane당 세포 1개(p.195).
  - 학습: **교사 없는(unsupervised) 자기조직화**. 각 S-plane에서 가장 강하게 반응한 대표 세포를 골라 그 시냅스만 강화하고, 같은 plane의 다른 세포도 같은 양만큼 강화(공유 유지)(§3, Eq.7–8). 역전파 없음.
- 핵심 식: S-cell 출력 Eq.(1) u_Sl(k_l,n) = r_l·φ[(1+Σ a_l(k_{l−1},ν,k_l)·u_{Cl−1}(k_{l−1},n+ν)) / (1 + r_l/(1+r_l)·b_l(k_l)·v_{Cl−1}(n)) − 1], φ[x]=max(x,0) (Eq.2). 강의 표기로: "공유 필터 W와 국소 입력의 내적을 억제 신호로 나눈 뒤 ReLU 비슷한 φ" — 나눗셈형(shunting) 억제가 있어 오늘날 합성곱과 똑같지는 않다.
- 실험 설정(§5): 7층 U0→US1→UC1→US2→UC2→US3→UC3. 각 층 24개 cell-plane. 세포 수 16×16(U0), 16×16×24(US1), 10×10×24(UC1), 8×8×24(US2), 6×6×24(UC2), 2×2×24(US3), 24(UC3). S-cell 연결 영역은 모든 S-층에서 5×5(US1: 5×5 = 25 시냅스, US2/US3: 5×5×24 = 600).
- 주요 결과: 숫자 "0"–"4" 다섯 패턴을 위치를 무작위로 옮겨가며 각 20번 제시 → UC3의 각 세포가 한 패턴에만 반응, **위치 이동에 전혀 영향받지 않고** 약간의 모양·크기 변화에도 둔감(p.200, Fig.6). X/Y/T/Z 실험도 성공. 10개 숫자는 "파라미터를 잘 조정하고 제시 순서를 잘 고르면" 가능했으나 작은 변화에 민감 — 저자는 cell-plane 24개가 부족하다고 봄(메모리 부족으로 더 큰 실험 못 함)(p.201).
- 저자가 밝힌 한계 / 이후 비판: 10패턴에서 파라미터 민감(p.201). Hubel–Wiesel 계층 모델 자체가 완전히 맞지 않음을 인정(p.194, p.201). 이후 LeCun 1998 §II.A: "역전파 같은 전역 지도학습 절차가 당시엔 없었다".
- 흔한 오해 바로잡기: "Neocognitron = 최초의 CNN(역전파 학습)"이 아니다 — 구조(국소 연결·공유·풀링 계층)는 선구적이지만 학습은 비지도 경쟁 학습. "완벽한 위치 불변"도 실험 조건(16×16, 5개 패턴)에서의 관찰이다.
- 슬라이드용 손계산 예시: US1 한 세포의 입력 시냅스 5×5 = 25개, US2는 5×5×24 = 600개 → 오늘날 Conv2d(24, ·, 5)의 필터 하나 가중치 수 600과 같다(검산 완료).
- 다시 그릴 만한 그림: Fig.1(Hubel–Wiesel 계층 ↔ U0→US1→UC1… 대응), Fig.2(층 간 연결: S-plane, C-plane, 타원 모양 연결 영역), Fig.6(이동·왜곡된 숫자들이 같은 출력을 내는 예).
- 읽기 안내: 초록, §2 앞 두 쪽(Fig.2–3), §5 첫 문단.

## [LeCun1989] Y. LeCun, B. Boser, J. S. Denker, D. Henderson, R. E. Howard, W. Hubbard, L. D. Jackel (1989) — Backpropagation Applied to Handwritten Zip Code Recognition
- 서지: Neural Computation 1(4), 541–551 (1989). DOI 10.1162/neco.1989.1.4.541. 읽은 판본: http://yann.lecun.com/exdb/publis/pdf/lecun-89e.pdf (스캔 이미지 PDF — 텍스트 레이어가 없어 페이지 이미지를 직접 읽음)
- 접근: 원문 확인
- 이 논문이 풀려던 문제: 과제 영역의 제약을 **신경망 구조에** 넣어 일반화를 높이는 것(초록). 이전 Bell Labs 시스템(Denker et al. 1989)은 앞 몇 층의 커널을 손으로 설계했다(§3.1, §5.1). 여기서는 정규화된 이미지를 그대로 넣고 **모든 연결을 역전파로** 학습한다.
- 핵심 아이디어:
  - **Feature map + weight sharing**(§3.2): 한 plane의 모든 유닛이 같은 가중치 집합을 공유 → 같은 특징을 다른 위치에서 탐지. "weight sharing"은 Rumelhart et al. 1986(T-C 문제)에서 왔다고 명시. 위치 정보는 일부 버려도 되지만 "대략적 위치"는 보존해야 한다(Fukushima 1980 인용).
  - **별도 pooling 층이 없다**: H1 유닛들은 입력에서 2픽셀 간격으로 놓여 "undersampled"(§3.3) — 오늘날 말로 **stride 2 합성곱**. H1→H2도 같은 2:1 서브샘플링.
  - 저자 표현: feature map이 하는 일은 "nonlinear subsampled convolution with a 5 by 5 kernel"(§3.3).
  - 편향은 공유하지 않는다(유닛마다 bias) — 오늘날 Conv2d(필터당 bias 1개)와 다름.
- 구조(§3.3, Fig.3[원문에서 Fig.2/3 캡션이 뒤바뀌어 인쇄됨]):
  - 입력 16×16(256 유닛), 회색조 −1~1.
  - H1: 12개 특징 맵 × 8×8 = 768 유닛, 5×5 커널, 연결 19,968(768×26), 자유 파라미터 1,068(768 bias + 25×12).
  - H2: 12개 맵 × 4×4 = 192 유닛, 각 유닛은 H1의 12개 맵 중 **8개**에서 5×5씩(200 입력), 연결 38,592(192×201), 파라미터 2,592(12×200 + 192).
  - H3: 30 유닛, H2와 완전 연결 — 5,790 연결. 출력 10 유닛 완전 연결 — 310.
  - 합계: 1,256 유닛, 64,660 연결, **9,760 독립 파라미터**(§3.3 끝).
- 학습 설정(§4): SUN-4/260에서 SN 시뮬레이터. 비선형성 scaled tanh, 손실 MSE, 초기화 U(−2.4/F_i, 2.4/F_i)(F_i = fan-in), 패턴마다 갱신하는 확률적 경사("on-line"), 대각 Hessian 근사를 쓴 Newton 변형. 23 pass(167,693 패턴 제시). 학습 시간 약 3일(§5.1).
- 데이터(§2.1): 버펄로 우체국 우편물의 손글씨 숫자 **9,298개** — 학습 7,291 / 테스트 2,007. 원래 약 40×60 픽셀을 종횡비 유지하며 16×16으로 선형 변환(§2.2).
- 주요 결과(§5): 23 pass 후 MSE 학습 2.5×10⁻³, 테스트 1.8×10⁻². 오분류율 **학습 0.14%(10개), 테스트 5.0%(102개)**. 테스트 1% 오류를 얻으려면 12.1% 거부. 비교: 은닉 40유닛 완전연결망(10,690 연결) — 학습 1.6%, **테스트 8.1%**, 거부 19.4%(p.547–548). DSP(AT&T DSP-32C) 구현에서 초당 10–12개 분류(정규화 숫자만이면 30개 이상)(§5.2).
- 저자가 밝힌 한계: 대부분의 오류는 분할(segmentation) 오류, 모호한 패턴, 학습셋에 없는 필체(§5). 거부 임계값을 테스트셋으로 정했다고 스스로 강조.
- 흔한 오해 바로잡기: (1) "LeNet-1989에 max pooling이 있었다" — 아니다, stride 2(undersampling)만 있다. (2) "합성곱 구조를 LeCun이 처음 만들었다" — 구조 아이디어는 Fukushima 1980, 가중치 공유는 Rumelhart et al. 1986; 이 논문의 기여는 **실제 대규모 과제에서 역전파로 커널까지 학습**한 것.
- 슬라이드용 손계산 예시(검산 완료): H1 = 12맵 × 64 = 768 유닛, 연결 768×(25+1) = 19,968, 파라미터 768 + 12×25 = 1,068. 전체 64,660 연결 vs 9,760 파라미터 → 연결 하나당 평균 약 6.6번 재사용.
- 다시 그릴 만한 그림: 원문 p.548의 구조도(256 입력 → H1 12×64 → H2 12×16 → H3 30 → 10, 각 층 링크 수 표시), p.545 학습 곡선(학습/테스트 오류 vs pass).
- 읽기 안내: §3.2–3.3(2쪽), §5 첫 세 문단.

## [LeCun1998] Y. LeCun, L. Bottou, Y. Bengio, P. Haffner (1998) — Gradient-Based Learning Applied to Document Recognition
- 서지: Proceedings of the IEEE 86(11), 2278–2324 (1998). DOI 10.1109/5.726791. 읽은 판본: http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf (텍스트 추출이 글꼴 문제로 깨져 페이지 7–12를 이미지로 읽음; 쪽 번호는 이 PDF의 쪽)
- 접근: 원문 확인 (§I–III 중심. 이후 GTN 부분은 범위 밖)
- 이 논문이 풀려던 문제: 손으로 설계한 특징 추출기 + 학습 분류기 구조 대신, 픽셀에서 바로 학습하는 시스템. 완전연결망은 (1) 파라미터가 너무 많고 (2) 이동·왜곡에 대한 불변성이 내장돼 있지 않으며 (3) 입력의 2D 국소 구조를 무시한다(§II 도입, p.5–6).
- 핵심 아이디어(§II.A, p.6–7): "local receptive fields, shared weights, spatial sub-sampling" 세 가지. 합성곱/서브샘플링 조합은 Hubel–Wiesel의 simple/complex cell에서 영감을 받았고 Fukushima Neocognitron에 구현됐지만 "역전파 같은 전역 지도학습 절차가 당시엔 없었다"(p.7).
- LeNet-5 구조(§II.B, p.7–8, Fig.2) — 입력 32×32(MNIST 숫자는 28×28 칸 중앙 20×20 안; 끝점·모서리가 최상위 특징 탐지기 수용 영역 중앙에 오도록 일부러 크게 잡음). 배경 −0.1, 전경 1.175(평균≈0, 분산≈1).

  | 층 | 내용 | 출력 | 학습 파라미터 | 연결 |
  |---|---|---|---|---|
  | C1 | 5×5 합성곱 6맵 | 6@28×28 | 156 | 122,304 |
  | S2 | 2×2 서브샘플링(4개 합 × 학습 계수 + 학습 bias → sigmoid) | 6@14×14 | 12 | 5,880 |
  | C3 | 5×5 합성곱 16맵, **S2 맵의 일부 조합에만 연결**(Table I) | 16@10×10 | 1,516 | 151,600 |
  | S4 | 2×2 서브샘플링 | 16@5×5 | 32 | 2,000 |
  | C5 | 5×5 합성곱 120맵(입력이 5×5라 결과 1×1 = 사실상 완전연결) | 120 | 48,120 | 48,120 |
  | F6 | 완전연결 | 84 | 10,164 | 10,164 |
  | 출력 | 유클리드 **RBF** 10개, y_i = Σ_j (x_j − w_ij)² (Eq.7), 파라미터는 7×12 비트맵 모양으로 손으로 정해 고정 | 10 | (고정) | 840 |

  전체: "340,908 connections, but only 60,000 trainable free parameters"(p.7). 비선형성 f(a) = A·tanh(Sa), A = 1.7159(Eq.6).
- 핵심 식: 강의 표기로 C1 파라미터 = C_out·(C_in·K·K) + C_out = 6·(1·5·5) + 6 = 156. C3는 Table I 연결 수(3맵 연결 6개, 4맵 9개, 6맵 1개)를 반영해 Σ(n·25+1) = 1,516.
- 실험 설정(§III.A–B): MNIST = NIST SD-3(인구조사국 직원) + SD-1(고등학생) 혼합, 학습 60,000 / 테스트 10,000(SD-1 5,000 + SD-3 5,000). 20×20으로 크기 정규화 후 질량중심으로 28×28 중앙 정렬. 학습 20 pass, 전역 학습률 0.0005 → 0.00001 스케줄, 대각 Hessian 근사(stochastic diagonal Levenberg–Marquardt).
- 주요 결과(§III.B, Fig.9, p.10–12): LeNet-5 **테스트 0.95%**(약 10 pass 후 안정), 학습 오류 0.35%(19 pass). 왜곡 증강(540,000장 추가)으로 **0.8%**, [dist] Boosted LeNet-4 **0.7%**(최저). 비교: 선형 12.0%, k-NN(유클리드) 5.0%, 완전연결 28×28-300-10 4.7%, 28×28-1000-10 4.5%, 1000 RBF 3.6%, SVM poly 4 **1.1%**, RS-SVM 1.0%, [dist] V-SVM poly 9 **0.8%**, Tangent Distance 1.1%, LeNet-1 1.7%, LeNet-4 1.1%. 캡션: "uncertainty in the quoted error rates is about 0.1%".
- 저자가 밝힌 한계 / 이후 비판: 학습 데이터를 늘리면 LeNet-5도 더 좋아진다(Fig.6) — 구조만으로 끝이 아님. SVM은 비슷한 정확도를 내지만 메모리·연산이 크다고 비교(§III.C).
- 흔한 오해 바로잡기: (1) LeNet-5의 S2/S4는 **max pooling이 아니라** 학습 계수·bias가 있는 평균형 서브샘플링(+sigmoid)이다. (2) 출력층은 softmax가 아니라 RBF. (3) C3는 S2의 모든 맵에 연결되지 않는다(대칭 깨기 + 연결 수 절감, p.8). (4) "LeNet-5 = 1989 망"이 아니다 — 1989 망은 16×16 입력, pooling 층 없음, 9,760 파라미터.
- 슬라이드용 손계산 예시(검산 완료): C1 6×(25+1) = 156; S2 6×2 = 12; C3 1,516; S4 16×2 = 32; C5 120×(16×25+1) = 48,120; F6 84×(120+1) = 10,164; 합 **60,000**. 연결: 122,304 + 5,880 + 151,600 + 2,000 + 48,120 + 10,164 + 840 = **340,908**. 출력 크기 32 → 28 → 14 → 10 → 5 → 1.
- 다시 그릴 만한 그림: Fig.2(LeNet-5 구조), Table I(C3 연결표 — "모든 맵을 다 잇지 않는다"), Fig.9(분류기별 MNIST 오류 막대그래프).
- 읽기 안내: §II.A(1쪽), §II.B(2쪽), Fig.9.

## [Cortes1995] C. Cortes, V. Vapnik (1995) — Support-Vector Networks
- 서지: Machine Learning 20, 273–297 (1995). DOI 10.1007/BF00994018. 읽은 판본: https://homepages.math.uic.edu/~lreyzin/papers/cortes95.pdf (스캔본; 식은 페이지 이미지로 확인)
- 접근: 원문 확인
- 이 논문이 풀려던 문제: 입력을 고차원 특징 공간으로 비선형 사상한 뒤 선형 경계를 만드는 "support-vector network"는 이전에 **오류 없이 분리되는 학습 데이터에만** 구현돼 있었다 → 분리 불가능한 데이터로 확장(초록).
- 핵심 아이디어:
  - 최적 초평면 = 두 클래스 사이 **마진이 최대**인 선형 결정 함수. 이 개념은 1965년(Vapnik 1982에 정리)에 이미 풀렸다고 논문이 직접 서술(p.275). 해는 소수의 학습 벡터(**support vectors**)만으로 결정: w₀ = Σ α_i z_i (Eq.6).
  - 커널("convolution of the dot-product")로 특징 공간을 명시적으로 계산하지 않음 — Boser, Guyon & Vapnik(1992)이 보였다고 명시(p.276). 다항식 K(u,v) = (u·v + 1)^d, RBF K(u,v) = exp(−|u−v|²/σ²)(§4, p.285).
  - **이 논문의 새 기여 = soft margin**(§3): 여유 변수 ξ_i ≥ 0을 넣어 일부 오류를 허용.
  - 일반화 한계: E[Pr(test error)] ≤ E[#support vectors] / #training vectors (Eq.5) — 차원이 명시적으로 들어 있지 않음.
- 핵심 식(원문 표기):
  - 제약 y_i(w·x_i + b) ≥ 1 − ξ_i, ξ_i ≥ 0 (Eq.22–23).
  - 최소화 ½w² + C·F(Σ ξ_i^σ) (Eq.24); σ = 1이 유일해가 있는 가장 작은 값이라 이를 택하고 "soft margin hyperplane"이라 부름(p.281). 최적 초평면의 마진은 2/|w₀|(Eq.12).
  - 강의 표기: min_{w,b} ½‖w‖² + C·Σ_i ξ_i, s.t. y_i(w·x_i + b) ≥ 1 − ξ_i. C가 크면 학습 오류를 덜 허용, 작으면 마진을 넓게.
- 실험 설정(§6.2): (a) US Postal Service 7,300 학습 / 2,000 테스트, 16×16, 전처리(중앙 정렬·deslant·가우시안 스무딩 σ=0.75). 클래스마다 분류기 10개, 최대 출력으로 판정. (b) NIST 60,000 / 10,000, 28×28(784차원), 4차 다항식만, 전처리 없음, 벤치마크 기간 2주.
- 주요 결과:
  - USPS Table 1: 사람 2.5%, CART 17%, C4.5 16%, 최선 2층 신경망 6.6%, 특수 구조 5층 신경망(LeNet1) **5.1%**.
  - USPS Table 2(다항식 차수 1–7): 오류 12.0 / 4.7 / 4.4 / 4.3 / 4.3 / 4.2 / 4.3%, support vector 수 200 / 127 / 148 / 165 / 175 / 185 / 190, 특징 공간 차원 256 → ~10¹⁶. "2차 이상 다항식이 LeNet1보다 낫다"(p.289), 차원이 커져도 성능이 거의 그대로 — 과적합 없음.
  - NIST Table 3: 4차 다항식 SVM 10개 결합 **테스트 1.1%**; 같은 벤치마크의 LeNet4와 대등(LeCun 1998 Fig.9에서도 SVM poly 4 = 1.1%, LeNet-4 = 1.1%).
  - 인용(Bottou et al. 1994, p.289–290): SVM은 기하 지식을 넣지 않았는데도 정확하며, "픽셀을 고정된 무작위 순열로 섞어도 똑같이 잘 할 것".
- 저자가 밝힌 한계: 저자 스스로 "문제에 대한 사전 지식을 반영한 커널을 만들면 더 좋아질 것"이라고 결론(p.290).
- 흔한 오해 바로잡기: "마진 최대화·커널 트릭을 1995년에 발명" — 아니다. 마진(최적 초평면)은 1960년대 Vapnik, 커널을 이용한 비선형 SVM은 1992 Boser–Guyon–Vapnik. 1995년의 기여는 **soft margin**과 체계적 실험. 또한 "SVM이 신경망을 완전히 이겼다"도 과장 — MNIST에서는 LeNet-4/5와 비슷하거나(1.1% vs 0.95%), 증강 V-SVM 0.8% ≈ [dist] LeNet-5 0.8%.
- 슬라이드용 손계산 예시: 2차원 점 x₁=(1,1) y=+1, x₂=(−1,−1) y=−1. w=(0.5,0.5), b=0이면 y_i(w·x_i+b) = 1 (둘 다 support vector), 마진 = 2/‖w‖ = 2/0.7071 = 2.828 = 두 점 사이 거리(√8)와 일치(검산 완료).
- 다시 그릴 만한 그림: Fig.2(분리 가능한 2D 예, support vector 표시, 최적 마진), Fig.5(2차 다항식 결정면), Table 2(차수가 올라가도 오류·support vector 수가 거의 그대로).
- 읽기 안내: 초록, §1 마지막 두 쪽(p.275–276), §6.2.1 Table 1–2.

## [Hinton2006] G. E. Hinton, S. Osindero, Y.-W. Teh (2006) — A Fast Learning Algorithm for Deep Belief Nets
- 서지: Neural Computation 18(7), 1527–1554 (2006). DOI 10.1162/neco.2006.18.7.1527. 읽은 판본: https://www.cs.toronto.edu/~hinton/absps/fastnc.pdf (저자 공개 preprint "To appear in Neural Computation 2006")
- 접근: 원문 확인
- 이 논문이 풀려던 문제: 은닉층이 많은 조밀한 방향성 신뢰망은 "explaining away" 때문에 은닉 활성의 사후분포 추론이 어렵고, 변분법은 근사가 나쁘고 모든 파라미터를 함께 학습해야 해서 느리다(§1).
- 핵심 아이디어:
  - "complementary prior"로 explaining away를 상쇄 → 가중치를 묶은 무한 방향성 망 = RBM(§2–3).
  - **탐욕적 층별 학습**(§4): RBM 하나를 학습 → 그 은닉 활성을 다음 RBM의 데이터로 → 반복. 층을 추가할 때마다 로그우도의 변분 하한이 개선됨을 보임.
  - 맨 위 두 층은 무방향 연합 기억(associative memory), 아래는 방향성 생성 연결(Fig.1).
  - 미세 조정은 **역전파가 아니라 "up-down" 알고리즘** = wake-sleep의 contrastive 버전(§5, 초록). 모델은 이미지와 라벨의 결합분포를 학습하는 **생성 모델**.
- 핵심 식: RBM 학습 Δw_ij ∝ ⟨v_i h_j⟩⁰ − ⟨v_i h_j⟩^∞ (Eq.3 부근; 실제로는 contrastive divergence로 근사). 라벨은 10개짜리 softmax 그룹 p_i = exp(x_i)/Σ_j exp(x_j)(Eq.10).
- 실험 설정(§6.1): 784(28×28) → 500 → 500 ↔ 2000(+10 라벨 유닛), 약 170만 가중치. 각 층 RBM 30 epoch, 층당 Matlab(3GHz Xeon)으로 몇 시간; 탐욕 학습 직후 테스트 2.49%. 이후 up-down 300 epoch(44,000장, 1만 검증) → 1.39%, 다시 6만 장 전부로 59 epoch. 총 학습 약 1주.
- 주요 결과: MNIST "permutation-invariant"(기하 지식·특수 전처리 없음) 과제에서 **테스트 1.25%**. 비교: 손으로 맞추지 않은 역전파망 최선 1.5%(800 은닉 1층 1.53%, 500-300 2층 1.51%), SVM 1.4%(Decoste & Schölkopf 2002), k-NN 3.1%. 가중치 공유·서브샘플링을 쓴 LeCun 1998은 0.95%, 탄성 변형 CNN(Simard 2003) 0.4%(§6.1, Table 1).
- 저자가 밝힌 한계: 기하 지식(가중치 공유 등)을 아직 쓰지 않음, 왜곡 데이터 미탐색, 미세 조정 알고리즘이 너무 느림(§6.1 끝).
- 흔한 오해 바로잡기: (1) 이 논문의 미세 조정은 **역전파가 아니다**(up-down). 사전학습 후 역전파 미세 조정은 같은 해 Hinton & Salakhutdinov(Science 2006, 오토인코더)와 Bengio et al.(2007) 계열에서 표준이 됨 [이 두 논문은 이번에 원문 미확인]. (2) 이 결과는 CNN보다 좋지 않았다(1.25% vs 0.95%) — 의의는 "깊은 망을 층별로 학습할 수 있다"는 것이지 절대 성능이 아니다. (3) 당시 "pre-training"은 비지도 RBM 쌓기 — LLM의 자기지도 사전학습과 다른 개념(덱의 주의 문구는 맞음).
- 슬라이드용 손계산 예시: 가중치 수 784×500 + 500×500 + (500+10)×2000 = 392,000 + 250,000 + 1,020,000 = 1,662,000 ≈ "about 1.7 million weights"(§1) (검산 완료, bias 제외).
- 다시 그릴 만한 그림: Fig.1(784–500–500–2000+10 구조, 위 두 층 무방향), Fig.2(explaining away 예: 지진/트럭/집 흔들림), Fig.8류(생성된 숫자 샘플).
- 읽기 안내: 초록, §1, §6.1.

## [Glorot2010] X. Glorot, Y. Bengio (2010) — Understanding the difficulty of training deep feedforward neural networks
- 서지: AISTATS 2010, PMLR 9:249–256. 읽은 판본: https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf
- 접근: 원문 확인
- 이 논문이 풀려던 문제: 2006년 이후 새 초기화/학습법(사전학습)으로 깊은 망이 학습되지만, "왜 표준 경사하강 + 랜덤 초기화는 깊은 망에서 그렇게 못하는가?"(초록, §1).
- 핵심 아이디어:
  - **sigmoid는 평균이 0이 아니라** 랜덤 초기화된 깊은 망에서 특히 **맨 위 은닉층을 0 근처 포화**로 몰아 학습을 늦춘다(§3.1, Fig.2). 5층 sigmoid 망은 학습 내내 포화에서 못 벗어났고, 4층은 천천히 탈출(plateau 설명).
  - tanh는 아래층부터 차례로 포화, softsign x/(1+|x|)은 덜 포화(§3.2–3.3).
  - 층마다 활성 분산과 역전파 기울기 분산을 유지하려면 n_i·Var[W] = 1(순방향)과 n_{i+1}·Var[W] = 1(역방향)이 필요 → 절충 Var[W] = 2/(n_i + n_{i+1}) (Eq.12).
  - 표준 초기화 U[−1/√n, 1/√n](Eq.1)은 n·Var[W] = 1/3(Eq.15) → 역전파 기울기 분산이 층을 내려갈수록 감소.
- 핵심 식: **normalized initialization** W ~ U[−√6/√(n_j + n_{j+1}), +√6/√(n_j + n_{j+1})] (Eq.16) — 오늘날 "Xavier/Glorot 초기화". 강의 표기: Var[w] = 2/(d_in + d_out).
- 실험 설정: Shapeset-3×2(합성 도형, 32×32), MNIST, CIFAR-10, Small-ImageNet. 5개 은닉층, 층당 1,000 유닛, 미니배치 10, 학습률 검증으로 선택(§2).
- 주요 결과(Table 1, 5층 테스트 오류 %): MNIST — Sigmoid 2.21, Tanh 1.76, Tanh N(normalized init) 1.64, Softsign 1.64. CIFAR-10 — Sigmoid 57.28, Tanh 55.9, Tanh N 52.92. Shapeset — Sigmoid 82.61, Tanh 27.15, Tanh N 15.60.
- 저자가 밝힌 한계: 분석은 선형 영역 가정(Bradley 2009 따름); 비지도 사전학습과의 차이는 여전히 남는다(Fig.11).
- 흔한 오해 바로잡기: "기울기 소실 = sigmoid 도함수 ≤ 0.25 때문" 하나만이 아니다. 이 논문은 **초기화 스케일(층별 분산 곱)과 sigmoid 평균이 만드는 포화**를 원인으로 지목한다. 또 이 논문은 ReLU를 다루지 않는다(ReLU는 다음 두 논문).
- 슬라이드용 손계산 예시: n_in = n_out = 1000이면 normalized init 범위 ±√6/√2000 = ±0.0548, Var = 0.0548²/3 = 0.001 = 2/2000 (검산 완료). 표준 init ±1/√1000 = ±0.0316 → n·Var = 1000·(0.0316²/3) = 0.333 → 5층 지나면 기울기 분산 약 (1/3)^5 ≈ 0.004배.
- 다시 그릴 만한 그림: Fig.2(sigmoid 망의 층별 활성 평균 — 맨 위 층이 0으로 붙음), Fig.6–7(표준 vs normalized init의 층별 활성/기울기 히스토그램).
- 읽기 안내: 초록, §3.1, §4.2 Eq.12–16.

## [Nair2010] V. Nair, G. E. Hinton (2010) — Rectified Linear Units Improve Restricted Boltzmann Machines
- 서지: ICML 2010, 807–814. 읽은 판본: https://www.cs.toronto.edu/~hinton/absps/reluICML.pdf
- 접근: 원문 확인 (짧게)
- 문제·아이디어: RBM의 이진 은닉 유닛을 무한히 복제(bias를 점점 음수로)한 "stepped sigmoid"는 noisy rectified linear unit max(0, x + N(0, σ(x)))로 효율적으로 근사된다(§2). 결정론적 버전 y = max(0, x)를 역전파에서도 사용. ReLU는 여러 층을 지나도 **상대 강도 정보(intensity equivariance)**를 보존(초록, §4).
- 결과: Jittered-Cluttered NORB 물체 인식, Labeled Faces in the Wild 얼굴 검증에서 이진 유닛보다 좋은 특징(§5–6).
- 흔한 오해: ReLU를 "AlexNet이 처음 썼다"가 아니다 — AlexNet도 Nair & Hinton을 인용. 또 그 이전 Jarrett et al. 2009도 rectification을 썼다(AlexNet §3.1이 언급).

## [Glorot2011] X. Glorot, A. Bordes, Y. Bengio (2011) — Deep Sparse Rectifier Neural Networks
- 서지: AISTATS 2011, PMLR 15:315–323. 읽은 판본: https://proceedings.mlr.press/v15/glorot11a/glorot11a.pdf
- 접근: 원문 확인 (짧게)
- 문제·아이디어: 0에서 미분 불가능하고 0 아래로 딱딱하게 포화하는 rectifier max(0, x)가 tanh보다 같거나 좋다. 실제 0을 내는 **희소 표현**(초록, §2.2–3). 기울기가 일부 경로로만 흘러도 학습에 문제 없다는 가설(§3.1).
- 결과(Table 1, 3층 테스트 오류): 비지도 사전학습 **없이** — Rectifier MNIST 1.43%, CIFAR-10 50.86%, NORB 16.40% vs Tanh 1.57% / 52.62% / 19.29%. 사전학습 있을 때 Rectifier 1.20%. 결론: 큰 라벨 데이터의 순수 지도학습에서는 deep rectifier net이 **사전학습 없이도 최고 성능**에 도달(초록).
- 덱 연결: "이후 ReLU·초기화·데이터·GPU가 갖춰지며 층별 사전학습 없이도 학습 가능" 문장의 직접 근거.
- 슬라이드용 손계산: sigmoid′ 최댓값 0.25(at 0) → 10층 곱 0.25¹⁰ = 9.54×10⁻⁷ (검산 완료). ReLU′는 양수 구간 1.

## [Krizhevsky2012] A. Krizhevsky, I. Sutskever, G. E. Hinton (2012) — ImageNet Classification with Deep Convolutional Neural Networks
- 서지: NeurIPS 25 (2012), 1097–1105. 읽은 판본: https://papers.nips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf
- 접근: 원문 확인
- 이 논문이 풀려던 문제: 이전 이미지 데이터셋은 수만 장(NORB, Caltech, CIFAR) 수준. 수백만 장 ImageNet의 1,000 클래스를 배우려면 큰 용량 + 강한 사전 가정(CNN)이 필요하고, 이를 현실적인 시간에 학습할 GPU 구현이 필요(§1).
- 핵심 아이디어 / 기법(§3–4):
  - **ReLU**(§3.1): 4층 CNN이 CIFAR-10에서 학습 오류 25%에 tanh보다 **6배 빨리** 도달(Fig.1).
  - **GPU 2대 병렬**(§3.2): GTX 580 3GB 메모리 한계 때문에 커널을 반씩 나누고 특정 층에서만 통신. 단일 GPU 절반 망 대비 top-1/top-5 1.7%/1.2% 개선.
  - Local Response Normalization(§3.3, top-1/top-5 1.4%/1.2% 개선), 겹치는 pooling z=3, s=2(§3.4, 0.4%/0.3% 개선).
  - 데이터 증강(§4.1): 256×256에서 무작위 224×224 자르기 + 좌우 반전(학습셋 2048배), RGB PCA 색 변형(top-1 1% 이상 개선). 테스트는 10개 patch 평균.
  - **Dropout** p = 0.5(§4.2): 처음 두 완전연결층에. 없으면 심한 과적합, 수렴 iteration은 약 2배.
- 구조(§3.5, Fig.2): 합성곱 5 + 완전연결 3 + 1000-way softmax. conv1 96@11×11×3 stride 4, conv2 256@5×5×48, conv3 384@3×3×256, conv4 384@3×3×192, conv5 256@3×3×192, FC 4096–4096–1000. **6,000만 파라미터, 65만 뉴런**(초록).
- 학습 설정(§5): SGD 배치 128, momentum 0.9, weight decay 0.0005("단순한 규제가 아니라 학습 오류도 줄인다"). 초기화 N(0, 0.01²), 일부 층 bias 1. 학습률 0.01에서 검증 오류가 멈추면 1/10(3번). 약 90 epoch, **GTX 580 3GB 2대로 5–6일**.
- 주요 결과:
  - ILSVRC-2010 테스트(Table 1): CNN top-1 37.5% / top-5 **17.0%** vs 대회 최고 47.1% / 28.2%(sparse coding), 이후 최고 45.7% / 25.7%(SIFT+FV).
  - ILSVRC-2012(Table 2): 1 CNN 검증 top-5 18.2%, 5 CNN 16.4%(테스트 16.4%), ImageNet Fall 2011(1,500만 장, 22K 클래스)로 사전학습한 CNN 2개 + 5 CNN = **7 CNN, 테스트 15.3%**. 2위 26.2%(SIFT+FV 여러 분류기 평균).
  - 깊이: 중간 합성곱 층 하나를 빼면 top-1이 약 2% 나빠짐(§7).
- 저자가 밝힌 한계: 망 크기는 GPU 메모리와 학습 시간이 제한, "더 빠른 GPU와 더 큰 데이터만 기다려도 좋아질 것"(§1). 비지도 사전학습은 쓰지 않았음(§7).
- 흔한 오해 바로잡기: (1) **15.3%는 단일 모델·120만 장만의 결과가 아니다** — 7개 앙상블이고 그중 2개는 ImageNet Fall 2011 전체(1,500만 장)로 사전학습. 외부 데이터 없이 공식 결과는 16.4%(Russakovsky Table 8: SuperVision 16.42%, †외부 데이터 15.32%). (2) ReLU·dropout·GPU CNN 모두 이 논문이 최초는 아님(Nair & Hinton 2010, Hinton et al. 2012 dropout, Cireşan et al. GPU CNN) — 조합과 규모가 핵심. (3) 원문 conv1 서술(224 입력, 11×11, stride 4)로는 출력이 정수가 안 된다: (224−11)/4+1 = 54.25. 실제 구현은 227 입력(→55)으로 알려져 있음 — 슬라이드에서 shape 계산 예시로 쓸 때 주의.
- 슬라이드용 손계산 예시(검산 완료): conv1 파라미터 96×(11·11·3)+96 = 34,944. 출력 크기 O = ⌊(227 − 11)/4⌋ + 1 = 55. 증강 배수 (256−224)² × 2 = 2,048.
- 다시 그릴 만한 그림: Fig.1(ReLU vs tanh 학습 곡선, 6배), Fig.2(두 GPU로 나뉜 구조), Fig.3(conv1이 학습한 96개 필터: 위 GPU는 색 무관, 아래 GPU는 색 특이), Table 2.
- 읽기 안내: 초록, §3.1, §4(과적합 줄이기), Table 2.

## [Simonyan2014] K. Simonyan, A. Zisserman (2014/ICLR 2015) — Very Deep Convolutional Networks for Large-Scale Image Recognition
- 서지: ICLR 2015, arXiv:1409.1556 (v6). 읽은 판본: https://arxiv.org/pdf/1409.1556
- 접근: 원문 확인 (짧게)
- 핵심 논증(§2.3): 3×3 두 층(사이 pooling 없음)의 유효 수용 영역은 5×5, 세 층은 7×7. 7×7 한 층 대신 3×3 세 층을 쓰면 (1) 비선형(ReLU) 3번 → 결정 함수가 더 변별적, (2) 입출력 C채널일 때 3·(3²C²) = **27C²** vs 7²C² = **49C²**, "81% more". 7×7 필터에 3×3 분해를 강제하는 규제로 볼 수 있음.
- 구조: 11층(A)~19층(E), 파라미터 133M~144M(Table 2).
- 결과(Table 7): ILSVRC-2014 제출(7개 앙상블) top-5 테스트 **7.3%(2위)**; 제출 후 2개 앙상블 6.8%, 단일 7.0%. 같은 표에서 GoogLeNet 7개 6.7%.
- 흔한 오해: 27C² vs 49C²는 bias 제외. 3×3 쌓기는 VGG가 처음 생각한 것이 아니라 VGG가 체계적으로 보인 것(Ciresan 2011 등 작은 필터 사용 언급).
- 손계산(검산 완료): C=64면 27·64² = 110,592 vs 49·64² = 200,704. 49/27 − 1 = 0.815.

## [Ioffe2015] S. Ioffe, C. Szegedy (2015) — Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift
- 서지: ICML 2015, PMLR 37:448–456; arXiv:1502.03167 (v3). 읽은 판본: https://arxiv.org/pdf/1502.03167
- 접근: 원문 확인
- 이 논문이 풀려던 문제: 앞 층 파라미터가 바뀌면 각 층 입력 분포가 계속 바뀌어 낮은 학습률·조심스러운 초기화가 필요하고 포화 비선형 학습이 어렵다. 저자는 이를 **internal covariate shift(ICS)** — "학습 중 파라미터 변화로 인한 망 활성 분포의 변화" — 라 정의하고 줄이려 함(§2).
- 핵심 아이디어(§3, Algorithm 1): 각 스칼라 특징을 미니배치 평균·분산으로 독립 정규화(완전 whitening은 비쌈) → 학습되는 γ, β로 스케일·이동(γ = √Var, β = E이면 원래 활성 복원 가능 → 항등 변환도 표현 가능). 추론 때는 이동 평균한 **모집단 통계**로 고정된 선형 변환(Alg.2).
  - 합성곱 층(§3.2): 같은 특징 맵의 값은 위치와 무관하게 같은 방식으로 정규화 → 미니배치 m개 × 공간 p×q 전체(유효 배치 m·pq)로 통계, γ·β는 **특징 맵(채널)당 한 쌍**.
  - 규제 효과(§3.4): 샘플이 배치의 다른 샘플과 함께 보이므로 결정론적 출력이 아님 → Dropout을 줄이거나 없앨 수 있음.
- 핵심 식(Alg.1): μ_B = (1/m)Σx_i, σ_B² = (1/m)Σ(x_i − μ_B)², x̂_i = (x_i − μ_B)/√(σ_B² + ε), y_i = γx̂_i + β. 강의 표기: 입력 (B, C, H, W)에서 채널 c마다 (B, H, W) 축으로 평균·분산.
- 실험 설정(§4.2): Inception(GoogLeNet 변형) + BN, 학습률 5배(BN-x5)·30배(BN-x30), Dropout 제거, LRN 제거 등.
- 주요 결과(Fig.3): Inception이 72.2% 정확도에 31.0M step, BN-Baseline 13.3M, **BN-x5 2.1M(14배 적음)**, BN-x30 2.7M에 최고 74.8%. BN-x5-Sigmoid 69.8%(원래 Inception은 sigmoid로 chance 수준). 앙상블 6개: ImageNet top-5 검증 **4.9%, 테스트 4.82%**, "사람 평가자 정확도 초과"(초록, §4.2.3; 사람 5.1%는 Russakovsky Table 9).
- 저자가 밝힌 한계: 배치 통계에 의존 — 작은 배치·RNN 적용은 미래 과제(§5).
- 이후 비판 — **Santurkar, Tsipras, Ilyas, Madry (2018) "How Does Batch Normalization Help Optimization?"**, NeurIPS 2018, arXiv:1805.11604 (v5) 원문 확인:
  - BN의 성공은 층 입력 분포 안정(ICS 감소)과 "거의 관련이 없다"(초록). BN 뒤에 시간에 따라 변하는 평균·분산 잡음을 일부러 넣어 분포를 불안정하게 만든 "noisy BatchNorm"도 표준 BN과 거의 같은 성능(Fig.2).
  - 어떤 의미에서 BN은 ICS를 줄이지도 않을 수 있다(§2.2).
  - 대신 BN은 손실과 기울기의 Lipschitz성(β-smoothness)을 개선해 **최적화 지형을 매끄럽게** 만든다 → 기울기가 더 예측 가능, 큰 학습률 가능(§3, Fig.4; 정리 4.1, 4.4). ℓp 정규화 등 다른 방법도 비슷한 효과(§3.3).
- 흔한 오해 바로잡기: "BN은 internal covariate shift를 줄여서 효과가 있다"는 원 논문의 **가설**이지 확립된 설명이 아니다. CNN의 BN은 "같은 특징의 배치 전체"가 아니라 "같은 채널의 배치 × 공간 위치 전체"로 정규화.
- 슬라이드용 손계산 예시(검산 완료): x = (1, 2, 3, 4) → μ = 2.5, σ² = 1.25, σ = 1.118, x̂ = (−1.342, −0.447, 0.447, 1.342). 유효 배치: B=32, 특징 맵 14×14면 채널당 32·196 = 6,272개 값으로 통계.
- 다시 그릴 만한 그림: Algorithm 1(식 네 줄), Fig.2(Inception vs BN 변형의 검증 정확도 곡선), Santurkar Fig.2(noisy BN도 잘 학습)·Fig.4(손실 지형 매끄러움).
- 읽기 안내: §2 첫 문단(ICS 정의), §3 Alg.1, §3.2 합성곱 문단; Santurkar 초록 + Fig.2.

## [He2016] K. He, X. Zhang, S. Ren, J. Sun (2015/CVPR 2016) — Deep Residual Learning for Image Recognition
- 서지: CVPR 2016, 770–778; arXiv:1512.03385 (v1, 2015-12-10). 읽은 판본: https://arxiv.org/pdf/1512.03385
- 접근: 원문 확인
- 이 논문이 풀려던 문제: 기울기 소실/폭발은 normalized 초기화와 중간 정규화(BN)로 "대체로 해결"돼 수십 층 망이 수렴은 한다(§1). 그런데 깊이를 늘리면 정확도가 포화 후 급격히 나빠지는 **degradation**이 나타나고, 이는 과적합이 아니라 **훈련 오류**가 커지는 현상이다(Fig.1: CIFAR-10 20층 vs 56층 plain). 얕은 망 + 항등 층으로 만든 해가 존재하므로 깊은 망의 훈련 오류가 더 높을 이유가 없는데 solver가 못 찾는다(§1).
- 핵심 아이디어(§3.1–3.2): 원하는 사상 H(x)를 직접 배우지 않고 F(x) := H(x) − x를 배우게 함. 항등이 최적이면 "잔차를 0으로 미는 것이 비선형 층 여러 개로 항등을 맞추는 것보다 쉽다"(§1). 지름길은 파라미터·연산 추가 없음. 차원이 다르면 projection W_s.
- 핵심 식: y = F(x, {W_i}) + x (Eq.1), y = F(x, {W_i}) + W_s x (Eq.2). 2층 블록 F = W₂σ(W₁x), **덧셈 뒤에 두 번째 ReLU**(§3.2: "second nonlinearity after the addition"). 강의 표기: h_{l+1} = ReLU(h_l + F(h_l)) — 원 논문 블록은 덧셈 후 ReLU가 있어 순수 항등 경로가 아니다.
- 실험 설정: ImageNet 2012(128만 학습, 5만 검증, 10만 테스트), plain/ResNet 18·34층, bottleneck 50/101/152층. 합성곱 직후 BN, He 초기화, SGD 배치 256, 학습률 0.1, dropout 없음(§3.4). CIFAR-10 20–1202층.
- 주요 결과:
  - Table 2(ImageNet 검증 top-1, 10-crop): plain 18층 27.94%, **plain 34층 28.54%(더 나쁨)**; ResNet 18층 27.88%, **ResNet 34층 25.03%**.
  - Table 4(단일 모델 검증): ResNet-152 top-1 19.38%, **top-5 4.49%** — 이전 모든 앙상블보다 좋음.
  - Table 5(앙상블, 테스트 서버 top-5): VGG 7.32, GoogLeNet 6.66, PReLU-net 4.94, BN-inception 4.82, **ResNet 3.57** — "서로 다른 깊이 6개 모델 앙상블(제출 시 152층은 2개뿐)", ILSVRC 2015 1위(§4.1).
  - CIFAR-10(Table 6): ResNet-20 8.75%, ResNet-110 6.43%, **ResNet-1202 7.93%**(110보다 나쁨 — 저자는 과적합으로 봄).
  - 152층도 VGG-16/19보다 FLOPs가 적다(11.3B vs 15.3/19.6B).
- 저자가 밝힌 한계 / 해석: plain 망의 최적화 어려움은 "**기울기 소실 때문은 아닐 것**" — BN으로 순방향 신호의 분산이 0이 아니고 역방향 기울기 노름도 건강함을 확인했다(§4.1). 대신 "지수적으로 낮은 수렴 속도"를 추측하고 원인 규명은 미래 과제로 남김. 1202층은 과적합.
- 흔한 오해 바로잡기: (1) "ResNet은 기울기 소실을 해결했다"는 원 논문의 주장이 아니다 — 원 논문은 degradation을 기울기 소실과 **구별**한다. ∂y/∂x = I + ∂F/∂x로 기울기가 직접 흐른다는 분석은 후속 논문 He et al. 2016 "Identity Mappings in Deep Residual Networks"(ECCV, pre-activation 블록)의 논리다 [이번에 원문 미확인]. (2) 지름길 아이디어 자체는 Highway Networks(2015) 등 선행 연구가 있음(§2에서 언급). (3) 3.57%는 152층 단일 모델이 아니라 6개 앙상블.
- 슬라이드용 손계산 예시: 스칼라 toy — y = x + F(x), F(x) = w·x에서 ∂y/∂x = 1 + w; w = 0이면 항등, 20개 블록 연쇄 미분 (1+w)^20: w = 0.01이면 1.22, plain(y = w′x, w′ = 0.9)이면 0.9^20 = 0.12 (검산 완료; 덧셈 뒤 ReLU·BN 무시한 단순화임을 명시).
- 다시 그릴 만한 그림: Fig.1(CIFAR-10 20 vs 56층 plain, 훈련·테스트 오류), Fig.2(잔차 블록: weight layer–ReLU–weight layer + 항등 지름길 → ReLU), Fig.4(ImageNet plain-18/34 vs ResNet-18/34 곡선), Fig.5(bottleneck).
- 읽기 안내: §1(1쪽), §3.1, Fig.1·Fig.4·Table 2.

## [Ba2016] J. L. Ba, J. R. Kiros, G. E. Hinton (2016) — Layer Normalization
- 서지: arXiv:1607.06450 (v1, 2016-07-21; NIPS 2016 Deep Learning Symposium). 읽은 판본: https://arxiv.org/pdf/1607.06450
- 접근: 원문 확인
- 이 논문이 풀려던 문제: BN은 미니배치 크기에 의존하고 RNN에 적용하기 어렵다(초록, §2: 기대값을 미니배치로 추정 → 배치 크기 제약).
- 핵심 아이디어(§3): 한 층의 **모든 은닉 유닛**의 합산 입력으로 평균·분산을 계산 — 같은 층의 유닛들은 같은 정규화 항을 공유하고, **훈련 사례마다** 정규화 항이 다르다. 배치 크기 1(online)도 가능, 학습·추론 계산이 동일. RNN에서는 time step마다 별도 통계(§3.1).
- 핵심 식(Eq.3): μ^l = (1/H)Σ_{i=1}^H a_i^l, σ^l = √((1/H)Σ_{i=1}^H (a_i^l − μ^l)²), H = 층의 은닉 유닛 수. 정규화 뒤 유닛별 gain g와 bias b를 **비선형 전에** 적용(초록; RNN 식 Eq.4: h^t = f[(g/σ^t)⊙(a^t − μ^t) + b]). 원문 Eq.3에는 ε이 없음(구현에서는 보통 추가). 강의 표기: 입력 (B, N, d)에서 각 (b, n)마다 d개 값으로 μ, σ.
- 실험: 주로 RNN — 이미지-문장 순위, QA(attentive reader), skip-thought, DRAW, 손글씨 시퀀스 생성, permutation-invariant MNIST(§6).
- 비교(Table 1, 불변성): BN — 가중치 행렬 re-scaling 불변, re-centering 불변 아님, 데이터셋 re-scaling·re-centering 불변, **단일 사례 re-scaling 불변 아님**. LN — 가중치 행렬 re-scaling·re-centering 불변, 단일 가중치 벡터 re-scaling 불변 아님, 데이터셋 re-scaling 불변, re-centering 아님, **단일 사례 re-scaling 불변**.
- 저자가 밝힌 한계(§6.7): 합성곱 망에서는 LN이 정규화 없음보다 빠르지만 **BN이 더 좋았다** — 완전연결층과 달리 CNN에서는 유닛들의 기여가 비슷하다는 가정이 깨짐(이미지 가장자리 수용 영역 유닛은 거의 켜지지 않음).
- 흔한 오해 바로잡기: LN 논문 자체는 Transformer와 무관(2017년 이전). "LN은 CNN에서도 BN보다 낫다"가 아니다 — 저자들이 CNN에선 BN이 낫다고 보고.
- 슬라이드용 손계산 예시(검산 완료): 토큰 하나 h = (1, 2, 3, 4)(d=4) → μ = 2.5, σ = 1.118, 정규화 (−1.342, −0.447, 0.447, 1.342). 배치 안 다른 토큰의 값과 무관.
- 다시 그릴 만한 그림: 원문에는 축 그림이 없음 — Table 1(불변성 표)을 단순화하거나, (B, d) 행렬에서 BN = 열 방향, LN = 행 방향으로 새로 그린다.
- 읽기 안내: 초록, §3(반 쪽), §6.7(CNN 한계 한 문단).

## [ILSVRC] ILSVRC top-5 수치 검증 — Russakovsky et al. (2015) "ImageNet Large Scale Visual Recognition Challenge" + 각 원 논문
- 서지: IJCV 115(3), 211–252 (2015), arXiv:1409.0575. 읽은 판본: https://arxiv.org/pdf/1409.0575. image-net.org 결과 페이지는 이번 환경에서 접속 실패(연결 리셋) → 2015년은 He et al. Table 5로 확인.
- 접근: 원문 확인

| 연도 | 덱 값 | 원문 값 | 우승팀 · 방법 | 출처 | 판정 |
|---|---|---|---|---|---|
| 2010 | 28.2 | **28.2** | NEC — SIFT·LBP + 비선형 코딩 + SVM | Russakovsky Table 5, §5.1 | 맞음 |
| 2011 | 25.8 | **25.8** | XRCE — Fisher vector 등 + 선형 SVM | Russakovsky Table 5 | 맞음 |
| 2012 | 15.3 | 16.4 (외부 데이터 없음, 16.42) / **15.3 (ImageNet Fall 2011 외부 데이터 사용, 15.32)** | SuperVision(AlexNet) 앙상블; 2위 ISI 26.2(26.17) | Russakovsky Table 5 캡션, Table 8; Krizhevsky Table 2 | 숫자는 맞지만 **외부 데이터·7개 앙상블** 단서 필요 |
| 2013 | 11.7 | **11.7 (11.74)**; 외부 데이터 사용 시 11.2 | Clarifai(Zeiler) — 여러 CNN 평균 | Russakovsky Table 6, Table 8 | 맞음 |
| 2014 | 6.67 | **6.66** (논문 본문 반올림 6.7) | GoogLeNet; 2위 VGG 7.32 | Russakovsky Table 8; He et al. Table 5 | **틀림(6.67 → 6.66 또는 6.7)** |
| 2015 | 3.57 | **3.57** | MSRA ResNet — 깊이가 다른 6개 앙상블(152층은 2개) | He et al. §4.1, Table 5 | 맞음 |

- 추가 맥락: Russakovsky Table 9 — 사람 전문 주석자 A1의 추정 분류 오류 **5.1%**(A2는 12.0%). BN 앙상블(4.82%, 2015년 2월)·PReLU-net(4.94%)이 이미 사람 A1 추정치보다 낮았고, ResNet 3.57%는 대회 우승 기록. 2012→2014 감소: "16.4% → 6.7%, 2.4배"(Russakovsky §6 결론, 외부 데이터 없는 기준).
- 깊이: AlexNet 8층(합성곱 5 + FC 3, Krizhevsky §3.5), VGG 16–19층(Simonyan §2), ResNet 152층(He Table 1). GoogLeNet 22층은 Szegedy et al. 2015 원문을 이번에 받지 않아 **[원문 미확인]** — 널리 알려진 값으로 표시.

---

## 현재 강의자료(build/week3.py)와 원문이 어긋나는 곳

| # | 슬라이드 제목 | 무엇이 틀렸나 / 부족한가 | 원문 근거 |
|---|---|---|---|
| 1 | "2012: AlexNet" (lead·표·노트) | "top-5 15.3%" 옆에 "데이터 ImageNet 약 120만 장"만 적혀 있어 **15.3%가 120만 장 단일 모델 결과**처럼 읽힘. 실제로는 7개 CNN 앙상블이며 그중 2개는 ImageNet Fall 2011(1,500만 장, 22K 클래스)로 사전학습. 외부 데이터 없는 공식 결과는 **16.4%**, 단일 CNN은 검증 18.2%. → "15.3% (7개 앙상블, 외부 데이터 사용; 외부 데이터 없이 16.4%)"로. "구조 하나 덕분이 아니다" 메시지를 오히려 강화하는 사실. | Krizhevsky et al. §6, Table 2; Russakovsky Table 5 캡션·Table 8 |
| 2 | "2006: 깊은 망을 다시 학습시키려는 시도" (flow 마지막 "전체 미세 조정: 역전파로 함께", 노트) | Hinton·Osindero·Teh(2006)의 미세 조정은 **역전파가 아니라 up-down 알고리즘**(contrastive wake-sleep), 모델은 이미지·라벨 결합분포의 **생성 모델**. "사전학습 → 역전파 미세 조정"은 같은 해 Hinton & Salakhutdinov(2006)·Bengio et al.(2007) 계열. → "전체 미세 조정(up-down 알고리즘)"으로 바꾸거나 "이후 연구에서는 역전파로 미세 조정"이라고 분리. 결과 수치도 추가 가능: MNIST 1.25%(SVM 1.4%, 일반 역전파망 1.5%; 단 LeNet-5 0.95%보다는 나쁨). | Hinton et al. 2006 초록, §5, §6.1 |
| 3 | "잔차 연결: y = x + F(x)" (노트·bullet "항등 경로로 기울기가 직접 흐른다") + quiz/오해 표 | He et al.(2015)은 degradation이 **기울기 소실 때문이 아닐 것**이라고 명시(BN으로 순·역방향 신호가 건강함을 확인)하고, 동기를 "잔차를 0으로 미는 것이 항등을 맞추는 것보다 쉽다"로 설명. ∂y/∂x = I + ∂F/∂x 기울기 논리는 후속 논문(He et al. 2016 Identity Mappings)의 것. 또 원 블록은 **덧셈 뒤 ReLU**가 있어 순수 항등 경로가 아니다. → "원 논문의 설명: 항등을 배우기 쉬워진다 / 기울기 흐름 해석은 2016 후속 연구"로 출처를 나누기. | He et al. 2015 §1, §3.1–3.2, §4.1 "unlikely to be caused by vanishing gradients" |
| 4 | "오류는 줄고, 층은 깊어졌다" (bullet·노트·ilsvrc.png) | 2014 GoogLeNet **6.67% → 6.66%**(또는 6.7%). 2015 ResNet 3.57%는 152층 단일이 아니라 **6개 앙상블**(152층은 2개) — "152층"은 대표 깊이로만. 2012도 외부 데이터 단서(위 1번). 그림 assets/week3/ilsvrc.png에 6.67이 들어갔다면 함께 수정. | Russakovsky Table 8; He et al. §4.1·Table 5 |
| 5 | "SVM: 가장 넓은 여백을 가진 경계" | "Cortes & Vapnik(1995)" 아래에 마진 최대화를 그 논문의 발명처럼 제시. 원문이 직접 밝히듯 최적 초평면(마진)은 1965년(Vapnik 1982), 커널 비선형 SVM은 Boser·Guyon·Vapnik(1992); **1995년의 기여는 soft margin**(오류 허용, ξ_i와 C). → bullet에 "1995의 새 점: soft margin — 분리 불가능한 데이터 허용" 추가. 결과도 추가 가능: USPS 4차 다항식 4.3% vs LeNet1 5.1%, NIST 1.1% ≈ LeNet-4 1.1%. | Cortes & Vapnik p.275–276, §3 Eq.22–24, Table 1–3 |
| 6 | "LeNet: 합성곱 신경망의 원형" (표 S2 "2×2 pooling", "출력 10개 숫자 클래스", 노트) | LeNet-5의 S2/S4는 max pooling이 아니라 **학습 계수·bias가 있는 평균형 서브샘플링 + sigmoid**(층당 12, 32 파라미터). C3는 S2 맵 일부 조합에만 연결(Table I). 출력은 softmax가 아닌 **유클리드 RBF**. 1989 망에는 pooling 층이 없고 stride 2(undersampling)만 있음 — "Pooling" 슬라이드의 "대안: stride 2 합성곱"과 연결하면 좋은 역사적 사례. 파라미터 총 6만, 연결 340,908. | LeCun 1998 §II.B p.7–8, Table I, Eq.7; LeCun 1989 §3.3 |
| 7 | "BatchNorm vs LayerNorm" (표 "같은 특징, 배치 전체") | CNN에서 BN은 채널마다 **배치 × 공간 위치(B, H, W)** 전체로 통계를 내고 γ·β도 채널당 한 쌍. "배치 전체"만 쓰면 오해. 또 BN 원 논문의 'internal covariate shift' 설명은 Santurkar et al.(2018)이 반박(noisy BN도 잘 학습, 실제 효과는 손실 지형 평활화) — 노트에 한 줄 추가 권장. LN 논문은 CNN에선 BN이 더 낫다고 보고(§6.7)해 "주 사용처 CNN/RNN·Transformer" 구분을 뒷받침. | Ioffe & Szegedy §3.2; Santurkar et al. 초록·Fig.2; Ba et al. §6.7 |
| 8 | "기울기가 곱해지며 사라진다" (노트) | 단순화 자체는 괜찮지만, Glorot & Bengio(2010)의 진단은 "sigmoid′ ≤ 0.25"보다 **초기화 스케일(층별 분산 곱, 표준 init에서 n·Var[W] = 1/3)과 sigmoid 평균이 만드는 맨 위 층 포화**. "초기화/최적화" 카드 근거로 Xavier 초기화 Var[W] = 2/(n_in + n_out)를 한 줄 추가 가능. 참고로 LeNet(1989/1998)은 sigmoid가 아니라 scaled tanh를 썼다. | Glorot & Bengio §3.1, Eq.12–16; LeCun 1989 §4; LeCun 1998 Eq.6 |
| 9 | "2012: AlexNet" bullet "ReLU: 학습이 몇 배 빨라짐" | 원문 수치는 구체적: 4층 CNN이 CIFAR-10 학습 오류 25%에 **6배** 빨리 도달(Fig.1). "몇 배" → "6배(CIFAR-10, Fig.1)"로 구체화 가능. ReLU는 AlexNet이 처음이 아님(Nair & Hinton 2010, Jarrett 2009). | Krizhevsky §3.1, Fig.1 |
| 10 | "LeNet" 표 "S4 → C5 → F6: pooling → 완전 연결" | C5는 원문에서 **합성곱 층**(5×5×16 → 1×1, 입력이 커지면 1×1보다 커짐)이라 명시. 완전연결과 결과는 같지만 "합성곱"으로 표기하는 것이 원문에 맞음. | LeCun 1998 p.8 C5 문단 |
| 11 | "깊게 쌓으면 더 나빠진다?" | 원문과 일치(Fig.1: CIFAR-10 20 vs 56층 plain, 훈련·테스트 모두 56층이 높음). ImageNet에서도 plain-34 top-1 28.54% > plain-18 27.94%(Table 2) — 실제 데이터 근거로 추가 가능. 노트 "그림은 논문 경향을 단순화한 개념도" 유지. | He et al. Fig.1, Table 2 |
| 12 | 참고문헌 슬라이드 | Fukushima(1980), LeCun et al.(1989), Glorot & Bengio(2010), Simonyan & Zisserman(2014), Santurkar et al.(2018), Russakovsky et al.(2015)이 본문에서 쓰이는데 목록에 없음. | — |

### 원문에서 확인된, 덱에 그대로 써도 되는 수치 (검산 완료)
- 32×32×3 → 32×32×64 완전연결 3,072 × 65,536 = 201,326,592; 국소 65,536 × 27 = 1,769,472; 공유 64×27 = 1,728 (+64 = 1,792).
- 출력 크기: 6/3/0/1 → 4, 32/5/0/1 → 28, 32/3/1/1 → 32, 32/3/1/2 → 16, 64/5/2/2 → 32. LeNet C1 6×25+6 = 156. 16→32 3×3: 32·16·9+32 = 4,640.
- VGG 27C² vs 49C²(81% 더 많음). 0.25¹⁰ = 9.54×10⁻⁷. (1,2,3,4) 정규화 → (−1.342, −0.447, 0.447, 1.342).
- AlexNet: 6,000만 파라미터, 65만 뉴런, 합성곱 5 + FC 3, GTX 580 3GB 2대 5–6일, 약 90 epoch, dropout 0.5, momentum 0.9, weight decay 0.0005, 2위 26.2%.
- ILSVRC 28.2 / 25.8 / 15.3(외부 데이터) / 11.7 / 6.66 / 3.57; VGG 7.3(7.32).

### 원문 미확인 목록
- Szegedy et al. 2015 (GoogLeNet) — 22층이라는 깊이는 원문 미확인(널리 알려진 값).
- He et al. 2016 "Identity Mappings in Deep Residual Networks" — 기울기 흐름 해석의 출처로만 언급.
- Hinton & Salakhutdinov 2006 (Science), Bengio et al. 2007 — 사전학습 후 역전파 미세 조정의 출처로만 언급.
- image-net.org 공식 결과 페이지 — 접속 실패, Russakovsky 2015와 He et al. Table 5로 대체 검증.
