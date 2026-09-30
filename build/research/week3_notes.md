# Week 3 — CNN과 깊은 모델의 조건 · 연구 노트

강의일 2026-10-19 · 빌드 스크립트 `build/week3.py` · 그림 `build/assets/week3/`

## 1. 원자료 범위와 소제목 커버리지 체크리스트

| source.txt 줄 | 소제목 (`## ...`) | 반영 슬라이드 |
|---|---|---|
| 160–162 | 시간·일반화·기억·공간을 다루는 여러 길 (SVM 마진, LeNet 국소 연결·가중치 공유, "CNN → RNN이 아니다") | 오늘의 위치, Part 01 계보, 다리 놓기(오개념 1) |
| 164–167 | 분산 표현과 깊은 모델의 학습 (2006 DBN, 층별 학습, 당시 사전학습 ≠ 오늘의 사전학습) | Part 04 "2006: 깊은 모델 다시 학습하기" |
| 172–174 | AlexNet과 Word2Vec (AlexNet 부분: 데이터·GPU·CNN·학습 기법의 결합) | Part 04 AlexNet, 다섯 조건 |
| 184–186 | 잔차·정규화·병렬 시퀀스 계산 (ResNet, LayerNorm, ConvS2S; Attention만 병렬화를 시도한 게 아님) | Part 05 residual, 정규화, "잔차·정규화를 어떻게 볼까" |
| 721–723 | CNN과 깊은 모델의 조건 (장 도입: 데이터에 맞는 가정 / 깊게 쌓기 vs 잘 학습하기) | 학습 목표 |
| 725–796 | 모든 입력을 모든 뉴런에 연결해야 할까 (국소 연결, 가중치 공유, 식 y_{i,j,o}, cross-correlation 주석, 4개념 표, 위치 불변성 주의) | Part 01–02 전체 |
| 798–800 | SVM이라는 옆길에서 배울 것 (마진, 일반화, 모델 복잡도; 커널 유도는 생략) | Part 03 |
| 802–804 | 깊은 모델이 가능해진 것은 구조 하나 덕분이 아니다 (AlexNet 결합, DBN, 표현력 vs 학습 가능성) | Part 04 |
| 806–818 | Residual과 정규화의 문제의식 (y=x+F(x), Jacobian I+∂F/∂x, Post-LN 주의, LayerNorm은 스케일 도구) | Part 05 |
| 820–826 | BRIDGE QUESTION + 권장 실습 (3×3 필터를 6×6 입력에, 패턴 이동, FC 파라미터 비교) | 다리 놓기, 등변성 그림, 이번 주 과제 |
| 3811, 3813, 3817, 3835 | 오개념 1 (CNN→RNN→Transformer 교체), 2 (역전파가 업데이트), 3 (선형층 쌓기), 13 (LayerNorm이 batch 정규화) | 복습, 퀴즈, BN vs LN |
| 3592–3595 | 멘토링 3회차 "CNN·깊은 학습: 필터·수용 영역·파라미터 수" | 이번 주 과제 |
| 4094, 4097, 4103, 4104, 4105, 4091, 4096 | 참고문헌 [07][10][12][13][19][20][21] | 참고 자료 |

## 2. 검증한 사실 (연도·인물·논문·수치)

- 1959/1962 Hubel & Wiesel: 고양이 시각피질의 국소 수용 영역, simple/complex cell. (배경 설명용)
- 1980 Fukushima, *Neocognitron* (Biological Cybernetics 36): 국소 특징 추출(S-cell)과 위치 이동 허용(C-cell)을 층층이 쌓음. 역전파로 학습하지 않음.
- 1989 LeCun et al., *Backpropagation Applied to Handwritten Zip Code Recognition* (Neural Computation 1(4)): 역전파로 학습한 합성곱 신경망.
- 1998 LeCun, Bottou, Bengio, Haffner, *Gradient-Based Learning Applied to Document Recognition* (Proc. IEEE 86(11)): LeNet-5. 입력 32×32, C1 6@28×28, S2 6@14×14, C3 16@10×10, S4 16@5×5, C5 120, F6 84, 출력 10. 약 6만 개 학습 파라미터. 원자료 [10] 주석: "CNN이 1998년에 처음 발명되었다는 의미는 아니다."
- 1992 Boser, Guyon, Vapnik: 커널 트릭을 최대 마진 분류기에 적용. 1995 Cortes & Vapnik, *Support-Vector Networks* (Machine Learning 20): soft margin.
- 2006 Hinton, Osindero & Teh, *A Fast Learning Algorithm for Deep Belief Nets* (Neural Computation 18(7)): RBM을 한 층씩 탐욕적으로 학습한 뒤 전체 미세조정. 오늘날 언어 모델 사전학습과는 다른 알고리즘(원자료 [12]).
- 2009 Deng et al., *ImageNet: A Large-Scale Hierarchical Image Database* (CVPR 2009). ILSVRC(2010~2017) 분류 과제: 1000개 클래스, 학습 이미지 약 120만 장, 검증 5만, 테스트 15만. 전체 ImageNet은 약 1400만 장·2만여 개 범주.
- 2010 Nair & Hinton (RBM에서 ReLU), 2011 Glorot, Bordes & Bengio (deep sparse rectifier) — ReLU 확산.
- 2010 Glorot & Bengio: Xavier 초기화 Var(W)=2/(n_in+n_out). 2015 He et al. *Delving Deep into Rectifiers*: He 초기화 Var(W)=2/n_in (ReLU용).
- 2012 Krizhevsky, Sutskever & Hinton (NeurIPS 2012) AlexNet: 5개 conv + 3개 FC, 약 6천만 파라미터, 65만 뉴런, GTX 580 3GB GPU 2장으로 5~6일 학습. ILSVRC-2012 top-5 테스트 오류 15.3% (2위 26.2%). ReLU(4층 CNN에서 CIFAR-10 25% 학습오류 도달이 tanh보다 약 6배 빠름), Dropout(p=0.5, 앞 두 FC층), 데이터 증강(224×224 랜덤 crop·좌우 반전·PCA 색 변형), LRN, overlapping pooling, SGD momentum 0.9 + weight decay 5e-4. 입력은 논문에 224×224로 적혀 있으나 첫 층 산술이 맞으려면 227×227(널리 알려진 정정).
- 2012 Hinton et al. dropout 제안(arXiv) → 2014 Srivastava et al. JMLR.
- ILSVRC top-5 분류 우승 오류: 2010 28.2% (NEC-UIUC), 2011 25.8% (XRCE), 2012 15.3% (AlexNet), 2013 11.7% (Clarifai), 2014 6.67% (GoogLeNet; VGG 7.3%로 2위), 2015 3.57% (ResNet 앙상블).
- 2014 Simonyan & Zisserman VGG (ICLR 2015): 3×3 conv만 쌓음, 16–19층, VGG-16 약 1.38억 파라미터. 3×3 두 번 = 5×5 수용영역, 세 번 = 7×7이면서 파라미터 27C² vs 49C².
- 2014 Szegedy et al. GoogLeNet "Going Deeper with Convolutions" (CVPR 2015): 22층, Inception 모듈, 1×1 conv로 차원 축소, AlexNet보다 약 12배 적은 파라미터.
- 2015 Ioffe & Szegedy, Batch Normalization (ICML 2015).
- 2015 He, Zhang, Ren, Sun, *Deep Residual Learning for Image Recognition* (arXiv 2015-12, CVPR 2016): degradation 문제(CIFAR-10에서 56층 plain 망이 20층보다 **학습** 오류도 높음 → 과적합이 아니라 최적화 문제), identity shortcut, ImageNet 152층, CIFAR-10 1202층 실험, ILSVRC 2015 분류 3.57%.
- 2016 Ba, Kiros & Hinton, Layer Normalization: 각 샘플의 특징 축 통계로 정규화, batch 크기와 무관.
- 2017 Gehring et al. ConvS2S: 순환 없이 합성곱으로 시퀀스 변환 (Attention만이 병렬화 시도가 아님).

## 3. 핵심 수식(필수만)

1. 합성곱(cross-correlation, stride 1): y_{i,j,o} = b_o + Σ_{u,v,c} W_{u,v,c,o} · x_{i+u, j+v, c}
2. 출력 크기: O = ⌊(N + 2P − K) / S⌋ + 1. 예: 6,3,0,1 → 4; 32,5,0,1 → 28 (LeNet C1); 227,11,0,4 → 55 (AlexNet conv1); 224,3,1,1 → 224.
3. conv 파라미터: K·K·C_in·C_out + C_out. 예: 3×3, 3→64: 27·64+64 = 1,792. FC(32·32·3 → 32·32·64): 3,072 × 65,536 = 201,326,592 가중치(+65,536 bias).
4. 잔차: y = x + F(x), ∂y/∂x = I + ∂F/∂x.
5. 정규화: x̂ = (x − μ)/√(σ² + ε), y = γ·x̂ + β. 예: x=(1,2,3,4) → μ=2.5, σ²=1.25, x̂≈(−1.34, −0.45, 0.45, 1.34).
6. 시그모이드 미분 최댓값 0.25 → 10층 연쇄 시 0.25¹⁰ ≈ 9.5×10⁻⁷.

## 4. 슬라이드별 개요 (본문 39장 + 표지 + Question)

0. 표지
1. 지난 주 복습 — flow: Perceptron → XOR 한계 → MLP(비선형) → 역전파 → ReLU. 오개념 2·3 상기.
2. 오늘의 위치 — timeline: 1980 Neocognitron, 1989/98 LeNet, 1995 SVM, 2006 DBN, 2009 ImageNet, 2012 AlexNet, 2015 ResNet·BN.
3. 학습 목표 — 4개 카드(구조적 가정, 합성곱 계산, SVM 관점, 깊이의 조건).
4. Part 01 표지 — 이미지를 보는 가정
5. 이미지는 숫자 텐서 — (B, C, H, W), 그림.
6. FC로 이미지를 다루면 — stats: 150,528 입력, 1.5억 가중치, 1 위치 이동에도 다른 가중치.
7. 이미지의 두 가지 성질 — cards: 지역성, 위치가 달라도 같은 패턴, + 계층성. Hubel&Wiesel/Neocognitron.
8. Part 02 표지 — 합성곱 연산
9. 합성곱의 식 — formula y_{i,j,o}, cross-correlation 주석.
10. 필터가 미끄러지며 계산 — 6×6 입력, 3×3 세로 경계 필터, 4×4 출력 그림.
11. 출력 크기 공식 — formula O=⌊(N+2P−K)/S⌋+1 + 예제 표.
12. 파라미터 수: FC vs Local vs Conv — 막대(log) 그림.
13. 여러 채널 — 필터 한 개 = K×K×C_in, 출력 채널 수 = 필터 수. (formula/cards)
14. Pooling — 2×2 max 그림, 파라미터 0.
15. 수용 영역(Receptive field) — 층을 쌓으면 3→5→7.
16. LeNet-5 feature map 흐름 — shape 파이프라인 그림.
17. CNN의 네 가지 개념 — 원자료 표(개념/얻는 것/제약).
18. 등변성 vs 불변성 — 이동 실험 그림(권장 실습 재현).
19. PyTorch로 확인 — Conv2d/MaxPool2d shape·파라미터 수 코드.
20. Part 03 표지 — SVM이라는 옆길
21. 최대 마진 분류기 — 마진 그림, support vector.
22. 커널: 차원을 올려 선형 분리 — 1D → (x, x²) 그림.
23. SVM에서 가져올 질문 — 카드: 복잡도, 일반화, 볼록 최적화, 당시 신경망과의 비교.
24. Part 04 표지 — 깊은 모델이 가능해진 조건
25. 2006: 깊은 모델 다시 학습하기 — DBN 층별 학습 flow + 주의.
26. ImageNet — stats: 1000 클래스, 120만 장, 1400만 장.
27. AlexNet 구조 — 파이프라인 그림 + side 수치.
28. 구조 하나가 아니다 — 카드 6: 데이터, GPU, ReLU, Dropout·증강, 초기화·최적화, CNN 구조.
29. ReLU와 기울기 — 그림(미분 비교 + 0.25^L), 오개념 "ReLU면 소실이 모두 사라진다".
30. ILSVRC 오류율과 깊이 — 막대 그림 + VGG/GoogLeNet 설명.
31. Part 05 표지 — Residual과 정규화
32. 깊게 쌓으면 더 나빠진다? — degradation 개념도.
33. 잔차 연결 — formula y=x+F(x), Jacobian.
34. 잔차 블록과 기울기 경로 — block 그림 + toy gradient norm.
35. 정규화의 식 — formula, x=(1,2,3,4) 예.
36. BatchNorm vs LayerNorm — 축 그림, 오개념 13.
37. 잔차·정규화를 어떻게 볼까 — 카드: 학습 조건, Post-LN 주의, ConvS2S.
38. 다리 놓기: CNN → Attention? — compare: 고정 국소창 vs 입력 의존 참조, 오개념 1.
39. 개념 확인 — 퀴즈 5문항.
40. 이번 주 과제 — 카드.
41. 참고 자료 — 표.
42. 오늘의 정리 — summary + next_week.
43. Question (템플릿)

(발표자 노트는 `build/week3.py` 각 슬라이드 `notes=`에 2~5문장으로 작성.)

## 5. 퀴즈 Q&A

1. 입력 32×32, 필터 5×5, padding 0, stride 1이면 출력 크기는? → 28×28 (LeNet C1).
2. 3×3 conv, 입력 3채널, 출력 64채널의 파라미터 수는? → 3·3·3·64 + 64 = 1,792.
3. "CNN은 입력을 옮겨도 최종 출력이 항상 같다" O/X → X. 합성곱은 이동 등변성, 완전한 불변성은 경계·stride·pooling에 따라 성립하지 않을 수 있음.
4. 56층 plain 망이 20층보다 학습 오류가 높다. 과적합인가? → 아님. 학습 오류 자체가 높으므로 최적화 문제(degradation). Residual이 identity 경로 제공.
5. LayerNorm은 batch 전체의 같은 특징을 정규화한다 O/X → X. 각 샘플/토큰의 특징 축(마지막 축). batch 축은 BatchNorm.
6. (예비) "AlexNet의 성공은 CNN 구조 덕분" → 데이터·GPU·ReLU·dropout·증강의 결합.

## 6. 오개념 (이번 주 배정)

- [3811] CNN이 RNN으로, RNN이 Transformer로 교체되었다 → 서로 다른 데이터 구조·목표의 계보가 병행.
- [3835] LayerNorm은 Batch 전체를 정규화한다 → token별 마지막 특징 축.
- [3813][3817] 복습: 역전파는 gradient 계산, Optimizer가 업데이트 / 선형층만 쌓으면 affine.
- 본문 내 주의: CNN이 완벽한 위치 불변성 보장 X (796), ReLU면 기울기 소실이 모두 사라짐 X (704), CNN이 1998년에 발명된 게 아님 ([10]), DBN 사전학습 ≠ 현대 사전학습 ([12]), Post-LN 전체 미분을 I+∂F/∂x라 하면 안 됨 (812).

## 7. 참고 문헌 (이번 주)

[07] Cortes & Vapnik 1995 · [10] LeCun et al. 1998 · [12] Hinton, Osindero & Teh 2006 · [13] Krizhevsky, Sutskever & Hinton 2012 · [19] He et al. 2015/2016 · [20] Ba, Kiros & Hinton 2016 · [21] Gehring et al. 2017 · [42] Goodfellow et al. 2016 Ch.9 · 추가: Fukushima 1980, LeCun et al. 1989, Deng et al. 2009, Ioffe & Szegedy 2015, Simonyan & Zisserman 2014, Szegedy et al. 2014.
