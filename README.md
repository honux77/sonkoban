# MSX SONKOBAN

MSX BASIC으로 만든 간단한 소코반 게임입니다.

## 데모

**WebMSX에서 바로 플레이:**

https://webmsx.org/?MACHINE=MSX2P&BASIC_URL=https://raw.githubusercontent.com/honux77/sonkoban/main/sokoban.bas

> WebMSX가 열리면 자동으로 BASIC 파일을 로드하고 `RUN` 명령으로 실행하세요.

## 조작 방법

| 입력 | 동작 |
|------|------|
| 화살표 키 / 조이스틱 | 이동 |
| R / ESC / 조이스틱 버튼 | 스테이지 리셋 |
| 1 ~ 5 | 스테이지 선택 |
| CTRL+STOP | 종료 |

## 스테이지

| 스테이지 | 설명 |
|---------|------|
| 1 | 입문 (6×5) |
| 2 | 박스 2개 (7×7) |
| 3 | 순서가 중요 (7×6) |
| 4 | Begoon Map 1 (22×11) |
| 5 | Begoon Map 2 (14×10) |

## 실행 방법

1. [WebMSX](https://webmsx.org) 접속
2. `sokoban.bas` 파일을 드래그 앤 드롭하거나 위 데모 링크를 클릭
3. MSX BASIC 프롬프트에서 `RUN` 입력

또는 실제 MSX / 에뮬레이터에서 직접 로드할 수 있습니다.

## 개발 환경

- MSX BASIC (MSX1/MSX2 호환)
- SCREEN 1, 스프라이트 모드 2
- 8×8 타일 및 스프라이트 사용

## 참고 자료

- [Modern MSX BASIC Game Dev](https://github.com/plattysoft/Modern-MSX-BASIC-Game-Dev)
- [MSX Wiki - INKEY$](https://www.msx.org/wiki/INKEY$)
- [MSX Wiki - STICK()](https://www.msx.org/wiki/STICK)
- [MSX Wiki - STRIG()](https://www.msx.org/wiki/STRIG)
