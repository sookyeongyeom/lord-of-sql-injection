---
title: LOS - 31번 zombie
category: Lord of SQL Injection
---

# [31] zombie

## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbvYFVh%2FbtrpvS5twXG%2F4yglcpJkyzRcyyqQg3UKb0%2Fimg.png">

## 풀이

필터링을 제외하면 이전 문제와 완전히 동일하다.

다만, 문자열 ace를 필터링하여 replace를 사용하지 못하게 막고 있기 때문에 Quine을 구현할 수 있는 다른 방법이 필요하다.

<br>

이와 관련해서 MySql Quine에 대해서 찾아본 결과,

MySql에서만 사용할 수 있는 또 다른 구현 방법이 있음을 알게 되었다.

<br>

바로 **information_schema.processlist** 테이블의 **info** 컬럼에 **현재 실행중인 쿼리**가 담긴다는 점을 이용하는 것이다.

마침 이번 문제에서는 \_와 .를 필터링하고 있지 않기 때문에 올바른 접근이라는 예감이 들었다.

<br>

주입할 쿼리문은 다음과 같다.

```
1' union select substr(info,locate('1',info),length(info)-locate('1',info)) from information_schema.processlist %23
```

## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FLVJ7E%2Fbtrpu1ViyFr%2FvfYKBMTbclaTqnOJkAjWi0%2Fimg.png">