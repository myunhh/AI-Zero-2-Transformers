# AI Zero 2 Transformer — 6주 강의 설계서 (모든 주차 에이전트 공통)

원자료: `build/research/AI_Zero_2_Transformer.html` (텍스트 추출본: `build/research/source.txt`, 줄 번호는 이 파일 기준)
템플릿: `build/Lab-template.pptx` (AICA Lab) — 반드시 `build/deckkit.py`로만 슬라이드 생성
산출물: `lectures/weekNN_<slug>.pptx` 6개

## 전체 원칙
1. **원자료의 모든 내용을 6주 안에 빠짐없이 다룬다.** 각 주차 담당 범위(아래 표)의 모든 소제목(`## ...`)이 최소 1장 이상의 슬라이드(또는 슬라이드 일부)에 반영되어야 한다. 인터랙티브 위젯(예: "01 / 경사하강법 한 걸음 INTERACTIVE")은 정적 그림(matplotlib) + 수치 예제로 대체한다.
2. **시간순 계보**: 각 주차는 "AI 계보 타임라인에서 지금 어디인가"로 시작하고, 다음 주 예고로 끝난다. 연도·인물·논문명은 정확해야 한다(자료조사 에이전트가 검증).
3. **수학은 필수적인 것만**: 공식은 한 슬라이드에 하나, 기호 설명 + 작은 숫자 예제로. 증명·유도는 생략하고 "왜 필요한가"를 우선.
4. **표기 통일**(원자료 기준): 배치 B, 길이 N(또는 query 길이 T, key 길이 S), 모델 차원 d, head 수 H, head 차원 dₕ=d/H, FFN 차원 d_ff, 어휘 크기 |V|. 벡터는 행벡터 관례, 행렬곱 `@`.
5. 언어: 한국어 본문, 전문용어는 영어 병기(예: 역전파(Backpropagation)). 슬라이드 제목은 짧게(한글 기준 ~20자 이내).
6. **분량**: 주차당 본문 28~40장 (표지·Question 장 제외). 2시간 강의 기준.
7. **모든 슬라이드에 발표자 노트**(notes=)를 2~5문장으로: 강사가 말할 설명, 예시, 학생 질문 대비.
8. 매 주차 필수 구성: 표지 → 지난 주 복습(1주차는 과정 소개/전체 지도) → 오늘의 위치(타임라인) → 학습 목표 → 본문(Part 01..0k 섹션 구분) → 개념 확인 퀴즈(원자료 "개념 확인" 문항 + 오개념 중 해당 주차 것) → 오늘의 정리(summary, next_week=...) → Question(템플릿 자동).
9. 시각 요소: 텍스트만 있는 슬라이드 연속 3장 금지. deckkit의 cards/flow/timeline/compare/formula/table/code/image/stats를 섞어 쓴다. 그림은 matplotlib(`deckkit.mpl_setup()`, 팔레트 `PALETTE_HEX`)로 `build/assets/weekN/`에 PNG 생성.
10. 코드 예제는 PyTorch 기준, 짧게(≤ 15줄).

## 주차별 범위 (source.txt 줄 번호)

| 주차 | 제목(안) | 시대 | 원자료 범위 |
|---|---|---|---|
| 1 | Tensor와 학습의 기초 | 1943~ 계산 모델, 과정 전체 지도 | 32–205 (도입, 학습 루프, 전체 지도·계보 개관 136–205는 **개관 수준**으로), 206–440 (수학 준비: 벡터·행렬·내적·Softmax·미분/연쇄법칙·Entropy/CE), 441–535 (학습이란: 파라미터, 경사하강법, 일반화, 학습방식 vs 아키텍처). **Tensor 기초(스칼라→벡터→행렬→텐서, shape, 배치 축, broadcasting, PyTorch 텐서)로 시작** |
| 2 | Perceptron에서 MLP로 | 1958 Perceptron → 1969 XOR 한계 → 1986 역전파 | 142–159 (Perceptron, 규칙 기반 방법의 발전, 다층 표현학습·역전파 확산), 536–720 (선형 분리, XOR 결정경계, 비선형성, 선형층 붕괴, ReLU와 gradient). 개념 확인 01, 02 |
| 3 | CNN과 깊은 모델의 조건 | 1989 LeNet/CNN → 1995 SVM → 2006~2012 딥러닝 부활·AlexNet → 2015 ResNet/BatchNorm | 160–177 중 CNN·SVM·AlexNet 관련, 184–189 (잔차·정규화), 721–829 (CNN, 가중치 공유/지역성, SVM이라는 옆길, 깊은 모델이 가능해진 조건, Residual과 정규화의 문제의식) |
| 4 | 언어·순서·기억: Word2Vec, RNN, LSTM, Seq2Seq | 1986~1990 RNN → 1997 LSTM → 2003 신경 언어모델 → 2013 Word2Vec → 2014 Seq2Seq | 160–183 중 시퀀스·Word2Vec·Encoder-Decoder 관련, 830–984 (언어를 벡터로: one-hot vs 임베딩, 토큰화, Word2Vec, 조건부 확률 연결, contextual representation), 985–1273 (RNN, 장기 의존성, LSTM 게이트, 사고실험), 1274–1319 (Seq2Seq, 길이가 다른 입력/출력). 개념 확인 03. **Attention 직전(고정 문맥 벡터 병목 문제 제기)에서 끝낸다** |
| 5 | Attention과 Transformer의 핵심 | 2014 Bahdanau Attention → 2017 "Attention Is All You Need" | 1320–1449 (병목 → Attention, 가중합 계산, "Attention을 본체로"), 178–193 (계보: Encoder–Decoder와 Attention, Transformer), 1450–1554 (Transformer 전체 구조, 입출력 계약, 세 종류 Attention, 블록 역할), 1555–1739 (위치 정보, Sinusoidal PE), 1740–1857 (Q/K/V, 투영 행렬, cross-attention), 1858–1981 (Scaled dot-product 수치 계산, √dₕ, 경계조건), 1982–2113 (Multi-head, tensor shape 추적, d=8,H=2,N=5). 개념 확인 04–10 |
| 6 | Transformer 완성: 학습·추론·그 이후 | 2017 Transformer → Pre-LN, KV cache, ViT(2020), DiT(2022/23) | 2114–2319 (FFN, Residual, LayerNorm, Post/Pre-LN), 2320–2425 (Mask, Teacher forcing), 2426–2720 (Encoder/Decoder 한 층, 출력 head, 한 샘플 추적, 파라미터 수), 2721–2903 (학습: NLL, 학습 step, 원논문 조건, 지표), 2904–3062 (추론, 토큰 선택, KV cache, 연산량/메모리), 3063–3568 (작은 Transformer 실습, 실험 설계, 최종 프로젝트), 3690–3803 (Transformer 이후: Encoder-only/Decoder-only, ViT, DiT), 3804–3885 (오개념 20가지 중 Transformer 관련), 3886–4080 (개념 확인 11–18, 기호 사전, 참고문헌). 과정 전체 마무리 포함 |

- 3569–3689 (10회 멘토링 운영안, 여섯 화면 구성, 숙제, 구술평가)는 **교수법 참고용** — 각 주차의 과제/실습 슬라이드 구성에 활용(주차 마지막에 "이번 주 과제" 1장 권장).
- 3804–3885 (오개념 20가지)는 해당 개념이 나오는 주차의 퀴즈/주의 슬라이드에 분배. 1–5주차 담당도 이 구간을 읽고 자기 주차 관련 오개념을 가져간다.
- 4060–4080 (원문과 참고자료)는 각 주차 마지막 "참고 자료" 1장에 해당 주차 논문만 추려서.

## 주차 간 연결 (계보 스토리)
1주: "학습 = 손실을 줄이는 파라미터 찾기"와 그 계산 언어(Tensor) → 2주: 가장 단순한 학습 모델 Perceptron의 한계(XOR)와 MLP+역전파로의 해결 → 3주: 층을 깊게 쌓기 위한 조건(CNN의 구조적 가정, ReLU·GPU·데이터, Residual·Normalization) → 4주: 순서가 있는 데이터(언어)를 벡터로, RNN/LSTM의 기억, Seq2Seq의 고정 벡터 병목 → 5주: 병목을 푸는 Attention, Attention을 본체로 한 Transformer의 핵심 연산 → 6주: 블록 완성, 학습·추론·효율, 그리고 Transformer 이후.

## 날짜 (푸터)
W1 2026-10-05, W2 2026-10-12, W3 2026-10-19, W4 2026-10-26, W5 2026-11-02, W6 2026-11-09

## 기술 규칙
- `sys.path.insert(0, "<repo>/build")` 후 `from deckkit import *`. deckkit.py의 docstring과 각 메서드 시그니처를 먼저 읽을 것. deckkit.py는 **수정 금지**(공유 파일) — 필요한 레이아웃이 없으면 자기 빌드 스크립트 안에서 `d.blank()` + `d.box/d.text/d.arrow/d.circle_num`으로 직접 배치.
- 빌드 스크립트: `build/weekN.py` (실행 시 `lectures/weekNN_slug.pptx` 생성). 그림: `build/assets/weekN/*.png`.
- 렌더 QA: `build/render.sh lectures/weekNN_x.pptx /tmp/qa_weekN` → JPG를 직접 보고 텍스트 넘침/겹침/빈 공간 과다/잘림 확인 후 수정. 검증: `python <pptx skill>/scripts/office/validate.py <deck> --original build/Lab-template.pptx`.
- 카드/박스 안 텍스트가 너무 적어 큰 빈 공간이 생기지 않도록 내용을 충실히 채우거나 카드 수/레이아웃을 조정.
- git commit/push 하지 말 것 (오케스트레이터가 일괄 처리).
