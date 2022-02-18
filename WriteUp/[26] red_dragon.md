---
title: LOS - 26번 red_dragon
category: Lord of SQL Injection
---

# [26] red_dragon

## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fbej7lT%2FbtroAJ1aT87%2Fla5GHQwr77I6tDsLeh3VmK%2Fimg.png">

## 풀이

1. 딱히 필터링 없음

2. id값이 7자 이내여야함

<br>
 
solve 조건은 admin 계정의 no를 알아내는 것이다.

<br>

주어진 쿼리문이다.

```php
$query = "select id from prob_red_dragon where id='{$_GET['id']}' and no={$no}";
```

이것만 보면 상당히 간단해보이는 문제다.

no를 맞춰주는 것이 목표이기 때문에, id값을 닫아주고 뒷부분을 주석으로 날려준 후 $no는 개행해주면 된다.

이전에 마주친 적이 있었던 것 같은 문제다.

<br>

이 경우의 페이로드 예시는 다음과 같다.

<br>

[1] id 페이로드

```
'||no=%23
```

- 딱 7자다.


[2] pw 페이로드

```
%0a[비교할숫자]
```

<br>

페이로드에 의해 변조된 쿼리문은 다음과 같아진다.

```php
$query = "select id from prob_red_dragon where id=''||no=#' and no=
	[비교할숫자]";
```

따라서, no=[비교할숫자] 일 시 Hello admin이 출력된다.

<br>

기다리다보면 나타나겠지의 심산으로

자동화 도구를 이용해 0부터 하나하나 올라가봤지만... 시간이 아무리 지나도 답을 뱉지 않았다.

이유를 고민해보니... 아무래도 엄청 큰 수인 것 같았다.

때문에 no의 대략적인 범위를 찾아내는 것으로 접근 방법을 바꿨다.

<br>

새로운 접근의 페이로드 예시는 다음과 같다.

<br>

[1] id 페이로드

```
'||no>%23
```

- = ⇒ >


[2] pw 페이로드

```
%0a[비교할숫자]
```

<br>


먼저, url에 직접 페이로드를 전달하여 대략적인 자릿수를 알아내고자 했다.


<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FIJI4g%2FbtroAz5o6kf%2FIpvCdO1UjJlYltPVXaMdIK%2Fimg.png">

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdGxzKr%2FbtroyGRurIT%2FVtSroCXNBk1JysBE4C9kBK%2Fimg.png">

그 결과...

찾고 있는 숫자가 무려 **500000000**대라는 이보다 대략적일 수 없는 정보를 얻었다.

이진탐색을 적용한다고 해도 터무니 없이 큰 숫자다.

별 수 없이 위에서부터 한자리씩 숫자를 바꿔가며 범위를 찾고 있자니...

상당히 찝찝했지만 이틀 밤을 샌 관계로 더 이상은 한계였다...

그냥 내려놓고 찾기로 했다.

<br>

한참을 찾은 끝에...


<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fb0yOFy%2FbtrowlAMm8d%2FFfkrMkaqKK6Ps7hhM30vCk%2Fimg.png">

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbPUEJm%2FbtrozxmseDG%2FrcS3dnaTermhqDfelYsRrk%2Fimg.png">

**586482013**에서는 뜨는 admin이

**586482014**에서는 뜨지 않는 것을 발견했다!

이로써 답은 `586482014`임을 확신할 수 있었다...

## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbpKA36%2FbtroABoB8eg%2FM4srRHqJHCs0LQ0XGxhL61%2Fimg.png">