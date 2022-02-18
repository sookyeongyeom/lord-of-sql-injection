---
title: LOS - 1번 gremlin
category: Lord of SQL Injection
---

# [01] gremlin
 
## 문제

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdhlchW%2Fbtrjk4pXRje%2FZVxs9xt5bWbNtRrhnkvfM0%2Fimg.png">

## 풀이

첫 줄부터 내려오다보면 낯선 함수가 보인다.

<br>

**preg_match()** 란?

인자로 전달받은 정규 표현식과 일치하는 패턴을 검색하는 php의 함수이다.

<br>

**정규 표현식**이란?

문자열을 바탕으로 검색을 수행하여 패턴과 일치하는지 조사하고, 분할하는 문자열 처리 방법이다.

<br>
 

말이 어렵지만 결국

preg_match() 함수에 인자로 들어오는 정규식 표현을 토대로

검색 대상 문자열을 싹 다 훑어서 해당 정규식 표현과 일치하는 패턴을 찾아낸다는 말이다.

<br>

preg_match() 는 세가지 인자를 받는다.

1. 정규식 표현

2. 검색 대상 문자열

3. 매칭된 값을 배열로 저장하고 싶을 시, 배열의 변수

<br>

따라서 다음과 같은 모양이다.

 
```php
preg_match('/정규식표현/', '검색대상문자열', '배열변수')
```

 
```php
preg_match($pattern, $subject, $matches)
```


$pattern 부분에 정규식 표현을 작성하고,

$subject 부분에 검색 대상 문자열을 알려주고,

매칭된 값을 따로 배열에 저장하고 싶다면 $matches 를 적어주면 되는 것이다.

<br>

이제 다시 문제로 돌아가보면 다음 코드가 의미하는 바를 알 수 있다.

 
```php
preg_match('/prob|_|\.|\(\)/i', $_GET[id])
```

GET으로 받은 id 값을 대상으로,

1. /prob

2. _

3. .

4. (

5. )

위 다섯가지 표현을 검색한다는 것이다.

- 참고로 preg_match() 함수는 검색 결과가 있을 시 1을, 없을 시 0을 반환한다.

<br>

여기까지 오면 아래 코드도 이해가 된다.

 
```php
if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~");
```


결국 이 한 줄이 의미하는 바는,

GET으로 받은 id 값을 대상으로 다섯가지 표현을 검색한 후,

매칭되는 패턴이 존재하면 exit 된다는 뜻이다.

- pw 값에도 같은 필터링 규칙이 적용된다.

<br>

이제 그 아랫줄을 보겠다.

 
```php
$query = "select id from prob_gremlin where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
$result = @mysqli_fetch_array(mysqli_query($db,$query));
```


GET으로 전달받은 id와 pw가 동시에 일치하는 레코드의 id 값을 갖고 오겠다는 것이다.

<br>

이해에 무리가 없으니 그 아랫줄로 넘어가겠다.


 
```php
if($result['id']) solve("gremlin");
```

아까 fetch해준 $result에 id 값이 정상적으로 존재하면 문제가 풀린다는 것을 알 수 있다.

<br>

지금까지의 분석을 통해,

WHERE절 뒷부분을 True로 만들어 조건을 충족시켜주는 것으로 해결 가능한 예제임을 알 수 있다.

<br>

쿼리문을 다시 한번 보겠다.


 
```php
"select id from prob_gremlin where id='{$_GET[id]}' and pw='{$_GET[pw]}'"
```

<br>

GET으로 넘길 id 값에 **' or 1 = 1 #** 을 입력해주면 최종 쿼리문은 다음과 같이 완성된다.


 
```php
"select id from prob_gremlin where id='' or 1 = 1 # ' and pw='{$_GET[pw]}'"
```


결과적으로 조건절이 참이 되며

prob_gremlin의 모든 id를 요청하게 된다.

그렇게 되면 $result['id']에는 prob_gremlin 첫 행의 id 값이 담기게 되고, 문제는 풀리게 된다.

- mysqli_fetch_array 함수의 특성상 한번의 콜에 하나의 행만 가져올 수 있기 때문이다.

<br>

자, 그럼 처음에 언급했듯, **' or 1 = 1 #** 을 url 뒤에 붙여준다.



```
' or 1 = 1 #
```


엔터 쳐보면... 안 풀린다.

<br>

url에 직접 값을 붙여줄때는

url encoding을 거쳐줘야하기 때문이다.

<br>

#은 인코딩했을 때 %23 이다.

자주 쓰기 때문에 외워두면 좋고,

구글링하면 나오는 url encoder를 사용해도 된다.

<br>

그럼 다시 입력해보자.



```
' or 1 = 1 %23
```



## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FHUeaf%2Fbtrjl9K2MmS%2FJyn1v5KS43aJwbdsrJ6d6K%2Fimg.png">