---
title: LOS - 14번 giant
category: Lord of SQL Injection
---

# [14] giant

## 문제
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdUYN3Y%2FbtrnqxuuFgS%2FyhucoKCdPDfUVNysV516gk%2Fimg.png">

## 풀이

이전과는 조금 다른 형태다.

처음 보고는 이게 뭐지 싶었지만...

where 1 == TRUE 임을 알고 나니 감이 왔다.


<br>
 

from과 prob_giant 사이에 공백을 삽입하여 올바른 쿼리로 만들어주면 풀리는 문제인 것 같다.


<br>


다만, preg_match를 살펴보면

공백 및 자주 쓰이는 공백 우회 문자들을 필터링하고 있기 때문에

해당 문자들을 제외한 우회 문자를 적용해줘야 할 것 같다.

그 예로는 %0b, %0c 등이 있다.

<br> 

한편, strlen은 해당 문자열의 Byte 크기를 반환하는 함수이다.

공백은 1Byte이기 때문에 해당 함수에 걸러질 일은 없을 것이다. 

<br> 

입력할 문자열은 `%0b` 이다.

## 결과
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbiLSyp%2FbtrnpOpKbYH%2F8pf6dmo4lCjTodP4pSKjKk%2Fimg.png">