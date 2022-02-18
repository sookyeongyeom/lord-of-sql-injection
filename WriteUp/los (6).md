---
title: LOS - 6번 darkelf
category: Lord of SQL Injection
---

# [06] darkelf

## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fc57h7M%2FbtrndHKZSPe%2FqqHttLfywOqUKhF01uSGeK%2Fimg.png">

## 풀이

solve 조건은 이전 문제와 동일하다.

<br>

이번 문제에서는 파라미터에 or이나 and이 포함되어있을 시 접근을 제한하고 있음을 알 수 있다.

즉, 논리연산자 필터링을 우회하는 문제이다. 

<br>

**or/and 논리연산자 필터링 우회**를 위한 적절한 대체 문자의 예시는 다음과 같다.

1. or : \|\|

2. and : &&, %26%26

<br>

따라서, 주입해야할 쿼리문인 `' or id='admin` 에 우회 문자를 적용한 최종 쿼리문은 다음과 같다.


``` 
' || id='admin
```

## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcL53rR%2Fbtrnc29W1l5%2FHqGm774OVFP2iiyoFqLefK%2Fimg.png">