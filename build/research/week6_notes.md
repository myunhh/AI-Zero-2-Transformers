# Week 6 연구 노트: Transformer 완성: 학습·추론·그 이후

원자료 범위: source.txt 2114–3568, 3690–4080 (3569–3689 멘토링 운영안은 교수법 참고).
산출물: `lectures/week06_transformer_complete.pptx` (빌드: `python build/week6_figs.py && python build/week6.py`)

## 1. 검증한 사실 (원논문·참고문헌 기준)

| 항목 | 값 | 근거 |
|---|---|---|
| 원형 Base | Enc/Dec 각 6층, d=512, d_ff=2048, H=8, dₕ=64, P_drop=0.1, ε_ls=0.1, 약 65M 파라미터 | Vaswani 등 2017 §3, Table 3 |
| 원형 Big | d=1024, d_ff=4096, H=16, 약 213M, EN–DE는 P_drop 0.3 | 같은 논문 Table 3 |
| Optimizer | Adam β₁=0.9, β₂=0.98, ε=10⁻⁹ | §5.3 |
| 학습률 | η = d^-0.5·min(s^-0.5, s·w^-1.5), w=4000 | §5.3 |
| Label smoothing 0.1 | perplexity는 나빠지지만 정확도·BLEU는 개선 | §5.4 |
| 하드웨어·step | 8×P100, Base 100K step(약 12시간, 0.4 s/step), Big 300K step(3.5일) | §5.2 |
| BLEU (WMT14) | EN–DE 27.3(Base) / 28.4(Big), EN–FR 41.8(Big, arXiv 최종판; v1은 41.0) | §6.1 Table 2 |
| 디코딩 | beam 4, length penalty α=0.6, 최대 출력 길이 = 입력 + 50 | §6.1 |
| 어휘 | EN–DE: 공유 BPE 약 37,000 / EN–FR: word-piece 32,000 | §5.1 |
| 연도 | Pre-LN 분석 Xiong 등 2020, BERT 2018(NAACL 2019), GPT 2018, T5 2019(JMLR 2020), ViT arXiv 2020(ICLR 2021), DiT arXiv 2022-12(ICCV 2023), FlashAttention 2022, RoPE 2021, GLU 변형 2020, GQA 2023 | 원자료 참고문헌 [19]–[41] |
| API | SDPA boolean True=허용 / nn.MultiheadAttention boolean True=차단 | PyTorch 문서 [27][28] |

## 2. Python으로 재계산한 수치

- 층당 파라미터(bias 제외) 4d²+2d·d_ff: d=512 → 1,048,576 + 2,097,152 = **3,145,728 (≈3.15M)**; Decoder +4d² → **4,194,304**.
- bias·LN 포함: Encoder 층 3,152,384, Decoder 층 4,204,032. 12개 층 ≈ 44.1M. 공유 embedding 37,000×512 ≈ 18.9M → 합계 ≈ **63.1M** (논문 65M). Big은 같은 식으로 ≈ 214M (논문 213M).
- LayerNorm x=(1,2,3,4): μ=2.5, σ²=1.25, 정규화 (−1.342, −0.447, 0.447, 1.342); γ=2, β=1 → (−1.68, 0.11, 1.89, 3.68), 평균 1, 분산 4.
- Causal 예시 점수 [2,1,3]: −∞ → softmax [0.731, 0.269, 0]; 0으로 바꾸면 [0.665, 0.245, 0.090].
- NLL 예시 p=[0.7,0.5,0.9,0.2] → −log p=[0.357, 0.693, 0.105, 1.609], 평균 0.691, perplexity 1.996.
- 학습률 최고점(s=4000): 512^-0.5·4000^-0.5 = **6.99×10⁻⁴**.
- MACs/샘플/층 (d=512, d_ff=2048): N=512 → 0.54+0.27+1.07 = 1.88G; N=4096 → 4.29+17.18+8.59 = 30.06G. 2N²d = 12Nd² → N = 6d = 3072.
- KV cache bytes = 2·B·L·N·H_kv·dₕ·b: Base 디코더 L=6, d=512, N=1024, FP16 → 12 MiB; L=32, d=4096, N=4096, FP16 → 2 GiB (B=8 → 16 GiB, GQA H_kv=8 → 0.5 GiB). Score 표 B·H·N² (H=32, N=4096, FP16) = 1 GiB/층.
- ViT 224/16 = 14 → 196 patch, patch당 16·16·3 = 768 값.
- Toy lab 파라미터(d=64, d_ff=256, |V|=16, 2+2층, bias 포함, 출력층 미공유) ≈ 235,536.
- 실습 결과(원자료 실행 기록, 재현 아님): 3–8 NLL 1.0450 / token acc 56.77% / exact 5/72; 9–12 NLL 1.7640 / 33.82% / 0/72; train NLL 2.8998 → 1.2299.

## 3. 소제목 커버리지 (source.txt `##` → 슬라이드 번호, 표지 = 1)

| 원자료 소제목 | 슬라이드 |
|---|---|
| FFN: 모인 정보를 비선형적으로 바꾸기 | 6 |
| Residual: 기존 표현을 보존할 통로 | 8 |
| LayerNorm은 어느 축을 정규화할까 (+ Norm 손풀기) | 7 |
| Post-LN과 Pre-LN | 8 |
| 원형과 후속 변형을 구분하기 | 35 |
| Decoder 입력과 정답을 한 칸 어긋나게 | 9 |
| 정답 누출 탐지기 / Causal mask는 Softmax 이전에 | 10 |
| Causal, Padding, Loss mask / API boolean 의미 | 11 |
| 왜 학습을 병렬 계산할 수 있나 | 9, 21 |
| Encoder 한 층 / Decoder 한 층 / 출력 Head | 13 |
| 한 샘플을 끝까지 추적하기 | 14 |
| 파라미터 수를 직접 유도하기 (+ Base 설정) | 15 |
| 다음 토큰의 음의 로그 가능도 | 16 |
| 한 학습 step의 순서 / 학습 모드와 평가 모드 | 17 |
| 원논문의 학습 조건 | 18 |
| 어떤 지표를 기록할까 (+ loss가 안 떨어질 때) | 19 |
| 추론 / 정답 prefix가 없다 / 토큰 선택 정책 | 21 |
| KV Cache / 순차성은 남나 / Cache 공유 / Prefill과 Decode | 22 |
| O(N²)만으로는 부족 / 연산량·메모리 계산기 | 23, 24 |
| KV Cache의 저장량 | 24 |
| Explicit 표와 실제 메모리 / 경로 길이 / 측정 통제 | 25 |
| 실습 목표·범위 / 실행 순서 / 아홉 검사 / 코드 읽는 순서 | 27 |
| 첫 결과를 해석하는 방법 | 28 |
| 실험으로 구조의 필요성 / 질문 고정 | 29 |
| 작은 task / 기록할 최소 필드 / 네 가지 그림 | 30 |
| 최종 프로젝트 제출안 (+ 세 질문) | 31 |
| 구조·입력·학습 목표 비교 / Encoder-only·Decoder-only | 33 |
| ViT / DiT | 34 |
| 후속 구조를 읽는 네 가지 질문 | 35 |
| 다음 학습 방향을 고르는 기준 | 42 |
| 오개념 12–20 / 실무에서 틀리기 쉬운 것 | 36 |
| 더 좋은 설명의 형식 | 37 |
| 개념 확인 11–18 | 38, 39 |
| 마지막 설명 과제 / 기호 사전 / 같은 단어 다른 역할 | 40 |
| 원문 읽는 순서 / 참고 자료 / 출처와 범위 | 42 (+ 노트) |
| 과정 마무리: 계보 1943 → 2017 → 이후, 여섯 질문 | 41, 43 |

개념 확인 01–10은 1–5주차 담당이다. 3569–3689 멘토링 운영안은 과제·구술평가 슬라이드(31, 40)에 반영했다.

## 4. 퀴즈 정답 (개념 확인 11–18)

11 C (위치별 비선형 변환) · 12 A (각 token의 d개 특징) · 13 B (순열 등변성) · 14 C (logits) · 15 A (동시에 성립) · 16 B (Attention 항 4배, 투영·FFN 2배) · 17 C (과거 K/V 재계산 감소) · 18 A (관찰과 인과 검증 구분)

## 5. 참고문헌 (6주차)

[19] He 2015 ResNet · [20] Ba 2016 LayerNorm · [22] Vaswani 2017 · [24] Kingma & Ba Adam · [25] Xiong 2020 Pre-LN · [26] TF Transformer tutorial · [27] PyTorch SDPA · [28] nn.MultiheadAttention · [29] CrossEntropyLoss · [30] LayerNorm · [31] BERT · [32] GPT · [33] T5 · [34] ViT · [35] RoFormer · [36] GLU variants · [37] GQA · [38] FlashAttention · [39] Jain & Wallace · [40] Wiegreffe & Pinter · [41] DiT

## 6. 슬라이드별 개요와 발표자 노트 (빌드된 덱에서 추출)

### 1. Week 6. Transformer 완성: 학습·추론·그 이후

오른쪽: →
왼쪽: ←
위쪽: ↑
아래쪽: ↓
좌우 양방향: ↔ ⇔
상하 양방향: ↕
대각선: ↗ ↘ ↖ ↙

### 2. 지난 주 복습: Attention의 핵심

지난 주에는 Seq2Seq의 고정 문맥 벡터 병목에서 출발해 Attention을 가중합으로 이해했고, Q/K/V 투영과 Multi-head의 shape를 d=8, H=2, N=5 예시로 추적했습니다. 오늘은 그 Attention 블록이 실제 Transformer가 되기 위해 필요한 나머지 부품(FFN, Residual, LayerNorm, Mask)과 학습·추론 절차를 완성합니다. 시작 전에 학생에게 QKᵀ의 shape와 Softmax 축을 한 번 더 말하게 하면 좋습니다.

### 3. 오늘의 위치: 2017년 원형과 그 이후

5주차까지는 2014년 Attention에서 2017년 Transformer의 핵심 연산까지 왔습니다. 오늘은 2017년 원형의 블록을 끝까지 조립하고 학습·추론을 다룬 뒤, 2018년 BERT·GPT, 2020년 ViT와 Pre-LN 분석(Xiong 등), 2022년 FlashAttention과 DiT(arXiv 2022, ICCV 2023)로 이어지는 길을 봅니다. 이후 연구는 최신 순위표가 아니라 원형과 무엇이 달라졌는지 비교하는 틀로만 다룬다는 점을 먼저 밝힙니다.

### 4. 학습 목표

오늘 목표는 여섯 가지입니다. 앞의 다섯은 2017년 원형 Transformer를 입력부터 다음 토큰까지 완전히 설명하는 것이고, 마지막은 그 지식을 실험과 후속 모델 읽기로 옮기는 것입니다. 수업 끝에 빈 종이에 전체 구조를 그리는 과제로 목표 달성 여부를 확인합니다.

### 5. Week 6 · Part 01

첫 파트에서는 Attention 주변의 부품을 채웁니다. FFN, Residual, LayerNorm으로 한 블록을 완성하고, Decoder 학습에 꼭 필요한 target shift와 mask를 다룹니다. 원자료 14–15장에 해당합니다.

### 6. FFN: 위치별 비선형 변환

FFN은 각 위치에 똑같이 적용되는 2층 MLP입니다. d=512를 d_ff=2048로 넓혔다가 다시 512로 줄이는데, 마지막이 d로 돌아와야 residual 합이 가능합니다. FFN 자체는 위치 간 결합을 하지 않지만, 입력 x가 이미 Attention을 거쳐 다른 토큰 정보를 담고 있을 수 있습니다. '토큰 믹싱 vs 특징 변환'은 첫 설명으로 좋지만 Q/K/V 투영도 특징을 바꾼다는 점을 함께 말해 줍니다.

### 7. LayerNorm은 어느 축을 정규화하나

LayerNorm(d)는 (B,N,d) 입력에서 각 토큰의 마지막 d축으로 평균과 분산을 구합니다. BatchNorm처럼 배치 전체의 같은 특징을 묶지 않습니다. x=(1,2,3,4)로 손계산하면 평균 2.5, 분산 1.25이고 정규화 결과는 약 ±1.34, ±0.45입니다. γ=2, β=1을 적용하면 평균 1, 분산 4가 되므로 최종 출력이 항상 평균 0·분산 1일 필요는 없습니다. γ, β는 토큰마다 따로 있는 것이 아니라 특징 축에 공유됩니다. [20][30]

### 8. Residual과 Post-LN vs Pre-LN

Residual은 기존 표현을 보존하는 통로입니다. 더하려면 shape가 같아야 하므로 원형의 모든 sublayer는 d차원으로 돌아옵니다. Post-LN은 합한 뒤 정규화하고(y=LN(x+F(x))), Pre-LN은 sublayer 입력을 정규화한 뒤 더합니다(y=x+F(LN(x))). Pre-LN에서는 잔차 경로에 정규화가 끼지 않아 초기 gradient가 안정적이라는 분석이 있지만, 한 설정의 결과로 보편적 우열을 결론 내리지 않도록 합니다.

### 9. Decoder 입력과 정답을 한 칸 어긋나게

설명용 문장 I am a student로 Decoder 입력은 BOS부터, 정답은 EOS까지 한 칸 어긋나게 둡니다. 학습 때 이전 정답을 입력으로 쓰는 것을 teacher forcing이라 합니다. 정답 prefix가 모두 있으므로 위치별 예측을 병렬로 계산하고, causal mask로 미래 접근만 막습니다. 생성 때는 다음 입력이 아직 없으므로 순차성이 남고, 층 사이의 의존성도 있으므로 '모든 계산을 한 번에 병렬화한다'고 말하지 않습니다. [26]

### 10. Causal mask는 Softmax 이전에: −∞

정답 누출 탐지기 그림에서 행은 Query 위치, 열은 참조할 Decoder 입력 위치입니다. 예측할 위치 2(입력 I, 정답 am)는 BOS와 I만 볼 수 있습니다. 차단은 Softmax 전에 점수에 −∞를 더하는 방식이어야 exp(−∞)=0으로 가중치가 사라집니다. 점수를 0으로 바꾸면 exp(0)=1이라 미래 가중치가 남습니다. FP16에서 큰 음수를 직접 쓸 때는 dtype 범위와 수치 안정성을 확인합니다. 실습으로 causal mask만 제거해 보면 훈련 손실은 낮아지지만 실제 생성은 망가지는 누출 효과를 볼 수 있습니다(결과 정도는 데이터에 따라 다름). [27]

### 11. Causal · Padding · Loss mask는 다르다

네 가지 mask는 막는 대상과 적용 위치가 다릅니다. Key padding mask는 PAD 위치를 Key로 참조하지 못하게 할 뿐, PAD 위치 Query의 출력을 자동으로 0으로 만들지 않으므로 loss·pooling·평가에서 별도로 빼야 합니다. API마다 boolean 의미가 반대라는 점도 중요합니다. PyTorch scaled_dot_product_attention은 True가 허용, nn.MultiheadAttention의 attn_mask/key_padding_mask는 True가 차단입니다. 이 강의 실습 코드는 allow=True(허용)로 통일합니다. [27][28][29]

### 12. Week 6 · Part 02

두 번째 파트는 원자료 16–17장입니다. 한 층의 수식, 출력 head, 한 샘플의 shape 추적, 파라미터 수를 유도한 뒤 학습 손실과 한 학습 step, 원논문의 학습 조건과 지표를 다룹니다.

### 13. Encoder 한 층, Decoder 한 층

Encoder 층은 self-attention과 FFN 두 sublayer, Decoder 층은 masked self-attention, cross-attention, FFN 세 sublayer입니다. 여기서 MHA(Q원본,K원본,V원본)는 내부 투영을 포함한 모듈 표기입니다. Cross-attention의 K, V는 Encoder stack의 최종 출력 E에서 오며, 각 Decoder 층은 자신만의 cross-attention 투영 가중치를 가집니다. 마지막 선형층 W_vocab이 d를 |V|개 점수로 바꾸고 softmax가 다음 토큰 확률을 줍니다. 모든 Transformer가 weight tying을 쓰는 것은 아닙니다. [22 §3.1, §3.4]

### 14. 한 샘플을 끝까지 추적하기

5주차의 d=8, H=2 설정으로 한 배치를 끝까지 따라갑니다. Cross-attention 표 (2,2,3,5)는 T=3개 Query가 S=5개 source Key를 보는 표이고, 출력은 Query 길이 3을 유지합니다. 보드 활동: 빈 Encoder/Decoder 박스를 보여 주고 Attention의 출처, mask, residual, FFN, output head를 채우게 한 뒤 '어느 단계에서 길이가 바뀌나?'를 묻습니다.

### 15. 파라미터 수를 직접 유도하기

Self-attention의 네 투영 행렬이 4d², FFN이 2d·d_ff이므로 d_ff=4d이면 Encoder 층 약 12d², cross-attention이 더해진 Decoder 층 약 16d²입니다. Base에 대입하면 층당 3.15M, 4.19M이고 12개 층 합이 약 44M입니다. 약 37,000개 공유 BPE 어휘 embedding(약 18.9M)을 더하면 63M 정도로, 논문의 65M과 가깝습니다(bias·Norm 포함 여부에 따라 차이). Python으로 재계산해 확인한 수치입니다. [22 §3, Table 3]

### 16. 다음 토큰의 음의 로그 가능도

학습 목표는 각 위치에서 정답 다음 토큰의 로그 확률을 높이는 것, 즉 음의 로그 가능도(NLL)를 줄이는 것입니다. PAD가 아닌 토큰 수로 정규화하며, 긴 시퀀스와 짧은 시퀀스를 어떤 단위로 평균하는지에 따라 가중이 달라지므로 집계 규칙을 명시합니다. PyTorch CrossEntropyLoss는 softmax 전 logits를 받습니다. 예시에서 네 토큰의 평균 NLL 0.69는 perplexity 약 2, 즉 '평균적으로 두 후보 중 고르는 정도의 불확실성'으로 읽을 수 있습니다. [29]

### 17. 한 학습 step의 순서

한 step은 train 모드 → gradient 초기화 → forward → masked cross-entropy → backward → (clipping) → optimizer step 순서입니다. logits (B,T,|V|)를 (B·T,|V|)로, 정답을 (B·T)로 펼쳐 class 축을 맞춥니다. 평가 때 model.eval()과 torch.no_grad()는 서로 다른 일을 하므로 둘 다 필요할 수 있습니다. [27][29]

### 18. 원논문의 학습 조건

원논문은 Adam(β₁=0.9, β₂=0.98, ε=10⁻⁹)과 warm-up 후 감소하는 학습률을 씁니다. d=512, w=4000이면 최고 학습률은 약 7.0×10⁻⁴입니다(재계산). Label smoothing은 정답을 확률 1로 몰지 않게 하며, 논문은 perplexity는 나빠지지만 정확도와 BLEU는 좋아진다고 보고합니다. 학습 loss 하나가 평가 목표 전체를 대변하지 않는다는 사례입니다. 이 조건들은 모델 구조와 별개인 실험 조건입니다. [22 §5–6][24]

### 19. 어떤 지표를 기록할까

Perplexity는 raw NLL로 계산해야 해석이 됩니다. Token accuracy는 teacher forcing 조건의 값이라 실제 생성 성능과 다릅니다. 학습 loss가 떨어지지 않으면 층 수나 GPU를 늘리기 전에 작은 샘플 과적합부터 확인하고, 그마저 안 되면 데이터 정렬, target shift, mask 방향, logits shape, ignore_index, optimizer에 파라미터가 들어갔는지를 점검합니다.

### 20. Week 6 · Part 03

세 번째 파트는 원자료 18–19장입니다. 자기회귀 생성과 토큰 선택 정책, KV Cache의 정확한 역할, 그리고 O(N²)만으로는 부족한 비용 분석을 다룹니다.

### 21. 추론: 토큰을 하나씩 생성하기

추론에서는 source를 Encoder로 한 번 처리하고 BOS로 Decoder를 시작합니다. 마지막 위치 logits에서 다음 토큰을 골라 prefix에 붙이고, EOS나 최대 길이에서 멈춥니다. 토큰을 고르는 정책은 모델과 별개입니다. 원논문 번역 실험은 beam size 4, length penalty α=0.6을 썼습니다. 정답 prefix를 주었을 때의 token accuracy와 처음부터 생성했을 때의 exact match를 같이 보여 주면 teacher forcing과 생성의 차이를 체감할 수 있습니다. [22 §6.1][26]

### 22. KV Cache: Prefill과 Decode

KV Cache는 과거 토큰의 K, V가 미래 토큰 추가로 바뀌지 않는다는 성질을 이용합니다. Cache를 쓰든 안 쓰든 올바른 구현은 같은 결과를 목표로 하며, 수치 오차·커널 차이 정도만 생길 수 있습니다. Prefill은 주어진 prefix를 한꺼번에 처리하는 단계, Decode는 토큰을 하나씩 늘리는 단계로 병목이 다르므로 TTFT와 token당 지연을 나눠 기록합니다. 이 강의의 Python 실습은 흐름을 보이려고 KV Cache 없이 prefix를 재계산하며, Cache 적용은 확장 과제입니다. [26][37]

### 23. “Transformer는 O(N²)”만으로는 부족하다

길이 N, 폭 d의 dense self-attention 블록에서 주요 행렬 곱을 직접 세면 4Nd² + 2N²d + 2Nd·d_ff MAC입니다. d=512, d_ff=2048에서 N=512이면 투영·FFN 항이 대부분이고, N=4096이 되어야 Attention 항이 가장 커집니다(Python 재계산). 그래서 'O(N²)'만 말하면 짧은 입력에서의 실제 비용 구조를 놓칩니다. 계산기 활동: d를 고정하고 N을 두 배로, 다음엔 N을 고정하고 d를 두 배로 바꿔 각 항이 몇 배가 되는지 먼저 쓰게 합니다.

### 24. KV Cache의 저장량

K와 V를 각각 저장하므로 2가 붙고, 층 수 L, 배치 B, 길이 N, KV head 수 H_kv, head 차원 dₕ, 원소당 bytes를 곱합니다. MHA에서는 H_kv·dₕ = d이므로 2·L·B·N·d·bytes입니다. 원형 Base 디코더(6층, d=512)는 N=1024, FP16에서 12 MiB에 불과하지만, L=32·d=4096 가정의 큰 모델은 N=4096에서 2 GiB, 배치 8이면 16 GiB입니다. GQA로 KV head를 8개로 줄이면 1/4이 됩니다. 순수 K/V 데이터만의 크기이며 allocator·padding·metadata는 제외입니다. [37]

### 25. 측정할 때 구분할 것

연산량 계산기 값은 이론 추정이지 실제 지연·GPU peak memory 예측기가 아닙니다. FlashAttention은 정확한 attention을 IO 효율적으로 계산할 뿐, dense 상호작용의 산술량을 줄이지는 않습니다. 경로 길이가 짧다는 것과 원하는 의미 관계를 잘 학습한다는 것은 다릅니다. 실험에서는 조건을 기록하고, 식으로 비율을 예측한 뒤 실행 시간은 따로 잽니다.

### 26. Week 6 · Part 04

네 번째 파트는 원자료 20–21장입니다. 교육용 transformer_lab.py를 실행하고 검사하며 결과를 해석한 뒤, ablation 실험과 최종 프로젝트를 설계합니다.

### 27. 실습: 작은 Transformer 실행

실습 파일은 명시적 Q/K/V, causal·padding mask, Post-LN, sinusoidal position, cross-attention, loss, greedy generation을 모두 포함하는 작은 Encoder–Decoder입니다(d=64, H=4, 각 2층, 출력 head는 embedding과 묶지 않음). 먼저 --mode check로 아홉 검사를 통과시키고 학습합니다. 검사에서는 dropout을 끄고 허용 오차를 명시합니다. 자료 제작 시 PyTorch 2.10.0/CPU에서 아홉 검사를 통과했지만, 이것이 다른 장치의 성능이나 400 step 수렴을 보장하지는 않습니다. 코드 리뷰는 mask·shape·loss/metric·generation을 한 명씩 맡겨 설명하게 합니다.

### 28. 첫 결과를 해석하는 방법

원자료 제작 시 실제 실행 사례입니다. 각 길이 구간 평가 예시는 72개이며, 9–12 구간의 token accuracy는 33.82%였습니다. 400 step은 실행 예시일 뿐 충분한 학습의 보장이 아니고, 이 결과만으로 Transformer의 구조적 한계를 결론 내리지 않습니다. 교육용 코드는 mask 검증을 위해 GPU 동기화가 있으므로 그대로 성능 벤치마크로 쓰지 않습니다.

### 29. 실험으로 구조의 필요성 확인하기

'Transformer가 더 좋다'가 아니라 통제된 비교 질문으로 바꿉니다. RNN Seq2Seq, Attention Seq2Seq, 작은 Transformer를 비교할 수 있고, 구현이 부담스러우면 기준 모델을 제공하고 한 모델만 작성하게 합니다. Pre-LN/Post-LN 비교도 한 설정으로 보편적 우열을 결론 내리지 않습니다. [25]

### 30. 작은 task와 기록 규칙

작은 task부터 시작합니다. 복사는 output=input, 반전은 순서 뒤집기, 기호 치환은 정해진 매핑으로 토큰을 바꾸는 과제로 필요한 순서 정보가 다릅니다. seed 개수만 늘린다고 편향된 실험이 해결되지는 않습니다. 그래프의 범위를 바꿔 효과를 과장하지 않도록 하고, 각 그림은 한 가지 질문만 답하게 분리합니다.

### 31. 최종 프로젝트 제출안

배점은 멘토링 운영을 위한 제안입니다. 예상과 다른 결과를 얻어도 실험 조건과 가능한 설명을 정확히 정리했다면 좋은 연구 연습이며, 정해 둔 결론에 맞춰 데이터나 조건을 숨기지 않습니다. 구술 평가에서는 처음 보는 d, H, S, T 설정으로 입력부터 logits까지 추적하게 하고, 위치 정보 제거·잘못된 mask·KV Cache 추가 중 하나의 효과를 설명하게 합니다.

### 32. Week 6 · Part 05

마지막 파트는 원자료 23–27장입니다. 후속 구조를 원형과 비교하는 틀을 세우고, 오개념·개념 확인·마지막 설명 과제로 과정 전체를 정리합니다.

### 33. 세 가지 조립 방식

BERT, GPT, T5는 같은 부품을 쓰지만 mask와 학습 목표, output head, 데이터가 함께 다릅니다. BERT의 masked language modeling은 입력에서 가린 위치를 복원하는 목표라서, '미래 정답을 보고 다음 토큰을 예측하는' 누출과 다릅니다. 각 설명은 대표 원형 연구 기준이며 모든 후속 변형의 정의는 아닙니다. [31][32][33]

### 34. ViT와 DiT: 무엇을 token이라 부를까

이미지를 16×16 patch로 나누면 224×224 이미지는 14×14=196개 patch가 되고, 각 patch(16·16·3=768개 값)를 선형 투영해 token으로 씁니다. CLS 사용, 위치 임베딩, pooling은 모델별로 확인해야 하며 모든 Vision Transformer가 CLS를 갖는 것은 아닙니다. ViT는 arXiv 2020, ICLR 2021입니다. DiT는 diffusion의 denoising 예측에 Transformer block을 쓰며, timestep과 class 조건을 넣는 방식을 비교합니다. [34 §3][41 §3]

### 35. 원형과 후속 변형을 구분하기

후속 변형이 존재한다고 특정 조합이 모든 모델의 표준이라는 뜻은 아닙니다. 각 변형을 원형 표의 한 칸에 꽂아 넣고 무엇이 바뀌는지 설명할 수 있을 정도로만 다룹니다. SwiGLU 등 GLU 변형(Shazeer 2020), RoPE(Su 등 2021), GQA(Ainslie 등 2023), FlashAttention(Dao 등 2022)이 대표 예입니다. GQA는 Grouped-query Attention이며 시각 질의응답 데이터셋 GQA와 다릅니다. 강의 목표를 달성하기 전에는 세부 구현까지 확장하지 않습니다. [35][36][37][38]

### 36. 자주 생기는 오개념: Transformer 편

원자료의 오개념 20가지 중 6주차 내용과 직결되는 것들입니다. 실무에서 추가로 틀리기 쉬운 것: softmax(dim=-1)의 마지막 축이 정말 Key 축인지, reshape가 token과 head를 의도대로 합치는지, model.eval()과 gradient 비활성화의 구분, padding mask와 loss의 PAD 제외 둘 다 적용했는지, teacher forcing 평가를 생성 성능으로 보고하지 않았는지. 경고 신호: 너무 빨리 낮아지는 loss, PAD를 맞히는 높은 accuracy, EOS 없이 계속되는 생성, 모든 위치가 비슷한 출력.

### 37. 더 좋은 설명의 형식

강의와 보고서에서 쓰는 문장의 형식을 바꾸는 연습입니다. '이해한다', '항상'처럼 검증 범위를 넘는 표현 대신, 어떤 입력·장치·조건에서 무엇을 관찰·측정했는지를 씁니다. Attention 가중치에는 V의 크기와 방향, output projection, residual과 후속 층도 관여하므로 큰 가중치 하나로 인과를 결론 내리지 않습니다.

### 38. 개념 확인 11–14

원자료 개념 확인 11–14번입니다. 정답보다 틀린 보기가 왜 틀렸는지 계산 언어로 설명하게 합니다.

[정답]
Q1. FFN은 어떤 계산인가? (A) 위치 간 Value 가중합 (B) 시간 step 순환 갱신 (C) 각 위치 특징의 비선형 변환
  → C. 동일 FFN을 각 위치에 적용 — 입력에 문맥이 있을 수 있지만 FFN 자체는 새 위치 결합을 하지 않는다.
Q2. LayerNorm(d)의 전형적인 정규화 범위는? (A) 각 token의 d개 특징 (B) Batch 전체의 같은 특징 (C) token ID 번호
  → A. (B,N,d) 입력이면 마지막 d축의 평균·분산.
Q3. 위치·mask가 없는 self-attention에서 입력 순서를 섞으면? (A) 출력이 완전히 같다 (B) 출력도 같은 순열로 섞인다 (C) 0이 된다
  → B. SA(PX) = P·SA(X), 순열 등변성 — 불변성과 구분.
Q4. CrossEntropyLoss에 일반적으로 전달하는 값은? (A) softmax를 두 번 한 확률 (B) argmax token ID (C) 정규화 전 logits
  → C. logits를 전달하고 PAD 제외(ignore_index)와 class 축을 확인.

### 39. 개념 확인 15–18

원자료 개념 확인 15–18번입니다. 16번은 4Nd² + 2N²d + 2Nd·d_ff 식에 N 대신 2N을 넣어 직접 확인하게 합니다.

[정답]
Q1. 병렬 학습과 자기회귀 생성은? (A) 동시에 성립할 수 있다 (B) 서로 모순이다 (C) 둘 다 미래 정답이 필요하다
  → A. 학습은 정답 prefix가 주어져 위치별 병렬, 생성은 다음 입력이 아직 없어 순차.
Q2. d를 고정하고 N을 2배로 하면 주요 항은? (A) 모두 4배 (B) Attention 곱셈 항 4배, 투영·FFN 항 2배 (C) 모두 2배
  → B. N²d와 Nd² 항이 함께 있다. 실제 시간에는 overhead·kernel 특성도 작용.
Q3. KV Cache가 하는 일은? (A) 미래 정답을 미리 저장 (B) Attention을 제거 (C) 과거 위치의 K/V 재계산을 줄임
  → C. 새 Query의 문맥 참조와 자기회귀 루프는 남는다.
Q4. 큰 Attention 가중치를 관찰했다면? (A) 큰 참조 비중이 '관찰'되었다고 말하고 인과는 추가 검증 (B) 유일한 원인 (C) 사람처럼 이해
  → A. V·output projection·residual·후속 층도 관여 — 관찰과 인과 검증을 구분.

### 40. 마지막 설명 과제와 기호 사전

이번 주 과제이자 과정의 마지막 과제입니다. 빈 종이에 입력 ID부터 다음 토큰까지 그리고 각 구간의 shape, 학습 파라미터, mask를 적은 뒤 학습과 생성의 차이를 다른 사람에게 설명합니다. 설명 중 막힌 위치가 복습할 장입니다. 그림에는 입력·출력 shape, 학습되는 파라미터, 정보가 이동하는 방향, mask가 막는 연결 네 가지를 반드시 적습니다. 오른쪽 기호 사전으로 표기를 통일합니다. 'Layer'가 block 전체인지 sublayer인지, 0-based인지 1-based인지도 명시하게 합니다.

### 41. 과정 전체의 계보: 1943 → 2017 → 이후

과정 전체를 한 장으로 되돌아봅니다. 규칙을 다 쓰지 않고 배울 수 있을까(1주, 학습·Tensor) → 직선으로 안 되는 문제는(2주, Perceptron과 MLP·역전파) → 공간 구조는(3주, CNN·ResNet·정규화) → 순서와 먼 기억은(4주, RNN·LSTM·Seq2Seq) → 필요할 때 원문을 찾아보면(5주, Attention) → 참조만으로 시퀀스 표현을 만들면(6주, Transformer)의 순서였습니다. 연도는 대표 논문 기준이며 역전파가 1986년에 처음 발명된 것은 아니고, Word2Vec이 embedding을 처음 만든 것도 아닙니다. 2017년 이후 칸은 확장 학습으로 구분합니다.

### 42. 다음 학습 방향과 읽을 원문

관심사에 따라 다음 방향을 고릅니다. 언어 생성이면 Decoder-only와 KV Cache, 시각이면 patch·공간 위치·CLS와 pooling, 최적화면 실제 병목·kernel·메모리 이동, 생성 모델이면 diffusion 목표와 timestep conditioning입니다. 처음부터 모든 논문의 모든 실험을 읽기보다 질문에 맞는 그림·식·절을 지정해 읽습니다. 공식 구현 참고: TensorFlow Transformer 튜토리얼 [26], PyTorch SDPA·MultiheadAttention·CrossEntropyLoss·LayerNorm 문서 [27–30]. API 문서는 버전마다 바뀔 수 있으므로 설치한 버전에서 mask와 shape 규약을 다시 확인합니다. 원자료의 식·손계산·toy model 결과는 교육용 재구성이며 원논문의 실험 결과가 아닙니다.

### 43. 오늘의 정리 · 과정의 정리

오늘은 2017년 원형을 입력 ID부터 다음 토큰까지 완성했고, 학습과 추론의 차이, 비용 분석, 후속 구조 읽는 법까지 다뤘습니다. 6주 과정 전체로 보면 '왜 이 계산이 필요한가?'라는 질문에 답하며 Tensor에서 Transformer까지 왔습니다. 다음 주는 없으며, 최종 프로젝트 발표와 구술 평가로 과정을 마무리합니다.

### 44. Question ?

(템플릿 슬라이드)
