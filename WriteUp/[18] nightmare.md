---
title: LOS - 18번 nightmare
category: Lord of SQL Injection
---

# [18] nightmare

## 문제
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F2bZtO%2FbtrnB7pSacd%2F4hRjKEvykh9qZCJrFF1x8K%2Fimg.png">

## 풀이

이번 문제에서는 #과 -를 추가로 필터링해주고 있다.

자주 사용되는 형식의 주석을 필터링하기위한 목적으로 보인다.

또한, strlen을 이용해 pw의 페이로드 길이를 6Byte 이하로 제한하고 있다.

<br>

주어진 쿼리문을 보겠다.

```php
$query = "select id from prob_nightmare where pw=('{$_GET[pw]}') and id!='admin'";
```

solve 조건은 아무 id나 fetch 해오는 것이다.

<br>

따라서, and를 기준으로


① pw=('{$_GET[pw]}') 까지를 True로 만들어주고

② and id!='admin' 부분을 날려주면 될 것 같다.


<br> 

②번의 경우에는, #과 --에 필터링이 걸려있으므로

**;%00**을 주석으로 사용해주면 된다.

- 참고로, 바로 앞 문자와 띄우지 않고 붙여서 써주어야 하는 것으로 보인다.

<br>

①번이 관건인데, 6글자 길이 제한 때문에 최대한 단순하게 True문을 만들어주어야 한다.

<br>

아무리 생각해도 적절한 방법이 떠오르지 않아서 구글링으로 힌트를 구했는데,

Sql에서 숫자 없이 문자로만 이루어진 문자열은 0으로 자동 형변환된다고 한다.

대표적인 예시로, **('')=0** 은 참이다.

<br>

이상의 분석을 통해, 입력할 답은 다음과 같다.

 
```
')=0;%00
```


## 결과
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FyX86N%2FbtrnGjo6fpG%2FWuxRqIuKMTkzcpfjB9dnx1%2Fimg.png">