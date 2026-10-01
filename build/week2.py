"""Week 2 — Perceptron에서 MLP로: 직선으로 안 되는 문제는?"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from deckkit import *  # noqa

A = lambda p: os.path.join(HERE, "assets", p)
OUT = os.path.join(HERE, "..", "lectures", "week02_perceptron_to_mlp.pptx")

d = Deck(2, "Perceptron에서 MLP로", date="2026-10-12")

# ============================================================ 도입
d.question("직선으로 안 되는 문제는?", "1958–1986 · Perceptron · XOR · MLP · 역전파 · Softmax",
           notes="지난주의 선형 모델에 '예/아니오'를 붙인 Perceptron에서 출발한다. 그런데 직선 하나로는 절대 나눌 수 없는 문제가 있다. "
                 "그 벽을 넘는 두 가지 열쇠 — 비선형 은닉층과 역전파 — 가 오늘의 주제다.")

d.bridge(["텐서와 shape", "모델 ŷ = wx + b, 손실(MSE)", "경사하강법으로 **규칙 y = 2x + 1**을 스스로 찾음"],
         ["출력이 **예/아니오**(분류)라면?", "가중합 + 임계값 뉴런 **하나**로 모든 규칙을 배울 수 있을까?"],
         ["**직선으로 안 되는 문제는?**", "그 문제를 풀려면 무엇을 바꿔야 하나?"],
         notes="지난주 복습 3줄: 텐서, 손실, 경사하강법. 이번 주는 출력을 0/1로 바꾸는 순간 생기는 일에서 출발한다.")

d.roadmap(["Perceptron (1958): 분류를 배우는 뉴런", "XOR의 벽 (1969): 직선의 한계",
           "MLP: 층을 쌓아 새 좌표 만들기", "역전파 (1986): 은닉층은 무엇을 기준으로 배우나",
           "확률로 답하기: Softmax와 Cross-entropy"],
          ["Perceptron의 **결정 경계**가 직선인 이유를 설명한다",
           "XOR이 직선 하나로 **불가능함**을 부등식으로 보인다",
           "**비선형 활성화**가 없으면 층을 쌓아도 소용없는 이유를 말한다",
           "작은 MLP에서 **역전파**를 손으로 계산한다",
           "Softmax와 **Cross-entropy**를 숫자로 계산한다"])

_terms = [["분류", "입력을 정해진 범주 중 하나로 고르는 문제", "스팸 / 정상"],
          ["결정 경계", "예측이 0과 1로 바뀌는 경계선", "지도 위의 국경선"],
          ["선형 분리", "직선(초평면) 하나로 두 부류를 나눌 수 있음", "자 하나로 나누기"],
          ["활성화 함수", "층 사이에 넣는 비선형 함수 (ReLU 등)", "직선을 구부리는 관절"],
          ["은닉층", "입력과 출력 사이의 중간 표현", "문제를 풀기 쉬운 새 좌표"],
          ["역전파", "연쇄법칙으로 모든 기울기를 한 번에 계산", "책임을 거꾸로 나누기"],
          ["Softmax", "점수들을 합이 1인 양수 비중으로", "득표수 → 득표율"],
          ["Cross-entropy", "정답 확률의 −log — 분류용 손실", "확신하고 틀리면 큰 벌점"]]
s = d.slide("오늘의 새 용어", lead="낯선 단어를 먼저 한 번 보고 시작한다", stage="도입",
            notes="오늘 처음 나오는 용어들. 외울 필요는 없고, 설명 중 막히면 이 표로 돌아온다. "
                  + " / ".join(f"{r[0]}: {r[1]}" for r in _terms)
                  + " 아래 줄은 오늘 이야기의 순서 — 용어가 등장하는 차례와 같다.")
s.table(["용어", "한 줄 뜻", "비유 · 예"], _terms, Box(s.area.x, s.area.y, s.area.w, 4.0), widths=[2.2, 5.2, 4.9], size=17)
s.callout("오늘의 흐름: **분류** → **결정 경계**가 직선 → **선형 분리**가 안 되는 XOR → **은닉층** + **활성화 함수** → "
          "**역전파**로 학습 → 출력은 **Softmax**, 손실은 **Cross-entropy**",
          Box(s.area.x, s.area.y + 4.25, s.area.w, 1.0), kind="tip", size=16)

# ============================================================ Part 1
d.part(1, "Perceptron: 분류를 배우는 뉴런 (1958)", "지난주의 가중합에 ‘예/아니오’를 붙이면?")

s = d.slide("회귀에서 분류로", lead="출력이 숫자가 아니라 ‘범주’라면 — 가중합 뒤에 판정을 붙인다", stage="문제",
            notes="지난주 문제(점수 예측)는 출력이 연속된 숫자인 회귀였다. 스팸 판별, 합격/불합격처럼 출력이 범주인 문제는 분류다. "
                  "가장 단순한 방법: 지난주처럼 가중합 z를 계산하고, z가 0 이상이면 1, 아니면 0이라고 판정한다. "
                  "이것이 1958년 Rosenblatt의 Perceptron의 핵심 계산이다.")
rest = s.cards([{"head": "회귀 (1주차)", "tone": "plain",
                 "body": ["출력: 연속된 숫자", "예: 공부 시간 → **점수 7.0**", "손실: MSE"]},
                {"head": "분류 (2주차)",
                 "body": ["출력: 범주 (0 또는 1, 혹은 여러 개 중 하나)", "예: 메일 → **스팸(1) / 정상(0)**",
                          "손실: 틀린 개수? 확률? → Part 5"]}], cols=2, body_size=18, head_size=20)
s.formula("z = w · x + b   →   ŷ = 1 (z ≥ 0),  0 (z < 0)", Box(rest.x, rest.y + 0.1, rest.w, 1.1), size=26)
s.bullets(["앞부분 w·x + b는 **1주차 선형 모델 그대로**, 뒤에 ‘0 이상이면 1’이라는 **판정**만 붙였다",
           "예: 공부 시간 x = 3, w = 1, b = −2 → z = 1 ≥ 0 → ŷ = 1 (합격)",
           "이 단순한 판정이 무엇을 할 수 있고 **무엇을 못 하는지**가 오늘의 이야기"],
          Box(rest.x, rest.y + 1.45, rest.w, rest.h - 1.45), size=18)

s = d.slide("Perceptron의 구조", lead="가중합 → 계단 함수 → 0 또는 1. McCulloch–Pitts와 다른 점은 ‘학습 규칙’", stage="아이디어",
            notes="입력마다 가중치를 곱해 더하고 편향 b를 더한 z를 계단 함수에 넣는다. 구조는 1943년 McCulloch–Pitts 뉴런과 거의 같다. "
                  "결정적 차이는 가중치를 사람이 정하지 않고 '틀리면 고친다'는 학습 규칙으로 데이터에서 찾는다는 것. "
                  "편향 b는 항상 1인 입력에 붙은 가중치로 볼 수 있다(그림의 아래 입력).")
L, R = s.cols(0.55)
s.image(A("week2/perceptron.png"), L)
s.bullets(["**z = w1·x1 + w2·x2 + b** (가중합)", "**ŷ = 1[z ≥ 0]** (계단 함수)",
           "b = 항상 1인 입력에 붙은 가중치", "1943 McCulloch–Pitts 뉴런과 계산은 같다",
           "다른 점: w, b를 **데이터로 학습**", ("Rosenblatt (1958)", 1)], R)

s = d.slide("결정 경계는 직선이다", lead="w·x + b = 0 인 점들이 경계 — 2차원 입력이면 항상 직선", stage="계산",
            notes="z = 0이 되는 점들의 집합이 결정 경계다. 입력이 2개면 w1x1 + w2x2 + b = 0은 직선의 방정식이다. "
                  "w 벡터는 경계에 수직이고, w가 가리키는 쪽이 ŷ=1 영역이다. 입력이 3개면 평면, 그 이상이면 초평면. "
                  "즉 Perceptron은 입력 공간을 '평평한 칼' 하나로 둘로 자르는 모델이다. 이 사실이 Part 2의 벽이 된다.")
L, R = s.cols(0.5)
s.image(A("week2/halfplane.png"), L)
s.bullets(["예: w = (1, 1), b = −1.5", ("경계: x1 + x2 − 1.5 = 0 (직선)", 1),
           "w는 경계에 **수직**, w 쪽이 ŷ = 1", "입력 3개 → 평면, 더 많으면 **초평면**",
           "Perceptron = 입력 공간을 **평평한 칼 하나**로 자르는 모델"], R)

s = d.slide("Perceptron 학습 규칙", lead="맞으면 그대로, 틀리면 틀린 쪽으로 w를 조금 옮긴다", stage="계산",
            notes="규칙: w ← w + η(y − ŷ)x, b ← b + η(y − ŷ). 맞히면 y − ŷ = 0이라 변화 없음. "
                  "1이어야 하는데 0이라고 했으면(y−ŷ=+1) w에 x를 더해 z를 키운다. 0이어야 하는데 1이면 x를 빼서 z를 줄인다. "
                  "예: w=(0,0), b=0, 입력 (1,1), 정답 1인데 z=0 → ŷ=1로 맞음. 입력 (0,1) 정답 0인데 ŷ=1 → w=(0,−1), b=−1(η=1). "
                  "지난주 경사하강법과 모양이 비슷하지만, 계단 함수는 미분할 수 없어서 기울기 대신 이 규칙을 쓴다.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("w ← w + η · (y − ŷ) · x        b ← b + η · (y − ŷ)", top, size=22)
L, R = bot.cols(0.5, gap=0.4)
s.table(["상황", "y − ŷ", "변화"], [["맞힘", "0", "그대로"], ["1인데 0이라 함", "+1", "w += ηx  → z 커짐"],
                                    ["0인데 1이라 함", "−1", "w −= ηx  → z 작아짐"]], Box(L.x, L.y, L.w, 2.0),
        size=15, align="lcl")
s.callout("계단 함수는 미분할 수 없다(기울기가 0 아니면 정의 안 됨) → 경사하강법 대신 이 **오류 교정 규칙**을 쓴다.",
          Box(L.x, L.y + 2.3, L.w, 1.3), kind="tip", size=15)
rest = s.card(R, "숫자로 확인 (η = 1)", ["시작 w = (0, 0), b = 0", "입력 (0, 1), 정답 0 → z = 0 → ŷ = 1 ✘",
                                     "y − ŷ = −1 → w = (0, −1), b = −1", "다시 z = −1 − 1 = −2 → ŷ = 0 ✔"],
              tone="accent", bullets=True, fit_h=True)
s.callout("틀린 쪽으로 w가 **x만큼** 움직인다 — 1주차 경사하강법의 ‘틀린 만큼 고친다’와 같은 정신",
          Box(rest.x, rest.y, rest.w, min(1.2, rest.h)), kind="tip", size=15)

s = d.slide("AND를 배우는 과정", lead="선형으로 나뉘는 문제라면 규칙을 반복하는 것만으로 경계를 찾는다", stage="검증",
            notes="AND 데이터 4점에 규칙을 반복 적용하면 몇 번의 갱신 끝에 네 점을 모두 맞히는 직선을 찾는다. "
                  "Perceptron 수렴 정리: 데이터가 선형 분리 가능하면 유한 번의 갱신 안에 분리하는 경계를 찾는다. "
                  "거꾸로 말하면, 선형 분리가 불가능하면 이 규칙은 끝없이 흔들린다. 다음 파트에서 그런 문제를 만난다.")
L, R = s.cols(0.68)
s.image(A("week2/perceptron_train.png"), L)
s.bullets(["갱신할 때마다 경계선이 이동", "몇 번 만에 AND의 네 점을 모두 맞힘",
           "**수렴 정리**: 선형 분리 **가능**하면 유한 번에 찾는다", ("(Rosenblatt 수렴 정리)", 1),
           ("불가능하면? → 규칙이 끝없이 흔들린다", 1), "OR도 같은 방식으로 학습된다"], R)

# ============================================================ Part 2
d.part(2, "XOR의 벽 (1969)", "직선 하나로는 절대 나눌 수 없는 문제가 있다면?")

s = d.slide("AND · OR · XOR", lead="XOR은 ‘둘 중 하나만 1일 때 1’ — 양성 두 점이 대각선으로 엇갈린다", stage="문제",
            notes="AND와 OR은 직선 하나로 1 영역과 0 영역을 나눌 수 있다. XOR은 (0,1)과 (1,0)이 1, (0,0)과 (1,1)이 0이라 "
                  "같은 부류가 대각선으로 엇갈려 있다. 어떤 직선을 그어도 네 점 중 적어도 하나는 틀린다. 직접 그어 보자.")
top, bot = s.area.top(3.1, gap=0.25)
s.image(A("week2/and_or_xor.png"), top)
s.table(["x1", "x2", "AND", "OR", "XOR"], [["0", "0", "0", "0", "**0**"], ["0", "1", "0", "1", "**1**"],
                                          ["1", "0", "0", "1", "**1**"], ["1", "1", "1", "1", "**0**"]],
        Box(bot.x + 2.5, bot.y, bot.w - 5.0, bot.h), size=14, align="ccccc", first_col_bold=False)

s = d.slide("XOR이 직선으로 불가능한 이유", lead="네 점이 요구하는 조건을 적으면 서로 모순된다", stage="계산",
            notes="ŷ = 1[w1x1 + w2x2 + b ≥ 0]이 XOR을 맞히려면 네 부등식이 동시에 성립해야 한다. "
                  "(0,0)→0: b < 0. (0,1)→1: w2 + b ≥ 0. (1,0)→1: w1 + b ≥ 0. (1,1)→0: w1 + w2 + b < 0. "
                  "가운데 두 식을 더하면 w1 + w2 + 2b ≥ 0, 즉 w1 + w2 + b ≥ −b > 0 (b<0이므로). 넷째 식과 모순. "
                  "따라서 어떤 w, b로도 불가능하다 — 학습을 더 오래 해서 해결되는 문제가 아니라, 모델이 표현할 수 없는 함수다.")
L, R = Box(s.area.x, s.area.y, s.area.w, s.area.h - 0.8).cols(0.48, gap=0.4)
s.table(["입력", "정답", "필요한 조건"], [["(0, 0)", "0", "b < 0"], ["(0, 1)", "1", "w2 + b ≥ 0"],
                                     ["(1, 0)", "1", "w1 + b ≥ 0"], ["(1, 1)", "0", "w1 + w2 + b < 0"]],
        Box(L.x, L.y, L.w, 3.2), size=18, align="ccl", widths=[1.0, 0.7, 1.8])
s.card(R, "모순 찾기", ["가운데 두 식을 더하면", "w1 + w2 + 2b ≥ 0", "→ w1 + w2 + b ≥ −b",
                     "b < 0 이므로 −b > 0", "→ w1 + w2 + b **> 0**", "하지만 넷째 조건은 **< 0** → ==모순=="],
       tone="accent", bullets=False, body_size=18, head_size=18, fit_h=True)
s.takeaway("학습을 오래 한다고 풀리지 않는다 — 이 모델이 ‘표현할 수 없는’ 함수다")  # 마지막에: deckkit 자동 내림 계산에 포함되도록

s = d.slide("실험: 직선의 최선은 3/4", lead="선형 경계는 기껏해야 세 점, 비선형 경계는 네 점 모두", stage="검증",
            notes="왼쪽: w1=w2=1, b=−0.5인 직선(OR 경계)은 (1,1)을 틀려 3/4. 어떤 직선도 4/4는 안 된다. "
                  "오른쪽: 뒤에서 만들 비선형 함수 ReLU(s) − 2·ReLU(s−1) (s = x1+x2)는 네 점을 모두 맞힌다. "
                  "이 비선형 해가 어디서 왔는지가 Part 3의 주제다.")
L, R = s.cols(0.62)
s.image(A("week2/xor_experiment.png"), L)
s.bullets(["왼쪽: 직선 w = (1, 1), b = −0.5", ("(1, 1)을 틀림 → **3/4**", 1),
           "오른쪽: 비선형 함수 ReLU(s) − 2·ReLU(s − 1)", ("s = x1 + x2", 1),
           ("ReLU(z) = max(0, z): 음수를 0으로 (Part 3에서 자세히)", 1), ("네 점 모두 → **4/4**", 1),
           "이 함수는 어디서 왔나? → Part 3"], R, size=16)

s = d.slide("1969 『Perceptrons』와 그 이후", lead="단층 Perceptron의 한계가 분석되었다 — 하지만 ‘AI 겨울’의 원인은 하나가 아니다",
            stage="역사",
            notes="1969년 Minsky와 Papert의 책 『Perceptrons』는 단층 Perceptron이 parity(XOR의 일반화)나 연결성 같은 성질을 다루기 어렵다는 것을 수학적으로 분석했다. "
                  "이후 신경망 연구가 위축된 시기가 있었지만, 그 원인을 'XOR 하나'로 말하는 것은 과도한 단순화다 — 연산 능력, 과도한 기대, 투자, 평가 방식 등 여러 맥락이 얽혀 있다. "
                  "같은 시기 사람이 지식과 규칙을 직접 작성하는 기호·지식 기반 AI(전문가 시스템: MYCIN, R1/XCON 등)도 발전했다. 규칙은 점검하기 쉽지만 예외를 계속 유지·보수하는 비용이 컸다.")
s.timeline([(1958, "Perceptron", "가중치를 학습하는 단층 뉴런"),
            (1969, "『Perceptrons』", "Minsky & Papert: 단층의 표현 한계(parity (홀짝) 등) 분석"),
            ("1970s–80s", "규칙 기반 AI", "전문가 시스템(MYCIN, R1/XCON) — 사람이 지식을 규칙으로 작성"),
            (1986, "역전파 확산", "다층 신경망의 은닉 표현 학습 (→ Part 4)")],
           Box(s.area.x, s.area.y, s.area.w, 3.2), highlight=[1], body_size=15)
s.callout("“AI 겨울은 XOR 하나 때문?” → 아니다. 기술·연산·기대·투자·평가 등 여러 맥락을 분리해서 본다. "
          "이 수업은 역사적 인과보다 ‘어떤 표현이 어떤 문제를 풀 수 있는가’를 직접 확인하는 데 집중한다.",
          Box(s.area.x, s.area.y + 3.45, s.area.w, 1.2), kind="warn", size=15)

# ============================================================ Part 3
d.part(3, "MLP: 층을 쌓아 새 좌표 만들기", "입력을 다른 좌표로 옮기면, 직선 하나로 나뉘지 않을까?")

s = d.slide("그런데 선형층만 쌓으면?", lead="선형 변환을 여러 번 합성해도 결국 선형 변환 하나 — 직선은 직선이다", stage="문제",
            notes="Part 3의 출발: 층을 쌓으면 될까? 은닉층을 두 개 쌓아도 사이에 비선형 함수가 없으면 "
                  "(xW1 + b1)W2 + b2 = x(W1W2) + (b1W2 + b2)로 하나의 선형 변환이 된다. "
                  "즉 층을 몇 개 쌓든 결정 경계는 여전히 직선이다. 원자료: bias를 포함한 affine 변환은 여러 번 합쳐도 하나의 affine 변환. "
                  "PyTorch로 두 Linear 층의 출력이 하나의 합친 행렬 결과와 완전히 같은지 확인할 수 있다(allclose = True). "
                  "아래 숫자 예: 은닉 1개짜리 두 층을 합치면 W' = [[2],[2]], b' = −1 → 경계 x1 + x2 = 0.5, Part 2에서 3/4밖에 못 맞힌 OR 직선 그대로다.")
top, bot = s.area.top(1.1, gap=0.3)
s.formula(["(x W1 + b1) W2 + b2  =  x (W1 W2) + (b1 W2 + b2)", "=  x W' + b'    ← 선형층 하나와 같다"], top, size=21)
L, R = bot.cols(0.55)
s.code("import torch\n"
       "l1 = torch.nn.Linear(2, 3)\n"
       "l2 = torch.nn.Linear(3, 1)\n"
       "W = l1.weight.T @ l2.weight.T      # 합친 행렬\n"
       "b = l1.bias @ l2.weight.T + l2.bias\n"
       "x = torch.randn(5, 2)\n"
       "print(torch.allclose(l2(l1(x)), x @ W + b))\n"
       "# True", L, size=13)
cb = s.last_code_box
s.bullets(["층을 100개 쌓아도 **직선 하나**", "해결책: 층 사이에 **비선형 함수**", ("= 활성화 함수 (activation)", 1),
           "직선을 ‘구부리는 관절’ 역할 → 다음 장"], R)
s.card(Box(bot.x, cb.b + 0.25, bot.w, bot.b - cb.b - 0.25), "숫자로 확인: 두 층을 합쳐도 Part 2의 직선 그대로",
       ["W1 = [[1], [1]], b1 = −0.5 (2 → 1),  W2 = [[2]], b2 = 0 (1 → 1)   →   W' = W1 W2 = [[2], [2]],  b' = b1 W2 + b2 = −1",
        "경계 2·x1 + 2·x2 − 1 = 0, 즉 x1 + x2 = 0.5 — ‘실험’ 장의 OR 직선과 같다 → XOR은 여전히 **3/4**"],
       tone="accent", bullets=False, body_size=15, head_size=16, fit_h=True)

s = d.slide("활성화 함수", lead="층 사이의 비선형 함수 — 모양보다 ‘기울기가 어떻게 전달되나’가 중요", stage="아이디어",
            notes="sigmoid σ(z)=1/(1+e^−z): 0~1로 눌러 준다. 도함수 최대 0.25. tanh: −1~1, 도함수 최대 1. "
                  "ReLU(z)=max(0, z): 양수는 그대로, 음수는 0. 기울기는 양수 구간 1, 음수 구간 0. 계산이 가볍다. "
                  "오른쪽 그래프(도함수)는 역전파 때 곱해지는 값이다. sigmoid는 최대 0.25라 층이 깊어지면 기울기가 급격히 줄어든다 — 다음 주의 문제. "
                  "원자료 주의: 'ReLU면 기울기 소실이 모두 사라진다'고 말하지 않는다. 초기화·학습률·입력 분포에 따라 달라진다. "
                  "다음 두 장에서는 ReLU만 쓴다: 먼저 ReLU 두 개로 새 좌표를 만들고, 그 좌표에서 XOR이 직선으로 나뉘는 것을 본다.")
top, bot = s.area.top(3.2, gap=0.25)
s.image(A("week2/activations.png"), top)
s.table(["함수", "식", "출력 범위", "기울기"], [["sigmoid", "1 / (1 + e^−z)", "0 ~ 1", "최대 0.25"],
                                          ["tanh", "(e^z − e^−z)/(e^z + e^−z)", "−1 ~ 1", "최대 1"],
                                          ["ReLU", "max(0, z)", "0 ~ ∞", "0 또는 1"]], bot, size=14, align="cccc")

s = d.slide("아이디어: 좌표를 바꾸면 직선으로 나뉜다", lead="은닉층 = 문제를 풀기 쉬운 새 좌표를 만드는 층", stage="아이디어",
            notes="앞 장의 ReLU를 바로 써 본다. 원래 공간에서는 안 되지만, 좌표를 바꾸면 된다. h1 = ReLU(x1 + x2), h2 = ReLU(x1 + x2 − 1)로 바꾸면 "
                  "(0,0)→(0,0), (0,1)과 (1,0)→(1,0), (1,1)→(2,1). 새 공간에서는 두 XOR=1 점이 한 곳으로 모이고, "
                  "직선 h1 − 2h2 = 0.5로 깔끔하게 나뉜다. 이렇게 입력을 새 좌표(표현)로 바꾸는 것이 은닉층의 역할이다. "
                  "다음 장에서 같은 h1, h2를 출력 가중치 (1, −2)로 묶어 XOR 함수 하나로 적는다.")
L, R = s.cols(0.6)
s.image(A("week2/hidden_space.png"), L)
s.table(["입력", "h1", "h2", "XOR"],
        [["(0, 0)", "0", "0", "0"], ["(0, 1)", "1", "0", "1"], ["(1, 0)", "1", "0", "1"], ["(1, 1)", "2", "1", "0"]],
        Box(R.x, R.y, R.w, 2.2), size=13, align="cccc")
s.bullets(["ReLU(z) = max(0, z) (앞 장)", "h1 = ReLU(x1 + x2),  h2 = ReLU(x1 + x2 − 1)",
           "새 좌표에서는 **직선 하나**로 분리", ("h1 − 2·h2 = 0.5", 1),
           "(0,1)과 (1,0)이 **같은 점**으로 모인다"], Box(R.x, R.y + 2.4, R.w, R.h - 2.4), size=15)

s = d.slide("손으로 만든 XOR 해", lead="ReLU 두 개를 조합하면 XOR을 정확히 표현한다 — 학습 결과가 아니라 직접 구성한 해", stage="계산",
            notes="s = x1 + x2라 두면 f = ReLU(s) − 2·ReLU(s − 1). s가 0, 1, 2일 때 f는 0, 1, 0으로 XOR과 같다. "
                  "ReLU(s), ReLU(s−1)은 앞 장의 h1, h2 그대로이고, 출력은 h1 − 2h2 — 앞 장의 직선 h1 − 2h2 = 0.5를 0.5 기준으로 읽은 것과 같다. "
                  "이는 은닉 유닛 2개와 출력 가중치 (1, −2)를 가진 MLP다. 아래 W1, b1, W2는 다음 장의 shape 그대로다. "
                  "중요한 구분: 이 해는 사람이 직접 만든 것이다. '이런 해가 존재한다(표현 가능)'와 '학습으로 찾을 수 있다'는 다른 문제 → Part 4에서 확인.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("f(x) = ReLU(s) − 2 · ReLU(s − 1),     s = x1 + x2", top, size=22)
L, R = bot.cols(0.55, gap=0.4)
s.table(["(x1, x2)", "s", "ReLU(s)", "ReLU(s−1)", "f", "XOR"],
        [["(0, 0)", "0", "0", "0", "0", "0"], ["(0, 1)", "1", "1", "0", "1", "1"], ["(1, 0)", "1", "1", "0", "1", "1"],
         ["(1, 1)", "2", "2", "1", "2 − 2 = **0**", "0"]], Box(L.x, L.y, L.w, 2.6), size=16, align="cccccc",
        widths=[1.3, 0.6, 1.2, 1.4, 1.4, 0.8])
s.bullets(["= 좌표 바꾸기 장의 h1, h2 그대로 — 출력 = h1 − 2·h2", "은닉 유닛 2개 + 출력 가중치 (1, −2)",
           "= **MLP** (Multi-Layer Perceptron)",
           "==주의== 존재한다 ≠ 학습으로 찾는다", ("‘표현 가능’과 ‘학습 가능’은 다른 질문", 1)], R, size=16)
s.callout("같은 해를 행렬로 쓰면 (다음 장의 shape 그대로): h = ReLU(x W1 + b1), ŷ = h W2  —  "
          "W1 = [[1, 1], [1, 1]],  b1 = [0, −1],  W2 = [[1], [−2]]",
          Box(bot.x, bot.y + 2.85, bot.w, 0.9), kind="tip", size=15)

s = d.slide("MLP의 구조와 shape", lead="선형 → 비선형 → 선형. 배치 B개를 한 번에 계산한다", stage="계산",
            notes="h = ReLU(x W1 + b1), ŷ = h W2 + b2. 입력 2개, 은닉 m개, 출력 1개면 W1: (2, m), b1: (m,), W2: (m, 1), b2: (1,). "
                  "손으로 만든 XOR 해는 m = 2인 경우. 파라미터 수 = 2m + m + m + 1 = 4m + 1. 배치 B개 입력 (B, 2) → 은닉 (B, m) → 출력 (B, 1). "
                  "Transformer의 FFN(6주차)도 정확히 이 구조를 각 토큰에 적용한다: d → d_ff → d (입력 크기 → 더 큰 은닉 → 입력 크기).")
top, bot = s.area.top(1.9, gap=0.3)
s.flow([{"head": "입력 x", "body": "(B, 2)"}, {"head": "Linear W1, b1", "body": "(B, 2) → (B, m)"},
        {"head": "ReLU", "body": "(B, m) 비선형", "tone": "accent"}, {"head": "Linear W2, b2", "body": "(B, m) → (B, 1)"},
        {"head": "출력 ŷ", "body": "(B, 1)", "tone": "dark"}], top, body_size=15, head_size=16, gap=0.35)
L, R = bot.cols(0.5, gap=0.4)
s.formula(["h = ReLU(x W1 + b1)", "ŷ = h W2 + b2"], Box(L.x, L.y, L.w, 1.4), size=22)
s.bullets(["m = 은닉 유닛 수 (앞 장의 손으로 만든 해는 m = 2)",
           "파라미터: W1 (2, m), b1 (m,), W2 (m, 1), b2 (1,)", ("총 4m + 1개", 1)],
          Box(L.x, L.y + 1.6, L.w, L.h - 1.6), size=16)
s.callout("6주차 연결: Transformer의 **FFN**은 이 MLP를 **토큰마다** 적용한다 (입력 크기 → 더 큰 은닉 → 입력 크기).",
          R, kind="tip", size=18)

# ============================================================ Part 4
d.part(4, "역전파: 은닉층은 무엇을 기준으로 배우나 (1986)", "정답은 출력에만 있다 — 은닉층 가중치의 책임은 어떻게 계산할까?")

s = d.slide("책임 나누기 문제", lead="출력의 오차는 알지만, 은닉층 가중치가 얼마나 책임이 있는지는 간접적이다", stage="문제",
            notes="지난주에는 파라미터가 w, b 두 개뿐이라 기울기 공식을 직접 썼다. MLP에서는 W1의 한 칸이 h를 바꾸고, h가 ŷ를 바꾸고, ŷ가 손실을 바꾼다. "
                  "가장 단순한 방법은 가중치 하나를 조금 흔들어 보고 손실 변화를 재는 것(수치 미분)인데, 파라미터가 P개면 forward를 P+1번 해야 한다. "
                  "파라미터가 수백만 개면 불가능. 역전파는 forward 한 번 + backward 한 번으로 모든 기울기를 구한다.")
rest = s.cards([{"head": "방법 1 · 하나씩 흔들어 보기", "tone": "plain",
                 "body": ["가중치 하나를 +0.001 → 손실 변화 측정", "파라미터 P개면 forward **P + 1번**",
                          "GPT급 모델(수십억 개)이면 불가능"]},
                {"head": "방법 2 · 역전파", "tone": "accent",
                 "body": ["forward **1번** + backward **1번**", "출력에서 입력 쪽으로 **연쇄법칙**을 따라감",
                          "모든 파라미터의 기울기를 한꺼번에"]}], cols=2, body_size=18, head_size=20)
s.textbox("왜 간접적인가 — W1의 한 칸을 조금 바꾸면:", Box(rest.x, rest.y + 0.05, rest.w, 0.4), size=16, bold=True,
          color=TEAL, gap=0)
s.flow([{"head": "W1의 한 칸", "body": "+0.001"}, {"head": "h (은닉값)", "body": "이 바뀌고"},
        {"head": "ŷ (출력)", "body": "이 바뀌고"}, {"head": "L (손실)", "body": "이 바뀐다", "tone": "accent"}],
       Box(rest.x, rest.y + 0.5, rest.w, 1.25), body_size=15, head_size=16, gap=0.45)
s.callout("핵심 도구는 고등학교 미분의 **연쇄법칙** 하나다 — 이 사슬을 따라 변화율을 곱한다.",
          Box(rest.x, rest.y + 2.0, rest.w, 0.8), kind="key", size=17)

s = d.slide("연쇄법칙: 변화율은 곱해진다", lead="A가 B를, B가 C를 바꾸면 — A가 C를 바꾸는 비율은 두 비율의 곱", stage="아이디어",
            notes="톱니바퀴 비유: A가 1칸 돌면 B가 2칸, B가 1칸 돌면 C가 3칸 → A가 1칸 돌면 C는 6칸. "
                  "신경망에서: w가 h를, h가 ŷ를, ŷ가 L을 바꾼다. 그래서 ∂L/∂w = ∂L/∂ŷ × ∂ŷ/∂h × ∂h/∂w. "
                  "지난주 예제로 확인: ŷ = wx, L = ½(ŷ − y)². ∂L/∂ŷ = ŷ − y = 2 − 6 = −4, ∂ŷ/∂w = x = 2 → ∂L/∂w = −8. 지난주와 같은 값이다.")
top, bot = s.area.top(1.05, gap=0.3)
s.formula("∂L/∂w = ∂L/∂ŷ × ∂ŷ/∂w", top, size=26)
rest = s.cards([{"head": "톱니바퀴 비유", "body": ["A 1칸 → B 2칸, B 1칸 → C 3칸", "→ A 1칸 → C **2 × 3 = 6칸**"]},
                {"head": "지난주 예제로 확인", "tone": "accent",
                 "body": ["ŷ = wx, L = ½(ŷ − y)², x=2, y=6, w=1", "∂L/∂ŷ = ŷ − y = −4,  ∂ŷ/∂w = x = 2",
                          "∂L/∂w = −4 × 2 = **−8** (1주차와 같다)"]}], bot, cols=2, body_size=16, head_size=18)
s.bullets(["MLP에서는 은닉값 h를 거쳐 **한 단계 더** 곱해진다: ∂L/∂ŷ × ∂ŷ/∂h × ∂h/∂w (다음 장)",
           "역전파 = 이 곱셈을 **출력 쪽부터** 차례로, **중간 결과를 재사용**하며 계산하는 방법"], rest, size=17)

s = d.slide("예제 MLP: forward", lead="입력 → 은닉 → 출력 → 손실. 각 단계의 값을 저장해 둔다", stage="계산",
            notes="예제: x = [1, 1], W1 = [[1, −1], [0.5, 0.5]], 편향은 0으로 고정, W2 = [[2], [1]], 정답 y = 2. "
                  "z = xW1 = [1·1 + 1·0.5, 1·(−1) + 1·0.5] = [1.5, −0.5]. h = ReLU(z) = [1.5, 0]. "
                  "ŷ = hW2 = 1.5·2 + 0·1 = 3. L = ½(3 − 2)² = 0.5. forward 동안 z, h 같은 중간값을 저장해 두는 이유는 backward에서 재사용하기 때문.")
top, bot = s.area.top(3.2, gap=0.2)
L, R = top.cols(0.66, gap=0.3)
s.image(A("week2/graph.png"), L)
s.bullets(["파란 화살표 = forward, 상자 안 = 각 단계의 **값**", "**주황** = 다음 장 backward에서 쓰는 **기울기**",
           "중간값 z, h를 **저장**해 두는 이유 → backward에서 재사용"], R, size=15)
s.table(["단계", "계산", "값"], [["z = x W1", "[1·1 + 1·0.5,  1·(−1) + 1·0.5]", "[1.5, −0.5]"],
                               ["h = ReLU(z)", "음수는 0으로", "[1.5, 0]"],
                               ["ŷ = h W2", "1.5·2 + 0·1", "3"], ["L = ½(ŷ − y)²", "½(3 − 2)²", "0.5"]],
        bot, widths=[1.6, 3.2, 1.4], size=14, align="lcc")

s = d.slide("Backward: 기울기를 거꾸로 전달", lead="각 단계는 ‘위에서 받은 기울기 × 자기 국소 미분’만 계산한다", stage="계산",
            notes="∂L/∂ŷ = ŷ − y = 1. ∂L/∂h = ∂L/∂ŷ × W2ᵀ = [2, 1]. ReLU의 국소 미분은 z>0이면 1, 아니면 0 → ∂L/∂z = [2·1, 1·0] = [2, 0]. "
                  "파라미터 기울기: ∂L/∂W2 = hᵀ × ∂L/∂ŷ = [[1.5], [0]], ∂L/∂W1 = xᵀ × ∂L/∂z = [[2, 0], [2, 0]]. "
                  "두 번째 은닉 유닛은 ReLU에서 0이 되었기 때문에 기울기도 0 — 이번 예시에서는 학습되지 않는다(ReLU의 특징).")
body = Box(s.area.x, s.area.y, s.area.w, s.area.h - 0.8)   # 아래 takeaway 자리
s.table(["거꾸로 계산", "규칙", "값"],
        [["∂L/∂ŷ", "ŷ − y", "1"], ["∂L/∂h", "∂L/∂ŷ × W2ᵀ", "[2, 1]"],
         ["∂L/∂z", "∂L/∂h × ReLU′(z)  (z > 0 → 1, 아니면 0)", "[2, 0]"],
         ["∂L/∂W2", "hᵀ × ∂L/∂ŷ", "[[1.5], [0]]"], ["∂L/∂W1", "xᵀ × ∂L/∂z", "[[2, 0], [2, 0]]"]],
        Box(body.x, body.y, body.w, 2.4), widths=[1.6, 4.6, 2.2], size=16, align="lcc", highlight=[3, 4])
s.image(A("week2/graph.png"), Box(body.x, body.y + 2.55, body.w, body.h - 2.55))
s.takeaway("각 노드는 ‘받은 기울기 × 국소 미분’만 알면 된다 — 그래서 아무리 깊어도 계산할 수 있다")

s = d.slide("한 번의 업데이트", lead="기울기를 받으면 지난주와 똑같이 W ← W − η·∇W", stage="검증",
            notes="η = 0.1로 갱신: W2 = [[2 − 0.15], [1 − 0]] = [[1.85], [1]]. W1 = [[1 − 0.2, −1], [0.5 − 0.2, 0.5]] = [[0.8, −1], [0.3, 0.5]]. "
                  "다시 forward: z = [0.8 + 0.3, −1 + 0.5] = [1.1, −0.5], h = [1.1, 0], ŷ = 1.1 × 1.85 = 2.035. "
                  "손실 0.5 → 0.0006. 한 번에 정답 2에 거의 도착했다. PyTorch로 같은 값을 확인할 수 있다(다음 슬라이드 뒤 코드).")
L, R = s.cols(0.5, gap=0.4)
s.table(["", "이동 전", "이동 후 (η = 0.1)"], [["W1", "[[1, −1], [0.5, 0.5]]", "[[0.8, −1], [0.3, 0.5]]"],
                                            ["W2", "[[2], [1]]", "[[1.85], [1]]"], ["ŷ", "3", "**2.035**"],
                                            ["손실 L", "0.5", "**0.0006**"]], Box(L.x, L.y, L.w, 2.8), size=15, align="lcc",
        highlight=[2, 3])
s.bullets(["정답 y = 2에 **거의 도착**", "두 번째 은닉 유닛(ReLU = 0)은 이번엔 변화 없음",
           "역전파는 기울기 **계산**, 갱신은 **optimizer** — 1주차 구분 그대로", "이 과정을 수천 번 반복 = 학습"], R)
s.callout("forward → backward → update를 **수천 번 반복**하면 — 다음 장: 실제로 XOR을 학습시켜 본다",
          Box(s.area.x, s.area.y + 3.2, s.area.w, 0.8), kind="key", size=16)

s = d.slide("학습으로 XOR 찾기", lead="표현할 수 있다고 해서 항상 찾아지는 것은 아니다 — 은닉층 크기가 성공률을 바꾼다", stage="검증",
            notes="직접 실험: ReLU 은닉층 MLP, BCE 손실, SGD lr=0.5, 3000 step, 무작위 초기화 20회. "
                  "은닉 2개: 20번 중 4번 성공, 4개: 15번, 8개: 19번. 은닉 2개로도 XOR 해가 존재(앞에서 직접 구성)하지만 학습이 그 해를 못 찾는 경우가 많다. "
                  "은닉 유닛 일부가 ReLU 음수 구간에 갇혀 기울기가 0이 되는 등 이유가 있다. 여유 있는 모델이 학습하기 쉽다는 경험적 관찰로 이어진다.")
L, R = s.cols(0.62)
s.image(A("week2/mlp_trained.png"), L)
s.table(["은닉 유닛 수", "성공 (20회 중)"], [["2", "4"], ["4", "15"], ["8", "19"]], Box(R.x, R.y, R.w, 1.7),
        size=15, align="cc")
s.bullets(["2-4-1 = 입력 2 · 은닉 4 · 출력 1", "손실: 이진 cross-entropy, 경사하강법 lr 0.5, 3000 step",
           "은닉 2개로도 해는 **존재**하지만 자주 못 찾는다",
           "원인 예: ReLU가 0에 갇힌 유닛 → 기울기 0"], Box(R.x, R.y + 1.9, R.w, R.h - 1.9), size=15)

s = d.slide("모델 부족인가, 학습 실패인가", lead="성능이 낮을 때 두 원인을 분리해서 점검한다", stage="검증",
            notes="원자료의 질문: XOR에서 성능이 낮으면 모델이 부족한 건가, 학습이 안 된 건가? "
                  "표현 가능한 함수 자체가 제한된 경우(단층 Perceptron과 XOR)와, 표현 가능한 함수를 optimizer가 찾지 못한 경우(은닉 2개 MLP의 실패)를 나눈다. "
                  "학습형 MLP가 실패하면 구현(shape, 활성화 위치), 초기화, 학습률, 반복 수, 모델 크기를 차례로 점검한다. 이 구분은 Transformer 실험(6주차)에서도 그대로 쓴다. "
                  "수업 팁: 직접 구성한 XOR 해를 먼저 보여 준 뒤, 학습형 MLP가 실패하면 구현 · 초기화 · 학습률 · 반복 수를 차례로 점검하게 한다.")
s.table(["", "모델이 부족 (표현력 한계)", "학습이 실패 (최적화 문제)"],
        [["뜻", "어떤 파라미터로도 원하는 함수를 못 만든다", "만들 수 있는 파라미터가 있는데 못 찾았다"],
         ["예", "단층 Perceptron으로 XOR", "은닉 2개 MLP가 XOR에서 실패"],
         ["확인 방법", "직접 해를 구성해 보기 · 이론적 분석", "같은 모델로 해를 직접 넣어 보기 · 여러 seed"],
         ["처방", "구조를 바꾼다 (층, 비선형성)", "구현 · 초기화 · 학습률 · 반복 수 · 크기 점검"]],
        Box(s.area.x, s.area.y, s.area.w, 3.1), widths=[1.4, 4.2, 4.2], size=18)
s.callout("학습이 안 될 때 점검 순서: 구현 → 초기화 → 학습률 → 반복 수 → 모델 크기   (6주차 Transformer 실험에서도 같은 순서)",
          Box(s.area.x, s.area.y + 3.3, s.area.w, 1.1), kind="key", size=16)

s = d.slide("역전파의 계보", lead="1986년은 ‘발명’이 아니라 은닉 표현 학습을 보여주며 ‘확산’된 해", stage="역사",
            notes="역방향 자동 미분의 아이디어는 1970년 Linnainmaa의 석사 논문에서 나타났고, 1974년 Werbos가 박사 논문에서 신경망 학습에 적용할 수 있음을 제시했다. "
                  "1986년 Rumelhart, Hinton, Williams의 Nature 논문 'Learning representations by back-propagating errors'는 은닉층이 유용한 내부 표현을 스스로 학습한다는 것을 보여주며 널리 확산시켰다. "
                  "원자료 주의: '역전파는 1986년에 처음 발명되었다'고 말하지 않는다.")
s.timeline([(1970, "Linnainmaa", "역방향 자동 미분 (reverse-mode AD)의 아이디어"),
            (1974, "Werbos", "박사 논문: 신경망 학습에 적용 가능성 제시"),
            (1986, "Rumelhart · Hinton · Williams", "Nature 논문 — 은닉층이 **내부 표현**을 학습함을 보여주며 확산"),
            ("오늘", "autograd", "PyTorch 등 모든 딥러닝 프레임워크의 핵심")],
           Box(s.area.x, s.area.y, s.area.w, 3.3), highlight=[2], body_size=15)
s.callout("배울 것: 연쇄법칙, 계산 그래프, 그리고 ‘표현력’(무엇을 만들 수 있나)과 ‘학습 알고리즘’(어떻게 찾나)의 구분.",
          Box(s.area.x, s.area.y + 3.55, s.area.w, 1.0), kind="tip", size=16)

s = d.slide("PyTorch autograd로 확인", lead="loss.backward() 한 줄이 방금 손으로 한 backward 표 전체", stage="코드",
            notes="requires_grad=True인 텐서로 forward를 하면 PyTorch가 계산 그래프를 기록한다. L.backward()를 호출하면 역전파로 모든 기울기를 채운다. "
                  "출력: W1.grad = [[2, 0], [2, 0]], W2.grad = [[1.5], [0]] — 손 계산과 같다. "
                  "과제: 편향 b1, b2도 넣어서 기울기를 손으로 계산하고 autograd와 비교해 보기.")
L, R = s.cols(0.6)
s.code("import torch\n"
       "x  = torch.tensor([[1., 1.]])\n"
       "W1 = torch.tensor([[1., -1.], [0.5, 0.5]], requires_grad=True)\n"
       "W2 = torch.tensor([[2.], [1.]], requires_grad=True)\n\n"
       "h = torch.relu(x @ W1)        # [[1.5, 0.0]]\n"
       "y_hat = h @ W2                # [[3.0]]\n"
       "L = 0.5 * (y_hat - 2) ** 2    # 0.5\n"
       "L.backward()\n\n"
       "print(W1.grad)  # [[2., 0.], [2., 0.]]\n"
       "print(W2.grad)  # [[1.5], [0.]]", L, size=14)
cb = s.last_code_box
s.callout("손 계산 표와 완전히 같은 값", Box(L.x, cb.b + 0.25, L.w, 0.7), kind="key", size=16)
s.bullets(["`requires_grad=True`: 기울기를 추적", "forward 중 **계산 그래프** 기록", "`backward()`: 역전파로 `.grad` 채움",
           "갱신은 따로: `opt.step()`"], Box(R.x, R.y, R.w, 2.3), size=17)
s.table(["손 계산", "코드"], [["forward 표 (z, h, ŷ, L)", "h = relu(x @ W1) … L = …"], ["backward 표 전체", "L.backward()"],
                            ["∂L/∂W1, ∂L/∂W2", "W1.grad, W2.grad"], ["갱신 W ← W − η·∇W", "opt.step()"]],
        Box(R.x, R.y + 2.45, R.w, R.h - 2.45), widths=[1.1, 1.0], size=14)

# ============================================================ Part 5
d.part(5, "확률로 답하기: Softmax와 Cross-entropy", "‘예/아니오’ 대신 ‘얼마나 확신하는가’, 여러 선택지 중 하나를 고르려면?")

s = d.slide("Sigmoid: 출력층에서 점수를 확률로", lead="출력층의 함수 — 계단 대신 부드러운 S자: 미분할 수 있고, 확신의 정도를 말해 준다",
            stage="아이디어",
            notes="계단 함수는 미분이 안 돼서 역전파를 쓸 수 없다. sigmoid σ(z) = 1/(1 + e^−z)는 z를 0~1 사이로 부드럽게 바꾼다. "
                  "z = 0 → 0.5, z = 2 → 0.88, z = −2 → 0.12. 출력을 '1일 확률'처럼 읽을 수 있다. "
                  "위치 구분: Part 3의 ReLU는 은닉층 사이에서 직선을 구부리는 역할이고, sigmoid는 마지막 출력층에서 점수를 확률로 바꾸는 역할이다 "
                  "(sigmoid를 은닉 활성화로 쓰면 도함수 ≤ 0.25 때문에 기울기가 줄어든다 — 다음 주). "
                  "주의: 0~1 사이 값이라고 해서 현실적으로 잘 보정된(calibrated) 확률이라는 보장은 없다 — 흔한 오해 장에서 다시 다룬다.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("σ(z) = 1 / (1 + e^(−z))", top, size=26)
L, R = bot.cols(0.5, gap=0.4)
s.table(["z (점수)", "σ(z)", "읽는 법"], [["−2", "0.12", "1일 가능성 낮음"], ["0", "0.50", "반반"],
                                         ["2", "0.88", "1일 가능성 높음"]], Box(L.x, L.y, L.w, 2.0), size=16, align="ccl")
s.bullets(["**출력층**에 쓰는 함수: 마지막 점수 z → ‘1일 확률’", ("은닉층의 ReLU(직선 구부리기)와 자리가 다르다", 1),
           "계단 함수와 달리 **미분 가능** → 역전파 OK", "선택지가 **여러 개**라면? → Softmax"], Box(R.x, R.y, R.w, 2.6))
s.callout("Perceptron의 판정 ŷ = 1[z ≥ 0] 은 σ(z) ≥ 0.5 와 같은 경계다 — 결정 경계는 그대로 두고, "
          "‘얼마나 확신하는가’(0.12 / 0.50 / 0.88)만 더해졌다.", Box(bot.x, bot.y + 2.75, bot.w, 1.0), kind="key", size=16)

s = d.slide("Softmax: 점수들을 비중으로", lead="모든 점수를 exp로 양수로 만든 뒤, 합이 1이 되게 나눈다", stage="계산",
            notes="클래스가 K개면 모델은 점수(logit) K개를 낸다. softmax는 각 점수를 exp로 양수로 바꾸고 전체 합으로 나눠 합이 1인 비중을 만든다. "
                  "예: z = [2, 1, 0] → exp = [7.39, 2.72, 1.00], 합 11.11 → p = [0.665, 0.245, 0.090]. 가장 큰 점수가 가장 큰 비중을 갖지만 나머지도 0이 아니다. "
                  "구현 팁: exp가 너무 커지지 않도록 최댓값을 빼고 계산해도 결과가 같다(수치 안정화).")
top, bot = s.area.top(1.05, gap=0.3)
s.formula("p_i = exp(z_i) / Σ_j exp(z_j)", top, size=26)
L, R = bot.cols(0.52, gap=0.4)
s.table(["", "고양이", "개", "새"], [["점수 z", "2", "1", "0"], ["exp(z)", "7.39", "2.72", "1.00"],
                                  ["p = exp / 11.11", "**0.665**", "0.245", "0.090"]], Box(L.x, L.y, L.w, 2.0),
        size=16, align="lccc")
s.bullets(["합 = 1, 모두 양수", "순서는 점수 순서 그대로", "가장 큰 점수가 가장 큰 비중 — 나머지도 0은 아니다"],
          Box(L.x, L.y + 2.3, L.w, L.h - 2.3), size=16)
s.callout("5주차 연결: Attention도 ‘비교 점수 → softmax → 비중’으로 어떤 토큰을 얼마나 참고할지 정한다.", R, kind="tip", size=17)

s = d.slide("Temperature: 분포의 뾰족함", lead="softmax(z / τ): 순서는 그대로, τ가 작으면 뾰족하게 · 크면 평평하게", stage="계산",
            notes="τ = 1이 기본 softmax. τ = 0.5로 점수를 두 배로 키우면 1등 비중이 0.867로 커지고, τ = 2면 0.506으로 평평해진다. "
                  "6주차에서 문장을 생성할 때 다음 토큰을 고르는 무작위성을 조절하는 데 쓴다. "
                  "원자료 주의: Attention의 √d 스케일과 생성 때의 temperature는 위치와 목적이 다르다(5주차).")
L, R = s.cols(0.6)
s.image(A("week1/softmax_temp.png"), L)
s.bullets(["τ = 0.5 → [0.867, 0.117, 0.016]", "τ = 1 → [0.665, 0.245, 0.090]", "τ = 2 → [0.506, 0.307, 0.186]",
           "**순서는 바뀌지 않는다**", "쓰임: 생성할 때 무작위성 조절 (6주차)"], R)

s = d.slide("Cross-entropy: 분류의 손실", lead="정답 클래스에 준 확률의 −log — 확신하고 틀릴수록 벌점이 급격히 커진다", stage="계산",
            notes="정답이 one-hot일 때 cross-entropy는 −log p(정답). 정답에 0.9를 주면 0.105, 0.5면 0.693, 0.1이면 2.303, 0.01이면 4.61. "
                  "앞 예시에서 정답이 고양이면 −log 0.665 = 0.408. "
                  "Entropy H(p) = −Σ p log p는 분포가 얼마나 퍼져 있는지(불확실성), cross-entropy H(q, p) = −Σ q log p는 정답 분포 q에 대해 예측 p가 내는 평균 '놀람'이다.")
L, R = s.cols(0.52)
s.image(A("week1/ce_curve.png"), L)
s.formula("L = −log p(정답)", Box(R.x, R.y, R.w, 0.95), size=24)
s.table(["정답에 준 확률", "손실"], [["0.9", "0.105"], ["0.665 (고양이 예)", "0.408"], ["0.5", "0.693"],
                                  ["0.1", "2.303"], ["0.01", "**4.605**"]], Box(R.x, R.y + 1.2, R.w, 2.5), size=15, align="cc")
s.bullets(["확신하고 틀리면 **큰 벌점**"], Box(R.x, R.y + 3.9, R.w, R.h - 3.9), size=16)

s = d.slide("왜 분류에는 Cross-entropy인가", lead="softmax + CE의 기울기는 놀랍도록 단순하다: p − y", stage="아이디어",
            notes="softmax 출력에 cross-entropy를 쓰면 점수(logit)에 대한 기울기가 p − y(예측 확률 − 정답 one-hot)가 된다. "
                  "앞 예시: p = [0.665, 0.245, 0.090], 정답 고양이 y = [1, 0, 0] → 기울기 [−0.335, 0.245, 0.090]. "
                  "정답 점수는 올리고 오답 점수는 내리는 방향이 자연스럽게 나온다. MSE를 쓰면 확신하고 틀린 경우 기울기가 오히려 작아지는 문제가 있다. "
                  "PyTorch의 CrossEntropyLoss는 softmax를 내부에서 하므로 logits(softmax 전 점수)를 넣는다 — 원자료 개념 확인 14.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("∂L/∂z = p − y", top, size=28)
L, R = bot.cols(0.5, gap=0.4)
s.table(["", "고양이 (정답)", "개", "새"], [["p", "0.665", "0.245", "0.090"], ["y (one-hot)", "1", "0", "0"],
                                        ["p − y", "**−0.335**", "0.245", "0.090"]], Box(L.x, L.y, L.w, 1.9), size=17,
        align="lccc")
s.bullets(["정답 점수는 **올리고**(−0.335), 오답 점수는 **내린다**(+0.245, +0.090)",
           "틀린 만큼(p − y) **그대로** 미는 힘 — 확신하고 틀릴수록 크다"], Box(L.x, L.y + 2.1, L.w, L.h - 2.1), size=16)
rest = s.card(R, "실전 주의 (PyTorch)", ["`nn.CrossEntropyLoss`는 softmax를 **내부에서** 한다",
                                       "→ softmax 전 점수(**logits**)를 넣는다", "softmax를 두 번 하면 학습이 이상해진다"],
              tone="accent", bullets=True, fit_h=True)
s.callout("MSE였다면? 정답에 p = 0.01을 준 ‘확신한 오답’에서 sigmoid 기울기 p(1 − p) ≈ 0.01이 곱해져 "
          "거의 배우지 못한다. CE는 이 항이 약분되어 p − y만 남는다.",
          Box(rest.x, rest.y + 0.1, rest.w, rest.h - 0.1), kind="warn", size=15)

s = d.slide("Transformer와의 연결", lead="오늘 배운 부품들이 6주 뒤 Transformer 안에 그대로 있다", stage="정리",
            notes="MLP → Transformer의 FFN(토큰마다 적용하는 2층 MLP). ReLU → FFN의 활성화(후속 모델은 GELU 등). "
                  "softmax + cross-entropy → 다음 토큰 예측: 어휘 |V|개 중 하나를 고르는 분류 문제. "
                  "역전파 → 수십억 개 파라미터를 가진 Transformer도 같은 방법으로 기울기를 구한다. "
                  "원자료: Q/K/V 투영도 학습 가능한 선형층이지만, 다른 토큰의 정보를 결합하는 것은 Attention 가중합이다(5주차).")
rest = s.cards([{"head": "MLP", "body": ["→ Transformer의 **FFN**", "토큰마다 d → d_ff → d"]},
                {"head": "ReLU", "body": ["→ FFN의 활성화", "후속 모델은 GELU 등"]},
                {"head": "Softmax + CE", "body": ["→ **다음 토큰 예측**", "어휘 |V|개 중 하나 고르기"]},
                {"head": "역전파", "body": ["→ 수십억 파라미터도", "같은 방법으로 학습"], "tone": "accent"}],
               cols=4, body_size=16, head_size=19)
s.textbox("Transformer 블록 하나를 오늘의 부품으로 읽으면:", Box(rest.x, rest.y, rest.w, 0.4), size=16, bold=True,
          color=TEAL, gap=0)
s.flow([{"head": "토큰 벡터 x", "body": "(B, T, d)"}, {"head": "Attention", "body": "다른 토큰과 섞기 (5주차)", "tone": "plain"},
        {"head": "FFN = 오늘의 MLP", "body": "d → d_ff → ReLU → d, 토큰마다", "tone": "accent"},
        {"head": "Softmax + CE", "body": "다음 토큰 분류 (오늘)", "tone": "dark"}],
       Box(rest.x, rest.y + 0.45, rest.w, 1.3), body_size=14, head_size=16, gap=0.4)
s.callout("Q/K/V 투영도 학습되는 선형층이다. 하지만 **다른 토큰의 정보를 섞는 것**은 MLP가 아니라 "
          "Attention의 가중합이다 (5주차) — MLP는 토큰 하나 안에서만 계산한다.",
          Box(rest.x, rest.y + 2.0, rest.w, 1.2), kind="tip", size=16)

# ============================================================ 마무리
d.summary(["**Perceptron** = 가중합 + 계단 함수, 결정 경계는 **직선** (1958)",
           "**XOR**은 직선 하나로 불가능 — 부등식이 모순 (1969년 한계 분석)",
           "은닉층은 **새 좌표**를 만든다 — 단, 층 사이 **비선형 활성화**가 없으면 하나로 합쳐진다",
           "**역전파** = 연쇄법칙을 출력부터 거꾸로, 중간값을 재사용해 모든 기울기를 한 번에 (1986 확산)",
           "‘**표현 가능**’과 ‘**학습으로 찾음**’은 다른 질문이다",
           "분류 출력은 **Softmax**, 손실은 **Cross-entropy** (기울기 p − y)"])

d.quiz("셀프 체크", [("역전파와 optimizer는 각각 무슨 일을 하나?", "역전파는 각 파라미터의 기울기를 계산, optimizer는 그 기울기로 파라미터를 갱신"),
                   ("활성화 없이 affine 층을 여러 개 합치면?", "하나의 affine 변환과 같다 — 표현할 수 있는 함수 종류가 늘지 않는다"),
                   ("XOR을 단층 Perceptron으로 못 푸는 이유를 한 문장으로?", "네 점이 요구하는 부등식이 모순 — 어떤 직선도 네 점을 모두 가를 수 없다"),
                   ("ReLU에서 z < 0인 유닛의 기울기는? 무슨 일이 생기나?", "0 — 그 입력에서는 해당 유닛의 앞쪽 가중치가 학습되지 않는다"),
                   ("z = [1, 1, 1]의 softmax와, 정답이 첫째일 때 CE는?", "[1/3, 1/3, 1/3], CE = −log(1/3) ≈ 1.099")],
       notes="Q1, Q2는 원자료 '개념 확인' 01, 02번.")

d.misconceptions([["“역전파는 1986년에 처음 발명되었다”", "1970 Linnainmaa, 1974 Werbos 등 선행 연구 — 1986년은 **확산**의 이정표"],
                  ["“AI 겨울은 XOR 하나 때문에 왔다”", "기술·연산·기대·투자·평가 등 **여러 맥락**. 단일 원인으로 서술하지 않는다"],
                  ["“층을 많이 쌓으면 표현력이 늘어난다”", "**비선형 활성화**가 없으면 층 수와 무관하게 선형 변환 하나"],
                  ["“ReLU면 기울기 소실이 모두 사라진다”", "초기화·학습률·입력 분포에 따라 달라진다. 음수 구간 기울기는 0"],
                  ["“해가 존재하면 학습이 찾아 준다”", "은닉 2개 MLP는 XOR 해가 있어도 20번 중 16번 실패했다"],
                  ["“softmax 출력은 믿을 만한 확률이다”", "합 1인 양수 비중일 뿐, **잘 보정된 확률**이라는 보장은 없다"]])

d.homework([("XOR 부등식", "OR, AND에 대해 네 부등식을 적고 만족하는 (w1, w2, b)를 하나씩 찾는다. XOR은 왜 모순인지 자기 말로 설명."),
            ("역전파 손계산", "오늘 예제에 편향 b1 = [0, 0], b2 = 0을 넣고 ∂L/∂b1, ∂L/∂b2를 손으로 구한 뒤 autograd와 비교."),
            ("XOR 학습 실험", "은닉 크기 2/4/8, 학습률 0.1/0.5로 seed 10개씩 돌려 성공률 표를 만든다. 실패한 경우의 은닉 활성값을 출력해 원인을 추측.")],
           notes="원자료 운영안 2회차 산출물: XOR 비교, 한 번의 gradient 업데이트.")

d.references([["[04] Rosenblatt (1958). The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain", "도입부: 학습 규칙의 아이디어"],
              ["Minsky & Papert (1969). Perceptrons. MIT Press", "단층의 한계 (parity, 연결성) — 보충 자료"],
              ["[05] Rumelhart, Hinton & Williams (1986). Learning representations by back-propagating errors. Nature", "은닉 표현 그림"],
              ["[42] Goodfellow et al. (2016). Deep Learning", "Ch.6 MLP · 6.5 역전파"],
              ["PyTorch 튜토리얼: Autograd mechanics", "requires_grad, backward"]])

d.handoff(["비선형 은닉층으로 **새 좌표**를 만들고", "역전파로 모든 층을 학습해", "**직선으로 안 되는 경계**도 배울 수 있다"],
          ["입력이 **이미지**(수만 픽셀)면? 모든 입력을 모든 뉴런에 연결하면 파라미터 폭발",
           "층을 **깊게** 쌓으면? 기울기가 곱해지며 사라진다 (sigmoid′ ≤ 0.25)"],
          ["**공간 구조를 어떻게 쓰고,**", "**깊은 모델은 어떻게 학습시키나?**", "CNN · AlexNet · ResNet"],
          notes="다음 주: 이미지처럼 구조가 있는 큰 입력, 그리고 깊이의 문제. CNN(1989)부터 ResNet(2015)까지.")

d.save(OUT)
print("saved", OUT, d.n + 2, "slides")
