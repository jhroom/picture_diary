## Day별 핵심 산출물
| Day | 강의 트랙 | 셀프 트랙 | 실행 확인 |
|---|---|---|:---:|
| Day 1 | `main.py` (환경 확인 · 첫 호출) | `day1_self1.py` (DALL-E 첫 장면 호출)<br>`day1_self2.py` (앵글·구도 비교 생성) | ✅ |
| Day 2 | `agents/scene.py` (장면 추출 · 검증) | `day2_self1.py` (scene_draft.md 파싱)<br>`day2_self2.py` (scene_prompts.json 7필드 검증) | ✅ |
| Day 3 | `agents/image.py` (배치 이미지 생성) | `day3_self1.py` (scene.py 시범 호출)<br>`day3_self2.py` (4장면 배치 이미지 저장) | ✅ |
| Day 4 | `agents/video.py` + `guardrails.py` (Kling 비동기 · 가드레일) | `day4_self1.py` (Kling submit 1회)<br>`day4_self2.py` (상태 조회 · 결과 수신) | ✅ |
| Day 5 | `ab_test.py` + `final_check.py` (A/B 테스트 · 최종 점검) | `day5_self1.py` (travel 도메인 A/B 실행) | ✅ |

## 잘 된 점
scene → image → video → A/B 테스트까지 5일 안에 전체 파이프라인을 완성했다.

## 개선할 점
처음 기반을 잘 쌓아 나중에 에러가 났을때 쉽게 대처하기

## GitHub 저장소
https://github.com/jhroom/picture_diary