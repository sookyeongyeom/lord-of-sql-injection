---
title: LOS - 29번 phantom
category: Lord of SQL Injection
---

# [29] phantom

## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fzr5Q9%2FbtrpdnYOpmd%2FUYAy063HqOaz1BC4eWUew0%2Fimg.png">

## 풀이

no=1 레코드의 email을 찾는 문제이다.

<br>

먼저, 준비된 쿼리문을 보겠다.

```php
$query = "insert into prob_phantom values(0,'{$_SERVER[REMOTE_ADDR]}','{$_GET[joinmail]}')";
```

쿼리문으로부터 추측할 수 있는 바는 다음과 같다.

1. 첫 컬럼의 데이터로 0이 들어가는 것으로 보아, no는 AUTO_INCREMENT PRIMARY KEY로 추정할 수 있다.

2. 접속한 ip와 joinmail을 매칭하여 저장함을 알 수 있다.

<br>

다음은 표가 출력되는 과정을 보겠다.

```php
$rows = mysqli_query($db,"select no,ip,email from prob_phantom where no=1 or ip='{$_SERVER[REMOTE_ADDR]}'");
echo "<table border=1><tr><th>ip</th><th>email</th></tr>";
while(($result = mysqli_fetch_array($rows))){
if($result['no'] == 1) $result['email'] = "**************";
echo "<tr><td>{$result[ip]}</td><td>".htmlentities($result[email])."</td></tr>";
}
echo "</table>";
```

1. no=1이거나, ip=[접속한 ip] 인 레코드를 표로 출력한다.

2. no=1인 경우, email을 \*\*\*\*\*\*\*\*\*\*\*\*\*\*로 바꾸어 표시한다.

<br>

목표는 no=1의 email을 알아내는 것이기에, 접근 방법을 고민해봤다.

preg_match를 보면 duplicate를 필터링하고 있는데, 이는 ON DUPLICATE UPDATE를 걸러내고자 하는 듯 했다.

ON DUPLICATE UPDATE는 PRIMARY KEY가 중복되는 레코드가 들어갈 시 기존의 레코드를 삭제하고 새로운 레코드가 그 자리를 대체하게끔 하는 구문이다.

만약 이 구문을 필터링하고 있지 않았다면, no=1인 새로운 레코드를 넣음으로써 문제를 간단히 해결할 수 있었을 것이다.

그래서 중복 레코드를 관리하는 다른 방법에 대해서도 찾아봤는데, 이 상황에서 쓸 수 있을 만한 방법은 보이지 않았다.

- ex) INSERT IGNORE, REPLACE INTO

<br>

따라서 여러개의 레코드를 동시에 INSERT하는 방법을 생각했다.

이는 다음과 같이 VALUES 뒤에 괄호로 묶인 여러개의 레코드를 나열함으로써 수행 가능하다.

```sql
INSERT INTO [테이블명] VALUES(1, 1, 1), (2, 2, 2), (3, 3, 3);
```

<br>

이후의 풀이 과정은 다음과 같다.

<br>

[1] 여러 개 INSERT + 서브쿼리 확인

```
?joinmail=choco'), (0, '[접속한 ip]', (select 1 where 1=1)) %23
```

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FWWusj%2FbtrpcOvEW0j%2FCKRrL1LG8KK45BCRzku1s1%2Fimg.png">

정상적으로 실행되어 choco와 1이 INSERT 된 것을 확인할 수 있다.

서브쿼리가 먹히는 것을 확인했으니, 그 자리에 no=1의 email을 넣어주면 **************로 바뀌기 전의 진짜 email을 쉽게 확인할 수 있을 것 같았다.

<br>

[2] 서브쿼리에 원하는 작업 적용해보기

```
?joinmail=choco'), (0, '[접속한 ip]', (select email from prob_phantom where no=1)) %23
```

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcPyesx%2Fbtrpjw8kHkz%2FhtWK7skuvlKMQKtwDffWb0%2Fimg.png">

음... 안된다.

Syntax가 잘못되었나 싶어서 별의 별 베리에이션을 다 시도해봤지만 하나같이 다... 안됐다.

1=1, 1=2 등의 기본적인 조건이 적용된 서브쿼리는 문제없이 실행되었지만, prob_phantom 테이블안의 기존 레코드에 접근하려고 하기만 하면 아무 반응도 볼 수가 없었다.

한참 고통받다가... 문득 의심이 들었다.

동일 테이블 안의 레코드에는 일반적인 서브쿼리로 접근할 수 없나?

- [[SQL] 동일(같은) 테이블 서브쿼리](https://do-hansung.tistory.com/9)

그것이 맞았다...

그래서 페이로드를 아래와 같이 바꿔주었다.

<br>

[3] 최종 페이로드

```
?joinmail=choco'), (0, '[접속한 ip]', (select * from (select email from prob_phantom where no=1) as temp)) %23
```

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbGnBZW%2Fbtro8x2ffmQ%2FjoSP2d93AeOTRHD68HHL61%2Fimg.png">

결과적으로, no=1 레코드의 email은 `admin_secure_email@rubiya.kr` 임을 확인할 수 있었다.


## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbJxRyo%2FbtrpkuvB2eU%2FdKEOvRoSJ5Qb0r8Ydw1YI0%2Fimg.png">