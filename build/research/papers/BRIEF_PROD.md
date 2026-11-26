# 논문 기반 주차 자료 재생성 지침 (주차별 제작 에이전트 공통)

입력: `build/research/papers/weekN.md`(검증된 논문 노트), 현재 `build/weekN.py`, `build/deckkit.py`(API).
출력: 새 `build/weekN.py`(+ 필요하면 새 그림 스크립트 `build/paper_figs_wN.py`), 빌드된 `lectures/weekNN_*.pptx`.

## 바꾸지 말 것
- 디자인: Apple 디자인 원칙 테마. 스크립트 맨 위의 `deckkit.use_theme("clean")` 와 `Deck(..., theme="clean")` 유지.
- 과정의 뼈대: 여섯 질문(이번 주 질문 → 다음 주 질문), 각 Part의 단계 태그(문제·아이디어·계산·검증·역사·코드·정리·실습 + 새로 `논문`·`결과`).
- 이미 검산된 손계산 예제와 좋은 그림은 버리지 말고 해당 논문의 '계산' 단계로 옮겨 쓴다.
- `build/deckkit.py`, `build/regen_figs.py`, 다른 주차 파일, README/CURRICULUM은 수정하지 않는다. 커밋하지 않는다.

## 새 구조 (논문 중심)
1. 도입: `d.question` → (2주차부터) `d.bridge` → `d.roadmap` → **`d.paper_map(rows)`**(이번 주 논문 지도) → `d.glossary`.
2. Part마다 논문 한 편(짧은 논문 두세 편은 한 Part로 묶어도 됨):
   `d.part` → **`d.paper(cite, title, venue, problem, idea, read, url=, result=)`** 카드 →
   문제(그 논문이 밝힌 앞선 방법의 한계) → 아이디어(핵심 구조) → 계산(논문 식 + 우리 표기, 작은 손계산) →
   결과/검증(논문이 보고한 실험 설정과 원문 표의 수치 — 표·차트로) → 한계와 다음 논문으로의 연결.
   논문이 아닌 도구 부분(예: 1주차 텐서·shape, PyTorch 코드)은 "도구" Part로 짧게 두고, 노트가 권하는 대로 솔직하게 표시한다.
3. 마무리: `d.summary` → `d.quiz`(정답은 노트) → `d.misconceptions`(노트의 '흔한 오해' 활용) →
   `d.homework`(논문 읽기 과제: 어떤 절/그림을 읽고 무엇을 제출하는지 분명하게) → `d.references`(논문 + 읽을 절) → `d.handoff`.
- 분량: 45–55장 정도(90분 강의). 처음 공부하는 사람이 따라올 수 있게 — 논문 용어는 처음 나올 때 풀어 쓴다.

## 사실 규칙
- 숫자·식·연도·저자·학회는 **노트에 출처와 함께 있는 것만** 쓴다. 노트에 [원문 미확인]이면 정확한 수치를 쓰지 않는다.
- 발표자 노트(`notes=`)에 출처를 적는다: 예) "출처: Widrow & Hoff (1960) Eq. 5, p. 98".
- 노트 끝의 '현재 자료와 원문이 어긋나는 곳'은 모두 반영한다.
- 논문 그림은 원본 이미지를 쓰지 않고 matplotlib 도식으로 새로 그린다. 그림 안이나 노트에 "원문 Fig. N 기반 재구성"이라고 밝힌다.

## 그림
- 새 그림은 `build/paper_figs_wN.py`에 둔다(독립 실행): 맨 위에서 `sys.path.insert(0, build)`, `import deckkit; deckkit.use_theme("clean")`,
  `from deckkit import mpl_setup, PALETTE_HEX as P`, 저장은 `build/assets/weekN/` 로. 색은 `P[...]`/`P.get(...)`만 쓴다
  (TEAL=파랑, TEAL2, MINT, MINT2, DARK, GRAY, ACCENT=주황, LINE, BG, MID, OFF, GRID, ACC_MID, CMAP).
- 글자는 슬라이드에서 읽히게 크게(축 라벨 13pt 이상 상당). 기존 그림은 `python regen_figs.py <그 주차 그림 스크립트>`로 다시 만들 수 있다.

## 검수 (반드시)
- `cd build && python weekN.py` — "!" 경고가 없어야 한다.
- `python qa_grid.py ../lectures/<파일>.pptx <scratchpad>/pN` 로 렌더링하고 **모든 슬라이드를 원본 크기로** 읽어
  겹침·잘림·푸터 침범(아래 ~0.55")·어색한 줄바꿈·빈 슬라이드를 고친다. 렌더러는 맑은 고딕 대신 나눔고딕을 쓴다(작은 줄바꿈 차이, 굵은 글씨의 "²"/"∂" 이상 글리프는 무시).
- 모든 본문 슬라이드에 발표자 노트가 있어야 한다.
- 마지막 보고: 새 슬라이드 목록(번호·제목·근거 논문), 반영한 정정 사항, 못 한 것.
