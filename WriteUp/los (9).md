---
title: LOS - 9번 vampire
date: 21-12-07 08:00:00 + 0900
category: Lord of SQL Injection
---

# [09] vampire

## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fpfg0X%2FbtrnfATFU5P%2FkQQttq6zigzehOSATX7rWK%2Fimg.png">

## 풀이

새로운 함수들이 눈에 띈다.

<br>

천천히 살펴보면,

① 싱글쿼터 필터링

② 문자열을 소문자로 변환

③ admin 문자열 삭제


를 적용하고 있음을 확인할 수 있다.

<br>

adadminmin을 입력해주면 중간에 있는 admin이 필터에 걸려 삭제되고,

최종적으로 남는 문자열은 결국 admin이 될 것 같다.

<br>

입력할 문자열은 `adadminmin` 이다.


## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FxFUAJ%2FbtrnhCjkWkU%2FL8tJShyTGyz5Cd1CQbrAf0%2Fimg.png">