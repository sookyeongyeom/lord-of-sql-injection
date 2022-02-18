---
title: LOS - 2번 cobolt
category: Lord of SQL Injection
---

# [02] cobolt

 
## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FqnNjN%2FbtrjsqeGG4f%2FTEkHdaKEKRqA0PYzb7foH0%2Fimg.png">
 
## 풀이

저번 문제에서 이미 다뤘던 preg_match()가 반겨준다.

필터링 부분에서 달라진 점은 없다.

이번에도 역시 필터링 문제는 없을 것 같다.

<br> 

그 아래 쿼리문을 보겠다.


```php
$query = "select id from prob_cobolt where id='{$_GET[id]}' and pw=md5('{$_GET[pw]}')";
$result = @mysqli_fetch_array(mysqli_query($db,$query));
```

prob_cobolt에 저장된 사용자의 비밀번호는 해싱되어있다는 것을 유추할 수 있다.

id 값과 pw 값의 해시값이 동시에 일치하는 레코드의 id를 뽑아오는 구조다.

<br>

일단 아래로 넘어간다.


```php
if($result['id'] == 'admin') solve("cobolt");
elseif($result['id']) echo "<h2>Hello {$result['id']}<br>You are not admin :(</h2>";
```


뽑아온 id 값이 admin인 경우에만 문제가 풀린다는 것을 알 수 있다.

<br> 

위에서 pw의 해시값을 쓰는 것을 보고 잠깐 멈칫했으나,

어차피 #을 필터링하고 있지 않기 때문에 아이디 뒷부분을 주석 처리해주면 간단히 풀릴 것 같다.

<br> 

```
admin' #
```


를 입력하면 될 것 같은데,

저번 문제에서 언급했다시피 #은 %23으로 대체해서 입력해준다.

<br>

```
admin' %23
```

## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdAiB1m%2Fbtrjr2ZiWeS%2FkDomTKTWUsRQq72lYuZUAK%2Fimg.png">