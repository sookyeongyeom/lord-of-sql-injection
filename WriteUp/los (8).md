---
title: LOS - 8번 troll
date: 21-12-07 07:00:00 + 0900
category: Lord of SQL Injection
---

# [08] troll

## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FHCbch%2FbtrniUKNlLO%2FDWX4UNhEnqbcdCEfBcFvz0%2Fimg.png">

## 풀이

preg_match를 살펴보면, 싱글쿼터와 admin 문자열을 필터링하고 있음을 알 수 있다.

<br>

preg_match() 내부를 살펴보면,

패턴임을 명시하기 위해 해당 부분을 슬래시(/)로 감싸놓았다.

마지막 슬래시 뒤에는 옵션을 줄 수 있는데, i는 대소문자 구분을 하지 않음을 의미한다.

지금까지의 문제들은 항상 옵션으로 i가 적용되어 있었다.

<br>

그러나 이번 문제의 admin 필터를 보면, 마지막 슬래시 뒤에 옵션이 붙어있지 않음을 알 수 있다.

이는 해당 함수가 오로지 소문자 admin만을 필터링하고 있음을 말한다.

<br>

즉, Admin이나 ADMIN이나 AdMiN 등은 전혀 거르지 않고 있다는 것이다.

<br>

Sql은 대소문자 구분을 하지 않기 때문에, admin이나 ADMIN이나 같은 문자열로 인식한다.

<br>

따라서, 이번 문제의 답은 그냥 `Admin` 이다.

## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FT8aGN%2FbtrndIdwgyw%2FehtcSS79WvqUlN2lkhpvM1%2Fimg.png">