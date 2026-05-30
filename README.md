# 글로 쓰는 그림일기 — Picture Diary
일기 텍스트으로 4장면 이미지와 영상으로 변환하는 LLM 파이프라인

## 빠른 시작
```bash
uv venv && uv pip install -r requirements.txt
# .env에 OPENAI_API_KEY와 FAL_KEY 추가 후 실행
python pipeline.py
```

## 결과 미리보기
![scene_1](outputs/2026-05-30/travel_1.png))

## 운영 지표
| Day | 주요 작업 | 호출 수 | 단가 또는 추정 단가 | 합계 |
|---|---|---:|---:|---:|
| Day 1 | 환경 확인과 첫 호출 | 2 | $0.10 | $0.20 |
| Day 2 | 장면 JSON 생성 | 4 | $0.13 | $0.50 |
| Day 3 | 이미지 생성 | 4 | $0.20 | $0.80 |
| Day 4 | 영상 생성 | 2 | $0.50 | $1.00 |
| Day 5 | 도메인 A/B 테스트 | 6 | $0.08 | $0.50 |
| 합계 |  | 18 |  | $3.00 |

## A/B 테스트 요약
| 항목 | A | B |
|---|---|---|
| 시드 | 42 | 137 |
| P95 지연시간 | 1.71 s | 0.61 s |

B가 A 대비 P95 지연시간 약 **2.8배 빠름** (도메인: travel)

## 도메인 응용
<!-- # 여기에 Day 5 self1에서 선택한 도메인 결과를 채워요 -->

## 파일 구조
```
picture_diary/
├── README.md
├── .gitignore
├── week7_retrospective.md
├── pipeline.py
├── agents/
│   ├── scene.py
│   ├── image.py
│   └── video.py
├── cost_report.md
├── ab_test_results.json
├── domains/
│   └── travle_prompts.json
└── outputs/
    └── (이미지·영상 샘플)
```

## 라이선스
MIT
