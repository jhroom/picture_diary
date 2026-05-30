# Day 1 self1 개발 기록

- 배운 점: .env에 API 키를 넣고 load_dotenv()로 읽으면 코드에 키를 직접 쓰지 않아도 된다.
- 막힌 점: api 파라미터값 특정 model이 deprecated됨에 따라 다른 모델 선택과 해당 가이드를 따라가는 점
- 내일 시도할 것: 에러로그만으로 어디가 문제인지 파악하는 연습


## Day 1 self2 시작 전 관찰
- 마음에 든 부분:배경이나 전체적인 사물 배치
- 바꾸고 싶은 부분: 앵글 구도 날씨

## 응답 구조 비교 메모
- gpt-image-2: response.data[0].b64_json    점 표기법
- fal.ai: result["images"][0]["url"]        딕셔너리 키 표기법


## Day 1 self2 기록
추가 프롬프트: 핵심 키워들을 구상하고 들어가는것이 좋아보인다


WS 이미지는 배경이 전체적으로 보여서 시원한 느낌이 났어요.
CU 이미지는 인물들 이 크게 보여서 사람 중심적 느낌이 났어요.


## Day 2 self1 기록
- 오늘 만든 파일: scene_draft.md, day2_self1.py
- 장면 1:
- 장면 2:
- 장면 3:
- 장면 4:
- 가장 어려웠던 선택:
- 다음 self2에서 확인할 것:

## Day 4 self1

- 동기 호출은 결과를 바로 기다리고, 비동기 호출은 task_id를 받아 나중에 status/result로 확인한다.
- 가드레일 반복 횟수, 대기 시간, 완료 조건, 비용 상한을 제한해 무한 대기와 비용 초과를 막는다.

## Day 4 self2

Kling은 submit 직후 URL을 주지 않아 status 상태값으로 result얻기

picture_diary_pipeline는 scene→image→video→results 흐름을 
하나로 호출하는 인터페이스