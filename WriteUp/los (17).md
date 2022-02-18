---
title: LOS - 17번 assassin
category: Lord of SQL Injection
---

# [17] assassin

## 문제
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcaJoin%2Fbtrnv2nQH5t%2F6gwsXknWYq16dGaBl6TdQk%2Fimg.png">

## 풀이
처음 보는 함수가 나왔다.

<br>

strrev는 입력받은 문자열을 거꾸로 뒤집어서 반환하는 함수다.

strrev("hello") ⇒ olleh

이런 식이다.

<br>

주의할 점은, Byte 단위로 뒤집기 때문에 2Byte 문자인 한글이 들어가면 깨지게 된다는 점이다.

<br>

이번 문제에서는 여러번 접했었던 addslashes를 좀 더 정확히 볼 필요가 있을 것 같다.

addslashes는 **싱글쿼터, 더블쿼터, 역슬래시, Null Byte** 앞에 역슬래시를 붙여주는 함수다.

<br>

주어진 쿼리문을 보겠다.


```php
$query = "select id from prob_zombie_assassin where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
```

쿼리문 자체는 16번 문제와 다른 점이 없다.

16번에서는 id에 **역슬래시**, pw에 **or 1=1 %23** 을 주어 문제를 풀었었다.

<br>

이번 문제에서 새로 고려하여야하는 점은

① 역슬래시가 이스케이핑 될 것이라는 점과

② strrev에 의해 문자열이 거꾸로 읽힐 것이라는 점이다.

<br>

pw의 경우는 간단하다. 그냥 문자열을 거꾸로 입력해주면 된다.

- %23 1=1 ro

<br>

id가 이 문제의 포인트인데,

싱글쿼터, 더블쿼터, 역슬래시, Null Byte를 id의 페이로드로 주었을 때를 각각 살펴보겠다.

<br>

[1] 싱글쿼터 (id=<span style="background:aquamarine;">'</span>&pw=%23 1=1 ro)

addslashes ⇒ \\'

strrev ⇒ '\

최종 쿼리 ⇒ where id=''<span style="background:lightgrey">\\'</span> and pw='or 1=1 %23'

- 잘못된 접근이다. 싱글쿼터에 의해 id의 파라미터 부분이 바로 닫혀버린 후, \\'가 바깥에 남겨지므로 올바르지 않은 쿼리문이 만들어진다.

<br>

[2] 더블쿼터 (id=<span style="background:aquamarine;">"</span>&pw=%23 1=1 ro)

addslashes ⇒ \\"

strrev ⇒ "\

최종 쿼리 ⇒ where id='<span style="background:lightpink;">"\\' and pw=</span>'or 1=1 %23'

- 올바른 접근이다! 빨간색 부분이 통째로 id의 파라미터로 취급된다.

- FALSE or TRUE 이므로 문제가 풀릴 것이다.

- solve

<br>

[3] 역슬래시 (id=<span style="background:aquamarine;">\\</span>&pw=%23 1=1 ro)

addslashes ⇒ \\\\

strrev ⇒ \\\\

최종 쿼리 ⇒ where id='<span style="background:lightpink;">\\\\</span>' and pw='or 1=1 %23'

- 잘못된 접근이다. \\는 일반 문자 역슬래시로 취급되므로, 빨간색 부분이 id의 파라미터가 된다.

<br>

[4] Null Byte (id=<span style="background:aquamarine;">%00</span>&pw=%23 1=1 ro)

addslashes ⇒ \0 

strrev ⇒ 0\

최종 쿼리 ⇒ where id='<span style="background:lightpink;">0\\' and pw=</span>'or 1=1 %23'

- 올바른 접근이다! 빨간색 부분이 통째로 id의 파라미터로 취급된다.

- FALSE or TRUE 이므로 문제가 풀릴 것이다.

- solve

<br>

이상의 분석을 통해, 정답은 두 가지임을 확인했다.

 
```
id="&pw=%23 1=1 ro
```

```
id=%00&pw=%23 1=1 ro
```

## 결과
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbO4j8k%2Fbtrnv13x3ev%2FvuNs9qfwKd6dQJIrzqtXB0%2Fimg.png">