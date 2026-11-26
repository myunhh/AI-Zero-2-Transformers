"""Week 3 — CNN과 깊은 학습의 조건: 공간과 깊이는? (논문 중심 구성)

근거: build/research/papers/week3.md (검증된 논문 노트). 숫자·식은 그 노트에 출처와 함께 있는 것만 쓴다.
새 그림: build/paper_figs_w3.py → assets/week3/paper_*.png / 기존 그림: build/week3_figs.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deckkit  # noqa: E402
deckkit.use_theme("clean")  # Apple 디자인 원칙 테마 — import * 보다 먼저
from deckkit import *  # noqa

A = lambda p: os.path.join(HERE, "assets", p)
OUT = os.path.join(HERE, "..", "lectures", "week03_cnn_and_deep_learning.pptx")

d = Deck(3, "CNN과 깊은 학습의 조건", date="2026-10-19", theme="clean")

# ============================================================ 도입
d.question("공간 구조를 어떻게 쓰고,\n깊은 모델은 어떻게 학습시키나?",
           "1980–2016 · 논문으로 읽는 CNN · SVM · AlexNet · BatchNorm · ResNet · LayerNorm",
           notes="지난주 MLP는 이론적으로 강력하지만 두 가지 벽에 부딪힌다: 입력이 크면 파라미터가 폭발하고, 층이 깊으면 학습이 잘 안 된다. "
                 "오늘은 이 두 벽을 넘은 과정을 논문 순서대로 읽는다. 공간: Fukushima(1980) → LeCun(1989) → LeNet-5(1998). "
                 "옆길: SVM(1995). 깊이: DBN(2006) → Glorot & Bengio(2010) · ReLU(2010–11) → AlexNet(2012) → VGG(2014) → BatchNorm(2015) → ResNet(2015) → LayerNorm(2016). "
                 "출처: build/research/papers/week3.md 주차 요약 표.")

d.bridge(["Perceptron의 한계(XOR)", "비선형 은닉층 + **역전파** = MLP", "분류 출력: Softmax + Cross-entropy"],
         ["입력이 **이미지**(수만 픽셀)면 모든 입력을 모든 뉴런에 연결 → 파라미터 폭발",
          "층을 **깊게** 쌓으면 학습이 잘 안 된다"],
         ["**공간 구조를 어떻게 쓰고,**", "**깊은 모델은 어떻게 학습시키나?**"])

d.roadmap(["합성곱의 탄생 — Fukushima 1980 · LeCun 1989", "LeNet-5 (1998)", "옆길: SVM (1995)",
           "깊이의 벽 — DBN 2006 · Glorot 2010 · ReLU", "AlexNet (2012) · VGG (2014)", "BatchNorm (2015)",
           "ResNet (2015)", "LayerNorm (2016)과 정리"],
          ["합성곱의 **출력 크기**와 **파라미터 수**를 계산한다",
           "LeNet-5 구조를 원문대로 설명한다 (서브샘플링 · RBF)",
           "SVM 1995의 새 기여(**soft margin**)를 말한다",
           "AlexNet **15.3%**가 무엇의 결과인지 정확히 말한다",
           "ResNet 원 논문의 논리와 후속 해석을 구분한다",
           "BatchNorm과 **LayerNorm**의 정규화 축을 구분한다"])

d.paper_map([
    ("1980", "Fukushima — Neocognitron", "S-cell(공유 국소 특징) + C-cell(모으기)", "위치가 바뀌면 다른 패턴으로 인식"),
    ("1989", "LeCun et al. — 우편번호 인식", "**역전파로 합성곱 커널**까지 학습", "커널을 손이나 비지도 규칙으로 정함"),
    ("1995", "Cortes & Vapnik — Support-Vector Networks", "**soft margin** + 커널", "오류 없이 분리되는 데이터만 다룸"),
    ("1998", "LeCun et al. — LeNet-5", "표준 CNN 구조, MNIST 0.95%", "작은 16×16 데이터, 체계적 비교 부족"),
    ("2006", "Hinton, Osindero, Teh — DBN", "층별 탐욕 학습", "깊은 망은 추론·학습이 어렵다"),
    ("2010", "Glorot & Bengio", "포화·분산 진단, normalized 초기화", "왜 랜덤 초기화가 깊은 망에서 실패?"),
    ("2010–11", "Nair & Hinton / Glorot et al. — ReLU", "사전학습 없이 깊은 지도학습", "sigmoid·tanh의 포화"),
    ("2012", "Krizhevsky et al. — AlexNet", "데이터 + GPU + ReLU + dropout", "작은 데이터셋, CPU 한계"),
    ("2014", "Simonyan & Zisserman — VGG", "3×3만 깊게 쌓기", "큰 첫 필터(11×11)"),
    ("2015", "Ioffe & Szegedy — BatchNorm", "미니배치 통계로 정규화", "학습률·초기화에 민감"),
    ("2015", "He et al. — ResNet", "잔차 학습 F(x) + x", "깊을수록 **훈련** 오류가 커짐"),
    ("2016", "Ba, Kiros, Hinton — LayerNorm", "샘플 하나 안에서 정규화", "BN은 배치 크기에 의존"),
], notes="이번 주 논문을 시간 순서로 본다(SVM 1995는 LeNet-5 1998보다 먼저 나왔지만, 강의에서는 CNN 계보를 먼저 끝내고 옆길로 본다). "
         "각 논문이 바로 앞의 어떤 한계를 풀었는지 한 줄씩 짚는다. 보조 논문: Santurkar et al.(2018, BN 재해석), Russakovsky et al.(2015, ILSVRC 수치). "
         "출처: week3.md 주차 요약 표.")

d.glossary([["특징 맵 (feature map)", "필터 하나를 모든 위치에 적용한 결과 격자", "‘세로 경계’ 지도 한 장"],
            ["가중치 공유", "모든 위치가 같은 필터(같은 가중치)를 씀", "같은 돋보기로 전체를 훑기"],
            ["stride · padding", "필터가 움직이는 간격 · 가장자리에 덧댄 0", "보폭 · 여백"],
            ["서브샘플링 · pooling", "영역을 요약해 해상도를 줄임 (평균, 최댓값)", "지도 축소"],
            ["마진 · 서포트 벡터", "경계와 가장 가까운 점 사이 거리 · 그 점들", "도로 폭 · 도로변 집"],
            ["사전학습 (2006)", "층을 하나씩 비지도로 먼저 학습", "LLM 사전학습과는 다른 개념"],
            ["앙상블", "여러 모델의 예측을 평균", "여러 심사위원 점수 평균"],
            ["잔차 · 정규화", "입력을 출력에 더하는 지름길 · 평균 0, 분산 1로 맞춤", "원본 + 수정본 · 표준점수"]])

# ============================================================ Part 1
d.part(1, "합성곱의 탄생 (1980 · 1989)", "모든 픽셀을 모든 뉴런에 연결해야 할까?",
       notes="Part 1: 이미지 텐서와 합성곱의 기본 계산을, 합성곱 구조를 처음 제안한 Neocognitron(1980)과 역전파로 커널을 학습한 LeCun et al.(1989)에 걸어 본다.")

s = d.slide("MLP로 이미지를 다루면", lead="작은 32×32 컬러 이미지에서도 층 하나에 2억 개 파라미터", stage="문제",
            notes="[도구] 이미지 한 칸(픽셀)은 밝기 숫자. 컬러는 R·G·B 3채널이라 (3, H, W), 여러 장이면 (B, C, H, W). "
                  "입력 32×32×3을 같은 크기의 64채널 특징 맵(32×32×64)으로 바꾸는 층을 생각하자. 모든 입력(3,072)을 모든 출력(65,536)에 연결하면 "
                  "3,072 × 65,536 = 201,326,592개. 국소 3×3 영역만 연결하면 65,536 × 27 = 1,769,472개, 거기에 가중치를 공유하면 64 × 27 = 1,728개(편향 포함 1,792). "
                  "LeCun 1998 §II 도입도 같은 진단: 완전연결망은 (1) 파라미터가 너무 많고 (2) 이동·왜곡 불변성이 없으며 (3) 2D 국소 구조를 무시한다. "
                  "출처: week3.md '원문에서 확인된 수치'(검산 완료); LeCun et al. 1998 §II p.5–6.")
L, R = s.cols(0.58)
s.image(A("week3/params_fc_conv.png"), L)
s.bullets(["이미지 = 숫자 텐서 `(B, C, H, W)`", ("컬러 32×32 → 3 × 32 × 32 = 3,072개 입력", 1),
           "출력 32×32×64, **모든 연결**: 3,072 × 65,536", ("= ==201,326,592== 개", 1),
           "국소 연결만 (3×3×3 = 27): 1,769,472개", "국소 + **가중치 공유**: **1,728**개 (+편향 64)",
           "펼치는 순간 **이웃 관계**도 사라진다"], R, size=17)

d.paper("Fukushima (1980)",
        "Neocognitron: A Self-organizing Neural Network Model for a Mechanism of Pattern Recognition Unaffected by Shift in Position",
        "Biological Cybernetics 36, 193–202",
        "퍼셉트론·cognitron 같은 기존 모델은 패턴이 **다른 위치**에 있으면 다른 패턴으로 취급했다.",
        "시각 피질의 simple/complex cell 계층을 본떠, **S-cell**(국소 특징, 같은 plane은 같은 가중치)과 **C-cell**(이웃 반응 모으기)을 번갈아 쌓는다.",
        "초록, §2 앞 두 쪽(Fig.2–3), §5 첫 문단",
        url="princeton.edu · Fukushima1980.pdf",
        lead="Neocognitron — 위치가 바뀌어도 영향받지 않는 패턴 인식 모델",
        result="숫자 0–4를 위치를 옮겨 제시해도 같은 출력. 학습은 **비지도** 자기조직화(역전파 없음).",
        notes="Fukushima (1980) Neocognitron. 문제: 기존 모델은 '위치 이동이나 모양 왜곡에 심하게 영향받는다'(p.193 서론). "
              "아이디어: U0 뒤에 (S-층, C-층) 모듈을 쌓는다(§2, Fig.1–2). 같은 S-plane의 모든 S-cell은 'identical set of input synapses'(p.196) — 오늘의 가중치 공유·특징 맵. "
              "C-cell은 고정 연결로 이웃 S-cell 중 하나라도 크게 반응하면 반응 → pooling의 조상. 학습은 교사 없는 경쟁 학습(§3, Eq.7–8). "
              "결과: p.200 Fig.6. 출처: Fukushima 1980, 초록·§2·§3·§5.")

s = d.slide("Neocognitron: S-cell과 C-cell", lead="공유된 5×5 특징 탐지(S)와 고정된 모으기(C)를 번갈아 — 깊어질수록 넓게, 해상도는 낮게",
            stage="아이디어",
            notes="원문 §5의 실험 망: U0 → US1 → UC1 → US2 → UC2 → US3 → UC3, 각 층 24개 cell-plane. 세포 수 16×16(U0), 16×16×24(US1), 10×10×24(UC1), "
                  "8×8×24(US2), 6×6×24(UC2), 2×2×24(US3), 24(UC3). S-cell 연결 영역은 모든 S-층에서 5×5: US1 한 세포는 5×5 = 25 시냅스, US2·US3은 5×5×24 = 600 — "
                  "오늘날 Conv2d(24, ·, 5) 필터 하나의 가중치 수 600과 같다(검산 완료). "
                  "S-cell 식(Eq.1)은 공유 가중치와 국소 입력의 내적을 억제 신호로 나눈 뒤 φ[x] = max(x, 0)(Eq.2) — 나눗셈형 억제가 있어 오늘날 합성곱과 똑같지는 않다. "
                  "결과: 0–4 다섯 패턴을 위치를 바꿔 각 20번 제시 → UC3의 각 세포가 한 패턴에만 반응, 위치 이동에 영향받지 않음(p.200, Fig.6). "
                  "10개 숫자는 파라미터에 민감했고 저자는 cell-plane 24개가 부족하다고 봄(p.201). 그림: 원문 §5·Fig.2 기반 재구성.")
top, bot = s.area.top(3.15, gap=0.25)
s.image(A("week3/paper_neocognitron.png"), top)
L, R = bot.cols(0.5, gap=0.4)
s.bullets(["**S-cell**: 같은 plane = 같은 시냅스 → **가중치 공유**", ("US1 한 세포 5×5 = 25, US2는 5×5×24 = **600**", 1),
           "**C-cell**: 이웃 S-cell 반응을 모음 → **pooling의 조상**"], L, size=16)
s.bullets(["결과: 숫자 0–4를 **위치를 옮겨도** 같은 출력 (p.200)", "한계: 10개 숫자에서는 파라미터에 민감",
           ("==주의== 학습은 비지도 — **역전파가 아니다**", 1)], R, size=16)

d.paper("LeCun et al. (1989)", "Backpropagation Applied to Handwritten Zip Code Recognition",
        "Neural Computation 1(4), 541–551",
        "이전 시스템은 앞 몇 층의 커널을 **손으로 설계**했다. 과제의 제약을 구조에 넣되, 특징은 데이터에서 배우고 싶다.",
        "feature map + **weight sharing** 구조에, 정규화된 이미지를 그대로 넣고 **모든 연결을 역전파로** 학습한다.",
        "§3.2–3.3 (2쪽), §5 첫 세 문단",
        url="yann.lecun.com/exdb/publis/pdf/lecun-89e.pdf",
        result="실제 우편번호 9,298장에서 테스트 오류 5.0% (완전연결망 8.1%).",
        notes="LeCun et al. (1989). 문제: Denker et al. 1989 등 이전 Bell Labs 시스템은 앞 층 커널을 손으로 설계(§3.1, §5.1). "
              "아이디어(§3.2): 한 plane의 모든 유닛이 같은 가중치 집합 공유 → 같은 특징을 다른 위치에서 탐지. weight sharing은 Rumelhart et al. 1986에서 왔다고 명시, "
              "Fukushima 1980을 인용. 저자 표현: 'nonlinear subsampled convolution with a 5 by 5 kernel'(§3.3). "
              "이 논문의 기여는 구조 발명보다 '실제 대규모 과제에서 역전파로 커널까지 학습'한 것. 출처: LeCun et al. 1989 초록, §3, §5.")

s = d.slide("합성곱: 필터가 미끄러지며 내적한다", lead="출력 한 칸 = 필터와 입력 조각의 내적 + 편향 — 같은 가중치를 모든 위치에서 재사용",
            stage="계산",
            notes="입력 6×6은 왼쪽이 밝고(10) 오른쪽이 어둡다(0). 필터 [[1,0,−1]]×3줄은 '왼쪽 밝고 오른쪽 어두운' 세로 경계에 반응. "
                  "주황 창: (10·1 + 10·0 + 0·(−1)) × 3줄 = 30, 경계 없는 곳은 0. 식: y[i, j] = Σ_u Σ_v W[u, v] · x[i+u, j+v] + b — 1주차 내적을 위치마다 반복. "
                  "딥러닝의 'convolution' 구현은 대부분 필터를 뒤집지 않는 cross-correlation이다(필터가 학습되므로 실용적 차이 없음). "
                  "역사: Fukushima의 S-cell이 이 '공유 필터'의 원형이고, LeCun 1989가 필터 값을 역전파로 학습했다. 1989 망의 편향은 공유하지 않고 유닛마다 따로 있었다(§3.3).")
top, bot = s.area.top(2.85, gap=0.25)
s.image(A("week3/conv_sliding.png"), top)
L, R = bot.cols(0.52, gap=0.4)
s.formula("y[i, j] = Σ_u Σ_v W[u, v] · x[i+u, j+v] + b", Box(L.x, L.y, L.w, 0.95), size=19)
s.bullets(["주황 창: (10·1 + 10·0 + 0·(−1)) × 3줄 = **30**", "W는 사람이 아니라 **역전파로 학습** (LeCun 1989)",
           ("딥러닝의 ‘convolution’ = 뒤집지 않는 cross-correlation", 1)], R, size=16)

s = d.slide("출력 크기와 파라미터 수", lead="O = ⌊(N − K + 2P) / S⌋ + 1 · params = C_out · C_in · K · K + C_out",
            stage="계산",
            notes="N: 입력 한 변, K: 필터 크기, P: padding, S: stride. 예: 6/3/0/1 → 4, 32/5/0/1 → 28(LeNet-5 C1), 32/3/1/1 → 32(크기 유지), 32/3/1/2 → 16. "
                  "필터 하나는 입력의 모든 채널을 본다: 컬러 입력(C_in=3)에 3×3 필터면 3×3×3 = 27. 필터 64개면 64 × 27 = 1,728, 편향 64를 더해 1,792. "
                  "입력 이미지 크기와 무관 — 앞 장의 완전 연결 2억 개와 비교. LeNet-5 C1: 6 × 25 + 6 = 156. "
                  "출처: week3.md 검산 목록(출력 크기, 1,792, 156).")
s.takeaway("파라미터 수가 이미지 크기와 무관하다 — 201,326,592 → 1,792")
L, R = s.cols(0.55, gap=0.45)
s.formula("O = ⌊ (N − K + 2P) / S ⌋ + 1", Box(L.x, L.y, L.w, 0.95), size=22)
s.formula("params = C_out · C_in · K · K + C_out", Box(R.x, R.y, R.w, 0.95), size=20)
L = Box(L.x, L.y + 1.2, L.w, L.h - 1.2)
R = Box(R.x, R.y + 1.2, R.w, R.h - 1.2)
s.table(["N", "K", "P", "S", "출력 O"],
        [["6", "3", "0", "1", "**4**"], ["32", "5", "0", "1", "**28** (LeNet-5 C1)"], ["32", "3", "1", "1", "**32** (크기 유지)"],
         ["32", "3", "1", "2", "**16** (절반)"]], L, size=15, align="ccccc", widths=[0.8, 0.8, 0.8, 0.8, 2.4])
s.table(["항목", "값"], [["입력", "(B, 3, 32, 32)"], ["필터", "64개 × (3 × 3 × 3)"], ["가중치", "64 × 27 = 1,728"],
                        ["편향", "64"], ["합계", "**1,792**"], ["출력 (P = 1)", "(B, 64, 32, 32)"]], R, size=15, align="lc")
s.textbox(["**N** 입력 한 변 · **K** 필터 크기 · **P** padding · **S** stride", "‘same’ padding: P = (K − 1) / 2 → 크기 유지"],
          Box(L.x, L.y + 2.2, L.w, 1.0), size=15, color=GRAY, gap=0.2)

s = d.slide("1989 망: 연결 6만 개, 파라미터 1만 개", lead="16×16 입력 → H1 → H2 → H3 → 10 — pooling 층 없이 stride 2로 해상도를 줄였다",
            stage="계산",
            notes="원문 §3.3 구조. 입력 16×16(256), 회색조 −1~1. H1: 12개 특징 맵 × 8×8 = 768 유닛, 5×5 커널, 연결 768 × (25+1) = 19,968, "
                  "자유 파라미터 768(유닛별 bias) + 12 × 25 = 1,068. H2: 12맵 × 4×4 = 192 유닛, 각 유닛은 H1의 12개 맵 중 8개에서 5×5씩(200 입력), "
                  "연결 192 × 201 = 38,592, 파라미터 12 × 200 + 192 = 2,592. H3 30 유닛 완전 연결 5,790, 출력 10 유닛 310. "
                  "합계 1,256 유닛, 64,660 연결, 9,760 독립 파라미터 → 연결 하나당 평균 약 6.6번 재사용(검산 완료). "
                  "H1 유닛은 입력에서 2픽셀 간격(undersampled, §3.3) = 오늘날 stride 2 합성곱. 별도 pooling 층은 없다 — 'LeNet-1989에 max pooling이 있었다'는 오해. "
                  "그림: 원문 §3.3 · p.548 구조도 기반 재구성(원문에서 Fig.2/3 캡션이 뒤바뀌어 인쇄됨).")
top, bot = s.area.top(3.3, gap=0.2)
s.image(A("week3/paper_lecun89_arch.png"), top)
L, R = bot.cols(0.5, gap=0.4)
s.bullets(["H1 연결: 768 × (25 + 1) = **19,968**", "H1 파라미터: 768 (유닛별 bias) + 12 × 25 = **1,068**",
           ("편향은 공유하지 않음 — 오늘 Conv2d와 다름", 1)], L, size=16)
s.bullets(["전체 64,660 연결 vs **9,760** 파라미터", ("가중치 하나를 평균 약 **6.6번** 재사용", 1),
           "해상도 축소 = **stride 2** (별도 pooling 없음)"], R, size=16)

s = d.slide("1989 결과: 구조에 넣은 제약이 일반화를 돕는다", lead="같은 데이터에서 완전 연결망보다 테스트 오류가 낮다 — 학습 오류가 아니라 일반화의 차이",
            stage="결과",
            notes="데이터(§2.1): 버펄로 우체국 우편물 손글씨 숫자 9,298개 — 학습 7,291 / 테스트 2,007, 약 40×60 픽셀을 16×16으로 선형 변환. "
                  "학습(§4): SUN-4/260, scaled tanh, MSE 손실, 패턴마다 갱신하는 확률적 경사, 대각 Hessian 근사 Newton 변형, 23 pass(약 3일). "
                  "결과(§5): 오분류율 학습 0.14%(10개), 테스트 5.0%(102개). 테스트 1% 오류를 얻으려면 12.1% 거부. "
                  "비교: 은닉 40유닛 완전연결망(10,690 연결) — 학습 1.6%, 테스트 8.1%, 거부 19.4%(p.547–548). DSP 구현으로 초당 10–12개 분류(§5.2). "
                  "한계: 대부분의 오류는 분할 오류·모호한 패턴·학습셋에 없는 필체. 거부 임계값을 테스트셋으로 정했다고 저자 스스로 강조. 출처: LeCun et al. 1989 §2, §4, §5.")
s.table(["망", "연결 수", "학습 오류", "테스트 오류", "1% 오류를 위한 거부율"],
        [["합성곱 망 (공유 가중치)", "64,660", "0.14%", "**5.0%**", "12.1%"],
         ["완전 연결망 (은닉 40)", "10,690", "1.6%", "8.1%", "19.4%"]],
        Box(s.area.x, s.area.y, s.area.w, 1.5), size=16, align="lcccc", widths=[3.2, 1.6, 1.6, 1.8, 2.8], highlight=(0,))
s.cards([{"head": "실험 설정 (§2, §4)", "tone": "plain", "bullets": True,
          "body": ["실제 우편번호 **9,298장** (학습 7,291 / 테스트 2,007)", "16×16 입력, scaled tanh, MSE 손실",
                   "패턴마다 갱신, 23 pass — SUN-4로 약 **3일**"]},
         {"head": "읽을 거리", "tone": "plain", "bullets": True,
          "body": ["연결은 더 많은데 파라미터는 적다 → **일반화**", "저자가 밝힌 오류 원인: 분할 오류 · 모호한 글씨",
                   "남은 질문: 표준 벤치마크에서 다른 방법과 비교하면?"]}],
        Box(s.area.x, s.area.y + 1.85, s.area.w, s.area.h - 1.85), cols=2, body_size=16, head_size=17)

s = d.slide("등변성 ≠ 불변성", lead="입력이 옮겨지면 특징도 옮겨진다(등변). 최종 출력이 ‘완전히 같다’(불변)는 별개의 주장", stage="검증",
            notes="같은 필터를 모든 위치에 쓰므로 입력 패턴을 한 칸 옮기면 특징 맵의 반응도 한 칸 옮겨진다 — translation equivariance. "
                  "여기에 전체 max 같은 요약을 붙이면 이 예시에서는 위치와 무관한 값(불변)이 된다. "
                  "Fukushima(1980)의 '위치 이동에 영향받지 않음'도 16×16 입력, 5개 패턴이라는 실험 조건에서의 관찰이다(p.200). "
                  "LeCun 1989 §3.2도 위치 정보는 일부 버려도 되지만 '대략적 위치'는 보존해야 한다고 썼다. "
                  "CNN이 자동으로 완벽한 위치 불변성을 보장하는 것은 아니다 — 경계·padding·stride·pooling에 따라 달라진다. 그림은 직접 계산한 toy 예.")
L, R = s.cols(0.56)
s.image(A("week3/equivariance.png"), L)
s.bullets(["**등변성**: 입력 이동 → 특징도 같이 이동", ("같은 필터를 모든 위치에 쓰기 때문", 1),
           "**불변성**: 입력이 이동해도 출력이 같음", ("전체 max 같은 요약을 붙이면 (이 예시에서)", 1),
           "Fukushima의 ‘이동 불변’도 **실험 조건**에서의 관찰", "==주의== 완벽한 불변성은 **보장되지 않는다**",
           ("경계 · padding · stride · pooling에 따라 다름", 1)], R, size=16)

# ============================================================ Part 2
d.part(2, "LeNet-5 (1998)", "16×16 우편번호에서 표준 벤치마크로 — 구조를 어떻게 다듬었나?",
       notes="Part 2: LeCun, Bottou, Bengio, Haffner (1998). 1989 망을 MNIST 표준 벤치마크와 7층 LeNet-5로 정리하고, 여러 분류기와 체계적으로 비교했다.")

d.paper("LeCun et al. (1998)", "Gradient-Based Learning Applied to Document Recognition",
        "Proceedings of the IEEE 86(11), 2278–2324",
        "완전 연결망은 파라미터가 너무 많고, 이동·왜곡 불변성이 내장돼 있지 않으며, 입력의 **2D 국소 구조**를 무시한다.",
        "**local receptive fields · shared weights · spatial sub-sampling** 세 가지를 갖춘 7층 LeNet-5 — 픽셀에서 바로 학습.",
        "§II.A (1쪽), §II.B (2쪽), Fig.9",
        url="yann.lecun.com/exdb/publis/pdf/lecun-98.pdf",
        result="MNIST(학습 6만 / 테스트 1만) 테스트 오류 **0.95%**.",
        notes="LeCun et al. (1998). 문제(§II 도입, p.5–6): 손으로 설계한 특징 추출기 + 학습 분류기 대신 픽셀에서 바로 학습. 완전연결망의 세 가지 문제. "
              "아이디어(§II.A, p.6–7): 세 가지 구조. 합성곱/서브샘플링 조합은 Hubel–Wiesel의 simple/complex cell에서 영감을 받았고 Neocognitron에 구현됐지만 "
              "'역전파 같은 전역 지도학습 절차가 당시엔 없었다'(p.7). 이번 강의 범위는 §I–III(뒤의 GTN 부분 제외). 출처: LeCun et al. 1998 §II.")

s = d.slide("LeNet-5 구조 — 원문 그대로", lead="합성곱(C) → 서브샘플링(S) 두 번 → C5 → F6 → RBF 출력. 학습 파라미터 6만, 연결 34만",
            stage="아이디어",
            notes="§II.B, p.7–8, Fig.2. 입력 32×32 — MNIST 숫자는 28×28 칸 중앙 20×20 안에 있고, 끝점·모서리가 최상위 특징 탐지기 수용 영역 중앙에 오도록 일부러 크게 잡았다. "
                  "S2/S4는 max pooling이 아니다: 2×2 네 값을 더해 학습 계수를 곱하고 학습 bias를 더한 뒤 sigmoid — 맵마다 파라미터 2개. "
                  "C3는 S2의 모든 맵에 연결되지 않는다(Table I: 대칭 깨기 + 연결 수 절감, p.8). C5는 원문에서 '합성곱 층'(입력이 5×5라 결과 1×1, 사실상 완전연결). "
                  "출력은 softmax가 아니라 유클리드 RBF y_i = Σ_j (x_j − w_ij)²(Eq.7), 파라미터는 7×12 비트맵 모양으로 손으로 정해 고정. "
                  "비선형성 f(a) = A·tanh(Sa), A = 1.7159(Eq.6) — sigmoid가 아니라 scaled tanh. 그림: 원문 Fig.2 기반 재구성.")
top, bot = s.area.top(3.3, gap=0.2)
s.image(A("week3/paper_lenet5_arch.png"), top)
L, R = bot.cols(0.5, gap=0.4)
s.bullets(["**S2 · S4 = max pooling이 아니다**", ("2×2 합 × 학습 계수 + 학습 bias → sigmoid", 1),
           "**C3**는 S2의 일부 맵 조합에만 연결 (Table I)"], L, size=16)
s.bullets(["**C5**는 합성곱 층 (5×5 입력 → 1×1)", "출력 = softmax가 아닌 **유클리드 RBF** (Eq.7)",
           "활성화: A·tanh(Sa), A = 1.7159 (Eq.6)"], R, size=16)

s = d.slide("파라미터 6만 개를 손으로 세기", lead="params = C_out · (C_in · K · K) + C_out — 원문의 60,000 · 340,908을 그대로 재현한다",
            stage="계산",
            notes="C1 6 × (25 + 1) = 156; S2 6 × 2 = 12; C3: Table I에서 S2 맵 3개에 연결된 맵 6개, 4개에 연결 9개, 6개 모두에 연결 1개 → "
                  "6 × (75 + 1) + 9 × (100 + 1) + 1 × (150 + 1) = 456 + 909 + 151 = 1,516; S4 16 × 2 = 32; C5 120 × (16 × 25 + 1) = 48,120; F6 84 × (120 + 1) = 10,164. "
                  "합 60,000. 연결: 122,304 + 5,880 + 151,600 + 2,000 + 48,120 + 10,164 + 840 = 340,908. "
                  "원문 p.7: '340,908 connections, but only 60,000 trainable free parameters'. 출력 크기 32 → 28 → 14 → 10 → 5 → 1. "
                  "출처: LeCun et al. 1998 §II.B, Table I; week3.md 손계산(검산 완료).")
L, R = s.cols(0.64, gap=0.45)
s.table(["층", "출력", "학습 파라미터", "연결"],
        [["C1  합성곱 5×5", "6@28×28", "6 × (25+1) = 156", "122,304"],
         ["S2  서브샘플링", "6@14×14", "6 × 2 = 12", "5,880"],
         ["C3  합성곱 5×5 (부분 연결)", "16@10×10", "1,516", "151,600"],
         ["S4  서브샘플링", "16@5×5", "16 × 2 = 32", "2,000"],
         ["C5  합성곱 5×5", "120", "120 × (400+1) = 48,120", "48,120"],
         ["F6  완전 연결", "84", "84 × (120+1) = 10,164", "10,164"],
         ["출력  RBF", "10", "(고정)", "840"],
         ["합계", "", "**60,000**", "**340,908**"]], L, size=14, align="lccc", widths=[2.7, 1.45, 2.8, 1.1], highlight=(7,))
s.formula(["C3 (Table I)", "6·(3·25+1)", "+ 9·(4·25+1)", "+ 1·(6·25+1)", "= 1,516"], Box(R.x, R.y, R.w, 2.6), size=19)
s.bullets(["연결 34만 vs 파라미터 6만", ("공유 덕분에 **연결 ≫ 파라미터**", 1), "출력 크기 32 → 28 → 14 → 10 → 5 → 1"],
          Box(R.x, R.y + 2.85, R.w, R.h - 2.85), size=16)

s = d.slide("MNIST 결과: 여러 분류기와의 체계적 비교", lead="LeNet-5 0.95% — 단, SVM 계열도 1.0–1.1%로 가깝다",
            stage="결과",
            notes="§III.A–B. MNIST = NIST SD-3(인구조사국 직원) + SD-1(고등학생) 혼합, 학습 60,000 / 테스트 10,000. 20×20으로 크기 정규화 후 질량중심으로 28×28 중앙 정렬. "
                  "학습 20 pass, 전역 학습률 0.0005 → 0.00001, stochastic diagonal Levenberg–Marquardt. "
                  "결과(Fig.9, p.10–12): LeNet-5 테스트 0.95%(약 10 pass 후 안정), 학습 0.35%. 왜곡 증강(540,000장 추가)으로 0.8%, Boosted LeNet-4 [증강] 0.7%. "
                  "비교: 선형 12.0%, k-NN 5.0%, 28×28-300-10 4.7%, 1000 RBF 3.6%, SVM poly 4 1.1%, RS-SVM 1.0%, V-SVM poly 9 [증강] 0.8%, Tangent Distance 1.1%, LeNet-1 1.7%, LeNet-4 1.1%. "
                  "캡션: 'uncertainty in the quoted error rates is about 0.1%'. 한계: 학습 데이터를 늘리면 더 좋아진다(Fig.6). SVM은 비슷한 정확도지만 메모리·연산이 크다(§III.C). "
                  "그림: 원문 Fig.9 일부 발췌·재구성.")
L, R = s.cols(0.6, gap=0.45)
s.image(A("week3/paper_mnist_fig9.png"), L)
s.bullets(["데이터: 학습 **60,000** / 테스트 **10,000**", ("28×28, 질량중심 정렬", 1),
           "LeNet-5 테스트 **0.95%**, 학습 0.35%", "왜곡 증강 54만 장 추가 → **0.8%**",
           "SVM 다항식 4차 1.1% — **비슷한 수준**", ("원문: SVM은 메모리·연산이 크다 (§III.C)", 1),
           "오차 약 ±0.1%p → 0.1 차이는 비슷한 것"], R, size=16)

# ============================================================ Part 3
d.part(3, "옆길: SVM (1995)", "신경망이 주춤하던 시기, 다른 길은 일반화를 어떻게 다뤘나?",
       notes="Part 3: Cortes & Vapnik (1995) Support-Vector Networks. LeNet-5 논문(1998)이 직접 비교 대상으로 삼은 방법. 1990~2000년대의 강력한 기준 모델.")

d.paper("Cortes & Vapnik (1995)", "Support-Vector Networks", "Machine Learning 20, 273–297",
        "고차원 특징 공간에서 선형 경계를 만드는 support-vector network는 **오류 없이 분리되는** 학습 데이터에만 구현돼 있었다.",
        "여유 변수 ξ로 일부 오류를 허용하는 **soft margin** — 분리 불가능한 데이터까지 확장. 커널로 특징 공간을 직접 계산하지 않는다.",
        "초록, §1 마지막 두 쪽(p.275–276), §6.2.1 Table 1–2",
        url="math.uic.edu · cortes95.pdf",
        result="USPS 4.3% (LeNet1 5.1%), NIST 1.1% (LeNet-4와 대등).",
        notes="Cortes & Vapnik (1995). 문제(초록): 이전 구현은 오류 없이 분리되는 데이터에만. "
              "논문이 직접 서술하듯 최적 초평면(마진 최대)은 1965년(Vapnik 1982에 정리)에 이미 풀렸고(p.275), 커널을 이용한 비선형 SVM은 Boser, Guyon & Vapnik(1992)(p.276). "
              "이 논문의 새 기여 = soft margin(§3)과 체계적 실험(§6). 출처: Cortes & Vapnik 1995 초록, p.275–276, §3, §6.")

s = d.slide("마진과 서포트 벡터 — 1995년 이전부터 있던 생각", lead="여러 경계 중 두 부류 사이 여백(margin)이 가장 넓은 것 — 해는 소수의 점이 정한다",
            stage="아이디어",
            notes="최적 초평면 = 마진이 최대인 선형 결정 함수(1965, Vapnik). 해는 소수의 학습 벡터(support vectors)만으로 결정: w₀ = Σ α_i z_i (Eq.6). "
                  "마진 = 2/|w₀| (Eq.12). 일반화 한계: E[Pr(test error)] ≤ E[#support vectors] / #training vectors (Eq.5) — 차원이 식에 직접 들어 있지 않다. "
                  "손계산: x₁ = (1, 1), y = +1; x₂ = (−1, −1), y = −1. w = (0.5, 0.5), b = 0이면 y_i(w·x_i + b) = 1 — 둘 다 서포트 벡터. "
                  "마진 = 2/‖w‖ = 2/0.7071 = 2.828 = 두 점 사이 거리 √8과 일치(검산 완료). 볼록 최적화라 해가 유일하다. 그림은 개념도.")
L, R = s.cols(0.48, gap=0.45)
s.image(A("week3/svm_margin.png"), Box(L.x, L.y, L.w, L.h - 0.2))
s.formula(["x₁ = (1, 1) y = +1 · x₂ = (−1, −1) y = −1", "w = (0.5, 0.5), b = 0 → y·(w·x + b) = 1",
           "마진 = 2 / ‖w‖ = 2 / 0.7071 = 2.828 = √8"], Box(R.x, R.y, R.w, 1.6), size=16)
s.bullets(["**서포트 벡터**: 경계를 결정하는 가장 가까운 점 — 해는 이 점들만으로 정해진다 (Eq.6)",
           "일반화 한계: 테스트 오류 기댓값 ≤ **서포트 벡터 수 / 학습 벡터 수** (Eq.5)",
           "역사: 마진 **1965**, 커널 SVM **1992** — 1995년의 발명이 아니다"], Box(R.x, R.y + 1.85, R.w, R.h - 1.85), size=16)

s = d.slide("1995년의 새 점: soft margin", lead="제약을 ξ만큼 어기는 것을 허용하고, 어긴 양의 합에 C만큼 벌점을 준다",
            stage="계산",
            notes="원문 Eq.22–24: 제약 y_i(w·x_i + b) ≥ 1 − ξ_i, ξ_i ≥ 0; 최소화 ½w² + C·F(Σ ξ_i^σ). σ = 1이 유일해가 있는 가장 작은 값이라 이를 택하고 'soft margin hyperplane'이라 부름(p.281). "
                  "강의 표기: min ½‖w‖² + C·Σ ξ_i. C가 크면 학습 오류를 덜 허용(좁은 마진), 작으면 마진을 넓게. "
                  "그림 예: w = (0.5, 0.5), b = 0. 마진 안에 있지만 올바른 쪽의 − 점 (−0.3, −0.2): w·x = −0.25 → ξ = 1 − 0.25 = 0.75. "
                  "반대편으로 넘어간 + 점 (−0.6, −0.4): w·x = −0.5 → ξ = 1.5 (> 1이면 오분류). 그림: 원문 Fig.2·§3 기반 개념도(점 좌표는 설명용).")
L, R = s.cols(0.5, gap=0.45)
s.formula(["min  ½‖w‖² + C · Σ ξ_i", "s.t.  y_i (w·x_i + b) ≥ 1 − ξ_i", "ξ_i ≥ 0"], Box(L.x, L.y, L.w, 1.75), size=21)
s.symbols([("ξ_i", "점 i가 제약을 어긴 양 (여유 변수)"), ("C", "벌점 크기 — 크면 오류를 덜 허용"),
           ("ξ = 0", "마진 밖, 올바른 쪽"), ("0 < ξ ≤ 1", "마진 안, 분류는 맞음"), ("ξ > 1", "반대편 = 오분류")],
          Box(L.x, L.y + 2.0, L.w, L.h - 2.0), size=15, key_w=1.55)
s.image(A("week3/paper_svm_softmargin.png"), R)

s = d.slide("커널: 특징 공간을 계산하지 않고", lead="입력을 고차원으로 올리면 선형 분리가 쉬워진다 — 내적만 커널로 바꿔 계산한다",
            stage="아이디어",
            notes="1차원에서 점 하나로 안 나뉘는 데이터도 x → (x, x²)로 올리면 선형 분리. 커널('convolution of the dot-product')은 이 변환을 명시적으로 계산하지 않고 내적만 바꾼다 — "
                  "Boser, Guyon & Vapnik(1992)이 보였다고 원문이 명시(p.276). 원문 §4(p.285)의 예: 다항식 K(u, v) = (u·v + 1)^d, RBF K(u, v) = exp(−|u − v|²/σ²). "
                  "2주차 은닉층은 좋은 좌표를 학습하고, SVM 커널은 좋은 좌표를 사람이 고른다. 저자 결론(p.290): 문제의 사전 지식을 반영한 커널을 만들면 더 좋아질 것. "
                  "Bottou et al. 1994 인용(p.289–290): SVM은 기하 지식을 넣지 않아서 '픽셀을 고정된 무작위 순열로 섞어도 똑같이 잘 할 것' — CNN과 정반대의 선택.")
L, R = s.cols(0.52, gap=0.45)
s.image(A("week3/kernel_lift.png"), L)
s.formula(["K(u, v) = (u·v + 1)^d", "K(u, v) = exp(−|u − v|² / σ²)"], Box(R.x, R.y, R.w, 1.3), size=19)
s.bullets(["**MLP 은닉층** (2주차): 좌표를 **학습**", "**SVM 커널**: 좌표를 **사람이 선택**",
           "SVM은 픽셀을 무작위로 섞어도 똑같이 학습 (p.289)", ("CNN은 **이웃 관계**를 구조에 넣는다 — 정반대 선택", 1),
           "저자 결론: 사전 지식을 반영한 커널이면 더 좋아질 것"], Box(R.x, R.y + 1.5, R.w, R.h - 1.5), size=16)

s = d.slide("결과: 손글씨 숫자에서 특수 설계 신경망과 대등", lead="USPS: 2차 이상 다항식이 LeNet1(5.1%)보다 낫고, 차수를 올려도 과적합이 거의 없다",
            stage="결과",
            notes="§6.2. (a) USPS 7,300 학습 / 2,000 테스트, 16×16, 전처리(중앙 정렬·deslant·가우시안 스무딩). 클래스마다 분류기 10개, 최대 출력으로 판정. "
                  "Table 1: 사람 2.5%, CART 17%, C4.5 16%, 최선 2층 신경망 6.6%, 특수 구조 5층 신경망(LeNet1) 5.1%. "
                  "Table 2(다항식 차수 1–7): 오류 12.0/4.7/4.4/4.3/4.3/4.2/4.3%, support vector 수 200/127/148/165/175/185/190, 특징 공간 차원 256 → 약 10^16. "
                  "(b) NIST 60,000/10,000, 28×28, 4차 다항식만, 전처리 없음: 테스트 1.1% — 같은 벤치마크의 LeNet4와 대등(LeCun 1998 Fig.9에서도 SVM poly 4 = 1.1%, LeNet-4 = 1.1%). "
                  "'SVM이 신경망을 완전히 이겼다'는 과장: LeNet-5는 0.95%. 그림: 원문 Table 1–2 기반.")
L, R = s.cols(0.55, gap=0.45)
s.image(A("week3/paper_usps_table2.png"), L)
s.table(["방법 (USPS, Table 1)", "테스트 오류"],
        [["사람", "2.5%"], ["CART · C4.5", "17% · 16%"], ["최선 2층 신경망", "6.6%"], ["LeNet1 (특수 구조 5층)", "5.1%"],
         ["SVM 다항식 4차 (Table 2)", "**4.3%**"]], Box(R.x, R.y, R.w, 2.75), size=15, align="lc", highlight=(4,))
s.bullets(["NIST 6만/1만: 4차 다항식 **1.1%** ≈ LeNet-4 1.1%", "특징 공간 약 10^16차원인데 **과적합 거의 없음**",
           ("Eq.5: 차원이 아니라 서포트 벡터 수가 좌우", 1)], Box(R.x, R.y + 2.95, R.w, R.h - 2.95), size=16)

# ============================================================ Part 4
d.part(4, "깊이의 벽 (2006–2011)", "층을 깊게 쌓으면 왜 학습이 안 됐고, 무엇이 바뀌었나?",
       notes="Part 4: 깊은 망을 학습시키려는 2006–2011년의 세 갈래 — 층별 사전학습(Hinton et al. 2006), 실패 원인 진단과 초기화(Glorot & Bengio 2010), ReLU(Nair & Hinton 2010, Glorot et al. 2011).")

d.paper("Hinton, Osindero & Teh (2006)", "A Fast Learning Algorithm for Deep Belief Nets", "Neural Computation 18(7), 1527–1554",
        "은닉층이 많은 방향성 신뢰망은 ‘explaining away’ 때문에 은닉 활성의 추론이 어렵고, 모든 층을 함께 학습해야 해서 느리다.",
        "RBM을 **한 층씩 탐욕적으로** 쌓아 학습하고, 전체는 **up-down 알고리즘**(wake-sleep의 contrastive 버전)으로 미세 조정한다.",
        "초록, §1, §6.1",
        url="cs.toronto.edu/~hinton/absps/fastnc.pdf",
        result="MNIST(기하 지식 없음) 테스트 1.25% — 깊은 망도 학습될 수 있다.",
        notes="Hinton, Osindero, Teh (2006). 문제(§1): explaining away로 사후분포 추론이 어렵고 변분 근사는 나쁘다. "
              "아이디어: complementary prior → 가중치를 묶은 무한 방향성 망 = RBM(§2–3). 탐욕적 층별 학습(§4): 층을 추가할 때마다 로그우도 변분 하한이 개선. "
              "미세 조정은 역전파가 아니라 up-down 알고리즘(§5, 초록). 모델은 이미지와 라벨의 결합분포를 배우는 생성 모델. "
              "사전학습 후 '역전파' 미세 조정은 같은 해 Hinton & Salakhutdinov(2006)와 Bengio et al.(2007) 계열에서 표준이 됨 [이 두 논문은 원문 미확인 — 출처 언급만]. "
              "출처: Hinton et al. 2006 초록, §1, §4–6.")

s = d.slide("층별 탐욕 학습 → up-down 미세 조정", lead="RBM 하나를 학습하고 그 은닉 활성을 다음 RBM의 데이터로 — 마지막 조정도 역전파가 아니다",
            stage="아이디어",
            notes="실험(§6.1): 784(28×28) → 500 → 500 ↔ 2000(+10 라벨 유닛). 가중치 784×500 + 500×500 + (500+10)×2000 = 392,000 + 250,000 + 1,020,000 = 1,662,000 ≈ 'about 1.7 million'(검산, bias 제외). "
                  "각 층 RBM 30 epoch, 층당 몇 시간(Matlab, 3GHz Xeon); 탐욕 학습 직후 테스트 2.49%. up-down 300 epoch → 1.39%, 6만 장 전부로 59 epoch 더 → 1.25%. 총 약 1주. "
                  "비교(§6.1, Table 1): 손으로 맞추지 않은 역전파망 최선 1.5%(800 은닉 1층 1.53%, 500-300 2층 1.51%), SVM 1.4%(Decoste & Schölkopf 2002), k-NN 3.1%. "
                  "가중치 공유·서브샘플링을 쓴 LeCun 1998은 0.95% — 의의는 '깊은 망을 층별로 학습할 수 있다'는 것이지 절대 성능이 아니다. "
                  "주의: 당시의 '사전학습'은 비지도 RBM 쌓기 — 오늘 LLM의 자기지도 사전학습과 다른 개념. 그림: 원문 Fig.1 기반 재구성.")
L, R = s.cols(0.44, gap=0.45)
s.image(A("week3/paper_dbn_arch.png"), L)
s.table(["MNIST (기하 지식 없음, §6.1)", "테스트 오류"],
        [["DBN (탐욕 학습 직후)", "2.49%"], ["DBN (+ up-down 미세 조정)", "**1.25%**"], ["SVM", "1.4%"],
         ["역전파망 (최선)", "1.5%"], ["k-NN", "3.1%"], ["참고: LeNet-5 (가중치 공유)", "0.95%"]],
        Box(R.x, R.y, R.w, 3.0), size=15, align="lc", highlight=(1,))
s.bullets(["==주의== 미세 조정 = **up-down**, 역전파가 아니다", ("역전파 미세 조정은 Hinton & Salakhutdinov 2006 · Bengio 2007 계열", 1),
           "당시 ‘사전학습’ ≠ 오늘 LLM의 사전학습"], Box(R.x, R.y + 3.2, R.w, R.h - 3.2), size=15)

d.paper("Glorot & Bengio (2010)", "Understanding the difficulty of training deep feedforward neural networks", "AISTATS 2010, PMLR 9:249–256",
        "사전학습으로 깊은 망이 학습되지만, 왜 **표준 경사하강 + 랜덤 초기화**는 깊은 망에서 그렇게 못하는가?",
        "sigmoid 망의 **맨 위 은닉층 포화**와 **층별 분산 불균형**을 진단하고, 분산을 유지하는 **normalized 초기화**를 제안한다.",
        "초록, §3.1, §4.2 Eq.12–16",
        url="proceedings.mlr.press/v9/glorot10a/glorot10a.pdf",
        result="5층 tanh 망에서 normalized 초기화만으로 테스트 오류가 낮아진다 (Table 1).",
        notes="Glorot & Bengio (2010). §3.1: sigmoid는 평균이 0이 아니라 랜덤 초기화된 깊은 망에서 맨 위 은닉층을 0 근처 포화로 몰아 학습을 늦춘다(Fig.2). "
              "5층 sigmoid 망은 학습 내내 포화에서 못 벗어났고, 4층은 천천히 탈출. tanh는 아래층부터 차례로 포화, softsign은 덜 포화(§3.2–3.3). "
              "§4.2: 순방향 n_i·Var[W] = 1, 역방향 n_{i+1}·Var[W] = 1 → 절충 Var[W] = 2/(n_i + n_{i+1})(Eq.12). 이 논문은 ReLU를 다루지 않는다. 출처: Glorot & Bengio 2010.")

s = d.slide("분산을 지키는 초기화와 그 결과", lead="표준 초기화는 n·Var[W] = 1/3 → 층을 내려갈수록 기울기 분산이 줄어든다",
            stage="계산",
            notes="표준 초기화 U[−1/√n, 1/√n](Eq.1)은 n·Var[W] = 1/3(Eq.15). n = 1000이면 ±0.0316 → 1000 × (0.0316²/3) = 0.333 → 5층 지나면 기울기 분산 약 (1/3)^5 ≈ 0.004배. "
                  "normalized init(Eq.16): W ~ U[−√6/√(n_j + n_{j+1}), +√6/√(n_j + n_{j+1})] — 오늘날 Xavier/Glorot 초기화. n_in = n_out = 1000이면 ±√6/√2000 = ±0.0548, "
                  "Var = 0.0548²/3 = 0.001 = 2/2000(검산 완료). "
                  "결과 Table 1(5층, 층당 1,000 유닛, 테스트 오류 %): MNIST Sigmoid 2.21 / Tanh 1.76 / Tanh N 1.64; CIFAR-10 57.28 / 55.9 / 52.92; Shapeset 82.61 / 27.15 / 15.60. "
                  "흔한 오해: 기울기 소실 = 'sigmoid′ ≤ 0.25' 하나만이 아니다 — 초기화 스케일과 sigmoid 평균이 만드는 포화가 원인. 참고: LeNet(1989/1998)은 sigmoid가 아니라 scaled tanh. "
                  "그림: 원문 Table 1 기반.")
top, bot = s.area.top(1.25, gap=0.25)
L, R = top.cols(0.5, gap=0.4)
s.formula(["Var[W] = 2 / (n_in + n_out)", "W ~ U[ ± √6 / √(n_in + n_out) ]"], L, size=18)
s.formula(["n = 1000: ±√6/√2000 = ±0.0548 → Var = 0.001", "표준 init: n·Var = 1/3 → 5층 (1/3)⁵ ≈ 0.004"], R, size=16)
s.image(A("week3/paper_glorot_table1.png"), bot)

s = d.slide("ReLU: 사전학습 없이도 깊게", lead="양수 구간 기울기 1, 실제 0을 내는 희소 표현 — 큰 라벨 데이터에서는 사전학습이 필요 없었다",
            stage="논문",
            notes="Nair & Hinton (2010, ICML) 'Rectified Linear Units Improve Restricted Boltzmann Machines': RBM 이진 유닛을 무한 복제한 stepped sigmoid를 "
                  "noisy rectified linear unit max(0, x + N(0, σ(x)))로 근사(§2), 결정론적 max(0, x)를 역전파에도 사용. 여러 층을 지나도 상대 강도 정보 보존(초록, §4). NORB·LFW에서 이진 유닛보다 좋은 특징. "
                  "Glorot, Bordes & Bengio (2011, AISTATS) 'Deep Sparse Rectifier Neural Networks' Table 1(3층 테스트 오류, 사전학습 없음): Rectifier MNIST 1.43%, CIFAR-10 50.86%, NORB 16.40% vs Tanh 1.57% / 52.62% / 19.29%. "
                  "결론: 큰 라벨 데이터의 순수 지도학습에서는 deep rectifier net이 사전학습 없이도 최고 성능(초록). "
                  "손계산: sigmoid′ 최댓값 0.25 → 10층 0.25¹⁰ = 9.54×10⁻⁷(가중치 효과 제외 단순화). ReLU는 AlexNet이 처음이 아니다(Jarrett et al. 2009도 사용; AlexNet §3.1이 언급).")
top, bot = s.area.top(2.55, gap=0.25)
s.image(A("week3/relu_grad.png"), top)
L, R = bot.cols(0.56, gap=0.4)
s.table(["Glorot 2011 Table 1 (3층)", "Rectifier", "Tanh"],
        [["MNIST", "**1.43%**", "1.57%"], ["CIFAR-10", "**50.86%**", "52.62%"], ["NORB", "**16.40%**", "19.29%"]],
        L, size=15, align="lcc", widths=[3.2, 1.4, 1.4])
s.bullets(["Nair & Hinton (2010): RBM에서 **max(0, x)**", "Glorot et al. (2011): 큰 라벨 데이터면 **사전학습 불필요**",
           ("sigmoid′ ≤ 0.25 → 10층 0.25^10 ≈ 9.5×10⁻⁷", 1)], R, size=15)

# ============================================================ Part 5
d.part(5, "AlexNet · VGG (2012–2014)", "120만 장과 GPU 두 대 — 무엇이 2012년의 격차를 만들었나?",
       notes="Part 5: Krizhevsky, Sutskever, Hinton (2012)과 Simonyan & Zisserman (2014). ImageNet 시대의 CNN.")

d.paper("Krizhevsky et al. (2012)", "ImageNet Classification with Deep Convolutional Neural Networks", "NeurIPS 25 (2012), 1097–1105",
        "이전 데이터셋은 수만 장 수준. 수백만 장 · 1,000 클래스에는 큰 용량 + CNN의 사전 가정 + **GPU 구현**이 필요했다.",
        "합성곱 5 + 완전 연결 3층에 **ReLU · GPU 2대 · 데이터 증강 · dropout**을 결합한다.",
        "초록, §3.1, §4 (과적합 줄이기), Table 2",
        url="papers.nips.cc (NeurIPS 2012 proceedings)",
        result="ILSVRC-2012 top-5 15.3% — 단, **7개 CNN 앙상블**이고 2개는 외부 데이터로 사전학습 (외부 데이터 없이 16.4%).",
        notes="Krizhevsky et al. (2012). 문제(§1): NORB·Caltech·CIFAR 등 이전 데이터셋은 수만 장. 망 크기는 GPU 메모리와 학습 시간이 제한하며 "
              "'더 빠른 GPU와 더 큰 데이터만 기다려도 좋아질 것'(§1). 비지도 사전학습은 쓰지 않았다(§7). "
              "15.3%는 단일 모델·120만 장만의 결과가 아니다: Table 2와 Russakovsky Table 8(SuperVision 16.42%, †외부 데이터 15.32%). 출처: Krizhevsky et al. 2012 §1, §6–7, Table 2.")

s = d.slide("AlexNet 구조와 학습 설정", lead="6,000만 파라미터 · 65만 뉴런 — GTX 580 3GB 두 대로 5–6일",
            stage="계산",
            notes="§3.5, Fig.2: conv1 96@11×11×3 stride 4, conv2 256@5×5×48, conv3 384@3×3×256, conv4 384@3×3×192, conv5 256@3×3×192, FC 4096–4096–1000, 1000-way softmax. "
                  "6,000만 파라미터, 65만 뉴런(초록). 커널을 GPU 두 대에 반씩 나누고 특정 층에서만 통신(§3.2). "
                  "손계산: conv1 파라미터 96 × (11·11·3) + 96 = 34,944. 주의: 원문 서술(224 입력, 11×11, stride 4)로는 (224 − 11)/4 + 1 = 54.25로 정수가 아니다 — 실제 구현은 227 입력(→ 55)으로 알려져 있음. "
                  "학습(§5): SGD 배치 128, momentum 0.9, weight decay 0.0005('단순한 규제가 아니라 학습 오류도 줄인다'), 초기화 N(0, 0.01²), 학습률 0.01에서 검증 오류가 멈추면 1/10(3번), 약 90 epoch. "
                  "그림은 227 입력 기준 shape 흐름 개념도.")
top, bot = s.area.top(2.35, gap=0.25)
s.image(A("week3/alexnet_pipeline.png"), top)
L, R = bot.cols(0.5, gap=0.4)
s.formula(["conv1: 96 × (11·11·3) + 96 = 34,944", "O = ⌊(227 − 11) / 4⌋ + 1 = 55"], Box(L.x, L.y, L.w, 1.15), size=17)
s.bullets(["원문의 224 입력으로는 (224 − 11)/4 + 1 = **54.25**", ("구현은 227 입력으로 알려짐 — shape 계산 때 주의", 1)],
          Box(L.x, L.y + 1.3, L.w, L.h - 1.3), size=15)
s.bullets(["SGD 배치 128, momentum 0.9", "weight decay 0.0005, 초기화 N(0, 0.01²)", "학습률 0.01 → 정체 때 1/10 (3번)",
           "약 90 epoch, **GPU 2대 5–6일**"], R, size=16)

s = d.slide("15.3%의 정체", lead="단일 CNN은 검증 18.2% — 5개 평균 16.4%, 외부 데이터로 사전학습한 2개를 더한 7개 평균이 15.3%",
            stage="결과",
            notes="ILSVRC-2012(Table 2): 1 CNN 검증 top-5 18.2%, 5 CNN 16.4%(테스트 16.4%), ImageNet Fall 2011(약 1,500만 장, 22K 클래스)로 사전학습한 CNN 2개 + 5 CNN = 7 CNN 테스트 15.3%. "
                  "2위 26.2%(SIFT + Fisher Vector, 여러 분류기 평균). 외부 데이터 없는 공식 결과 16.4%(Russakovsky Table 8: SuperVision 16.42%, †외부 데이터 15.32%). "
                  "ILSVRC-2010 테스트(Table 1): CNN top-1 37.5% / top-5 17.0% vs 대회 최고 47.1% / 28.2%, 이후 최고 45.7% / 25.7%. "
                  "이 사실은 '구조 하나 덕분이 아니다'라는 메시지를 오히려 강화한다. 그림: 원문 Table 2 기반.")
L, R = s.cols(0.58, gap=0.45)
s.image(A("week3/paper_alexnet_table2.png"), L)
s.bullets(["CNN **1개**: 검증 18.2%", "**5개** 평균: 16.4% ← 외부 데이터 없는 공식 결과",
           "**7개** 평균: 15.3%", ("2개는 ImageNet Fall 2011 (약 1,500만 장)로 사전학습", 1),
           "2위 26.2% (SIFT + FV) — 격차는 어느 쪽이든 크다", "ILSVRC-2010: top-5 **17.0%** vs 28.2%"], R, size=16)

s = d.slide("구조 하나 덕분이 아니다 — 원문이 보고한 기여", lead="각 기법의 효과를 원문 수치로 — 데이터 · GPU · ReLU · 규제 · 앙상블이 함께 작동했다",
            stage="정리",
            notes="원문 수치: ReLU — 4층 CNN이 CIFAR-10 학습 오류 25%에 tanh보다 6배 빨리 도달(§3.1, Fig.1). GPU 2대 — 단일 GPU 절반 망 대비 top-1/top-5 1.7%/1.2% 개선(§3.2). "
                  "LRN — 1.4%/1.2%(§3.3). 겹치는 pooling z=3, s=2 — 0.4%/0.3%(§3.4). 증강(§4.1): 256×256에서 무작위 224×224 + 좌우 반전 → (256−224)² × 2 = 2,048배, "
                  "RGB PCA 색 변형 top-1 1% 이상. Dropout p = 0.5(§4.2): 처음 두 FC층, 없으면 심한 과적합, 수렴 iteration은 약 2배. "
                  "깊이: 중간 합성곱 층 하나를 빼면 top-1 약 2% 나빠짐(§7). ReLU·dropout·GPU CNN 모두 이 논문이 최초는 아니다(Nair & Hinton 2010, Hinton et al. 2012, Cireşan et al.) — 조합과 규모가 핵심. "
                  "이 관점은 Transformer에도 그대로 적용된다.")
s.table(["조건", "AlexNet 원문이 보고한 것"],
        [["데이터", "ImageNet 약 120만 장 · 1,000 클래스 (+ 15.3%에는 외부 데이터 사전학습 2개)"],
         ["증강", "무작위 자르기 + 좌우 반전 = (256 − 224)² × 2 = **2,048배**, PCA 색 변형으로 top-1 1% 이상 개선"],
         ["ReLU", "CIFAR-10 학습 오류 25%까지 tanh보다 **6배** 빠름 (Fig.1)"],
         ["GPU 2대", "GTX 580 3GB 두 대, 단일 GPU 절반 망 대비 top-1/top-5 1.7%/1.2% 개선"],
         ["Dropout 0.5", "없으면 심한 과적합 (대신 수렴 iteration 약 2배)"],
         ["깊이", "중간 합성곱 층 하나를 빼면 top-1 약 **2%** 나빠짐"],
         ["앙상블", "1개 18.2% → 5개 16.4% → 7개 15.3%"]],
        Box(s.area.x, s.area.y, s.area.w, 4.3), size=15, widths=[1.7, 10.4])
s.callout("표현력이 충분해도 학습 · 데이터 · 자원이 없으면 그 표현을 **얻지 못한다** — Transformer도 마찬가지.",
          Box(s.area.x, s.area.y + 4.45, s.area.w, 0.75), kind="key", size=16)

d.paper("Simonyan & Zisserman (2014)", "Very Deep Convolutional Networks for Large-Scale Image Recognition", "ICLR 2015 · arXiv:1409.1556",
        "AlexNet의 첫 층은 11×11 · stride 4처럼 **큰 필터**를 썼다. 깊이 자체의 효과를 따로 보고 싶다.",
        "모든 합성곱을 **3×3**으로 통일하고 깊게(11–19층) 쌓는다.",
        "§2.3 (3×3 논증), Table 2, Table 7",
        url="arxiv.org/pdf/1409.1556",
        result="ILSVRC-2014 top-5 7.3% (2위), 제출 후 2개 앙상블 6.8%.",
        notes="Simonyan & Zisserman (2014/ICLR 2015). 구조: 11층(A)~19층(E), 파라미터 133M~144M(Table 2). "
              "결과(Table 7): ILSVRC-2014 제출(7개 앙상블) top-5 테스트 7.3%(2위); 제출 후 2개 앙상블 6.8%, 단일 7.0%. 같은 표에서 GoogLeNet 7개 6.7%. "
              "3×3 쌓기는 VGG가 처음 생각한 것이 아니라 체계적으로 보인 것(Ciresan 2011 등 언급). 출처: arXiv:1409.1556 v6 §2.3, Table 2, Table 7.")

s = d.slide("3×3을 쌓는 이유", lead="3×3 세 층 = 7×7 한 층과 같은 수용 영역 — 파라미터는 27C² vs 49C², 비선형은 3번",
            stage="계산",
            notes="§2.3: 3×3 두 층(사이 pooling 없음)의 유효 수용 영역은 5×5, 세 층은 7×7. 7×7 한 층 대신 3×3 세 층을 쓰면 (1) ReLU 3번 → 결정 함수가 더 변별적, "
                  "(2) 입출력 C채널일 때 3·(3²C²) = 27C² vs 7²C² = 49C², '81% more'. 7×7 필터에 3×3 분해를 강제하는 규제로 볼 수 있다. "
                  "손계산(검산 완료): C = 64면 27·64² = 110,592 vs 49·64² = 200,704. 49/27 − 1 = 0.815. bias 제외. "
                  "제약: 멀리 떨어진 두 위치가 만나려면 층을 여러 번 거쳐야 한다(경로가 길다) — 5주차 Attention과 대비.")
top, bot = s.area.top(2.2, gap=0.3)
s.image(A("week3/receptive_field.png"), top)
L, R = bot.cols(0.5, gap=0.4)
s.formula(["3 · (3² C²) = 27 C²   vs   7² C² = 49 C²", "C = 64: 110,592 vs 200,704", "49 / 27 − 1 = 0.815 → 81% 더 많다"],
          Box(L.x, L.y, L.w, 1.75), size=17)
s.bullets(["3×3 한 번 **3칸**, 두 번 **5칸**, 세 번 **7칸**", "비선형(ReLU)이 1번 → **3번**",
           "결과: ILSVRC-2014 **7.3%** (2위, 7개 앙상블)", ("같은 해 우승 GoogLeNet 6.7% (VGG Table 7)", 1),
           "==제약== 먼 위치가 만나려면 **경로가 길다**"], R, size=16)

# ============================================================ Part 6
d.part(6, "BatchNorm (2015)", "깊은 망이 학습률과 초기화에 민감하다면?",
       notes="Part 6: Ioffe & Szegedy (2015) Batch Normalization과, 그 설명을 다시 검토한 Santurkar et al. (2018).")

d.paper("Ioffe & Szegedy (2015)", "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift",
        "ICML 2015, PMLR 37:448–456 · arXiv:1502.03167",
        "앞 층 파라미터가 바뀌면 각 층 입력 분포도 계속 바뀌어, 낮은 학습률 · 조심스러운 초기화가 필요하고 포화 비선형은 학습이 어렵다.",
        "각 특징을 **미니배치 평균·분산**으로 정규화한 뒤 학습되는 γ, β로 되돌릴 수 있게 한다. 추론 때는 고정된 모집단 통계를 쓴다.",
        "§2 첫 문단 (ICS 정의), §3 Algorithm 1, §3.2 합성곱 문단",
        url="arxiv.org/pdf/1502.03167",
        result="같은 정확도에 **14배 적은** step, 6개 앙상블 ImageNet top-5 테스트 4.82%.",
        notes="Ioffe & Szegedy (2015). 저자는 이 현상을 internal covariate shift(ICS) — '학습 중 파라미터 변화로 인한 망 활성 분포의 변화' — 라 정의하고 줄이려 했다(§2). "
              "완전 whitening은 비싸서 각 스칼라 특징을 독립 정규화(§3). 규제 효과(§3.4): 샘플이 배치의 다른 샘플과 함께 보이므로 출력이 결정론적이지 않다 → Dropout을 줄이거나 없앨 수 있음. "
              "한계(§5): 배치 통계에 의존 — 작은 배치·RNN 적용은 미래 과제. 출처: Ioffe & Szegedy 2015 §2–5.")

s = d.slide("BatchNorm의 계산", lead="미니배치로 평균·분산 → 정규화 → γ·β — 합성곱 층에서는 채널마다 B × H × W 전체로",
            stage="계산",
            notes="Algorithm 1: μ_B = (1/m)Σx_i, σ_B² = (1/m)Σ(x_i − μ_B)², x̂_i = (x_i − μ_B)/√(σ_B² + ε), y_i = γx̂_i + β. "
                  "γ = √Var, β = E이면 원래 활성 복원 가능 → 항등 변환도 표현 가능. 추론 때는 이동 평균한 모집단 통계로 고정된 선형 변환(Alg.2). "
                  "손계산: (1, 2, 3, 4) → μ = 2.5, σ² = 1.25, σ = 1.118, x̂ = (−1.34, −0.45, 0.45, 1.34)(검산 완료). "
                  "합성곱 층(§3.2): 같은 특징 맵의 값은 위치와 무관하게 같은 방식으로 정규화 → 미니배치 m개 × 공간 p×q 전체(유효 배치 m·pq)로 통계, γ·β는 특징 맵(채널)당 한 쌍. "
                  "예: B = 32, 14×14 맵이면 채널당 32 × 196 = 6,272개 값. 강의 표기: (B, C, H, W)에서 채널 c마다 (B, H, W) 축으로 평균·분산.")
L, R = s.cols(0.5, gap=0.45)
s.formula(["μ_B = (1/m) Σ x_i", "σ_B² = (1/m) Σ (x_i − μ_B)²", "x̂_i = (x_i − μ_B) / √(σ_B² + ε)", "y_i = γ · x̂_i + β"],
          Box(L.x, L.y, L.w, 2.3), size=19)
s.bullets(["μ, σ: 미니배치에서 **계산** (학습 X)", "γ, β: **학습** — γ = σ, β = μ면 원래 값 복원",
           "추론: 학습 중 모은 **모집단 통계**로 고정"], Box(L.x, L.y + 2.5, L.w, L.h - 2.5), size=16)
s.table(["단계", "값"], [["x (한 채널의 값들)", "(1, 2, 3, 4)"], ["μ", "2.5"], ["σ²  (σ)", "1.25  (1.118)"],
                        ["x̂", "(−1.34, −0.45, 0.45, 1.34)"]], Box(R.x, R.y, R.w, 2.1), size=15, align="lc")
s.callout("**합성곱 층**: 채널 c 하나의 통계 = 배치 B × 위치 H × W 전체\n"
          "예: B = 32, 14×14 맵 → 채널당 32 × 196 = **6,272**개 값, γ·β는 채널당 한 쌍 (§3.2)",
          Box(R.x, R.y + 2.35, R.w, R.h - 2.35), kind="tip", size=15)

s = d.slide("결과: 14배 적은 step으로 같은 정확도", lead="학습률을 키울 수 있게 되자 Inception의 72.2% 정확도를 2.1M step 만에",
            stage="결과",
            notes="§4.2 실험: Inception(GoogLeNet 변형) + BN, 학습률 5배(BN-x5)·30배(BN-x30), Dropout 제거, LRN 제거 등. "
                  "Fig.3: Inception이 72.2% 정확도에 31.0M step, BN-Baseline 13.3M, BN-x5 2.1M(14배 적음), BN-x30 2.7M에 최고 74.8%. "
                  "BN-x5-Sigmoid 69.8% — 원래 Inception은 sigmoid로는 chance 수준. 앙상블 6개: ImageNet top-5 검증 4.9%, 테스트 4.82%, '사람 평가자 정확도 초과'(초록, §4.2.3). "
                  "사람 5.1%는 Russakovsky Table 9(전문 주석자 A1 추정치; A2는 12.0%). 그림: 원문 Fig.3 표 기반.")
L, R = s.cols(0.6, gap=0.45)
s.image(A("week3/paper_bn_steps.png"), L)
s.bullets(["BN-x5: 31.0M → **2.1M** step (≈ 14배)", "BN-x30: 최종 **74.8%**", "sigmoid로도 학습: 69.8%",
           ("BN 없는 Inception은 sigmoid로 chance 수준", 1), "6개 앙상블 top-5 테스트 **4.82%**",
           ("사람 추정 5.1% (Russakovsky Table 9)보다 낮음", 1)], R, size=16)

s = d.slide("왜 효과가 있나 — 원 논문의 가설과 2018년의 반박", lead="‘internal covariate shift를 줄여서’는 가설이었다 — 분포를 일부러 흔들어도 BN은 잘 학습한다",
            stage="검증",
            notes="Santurkar, Tsipras, Ilyas, Madry (2018) 'How Does Batch Normalization Help Optimization?', NeurIPS 2018, arXiv:1805.11604. "
                  "BN의 성공은 층 입력 분포 안정(ICS 감소)과 '거의 관련이 없다'(초록). BN 뒤에 시간에 따라 변하는 평균·분산 잡음을 일부러 넣은 'noisy BatchNorm'도 표준 BN과 거의 같은 성능(Fig.2). "
                  "어떤 의미에서 BN은 ICS를 줄이지도 않을 수 있다(§2.2). 대신 BN은 손실과 기울기의 Lipschitz성(β-smoothness)을 개선해 최적화 지형을 매끄럽게 만든다 → 기울기가 더 예측 가능, 큰 학습률 가능(§3, Fig.4; 정리 4.1, 4.4). "
                  "ℓp 정규화 등 다른 방법도 비슷한 효과(§3.3). 교훈: 논문의 '방법'과 '설명'은 따로 검증된다.")
rest = s.cards([{"head": "Ioffe & Szegedy (2015)의 설명", "tone": "plain", "bullets": True,
                 "body": ["층 입력 분포가 학습 중 계속 바뀐다 = **internal covariate shift**", "BN이 이를 줄여서 학습이 빨라진다",
                          "→ 제목에 들어간 **가설**"]},
                {"head": "Santurkar et al. (2018)의 검증", "tone": "accent", "bullets": True,
                 "body": ["평균·분산 잡음을 일부러 넣은 **noisy BN**도 거의 같은 성능 (Fig.2)", "BN이 ICS를 줄이지 않을 수도 있다 (§2.2)",
                          "실제 효과: 손실 지형을 **매끄럽게** → 큰 학습률 가능 (§3)"]}],
               cols=2, body_size=16, head_size=18)
s.callout("논문의 **방법**과 **설명**은 따로 검증된다 — 방법은 살아남고, 설명은 바뀌었다.",
          Box(rest.x, rest.y + 0.15, rest.w, 0.8), kind="key", size=17)

# ============================================================ Part 7
d.part(7, "ResNet (2015)", "BN과 좋은 초기화로 수렴은 한다 — 그런데 더 깊게 쌓았더니 훈련 오류가 커졌다면?",
       notes="Part 7: He, Zhang, Ren, Sun (2015/CVPR 2016) Deep Residual Learning. 원 논문의 논리와 후속 해석을 구분해서 읽는다.")

d.paper("He et al. (2015)", "Deep Residual Learning for Image Recognition", "CVPR 2016, 770–778 · arXiv:1512.03385",
        "기울기 소실/폭발은 normalized 초기화와 BN으로 ‘대체로 해결’됐지만, 깊이를 늘리면 **훈련 오류가 커지는 degradation**이 나타난다.",
        "원하는 사상 H(x)를 직접 배우지 말고 **잔차 F(x) := H(x) − x**를 배운다. 항등이 최적이면 잔차를 0으로 미는 편이 쉽다.",
        "§1 (1쪽), §3.1, Fig.1 · Fig.4 · Table 2",
        url="arxiv.org/pdf/1512.03385",
        result="152층, ILSVRC-2015 top-5 **3.57%** (깊이가 다른 6개 앙상블) 1위.",
        notes="He et al. (2015). §1: 수십 층 망은 수렴은 한다. 그런데 깊이를 늘리면 정확도가 포화 후 급격히 나빠지고, 이는 과적합이 아니라 훈련 오류가 커지는 현상(Fig.1). "
              "얕은 망 + 항등 층으로 만든 해가 존재하므로 깊은 망의 훈련 오류가 더 높을 이유가 없는데 solver가 못 찾는다. 지름길 아이디어 자체는 Highway Networks(2015) 등 선행 연구가 있음(§2). "
              "출처: He et al. 2015 §1–4.")

s = d.slide("degradation: 깊을수록 ‘훈련’ 오류가 커진다", lead="과적합이 아니라 최적화 문제 — 그리고 원 논문은 기울기 소실 때문은 ‘아닐 것’이라고 썼다",
            stage="문제",
            notes="Fig.1: CIFAR-10 20층 vs 56층 plain — 훈련·테스트 오류 모두 56층이 높다. ImageNet Table 2: plain-34 top-1 28.54% > plain-18 27.94%. "
                  "§4.1: plain 망의 최적화 어려움은 '기울기 소실 때문은 아닐 것(unlikely to be caused by vanishing gradients)' — BN으로 순방향 신호의 분산이 0이 아니고 역방향 기울기 노름도 건강함을 확인. "
                  "대신 '지수적으로 낮은 수렴 속도'를 추측하고 원인 규명은 미래 과제로 남김. 2주차의 '표현 가능 ≠ 학습으로 찾음' 구분 그대로. "
                  "그림은 원문 Fig.1·Fig.6의 정성적 경향을 단순화한 개념도(실제 수치 아님).")
top, bot = s.area.top(2.85, gap=0.25)
s.image(A("week3/degradation.png"), top)
L, R = bot.cols(0.5, gap=0.4)
s.bullets(["CIFAR-10: 56층 plain의 **훈련** 오류 > 20층 (Fig.1)", "ImageNet: plain-34 **28.54%** > plain-18 27.94% (top-1)",
           ("과적합이면 훈련 오류는 낮아야 한다", 1)], L, size=16)
s.bullets(["깊은 망은 얕은 망 + 항등 층을 **흉내 낼 수 있다**", "그런데 solver가 그 해를 **못 찾는다**",
           "§4.1: BN 덕분에 기울기는 건강 → ==기울기 소실 때문은 아닐 것=="], R, size=16)

s = d.slide("잔차 학습: y = F(x) + x", lead="층 몇 개가 H(x) 대신 F(x) = H(x) − x를 배운다 — 지름길은 파라미터도 연산도 추가하지 않는다",
            stage="아이디어",
            notes="§3.1–3.2. y = F(x, {W_i}) + x (Eq.1), 차원이 다르면 y = F(x, {W_i}) + W_s x (Eq.2, projection). 2층 블록 F = W₂σ(W₁x). "
                  "§3.2: 'second nonlinearity after the addition' — 원 블록은 덧셈 뒤에 ReLU가 있다: y = ReLU(F(x) + x). 따라서 순수 항등 경로가 아니다. "
                  "원 논문의 동기(§1): 항등이 최적이라면 '잔차를 0으로 미는 것이 비선형 층 여러 개로 항등을 맞추는 것보다 쉽다'. "
                  "∂y/∂x = I + ∂F/∂x로 기울기가 직접 흐른다는 설명은 이 논문이 아니라 후속 논문 He et al. 2016 'Identity Mappings in Deep Residual Networks'(pre-activation 블록)의 논리 [원문 미확인 — 출처 언급만] → 다음 장. "
                  "학습 설정(§3.4): 합성곱 직후 BN, He 초기화, SGD 배치 256, 학습률 0.1, dropout 없음. 그림: 원문 Fig.2 기반 재구성.")
L, R = s.cols(0.4, gap=0.45)
s.image(A("week3/paper_resnet_block.png"), L)
s.formula(["y = F(x, {W_i}) + x        (Eq.1)", "y = F(x, {W_i}) + W_s x    (Eq.2)", "블록 출력 = ReLU(y)        (§3.2)"], Box(R.x, R.y, R.w, 1.6), size=18)
s.bullets(["**원 논문의 논리**: 항등이 최적이면 F → 0으로 미는 편이 여러 층으로 항등을 맞추기보다 **쉽다** (§1)",
           "지름길 = 추가 파라미터 · 연산 **0** (차원이 다를 때만 W_s)",
           "==주의== 원 블록은 **덧셈 뒤 ReLU** — 순수 항등 경로가 아니다 (§3.2)",
           "설정: 합성곱 직후 BN, SGD 배치 256, 학습률 0.1, dropout 없음"], Box(R.x, R.y + 1.8, R.w, R.h - 1.8), size=16)

s = d.slide("ResNet 결과", lead="같은 깊이 비교에서 plain은 깊어질수록 나빠지고 ResNet은 좋아진다 — 152층까지",
            stage="결과",
            notes="Table 2(ImageNet 검증 top-1, 10-crop): plain 18층 27.94%, plain 34층 28.54%; ResNet 18층 27.88%, ResNet 34층 25.03%. "
                  "Table 4(단일 모델 검증): ResNet-152 top-1 19.38%, top-5 4.49% — 이전 모든 앙상블보다 좋음. "
                  "Table 5(앙상블, 테스트 서버 top-5): VGG 7.32, GoogLeNet 6.66, PReLU-net 4.94, BN-inception 4.82, ResNet 3.57 — '서로 다른 깊이 6개 모델 앙상블(제출 시 152층은 2개뿐)', ILSVRC 2015 1위(§4.1). "
                  "CIFAR-10(Table 6): ResNet-20 8.75%, ResNet-110 6.43%, ResNet-1202 7.93%(110보다 나쁨 — 저자는 과적합으로 봄). "
                  "152층도 VGG-16/19보다 FLOPs가 적다(11.3B vs 15.3/19.6B). 데이터: ImageNet 2012(128만 학습, 5만 검증, 10만 테스트). 그림: 원문 Table 2 기반.")
L, R = s.cols(0.45, gap=0.45)
s.image(A("week3/paper_resnet_table2.png"), L)
s.table(["ImageNet top-5 (Table 5, 앙상블 · 테스트)", "오류"],
        [["VGG", "7.32%"], ["GoogLeNet", "6.66%"], ["PReLU-net", "4.94%"], ["BN-inception", "4.82%"],
         ["**ResNet** (6개 앙상블, 152층은 2개)", "**3.57%**"]], Box(R.x, R.y, R.w, 2.65), size=15, align="lc", highlight=(4,))
s.bullets(["단일 ResNet-152: top-5 **4.49%** (검증, Table 4)", "152층 FLOPs 11.3B < VGG-16 15.3B",
           "CIFAR-10: 110층 6.43% → 1202층 **7.93%** (과적합)"], Box(R.x, R.y + 2.85, R.w, R.h - 2.85), size=16)

s = d.slide("기울기 흐름 해석은 2016년 후속 연구의 것", lead="∂y/∂x = I + ∂F/∂x — 덧셈 뒤 ReLU가 없는 ‘순수 항등’ 지름길에서의 직관",
            stage="검증",
            notes="'ResNet은 기울기 소실을 해결했다'는 원 논문의 주장이 아니다 — 원 논문은 degradation을 기울기 소실과 구별한다(§4.1). "
                  "∂y/∂x = I + ∂F/∂x로 기울기가 직접 흐른다는 분석은 He et al. 2016 'Identity Mappings in Deep Residual Networks'(ECCV, pre-activation 블록)의 논리 [원문 미확인]. "
                  "스칼라 toy(검산 완료): y = x + F(x), F(x) = w·x면 ∂y/∂x = 1 + w. 20개 블록 연쇄 미분 (1 + w)^20: w = 0.01이면 1.22. plain y = w′x, w′ = 0.9면 0.9^20 = 0.12. "
                  "덧셈 뒤 ReLU·BN은 무시한 단순화. 그림: 직접 만든 40층 toy 실험(무작위 가중치, BN 없음) — 논문 결과 아님. "
                  "원형 Transformer의 Post-LN도 잔차 합 뒤에 LN이 있어 이 식이 그대로 성립하지 않는다(6주차).")
L, R = s.cols(0.55, gap=0.45)
s.image(A("week3/paper_toy_grad.png"), L)
s.formula(["y = x + w·x → ∂y/∂x = 1 + w", "잔차 20블록: (1.01)²⁰ = 1.22", "plain 20층: (0.9)²⁰ = 0.12"], Box(R.x, R.y, R.w, 1.6), size=18)
s.bullets(["원 논문(2015): degradation ≠ 기울기 소실, 동기는 **‘잔차 → 0이 쉽다’**",
           "후속(He et al. **2016**, Identity Mappings): 순수 항등 지름길 → **기울기가 직접** 흐른다",
           ("toy는 덧셈 뒤 ReLU · BN을 뺀 단순화", 1)], Box(R.x, R.y + 1.8, R.w, R.h - 1.8), size=16)

# ============================================================ Part 8
d.part(8, "LayerNorm (2016)과 정리", "배치에 기대지 않고 정규화하려면?",
       notes="Part 8: Ba, Kiros, Hinton (2016) Layer Normalization, 그리고 ILSVRC 연표로 이번 주를 정리한다.")

d.paper("Ba, Kiros & Hinton (2016)", "Layer Normalization", "arXiv:1607.06450 (NIPS 2016 Deep Learning Symposium)",
        "BatchNorm은 미니배치 크기에 의존하고, 길이가 제각각인 **RNN**에 적용하기 어렵다.",
        "한 층의 **모든 은닉 유닛**으로 평균·분산을 계산 — 훈련 사례마다 정규화 항이 다르고, 배치 크기 1에서도 학습·추론 계산이 같다.",
        "초록, §3 (반 쪽), §6.7 (CNN 한계 한 문단)",
        url="arxiv.org/pdf/1607.06450",
        result="주로 RNN 과제에서 효과. 단, 합성곱 망에서는 **BN이 더 좋았다** (§6.7).",
        notes="Ba, Kiros, Hinton (2016). 핵심 식(Eq.3): μ^l = (1/H)Σ a_i^l, σ^l = √((1/H)Σ (a_i^l − μ^l)²), H = 층의 은닉 유닛 수. 정규화 뒤 유닛별 gain g와 bias b를 비선형 전에 적용. "
              "원문 Eq.3에는 ε이 없다(구현에서는 보통 추가). RNN에서는 time step마다 별도 통계(§3.1). 실험: 이미지-문장 순위, QA, skip-thought, DRAW, 손글씨 생성, permutation-invariant MNIST(§6). "
              "§6.7: CNN에서는 LN이 정규화 없음보다 빠르지만 BN이 더 좋았다 — 가장자리 수용 영역 유닛은 거의 켜지지 않아 '유닛들의 기여가 비슷하다'는 가정이 깨짐. "
              "LN 논문 자체는 Transformer(2017) 이전이다. 출처: Ba et al. 2016 초록, §3, §6.7.")

s = d.slide("BatchNorm vs LayerNorm: 어느 축으로 평균을 내나", lead="BN은 채널마다 배치 × 위치 전체, LN은 샘플(토큰) 하나의 특징 전체",
            stage="계산",
            notes="BN(합성곱 층, Ioffe & Szegedy §3.2): 채널 c마다 (B, H, W) 전체로 통계, γ·β는 채널당 한 쌍 — 배치 크기와 다른 샘플에 의존. "
                  "LN(Ba et al. §3): 샘플 하나의 H개 은닉 유닛으로 통계 — 배치와 무관, 학습·추론 동일. 손계산: 토큰 하나 h = (1, 2, 3, 4)(d = 4) → μ = 2.5, σ = 1.118, "
                  "정규화 (−1.34, −0.45, 0.45, 1.34) — 배치 안 다른 토큰의 값과 무관(검산 완료). "
                  "Table 1(불변성): BN은 단일 사례 re-scaling에 불변이 아니고, LN은 단일 사례 re-scaling에 불변. §6.7: CNN에서는 BN이 더 좋았다 → 주 사용처 구분(CNN: BN, RNN·Transformer: LN). "
                  "Transformer 입력 (B, N, d)에서 LayerNorm(d)는 토큰마다 d개 값으로 평균·분산을 낸다(6주차). 그림: Ioffe §3.2 · Ba §3 기반 새 도식.")
top, bot = s.area.top(3.05, gap=0.2)
s.image(A("week3/paper_bn_cnn_axes.png"), top)
L, R = bot.cols(0.62, gap=0.4)
s.table(["구분", "BatchNorm (2015)", "LayerNorm (2016)"],
        [["통계 범위", "채널마다 **B × H × W**", "샘플(토큰) 하나의 **d개**"], ["배치 크기 영향", "받는다", "받지 않는다"],
         ["학습 · 추론", "다름 (모집단 통계)", "같음"], ["원 논문의 결과", "CNN에선 BN 우세 (§6.7)", "RNN 과제에서 효과"]],
        L, size=13, align="lcc", widths=[1.5, 2.2, 2.2])
s.formula(["LN: h = (1, 2, 3, 4)", "μ = 2.5, σ = 1.118", "→ (−1.34, −0.45, 0.45, 1.34)"], Box(R.x, R.y, R.w, 1.3), size=15)
s.textbox("배치의 다른 토큰과 무관 — Transformer의 LayerNorm(d)가 이것 (6주차)", Box(R.x, R.y + 1.4, R.w, R.h - 1.4),
          size=14, color=GRAY)

s = d.slide("ILSVRC: 오류는 줄고, 층은 깊어졌다", lead="28.2% → 3.57% (2010–2015) — 각 숫자 뒤의 조건까지 정확하게",
            stage="역사",
            notes="ILSVRC 분류 top-5 테스트 오류(Russakovsky et al. 2015 Table 5·8, He et al. 2015 Table 5): 2010 NEC 28.2%(SIFT·LBP + 비선형 코딩 + SVM), "
                  "2011 XRCE 25.8%(Fisher vector + 선형 SVM), 2012 SuperVision(AlexNet) 15.3% — 외부 데이터(ImageNet Fall 2011) 사용, 외부 데이터 없이 16.4%(16.42). 2위 26.2. "
                  "2013 Clarifai 11.7%(11.74; 외부 데이터 사용 시 11.2), 2014 GoogLeNet 6.66%(본문 반올림 6.7; 이전 자료의 6.67은 오기), 2위 VGG 7.32. 2015 MSRA ResNet 3.57% — 깊이가 다른 6개 앙상블(152층은 2개). "
                  "깊이: AlexNet 8층(합성곱 5 + FC 3), VGG 16–19층, ResNet 152층. GoogLeNet의 층수는 Szegedy et al. 2015 원문을 확인하지 못해 적지 않는다 [원문 미확인]. "
                  "Russakovsky §6: 2012→2014 '16.4% → 6.7%, 2.4배'(외부 데이터 없는 기준). 사람 주석자 A1 추정 5.1%(Table 9).")
L, R = s.cols(0.58, gap=0.45)
s.image(A("week3/ilsvrc.png"), L)
s.bullets(["2010–2011: 손으로 설계한 특징 + SVM", "2012 AlexNet **8층**: 15.3%†", ("외부 데이터 없이 **16.4%**, 7개 앙상블", 1),
           "2014 GoogLeNet **6.66%**, VGG 16–19층 7.3%", "2015 ResNet **152층**: 3.57%", ("깊이가 다른 **6개 앙상블**", 1),
           "참고: 사람 추정 5.1% (Russakovsky Table 9)"], R, size=16)

s = d.slide("CNN의 가정: 얻는 것과 대가 — 그리고 Attention으로", lead="모든 구조적 가정은 이득과 제약을 함께 가져온다",
            stage="정리",
            notes="원자료의 정리 표. 국소 연결·가중치 공유·수용 영역·이동 등변성 — 각각 무엇을 얻게 해 주고 어떤 제약을 만드는지. "
                  "CNN에서 어떤 위치를 볼지(K×K 이웃)와 비중(필터)은 학습 후 고정되고 입력과 무관하다. 입력마다 '어디를 얼마나 볼지'를 계산한다면? — 5주차 Attention. "
                  "그 전에 다음 주는 또 다른 데이터 구조 — 순서가 있고 길이가 제각각인 언어. "
                  "또 Residual(2015)과 LayerNorm(2016)은 '무언가를 알아내는 부품'이 아니라 깊은 계산을 이어 붙이는 조건으로 Transformer(2017)에 그대로 들어간다.")
s.table(["개념", "얻는 것", "함께 생기는 제약"],
        [["Local connection", "가까운 공간 구조 활용 (Fukushima, LeCun)", "한 층에서 멀리 떨어진 위치가 직접 만나지 않는다"],
         ["Weight sharing", "파라미터 절감 (2억 → 1,792)", "위치마다 독립된 필터를 쓰지 않는다"],
         ["Receptive field", "층을 쌓아 넓게 통합 (VGG 3×3)", "넓은 의존 관계를 만들 때 경로가 길어진다"],
         ["Translation equivariance", "입력 이동에 대응하는 특징 이동", "경계 · padding · stride · pooling에 따라 달라진다"]],
        Box(s.area.x, s.area.y, s.area.w, 3.1), widths=[2.6, 3.9, 4.9], size=15)
s.image(A("week3/bridge_sketch.png"), Box(s.area.x, s.area.y + 3.25, s.area.w, 1.25))
s.callout("CNN은 참조할 위치와 비중을 **미리 정한다** — 입력에 따라 **계산**하면? → 5주차 Attention. 그 전에 다음 주는 **순서**가 있는 언어.",
          Box(s.area.x, s.area.y + 4.6, s.area.w, 0.75), kind="tip", size=15)

# ============================================================ 마무리
d.summary(["CNN = **국소 연결 + 가중치 공유 + 계층**: Neocognitron(1980) 구조 → LeCun(1989) **역전파 학습** → LeNet-5(1998)",
           "O = ⌊(N − K + 2P)/S⌋ + 1, params = C_out·C_in·K² + C_out — 2억 → **1,792**",
           "SVM(1995)의 새 기여는 **soft margin** — 마진(1965) · 커널(1992)은 그 전부터",
           "깊이의 벽: 층별 사전학습(2006) → 초기화 · **ReLU**로 사전학습 없이 (2010–11)",
           "AlexNet **15.3%** = 7개 앙상블 + 외부 데이터 (없이 16.4%) — 데이터 · GPU · ReLU · 규제가 함께",
           "ResNet: degradation을 **잔차 학습**으로 · BN(채널마다 B×H×W) vs **LN**(토큰마다 d)"],
          notes="오늘의 요약. 각 줄을 학생이 자기 말로 다시 설명하게 한다. 각 숫자의 출처는 해당 슬라이드 노트(week3.md)에 있다.")

d.quiz("셀프 체크", [("입력 64×64, 필터 5×5, padding 2, stride 2일 때 출력 크기는?", "⌊(64 − 5 + 4)/2⌋ + 1 = ⌊31.5⌋ + 1 = 32"),
                   ("입력 채널 16, 출력 채널 32, 3×3 합성곱의 파라미터 수는?", "32 × 16 × 9 + 32 = 4,640"),
                   ("LeNet-5의 S2 층은 max pooling인가? 출력층은 softmax인가?",
                    "둘 다 아니다. S2는 2×2 합에 학습 계수·bias를 곱하고 더한 뒤 sigmoid를 거치는 평균형 서브샘플링(맵당 파라미터 2개), 출력은 유클리드 RBF(LeCun 1998 §II.B, Eq.7)"),
                   ("‘AlexNet은 120만 장으로 학습한 CNN 하나로 15.3%를 냈다’ — 무엇이 틀렸나?",
                    "15.3%는 7개 CNN 앙상블이고 그중 2개는 ImageNet Fall 2011(약 1,500만 장)로 사전학습했다. 외부 데이터 없는 공식 결과는 16.4%, 단일 CNN은 검증 18.2%(Krizhevsky Table 2)"),
                   ("ResNet 원 논문은 깊은 plain 망이 학습되지 않는 이유를 기울기 소실이라고 했나?",
                    "아니다. BN으로 순·역방향 신호가 건강함을 확인하고 '기울기 소실 때문은 아닐 것'이라 했다(§4.1). 동기는 '잔차를 0으로 미는 것이 항등을 맞추기보다 쉽다'. I + ∂F/∂x 기울기 해석은 2016 후속 논문")],
       notes="Q1–Q2는 계산, Q3–Q5는 원문 확인. 출처: week3.md 검산 목록, LeCun 1998 §II.B, Krizhevsky 2012 Table 2, He 2015 §4.1.")

d.misconceptions([["“Neocognitron이 최초의 역전파 CNN이다”", "구조는 선구적이지만 학습은 **비지도** 경쟁 학습. 역전파로 커널을 학습한 것은 LeCun 1989"],
                  ["“LeNet은 max pooling + softmax를 썼다”", "1989 망은 pooling 층 없이 **stride 2**, LeNet-5는 **평균형 서브샘플링** + **RBF** 출력"],
                  ["“마진 최대화·커널 트릭은 1995년 발명”", "마진 1965, 커널 SVM 1992. 1995년의 기여는 **soft margin**과 체계적 실험"],
                  ["“2006 DBN은 사전학습 후 역전파로 미세 조정”", "미세 조정은 **up-down** 알고리즘. 역전파 미세 조정은 Hinton & Salakhutdinov 2006 · Bengio 2007 계열"],
                  ["“AlexNet 15.3% = 단일 모델 · 120만 장”", "**7개 앙상블** + 외부 데이터 사전학습 2개. 외부 데이터 없이 16.4%"],
                  ["“ResNet은 기울기 소실을 해결했다”", "원 논문은 기울기 소실이 원인이 **아닐 것**이라 했다. 기울기 해석은 2016 후속 연구"],
                  ["“BN은 internal covariate shift를 줄여서 효과”", "원 논문의 **가설**. Santurkar 2018: 효과는 손실 지형 평활화"]],
                 notes="출처: week3.md 각 논문의 '흔한 오해 바로잡기' 항목.")

d.homework([("LeNet-5 파라미터 재현 (LeCun 1998 §II.B, Table I)",
             "Table I의 C3 연결표를 보고 C3의 1,516을 직접 세어 본다. 이어 C1–F6 파라미터 합 60,000과 연결 수 340,908을 표로 재현해 제출한다."),
            ("AlexNet Table 2 읽기 (Krizhevsky 2012 §6)",
             "Table 2의 다섯 행이 각각 무엇을 바꾼 결과인지(모델 수 · 외부 데이터 · 검증/테스트) 한 줄씩 적고, ‘15.3%’를 정확하게 설명하는 한 문장을 제출한다."),
            ("ResNet §1 · §4.1과 Santurkar Fig.2 읽기",
             "He et al.이 degradation의 원인을 무엇이라 ‘하지 않았는지’, Santurkar et al.이 BN의 어떤 설명을 반박했는지 각각 3문장으로 요약한다.")],
           lab="import torch, torch.nn as nn\n"
               "n = lambda m: sum(p.numel() for p in m.parameters())\n"
               "x = torch.randn(8, 3, 32, 32)    # (B, C, H, W)\n"
               "conv = nn.Conv2d(3, 64, 3, padding=1)\n"
               "print(conv(x).shape)   # (8, 64, 32, 32)\n"
               "print(n(conv))         # 1792\n\n"
               "c1 = nn.Conv2d(1, 6, 5)          # LeNet-5 C1\n"
               "print(n(c1))           # 156\n\n"
               "bn = nn.BatchNorm2d(64)  # 채널마다 (B,H,W)\n"
               "ln = nn.LayerNorm(64)    # 마지막 축 d\n"
               "print(bn.weight.shape) # (64,) 채널당 γ",
           notes="오른쪽 코드는 [도구] 확인용 — 주석을 가리고 먼저 손으로 계산한 뒤 실행해 맞춰 본다. 과제는 논문의 표와 절을 직접 읽고 제출물이 분명한 질문으로 준다.")

d.references([["Fukushima (1980). Neocognitron. Biological Cybernetics 36", "초록, §2 (Fig.2–3), §5 첫 문단"],
              ["LeCun et al. (1989). Backpropagation Applied to Handwritten Zip Code Recognition. Neural Comp. 1(4)", "§3.2–3.3, §5"],
              ["LeCun, Bottou, Bengio, Haffner (1998). Gradient-Based Learning Applied to Document Recognition", "§II.A–B, Table I, Fig.9"],
              ["Cortes & Vapnik (1995). Support-Vector Networks. Machine Learning 20", "p.275–276, §3, §6.2 Table 1–2"],
              ["Hinton, Osindero & Teh (2006). A Fast Learning Algorithm for Deep Belief Nets", "초록, §1, §6.1"],
              ["Glorot & Bengio (2010) · Nair & Hinton (2010) · Glorot, Bordes & Bengio (2011)", "§3.1·§4.2 · 초록 · Table 1"],
              ["Krizhevsky, Sutskever & Hinton (2012). ImageNet Classification with Deep CNNs", "§3.1, §4, Table 2"],
              ["Simonyan & Zisserman (2014). Very Deep Convolutional Networks", "§2.3, Table 7"],
              ["Ioffe & Szegedy (2015). Batch Normalization · Santurkar et al. (2018). How Does BN Help Optimization?", "§2, Alg.1, §3.2 · 초록, Fig.2"],
              ["He, Zhang, Ren & Sun (2015). Deep Residual Learning for Image Recognition", "§1, §3.1–3.2, §4.1, Table 2·5"],
              ["Ba, Kiros & Hinton (2016). Layer Normalization", "초록, §3, §6.7"],
              ["Russakovsky et al. (2015). ImageNet Large Scale Visual Recognition Challenge. IJCV 115", "Table 5, 8, 9"]],
             notes="원문은 표에 적은 절과 그림만 먼저 읽는다. 원문 미확인으로 출처 언급만 한 것: Szegedy et al. 2015(GoogLeNet 층수), He et al. 2016 Identity Mappings, "
                   "Hinton & Salakhutdinov 2006, Bengio et al. 2007. 읽은 판본 URL은 build/research/papers/week3.md에 있다.")

d.handoff(["**구조적 가정**(국소성 · 공유)으로 큰 입력을 효율적으로", "데이터 · GPU · ReLU · **BN · Residual · LN**으로 깊은 모델을 학습"],
          ["**언어**는 격자가 아니라 순서, 길이도 제각각", "“그 책은 … (20단어 뒤) … 재미있었다” — **먼 단어**를 어떻게 기억할까?"],
          ["**순서를 어떻게 표현하고,**", "**먼 정보를 어떻게 기억할까?**", "RNN · LSTM · Seq2Seq"],
          notes="다음 주(Week 4, 시퀀스와 기억): 문장을 숫자로 바꾸는 법(토큰, 임베딩)부터, 순서를 따라 상태를 전달하는 RNN과 LSTM, 번역을 위한 Seq2Seq까지. "
                "오늘 본 LayerNorm은 RNN을 위해 나왔다는 점을 기억해 두자.")

d.save(OUT)
print("saved", OUT, d.n + 2, "slides")
