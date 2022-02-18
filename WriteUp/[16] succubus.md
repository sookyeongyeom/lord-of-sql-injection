---
title: LOS - 16번 succubus
category: Lord of SQL Injection
---

# [16] succubus

## 문제
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdGYU25%2Fbtrns3nGHUj%2FzMxmr9YW2AVTAgWWcKELc1%2Fimg.png">

## 풀이

싱글쿼터 우회에는 두 가지 방법이 있다.

<br>

첫번째는 그냥 더블쿼터를 쓰는 것이다.

그러나 더블쿼터로는 서버측 쿼리문에 열려있는 싱글쿼터를 닫아줄 수가 없기 때문에 쿼리문을 원하는 방향으로 아예 틀어줄 수는 없다.

<br>

두번째는 아주 한정적인 상황에서만 쓸 수 있는 방법이다.

이번 문제처럼 두개 이상의 파라미터를 받고 있을 때, 그리고 둘 모두 싱글쿼터에 감싸져 있을 때만 사용할 수 있다.

그 내용은 다음과 같다.

<br>

id='  ' and pw='  '

id='<span style="color:red;">**\\**' and pw=</span>' or 1=1 %23 '


<br>

첫번째 파라미터로 **역슬래시(\\)**를 줘서 바로 뒤의 싱글쿼터를 일반 문자로 이스케이프 시켜주는 것이다.

그렇게 해주면 빨간색 부분이 통째로 id의 파라미터가 되어버린다.

<br>
 

그 후, 두번째 파라미터로 or 1=1 %23 을 주면 문제없이 첫번째 레코드를 뽑아올 수 있게 된다.

(∵ FALSE or TRUE ⇒ TRUE 가 되므로)

<br>
 

따라서, 입력할 답은 다음과 같다.

 
```
id=\&pw=or 1=1 %23
```

## 결과
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcAbgGU%2Fbtrnrj5t3IO%2FC3fP1RumEYKfRcKqmf6lNK%2Fimg.png">