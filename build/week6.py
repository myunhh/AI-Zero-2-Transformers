"""Week 6 — Transformer 완성: 조립·학습·생성 — 참조만으로 만들면? (논문으로 배우는 판)

근거: build/research/papers/week6.md (Vaswani 2017 v1–v7 대조, Adam, label smoothing, Xiong 2020, GPT-1, BERT, T5,
ViT, DiT, MQA, GQA, FlashAttention, Pope 2022, GLU variants, RoPE). 새 그림: build/paper_figs_w6.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deckkit  # noqa: E402
deckkit.use_theme("clean")  # Apple 디자인 원칙 테마 — import * 보다 먼저
from deckkit import *  # noqa

A = lambda p: os.path.join(HERE, "assets", p)
OUT = os.path.join(HERE, "..", "lectures", "week06_transformer_complete.pptx")

d = Deck(6, "Transformer 완성: 조립·학습·생성", date="2026-11-09", theme="clean")
for _t in d.prs.slides[0].shapes._spTree.iter(qn("a:t")):  # 표지 제목: '학/습' 중간 줄바꿈 대신 콜론 뒤에서 나눈다
    if _t.text == d.title:
        import copy as _copy
        _r = _t.getparent()
        _r2 = _copy.deepcopy(_r)
        _t.text, _r2.find(qn("a:t")).text = "Transformer 완성:", "조립·학습·생성"
        _br = _r.makeelement(qn("a:br"), {})
        if _r.find(qn("a:rPr")) is not None:
            _br.append(_copy.deepcopy(_r.find(qn("a:rPr"))))
        _r.addnext(_br)
        _br.addnext(_r2)
        break

V17 = "Vaswani et al. (2017) Attention Is All You Need, arXiv:1706.03762 v7 (v1–v6 대조)"

# ============================================================ 도입
d.question("참조만으로\n시퀀스 모델을 만들면?",
           "2017 Attention Is All You Need → 학습 · 결과 · 생성 비용 · 그 이후의 논문들",
           notes="마지막 주. 지난주의 attention에 FFN·잔차·LayerNorm을 붙여 층을 완성하고(Vaswani 2017 §3), 어떻게 학습시켰는지(§5, Adam, label smoothing), "
                 "무엇을 얼마의 비용으로 얻었는지(§6)를 원문 표로 확인한다. 그다음 원형이 남긴 문제를 푼 논문들 — Post-LN 학습 불안정(Xiong 2020), "
                 "생성 비용(Shazeer 2019, Pope 2022, Ainslie 2023, Dao 2022) — 과 2017 이후의 조립 방식(GPT-1, BERT, T5, ViT, DiT, GLU, RoPE)을 본다. "
                 "출처: build/research/papers/week6.md 주차 요약.")

d.bridge(["**Attention**: 점수 → softmax → 가중합", "Q · K · V, **Multi-head** (B, H, N, d_h)", "Self-attention + **위치 인코딩**"],
         ["attention만으로는 **위치별 비선형 변환**이 없다", "깊게 쌓기 · 정답을 **훔쳐보지 않고** 학습 · **생성**", "실제로 학습시키면 결과와 비용은?"],
         ["**참조만으로**", "**시퀀스 모델을 만들면?**", "Vaswani et al. (2017)을 처음부터 끝까지 읽는다"],
         notes="5주차 복습: Bahdanau의 attention, Q/K/V, scaled dot-product, multi-head, self-attention과 위치 인코딩(Vaswani §3.2, §3.5까지). "
               "남은 문제: (1) attention 출력은 Value의 가중합이라 위치별 비선형 변환이 따로 필요하다 — §3.3 FFN, (2) 깊게 쌓으려면 잔차·정규화 — §3.1, "
               "(3) Decoder가 정답을 보지 않게 — §3.1 mask + offset, (4) 어떻게 학습하고 결과가 어땠나 — §5, §6. "
               "출처: Vaswani et al. (2017) §3.1–§3.5, §5, §6.")

d.roadmap(["Vaswani §3 — Encoder·Decoder 조립", "Vaswani §5 + Adam + Label smoothing — 학습", "Vaswani §6 — 결과와 비용",
           "Xiong (2020) — Post-LN vs Pre-LN", "생성 비용 — MQA · KV cache · GQA · FlashAttention", "이 과정의 실험 · 2017 이후 · 마무리"],
          ["원형 Encoder/Decoder 층의 **모든 sublayer와 shape**을 그린다",
           "**shift + causal mask**, 공유 임베딩과 √d_model을 설명한다",
           "파라미터 수와 학습률 최고점을 **직접 계산**하고 원문과 비교한다",
           "원문 **Table 2·3**을 읽고 무엇이 증명되고 무엇이 아닌지 말한다",
           "KV cache 크기와 MQA/GQA·FlashAttention이 줄이는 것을 구분한다"],
          notes="여섯 질문 중 마지막. 오늘은 한 편의 논문(Vaswani 2017)을 절 순서대로 읽고, 그 논문이 남긴 문제를 푼 후속 논문으로 넘어간다. "
                "끝나면 할 수 있어야 하는 것은 오른쪽 다섯 가지 — 수업 끝 셀프 체크에서 다시 확인한다. 출처: week6.md 읽기 안내(§3.1 + Fig. 1 → §5 → §6.2 Table 3).")

d.paper_map([("2015", "Kingma & Ba — **Adam** · Szegedy et al. — **Label smoothing**", "Transformer의 optimizer와 정답 완화",
              "학습률 하나로 모든 파라미터를 · one-hot 과신"),
             ("2017", "Vaswani et al. — **Attention Is All You Need**", "조립(§3) · 학습(§5) · 결과(§6)", "RNN의 순차 계산 → 병렬화 불가"),
             ("2018–20", "Radford — **GPT-1** · Devlin — **BERT** · Raffel — **T5**", "세 가지 조립 방식과 사전학습 목표",
              "레이블 부족 · 단방향 · 과제마다 다른 형식"),
             ("2019", "Shazeer — **Multi-Query Attention**", "생성 때의 메모리 대역폭", "매 step 큰 K/V를 다시 읽는다"),
             ("2020", "Xiong et al. — **Post-LN vs Pre-LN**", "warm-up이 왜 필요한가", "원형은 warm-up 없이 발산"),
             ("2020–21", "Shazeer — **GLU variants** · Su — **RoPE**", "FFN과 위치 정보의 변형", "ReLU FFN · 덧셈형 위치"),
             ("2020–23", "Dosovitskiy — **ViT** · Peebles & Xie — **DiT**", "이미지 patch를 token으로", "CNN · U-Net 의존"),
             ("2022–23", "Dao — **FlashAttention** · Pope — 추론 · Ainslie — **GQA**", "IO · KV cache · head 공유", "N×N 표의 HBM IO · MQA 품질")],
            notes="시간 순서. 각 논문이 바로 앞의 어떤 한계를 풀었는지 한 줄씩. Adam(ICLR 2015, arXiv:1412.6980), Label smoothing(Szegedy et al., CVPR 2016 §7), "
                  "Vaswani(NIPS 2017), GPT-1(OpenAI 보고서 2018), BERT(NAACL 2019), T5(JMLR 2020), MQA(arXiv:1911.02150, 2019), Xiong(ICML 2020), "
                  "GLU variants(arXiv:2002.05202, 2020), RoPE(arXiv:2104.09864, 2021), ViT(ICLR 2021), DiT(ICCV 2023), FlashAttention(NeurIPS 2022), "
                  "Pope(MLSys 2023), GQA(EMNLP 2023). 출처: week6.md 주차 요약 표.")

d.glossary([["FFN", "토큰마다 같은 2층 MLP (d → d_ff → d)", "각자 자리에서 하는 정리"],
            ["Post-LN / Pre-LN", "LayerNorm을 잔차 합 뒤 / sublayer 앞에", "정리를 나중에 / 먼저"],
            ["Teacher forcing", "학습 때 이전 **정답** 토큰을 입력으로", "정답지를 한 칸씩 보여 주며 연습"],
            ["Causal mask", "미래 위치 점수를 −∞로 (softmax 전)", "아직 안 쓴 답안 가리기"],
            ["NLL · Perplexity", "정답 토큰의 −log 확률 평균 · 그 exp", "평균 놀람 · 헷갈리는 후보 수"],
            ["Warm-up", "처음 몇 천 step 동안 학습률을 서서히 올림", "출발 전 예열"],
            ["Label smoothing", "정답 확률 목표를 1 대신 1 − ε 근처로", "“100% 확신은 금지”"],
            ["BLEU", "기계 번역과 사람 번역의 n-gram 겹침 점수 (0–100)", "번역 채점표"],
            ["Beam search", "후보 문장 여러 개(beam)를 동시에 유지하며 생성", "여러 갈래 길을 함께 탐색"],
            ["KV cache", "생성 중 과거 토큰의 K, V를 저장해 재사용", "이미 쓴 메모 다시 보기"]],
           notes="오늘 처음 나오는 용어. 막히면 이 표로 돌아온다. BLEU는 원논문 Table 2·3의 지표(newstest2014/2013)이고 perplexity는 Table 3 PPL 열(wordpiece 단위). "
                 "warm-up·label smoothing은 Vaswani §5.3–5.4, beam search는 §6.1(beam 4, α 0.6). 출처: Vaswani et al. (2017) §5, §6.")

# ============================================================ Part 1 — Vaswani §3
d.part(1, "Vaswani et al. (2017) §3 — 조립", "attention 블록에 무엇을 더해야 깊은 Encoder–Decoder가 되나?",
       notes="Part 1: 원논문 §3.1(스택), §3.3(FFN), §3.4(임베딩·softmax), §3.2.3(mask)을 읽으며 그림 1의 상자를 하나씩 채운다. 출처: " + V17)

d.paper("Vaswani et al. (2017)", "Attention Is All You Need", "NIPS 2017 · arXiv:1706.03762 (v1 2017-06 → 현행 v7 2023-08)",
        "RNN Encoder–Decoder는 h_t가 h_(t−1)을 기다리는 **순차 계산** — 한 문장 안에서 병렬화가 안 된다 (§1)",
        "recurrence·convolution 없이 **attention + 위치별 FFN + 잔차 + LayerNorm**만으로 Encoder–Decoder (§3)",
        "§3.1 + Figure 1 → §5 (1쪽) → §6.2 Table 3",
        url="arxiv.org/abs/1706.03762",
        result="WMT14 영→독 BLEU **27.3**(base) · **28.4**(big) — base는 P100 8장 **12시간** (§5.2, Table 2)",
        notes="서지: Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin. NIPS 2017, arXiv:1706.03762. 오늘은 v7(2023-08)을 주 판본으로, v1–v6과 대조한 숫자만 쓴다. "
              "문제: 지배적인 시퀀스 변환 모델은 RNN/CNN Encoder–Decoder + attention이고, RNN은 순차 계산이라 병렬화가 어렵다(§1 2단락). "
              "주의: attention 자체는 이 논문이 처음이 아니다 — Bahdanau 2014 등 기존 Encoder–Decoder에 이미 있었다(§1, §2). 새로운 점은 recurrence/convolution을 완전히 없앤 것. "
              "EN-DE 27.3/28.4는 모든 판본에서 같다. 출처: Vaswani (2017) Abstract, §1, §5.2, Table 2.")

s = d.slide("Figure 1: 오늘 채울 그림", lead="Encoder 층 = self-attention + FFN · Decoder 층 = masked self + cross + FFN — 모두 Add & Norm",
            stage="아이디어",
            notes="원문 Figure 1 기반 재구성. §3.1: Encoder는 같은 층 N = 6개, 층마다 sublayer 2개(multi-head self-attention, position-wise FFN). "
                  "각 sublayer 출력은 LayerNorm(x + Sublayer(x)) — 잔차를 더한 뒤 정규화(Post-LN). 잔차를 위해 모든 sublayer와 임베딩 출력이 d_model = 512. "
                  "Decoder도 N = 6, Encoder의 두 sublayer 사이에 Encoder 출력 위의 multi-head attention(cross-attention)을 세 번째로 추가. "
                  "base 설정은 Table 3 첫 행: N 6, d_model 512, d_ff 2048, h 8, d_k = d_v 64, P_drop 0.1, ε_ls 0.1, 100K step, 65M. "
                  "출처: Vaswani (2017) §3.1, Figure 1, Table 3 (base 행).")
L, R = s.cols(0.56)
s.image(A("week6/encdec_layer.png"), L)
s.table(["원형 base (Table 3)", "값"], [["층 수 N (Encoder / Decoder)", "6 / 6"], ["d_model / d_ff", "512 / 2048"],
                                      ["head 수 h / d_k = d_v", "8 / 64"], ["P_drop / ε_ls", "0.1 / 0.1"],
                                      ["학습 step / 파라미터", "100K / 65M"]], Box(R.x, R.y, R.w, 2.6), size=15, align="lc")
s.bullets(["모든 sublayer 출력: **LN(x + Sublayer(x))** (§3.1)", "잔차를 위해 모든 출력이 **d_model = 512**",
           "attention 자체는 새것이 아니다 (Bahdanau 2014) — **recurrence를 없앤 것**이 새롭다"],
          Box(R.x, R.y + 2.85, R.w, R.h - 2.85), size=15)

s = d.slide("§3.3 FFN: 모은 정보를 위치마다 변환", lead="FFN(x) = max(0, xW1 + b1)W2 + b2 (Eq. 2) — 2주차 MLP를 위치마다 똑같이",
            stage="계산",
            notes="§3.3: 각 층에는 위치마다 따로, 똑같이 적용되는 FFN이 있다 — ReLU를 사이에 둔 선형 변환 두 개(Eq. 2). 위치끼리는 같은 파라미터, 층마다는 다른 파라미터. "
                  "논문은 이것을 'kernel size 1인 convolution 두 개'로도 설명한다. d_model = 512, 안쪽 d_ff = 2048. "
                  "FFN은 한 위치의 특징 축만 변환하고 다른 위치와 섞지 않는다 — 위치 간 결합은 attention의 가중합이 한다. "
                  "다만 attention의 투영 W_Q, W_K, W_V, W_O도 특징을 바꾼다는 점을 함께 기억. ReLU 대신 GEGLU/SwiGLU는 Part 7(Shazeer 2020). "
                  "출처: Vaswani (2017) §3.3 Eq. 2; Shazeer (2020) Eq. 6.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("FFN(x) = max(0, x W1 + b1) W2 + b2      512 → 2048 → 512", top, size=22)
s.table(["", "Attention (가중합 A·V)", "FFN (§3.3)"],
        [["하는 일", "**위치 간** 정보 결합", "**각 위치**의 비선형 특징 변환 — 2주차 **MLP 그대로**"],
         ["다른 토큰과 섞나?", "예", "**아니오**"], ["shape", "(B, N, d) 유지", "(B, N, d) → (B, N, d_ff) → (B, N, d)"],
         ["파라미터", "W_Q · W_K · W_V · W_O = 4d²", "W1 (d × d_ff) + W2 (d_ff × d) = 2·d·d_ff"],
         ["공유 범위", "한 층 안의 모든 위치", "한 층 안의 모든 위치가 **같은 FFN** — 층마다는 **별개**"],
         ["논문의 다른 설명", "—", "kernel size **1**인 convolution 두 개"]],
        Box(bot.x, bot.y, bot.w, 3.05), size=15, widths=[2.0, 4.0, 6.3])
s.callout("‘attention은 섞기, FFN은 변환’은 좋은 첫 설명 — 단, attention의 투영 W_Q·W_K·W_V·W_O도 **특징을 바꾼다**.",
          Box(bot.x, bot.y + 3.3, bot.w, 0.85), kind="tip", size=15)

s = d.slide("§3.1 Encoder 한 층: 잔차 + LayerNorm", lead="LN(x + Sublayer(x)) — 더하려면 shape이 같아야 하고, LN은 토큰 하나의 d개 값으로 정규화",
            stage="계산",
            notes="§3.1: 각 sublayer 출력은 LayerNorm(x + Sublayer(x)). 잔차 연결(3주차 ResNet)을 쓰려면 입력과 출력의 shape이 같아야 해서 모든 sublayer와 임베딩 출력이 d_model = 512. "
                  "우리 표기(dropout 포함): U = LN(X + Dropout(MHA(X))), X′ = LN(U + Dropout(FFN(U))). §5.4: dropout은 각 sublayer 출력에 — 더하고 정규화하기 전에 — 적용하고, "
                  "Encoder/Decoder 입력의 (임베딩 + 위치 인코딩) 합에도 적용한다. base P_drop = 0.1. "
                  "LayerNorm은 토큰 하나 x ∈ ℝ^d의 평균·분산으로 정규화: (1, 2, 3, 4) → μ 2.5, σ² 1.25 → (−1.34, −0.45, 0.45, 1.34) (검산 완료). "
                  "γ, β는 d차원이고 모든 토큰이 공유한다. '같은 층 반복'은 같은 설계일 뿐 가중치 공유가 아니다. "
                  "출처: Vaswani (2017) §3.1, §5.4; LayerNorm 예는 week6.md 검산 목록.")
top, bot = s.area.top(1.25, gap=0.25)
s.formula(["U  = LN( X + Dropout( MHA(X) ) )", "X′ = LN( U + Dropout( FFN(U) ) )"], top, size=20)
L, R = bot.cols(0.47, gap=0.4)
s.image(A("week6/ln_axis.png"), L)
s.table(["x (토큰 하나)", "μ", "σ²", "(x − μ) / σ"], [["(1, 2, 3, 4)", "2.5", "1.25", "(−1.34, −0.45, 0.45, 1.34)"]],
        Box(R.x, R.y, R.w, 1.0), size=14, align="cccc", widths=[1.45, 0.6, 0.7, 2.85])
s.bullets(["잔차 x + F(x): 더하려면 **같은 shape** → 모든 출력이 **d = 512**",
           "**Dropout** (§5.4): 각 sublayer 출력 + **(임베딩 + PE) 합**에도",
           "γ, β (d차원)는 모든 토큰이 **공유** — batch 축이 아니다",
           "층마다 파라미터는 **별개** (설계만 반복)"], Box(R.x, R.y + 1.25, R.w, R.h - 1.25), size=15)

s = d.slide("§3.1 Decoder: 정답을 한 칸 밀어 넣는다", lead="“output embeddings are offset by one position” — 입력 = BOS + 정답[:-1], 목표 = 정답 + EOS",
            stage="아이디어",
            notes="문제: 학습을 병렬로 하려면 정답 문장 전체를 Decoder에 한 번에 넣고 싶은데, 그러면 각 위치가 자기 정답을 볼 수 있다(정답 누출). "
                  "§3.1 Decoder 단락: self-attention이 뒤 위치를 보지 못하게 mask하고, 출력 임베딩을 한 위치 밀어(offset by one) 위치 i의 예측이 i보다 앞의 출력에만 의존하게 한다. "
                  "이 '이전 정답을 입력으로 주는' 학습을 teacher forcing이라 부른다(논문은 이 용어를 쓰지 않는다 — 강의 용어). "
                  "예: 목표 'I am a student' → Decoder 입력 [BOS, I, am, a, student], 예측 정답 [I, am, a, student, EOS]. 대각선(현재 입력)은 봐도 된다 — 목표가 한 칸 앞이다. "
                  "학습은 정답 prefix가 모두 있으므로 모든 위치를 한 번에, 생성은 다음 입력이 아직 없으므로 순차적 — 둘은 모순이 아니다. "
                  "출처: Vaswani (2017) §3.1 Decoder 단락.")
top, bot = s.area.top(2.75, gap=0.25)
s.image(A("week6/shift.png"), top)
L, R = bot.cols(0.5, gap=0.35)
s.bullets(["문제: 정답 전체를 넣으면 각 위치가 **자기 정답을 베낀다**",
           "해결 ① 입력을 **한 칸 밀기** + ② 미래를 **가리기** (다음 장)",
           "이전 정답을 입력으로 = **teacher forcing** (강의 용어)"], L, size=15)
s.callout("**학습은 병렬, 생성은 순차** — 학습 때는 정답 prefix가 모두 있어 모든 위치를 한 번에 예측. "
          "생성 때는 다음 입력이 **아직 없다**. 둘은 모순이 아니다.", R, kind="key", size=14.5)

s = d.slide("§3.2.3 Causal mask: softmax 전에 −∞", lead="원문: 불법 연결은 softmax 입력에서 −∞로 설정 — exp(−∞) = 0, 점수를 0으로 바꾸면 막히지 않는다",
            stage="계산",
            notes="§3.2.3 마지막 문장: Decoder의 왼쪽 방향 정보 흐름을 막기 위해 scaled dot-product attention 안에서 불법 연결에 해당하는 softmax 입력을 −∞로 둔다(mask out). "
                  "5주차 4토큰 예제 Query B 행: mask 없음 [0.14, 0.29, 0.29, 0.29] → causal mask [0.33, 0.67, 0, 0] (검산 완료). 점수를 0으로 바꾸면 exp(0) = 1이라 오히려 비중을 받는다. "
                  "실무 주의: source/target padding mask(PAD 위치 참조 차단)와 loss ignore mask(PAD 정답을 손실에서 제외)는 다른 것. "
                  "PyTorch F.scaled_dot_product_attention의 boolean mask는 True = 허용, nn.MultiheadAttention은 True = 차단. FP16에서는 −∞ 대신 큰 음수의 dtype 주의. "
                  "출처: Vaswani (2017) §3.2.3; 재정규화 예는 week6.md 검산 목록.")
L, R = s.cols(0.48)
s.image(A("week6/causal_mask.png"), Box(L.x, L.y, L.w, L.h - 0.3))
s.formula("A = softmax( QKᵀ/√d_k + M ),  M = −∞ (미래)", Box(R.x, R.y, R.w, 0.9), size=16)
s.table(["4토큰 예 · Query B", "A", "B", "C", "D"], [["mask 없음", "0.14", "0.29", "0.29", "0.29"],
                                               ["−∞ mask", "**0.33**", "**0.67**", "0", "0"]],
        Box(R.x, R.y + 1.15, R.w, 1.2), size=14, align="lcccc", highlight=[1], widths=[2.6, 0.85, 0.85, 0.85, 0.85])
s.bullets(["미래(C, D)가 사라지고 나머지가 **재정규화**", "점수를 **0으로** → exp(0) = 1 → 새어 나간다",
           "padding mask · loss mask와는 **다른 일**"], Box(R.x, R.y + 2.55, R.w, 1.55), size=15)
s.callout("==API 주의== `F.scaled_dot_product_attention`: True = **허용** · `nn.MultiheadAttention`: True = **차단**",
          Box(R.x, R.y + 4.2, R.w, 0.9), kind="warn", size=13.5)

s = d.slide("Cross-attention: Decoder가 원문을 참조한다", lead="Q는 Decoder에서, K · V는 Encoder 최종 출력 E에서 — 점수 표는 T × S",
            stage="아이디어",
            notes="§3.1·§3.2.3: Decoder의 세 번째 sublayer는 Encoder 스택 출력 위의 multi-head attention — Query는 이전 Decoder 층에서, Key·Value는 Encoder 출력에서. "
                  "4주차 Seq2Seq + 5주차 Bahdanau attention의 구조를 그대로 옮긴 것. 점수 표 T × S, 출력 길이는 Query 수 T. "
                  "모든 Decoder 층이 같은 최종 E를 참조하지만 층마다 자기 투영 가중치가 있다. Encoder는 한 번만 실행. causal mask는 필요 없다(source padding mask만). "
                  "shape 추적 예(B 2, S 5, T 3, d 8, H 2, |V| 16): source ID (2, 5) → E (2, 5, 8); target 입력 (2, 3) → (2, 3, 8); Decoder self 표 (2, 2, 3, 3); "
                  "cross 표 (2, 2, 3, 5); Decoder 출력 (2, 3, 8); logits (2, 3, 16). 길이가 섞이는 곳은 cross 점수 표뿐. "
                  "출처: Vaswani (2017) §3.1, §3.2.3 ('encoder-decoder attention' 항목).")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("CrossAttn(D, E) = softmax( (D W_Q)(E W_K)ᵀ / √d_k ) (E W_V)", top, size=20)
rest = s.cards([{"head": "출처", "body": ["Q ← Decoder 표현 (T개)", "K, V ← Encoder 최종 출력 **E** (S개)"]},
                {"head": "shape", "body": ["점수 표 **T × S**", "출력 길이 = Query 수 **T**", "예: (2, 2, 3, **5**)"]},
                {"head": "구조", "tone": "accent", "body": ["Encoder는 **한 번만** 실행", "모든 Decoder 층이 같은 E 참조", "층마다 자기 **투영 가중치**"]}],
               bot, cols=3, body_size=15, head_size=18)
s.callout("mask: causal은 **필요 없다** (source는 target의 미래가 아니다) — source padding mask만. 4주차 Seq2Seq + 5주차 attention이 여기 들어간다.",
          Box(rest.x, rest.y + 0.1, rest.w, 0.8), kind="tip", size=15)

s = d.slide("§3.4 임베딩과 출력: 한 행렬을 세 곳에서", lead="두 임베딩 층과 softmax 직전 선형 변환이 같은 가중치 — 임베딩 층에서는 √d_model을 곱한다",
            stage="계산",
            notes="§3.4: 학습형 임베딩으로 입력·출력 토큰을 d_model 벡터로 바꾸고, 학습형 선형 변환 + softmax로 다음 토큰 확률을 낸다. "
                  "원문: 두 임베딩 층(source, target)과 pre-softmax 선형 변환이 같은 가중치 행렬을 공유한다(Press & Wolf 유사) — 공유는 세 곳. "
                  "그리고 임베딩 층에서는 그 가중치에 √d_model을 곱한다: d = 512면 √512 ≈ 22.6. 논문은 이 배율의 이유를 적지 않는다. "
                  "§3.5: 그 결과에 sinusoidal 위치 인코딩을 더하고, §5.4: 그 합에 dropout. 공유가 가능한 전제: EN-DE는 source-target 공유 BPE 어휘 약 37,000(§5.1). "
                  "logits = D Eᵀ (B, T, |V|), CrossEntropyLoss에는 softmax 전 logits를 넣는다. "
                  "출처: Vaswani (2017) §3.4, §3.5, §5.1, §5.4.")
top, bot = s.area.top(1.25, gap=0.3)
s.formula(["입력 = Dropout( √d · E[id] + PE )        √512 ≈ 22.6", "logits = D · Eᵀ   (B, T, |V|)"], top, size=19)
mid, low = bot.top(1.65, gap=0.3)
s.cards([{"head": "① Source 임베딩", "body": "√d_model · E[id]"}, {"head": "② Target 임베딩", "body": "√d_model · E[id]"},
         {"head": "③ Pre-softmax 선형", "body": "logits = D Eᵀ"}, {"head": "= 같은 행렬 E", "body": "|V| × d — 공유 1벌", "tone": "accent"}],
        mid, cols=4, body_size=15, head_size=16, fit_h=False)
L, R = low.cols(0.5, gap=0.4)
s.bullets(["공유는 **세 곳** — 입력 두 개 + 출력 하나", "전제: source·target **공유 어휘** (EN-DE BPE ≈ 37,000)",
           "√d_model 배율의 **이유는 논문에 없다**"], L, size=15)
s.bullets(["logits = softmax **전** 점수 → CrossEntropyLoss에 그대로", "위치 정보는 그 뒤에 **더한다** (§3.5)",
           "학습형 위치 임베딩도 시험 — Table 3 (E), Part 3"], R, size=15)

s = d.slide("파라미터 수를 직접 세기", lead="공식으로 63.0M — 논문 65M과의 약 2M 차이는 bias · LayerNorm(0.1M)으로 설명되지 않는다",
            stage="계산",
            notes="우리 공식(bias·LN 제외): Encoder 층 4d² + 2·d·d_ff = 3,145,728(3.15M), Decoder 층 8d² + 2·d·d_ff = 4,194,304(4.19M, cross-attention 포함), "
                  "6 + 6층 = 44,040,192(44.0M), 공유 임베딩 37,000 × 512 = 18,944,000(18.9M) → 합 62.98M. bias와 LayerNorm을 넣어도 63.08M — 차이는 약 0.1M뿐. "
                  "따라서 '65M과의 차이는 bias·Norm 때문'이라는 이전 자료 설명은 틀렸다. 남는 약 1.9M은 논문이 설명하지 않는다. "
                  "Table 3의 다른 행도 같은 공식과 비교하면 d = 512 행은 모두 약 +2M, d = 256은 +1.2M, d = 1024는 +4M — 차이가 d에 비례해 어휘 행 수가 37,000보다 약 4k 많을 가능성과 맞는 패턴이지만, "
                  "big 행(213 < 214.2)은 맞지 않는다. 결론: 공식은 상대 변화를 잘 재현하지만 절대값 차이의 원인은 논문으로 확정할 수 없다. "
                  "주의: 4d²는 h·d_k = d일 때만(Table 3 (B)는 d_k만 줄여 58M, 60M). 37,000은 EN-DE BPE 어휘 — EN-FR(32,000 word-piece)이면 임베딩 16.4M. "
                  "출처: Vaswani (2017) §5.1, Table 3 params 열; 계산은 week6.md 파이썬 검산.")
top, bot = s.area.top(0.85, gap=0.25)
s.formula("Encoder 층 4d² + 2·d·d_ff   ·   Decoder 층 8d² + 2·d·d_ff   ·   임베딩 |V|·d", top, size=19)
L, R = bot.cols(0.44, gap=0.3)
s.table(["항목 (d 512, d_ff 2048)", "파라미터"], [["Encoder 층", "3.15M"], ["Decoder 층 (cross 포함)", "4.19M"],
                                             ["6 + 6층", "44.0M"], ["공유 임베딩 37,000 × 512", "18.9M"],
                                             ["합계 (bias · LN 제외)", "**62.98M**"], ["bias · LN 포함", "63.08M"],
                                             ["논문 (Table 3)", "==65M=="]],
        Box(L.x, L.y, L.w, 3.05), size=14, align="lc", highlight=[4], widths=[3.6, 1.9])
s.callout("남는 **≈ 1.9M**은 논문에 설명이 없다 — 실제 어휘 크기 등 추정만 가능. 37,000은 **EN-DE** 어휘.",
          Box(L.x, L.y + 3.2, L.w, 0.95), kind="warn", size=14)
s.image(A("week6/p_param_gap.png"), R)

# ============================================================ Part 2 — 학습
d.part(2, "학습 — §5 · Adam · Label smoothing", "구조가 계산을 정한다면, 목표 · optimizer · 학습률은 무엇을 어떻게 배울지 정한다",
       notes="Part 2: 다음 토큰 NLL(teacher forcing), Adam(Kingma & Ba 2015), 학습률 스케줄(Vaswani Eq. 3), label smoothing(Szegedy 2016 §7), 그리고 §5의 실제 학습 조건. "
             "출처: Vaswani (2017) §5; Kingma & Ba (2015) Algorithm 1; Szegedy et al. (2016) §7.")

d.paper("Kingma & Ba (2015)", "Adam: A Method for Stochastic Optimization", "ICLR 2015 · arXiv:1412.6980 (읽은 판본 v9)",
        "잡음이 크고 희소한 기울기, 파라미터마다 다른 기울기 크기 — **학습률 하나**로 맞추기 어렵다 (Abstract, §1)",
        "기울기의 **1차·2차 모멘트 이동평균** + 0 초기화 **편향 보정** → 파라미터마다 보폭 m̂ / √v̂ (Algorithm 1)",
        "Algorithm 1 (p. 2) · §2.1 보폭 해석 · §3 편향 보정",
        url="arxiv.org/abs/1412.6980",
        result="Transformer의 optimizer — 단 **β2 = 0.98, ε = 10⁻⁹**로 바꾸고 학습률은 스케줄로 (Vaswani §5.3)",
        notes="서지: Kingma & Ba, ICLR 2015, arXiv:1412.6980 v9. 문제: 잡음 크고 희소한 기울기, 고차원 파라미터에서 효율적인 1차 확률적 최적화(Abstract, §1). "
              "아이디어: 기울기의 지수 이동평균 m_t와 제곱 기울기의 이동평균 v_t, 0 초기화 편향을 (1 − β^t)로 나눠 보정, 파라미터마다 m̂/√v̂만큼 이동 — 기울기 대각 스케일 변화에 불변(Abstract, §2). "
              "기본값 α 0.001, β1 0.9, β2 0.999, ε 10⁻⁸. Transformer는 β2 0.98, ε 10⁻⁹(Vaswani §5.3). "
              "이후 비판(일반적으로 알려진 내용): 수렴 증명의 오류(Reddi et al. 2018, AMSGrad); Transformer 초기 적응 학습률 분산 → warm-up 필요(Liu et al. 2019, RAdam). "
              "출처: Kingma & Ba (2015) Abstract, §1–§3, Algorithm 1; Vaswani (2017) §5.3.")

s = d.slide("학습 목표: 다음 토큰의 음의 로그 가능도", lead="teacher forcing으로 모든 위치를 한 번에 — 정답 토큰에 준 확률의 −log를 PAD 아닌 토큰 수로 평균",
            stage="계산",
            notes="한 칸 민 입력(§3.1)을 넣으면 모든 위치에서 다음 토큰 분포가 나오고, 정답 토큰의 −log 확률을 평균한다(2주차 cross-entropy). "
                  "예: 'I am a student EOS'에 준 확률 0.5, 0.4, 0.6, 0.7, 0.9 → −log 0.693, 0.916, 0.511, 0.357, 0.105 → 평균 NLL 0.516, perplexity = exp(0.516) ≈ 1.68 (검산 완료). "
                  "구현: logits (B, T, |V|) → (B·T, |V|), 정답 (B, T) → (B·T), ignore_index = PAD. 그다음 backward → (clip) → optimizer.step(). "
                  "원논문 Table 3의 PPL은 wordpiece 단위 perplexity이고 label smoothing을 쓴 학습 — label-smoothed loss의 exp를 perplexity로 쓰면 안 된다(뒤 장). "
                  "출처: Vaswani (2017) §3.1(offset), Table 3 PPL 열 설명; 손계산은 week6.md 검산 목록.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("L = −(1 / |valid|) · Σ_t  log p(y_t | y_<t, x)", top, size=24)
L, R = bot.cols(0.56, gap=0.4)
s.table(["정답 토큰", "I", "am", "a", "student", "EOS"], [["p(정답)", "0.5", "0.4", "0.6", "0.7", "0.9"],
                                                      ["−log p", "0.693", "0.916", "0.511", "0.357", "0.105"]], Box(L.x, L.y, L.w, 1.3),
        size=14, align="cccccc")
s.bullets(["평균 NLL = **0.516**, perplexity = e^0.516 ≈ **1.68**"], Box(L.x, L.y + 1.5, L.w, 0.7), size=16)
s.callout("PAD 토큰은 분모와 분자에서 **제외** — 집계 단위(토큰 평균 / 문장 평균)를 명시한다.", Box(L.x, L.y + 2.3, L.w, 1.0), kind="tip", size=15)
s.code("loss = F.cross_entropy(\n"
       "    logits.reshape(-1, V),  # (B*T, |V|)\n"
       "    labels.reshape(-1),     # (B*T,)\n"
       "    ignore_index=PAD)\n"
       "loss.backward()\n"
       "optimizer.step()", R, size=13)

s = d.slide("Adam: 파라미터마다 다른 보폭", lead="Algorithm 1 — 첫 step은 기울기 크기와 거의 무관하게 약 α만큼 움직인다",
            stage="계산",
            notes="Algorithm 1(p. 2): m_t ← β1·m + (1 − β1)·g; v_t ← β2·v + (1 − β2)·g²; m̂ = m/(1 − β1^t); v̂ = v/(1 − β2^t); θ ← θ − α·m̂/(√v̂ + ε). "
                  "손계산(검산 완료): 첫 step, g = 0.5, β1 0.9, β2 0.98, α 7e−4 → m = 0.05, v = 0.005, m̂ = 0.5, v̂ = 0.25 → 이동량 7e−4·0.5/0.5 = 7e−4. "
                  "g가 0.05였어도 m̂/√v̂ ≈ 1이라 이동량은 같다 — 초기에 모든 파라미터가 학습률만큼 크게 움직일 수 있다는 것이 warm-up이 필요한 직관(강의용 직관, 원논문의 주장은 아님). "
                  "Transformer: β1 0.9, β2 0.98, ε 10⁻⁹(기본값과 다름). 흔한 오해: 'Transformer는 Adam 기본값을 쓴다'. "
                  "출처: Kingma & Ba (2015) Algorithm 1, §2.1; Vaswani (2017) §5.3; 손계산 week6.md.")
L, R = s.cols(0.5, gap=0.4)
s.formula(["m ← β1·m + (1−β1)·g", "v ← β2·v + (1−β2)·g²", "m̂ = m / (1−β1ᵗ)", "v̂ = v / (1−β2ᵗ)", "θ ← θ − α·m̂ / (√v̂ + ε)"],
          Box(L.x, L.y, L.w, 2.9), size=19)
s.table(["첫 step (g = 0.5)", "값"], [["m = 0.1 × 0.5", "0.05"], ["v = 0.02 × 0.25", "0.005"],
                                   ["m̂ = 0.05 / 0.1 · v̂ = 0.005 / 0.02", "0.5 · 0.25"], ["이동량 = 7e−4 × 0.5 / 0.5", "**7e−4**"]],
        Box(L.x, L.y + 3.1, L.w, 2.0), size=14, align="lc", highlight=[3], widths=[3.9, 1.6])
s.table(["", "Adam 기본값", "Transformer (§5.3)"], [["β1", "0.9", "0.9"], ["β2", "0.999", "**0.98**"], ["ε", "10⁻⁸", "**10⁻⁹**"],
                                                 ["학습률", "α = 0.001 고정", "**Eq. 3 스케줄** (다음 장)"]],
        Box(R.x, R.y, R.w, 2.3), size=15, align="lcc", widths=[1.2, 2.0, 2.6])
s.callout("직관: 초기에는 **모든 파라미터가 α만큼** 움직일 수 있다 → 처음엔 α를 작게 — **warm-up** (강의용 직관)",
          Box(R.x, R.y + 2.55, R.w, 1.1), kind="key", size=15)
s.bullets(["g = 0.05였어도 m̂/√v̂ ≈ 1 → 이동량 **같음**", "흔한 오해: “Transformer는 Adam 기본값” ✗"],
          Box(R.x, R.y + 3.9, R.w, 1.2), size=15)

s = d.slide("§5.3 Eq. 3 학습률: warm-up 후 감소", lead="lrate = d^−0.5 · min(step^−0.5, step · warmup^−1.5), warmup = 4000 — 최고점 6.99 × 10⁻⁴",
            stage="계산",
            notes="Eq. 3: 처음 warmup_steps = 4000 step 동안 선형 증가, 이후 step의 역제곱근에 비례해 감소. d = 512: step 1 → 1.75e−7, 1000 → 1.75e−4, "
                  "4000 → 6.99e−4(최고), 10,000 → 4.42e−4, 100,000 → 1.40e−4. big(d = 1024)의 최고점은 4.94e−4 — d가 크면 학습률이 작다. 모두 Eq. 3으로 검산. "
                  "왜 warm-up이 필요한지는 이 논문이 설명하지 않는다 — Part 4 Xiong et al. (2020)의 질문. "
                  "출처: Vaswani (2017) §5.3 Eq. 3; 계산은 week6.md 손계산 예시.")
L, R = s.cols(0.55)
s.image(A("week6/lr_schedule.png"), L)
s.table(["step", "학습률 (d = 512)"], [["1", "1.75e−7"], ["1,000", "1.75e−4"], ["**4,000**", "**6.99e−4** (최고)"],
                                     ["10,000", "4.42e−4"], ["100,000", "1.40e−4"]],
        Box(R.x, R.y, R.w, 2.65), size=15, align="cc", highlight=[2])
s.bullets(["최고점 = d^−0.5 · 4000^−0.5", "big (d = 1024) 최고점 **4.94e−4**", "**왜** warm-up이 필요한가? → 논문은 답하지 않는다 → **Part 4**"],
          Box(R.x, R.y + 2.9, R.w, R.h - 2.9), size=15)

s = d.slide("Label smoothing: “100% 확신은 금지”", lead="Szegedy et al. (2016) §7: q′ = (1 − ε)·δ + ε·u — Transformer는 ε_ls = 0.1",
            stage="논문",
            notes="Szegedy, Vanhoucke, Ioffe, Shlens, Wojna (CVPR 2016, arXiv:1512.00567) §7: one-hot 정답에 CE를 쓰면 정답 logit이 다른 모든 logit보다 한없이 커지도록 밀려 과적합·과신. "
                  "정답 분포를 q′(k) = (1 − ε)δ_{k,y} + ε·u(k)로 바꾼다 — u = 1/K는 정답 클래스도 포함(구현마다 다르니 표기 명시). ImageNet K = 1000, ε 0.1 → top-1·top-5 오류 약 0.2%p 개선. "
                  "손계산(|V| = 5, ε 0.1, 검산 완료): 목표 (0.92, 0.02, 0.02, 0.02, 0.02). 예측 p = (0.7, 0.1, 0.1, 0.05, 0.05) → hard CE 0.357, smoothed CE 0.540. "
                  "smoothed loss는 0이 될 수 없다 → label-smoothed loss의 exp를 perplexity로 쓰면 안 된다. "
                  "Vaswani §5.4: ε_ls = 0.1 — 'hurts perplexity … but improves accuracy and BLEU'. Table 3 (D): ε_ls 0 → PPL 4.67(더 좋음), BLEU 25.3(더 나쁨); base 0.1 → 4.92, 25.8. "
                  "흔한 오해: label smoothing은 Transformer의 발명이 아니다; perplexity를 개선하지 않는다. "
                  "출처: Szegedy et al. (2016) §7; Vaswani (2017) §5.4, Table 3 (D).")
L, R = s.cols(0.53, gap=0.4)
s.image(A("week6/p_label_smoothing.png"), L)
s.table(["예측 p = (0.7, 0.1, 0.1, 0.05, 0.05)", "loss"], [["hard CE (one-hot)", "0.357"], ["smoothed CE (ε = 0.1)", "0.540"]],
        Box(R.x, R.y, R.w, 1.25), size=14.5, align="lc", widths=[4, 1.2])
s.table(["Table 3 (D)", "PPL", "BLEU"], [["ε_ls = 0.0", "**4.67**", "25.3"], ["ε_ls = 0.1 (base)", "4.92", "**25.8**"]],
        Box(R.x, R.y + 1.45, R.w, 1.25), size=14.5, align="lcc", widths=[2.6, 1.3, 1.3])
s.callout("원문 §5.4: perplexity는 **나빠지지만** 정확도와 BLEU는 **좋아진다**. smoothed loss의 exp를 perplexity로 쓰지 않는다.",
          Box(R.x, R.y + 2.95, R.w, 1.2), kind="key", size=14.5)
s.bullets(["label smoothing은 Transformer의 **발명이 아니다** (2016)"], Box(R.x, R.y + 4.35, R.w, 0.8), size=14.5)

s = d.slide("§5 원논문의 학습 조건", lead="구조와 별도의 실험 조건 — base와 big은 dropout이 다르고, 최종 모델은 체크포인트 평균이다",
            stage="논문",
            notes="§5.1 데이터: WMT 2014 EN-DE 약 4.5M 문장쌍, 공유 source-target BPE 어휘 약 37,000; EN-FR 36M 문장, 32,000 word-piece. 길이가 비슷한 문장끼리 batch, batch당 source 약 25,000 + target 약 25,000 토큰. "
                  "§5.2: P100 8장 한 대. base step당 약 0.4초, 100,000 step = 12시간; big step당 1.0초, 300,000 step = 3.5일. "
                  "§5.3: Adam β1 0.9, β2 0.98, ε 10⁻⁹, Eq. 3 warmup 4000. "
                  "§5.4: residual dropout — 각 sublayer 출력(더하고 정규화하기 전) + Encoder/Decoder 입력의 (임베딩 + PE) 합. base P_drop 0.1; big(Table 3 마지막 행, EN-DE)은 0.3; EN-FR big은 0.1(§6.1). label smoothing 0.1. "
                  "§6.1 추론: base는 10분 간격으로 저장한 마지막 5개 체크포인트 평균, big은 마지막 20개 평균. beam 4, 길이 페널티 α 0.6(dev에서 선택), 최대 출력 길이 입력 + 50, 가능하면 조기 종료. "
                  "이전 자료의 'dropout 0.1'만 적은 표는 big에 대해 틀렸다. 출처: Vaswani (2017) §5.1–§5.4, §6.1, Table 3.")
s.table(["항목", "원논문", "절"],
        [["데이터", "EN-DE ≈ 4.5M 문장쌍 · 공유 BPE ≈ **37,000** / EN-FR 36M 문장 · word-piece 32,000", "§5.1"],
         ["Batch", "길이가 비슷한 문장끼리 · source ≈ 25,000 + target ≈ 25,000 토큰", "§5.1"],
         ["하드웨어", "P100 × 8 · base 0.4 s/step × 100K = **12시간** · big 1.0 s/step × 300K = **3.5일**", "§5.2"],
         ["Optimizer", "Adam β1 0.9 · β2 0.98 · ε 10⁻⁹ · Eq. 3 (warmup 4000)", "§5.3"],
         ["Dropout", "sublayer 출력 + **(임베딩 + PE) 합** · base **0.1** · big EN-DE **0.3** · big EN-FR 0.1", "§5.4 · §6.1"],
         ["Label smoothing", "ε_ls = 0.1", "§5.4"],
         ["최종 모델", "체크포인트 평균: base 마지막 **5**개 · big 마지막 **20**개", "§6.1"],
         ["생성", "beam **4** · 길이 페널티 α **0.6** · 최대 길이 입력 + 50", "§6.1"]],
        widths=[1.9, 8.9, 1.5], size=15, highlight=[4, 6])

# ============================================================ Part 3 — 결과
d.part(3, "Vaswani §6 — 결과와 비용", "무엇을, 얼마의 비용으로 얻었나? 그리고 원문 표는 무엇을 증명하지 않나?",
       notes="Part 3: Table 2(최종 test 결과와 학습 비용), Table 3(dev set 변형 실험), 그리고 저자가 밝힌 한계. 출처: " + V17 + " §6, §7.")

s = d.slide("Table 2: 더 좋은 BLEU를 훨씬 적은 비용으로", lead="newstest2014 영→독 — base 27.3 · big 28.4, 학습 비용은 기존 앙상블보다 한 자릿수 이상 적다",
            stage="결과",
            notes="원문 Table 2 기반 재구성. EN-DE: Transformer base 27.3, big 28.4; 비교 ConvS2S Ensemble 26.36, GNMT+RL Ensemble 26.30, MoE 26.03. "
                  "학습 비용: base 3.3·10¹⁸, big 2.3·10¹⁹ FLOPs, ConvS2S Ensemble 7.7·10¹⁹(EN-DE) / 1.2·10²¹(EN-FR). "
                  "비용 추정 방법(§6.1 각주): 학습 시간 × GPU 수 × GPU당 지속 단정밀도 성능(P100 = 9.5 TFLOPS). 검산: 8 × 9.5e12 × 12 h × 3600 = 3.28e18; 8 × 9.5e12 × 3.5일 × 86400 = 2.30e19. "
                  "EN-FR: base 38.1, big 41.8 — 단 41.8은 현행판(v5–v7)의 초록과 Table 2 수치. v1–v4의 Table 2와 현행판 §6.1 본문은 41.0, v2 초록은 41.2. 인용할 때 판본을 밝힌다. "
                  "§6.3 영어 구문 분석(WSJ §23 F1): WSJ만 91.3, semi-supervised 92.7 — 과제별 튜닝 없이도 RNNG(93.3)를 제외한 기존 모델보다 좋음. "
                  "출처: Vaswani (2017) Table 2, §6.1 각주 5, §6.3 Table 4; arXiv v1–v7 대조.")
top, bot = s.area.top(3.35, gap=0.2)
s.image(A("week6/p_table2.png"), top)
L, R = bot.cols(0.5, gap=0.35)
s.formula(["8 GPU × 9.5 TFLOPS × 12 h × 3600 s", "= 3.28·10¹⁸ ≈ 3.3·10¹⁸ (base)"], Box(L.x, L.y, L.w, 1.15), size=16)
s.callout("영→프 big **41.8**은 현행판(v5–v7) 초록·Table 2 수치 — **v1–v4**와 현행판 §6.1 본문은 **41.0**. 판본을 밝혀 인용한다.",
          R, kind="warn", size=14)

s = d.slide("Table 3: 부품을 바꿔 보면", lead="하나씩 바꾼 변형 실험 — head 수엔 적정점, 크기는 도움, label smoothing은 PPL과 BLEU를 반대로",
            stage="결과",
            notes="원문 Table 3 기반 재구성(EN-DE dev newstest2013, beam search, 체크포인트 평균 없음, PPL은 wordpiece 단위). base: PPL 4.92, BLEU 25.8, 65M. "
                  "(A) 계산량 고정에서 h·d_k = 512: h 1 → 24.9, 4 → 25.5, 8 → 25.8, 16 → 25.8, 32 → 25.4 — head 하나는 최고보다 0.9 낮고 너무 많아도 떨어진다(§6.2). "
                  "(B) d_k만 16 → 25.1(58M), 32 → 25.4(60M): 호환성 함수가 쉽지 않다는 저자 해석. "
                  "(C) N 2/4/8 → 23.7/25.3/25.5(36/50/80M), d 256 → 24.5(28M), d 1024 → 26.0(168M), d_ff 1024 → 25.4(53M), 4096 → 26.2(90M). "
                  "(D) P_drop 0.0 → PPL 5.77, BLEU 24.6 / 0.2 → 4.95, 25.5; ε_ls 0.0 → 4.67, 25.3 / 0.2 → 5.47, 25.7. "
                  "(E) sinusoidal 대신 학습형 위치 임베딩 → 4.92, 25.7 — 'nearly identical'. 단 (E) 행은 v2부터 있다. "
                  "big(d 1024, d_ff 4096, h 16, P_drop 0.3, 300K): 4.33, 26.4, 213M. 주의: 단일 실행 · dev set · 체크포인트 평균 없음 → 0.1–0.3 BLEU 차이를 과하게 해석하지 않는다. "
                  "출처: Vaswani (2017) Table 3, §6.2; 판본 차이는 week6.md.")
top, bot = s.area.top(3.4, gap=0.2)
s.image(A("week6/p_table3.png"), top)
L, R = bot.cols(0.55, gap=0.35)
s.table(["그 밖의 행", "PPL", "BLEU"], [["(B) d_k = 16 (58M)", "5.16", "25.1"], ["(D) P_drop = 0.0", "5.77", "24.6"],
                                     ["(E) 학습형 위치 임베딩", "4.92", "25.7"]], L, size=14, align="lcc", widths=[3.6, 1.0, 1.0])
s.callout("==주의== dev set · **단일 실행** · 체크포인트 평균 없음 — 0.1–0.3 BLEU 차이를 과하게 읽지 않는다. (E)는 v2부터.",
          R, kind="warn", size=14)

s = d.slide("원형이 남긴 문제 → 다음 논문", lead="저자들도 적었다 — 생성은 순차적이고, 아주 긴 시퀀스는 향후 과제였다",
            stage="정리",
            notes="§4: self-attention은 n < d일 때 recurrent보다 빠르다; 매우 긴 시퀀스를 위해 크기 r 이웃만 보는 restricted attention을 향후 과제로. "
                  "§7: 이미지·오디오·비디오용 local attention, 'Making generation less sequential'을 향후 목표로 — 저자들도 생성은 순차적임을 인정. "
                  "이후 비판: Post-LN의 warm-up 의존성(Xiong 2020), 생성 시 KV 메모리 대역폭(Shazeer 2019). "
                  "다른 과제: §6.3 영어 구문 분석 WSJ F1 91.3(WSJ만) / 92.7(semi-supervised). "
                  "출처: Vaswani (2017) §4, §6.3, §7; Xiong et al. (2020) §1; Shazeer (2019) §1.")
s.cards([{"head": "① 학습이 까다롭다", "body": ["Post-LN은 **warm-up 4000** 필요", "왜? → **Xiong et al. (2020)** · Part 4"]},
         {"head": "② 생성은 순차적", "tone": "accent", "body": ["§7 “making generation **less sequential**”", "→ KV cache · **MQA · GQA** · Part 5"]},
         {"head": "③ 긴 시퀀스", "body": ["§4 restricted attention을 향후 과제로", "→ IO를 줄인 **FlashAttention** · Part 5"]},
         {"head": "④ 다른 과제 · 다른 데이터", "body": ["§6.3 구문 분석 F1 91.3 / 92.7", "§7 이미지 · 오디오 → **GPT · BERT · T5 · ViT** · Part 7"]}],
        cols=2, body_size=16, head_size=18)

# ============================================================ Part 4 — Xiong
d.part(4, "Xiong et al. (2020) — Post-LN vs Pre-LN", "원형은 왜 warm-up 없이 발산하나? LayerNorm의 위치를 옮기면?",
       notes="Part 4: LayerNorm 위치와 warm-up의 관계. 출처: Xiong et al. (2020) On Layer Normalization in the Transformer Architecture, ICML 2020, arXiv:2002.04745 v2.")

d.paper("Xiong et al. (2020)", "On Layer Normalization in the Transformer Architecture", "ICML 2020 (PMLR 119) · arXiv:2002.04745",
        "Post-LN Transformer는 학습률 **warm-up이 필수**이고, 최종 성능이 최대 학습률·warm-up 길이에 민감 — **왜?** (Abstract, §1)",
        "평균장 이론으로 **초기화 시점** 기울기 분석: Post-LN은 출력층 근처 기울기가 크다 → **Pre-LN**이면 warm-up을 없앨 수 있다 (§3.3)",
        "Table 1 + Figure 1 · Theorem 1 해설 · Figure 2",
        url="arxiv.org/abs/2002.04745",
        result="warm-up 없는 Pre-LN이 **비슷한** 최종 성능에 **더 빨리** 도달 (§4)",
        notes="서지: Xiong, Yang, He, Zheng, Zheng, Xing, Zhang, Lan, Wang, Liu. ICML 2020(PDF 표기 PMLR 108), arXiv:2002.04745 v2. "
              "문제: Post-LN은 warm-up이 필수이고 최종 성능이 최대 학습률과 warm-up 길이에 민감(Popel & Bojar 2018 인용) — 느리고 튜닝 비용이 크다. "
              "아이디어: 평균장 이론으로 초기화 시 기울기를 분석 — Post-LN은 출력층 근처 파라미터의 기대 기울기가 커서 큰 학습률을 바로 쓰면 불안정, warm-up이 이를 피하게 해 준다. "
              "Pre-LN(LN을 잔차 안 sublayer 앞에 + 마지막 final LN)은 기울기가 잘 행동해 warm-up 제거 가능. "
              "한계(저자): 이론은 초기화 시점·단순화된 attention 등 여러 단순화 위에 있다(§3.4) — 경험적으로 검증. 출처: Xiong (2020) Abstract, §1, §3.3, §3.4, §4.")

s = d.slide("Table 1: LayerNorm을 어디에 두나", lead="Post-LN x + F(x) 뒤에 LN · Pre-LN F의 입력에 LN + 맨 끝 final LN",
            stage="아이디어",
            notes="원문 Table 1·Figure 1 기반(기존 그림 재사용). Post-LN: x_{l+1} = LN(x_l + F(x_l)) — 원형 Vaswani 2017. Pre-LN: x_{l+1} = x_l + F(LN(x_l)), 스택 끝에 Final LayerNorm. "
                  "Pre-LN에서는 잔차 경로가 LN을 거치지 않아 항등 경로가 깨끗하다(3주차 ∂y/∂x = I + ∂F/∂x). "
                  "역사: Pre-LN은 Xiong et al.이 발명한 것이 아니다 — Baevski & Auli 2018, Child et al. 2019, Wang et al. 2019가 이미 사용(Xiong §2), Nguyen & Salazar 2019도 독립적으로 관찰. "
                  "이 논문의 기여는 warm-up 필요성의 이론적 설명과 warm-up 제거. 그림 오른쪽 제목의 '후속 변형'은 2017 원형 이후라는 뜻. "
                  "출처: Xiong et al. (2020) Table 1, Figure 1, §2.")
L, R = s.cols(0.53)
s.image(A("week6/postpre_ln.png"), L)
s.table(["", "Post-LN (원형)", "Pre-LN"], [["식", "LN(x + F(x))", "x + F(LN(x))"], ["잔차 경로", "LN을 거친다", "**깨끗한** 항등 경로"],
                                       ["스택 끝", "—", "**Final LN**"], ["원문 학습", "warm-up **필수**", "warm-up **없이** 가능"]],
        Box(R.x, R.y, R.w, 2.5), size=15, align="lcc", widths=[1.5, 2.2, 2.2])
s.callout("Pre-LN은 Xiong이 **처음 제안한 것이 아니다** — Baevski & Auli 2018 · Child et al. 2019 · Wang et al. 2019. "
          "기여는 warm-up이 **왜** 필요한지의 설명과 **제거**.", Box(R.x, R.y + 2.75, R.w, 1.5), kind="tip", size=15)

s = d.slide("Theorem 1과 실험: warm-up이 필요한 이유", lead="초기화 때 마지막 FFN 기울기 상한 — Post-LN O(d√ln d)는 L과 무관, Pre-LN O(d√(ln d / L))은 층이 깊을수록 작다",
            stage="결과",
            notes="Theorem 1(§3.3): 마지막 층 FFN W² 기울기의 Frobenius norm 상한 — Post-LN O(d√(ln d)), Pre-LN O(d√(ln d / L)). 상한끼리의 비는 1/√L: L 6 → 0.41, 12 → 0.29, 24 → 0.20(상수 무시, 우리 계산). "
                  "실험(§3.2, IWSLT14 De-En): Post-LN은 warm-up 없이는 학습이 안 된다 — Adam·SGD 모두(Figure 2), warm-up 500은 4000보다 나쁘다 → warm-up의 이점은 Adam 고유가 아니다. "
                  "Figure 3: 초기화 시 마지막 FFN 기울기 norm — Post-LN은 6-6~14-14 모델에서 약 1.6으로 일정, Pre-LN은 층 수에 따라 감소. "
                  "§4.2: warm-up 없는 Pre-LN이 비슷한 최종 성능(IWSLT BLEU 약 34)에 더 빨리 — Pre-LN 9번째 체크포인트 ≈ Post-LN 15번째. "
                  "BERT(Figure 5a): 원문 문장은 'Post-LN 500k에 1.69, Pre-LN은 700k에 비슷 … 40% speed-up'이라 모델 이름이 뒤바뀐 서술로 보인다(700/500 = 1.4). "
                  "그래서 '같은 val loss 1.69에 약 40% 적은 update로 도달'만 말하고 숫자 배치는 Figure 5a로 확인한다. "
                  "흔한 오해: Pre-LN이 항상 최종 품질이 더 좋다 ✗(comparable); 후속 모델은 모두 Pre-LN ✗ — BERT·GPT-1은 원형 계열 Post-LN, T5·ViT는 Pre-LN. "
                  "출처: Xiong et al. (2020) Theorem 1, Figure 2, 3, 5a, §3.2, §4.2; T5 §2.1; ViT §3.1.")
L, R = s.cols(0.48, gap=0.4)
s.image(A("week6/p_xiong_bound.png"), Box(L.x, L.y, L.w, 3.3))
s.table(["모델", "LN 위치"], [["BERT (2018) · GPT-1 (2018)", "Post-LN (원형 계열)"], ["T5 (2019) · ViT (2020)", "**Pre-LN**"]],
        Box(L.x, L.y + 3.5, L.w, 1.2), size=14, align="ll", widths=[3.2, 2.4])
s.bullets(["Post-LN은 warm-up **없으면** 학습 실패 — Adam · SGD 모두 (Fig. 2)",
           "Post-LN 기울기 norm ≈ **1.6**으로 일정, Pre-LN은 층이 깊을수록 **감소** (Fig. 3)",
           "warm-up 없는 Pre-LN: IWSLT **9번째** 체크포인트 ≈ Post-LN **15번째**",
           "BERT: 같은 val loss **1.69**에 약 **40% 적은** update"], Box(R.x, R.y, R.w, 3.4), size=15)
s.callout("원문 BERT 문장은 두 모델 이름이 **뒤바뀐 듯** (700k/500k = 1.4) — 숫자 배치는 Figure 5a로 확인. 최종 성능은 “**comparable**”.",
          Box(R.x, R.y + 3.55, R.w, 1.2), kind="warn", size=14)

# ============================================================ Part 5 — 생성과 비용
d.part(5, "생성 비용 — KV cache와 그 해법", "학습은 병렬인데 생성은 순차적 — 무엇이 진짜 병목인가?",
       notes="Part 5: 자기회귀 생성(Vaswani §6.1), KV cache와 메모리 대역폭(Shazeer 2019, Pope 2022), head 공유(MQA, GQA), IO를 줄인 정확한 attention(Dao 2022), 블록 연산량. "
             "출처: Shazeer (2019) arXiv:1911.02150; Pope et al. (2022/2023) arXiv:2211.05102; Ainslie et al. (2023) arXiv:2305.13245; Dao et al. (2022) arXiv:2205.14135.")

s = d.slide("자기회귀 생성과 beam search", lead="source는 한 번 인코딩, 마지막 위치 logits로 다음 토큰을 고르고 붙이기를 EOS까지 — 원문은 beam 4, α 0.6",
            stage="아이디어",
            notes="추론: source를 Encoder로 한 번 처리하고 BOS로 Decoder를 시작, 마지막 위치 logits에서 다음 토큰을 고른 뒤 prefix에 붙여 반복. 다음 입력이 방금 생성한 결과에 의존하므로 순차적. "
                  "선택 정책은 모델과 별개: greedy, sampling, temperature(logits/τ), top-k/top-p, beam search. "
                  "원문 §6.1: beam size 4, 길이 페널티 α = 0.6(dev set 실험으로 선택), 최대 출력 길이 = 입력 길이 + 50, 가능하면 조기 종료. §6.3 구문 분석은 beam 21, α 0.3, 최대 입력 + 300. "
                  "§7: 'Making generation less sequential'을 향후 목표로. 흔한 오해: 'Transformer는 모든 토큰을 동시에 생성한다' — 학습의 위치 병렬성과 다르다. "
                  "출처: Vaswani (2017) §6.1, §6.3, §7.")
top, bot = s.area.top(1.75, gap=0.3)
s.flow([{"head": "Encoder", "body": "source → E (한 번만)"}, {"head": "Decoder", "body": "prefix [BOS, I, am]"},
        {"head": "마지막 위치 logits", "body": "(|V|,) 점수"}, {"head": "토큰 선택", "body": "“a”", "tone": "accent"},
        {"head": "붙이고 반복", "body": "EOS 또는 최대 길이까지", "tone": "dark"}], top, body_size=14, head_size=16, gap=0.35)
L, R = bot.cols(0.6, gap=0.35)
s.table(["정책", "방법", "특징"], [["Greedy", "가장 높은 점수", "전체 최적은 **보장 안 됨**"], ["Sampling · τ", "분포에서 추출 · logits / τ", "다양 · **재학습 아님**"],
                                  ["Top-k · Top-p", "상위 후보만 남기고 추출", "저확률 토큰 방지"],
                                  ["Beam search", "후보 prefix 여러 개 유지", "계산 증가 · 길이 페널티"]], L, size=14, widths=[1.8, 2.9, 2.6])
s.callout("원문 §6.1: beam **4** · 길이 페널티 α **0.6** (dev에서 선택) · 최대 길이 입력 + **50** · 가능하면 조기 종료. "
          "§7 “making generation **less sequential**” — 저자도 순차성을 인정.", R, kind="key", size=15)

s = d.slide("KV cache: 바뀌지 않는 것을 보관하면 얼마나 큰가", lead="KV bytes = 2 · L · B · N · H_kv · d_h · bytes — 큰 batch · 긴 문맥에서는 가중치보다 커진다",
            stage="계산",
            notes="고정 가중치와 causal mask 아래에서 기존 prefix 토큰의 각 층 K, V는 새 토큰이 와도 변하지 않는다 → 저장해 두고 새 토큰의 Q만 계산. Q는 cache하지 않는다. "
                  "Prefill(입력 B × L_input 토큰을 한 번의 forward로 병렬)과 decode(step마다 B개 샘플 하나씩)는 Pope §2의 구분. "
                  "크기(K와 V 두 벌이라 2): 원형 base Decoder self-attention FP32, 6층, B 1, 길이 100 → 2·6·1·100·8·64·4 B = 2.46 MB. "
                  "L 32, H 32, d_h 128(d 4096), N 4096, B 1, FP16 → 2 GiB(2³¹ B, 검산 완료). "
                  "Pope §2: 500B+급 모델, batch 512 · 문맥 2048에서 KV cache 약 3TB = 파라미터 크기의 약 3배. 검산: PaLM 540B 118층 multihead 변형 H 48, d_head 128, bf16 → 3.04TB; 540B × 2B = 1.08TB. "
                  "작은 batch·짧은 길이는 가중치 로딩, 2048+ 토큰·batch 512+에서는 KV cache 로딩이 지배. 흔한 오해: 'KV cache는 작다'. "
                  "출처: Pope et al. (2022) §2; 2 GiB·2.46 MB는 week6.md 검산.")
L, R = s.cols(0.55, gap=0.4)
s.image(A("week6/kv_cache.png"), L)
s.table(["예", "KV cache"], [["원형 base · FP32 · 6층 · 길이 100", "2.46 MB"], ["L 32 · d 4096 (H 32) · N 4096 · FP16", "**2 GiB**"],
                            ["500B+ · batch 512 · 문맥 2048 (Pope §2)", "≈ **3 TB**"]],
        Box(R.x, R.y, R.w, 2.1), size=14, align="lc", widths=[3.9, 1.5])
s.callout("Pope §2: 3TB = 파라미터 크기의 **약 3배** — 2048+ 토큰 · batch 512+에서는 **KV cache 읽기**가 지배한다.",
          Box(R.x, R.y + 2.3, R.w, 1.15), kind="warn", size=14.5)
s.bullets(["저장: 과거의 **K, V** (층마다) · 저장 안 함: **Q**", "**Prefill** (병렬) → **Decode** (step마다 하나)"],
          Box(R.x, R.y + 3.65, R.w, 1.4), size=15)

d.paper("Shazeer (2019)", "Fast Transformer Decoding: One Write-Head is All You Need", "arXiv:1911.02150 (학회 미게재)",
        "증분 생성은 병렬화가 안 되고, 매 step 큰 K/V를 다시 읽는 **메모리 대역폭**이 병목 — 메모리/연산 비 **Θ(n/d + 1/b)** (§2.4.1)",
        "모든 head가 **K, V 한 벌을 공유**(Multi-Query) → 문제 항 n/d가 **h배** 줄어 Θ(1/d + n/(dh) + 1/b) (§3)",
        "§2.4.1 비율 식 · §3 · Table 2",
        url="arxiv.org/abs/1911.02150",
        result="WMT14 EN-DE test BLEU 28.4 → **28.5** (beam 4), 디코더 토큰당 **46 µs → 3.8 µs** (TPUv2) (Table 1–2)",
        notes="서지: Noam Shazeer, arXiv:1911.02150 v1(2019-11), 학회 미게재. §2.3.1 batched MHA: 연산 Θ(bnd²), 메모리 O(bnd + bhn² + d²) → 비 O(1/k + 1/(bn)) — 좋다. "
              "§2.4.1 증분 MHA(n번 호출): 연산 Θ(bnd²), 메모리 Θ(bn²d + nd²) → 비 Θ(n/d + 1/b); n ≈ d이거나 b ≈ 1이면 1에 가까워 대역폭 병목. "
              "MQA: 메모리 Θ(bnd + bn²k + nd²), 비 Θ(1/d + n/(dh) + 1/b). 실험: WMT14 EN-DE, 6+6층, d 1024, h 8, d_k = d_v 128, 100k step; 파라미터를 맞추려고 d_ff 4096 → 5440, 모든 attention을 MQA로. "
              "결과: dev BLEU MHA 26.7 vs MQA 26.5, test beam 4 28.4 vs 28.5; 디코더 per-token 46 → 3.8 µs, beam-4 203 → 32 µs. 학습 시간은 13.2 vs 13.0 µs로 거의 같다. "
              "head 수나 d_k를 단순히 줄인 MHA는 품질이 더 나빴다. 출처: Shazeer (2019) §2.3–§3, Table 1–2.")

s = d.slide("MQA → GQA: K/V head를 몇 벌 둘까", lead="Ainslie et al. (2023): Query head를 G개 그룹으로 — GQA-1 = MQA, GQA-H = MHA",
            stage="논문",
            notes="원문 Ainslie et al. (EMNLP 2023) Figure 2 기반 재구성 + Table 1. 문제: MQA는 품질 저하·학습 불안정, MQA 전용 모델을 처음부터 학습해야 한다. "
                  "(1) Uptraining: MHA 체크포인트의 K, V head를 평균 풀링해 합친 뒤 원 사전학습 계산량의 5%만 추가 학습(평균이 첫 head 선택·무작위보다 좋음, Figure 4). "
                  "(2) GQA-G: Query head를 G 그룹으로 나눠 그룹마다 K/V head 하나. T5 실험에서는 Decoder self-attention과 cross-attention에만, Encoder self-attention에는 미적용. "
                  "Table 1(T5 XXL, 5% uptraining): 추론 시간/샘플 MHA-XXL 1.51 s, MQA-XXL 0.24 s, GQA-8-XXL 0.28 s, MHA-Large 0.37 s; 평균 점수 47.2 / 46.6 / 47.1 / 46.0. "
                  "KV 메모리(L 32, H 32, d_h 128, N 4096, FP16): MHA 2 GiB, GQA-8 0.5 GiB, MQA 0.0625 GiB(검산). "
                  "Pope §3.3: MQA의 메모리 이점은 head 방향으로 나누면(K/V 한 벌이 모든 chip에 복제) 사라지므로 batch 방향 분할이 필요 — 최적화 multiquery로 최대 문맥 32배 이상(Table 1). "
                  "흔한 오해: GQA는 Query head를 줄인다 ✗; GQA는 Llama 2가 발명 ✗. 출처: Ainslie et al. (2023) §2.1–2.2, Figure 2, 4, Table 1; Pope et al. (2022) §3.3, Table 1.")
top, bot = s.area.top(3.2, gap=0.2)
s.image(A("week6/p_gqa.png"), top)
L, R = bot.cols(0.45, gap=0.35)
s.table(["KV head (L 32 · N 4096 · FP16)", "cache"], [["MHA · H_kv = 32", "2 GiB"], ["GQA-8 · H_kv = 8", "0.5 GiB"], ["MQA · H_kv = 1", "0.0625 GiB"]],
        L, size=14, align="lc", widths=[3.4, 1.6])
s.bullets(["**Uptraining**: MHA의 K/V head를 **평균**해 합치고 사전학습의 **5%**만 추가 학습",
           "GQA-8: MHA에 가까운 품질 (47.1 vs 47.2) + MQA에 가까운 속도",
           "Query head는 그대로 — 줄이는 것은 **K/V head**",
           "Pope §3.3: MQA 이점을 살리려면 chip 사이를 **batch 방향**으로 분할"], R, size=14)

s = d.slide("FlashAttention: 연산이 아니라 메모리 이동을 줄인다", lead="Dao et al. (2022) — 정확한(exact) attention을 타일링 · 재계산으로, N×N 표를 HBM에 쓰지 않는다",
            stage="논문",
            notes="Dao, Fu, Ermon, Rudra, Ré — NeurIPS 2022, arXiv:2205.14135. 문제: 근사 attention들은 FLOPs를 줄여도 wall-clock이 빨라지지 않는 경우가 많다 — 병목은 느린 HBM(A100 40–80GB, 1.5–2.0TB/s)과 "
                  "빠른 on-chip SRAM(SM당 192KB, 약 19TB/s) 사이의 읽기·쓰기(IO)(§2.1, Figure 1). "
                  "아이디어: 타일링(K/V 블록을 SRAM에 올리고 Q 블록을 돌며 online softmax 통계 m, ℓ로 누적) + 역전파 때 재계산(N×N 행렬 저장 안 함), 한 커널로 융합(§3.1, Algorithm 1). "
                  "Theorem 1: O(N²d) FLOPs, O(N) 추가 메모리. Theorem 2: HBM 접근 표준 Θ(Nd + N²) vs Flash Θ(N²d²M⁻¹) (M = SRAM 크기). Proposition 3: 모든 M에서 이보다 점근적으로 나은 exact 알고리즘은 없다. "
                  "Figure 2(GPT-2 medium, N 1024, d 64, 16 head, batch 64, A100, fwd+bwd): GFLOPs 66.6 → 75.2(재계산으로 증가), HBM R/W 40.3 → 4.4 GB, 실행 41.7 → 7.3 ms. "
                  "종단 학습: BERT-large(N 512) MLPerf 1.1 기록 대비 15%, GPT-2(N 1K) 3×, LRA 2.4×. Path-X(16K) 61.4%, Path-256(64K) 63.1%. "
                  "흔한 오해: 근사 ✗(exact); 산술량이 선형 ✗ — 선형이 되는 것은 추가 메모리. 이론 MACs ≠ 실측 지연의 원문 근거. "
                  "출처: Dao et al. (2022) §2.1, §3.1, Theorem 1–2, Proposition 3, Figure 1–2.")
top, bot = s.area.top(2.75, gap=0.25)
s.image(A("week6/p_flash.png"), top)
L, R = bot.cols(0.52, gap=0.35)
s.table(["", "표준 attention", "FlashAttention"], [["FLOPs", "O(N²d)", "O(N²d) — **그대로**"], ["추가 메모리", "N×N 표", "**O(N)**"],
                                                ["HBM 접근", "Θ(Nd + N²)", "Θ(N²d² / M)"]], L, size=14, align="lcc", widths=[1.6, 2.0, 2.4])
s.bullets(["**exact** — 근사가 아니다", "산술량은 선형이 **아니다** (재계산으로 오히려 증가)",
           "병목: 느린 HBM ↔ 빠른 SRAM 사이 **IO** (§2.1)", "종단 학습: GPT-2 (N 1K) **3×** 빠름"], R, size=14.5)

s = d.slide("한 블록의 연산량: “O(N²)”만으로는 부족하다", lead="MACs ≈ 4Nd² (투영) + 2N²d (attention) + 2N·d·d_ff (FFN) — 짧을 때는 FFN이 가장 크다",
            stage="계산",
            notes="길이 N, 폭 d의 dense self-attention 블록 forward의 주요 행렬곱(MAC, 곱셈-누산 1회 ≈ 2 FLOPs). Q/K/V/O 투영 4Nd², QKᵀ와 AV 2N²d, FFN 2Nd·d_ff. "
                  "d 512, d_ff 2048: N 512 → 0.54G + 0.27G + 1.07G = 1.88G; N 1024 → 1.07G + 1.07G + 2.15G = 4.29G; N 2048 → 2.15G + 4.29G + 4.29G = 10.7G (검산 완료). "
                  "N을 2배로 하면 attention 항은 4배, 투영·FFN 항은 2배. 원문 §4 Table 1의 self-attention 층 복잡도 O(n²·d)와 같은 이야기이고, §4는 n < d일 때 self-attention이 recurrent보다 빠르다고 말한다. "
                  "이 식은 Encoder 스타일 한 블록 forward — backward·optimizer·생성 루프 전체 비용이 아니며, FlashAttention 예처럼 실측 지연은 IO에 좌우된다. "
                  "출처: Vaswani (2017) §4; MACs 표는 week6.md 검산 목록.")
top, bot = s.area.top(1.0, gap=0.3)
s.formula("MACs ≈ 4·N·d²  +  2·N²·d  +  2·N·d·d_ff", top, size=24)
L, R = bot.cols(0.52, gap=0.4)
s.image(A("week6/flops_terms.png"), L)
s.table(["N (d 512)", "투영", "attention", "FFN", "합"], [["512", "0.54G", "0.27G", "1.07G", "**1.88G**"],
                                                      ["1024", "1.07G", "1.07G", "2.15G", "**4.29G**"],
                                                      ["2048", "2.15G", "**4.29G**", "4.29G", "10.7G"]],
        Box(R.x, R.y, R.w, 1.75), size=14, align="ccccc")
s.bullets(["N × 2 → attention **×4**, 나머지 **×2**", "짧을 때는 FFN · 투영이 더 크다", "forward 한 블록 기준 — 실측 지연은 **IO**도 본다"],
          Box(R.x, R.y + 2.0, R.w, R.h - 2.0), size=15)

# ============================================================ Part 6 — 이 과정의 실험
d.part(6, "도구 · 이 과정의 작은 실험", "논문이 아니라 우리 손으로 — 구조를 먼저 검사하고, 작은 과제로 학습해 본다",
       notes="Part 6은 논문이 아닌 이 과정의 교육용 실습(transformer_lab.py)이다. 원논문의 축소 재현이 아님을 분명히 한다. 출처: 이 과정의 실습 코드와 실행 기록.")

s = d.slide("작은 Transformer 실습: 아홉 가지 검사", lead="수열 뒤집기 [3, 7, 5] → [5, 7, 3, EOS] — 학습 전에 구조부터 검증한다", stage="실습",
            notes="이 과정의 transformer_lab.py: 명시적 Q/K/V, causal·padding mask, Post-LN(Vaswani §3.1), sinusoidal 위치(§3.5), cross-attention, loss, greedy 생성을 포함한 교육용 Encoder–Decoder. "
                  "d 64, H 4, Encoder/Decoder 각 2층, Adam. 외부 데이터 없이 정수 수열을 뒤집는다. 원논문의 축소 재현이 아니다. "
                  "실행: python transformer_lab.py --mode check, --mode train --steps 400 --device cpu. 검사에서는 dropout을 끄고 허용 오차를 명시한다. "
                  "출처: 이 과정의 실습 코드(논문 아님).")
L, R = s.cols(0.4)
s.code("# 1. 구조 검사 (학습 없이)\n"
       "python transformer_lab.py --mode check\n\n"
       "# 2. CPU에서 작은 모델 학습\n"
       "python transformer_lab.py --mode train \\\n"
       "    --steps 400 --device cpu\n\n"
       "# 설정: d=64, H=4, 2+2층, Adam", L, size=12)
cb = s.last_code_box
s.bullets(["교육용 구현 — 원논문 재현 **아님**", "검사 때 **dropout 끄기**, 허용 오차 명시"], Box(L.x, cb.b + 0.25, L.w, L.b - cb.b - 0.25), size=15)
s.table(["검사", "확인하는 성질"], [["Shape", "Q/K/V · attention 출력 차원"], ["Row sum", "dropout 전 attention 행 합 = 1"],
                                  ["Future weight zero", "causal mask의 미래 가중치 = 0"], ["PyTorch reference", "직접 구현 = F.scaled_dot_product_attention"],
                                  ["Permutation equivariance", "위치·mask 없는 SA의 순열 대응"], ["Cross query length", "cross 출력 길이 = Query 길이"],
                                  ["Masked value independence", "가려진 Key의 Value를 바꿔도 출력 불변"],
                                  ["Full-model causal invariance", "미래 target을 바꿔도 이전 logits 불변"], ["Backward gradient", "Encoder 투영까지 기울기 전달"]],
        R, size=13, widths=[2.4, 3.6])

s = d.slide("이 과정의 실험 결과: 손실과 생성은 다르다", lead="400 step에서 손실은 내려갔지만 완전한 수열 생성은 아직 — 원문 Table 3처럼 조건을 함께 적는다",
            stage="검증",
            notes="이 과정의 실행 기록(PyTorch 2.10 CPU, seed 7, batch 32, 400 step, 단일 실행): 훈련 batch NLL 2.90 → 1.23. "
                  "평가: 훈련 길이 3–8에서 NLL 1.045, teacher-forced 토큰 정확도 56.8%, greedy exact match 6.9%(5/72). 더 긴 9–12에서 1.764, 33.8%, 0%(0/72). "
                  "400 step은 실행 예시이지 충분한 학습이 아니다. 긴 입력에서 떨어져도 구현 오류로 단정하지 않는다 — 학습 분포 밖. "
                  "원문 Table 3도 단일 실행·dev set·체크포인트 평균 없음이라는 조건을 함께 적었다 — 우리 실험도 조건을 함께 보고한다. "
                  "출처: 이 과정의 실습 실행 기록(논문 아님); Vaswani (2017) Table 3 설명.")
s.table(["평가 길이", "Raw NLL", "teacher-forced 토큰 정확도", "greedy exact match"],
        [["3–8 (훈련 범위)", "1.045", "56.8%", "6.9% (5 / 72)"], ["9–12 (더 긴 입력)", "1.764", "33.8%", "**0%** (0 / 72)"]],
        Box(s.area.x, s.area.y, s.area.w, 1.5), widths=[2.6, 1.6, 3.4, 3.2], size=16, align="lccc")
s.cards([{"head": "읽는 법 ①", "body": ["훈련 batch NLL 2.90 → 1.23, 평가(3–8) 1.045로 **내려갔지만**", "완전한 수열 생성은 **아직**"]},
         {"head": "읽는 법 ②", "body": ["토큰 정확도와 **exact match**는 다르다", "생성은 오류가 **누적**된다"]},
         {"head": "읽는 법 ③", "tone": "accent", "body": ["긴 입력에서 떨어져도 **구현 오류로 단정 X**", "학습 분포 밖 — 단일 실행 · 400 step"]}],
        Box(s.area.x, s.area.y + 1.8, s.area.w, s.area.h - 1.8), cols=3, body_size=16, head_size=17)

# ============================================================ Part 7 — 2017 이후
d.part(7, "2017 이후 — 바뀐 것과 남은 것", "GPT-1 · BERT · T5 · ViT · DiT · GLU · RoPE — 원형 표의 어느 칸을 바꿨나?",
       notes="Part 7: 후속 논문을 원형 Transformer의 표에 꽂아 보며 '바꾼 것 / 남긴 것'을 구분한다. 출처: Radford et al. (2018); Devlin et al. (2019); Raffel et al. (2020); "
             "Dosovitskiy et al. (2021); Peebles & Xie (2023); Shazeer (2020); Su et al. (2021).")

s = d.slide("세 가지 조립 방식: GPT-1 · BERT · T5", lead="반쪽을 떼어 낸 것이 아니다 — mask · 목표 · LN 위치가 함께 달라진다", stage="논문",
            notes="GPT-1(Radford, Narasimhan, Salimans, Sutskever 2018, OpenAI 보고서): 'multi-layer Transformer decoder'(Liu et al. 2018 인용) — Decoder-only는 GPT-1이 처음이 아니다. "
                  "12층, masked self-attention, d 768, 12 head, FFN 3072, GELU, 학습형 위치 임베딩, BooksCorpus, 출력 softmax(h_n W_eᵀ) = weight tying(Eq. 2). 파라미터 수는 논문에 없다(117M은 외부 수치). "
                  "BERT(Devlin et al., NAACL 2019): 양방향 Transformer encoder, MLM + NSP; BASE L 12, H 768, A 12, 110M / LARGE L 24, H 1024, A 16, 340M; 원형과 같은 Post-LN. "
                  "T5(Raffel et al., JMLR 2020): 원형 Encoder–Decoder를 거의 그대로 — 단 LN을 각 subcomponent 입력에(Pre-LN), bias 없는 단순화 LN(재스케일만), 상대 위치 bias(32 bucket, 최대 offset 128). "
                  "크기 Small ≈ 60M, Base ≈ 220M, Large ≈ 770M, 3B, 11B. "
                  "출처: GPT-1 §3.1, §4.1; BERT §3, §3.1; T5 §2.1, §3.6; Xiong (2020) §1.")
L, R = s.cols(0.46, gap=0.35)
s.image(A("week6/archs.png"), L)
s.table(["모델", "바꾼 것", "그대로 둔 것"],
        [["GPT-1 (2018)", "Decoder만 · cross-attn 없음 · GELU · **학습형** 위치", "masked self-attn · Post-LN · 출력 = 임베딩ᵀ"],
         ["BERT (2018/19)", "Encoder만 · **양방향** · MLM + NSP", "Post-LN 블록 · FFN · 잔차"],
         ["T5 (2019/20)", "**Pre-LN** · bias 없는 LN · **상대 위치 bias**", "Encoder–Decoder 원형 구조"]],
        Box(R.x, R.y, R.w, 3.4), size=14, widths=[1.65, 2.6, 2.6])
s.callout("Decoder-only를 GPT-1이 **처음** 만든 것은 아니다 — GPT-1은 Liu et al. (2018)의 “Transformer decoder”를 인용한다.",
          Box(R.x, R.y + 3.65, R.w, 1.1), kind="tip", size=14.5)

s = d.slide("목표가 mask를 정한다: GPT-1 · BERT · T5", lead="무엇이 입력이고 무엇이 정답인가 — 다음 토큰 · MLM + NSP · span corruption", stage="논문",
            notes="GPT-1 §3.1: L1 = Σ log P(u_i | u_{i−k..i−1}) (Eq. 1). 미세조정 L3 = L2 + λ·L1, λ 0.5. 결과: 12개 과제 중 9개 SOTA, GLUE 72.8(이전 68.9). "
                  "BERT §3.1 Task #1 MLM: WordPiece 토큰의 15% 위치를 골라 그중 80% [MASK], 10% 무작위 토큰, 10% 그대로 → 원 토큰 예측. [MASK]가 미세조정 때 없다는 불일치를 줄이려는 설계. "
                  "Task #2 NSP: 50% 실제 다음 문장(IsNext) / 50% 무작위(NotNext), [CLS] 표현으로 분류(최종 정확도 97–98%). 결과: GLUE 80.5, SQuAD v1.1 F1 93.2. "
                  "Table 5: NSP 제거 시 QNLI·MNLI·SQuAD 하락(이후 RoBERTa가 필요성에 반론 — 일반적으로 알려진 내용). MLM은 정답 누출이 아니다 — 입력에서 가린 위치를 복원하는 별도 목표. "
                  "T5 §3.1.4, Figure 2: span corruption — 토큰 15%를 떨어뜨리고 연속 구간은 sentinel 하나(<X>, <Y>)로, 출력은 sentinel로 구분된 떨어진 구간들 + 마지막 sentinel. 평균 span 길이 3. "
                  "모든 과제를 text-to-text로: 'translate English to German: That is good.' → 'Das ist gut.'(Figure 1). C4 약 750GB. "
                  "출처: GPT-1 §3.1–3.2; BERT §3.1, Table 5; T5 §2.2, §3.1.4, Figure 1–2.")
s.cards([{"head": "GPT-1 · 다음 토큰", "bullets": True,
          "body": ["L1 = Σ log P(u_i | u_<i) (Eq. 1)", "**causal** mask — 왼쪽만 본다", "BooksCorpus (7,000권 이상)", "미세조정 L2 + 0.5 · L1"]},
         {"head": "BERT · MLM + NSP", "tone": "accent", "bullets": True,
          "body": ["토큰 **15%** 선택 → **80%** [MASK] · **10%** 무작위 · **10%** 그대로", "**NSP**: 실제 다음 문장 50% / 무작위 50%",
                   "양방향 — MLM은 정답 누출이 **아니다**"]},
         {"head": "T5 · span corruption", "bullets": True,
          "body": ["토큰 **15%**를 떨어뜨리고 연속 구간은 sentinel **<X>**, **<Y>**로", "출력: <X> 구간 <Y> 구간 …",
                   "모든 과제를 **text-to-text**로"]}],
        cols=3, body_size=15, head_size=17)
s.area = Box(s.area.x, s.area.y + 3.55, s.area.w, s.area.h - 3.55)
s.callout("예 (T5 Figure 1): “translate English to German: That is good.” → “Das ist gut.” — 과제 이름도 **입력 텍스트**의 일부.",
          Box(s.area.x, s.area.y, s.area.w, 0.9), kind="key", size=16)

s = d.slide("ViT와 DiT: 이미지 patch도 token이다", lead="ViT (2021): 16×16 patch → token · DiT (2023): latent patch로 diffusion — 같은 블록, 다른 입력",
            stage="논문",
            notes="ViT(Dosovitskiy et al., ICLR 2021): 224×224, P 16 → 14 × 14 = 196 patch, patch당 16·16·3 = 768값을 학습형 선형 투영으로 D차원. BERT처럼 학습형 [class] 토큰, 학습형 1D 위치 임베딩(2D-aware는 유의한 이득 없음), LN을 각 블록 앞에(Pre-LN). "
                  "ViT-Base 12층 D 768 86M, Large 24층 307M, Huge 32층 632M. ImageNet(1.3M)만으로는 같은 크기 ResNet보다 몇 %p 낮다 — 귀납 편향 부족. 14M–300M장(ImageNet-21k, JFT-300M)에서는 "
                  "'large scale training trumps inductive bias'. ViT-H/14(JFT) ImageNet 88.55%, 2.5k TPUv3-core-days(최고 성적은 해상도 518로 미세조정; 196 patch는 설명용). "
                  "patch attention 자체는 Cordonnier et al. 2020이 먼저. "
                  "DiT(Peebles & Xie, ICCV 2023): Stable Diffusion VAE latent(256×256×3 → 32×32×4)를 p×p patch로 → T = (I/p)²(p 2 → 256 token). 조건(t, class) 주입 4가지 비교 — adaLN-Zero: LN의 γ, β와 잔차 직전 스케일 α를 회귀하고 α를 0으로 초기화 → 블록이 항등 함수로 시작. "
                  "Gflops와 FID 강한 음의 상관(Figure 8). DiT-XL/2(118.6 Gflops, 675M) cfg 1.5 → 256×256 FID 2.27(LDM 3.60). 원형 DiT는 class-conditional — 텍스트-이미지 모델이 아니다; 모든 patch를 동시에 예측, 반복은 diffusion step. "
                  "출처: ViT §3.1, §4.3, Table 1–2; DiT §3.2, §4, Table 1, Figure 5, 8.")
L, R = s.cols(0.56)
s.image(A("week6/vit_patch.png"), L)
rest = s.card(R, "ViT (Dosovitskiy et al., 2021)", ["224 / 16 → **196** patch, 각 768값 → D차원 투영",
                                                    "학습형 **[class]** · 학습형 1D 위치 · **Pre-LN**",
                                                    "ImageNet(1.3M)만이면 ResNet보다 낮다 → **14M–300M**장에서 우위"],
              bullets=True, fit_h=True, body_size=14.5)
s.card(rest, "DiT (Peebles & Xie, 2023)", ["VAE latent **32×32×4** → patch token (p 2 → 256개)", "**adaLN-Zero**: α = 0 초기화 → 블록이 **항등**으로 시작",
                                           "class 조건 · ImageNet 256 **FID 2.27**"],
       tone="accent", bullets=True, fit_h=True, body_size=14.5)

s = d.slide("GLU 변형과 RoPE: FFN과 위치 정보를 바꾸다", lead="Shazeer (2020): 게이트 달린 FFN · Su et al. (2021): Q·K를 위치만큼 회전 — 블록의 나머지는 그대로",
            stage="논문",
            notes="GLU variants(Shazeer 2020, arXiv:2002.05202): FFN_GEGLU = (GELU(xW) ⊗ xV)W2, FFN_SwiGLU = (Swish₁(xW) ⊗ xV)W2 (Eq. 6, bias 생략). 행렬이 3개라 파라미터·연산을 맞추려고 d_ff를 2/3로(3072 → 2048). "
                  "T5 base, C4 span-filling, 524,288 step. Table 1 held-out log-perplexity: ReLU 1.677, GELU 1.679, Swish 1.683, GLU 1.663, Bilinear 1.648, ReGLU 1.645, GEGLU 1.633, SwiGLU 1.636. "
                  "GLUE 평균 ReLU 83.80 → SwiGLU 84.36. 저자: 왜 되는지 설명 없음 — 'we attribute their success, as all else, to divine benevolence'(§4). "
                  "RoPE(Su et al., arXiv:2104.09864): 목표 ⟨f_q(x_m, m), f_k(x_n, n)⟩ = g(x_m, x_n, m − n) (Eq. 11). f(x_m, m) = R_{Θ,m} W x_m (Eq. 14), R은 d/2개의 2×2 회전 블록, θ_i = 10000^(−2(i−1)/d) — sinusoidal과 같은 주파수. "
                  "q_mᵀk_n = x_mᵀ W_q R_{Θ,n−m} W_k x_n (Eq. 16) — 상대 위치만 남는다. 덧셈이 아니라 곱셈(회전), Q와 K에만(V는 그대로). d = 8 → θ = (1, 0.1, 0.01, 0.001). "
                  "WMT14 EN-DE BLEU Transformer-base 27.3 → RoFormer 27.5(Table 1). "
                  "출처: Shazeer (2020) Eq. 6, Table 1–2, §4; Su et al. (2021) Eq. 11–16, Table 1.")
L, R = s.cols(0.5, gap=0.4)
s.image(A("week6/p_glu.png"), Box(L.x, L.y, L.w, 3.2))
s.formula(["SwiGLU(x) = (Swish(xW) ⊗ xV) W2", "행렬 3개 → d_ff × 2/3 (3072 → 2048)"], Box(L.x, L.y + 3.35, L.w, 0.95), size=15)
s.bullets(["바꾼 것: FFN **활성화와 게이트** · 그대로: 블록 구조", "저자도 이유는 모른다 — “divine benevolence” (§4)"],
          Box(L.x, L.y + 4.4, L.w, 1.0), size=14)
s.image(A("week6/p_rope.png"), Box(R.x, R.y, R.w, 3.2))
s.formula(["q_mᵀ k_n = x_mᵀ W_q R(n−m) W_k x_n", "θ_i = 10000^(−2(i−1)/d)"], Box(R.x, R.y + 3.35, R.w, 0.95), size=15)
s.bullets(["바꾼 것: 덧셈 → **회전(곱셈)**, **Q · K에만** (V 그대로)", "EN-DE BLEU 27.3 → **27.5** (Table 1)"],
          Box(R.x, R.y + 4.4, R.w, 1.0), size=14)

s = d.slide("원형과 후속 변형을 구분하기", lead="변형이 있다는 것 ≠ 특정 조합이 모든 모델의 표준 — 원형 표의 칸 단위로 말한다", stage="정리",
            notes="원형 기준과 대표 후속 설계. FFN: ReLU → GELU(GPT-1, BERT), GEGLU/SwiGLU(Shazeer 2020). 정규화: Post-LN → Pre-LN(T5, ViT; 설명은 Xiong 2020), T5의 bias 없는 LN. "
                  "위치: sinusoidal 덧셈 — 그러나 학습형 위치 임베딩은 원논문 자체가 Table 3 (E)에서 시험했다(PPL 4.92, BLEU 25.7 vs 25.8, 'nearly identical'; v2부터). sinusoidal을 고른 이유는 더 긴 길이로 외삽할 가능성(§3.5). "
                  "이후 GPT-1·BERT·ViT는 학습형, T5는 상대 위치 bias, RoPE는 Q·K 회전. Head: MHA → MQA(Shazeer 2019) / GQA(Ainslie 2023) — K/V head 공유, Query head는 그대로. "
                  "Attention 계산: FlashAttention(Dao 2022) — exact, IO 효율, 산술량은 선형 아님. 이 과정에서는 세부 구현까지 확장하지 않고 원형 표에 꽂아 무엇이 바뀌는지 설명할 수 있으면 충분. "
                  "출처: Vaswani (2017) §3.5, Table 3 (E); 각 후속 논문(week6.md).")
s.table(["부품", "원형 (2017)", "후속 설계 (논문)", "하지 않는 주장"],
        [["FFN 활성화", "ReLU (Eq. 2)", "GELU (GPT-1 · BERT) · **SwiGLU** (Shazeer 2020)", "attention을 대체하지 않는다"],
         ["정규화", "Post-LN", "**Pre-LN** (T5 · ViT; Xiong 2020이 설명)", "보편적 우열이 아니다"],
         ["위치 정보", "sinusoidal 덧셈 (학습형도 **Table 3 (E)**에서 시험)", "학습형 (GPT-1 · BERT · ViT) · 상대 bias (T5) · **RoPE**", "위치 정보를 없애는 것이 아니다"],
         ["Head 구성", "MHA (Q = K/V head 수)", "**MQA** (2019) · **GQA** (2023) — K/V head 공유", "Query head를 줄이는 것이 아니다"],
         ["Attention 계산", "N×N 표를 저장하는 dense", "**FlashAttention** (2022) — exact · IO 효율", "산술량이 선형이 되는 것이 아니다"]],
        Box(s.area.x, s.area.y, s.area.w, 3.8), widths=[1.7, 3.0, 4.0, 3.0], size=14.5)
s.callout("범위: RoPE · GQA · FlashAttention을 세부 구현까지 확장하지 않는다 — 원형 표에 꽂아 **무엇이 바뀌는지** 설명할 수 있으면 충분하다.",
          Box(s.area.x, s.area.y + 4.05, s.area.w, 0.9), kind="tip", size=15)

# ============================================================ 마무리
s = d.slide("여섯 질문으로 다시 보기", lead="1943 → 2017 → 이후: 각 구조는 이전 구조가 남긴 질문에 대한 답이었다", stage="정리",
            notes="과정 전체 회고. W1 규칙을 다 쓰지 않고 배울 수 있을까? → 텐서·손실·경사하강법. W2 직선으로 안 되면? → MLP·역전파. W3 공간·깊이는? → CNN·ResNet·Norm. "
                  "W4 먼 정보를 기억하려면? → RNN·LSTM·Seq2Seq. W5 원문을 다시 보면? → Attention·Q/K/V·Multi-head. W6 참조만으로 만들면? → Transformer(Vaswani 2017). "
                  "Transformer 안에는 이 모든 답이 들어 있다: 텐서·학습 루프(W1), FFN = MLP·softmax·CE(W2), 잔차·LayerNorm(W3), 임베딩·Encoder–Decoder(W4), attention(W5). "
                  "주의: 계보는 교육적 연결이며, 각 모델이 이전 모델을 완전히 대체했다는 주장이 아니다. 출처: 각 주차 논문 노트(week1–6.md).")
top, bot = s.area.top(2.6, gap=0.25)
s.image(A("week6/genealogy.png"), top)
s.table(["Transformer 안의 부품 (Vaswani 2017)", "처음 배운 곳"], [["텐서 · 손실 · 경사하강 · 학습 루프 → Adam (§5.3)", "Week 1"],
                                                            ["FFN(= MLP, §3.3) · 역전파 · softmax + cross-entropy", "Week 2"],
                                                            ["잔차 · LayerNorm (§3.1)", "Week 3"], ["임베딩(§3.4) · 다음 토큰 확률 · Encoder–Decoder", "Week 4"],
                                                            ["Attention · Q/K/V · Multi-head · 위치 인코딩 (§3.2, §3.5)", "Week 5"]],
        bot, widths=[7, 2], size=13.5, align="lc")

d.summary(["층 = attention + **FFN**(§3.3), 각각 **LN(x + Sublayer(x))**(§3.1) — 공유 임베딩 × √d_model (§3.4)",
           "**shift + causal mask(−∞)**로 정답을 보지 않고 모든 위치를 병렬 학습 — 생성은 순차적",
           "학습: Adam(β2 0.98) · **warm-up 4000 → 최고 7e−4** · dropout 0.1/0.3 · ε_ls 0.1 · 체크포인트 평균",
           "결과: 영→독 **27.3 / 28.4** · base 학습 3.3·10¹⁸ FLOPs — 파라미터 공식 63M vs 논문 65M (차이 원인 미상)",
           "Xiong (2020): Post-LN은 출력 근처 기울기가 커서 warm-up 필요 — **Pre-LN**이면 제거 가능",
           "생성 비용: KV cache (2 GiB 예) → **MQA · GQA**로 줄이고, **FlashAttention**은 FLOPs가 아니라 IO를 줄인다"],
          notes="한 줄씩 학생이 자기 말로 다시 설명하게 한다. 출처: Vaswani (2017) §3.1, §3.3, §3.4, §5, Table 2–3; Xiong (2020) Theorem 1; Shazeer (2019); Ainslie (2023); Dao (2022).")

d.quiz("셀프 체크", [("원논문에서 같은 가중치 행렬을 공유하는 곳은 몇 곳이고, 임베딩에는 무엇을 곱하나?", "세 곳(source 임베딩, target 임베딩, pre-softmax 선형) · √d_model (§3.4)"),
                   ("d = 512, warmup = 4000일 때 Eq. 3의 최고 학습률은?", "512^−0.5 × 4000^−0.5 ≈ 6.99 × 10⁻⁴ (step 4000에서)"),
                   ("공식으로 센 63.0M과 논문 65M의 차이를 bias·LayerNorm으로 설명할 수 있나?", "아니다 — bias·LN은 약 0.1M. 남는 약 1.9M은 논문에 설명이 없다"),
                   ("label smoothing(ε_ls = 0 → 0.1)은 PPL과 BLEU를 어떻게 바꿨나?", "PPL은 4.67 → 4.92로 나빠지고 BLEU는 25.3 → 25.8로 좋아졌다 (Table 3 (D))"),
                   ("Xiong et al.에 따르면 Post-LN에 warm-up이 필요한 이유는?", "초기화 때 출력층 근처 기울기가 커서(O(d√ln d), L과 무관) 큰 학습률이 불안정 — Pre-LN은 1/√L로 작아 warm-up 제거 가능"),
                   ("FlashAttention은 attention의 FLOPs를 선형으로 줄이나?", "아니다 — FLOPs는 O(N²d) 그대로(예: 66.6 → 75.2 GFLOPs). 줄이는 것은 HBM IO(40.3 → 4.4 GB)와 추가 메모리(O(N))")],
       notes="출처: Vaswani (2017) §3.4, Eq. 3, Table 3; Xiong (2020) Theorem 1; Dao (2022) Figure 2, Theorem 1. 추가 질문: (1) 정답을 한 칸 민 Decoder에서 대각선 참조는? → 허용 — 현재 입력은 다음 정답보다 한 칸 앞. "
             "(2) L 32, H_kv 8, d_h 128, N 4096, FP16의 KV cache는? → 0.5 GiB. (3) BERT의 MLM에서 선택된 15% 토큰은 어떻게 바뀌나? → 80% [MASK], 10% 무작위, 10% 그대로.")

d.misconceptions([["“Attention은 이 논문이 처음 제안했다”", "Bahdanau 2014 등에 이미 — 새로운 점은 **recurrence 완전 제거** (§1, §2)"],
                  ["“65M과 63M의 차이는 bias · Norm 때문”", "bias · LN은 **0.1M** — 남는 ≈ 1.9M은 논문에 설명 없음"],
                  ["“원형은 dropout 0.1”", "base만 0.1 — big EN-DE **0.3**, EN-FR big 0.1. **(임베딩 + PE) 합**에도"],
                  ["“영→프 41.8이 처음부터 보고된 숫자”", "v1–v4는 **41.0**, 현행판 §6.1 본문도 41.0"],
                  ["“label smoothing은 perplexity를 개선한다”", "논문은 perplexity를 **해친다**고 명시 — Table 3 (D)"],
                  ["“Pre-LN은 Xiong (2020)의 발명 · 후속 모델은 모두 Pre-LN”", "그 전에 이미 사용 · **BERT · GPT-1은 Post-LN**"],
                  ["“FlashAttention은 근사이고 산술량이 선형”", "**exact** · FLOPs O(N²d) 그대로 — 줄이는 것은 **IO**"],
                  ["“GQA는 Query head를 줄인다”", "줄이는 것은 **K/V head** — Query head는 그대로"]],
                 notes="출처: Vaswani (2017) §1–§2, §5.4, §6.1, Table 2–3 및 판본 대조; Xiong (2020) §1–§2; Dao (2022) Theorem 1, Figure 2; Ainslie (2023) §2.2.")

hw = d.homework([("Vaswani §3.1 · §3.4 · Figure 1", "Figure 1을 다시 그려 세 곳 공유 · √d_model · offset · shape 표시 → 사진 1장"),
            ("Vaswani §6.2 Table 3 (C)", "공식으로 N = 2 / 4 / 8 파라미터 계산 → 36 / 50 / 80M 비교표 + 가설 3문장"),
            ("Xiong (2020) Table 1 · Theorem 1 · Figure 2", "두 식 · warm-up이 필요한 이유 · BERT ‘40%’ 문장의 문제 → 한 단락"),
            ("후속 논문 한 편 골라 읽기", "지정 절을 읽고 ‘원형에서 바꾼 것 / 남긴 것’ 표 1장 (근거 절 번호 포함)")],
           notes="이번 주 과제는 논문 읽기 과제다. 각 과제는 읽을 절·그림과 제출물이 정해져 있다. 과제 1: Figure 1에 ① 세 곳의 가중치 공유 ② √d_model ③ offset by one ④ 각 구간 shape을 표시. 과제 3: 10문장 이내. 과제 4의 지정 절: GPT-1 §3.1, BERT §3.1, T5 §2.1, ViT §3.1, GQA §2, FlashAttention §3.1 중 하나. 실습 연장(선택): transformer_lab.py에서 causal mask를 일부러 제거하거나 Post-LN → Pre-LN으로 바꿔 "
                 "훈련 loss와 greedy 생성의 차이를 기록 — 원문 Table 3처럼 변경 변수 하나, 통제 조건, seed 3개를 함께 적는다. 출처: week6.md 각 논문의 '읽기 안내'.")

# 2 × 2 격자로 다시 배치 (한 열 4장은 본문이 너무 작아진다)
for _sh in list(hw.s.shapes)[hw._base_n:]:
    _sh._element.getparent().remove(_sh._element)
hw.cards([{"head": "Vaswani §3.1 · §3.4 · Figure 1", "body": "Figure 1을 빈 종이에 다시 그리고 ① 세 곳의 가중치 공유 ② √d_model ③ “offset by one” ④ 각 구간 shape을 표시 → **사진 1장**"},
          {"head": "Vaswani §6.2 Table 3 (C)", "body": "우리 공식으로 N = 2 / 4 / 8 행의 파라미터를 계산해 36 / 50 / 80M과 비교 → **비교표 1개 + 차이에 대한 가설 3문장**"},
          {"head": "Xiong (2020) Table 1 · Theorem 1 · Fig. 2", "body": "Post-LN · Pre-LN의 식, warm-up이 필요한 이유, 원문 BERT ‘40%’ 문장의 숫자 배치 문제 → **한 단락 (10문장 이내)**"},
          {"head": "후속 논문 한 편 골라 읽기", "body": "GPT-1 §3.1 · BERT §3.1 · T5 §2.1 · ViT §3.1 · GQA §2 · FlashAttention §3.1 중 하나 → **‘바꾼 것 / 남긴 것’ 표 1장** (근거 절 포함)"}],
         cols=2, numbered=True, body_size=16, head_size=17)

d.references([["Vaswani et al. (2017) Attention Is All You Need · NIPS · arXiv:1706.03762 (v7 인용, v1과 숫자 대조)", "§3.1 + Fig. 1 · §3.3 · §3.4 · §5 · §6.2 Table 3"],
              ["Kingma & Ba (2015) Adam · ICLR · Szegedy et al. (2016) Rethinking Inception · CVPR", "Algorithm 1 · §2.1 / §7 label smoothing"],
              ["Xiong et al. (2020) On Layer Normalization in the Transformer Architecture · ICML", "Table 1 · Fig. 1 · Theorem 1 · Fig. 2"],
              ["Radford et al. (2018) GPT-1 · Devlin et al. (2019) BERT · Raffel et al. (2020) T5", "§3.1 · §4.1 / Fig. 1 · §3.1 / Fig. 1–2 · §2.1"],
              ["Shazeer (2019) MQA · Pope et al. (2023) Scaling Inference · Ainslie et al. (2023) GQA", "§2.4.1 · Table 2 / §2 · Table 1 / Fig. 2 · Table 1"],
              ["Dao et al. (2022) FlashAttention · NeurIPS", "Fig. 1 · Fig. 2 (left) · Theorem 2"],
              ["Dosovitskiy et al. (2021) ViT · Peebles & Xie (2023) DiT", "Fig. 1 · §3.1 · Fig. 3 / Fig. 3 · Fig. 4"],
              ["Shazeer (2020) GLU Variants · Su et al. (2021) RoFormer (RoPE)", "Eq. 6 · Table 1 / Eq. 11 · Fig. 1 · Eq. 16"]],
             notes="처음부터 모든 실험을 읽지 말고 오른쪽 절과 그림만 먼저 읽는다. EN-FR BLEU는 판본(v7 권장, v1–v4는 41.0)을 밝혀 인용. 출처: week6.md 각 논문 서지와 읽기 안내.")

d.handoff(["여섯 질문을 따라", "텐서 → MLP → CNN → RNN → Attention → **Transformer**", "원논문을 **절 단위로** 읽고 숫자를 검산"],
          ["생성은 여전히 **순차적** (§7)", "긴 문맥의 **KV cache · IO** 비용", "warm-up · 정규화 위치 같은 **학습 안정성**", "patch · latent — **새 modality**"],
          ["**관심 분야의 논문 하나를 골라**", "원형 표에 꽂아 넣고", "무엇을 바꾸고 무엇을 남겼는지 **원문 표로** 설명해 보기"],
          notes="과정 마무리. 원형 Transformer를 입력부터 출력까지 설명할 수 있는지 스스로 확인한 다음, 관심 분야(언어 생성 → GPT 계열과 KV cache, 시각 → ViT, 효율 → FlashAttention·GQA, 생성 모델 → DiT)의 논문 하나를 골라 같은 방법으로 읽는다. "
                "출처: Vaswani (2017) §7(향후 과제); Pope (2022) §2; Xiong (2020); ViT; DiT.")

d.save(OUT)
print("saved", OUT, d.n + 2, "slides")
