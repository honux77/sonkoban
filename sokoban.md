# MSX BASIC SOKOBAN

## 참고자료

- https://github.com/plattysoft/Modern-MSX-BASIC-Game-Dev

## 키 입력 확인하기

https://www.msx.org/wiki/INKEY$

### 구현할 내용

화살표 키 - 이동
스페이스 - 되돌리기
F1 - 처음부터

keytest.bas로 누른 키의 아스키값 확인

```basic
5 REM MSX BASIC SPECIAL KEY CODE TEST
10 A$=INKEY$
30 PRINT "YOU PRESS ";ASC(A$)
40 IF A$="q" THEN END
50  GOTO 10
```

![](../images/keytest.png)

# 키코드 테이블

| 키 | 코드 |
|----|------|
| →  | 28   |
| ←  | 29   |
| ↑  | 30   |
| ↓  | 31   |
| 스페이스 | 32   |


## 8 * 8 스프라이트 그리기

https://www.msx.org/wiki/SPRITE$()

### 기본 그리기 예제

```
10 COLOR 15,1,7: SCREEN 2,0
20 B$=""
30 FOR I=0 TO 7: READ A: B$=B$+CHR$(A): NEXT
40 SPRITE$(0)=B$
50 PUT SPRITE 0, (100,100),15,0
60 A$=INPUT$(1)
70 SCREEN 1: PRINT SPRITE$(0)
80 DATA 24,60,126,255,36,36,66,129
```


### 이동시켜 보기

10 COLOR 15,1,7: SCREEN 2,0
20 B$=""
30 FOR I=0 TO 7: READ A: B$=B$+CHR$(A): NEXT
40 SPRITE$(0)=B$
45 X = 5, Y = 5
50 PUT SPRITE 0, (X,Y),15,0
55 X=X+1
IF X<>20 GOTO 50
60 A$=INPUT$(1)
70 SCREEN 1: PRINT SPRITE$(0)
80 DATA 24,60,126,255,36,36,66,129