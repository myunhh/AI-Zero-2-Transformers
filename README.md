# AI Zero 2 Transformer — 6주 강의자료

원자료 `AI Zero 2 Transformer` (HTML)로 만든 6회차 강의자료입니다. 디자인은 Apple 디자인 원칙(넓은 여백, 절제, 한 가지 강조색, 글자 위계)을 따른 자체 템플릿입니다.
Transformer 이전 4주 + Transformer 2주, 원자료의 **여섯 질문**을 따라 시간순으로 진행합니다.

| 주차 | 파일 | 중심 질문 | 이번 주의 논문 |
|---|---|---|---|
| 1 | `lectures/week01_tensor_and_learning.pptx` (58장) | 규칙을 다 쓰지 않고 배울 수 있을까? | McCulloch & Pitts 1943 · Turing 1950 · Dartmouth 1955 · Widrow & Hoff 1960 · Cauchy 1847 · Robbins & Monro 1951 |
| 2 | `lectures/week02_perceptron_to_mlp.pptx` (58장) | 직선으로 안 되는 문제는? | Rosenblatt 1958/1962 · Novikoff 1962 · Minsky & Papert 1969 · Cybenko/Hornik 1989 · Rumelhart·Hinton·Williams 1986 · Bridle 1990 |
| 3 | `lectures/week03_cnn_and_deep_learning.pptx` (63장) | 공간 구조와 깊은 학습은? | Fukushima 1980 · LeCun 1989/1998 · Cortes & Vapnik 1995 · Hinton 2006 · Glorot & Bengio 2010 · AlexNet 2012 · VGG 2014 · BatchNorm 2015 · ResNet 2015 · LayerNorm 2016 |
| 4 | `lectures/week04_rnn_lstm_seq2seq.pptx` (57장) | 먼 정보를 어떻게 기억할까? | Sennrich 2016 · Elman 1990 · Bengio 1994 · Pascanu 2013 · LSTM 1997 · Gers 2000 · Bengio 2003 · Word2Vec 2013 · Cho 2014a/b · Sutskever 2014 |
| 5 | `lectures/week05_attention.pptx` (63장) | 원문을 다시 찾아보면? | Bahdanau 2014 · Luong 2015 · Cheng/Parikh 2016 · ConvS2S 2017 · Vaswani 2017 §3.2·3.5·4 · Jain & Wallace / Wiegreffe & Pinter 2019 |
| 6 | `lectures/week06_transformer_complete.pptx` (55장) | 참조만으로 만들면? | Vaswani 2017 §3·5·6 · Adam · Label smoothing · Xiong 2020 · MQA/GQA · FlashAttention · Pope 2022 · GPT-1 · BERT · T5 · ViT · DiT · GLU · RoPE |

매 주 구성: 이번 주의 질문 → 지난 주에서 이번 주로 → 오늘의 지도 → 이번 주의 논문 → 새 용어 → Part별 논문 한 편씩 (논문 카드 → 문제 → 아이디어·식 → 손계산 → 원문의 실험·결과 → 한계와 다음 논문) → 요약 · 셀프 체크(정답은 발표자 노트) · 흔한 오해 · 과제 · 참고 자료 → 남은 문제와 다음 질문.
모든 본문 슬라이드에 발표자 노트가 있고, 노트마다 숫자·식의 출처(논문 §·Table·Figure)를 적었습니다. 논문 노트는 `build/research/papers/week1.md`~`week6.md`에 있습니다.

## 다시 만들기

```bash
pip install python-pptx matplotlib numpy pillow
cd build
python regen_figs.py   # 그림 다시 그리기 (선택)
python week1.py        # … week6.py → lectures/*.pptx
```

- `build/deckkit.py` — 슬라이드 빌더. 각 주차 스크립트는 `deckkit.use_theme("clean")` + `Deck(..., theme="clean")`으로 `build/clean-template.pptx`(표지 · 본문 · 구역 레이아웃)를 씁니다. 표지/푸터의 과정명은 `EVENT` 상수로 바꿀 수 있습니다.
- `build/make_clean_template.py` — `clean-template.pptx`를 만드는 스크립트 (기존 AICA 템플릿 `Lab-template.pptx`는 `theme="aica"`로 여전히 쓸 수 있음)
- `build/CURRICULUM.md` — 주차별 논문·Part 구성과 바로잡은 통념
- `build/research/papers/` — 주차별 논문 노트(원문 확인, 출처 포함)와 조사·제작 지침
- `build/paper_figs_wN.py` — 논문 그림·표를 도식으로 새로 그리는 스크립트
- `build/assets/weekN/` — 그림 (생성 스크립트: `figs_w1.py`, `week1_assets.py`, `week2_figs.py`, `week3_figs.py`, `assets/week4/make_figs.py`, `week5_assets.py`, `week6_figs.py`)
- `build/qa_grid.py` — LibreOffice로 렌더링해 검토용 이미지를 만드는 도구
