# AI Zero 2 Transformer — 6주 강의자료

원자료 `AI Zero 2 Transformer` (HTML)를 AICA Lab 템플릿으로 만든 6회차 강의자료입니다.
Transformer 이전 4주 + Transformer 2주, 원자료의 **여섯 질문**을 따라 시간순으로 진행합니다.

| 주차 | 파일 | 중심 질문 | 내용 |
|---|---|---|---|
| 1 | `lectures/week01_tensor_and_learning.pptx` | 규칙을 다 쓰지 않고 배울 수 있을까? | Tensor · shape · 내적 · 행렬곱 → 선형 모델 · MSE → 경사하강법 → 일반화 |
| 2 | `lectures/week02_perceptron_to_mlp.pptx` | 직선으로 안 되는 문제는? | Perceptron(1958) → XOR(1969) → MLP · 활성화 → 역전파(1986) → Softmax · Cross-entropy |
| 3 | `lectures/week03_cnn_and_deep_learning.pptx` | 공간 구조와 깊은 학습은? | CNN · 출력 크기 · 파라미터 → SVM → AlexNet의 조건 → ResNet · BatchNorm/LayerNorm |
| 4 | `lectures/week04_rnn_lstm_seq2seq.pptx` | 먼 정보를 어떻게 기억할까? | 토큰 · 임베딩 → RNN → 기울기 소실 → LSTM → 언어 모델 · Word2Vec → Seq2Seq 병목 |
| 5 | `lectures/week05_attention.pptx` | 원문을 다시 찾아보면? | Attention(2014) → Self-attention · Q/K/V → Scaled dot-product 손계산 → Multi-head → 위치 인코딩 |
| 6 | `lectures/week06_transformer_complete.pptx` | 참조만으로 만들면? | FFN · Residual · LayerNorm → Mask · Teacher forcing → 학습 → 생성 · KV Cache · 비용 → 실험 → 이후 |

매 주 구성: 이번 주의 질문 → 지난 주에서 이번 주로 → 오늘의 지도 → 새 용어 → Part별 (문제 → 아이디어 → 계산 → 검증) → 요약 · 셀프 체크(정답은 발표자 노트) · 흔한 오해 · 과제 · 참고 자료 → 남은 문제와 다음 질문.
모든 본문 슬라이드에 발표자 노트가 있습니다.

## 다시 만들기

```bash
pip install python-pptx matplotlib numpy pillow
cd build
python week1.py   # … week6.py → lectures/*.pptx
```

- `build/deckkit.py` — 템플릿(`build/Lab-template.pptx`)의 표지 · 구역 · Title and Content · 마지막 슬라이드와 본문 개체 틀을 그대로 쓰는 빌더. 표지/푸터의 행사명은 `EVENT` 상수로 바꿀 수 있습니다.
- `build/CURRICULUM.md` — 흐름 설계와 원자료 장 → 주차 대응표
- `build/assets/weekN/` — 그림 (생성 스크립트: `figs_w1.py`, `week1_assets.py`, `week2_figs.py`, `week3_figs.py`, `assets/week4/make_figs.py`, `week5_assets.py`, `week6_figs.py`)
- `build/qa_grid.py` — LibreOffice로 렌더링해 검토용 이미지를 만드는 도구
