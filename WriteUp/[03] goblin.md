---
title: LOS - 3번 goblin
category: Lord of SQL Injection
---

# [03] goblin



## 문제
 
<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbOraUh%2FbtrmXVcejj5%2F3I9yWj1qgD6rc10jlu7up1%2Fimg.png">

## 풀이

preg_match를 살펴보면, 쿼터를 필터링해주고 있음을 알 수 있다.

sql 삽입 시 쿼터를 사용하지 않는 우회 방법을 택해주어야 한다.

<br> 

쿼리문을 보겠다.


```php
$query = "select id from prob_goblin where id='guest' and no={$_GET[no]}"
```


id가 guest인 동시에 no 조건을 충족하는 레코드를 뽑아옴을 알 수 있다.

<br> 

no의 정체를 알기 위해 no=1을 시도해봤다.

아래처럼 guest 레코드가 정상 fetch된다.


<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fm5HY2%2FbtrmXQvmgHa%2FiHSOnMqxXyv3cAakDmRkX1%2Fimg.png">

<br> 

다음으로는 no=2를 시도해봤다.

아래처럼 아무 결과도 뜨지 않는다.

 
<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbD9Kvn%2FbtrmY4M9J88%2FlJ6KT2HxAVcksmLvnM3CtK%2Fimg.png">


따라서 guest 레코드의 no는 1임을 짐작할 수 있다.

<br> 

이 문제를 풀기 위해서는, 논리연산자의 특성을 이용하여 조건절 실행의 우선순위를 조정해주어야한다.

<br>

즉, 다음과 같은 형태의 쿼리문을 만들어줄 것이다.


```php
$query = "select id from prob_goblin where (id='guest' and no=2) or id='admin'"
```


where 조건절을 살펴보면,


**① id='guest' and no=2** ⇒ FALSE

**② id='admin'** ⇒ id가 admin인 레코드


**① or ②** 의 결과, id가 admin인 레코드를 뽑아오게 된다.

<br> 

이 때,

해당 문제에서는 쿼터가 필터링되고 있으므로 이를 우회하는 방식으로 sql을 삽입해주어야한다.

필터링 우회를 위해 char()을 이용하여 파라미터를 ASCII코드로 전달해준다.

<br> 

admin은 ASCII코드로 다음과 같이 나타낼 수 있다.
 

```
char(97,100,109,105,110)
```

<br> 

따라서, 최종 주입할 쿼리문은 다음과 같다.


```
no=2 or id=char(97,100,109,105,110)
```

## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FkFWfL%2FbtrmZHKXDOx%2FnPOH3JO9jIMagUxtB7RZG0%2Fimg.png">